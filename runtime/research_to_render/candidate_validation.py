from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Mapping

from .candidate_generation import (
    CandidateGenerationError,
    image_data_url,
    read_json,
    sha256_file,
    write_json,
)

RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"
CHECK_STATUS = ["pass", "fail", "uncertain"]

VALIDATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "subject_identity",
        "viewpoint",
        "required_features",
        "forbidden_features",
        "visual_style",
        "reference_fidelity",
        "repair_instructions",
    ],
    "properties": {
        "subject_identity": {
            "type": "object",
            "additionalProperties": False,
            "required": ["status", "evidence"],
            "properties": {
                "status": {"type": "string", "enum": CHECK_STATUS},
                "evidence": {"type": "string"},
            },
        },
        "viewpoint": {
            "type": "object",
            "additionalProperties": False,
            "required": ["status", "evidence"],
            "properties": {
                "status": {"type": "string", "enum": CHECK_STATUS},
                "evidence": {"type": "string"},
            },
        },
        "required_features": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["constraint", "status", "evidence"],
                "properties": {
                    "constraint": {"type": "string"},
                    "status": {"type": "string", "enum": CHECK_STATUS},
                    "evidence": {"type": "string"},
                },
            },
        },
        "forbidden_features": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["constraint", "status", "evidence"],
                "properties": {
                    "constraint": {"type": "string"},
                    "status": {"type": "string", "enum": CHECK_STATUS},
                    "evidence": {"type": "string"},
                },
            },
        },
        "visual_style": {
            "type": "object",
            "additionalProperties": False,
            "required": ["status", "evidence"],
            "properties": {
                "status": {"type": "string", "enum": CHECK_STATUS},
                "evidence": {"type": "string"},
            },
        },
        "reference_fidelity": {
            "type": "object",
            "additionalProperties": False,
            "required": ["status", "evidence"],
            "properties": {
                "status": {"type": "string", "enum": CHECK_STATUS},
                "evidence": {"type": "string"},
            },
        },
        "repair_instructions": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}


class CandidateValidationError(RuntimeError):
    pass


def _extract_output_text(response_payload: Mapping[str, Any]) -> str:
    for item in response_payload.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                return str(content["text"])
    raise CandidateValidationError(
        "Visual validation response did not contain structured output text."
    )


def build_validation_prompt(generation_package: Mapping[str, Any]) -> str:
    constraints = generation_package["compiled_constraints"]
    required = "\n".join(
        f"- {item}" for item in constraints["required_visible_features"]
    )
    forbidden = "\n".join(
        f"- {item}" for item in constraints["forbidden_features"]
    )
    visual = constraints["visual_output"]
    return f"""Independently validate a generated technical illustration against its authoritative reference image and compiled ConstraintOS specification.

The FIRST image is the authoritative reference. The SECOND image is the generated candidate.

SUBJECT
- {generation_package['subject']}

VIEWPOINT
- {constraints['viewpoint']}

REQUIRED VISIBLE FEATURES
{required}

FORBIDDEN FEATURES
{forbidden}
- generated words, letters, numbers, labels, dimensions, arrows, callout lines, title blocks, or watermarks
- generic substitution or invented geometry
- cropped required components

VISUAL OUTPUT CONSTRAINTS
- Illustration style: {visual['illustration_style']}
- Composition: {visual['composition']}
- Palette: {visual['palette']}
- Background: {visual['background']}
- Surface treatment: {visual['surface_treatment']}

VALIDATION RULES
- Compare component count, location, proportion, orientation, silhouette, and connectivity to the reference.
- Use pass only when the candidate visibly satisfies the check.
- Use fail when the candidate visibly violates the check.
- Use uncertain when the evidence is insufficient; never guess.
- Return exactly one required_features item for each exact required feature string above.
- Return exactly one forbidden_features item for each exact forbidden feature string above.
- For a forbidden constraint, pass means the forbidden condition is absent.
- Provide concise repair instructions for every fail or uncertain result.
- Do not approve the image; this is machine validation evidence only."""


