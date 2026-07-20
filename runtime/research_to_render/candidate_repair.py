from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable, Mapping

from .candidate_generation import (
    CandidateGenerationError,
    _api_key_looks_placeholder,
    _extract_image_result,
    _provider_http_error,
    image_data_url,
    read_json,
    sha256_file,
    write_json,
)
from .candidate_validation import validate_candidates


class CandidateRepairError(RuntimeError):
    pass


def _candidate_record(candidate_manifest: Mapping[str, Any], candidate_id: str) -> dict[str, Any]:
    for item in candidate_manifest.get("candidates", []):
        if str(item.get("candidate_id")) == candidate_id:
            return dict(item)
    raise CandidateRepairError(f"Candidate {candidate_id} is missing from its candidate manifest.")


def _select_repair_target(validation_manifest: Mapping[str, Any]) -> dict[str, Any] | None:
    for item in validation_manifest.get("candidate_results", []):
        decision = str(item.get("machine_decision", ""))
        instructions = [
            str(value).strip()
            for value in item.get("repair_instructions", [])
            if str(value).strip()
        ]
        if decision in {"rejected", "needs_review"} and instructions:
            selected = dict(item)
            selected["repair_instructions"] = instructions
            return selected
    return None


def build_repair_prompt(
    generation_package: Mapping[str, Any],
    repair_instructions: list[str],
    *,
    attempt_number: int,
) -> str:
    if not repair_instructions:
        raise CandidateRepairError("A repair attempt requires at least one repair instruction.")
    instruction_block = "\n".join(
        f"{index}. {instruction}"
        for index, instruction in enumerate(repair_instructions, start=1)
    )
    return f"""Revise the SECOND attached image into a corrected technical illustration.

IMAGE ROLES
- FIRST image: authoritative reference and controlling evidence.
- SECOND image: previously generated candidate that failed validation.

ORIGINAL CONSTRAINT PACKAGE
{generation_package['compiled_prompt']}

VALIDATOR-DIRECTED REPAIRS — ATTEMPT {attempt_number}
{instruction_block}

REVISION RULES
- Apply every repair instruction exactly.
- Use the authoritative reference to resolve geometry, component count, size, position, and orientation.
- Preserve all portions of the previous candidate that already satisfy the original constraints.
- Do not redesign or restyle unrelated regions.
- Do not remove, crop, move, or obscure already-correct required features.
- Do not add words, labels, numbers, legends, dimensions, arrows, title blocks, or callout lines.
- Do not invent components or hidden geometry.
- Return one complete corrected base illustration only.

The result is still an unapproved candidate and will be independently revalidated."""


def build_repair_payload(
    generation_package: Mapping[str, Any],
    parent_candidate_path: Path,
    repair_instructions: list[str],
    *,
    attempt_number: int,
) -> dict[str, Any]:
    references = generation_package.get("reference_inputs", [])
    if len(references) != 1:
        raise CandidateRepairError(
            "The current repair worker requires exactly one controlling reference image."
        )
    reference = references[0]
    reference_path = Path(str(reference["local_file"]))
    if not reference_path.exists() or sha256_file(reference_path) != str(reference["sha256"]):
        raise CandidateRepairError(
            "The controlling reference image is missing or no longer matches the generation package."
        )
    if not parent_candidate_path.exists():
        raise CandidateRepairError(f"Parent candidate is missing: {parent_candidate_path}")

    return {
        "model": generation_package["provider"]["controller_model"],
        "store": False,
        "tools": [dict(generation_package["provider"]["image_tool"])],
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": build_repair_prompt(
                            generation_package,
                            repair_instructions,
                            attempt_number=attempt_number,
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data_url(reference_path),
                        "detail": str(generation_package["provider"]["input_image_detail"]),
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data_url(parent_candidate_path),
                        "detail": "high",
                    },
                ],
            }
        ],
    }


