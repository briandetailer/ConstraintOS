from __future__ import annotations

import json
from pathlib import Path

import pytest

from runtime.research_to_render import candidate_validation as validation
from runtime.research_to_render.candidate_generation import sha256_file, write_json


REFERENCE_BYTES = b"\x89PNG\r\n\x1a\nreference"
CANDIDATE_BYTES = b"\x89PNG\r\n\x1a\ncandidate"


def install_validation_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    reference_path = tmp_path / "reference.png"
    candidate_path = tmp_path / "candidate.png"
    reference_path.write_bytes(REFERENCE_BYTES)
    candidate_path.write_bytes(CANDIDATE_BYTES)

    generation_package_path = tmp_path / "generation-package.json"
    generation_package = {
        "manifest_id": "constraintos-reference-conditioned-generation-package/v1",
        "status": "ready_for_generation",
        "subject": "Example technical subject",
        "reference_inputs": [
            {
                "source_id": "official-source",
                "local_file": str(reference_path),
                "sha256": sha256_file(reference_path),
            }
        ],
        "compiled_constraints": {
            "viewpoint": "locked_top_view",
            "required_visible_features": ["connector alpha", "connector beta"],
            "forbidden_features": ["invented connectors", "generated labels"],
            "visual_output": {
                "illustration_style": "publication-ready technical line illustration",
                "composition": "complete subject centered",
                "palette": "neutral grayscale",
                "background": "plain white background",
                "surface_treatment": "controlled linework",
            },
        },
    }
    write_json(generation_package_path, generation_package)

    candidate_manifest_path = tmp_path / "generated-candidate-manifest.json"
    candidate_manifest = {
        "status": "candidates_generated",
        "candidates": [
            {
                "candidate_id": "candidate-01",
                "output_file": str(candidate_path),
                "sha256": sha256_file(candidate_path),
            }
        ],
    }
    write_json(candidate_manifest_path, candidate_manifest)
    return generation_package_path, candidate_manifest_path, reference_path, candidate_path


def passing_result() -> dict:
    return {
        "subject_identity": {"status": "pass", "evidence": "Identity matches."},
        "viewpoint": {"status": "pass", "evidence": "Top view matches."},
        "required_features": [
            {
                "constraint": "connector alpha",
                "status": "pass",
                "evidence": "Visible in the expected position.",
            },
            {
                "constraint": "connector beta",
                "status": "pass",
                "evidence": "Visible in the expected position.",
            },
        ],
        "forbidden_features": [
            {
                "constraint": "invented connectors",
                "status": "pass",
                "evidence": "No extra connector is visible.",
            },
            {
                "constraint": "generated labels",
                "status": "pass",
                "evidence": "No generated text is visible.",
            },
        ],
        "visual_style": {"status": "pass", "evidence": "Style matches."},
        "reference_fidelity": {"status": "pass", "evidence": "Layout matches."},
        "repair_instructions": [],
    }


def test_validation_payload_contains_reference_candidate_and_strict_schema(
    tmp_path: Path,
) -> None:
    generation_package_path, _, _, candidate_path = install_validation_inputs(tmp_path)
    package = validation.read_json(generation_package_path)

    payload = validation.build_validation_payload(package, candidate_path)

    content = payload["input"][0]["content"]
    assert content[0]["type"] == "input_text"
    assert content[1]["type"] == "input_image"
    assert content[2]["type"] == "input_image"
    assert content[1]["detail"] == "high"
    assert content[2]["detail"] == "high"
    assert payload["text"]["format"]["type"] == "json_schema"
    assert payload["text"]["format"]["strict"] is True
    prompt = content[0]["text"]
    assert "connector alpha" in prompt
    assert "invented connectors" in prompt
    assert "The FIRST image is the authoritative reference" in prompt
    assert "The SECOND image is the generated candidate" in prompt


def test_normalization_machine_passes_only_when_every_check_passes(tmp_path: Path) -> None:
    generation_package_path, _, _, _ = install_validation_inputs(tmp_path)
    package = validation.read_json(generation_package_path)

    normalized = validation.normalize_validation_result(package, passing_result())

    assert normalized["machine_decision"] == "machine_passed"
    assert normalized["constraint_coverage_errors"] == []
    assert normalized["approval_allowed"] is False
    assert normalized["manual_review_required"] is True


def test_missing_required_check_fails_closed(tmp_path: Path) -> None:
    generation_package_path, _, _, _ = install_validation_inputs(tmp_path)
    package = validation.read_json(generation_package_path)
    result = passing_result()
    result["required_features"] = result["required_features"][:1]

    normalized = validation.normalize_validation_result(package, result)

    assert normalized["machine_decision"] == "rejected"
    assert "missing:connector beta" in normalized["constraint_coverage_errors"]
    beta = next(
        item
        for item in normalized["required_features"]
        if item["constraint"] == "connector beta"
    )
    assert beta["status"] == "fail"


def test_uncertain_check_requires_review(tmp_path: Path) -> None:
    generation_package_path, _, _, _ = install_validation_inputs(tmp_path)
    package = validation.read_json(generation_package_path)
    result = passing_result()
    result["reference_fidelity"] = {
        "status": "uncertain",
        "evidence": "One component is partially obscured.",
    }
    result["repair_instructions"] = ["Clarify the obscured component geometry."]

    normalized = validation.normalize_validation_result(package, result)

    assert normalized["machine_decision"] == "needs_review"
    assert normalized["repair_instructions"] == [
        "Clarify the obscured component geometry."
    ]


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_validate_candidates_writes_evidence_and_keeps_manual_approval(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    generation_package_path, candidate_manifest_path, _, _ = install_validation_inputs(
        tmp_path
    )
    provider_payload = {
        "id": "resp_validation_001",
        "output": [
            {
                "type": "message",
                "content": [
                    {
                        "type": "output_text",
                        "text": json.dumps(passing_result()),
                    }
                ],
            }
        ],
    }

    def fake_urlopen(_request: object, timeout: int) -> FakeResponse:
        assert timeout == 300
        return FakeResponse(provider_payload)

    monkeypatch.setattr(validation.urllib.request, "urlopen", fake_urlopen)
    output_root = tmp_path / "validation-run"
    manifest = validation.validate_candidates(
        generation_package_path,
        candidate_manifest_path,
        output_root,
        api_key="test-key",
        endpoint="https://example.invalid/v1/responses",
    )

    assert manifest["status"] == "validation_complete"
    assert manifest["overall_machine_decision"] == (
        "machine_passed_manual_review_required"
    )
    assert manifest["next_action"] == "manual_review"
    assert manifest["approval_allowed"] is False
    assert manifest["manual_review_required"] is True
    evidence_path = Path(manifest["candidate_results"][0]["evidence_file"])
    evidence = validation.read_json(evidence_path)
    assert evidence["validation_result"]["machine_decision"] == "machine_passed"
    assert evidence["provider_response_id"] == "resp_validation_001"
    assert (output_root / "candidate-validation-manifest.json").exists()


def test_validation_fails_if_candidate_changes_after_generation(tmp_path: Path) -> None:
    generation_package_path, candidate_manifest_path, _, candidate_path = (
        install_validation_inputs(tmp_path)
    )
    candidate_path.write_bytes(b"changed")

    with pytest.raises(
        validation.CandidateValidationError,
        match="missing or changed",
    ):
        validation.validate_candidates(
            generation_package_path,
            candidate_manifest_path,
            tmp_path / "validation-run",
            api_key="test-key",
        )
