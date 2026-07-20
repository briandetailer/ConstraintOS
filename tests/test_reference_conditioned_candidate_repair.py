from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import pytest

from runtime.research_to_render import candidate_repair as repair
from runtime.research_to_render.candidate_generation import sha256_file, write_json


REFERENCE_BYTES = b"\x89PNG\r\n\x1a\nreference"
CANDIDATE_BYTES = b"\x89PNG\r\n\x1a\nfailed-candidate"
REPAIRED_BYTES = b"\x89PNG\r\n\x1a\nrepaired-candidate"


def install_repair_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    reference_path = tmp_path / "reference.png"
    candidate_path = tmp_path / "candidate-01.png"
    reference_path.write_bytes(REFERENCE_BYTES)
    candidate_path.write_bytes(CANDIDATE_BYTES)

    generation_package_path = tmp_path / "generation-package.json"
    generation_package = {
        "manifest_id": "constraintos-reference-conditioned-generation-package/v1",
        "status": "ready_for_generation",
        "subject": "Example board",
        "compiled_prompt": "Create a complete constrained technical illustration.",
        "compiled_constraints": {
            "viewpoint": "locked_top_view",
            "required_visible_features": ["two USB 2.0 ports", "RTC battery connector"],
            "forbidden_features": ["invented connectors", "generated labels"],
            "visual_output": {
                "illustration_style": "publication-ready technical line illustration",
                "composition": "complete subject centered",
                "palette": "neutral grayscale",
                "background": "plain white background",
                "surface_treatment": "controlled linework",
            },
        },
        "reference_inputs": [
            {
                "source_id": "official-reference",
                "local_file": str(reference_path),
                "sha256": sha256_file(reference_path),
            }
        ],
        "provider": {
            "controller_model": "gpt-5",
            "endpoint": "https://api.openai.com/v1/responses",
            "input_image_detail": "high",
            "image_tool": {
                "type": "image_generation",
                "action": "edit",
                "model": "gpt-image-1",
                "input_fidelity": "high",
                "size": "1024x1024",
                "quality": "high",
                "background": "opaque",
                "output_format": "png",
            },
        },
    }
    write_json(generation_package_path, generation_package)

    candidate_manifest_path = tmp_path / "generated-candidate-manifest.json"
    candidate_manifest = {
        "status": "candidates_generated",
        "generation_package": str(generation_package_path),
        "candidates": [
            {
                "candidate_id": "candidate-01",
                "output_file": str(candidate_path),
                "sha256": sha256_file(candidate_path),
            }
        ],
    }
    write_json(candidate_manifest_path, candidate_manifest)

    validation_manifest_path = tmp_path / "candidate-validation-manifest.json"
    validation_manifest = {
        "status": "validation_complete",
        "generation_package": str(generation_package_path),
        "candidate_manifest": str(candidate_manifest_path),
        "overall_machine_decision": "rejected",
        "candidate_results": [
            {
                "candidate_id": "candidate-01",
                "candidate_file": str(candidate_path),
                "machine_decision": "rejected",
                "repair_instructions": [
                    "Render the two USB 2.0 ports as an unambiguous stacked pair.",
                    "Depict the RTC battery connector at the exact reference location.",
                ],
            }
        ],
    }
    write_json(validation_manifest_path, validation_manifest)
    return (
        generation_package_path,
        candidate_manifest_path,
        validation_manifest_path,
        reference_path,
        candidate_path,
    )


def test_repair_prompt_preserves_original_constraints_and_exact_instructions(
    tmp_path: Path,
) -> None:
    generation_package_path, _, _, _, _ = install_repair_inputs(tmp_path)
    package = repair.read_json(generation_package_path)
    instructions = [
        "Render the two USB 2.0 ports as an unambiguous stacked pair.",
        "Depict the RTC battery connector at the exact reference location.",
    ]

    prompt = repair.build_repair_prompt(package, instructions, attempt_number=1)

    assert package["compiled_prompt"] in prompt
    assert "FIRST image: authoritative reference" in prompt
    assert "SECOND image: previously generated candidate" in prompt
    assert "ATTEMPT 1" in prompt
    for instruction in instructions:
        assert instruction in prompt
    assert "Preserve all portions" in prompt
    assert "Do not redesign or restyle unrelated regions" in prompt
    assert "unapproved candidate" in prompt


