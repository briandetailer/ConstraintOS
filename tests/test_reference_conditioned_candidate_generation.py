from __future__ import annotations

import base64
import json
from pathlib import Path

import pytest

from runtime.research_to_render import candidate_generation as generation


PNG_BYTES = b"\x89PNG\r\n\x1a\nconstraintos-reference"
GENERATED_BYTES = b"\x89PNG\r\n\x1a\nconstraintos-generated-candidate"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def install_generation_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    request_path = tmp_path / "request.json"
    request = {
        "request_id": "request-001",
        "request_text": "Create a controlled technical illustration.",
        "subject": "Example technical subject",
        "output_kind": "technical_component_plate",
        "viewpoint": "locked_top_view",
        "constraints": {
            "required_visible_features": [
                "connector alpha",
                "connector beta",
            ],
            "forbidden_features": [
                "invented connectors",
                "hidden-component inference",
            ],
            "visual_output": {
                "illustration_style": "publication-ready technical line illustration",
                "composition": "complete subject centered with annotation space",
                "palette": "neutral grayscale with restrained blue accents",
                "background": "plain white background",
                "surface_treatment": "controlled linework without sketchiness",
                "label_strategy": "no generated text; deterministic labels follow validation",
                "output_size": "1024x1024",
                "quality": "high",
                "candidate_count": 1,
            },
        },
    }
    write_json(request_path, request)

    plan_path = tmp_path / "plan.json"
    plan = {
        "status": "planned",
        "request": {"request_id": "request-001"},
        "render_plan": {
            "production_mode": "reference_conditioned_generation",
            "canonical_source_ids": ["official-source-plate"],
        },
    }
    write_json(plan_path, plan)

    reference_path = tmp_path / "derived" / "official-source.png"
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    reference_path.write_bytes(PNG_BYTES)

    source_manifest_path = tmp_path / "derived" / "source-plate-extraction-manifest.json"
    source_manifest = {
        "manifest_id": "constraintos-derived-source-plate/v1",
        "status": "extracted",
        "scenario_id": "example_scenario",
        "source_id": "official-source-plate",
        "output_file": str(reference_path),
        "output_sha256": generation.sha256_file(reference_path),
        "approval_allowed": False,
    }
    write_json(source_manifest_path, source_manifest)
    return request_path, plan_path, source_manifest_path, reference_path


def test_generation_package_compiles_request_references_and_visual_constraints(
    tmp_path: Path,
) -> None:
    request, plan, source_manifest, reference = install_generation_inputs(tmp_path)
    output = tmp_path / "generation-package.json"

    package = generation.compile_generation_package(
        request,
        plan,
        source_manifest,
        output,
    )

    assert output.exists()
    assert package["manifest_version"] == "1.1.0"
    assert package["status"] == "ready_for_generation"
    assert package["generation_mode"] == "reference_conditioned_image_generation"
    assert package["book_image_role"] == (
        "generated_base_illustration_before_deterministic_annotation"
    )
    assert package["reference_inputs"][0]["local_file"] == str(reference.resolve())
    assert package["reference_inputs"][0]["sha256"] == generation.sha256_file(reference)
    assert package["reference_inputs"][0]["scenario_id"] == "example_scenario"
    assert "candidate_validation_reference" in package["reference_inputs"][0]["roles"]
    assert package["compiled_constraints"]["reference_geometry_is_binding"] is True
    assert package["compiled_constraints"]["provider_generated_labels_allowed"] is False
    assert package["compiled_constraints"][
        "deterministic_annotation_required_after_validation"
    ] is True
    assert package["provider"]["image_tool"]["action"] == "edit"
    assert package["provider"]["image_tool"]["input_fidelity"] == "high"
    assert package["compiled_prompt_sha256"]
    assert package["approval_allowed"] is False


def test_compiled_prompt_contains_every_required_and_forbidden_constraint(
    tmp_path: Path,
) -> None:
    request_path, plan, source_manifest, _ = install_generation_inputs(tmp_path)
    request_payload = generation.read_json(request_path)
    package = generation.compile_generation_package(request_path, plan, source_manifest)
    prompt = package["compiled_prompt"]

    for item in request_payload["constraints"]["required_visible_features"]:
        assert item in prompt
    for item in request_payload["constraints"]["forbidden_features"]:
        assert item in prompt
    assert "The reference is evidence, not a loose inspiration image." in prompt
    assert "Do not merely return the reference image" in prompt
    assert "words, letters, numbers" in prompt
    assert "deterministic labels" in prompt


