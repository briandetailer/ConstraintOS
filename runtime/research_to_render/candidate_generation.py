from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Mapping

RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"
ALLOWED_OUTPUT_SIZES = {"1024x1024", "1536x1024", "1024x1536", "auto"}
ALLOWED_QUALITIES = {"low", "medium", "high", "auto"}


class CandidateGenerationError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_manifest_file(manifest_path: Path, configured_path: str) -> Path:
    candidate = Path(configured_path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (manifest_path.parent / candidate).resolve()


def _mime_type(path: Path) -> str:
    detected, _ = mimetypes.guess_type(path.name)
    if detected and detected.startswith("image/"):
        return detected
    suffix = path.suffix.casefold()
    fallback = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    if suffix not in fallback:
        raise CandidateGenerationError(
            f"Reference-conditioned generation requires a supported image file, received: {path}"
        )
    return fallback[suffix]


def image_data_url(path: Path) -> str:
    mime_type = _mime_type(path)
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    raise CandidateGenerationError("Expected a string or list of strings in generation constraints.")


def _bounded_integer(value: Any, *, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(parsed, maximum))


def _visual_constraints(request_payload: Mapping[str, Any]) -> dict[str, Any]:
    constraints = request_payload.get("constraints", {})
    if not isinstance(constraints, Mapping):
        raise CandidateGenerationError("Request constraints must be an object.")
    visual = constraints.get("visual_output", {})
    if visual is None:
        visual = {}
    if not isinstance(visual, Mapping):
        raise CandidateGenerationError("constraints.visual_output must be an object.")
    output_size = str(visual.get("output_size", "1024x1024")).strip()
    quality = str(visual.get("quality", "high")).strip()
    if output_size not in ALLOWED_OUTPUT_SIZES:
        raise CandidateGenerationError(
            f"Unsupported image output size in visual constraints: {output_size}"
        )
    if quality not in ALLOWED_QUALITIES:
        raise CandidateGenerationError(
            f"Unsupported image quality in visual constraints: {quality}"
        )
    return {
        "illustration_style": str(
            visual.get(
                "illustration_style",
                "publication-ready technical illustration with clean controlled linework",
            )
        ).strip(),
        "composition": str(
            visual.get("composition", "single isolated subject, centered, complete subject visible")
        ).strip(),
        "palette": str(visual.get("palette", "neutral technical palette with restrained accents")).strip(),
        "background": str(visual.get("background", "plain white background")).strip(),
        "surface_treatment": str(
            visual.get("surface_treatment", "clear component separation without decorative texture")
        ).strip(),
        "label_strategy": str(
            visual.get(
                "label_strategy",
                "no generated text; labels and callouts are added after validation",
            )
        ).strip(),
        "output_size": output_size,
        "quality": quality,
        "candidate_count": _bounded_integer(
            visual.get("candidate_count", 1),
            default=1,
            minimum=1,
            maximum=4,
        ),
    }


def build_compiled_prompt(
    request_payload: Mapping[str, Any],
    reference_record: Mapping[str, Any],
    visual: Mapping[str, Any],
) -> str:
    constraints = request_payload.get("constraints", {})
    required_features = _string_list(constraints.get("required_visible_features"))
    forbidden_features = _string_list(constraints.get("forbidden_features"))
    viewpoint = str(request_payload.get("viewpoint", "unspecified")).strip()
    subject = str(request_payload.get("subject", "")).strip()
    output_kind = str(request_payload.get("output_kind", "technical_illustration")).strip()
    if not subject or not required_features:
        raise CandidateGenerationError(
            "Reference-conditioned generation requires a subject and required visible features."
        )

    required_block = "\n".join(f"- {item}" for item in required_features)
    forbidden_block = "\n".join(f"- {item}" for item in forbidden_features)
    return f"""Create a NEW illustration for publication. Use the attached authoritative reference image as the controlling evidence for subject identity, component geometry, component placement, proportions, and viewpoint. Do not merely return the reference image and do not add labels.

SUBJECT
- {subject}

DELIVERABLE
- {output_kind}
- Viewpoint: {viewpoint}
- Illustration style: {visual['illustration_style']}
- Composition: {visual['composition']}
- Palette: {visual['palette']}
- Background: {visual['background']}
- Surface treatment: {visual['surface_treatment']}

GEOMETRY AND IDENTITY LOCK
- Preserve the real layout, silhouette, proportions, orientation, component count, and relative component placement shown in the authoritative reference.
- The reference is evidence, not a loose inspiration image.
- Do not substitute a generic object, redesign the subject, simplify away required components, or invent hidden geometry.
- Reference source ID: {reference_record['source_id']}
- Reference SHA-256: {reference_record['sha256']}

REQUIRED VISIBLE FEATURES
{required_block}

FORBIDDEN FEATURES
{forbidden_block}
- words, letters, numbers, legends, dimensions, arrows, callout lines, title blocks, watermarks, or generated technical labels inside the image
- cropped-off required components
- decorative scenery or unrelated objects

TEXT AND ANNOTATION STRATEGY
- {visual['label_strategy']}
- Leave clean surrounding space for deterministic labels and leader lines to be added after candidate validation.

OUTPUT RULE
Produce only the new base illustration. It must be visually derived from and faithful to the attached reference while following every constraint above."""


def compile_generation_package(
    request_path: Path,
    orchestration_plan_path: Path,
    source_plate_manifest_path: Path,
    output_path: Path | None = None,
) -> dict[str, Any]:
    request_path = request_path.resolve()
    orchestration_plan_path = orchestration_plan_path.resolve()
    source_plate_manifest_path = source_plate_manifest_path.resolve()
    request_payload = read_json(request_path)
    orchestration = read_json(orchestration_plan_path)
    source_manifest = read_json(source_plate_manifest_path)

    if orchestration.get("status") != "planned":
        raise CandidateGenerationError("Research-to-render orchestration is not in planned state.")
    orchestration_request = orchestration.get("request", {})
    if orchestration_request.get("request_id") != request_payload.get("request_id"):
        raise CandidateGenerationError(
            "The orchestration plan was compiled for a different request."
        )
    render_plan = orchestration.get("render_plan", {})
    if render_plan.get("production_mode") != "reference_conditioned_generation":
        raise CandidateGenerationError(
            "This worker requires a reference_conditioned_generation render plan."
        )
    if source_manifest.get("status") != "extracted":
        raise CandidateGenerationError("The derived source plate is not in extracted state.")

    reference_path = _resolve_manifest_file(
        source_plate_manifest_path,
        str(source_manifest["output_file"]),
    )
    if not reference_path.exists():
        raise CandidateGenerationError(f"Derived reference image is missing: {reference_path}")
    observed_digest = sha256_file(reference_path)
    expected_digest = str(source_manifest.get("output_sha256", "")).lower()
    if not expected_digest or observed_digest != expected_digest:
        raise CandidateGenerationError(
            "Derived reference image digest does not match its extraction manifest."
        )

    source_id = str(source_manifest["source_id"])
    canonical_ids = [str(item) for item in render_plan.get("canonical_source_ids", [])]
    if not canonical_ids or source_id not in canonical_ids:
        raise CandidateGenerationError(
            "The extracted reference is not one of the orchestration plan's canonical sources."
        )

    visual = _visual_constraints(request_payload)
    reference_record = {
        "source_id": source_id,
        "scenario_id": source_manifest.get("scenario_id"),
        "local_file": str(reference_path),
        "sha256": observed_digest,
        "mime_type": _mime_type(reference_path),
        "roles": [
            "subject_identity",
            "geometry",
            "component_layout",
            "proportion",
            "viewpoint",
            "candidate_validation_reference",
        ],
    }
    prompt = build_compiled_prompt(request_payload, reference_record, visual)
    constraints = request_payload.get("constraints", {})
    package = {
        "manifest_id": "constraintos-reference-conditioned-generation-package/v1",
        "manifest_version": "1.1.0",
        "status": "ready_for_generation",
        "request_id": request_payload["request_id"],
        "subject": request_payload["subject"],
        "generation_mode": "reference_conditioned_image_generation",
        "book_image_role": "generated_base_illustration_before_deterministic_annotation",
        "request_file": str(request_path),
        "orchestration_plan": str(orchestration_plan_path),
        "source_plate_manifest": str(source_plate_manifest_path),
        "reference_inputs": [reference_record],
        "compiled_constraints": {
            "viewpoint": request_payload.get("viewpoint"),
            "required_visible_features": _string_list(
                constraints.get("required_visible_features")
            ),
            "forbidden_features": _string_list(constraints.get("forbidden_features")),
            "visual_output": visual,
            "reference_geometry_is_binding": True,
            "provider_generated_labels_allowed": False,
            "deterministic_annotation_required_after_validation": True,
        },
        "compiled_prompt": prompt,
        "compiled_prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "provider": {
            "api": "openai_responses",
            "endpoint": RESPONSES_ENDPOINT,
            "controller_model": os.environ.get(
                "CONSTRAINTOS_IMAGE_CONTROLLER_MODEL", "gpt-5"
            ),
            "image_tool": {
                "type": "image_generation",
                "action": "edit",
                "model": os.environ.get("CONSTRAINTOS_IMAGE_MODEL", "gpt-image-1"),
                "input_fidelity": "high",
                "size": visual["output_size"],
                "quality": visual["quality"],
                "background": "opaque",
                "output_format": "png",
            },
            "input_image_detail": "high",
        },
        "candidate_count": visual["candidate_count"],
        "post_generation_pipeline": [
            "candidate_artifact_manifest",
            "visual_constraint_validation",
            "evidence_report",
            "repair_or_reject",
            "manual_review",
            "deterministic_annotation_and_publication_finishing",
        ],
        "production_ready": False,
        "approval_allowed": False,
        "review_decision": "not_generated",
    }
    if output_path is not None:
        write_json(output_path.resolve(), package)
    return package