def build_validation_payload(
    generation_package: Mapping[str, Any],
    candidate_path: Path,
) -> dict[str, Any]:
    references = generation_package.get("reference_inputs", [])
    if len(references) != 1:
        raise CandidateValidationError(
            "The current validator requires exactly one controlling reference image."
        )
    reference = references[0]
    reference_path = Path(str(reference["local_file"]))
    if not reference_path.exists() or sha256_file(reference_path) != str(reference["sha256"]):
        raise CandidateValidationError(
            "The controlling reference image is missing or no longer matches its generation package."
        )
    if not candidate_path.exists():
        raise CandidateValidationError(f"Generated candidate is missing: {candidate_path}")

    return {
        "model": os.environ.get("CONSTRAINTOS_VALIDATION_MODEL", "gpt-5"),
        "store": False,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": build_validation_prompt(generation_package)},
                    {
                        "type": "input_image",
                        "image_url": image_data_url(reference_path),
                        "detail": "high",
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data_url(candidate_path),
                        "detail": "high",
                    },
                ],
            }
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "constraintos_visual_candidate_validation",
                "description": (
                    "Independent visual evidence for a generated technical illustration candidate."
                ),
                "strict": True,
                "schema": VALIDATION_SCHEMA,
            }
        },
    }


def _normalized(value: str) -> str:
    return " ".join(value.casefold().split())