def test_repair_payload_orders_reference_before_failed_candidate(tmp_path: Path) -> None:
    generation_package_path, _, _, _, candidate_path = install_repair_inputs(tmp_path)
    package = repair.read_json(generation_package_path)

    payload = repair.build_repair_payload(
        package,
        candidate_path,
        ["Correct the USB port separation."],
        attempt_number=1,
    )

    content = payload["input"][0]["content"]
    assert content[0]["type"] == "input_text"
    assert content[1]["type"] == "input_image"
    assert content[2]["type"] == "input_image"
    assert content[1]["image_url"].startswith("data:image/png;base64,")
    assert content[2]["image_url"].startswith("data:image/png;base64,")
    assert base64.b64decode(content[1]["image_url"].split(",", 1)[1]) == REFERENCE_BYTES
    assert base64.b64decode(content[2]["image_url"].split(",", 1)[1]) == CANDIDATE_BYTES
    assert payload["tools"][0]["action"] == "edit"


class FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_generate_repaired_candidate_records_parent_lineage_and_repairs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    generation_package, candidate_manifest, validation_manifest, _, _ = (
        install_repair_inputs(tmp_path)
    )
    provider_payload = {
        "id": "resp_repair_001",
        "output": [
            {
                "type": "image_generation_call",
                "status": "completed",
                "result": base64.b64encode(REPAIRED_BYTES).decode("ascii"),
            }
        ],
    }

    def fake_urlopen(_request: object, timeout: int) -> FakeResponse:
        assert timeout == 300
        return FakeResponse(provider_payload)

    monkeypatch.setattr(repair.urllib.request, "urlopen", fake_urlopen)
    output_root = tmp_path / "repair-attempt-01"
    manifest = repair.generate_repaired_candidate(
        generation_package,
        candidate_manifest,
        validation_manifest,
        output_root,
        attempt_number=1,
        api_key="test-key",
        endpoint="https://example.invalid/v1/responses",
    )

    candidate = manifest["candidates"][0]
    repaired_path = Path(candidate["output_file"])
    assert repaired_path.read_bytes() == REPAIRED_BYTES
    assert manifest["provider"] == "openai_responses_image_generation_repair"
    assert manifest["repair_attempt"] == 1
    assert manifest["parent_candidate_id"] == "candidate-01"
    assert manifest["parent_candidate_manifest"] == str(candidate_manifest.resolve())
    assert manifest["parent_validation_manifest"] == str(validation_manifest.resolve())
    assert len(manifest["repair_instructions"]) == 2
    assert candidate["candidate_id"] == "candidate-01-repair-01"
    assert candidate["status"] == "needs_visual_constraint_validation"
    assert manifest["approval_allowed"] is False


def _fake_generate_factory(call_log: list[int]):
    def fake_generate(
        generation_package_path: Path,
        parent_candidate_manifest_path: Path,
        parent_validation_manifest_path: Path,
        output_root: Path,
        *,
        attempt_number: int,
        **_kwargs: Any,
    ) -> dict[str, Any]:
        call_log.append(attempt_number)
        output_root.mkdir(parents=True, exist_ok=True)
        candidate_path = output_root / "generated-candidates" / f"candidate-repair-{attempt_number}.png"
        candidate_path.parent.mkdir(parents=True, exist_ok=True)
        candidate_path.write_bytes(REPAIRED_BYTES + bytes([attempt_number]))
        manifest_path = output_root / "generated-candidate-manifest.json"
        manifest = {
            "status": "candidates_generated",
            "generation_package": str(generation_package_path.resolve()),
            "manifest_file": str(manifest_path.resolve()),
            "candidates": [
                {
                    "candidate_id": f"candidate-repair-{attempt_number}",
                    "output_file": str(candidate_path.resolve()),
                    "sha256": sha256_file(candidate_path),
                }
            ],
        }
        write_json(manifest_path, manifest)
        return manifest

    return fake_generate


