import json
from pathlib import Path

from constraintos.candidate_manifests_cli import main
from constraintos.manual_observations import (
    build_manual_observation_payload,
    find_manual_observation_for_manifest,
    load_json,
    load_manual_observation_schema,
    load_validated_manual_observation,
    manual_observation_key,
    summarize_manual_observation,
)
from constraintos.candidate_manifests import load_candidate_manifest_report

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_manual_observation_key_removes_fixture_suffix() -> None:
    path = CANDIDATE_DIR / "perseverance_manual_observation.fixture.json"

    assert manual_observation_key(path) == "perseverance"


def test_manual_observation_fixtures_validate_against_schema() -> None:
    schema = load_manual_observation_schema(CANDIDATE_DIR)

    for filename in ["perseverance_manual_observation.fixture.json", "supra_2jz_gte_manual_observation.fixture.json"]:
        observation = load_validated_manual_observation(CANDIDATE_DIR / filename, schema)
        assert observation["manual_observation_fixture"]["status"] == "fixture_only"


def test_manual_observation_finds_fixture_for_manifest() -> None:
    manifest_report = load_candidate_manifest_report("perseverance", CANDIDATE_DIR)
    observation_path = find_manual_observation_for_manifest(manifest_report["summary"], CANDIDATE_DIR)

    assert observation_path.name == "perseverance_manual_observation.fixture.json"


def test_manual_observation_summary_exposes_guardrails() -> None:
    observation = load_json(CANDIDATE_DIR / "supra_2jz_gte_manual_observation.fixture.json")
    summary = summarize_manual_observation(CANDIDATE_DIR / "supra_2jz_gte_manual_observation.fixture.json", observation)

    assert summary["key"] == "supra_2jz_gte"
    assert summary["source_type"] == "manual_human_review"
    assert summary["real_image_ingestion_ran"] is False
    assert summary["computer_vision_ran"] is False
    assert summary["ocr_ran"] is False
    assert summary["image_generation_ran"] is False
    assert summary["approval_automation_ran"] is False
    assert summary["recommended_decision"] == "needs_review"
    assert summary["approval_allowed"] is False
    assert summary["manual_observations_can_approve_alone"] is False


def test_manual_observation_payload_preserves_needs_review() -> None:
    payload = build_manual_observation_payload("perseverance", CANDIDATE_DIR)
    summary = payload["summary"]
    metadata = payload["manual_observation"]

    assert metadata["mode"] == "fixture_only"
    assert metadata["real_image_ingestion"] == "not_run"
    assert metadata["computer_vision"] == "not_run"
    assert metadata["ocr"] == "not_run"
    assert metadata["image_generation"] == "not_run"
    assert metadata["approval_automation"] == "not_run"
    assert summary["candidate_manifest_key"] == "perseverance"
    assert summary["candidate_reference_status"] == "reference_only_not_loaded"
    assert summary["observation_key"] == "perseverance"
    assert summary["source_type"] == "manual_human_review"
    assert summary["overall_observation_status"] == "needs_review"
    assert summary["recommended_decision"] == "needs_review"
    assert summary["approval_allowed"] is False


def test_manual_observation_payload_resolves_by_contract_key() -> None:
    payload = build_manual_observation_payload("supra_2jz_gte_twin_turbo", CANDIDATE_DIR)
    summary = payload["summary"]

    assert summary["candidate_manifest_key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert summary["observation_key"] == "supra_2jz_gte"
    assert summary["recommended_decision"] == "needs_review"


def test_candidate_manifest_cli_observe_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "observe", "perseverance"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Manual observation: perseverance" in output
    assert "source_type: manual_human_review" in output
    assert "candidate_reference_status: reference_only_not_loaded" in output
    assert "overall_observation_status: needs_review" in output
    assert "recommended_decision: needs_review" in output
    assert "approval_allowed: False" in output
    assert "real_image_ingestion: not run" in output
    assert "computer_vision: not run" in output
    assert "ocr: not run" in output
    assert "image_generation: not run" in output


def test_candidate_manifest_cli_observe_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "observe", "supra_2jz_gte_twin_turbo"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert exit_code == 0
    assert payload["manual_observation"]["mode"] == "fixture_only"
    assert payload["manual_observation"]["real_image_ingestion"] == "not_run"
    assert payload["manual_observation"]["computer_vision"] == "not_run"
    assert payload["summary"]["candidate_manifest_key"] == "supra_2jz_gte"
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_candidate_manifest_cli_observe_writes_json(tmp_path) -> None:
    output_path = tmp_path / "manual-observations.json"
    exit_code = main([
        "--project-root",
        str(ROOT),
        "--format",
        "json",
        "--output",
        str(output_path),
        "observe",
        "perseverance",
    ])

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_command_reference_includes_manual_observation_commands() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Manual observation fixture adapter" in content
    assert "cos-graphics-candidates observe perseverance" in content
    assert "cos-graphics-candidates observe supra_2jz_gte_twin_turbo" in content
    assert "pytest tests/test_manual_observation_fixture_adapter.py" in content
