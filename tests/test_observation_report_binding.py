import json
from pathlib import Path

from constraintos.candidate_manifests_cli import main
from constraintos.observation_report_binding import build_observation_report_binding_payload

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_observation_report_binding_payload_preserves_safe_defaults() -> None:
    payload = build_observation_report_binding_payload("perseverance", CANDIDATE_DIR)
    summary = payload["summary"]
    metadata = payload["observation_report_binding"]

    assert metadata["mode"] == "fixture_only"
    assert metadata["real_image_ingestion"] == "not_run"
    assert metadata["computer_vision"] == "not_run"
    assert metadata["ocr"] == "not_run"
    assert metadata["image_generation"] == "not_run"
    assert metadata["approval_automation"] == "not_run"
    assert metadata["candidate_scoring"] == "not_run"
    assert summary["candidate_manifest_key"] == "perseverance"
    assert summary["candidate_reference_status"] == "reference_only_not_loaded"
    assert summary["observation_key"] == "perseverance"
    assert summary["report_key"] == "perseverance"
    assert summary["overall_observation_status"] == "needs_review"
    assert summary["overall_evidence_status"] == "not_observed"
    assert summary["recommended_decision"] == "needs_review"
    assert summary["approval_allowed"] is False


def test_observation_report_binding_resolves_by_contract_key() -> None:
    payload = build_observation_report_binding_payload("supra_2jz_gte_twin_turbo", CANDIDATE_DIR)
    summary = payload["summary"]

    assert summary["candidate_manifest_key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert summary["observation_key"] == "supra_2jz_gte"
    assert summary["report_key"] == "supra_2jz_gte"
    assert summary["recommended_decision"] == "needs_review"
    assert summary["approval_allowed"] is False


def test_observation_report_binding_nests_source_payloads() -> None:
    payload = build_observation_report_binding_payload("perseverance", CANDIDATE_DIR)

    assert payload["manual_observation"]["summary"]["candidate_manifest_key"] == "perseverance"
    assert payload["candidate_evaluation"]["summary"]["candidate_manifest_key"] == "perseverance"
    assert payload["manual_observation"]["summary"]["recommended_decision"] == "needs_review"
    assert payload["candidate_evaluation"]["summary"]["recommended_decision"] == "needs_review"


def test_candidate_manifest_cli_bind_observations_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "bind-observations", "perseverance"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Observation/report binding: perseverance" in output
    assert "observation_key: perseverance" in output
    assert "report_key: perseverance" in output
    assert "overall_observation_status: needs_review" in output
    assert "overall_evidence_status: not_observed" in output
    assert "recommended_decision: needs_review" in output
    assert "approval_allowed: False" in output
    assert "real_image_ingestion: not run" in output
    assert "computer_vision: not run" in output
    assert "ocr: not run" in output
    assert "candidate_scoring: not run" in output


def test_candidate_manifest_cli_bind_observations_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "bind-observations", "supra_2jz_gte_twin_turbo"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert exit_code == 0
    assert payload["observation_report_binding"]["mode"] == "fixture_only"
    assert payload["observation_report_binding"]["real_image_ingestion"] == "not_run"
    assert payload["observation_report_binding"]["candidate_scoring"] == "not_run"
    assert payload["summary"]["candidate_manifest_key"] == "supra_2jz_gte"
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_candidate_manifest_cli_bind_observations_writes_json(tmp_path) -> None:
    output_path = tmp_path / "observation-binding.json"
    exit_code = main([
        "--project-root",
        str(ROOT),
        "--format",
        "json",
        "--output",
        str(output_path),
        "bind-observations",
        "perseverance",
    ])

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_command_reference_includes_observation_report_binding_commands() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Observation-to-report binding" in content
    assert "cos-graphics-candidates bind-observations perseverance" in content
    assert "cos-graphics-candidates bind-observations supra_2jz_gte_twin_turbo" in content
    assert "pytest tests/test_observation_report_binding.py" in content