def test_repair_loop_stops_immediately_after_machine_pass(tmp_path: Path) -> None:
    generation_package, candidate_manifest, validation_manifest, _, _ = (
        install_repair_inputs(tmp_path)
    )
    generation_calls: list[int] = []

    def fake_validate(
        generation_package_path: Path,
        repaired_manifest_path: Path,
        output_root: Path,
        **_kwargs: Any,
    ) -> dict[str, Any]:
        repaired = repair.read_json(repaired_manifest_path)
        candidate = repaired["candidates"][0]
        manifest_path = output_root / "candidate-validation-manifest.json"
        result = {
            "status": "validation_complete",
            "generation_package": str(generation_package_path.resolve()),
            "candidate_manifest": str(repaired_manifest_path.resolve()),
            "manifest_file": str(manifest_path.resolve()),
            "overall_machine_decision": "machine_passed_manual_review_required",
            "candidate_results": [
                {
                    "candidate_id": candidate["candidate_id"],
                    "candidate_file": candidate["output_file"],
                    "machine_decision": "machine_passed",
                    "repair_instructions": [],
                }
            ],
        }
        write_json(manifest_path, result)
        return result

    result = repair.run_repair_loop(
        generation_package,
        candidate_manifest,
        validation_manifest,
        tmp_path / "repair-loop",
        max_attempts=3,
        api_key="test-key",
        generate_fn=_fake_generate_factory(generation_calls),
        validate_fn=fake_validate,
    )

    assert generation_calls == [1]
    assert result["status"] == "machine_passed_manual_review_required"
    assert result["attempts_used"] == 1
    assert result["overall_machine_decision"] == (
        "machine_passed_manual_review_required"
    )
    assert result["next_action"] == "manual_review"
    assert result["approval_allowed"] is False


def test_repair_loop_stops_at_configured_attempt_limit(tmp_path: Path) -> None:
    generation_package, candidate_manifest, validation_manifest, _, _ = (
        install_repair_inputs(tmp_path)
    )
    generation_calls: list[int] = []

    def fake_validate(
        generation_package_path: Path,
        repaired_manifest_path: Path,
        output_root: Path,
        **_kwargs: Any,
    ) -> dict[str, Any]:
        repaired = repair.read_json(repaired_manifest_path)
        candidate = repaired["candidates"][0]
        manifest_path = output_root / "candidate-validation-manifest.json"
        result = {
            "status": "validation_complete",
            "generation_package": str(generation_package_path.resolve()),
            "candidate_manifest": str(repaired_manifest_path.resolve()),
            "manifest_file": str(manifest_path.resolve()),
            "overall_machine_decision": "rejected",
            "candidate_results": [
                {
                    "candidate_id": candidate["candidate_id"],
                    "candidate_file": candidate["output_file"],
                    "machine_decision": "rejected",
                    "repair_instructions": ["Keep correcting the remaining component."],
                }
            ],
        }
        write_json(manifest_path, result)
        return result

    result = repair.run_repair_loop(
        generation_package,
        candidate_manifest,
        validation_manifest,
        tmp_path / "repair-loop",
        max_attempts=2,
        api_key="test-key",
        generate_fn=_fake_generate_factory(generation_calls),
        validate_fn=fake_validate,
    )

    assert generation_calls == [1, 2]
    assert result["status"] == "repair_attempts_exhausted"
    assert result["attempts_used"] == 2
    assert result["overall_machine_decision"] == "rejected"
    assert result["next_action"] == "manual_decision_or_additional_research"
    assert len(result["history"]) == 2
    assert result["approval_allowed"] is False


def test_repair_loop_rejects_unbounded_attempt_count(tmp_path: Path) -> None:
    generation_package, candidate_manifest, validation_manifest, _, _ = (
        install_repair_inputs(tmp_path)
    )

    with pytest.raises(repair.CandidateRepairError, match="between 0 and 5"):
        repair.run_repair_loop(
            generation_package,
            candidate_manifest,
            validation_manifest,
            tmp_path / "repair-loop",
            max_attempts=6,
            api_key="test-key",
        )