def test_generation_package_rejects_plan_for_a_different_request(tmp_path: Path) -> None:
    request, plan, source_manifest, _ = install_generation_inputs(tmp_path)
    plan_payload = generation.read_json(plan)
    plan_payload["request"]["request_id"] = "different-request"
    write_json(plan, plan_payload)

    with pytest.raises(generation.CandidateGenerationError, match="different request"):
        generation.compile_generation_package(request, plan, source_manifest)


def test_responses_payload_contains_reference_image_and_generation_tool(
    tmp_path: Path,
) -> None:
    request, plan, source_manifest, _ = install_generation_inputs(tmp_path)
    package = generation.compile_generation_package(request, plan, source_manifest)

    payload = generation.build_responses_payload(package)

    assert payload["model"] == "gpt-5"
    assert payload["store"] is False
    assert payload["tools"] == [
        {
            "type": "image_generation",
            "action": "edit",
            "model": "gpt-image-1",
            "input_fidelity": "high",
            "size": "1024x1024",
            "quality": "high",
            "background": "opaque",
            "output_format": "png",
        }
    ]
    content = payload["input"][0]["content"]
    assert content[0]["type"] == "input_text"
    assert content[1]["type"] == "input_image"
    assert content[1]["detail"] == "high"
    assert content[1]["image_url"].startswith("data:image/png;base64,")


def test_generation_fails_closed_when_reference_changes_after_compilation(
    tmp_path: Path,
) -> None:
    request, plan, source_manifest, reference = install_generation_inputs(tmp_path)
    package_path = tmp_path / "generation-package.json"
    generation.compile_generation_package(request, plan, source_manifest, package_path)
    reference.write_bytes(b"changed-reference")

    with pytest.raises(generation.CandidateGenerationError, match="changed after package"):
        generation.build_responses_payload(generation.read_json(package_path))


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_generate_candidates_writes_real_candidate_artifact_and_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request, plan, source_manifest, _ = install_generation_inputs(tmp_path)
    package_path = tmp_path / "generation-package.json"
    generation.compile_generation_package(request, plan, source_manifest, package_path)

    provider_payload = {
        "id": "resp_candidate_001",
        "output": [
            {
                "type": "image_generation_call",
                "status": "completed",
                "result": base64.b64encode(GENERATED_BYTES).decode("ascii"),
            }
        ],
    }
    captured: dict[str, object] = {}

    def fake_urlopen(request: object, timeout: int) -> FakeResponse:
        captured["request"] = request
        captured["timeout"] = timeout
        return FakeResponse(provider_payload)

    monkeypatch.setattr(generation.urllib.request, "urlopen", fake_urlopen)
    output_root = tmp_path / "run"
    manifest = generation.generate_candidates(
        package_path,
        output_root,
        api_key="test-key",
        endpoint="https://example.invalid/v1/responses",
    )

    candidate_path = output_root / "generated-candidates" / "candidate-01.png"
    assert candidate_path.read_bytes() == GENERATED_BYTES
    assert manifest["status"] == "candidates_generated"
    assert manifest["candidate_count"] == 1
    assert manifest["provider_request_sha256"]
    assert manifest["provider_response_ids"] == ["resp_candidate_001"]
    assert manifest["candidates"][0]["sha256"] == generation.sha256_file(candidate_path)
    assert manifest["candidates"][0]["status"] == (
        "needs_visual_constraint_validation"
    )
    assert manifest["next_required_worker"] == "visual_constraint_validator"
    assert manifest["approval_allowed"] is False
    assert (output_root / "generated-candidate-manifest.json").exists()
    assert captured["timeout"] == 300


def test_placeholder_api_key_is_rejected_before_provider_call(tmp_path: Path) -> None:
    request, plan, source_manifest, _ = install_generation_inputs(tmp_path)
    package_path = tmp_path / "generation-package.json"
    generation.compile_generation_package(request, plan, source_manifest, package_path)

    with pytest.raises(generation.CandidateGenerationError, match="placeholder"):
        generation.generate_candidates(
            package_path,
            tmp_path / "run",
            api_key="your_api_key_here",
        )


def test_cli_compiles_without_spending_provider_credits(tmp_path: Path) -> None:
    request, plan, source_manifest, _ = install_generation_inputs(tmp_path)
    output_root = tmp_path / "cli-run"

    exit_code = generation.main(
        [
            "--request",
            str(request),
            "--plan",
            str(plan),
            "--source-plate-manifest",
            str(source_manifest),
            "--output-root",
            str(output_root),
        ]
    )

    assert exit_code == 0
    package = generation.read_json(output_root / "generation-package.json")
    assert package["status"] == "ready_for_generation"
    assert not (output_root / "generated-candidate-manifest.json").exists()