def generate_repaired_candidate(
    generation_package_path: Path,
    parent_candidate_manifest_path: Path,
    parent_validation_manifest_path: Path,
    output_root: Path,
    *,
    attempt_number: int,
    api_key: str | None = None,
    endpoint: str | None = None,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    generation_package_path = generation_package_path.resolve()
    parent_candidate_manifest_path = parent_candidate_manifest_path.resolve()
    parent_validation_manifest_path = parent_validation_manifest_path.resolve()
    generation_package = read_json(generation_package_path)
    candidate_manifest = read_json(parent_candidate_manifest_path)
    validation_manifest = read_json(parent_validation_manifest_path)

    if generation_package.get("status") != "ready_for_generation":
        raise CandidateRepairError("Generation package is not ready_for_generation.")
    if candidate_manifest.get("status") != "candidates_generated":
        raise CandidateRepairError("Parent candidate manifest is not in candidates_generated state.")
    if validation_manifest.get("status") != "validation_complete":
        raise CandidateRepairError("Parent validation manifest is not in validation_complete state.")
    if Path(str(candidate_manifest.get("generation_package", ""))).resolve() != generation_package_path:
        raise CandidateRepairError("Parent candidate manifest belongs to a different generation package.")
    if Path(str(validation_manifest.get("generation_package", ""))).resolve() != generation_package_path:
        raise CandidateRepairError("Parent validation manifest belongs to a different generation package.")
    if Path(str(validation_manifest.get("candidate_manifest", ""))).resolve() != parent_candidate_manifest_path:
        raise CandidateRepairError("Parent validation manifest does not validate the supplied candidate manifest.")

    target = _select_repair_target(validation_manifest)
    if target is None:
        raise CandidateRepairError(
            "The validation manifest contains no rejected or uncertain candidate with repair instructions."
        )
    candidate_id = str(target["candidate_id"])
    parent_record = _candidate_record(candidate_manifest, candidate_id)
    parent_candidate_path = Path(str(parent_record["output_file"])).resolve()
    if not parent_candidate_path.exists() or sha256_file(parent_candidate_path) != str(
        parent_record["sha256"]
    ):
        raise CandidateRepairError(
            f"Parent candidate is missing or changed since validation: {parent_candidate_path}"
        )

    resolved_key = (api_key or os.environ.get("OPENAI_API_KEY", "")).strip()
    if not resolved_key:
        raise CandidateRepairError("Candidate repair requires OPENAI_API_KEY.")
    if _api_key_looks_placeholder(resolved_key):
        raise CandidateRepairError("OPENAI_API_KEY looks like placeholder text.")

    repair_instructions = list(target["repair_instructions"])
    payload = build_repair_payload(
        generation_package,
        parent_candidate_path,
        repair_instructions,
        attempt_number=attempt_number,
    )
    payload_json = json.dumps(payload, sort_keys=True)
    request_endpoint = endpoint or str(generation_package["provider"]["endpoint"])
    http_request = urllib.request.Request(
        request_endpoint,
        data=payload_json.encode("utf-8"),
        headers={
            "Authorization": f"Bearer {resolved_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(  # noqa: S310 - configured OpenAI endpoint by default
            http_request,
            timeout=timeout_seconds,
        ) as response:
            response_payload = json.loads(response.read().decode("utf-8-sig"))
    except urllib.error.HTTPError as exc:
        try:
            converted = _provider_http_error(exc)
        except CandidateGenerationError as generation_error:
            converted = generation_error
        raise CandidateRepairError(str(converted)) from exc
    except urllib.error.URLError as exc:
        raise CandidateRepairError(
            f"OpenAI candidate repair could not connect: {exc.reason}"
        ) from exc

    try:
        image_bytes = _extract_image_result(response_payload)
    except CandidateGenerationError as exc:
        raise CandidateRepairError(str(exc)) from exc

    output_root = output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    candidate_root = output_root / "generated-candidates"
    candidate_root.mkdir(parents=True, exist_ok=True)
    repaired_candidate_id = f"{candidate_id}-repair-{attempt_number:02d}"
    repaired_candidate_path = candidate_root / f"{repaired_candidate_id}.png"
    repaired_candidate_path.write_bytes(image_bytes)
    repaired_digest = sha256_file(repaired_candidate_path)

    manifest = {
        "manifest_id": "constraintos-generated-candidate-manifest/v1",
        "manifest_version": "1.1.0",
        "status": "candidates_generated",
        "generation_package": str(generation_package_path),
        "generation_package_sha256": sha256_file(generation_package_path),
        "provider": "openai_responses_image_generation_repair",
        "provider_request_sha256": hashlib.sha256(payload_json.encode("utf-8")).hexdigest(),
        "provider_response_ids": [response_payload.get("id")],
        "candidate_count": 1,
        "repair_attempt": attempt_number,
        "parent_candidate_manifest": str(parent_candidate_manifest_path),
        "parent_validation_manifest": str(parent_validation_manifest_path),
        "parent_candidate_id": candidate_id,
        "parent_candidate_file": str(parent_candidate_path),
        "parent_candidate_sha256": parent_record["sha256"],
        "repair_instructions": repair_instructions,
        "candidates": [
            {
                "candidate_id": repaired_candidate_id,
                "output_file": str(repaired_candidate_path),
                "sha256": repaired_digest,
                "status": "needs_visual_constraint_validation",
                "machine_decision": "not_evaluated",
                "approval_allowed": False,
            }
        ],
        "next_required_worker": "visual_constraint_validator",
        "production_ready": False,
        "approval_allowed": False,
        "review_decision": "needs_validation",
    }
    manifest_path = output_root / "generated-candidate-manifest.json"
    write_json(manifest_path, manifest)
    manifest["manifest_file"] = str(manifest_path)
    return manifest


def run_repair_loop(
    generation_package_path: Path,
    initial_candidate_manifest_path: Path,
    initial_validation_manifest_path: Path,
    output_root: Path,
    *,
    max_attempts: int = 2,
    api_key: str | None = None,
    generation_endpoint: str | None = None,
    validation_endpoint: str | None = None,
    timeout_seconds: int = 300,
    generate_fn: Callable[..., dict[str, Any]] = generate_repaired_candidate,
    validate_fn: Callable[..., dict[str, Any]] = validate_candidates,
) -> dict[str, Any]:
    if max_attempts < 0 or max_attempts > 5:
        raise CandidateRepairError("max_attempts must be between 0 and 5.")

    generation_package_path = generation_package_path.resolve()
    current_candidate_manifest_path = initial_candidate_manifest_path.resolve()
    current_validation_manifest_path = initial_validation_manifest_path.resolve()
    output_root = output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    history: list[dict[str, Any]] = []

    initial_validation = read_json(current_validation_manifest_path)
    initial_decision = str(initial_validation.get("overall_machine_decision", ""))
    if initial_decision == "machine_passed_manual_review_required":
        target = initial_validation.get("candidate_results", [{}])[0]
        final_manifest = {
            "manifest_id": "constraintos-candidate-repair-loop/v1",
            "manifest_version": "1.0.0",
            "status": "machine_passed_manual_review_required",
            "attempts_used": 0,
            "max_attempts": max_attempts,
            "history": history,
            "final_candidate_file": target.get("candidate_file"),
            "final_candidate_manifest": str(current_candidate_manifest_path),
            "final_validation_manifest": str(current_validation_manifest_path),
            "overall_machine_decision": initial_decision,
            "next_action": "manual_review",
            "production_ready": False,
            "approval_allowed": False,
            "manual_review_required": True,
        }
        manifest_path = output_root / "candidate-repair-loop-manifest.json"
        write_json(manifest_path, final_manifest)
        final_manifest["manifest_file"] = str(manifest_path)
        return final_manifest

    current_validation = initial_validation
    for attempt_number in range(1, max_attempts + 1):
        target = _select_repair_target(current_validation)
        if target is None:
            break
        attempt_root = output_root / f"repair-attempt-{attempt_number:02d}"
        repaired_manifest = generate_fn(
            generation_package_path,
            current_candidate_manifest_path,
            current_validation_manifest_path,
            attempt_root,
            attempt_number=attempt_number,
            api_key=api_key,
            endpoint=generation_endpoint,
            timeout_seconds=timeout_seconds,
        )
        repaired_manifest_path = Path(str(repaired_manifest["manifest_file"])).resolve()
        validation_kwargs: dict[str, Any] = {
            "api_key": api_key,
            "timeout_seconds": timeout_seconds,
        }
        if validation_endpoint is not None:
            validation_kwargs["endpoint"] = validation_endpoint
        repaired_validation = validate_fn(
            generation_package_path,
            repaired_manifest_path,
            attempt_root,
            **validation_kwargs,
        )
        repaired_validation_path = Path(str(repaired_validation["manifest_file"])).resolve()
        repaired_candidate = repaired_manifest["candidates"][0]
        decision = str(repaired_validation["overall_machine_decision"])
        history.append(
            {
                "attempt": attempt_number,
                "parent_candidate_id": target["candidate_id"],
                "repair_instructions": target["repair_instructions"],
                "candidate_id": repaired_candidate["candidate_id"],
                "candidate_file": repaired_candidate["output_file"],
                "candidate_sha256": repaired_candidate["sha256"],
                "candidate_manifest": str(repaired_manifest_path),
                "validation_manifest": str(repaired_validation_path),
                "overall_machine_decision": decision,
                "approval_allowed": False,
            }
        )
        current_candidate_manifest_path = repaired_manifest_path
        current_validation_manifest_path = repaired_validation_path
        current_validation = repaired_validation
        if decision == "machine_passed_manual_review_required":
            break

    final_results = current_validation.get("candidate_results", [])
    final_candidate_file = final_results[0].get("candidate_file") if final_results else None
    final_decision = str(current_validation.get("overall_machine_decision", "rejected"))
    passed = final_decision == "machine_passed_manual_review_required"
    status = "machine_passed_manual_review_required" if passed else "repair_attempts_exhausted"
    manifest = {
        "manifest_id": "constraintos-candidate-repair-loop/v1",
        "manifest_version": "1.0.0",
        "status": status,
        "attempts_used": len(history),
        "max_attempts": max_attempts,
        "history": history,
        "final_candidate_file": final_candidate_file,
        "final_candidate_manifest": str(current_candidate_manifest_path),
        "final_validation_manifest": str(current_validation_manifest_path),
        "overall_machine_decision": final_decision,
        "next_action": "manual_review" if passed else "manual_decision_or_additional_research",
        "production_ready": False,
        "approval_allowed": False,
        "manual_review_required": True,
    }
    manifest_path = output_root / "candidate-repair-loop-manifest.json"
    write_json(manifest_path, manifest)
    manifest["manifest_file"] = str(manifest_path)
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cos-repair-generated-candidates",
        description="Run a bounded validator-directed image repair and revalidation loop.",
    )
    parser.add_argument("--generation-package", type=Path, required=True)
    parser.add_argument("--candidate-manifest", type=Path, required=True)
    parser.add_argument("--validation-manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--max-attempts", type=int, default=2)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_repair_loop(
        args.generation_package,
        args.candidate_manifest,
        args.validation_manifest,
        args.output_root,
        max_attempts=args.max_attempts,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_machine_decision"] == "machine_passed_manual_review_required" else 2


if __name__ == "__main__":
    raise SystemExit(main())