def _validate_constraint_coverage(
    expected: list[str],
    observed: Any,
    group_name: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    if not isinstance(observed, list):
        raise CandidateValidationError(f"Validation group {group_name} is not a list.")
    records = [dict(item) for item in observed if isinstance(item, Mapping)]
    by_name: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    for record in records:
        normalized = _normalized(str(record.get("constraint", "")))
        if not normalized:
            continue
        if normalized in by_name:
            duplicates.append(str(record.get("constraint", "")))
        by_name[normalized] = record

    ordered: list[dict[str, Any]] = []
    missing: list[str] = []
    for constraint in expected:
        record = by_name.get(_normalized(constraint))
        if record is None:
            missing.append(constraint)
            ordered.append(
                {
                    "constraint": constraint,
                    "status": "fail",
                    "evidence": "The validator omitted this required check.",
                }
            )
        else:
            record["constraint"] = constraint
            ordered.append(record)
    extras = [
        str(record.get("constraint", ""))
        for normalized, record in by_name.items()
        if normalized not in {_normalized(item) for item in expected}
    ]
    coverage_errors = [
        *(f"missing:{item}" for item in missing),
        *(f"duplicate:{item}" for item in duplicates),
        *(f"unexpected:{item}" for item in extras),
    ]
    return ordered, coverage_errors


def normalize_validation_result(
    generation_package: Mapping[str, Any],
    raw_result: Mapping[str, Any],
) -> dict[str, Any]:
    constraints = generation_package["compiled_constraints"]
    expected_required = [str(item) for item in constraints["required_visible_features"]]
    expected_forbidden = [str(item) for item in constraints["forbidden_features"]]
    required, required_coverage_errors = _validate_constraint_coverage(
        expected_required,
        raw_result.get("required_features"),
        "required_features",
    )
    forbidden, forbidden_coverage_errors = _validate_constraint_coverage(
        expected_forbidden,
        raw_result.get("forbidden_features"),
        "forbidden_features",
    )

    normalized = dict(raw_result)
    normalized["required_features"] = required
    normalized["forbidden_features"] = forbidden
    coverage_errors = required_coverage_errors + forbidden_coverage_errors
    normalized["constraint_coverage_errors"] = coverage_errors

    statuses: list[str] = []
    for singleton in (
        "subject_identity",
        "viewpoint",
        "visual_style",
        "reference_fidelity",
    ):
        record = normalized.get(singleton, {})
        status = str(record.get("status", "fail")) if isinstance(record, Mapping) else "fail"
        statuses.append(status if status in CHECK_STATUS else "fail")
    statuses.extend(str(item.get("status", "fail")) for item in required)
    statuses.extend(str(item.get("status", "fail")) for item in forbidden)
    if coverage_errors or "fail" in statuses:
        machine_decision = "rejected"
    elif "uncertain" in statuses:
        machine_decision = "needs_review"
    else:
        machine_decision = "machine_passed"

    normalized["machine_decision"] = machine_decision
    normalized["approval_allowed"] = False
    normalized["manual_review_required"] = True
    return normalized


def _provider_error(exc: urllib.error.HTTPError) -> CandidateValidationError:
    _ = exc.read()
    if exc.code == 401:
        return CandidateValidationError(
            "OpenAI visual validation failed with HTTP 401: the API key was rejected."
        )
    if exc.code == 429:
        return CandidateValidationError(
            "OpenAI visual validation failed with HTTP 429: rate limit, quota, or billing availability."
        )
    return CandidateValidationError(
        f"OpenAI visual validation failed with HTTP {exc.code}."
    )


def validate_candidates(
    generation_package_path: Path,
    candidate_manifest_path: Path,
    output_root: Path,
    *,
    api_key: str | None = None,
    endpoint: str = RESPONSES_ENDPOINT,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    generation_package_path = generation_package_path.resolve()
    candidate_manifest_path = candidate_manifest_path.resolve()
    generation_package = read_json(generation_package_path)
    candidate_manifest = read_json(candidate_manifest_path)
    if generation_package.get("status") != "ready_for_generation":
        raise CandidateValidationError("Generation package is not ready_for_generation.")
    if candidate_manifest.get("status") != "candidates_generated":
        raise CandidateValidationError("Candidate manifest is not in candidates_generated state.")
    resolved_key = (api_key or os.environ.get("OPENAI_API_KEY", "")).strip()
    if not resolved_key:
        raise CandidateValidationError("Visual candidate validation requires OPENAI_API_KEY.")

    output_root = output_root.resolve()
    evidence_root = output_root / "validation-evidence"
    evidence_root.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    response_ids: list[str | None] = []

    for candidate in candidate_manifest.get("candidates", []):
        candidate_path = Path(str(candidate["output_file"]))
        if not candidate_path.exists() or sha256_file(candidate_path) != str(candidate["sha256"]):
            raise CandidateValidationError(
                f"Candidate is missing or changed since generation: {candidate_path}"
            )
        payload = build_validation_payload(generation_package, candidate_path)
        http_request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
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
            raise _provider_error(exc) from exc
        except urllib.error.URLError as exc:
            raise CandidateValidationError(
                f"OpenAI visual validation could not connect: {exc.reason}"
            ) from exc

        raw_result = json.loads(_extract_output_text(response_payload))
        normalized = normalize_validation_result(generation_package, raw_result)
        candidate_id = str(candidate["candidate_id"])
        evidence_path = evidence_root / f"{candidate_id}-validation.json"
        evidence_record = {
            "manifest_id": "constraintos-candidate-validation-evidence/v1",
            "candidate_id": candidate_id,
            "candidate_file": str(candidate_path),
            "candidate_sha256": candidate["sha256"],
            "generation_package": str(generation_package_path),
            "validation_result": normalized,
            "provider_response_id": response_payload.get("id"),
            "approval_allowed": False,
        }
        write_json(evidence_path, evidence_record)
        response_ids.append(response_payload.get("id"))
        results.append(
            {
                "candidate_id": candidate_id,
                "candidate_file": str(candidate_path),
                "evidence_file": str(evidence_path),
                "machine_decision": normalized["machine_decision"],
                "repair_instructions": normalized.get("repair_instructions", []),
                "approval_allowed": False,
            }
        )

    decisions = [item["machine_decision"] for item in results]
    if decisions and all(item == "machine_passed" for item in decisions):
        overall = "machine_passed_manual_review_required"
    elif "machine_passed" in decisions or "needs_review" in decisions:
        overall = "needs_review"
    else:
        overall = "rejected"
    manifest = {
        "manifest_id": "constraintos-candidate-validation-manifest/v1",
        "manifest_version": "1.0.0",
        "status": "validation_complete",
        "generation_package": str(generation_package_path),
        "candidate_manifest": str(candidate_manifest_path),
        "provider": "openai_responses_visual_validation",
        "provider_response_ids": response_ids,
        "candidate_results": results,
        "overall_machine_decision": overall,
        "next_action": (
            "manual_review"
            if overall == "machine_passed_manual_review_required"
            else "repair_or_reject"
        ),
        "production_ready": False,
        "approval_allowed": False,
        "manual_review_required": True,
    }
    manifest_path = output_root / "candidate-validation-manifest.json"
    write_json(manifest_path, manifest)
    manifest["manifest_file"] = str(manifest_path)
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cos-validate-generated-candidates",
        description="Validate generated technical image candidates against references and constraints.",
    )
    parser.add_argument("--generation-package", type=Path, required=True)
    parser.add_argument("--candidate-manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_candidates(
        args.generation_package,
        args.candidate_manifest,
        args.output_root,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_machine_decision"] != "rejected" else 2


if __name__ == "__main__":
    raise SystemExit(main())