def build_responses_payload(generation_package: Mapping[str, Any]) -> dict[str, Any]:
    references = generation_package.get("reference_inputs", [])
    if not references:
        raise CandidateGenerationError("Generation package contains no reference images.")
    content: list[dict[str, Any]] = [
        {
            "type": "input_text",
            "text": str(generation_package["compiled_prompt"]),
        }
    ]
    for reference in references:
        reference_path = Path(str(reference["local_file"]))
        if not reference_path.exists():
            raise CandidateGenerationError(f"Reference image is missing: {reference_path}")
        observed_digest = sha256_file(reference_path)
        if observed_digest != str(reference["sha256"]):
            raise CandidateGenerationError(
                f"Reference image changed after package compilation: {reference_path}"
            )
        content.append(
            {
                "type": "input_image",
                "image_url": image_data_url(reference_path),
                "detail": str(generation_package["provider"]["input_image_detail"]),
            }
        )
    return {
        "model": generation_package["provider"]["controller_model"],
        "store": False,
        "tools": [dict(generation_package["provider"]["image_tool"])],
        "input": [{"role": "user", "content": content}],
    }


def _api_key_looks_placeholder(api_key: str) -> bool:
    lowered = api_key.casefold().strip()
    markers = (
        "your_api_key",
        "paste_your",
        "api_key_here",
        "replace_me",
        "placeholder",
        "example",
    )
    return bool(lowered) and any(marker in lowered for marker in markers)


def _provider_http_error(exc: urllib.error.HTTPError) -> CandidateGenerationError:
    _ = exc.read()
    if exc.code == 401:
        return CandidateGenerationError(
            "OpenAI reference-conditioned generation failed with HTTP 401: the API key was rejected."
        )
    if exc.code == 429:
        return CandidateGenerationError(
            "OpenAI reference-conditioned generation failed with HTTP 429: rate limit, quota, or billing availability."
        )
    return CandidateGenerationError(
        f"OpenAI reference-conditioned generation failed with HTTP {exc.code}."
    )


def _extract_image_result(response_payload: Mapping[str, Any]) -> bytes:
    for item in response_payload.get("output", []):
        if item.get("type") == "image_generation_call" and item.get("result"):
            try:
                return base64.b64decode(item["result"], validate=True)
            except (ValueError, TypeError) as exc:
                raise CandidateGenerationError(
                    "OpenAI image_generation_call returned invalid base64 image data."
                ) from exc
    raise CandidateGenerationError(
        "OpenAI response did not contain a completed image_generation_call result."
    )


def generate_candidates(
    generation_package_path: Path,
    output_root: Path,
    *,
    api_key: str | None = None,
    endpoint: str | None = None,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    generation_package_path = generation_package_path.resolve()
    generation_package = read_json(generation_package_path)
    if generation_package.get("status") != "ready_for_generation":
        raise CandidateGenerationError("Generation package is not ready_for_generation.")
    resolved_key = (api_key or os.environ.get("OPENAI_API_KEY", "")).strip()
    if not resolved_key:
        raise CandidateGenerationError(
            "Reference-conditioned candidate generation requires OPENAI_API_KEY."
        )
    if _api_key_looks_placeholder(resolved_key):
        raise CandidateGenerationError("OPENAI_API_KEY looks like placeholder text.")

    output_root = output_root.resolve()
    candidate_root = output_root / "generated-candidates"
    candidate_root.mkdir(parents=True, exist_ok=True)
    candidates: list[dict[str, Any]] = []
    response_ids: list[str | None] = []
    request_payload = build_responses_payload(generation_package)
    request_payload_json = json.dumps(request_payload, sort_keys=True)
    request_endpoint = endpoint or str(generation_package["provider"]["endpoint"])

    for index in range(1, int(generation_package["candidate_count"]) + 1):
        http_request = urllib.request.Request(
            request_endpoint,
            data=request_payload_json.encode("utf-8"),
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
            raise _provider_http_error(exc) from exc
        except urllib.error.URLError as exc:
            raise CandidateGenerationError(
                f"OpenAI reference-conditioned generation could not connect: {exc.reason}"
            ) from exc

        image_bytes = _extract_image_result(response_payload)
        candidate_path = candidate_root / f"candidate-{index:02d}.png"
        candidate_path.write_bytes(image_bytes)
        candidate_digest = sha256_file(candidate_path)
        response_ids.append(response_payload.get("id"))
        candidates.append(
            {
                "candidate_id": f"candidate-{index:02d}",
                "output_file": str(candidate_path),
                "sha256": candidate_digest,
                "status": "needs_visual_constraint_validation",
                "machine_decision": "not_evaluated",
                "approval_allowed": False,
            }
        )

    manifest = {
        "manifest_id": "constraintos-generated-candidate-manifest/v1",
        "manifest_version": "1.0.0",
        "status": "candidates_generated",
        "generation_package": str(generation_package_path),
        "generation_package_sha256": sha256_file(generation_package_path),
        "provider": "openai_responses_image_generation",
        "provider_request_sha256": hashlib.sha256(
            request_payload_json.encode("utf-8")
        ).hexdigest(),
        "provider_response_ids": response_ids,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "next_required_worker": "visual_constraint_validator",
        "production_ready": False,
        "approval_allowed": False,
        "review_decision": "needs_validation",
    }
    manifest_path = output_root / "generated-candidate-manifest.json"
    write_json(manifest_path, manifest)
    manifest["manifest_file"] = str(manifest_path)
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cos-generate-candidates",
        description=(
            "Compile or execute reference-conditioned technical image candidate generation."
        ),
    )
    parser.add_argument("--request", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--source-plate-manifest", type=Path)
    parser.add_argument("--generation-package", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--generate", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    package_path = args.generation_package
    if package_path is None:
        if not all((args.request, args.plan, args.source_plate_manifest)):
            raise SystemExit(
                "Compilation requires --request, --plan, and --source-plate-manifest."
            )
        package_path = output_root / "generation-package.json"
        compile_generation_package(
            args.request,
            args.plan,
            args.source_plate_manifest,
            package_path,
        )
        print(f"Generation package: {package_path}")
    if args.generate:
        result = generate_candidates(package_path, output_root)
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Status: ready_for_generation")
        print("No provider call was made. Re-run with --generate to create candidates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
