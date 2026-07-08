import json
from pathlib import Path

from constraintos.candidate_evaluation import (
    build_fixture_only_candidate_evaluation,
    candidate_evaluation_report_key,
    find_candidate_evaluation_report_for_manifest,
    summarize_candidate_evaluation_report,
)
from constraintos.candidate_manifests import load_candidate_manifest_report, load_json
from constraintos.candidate_manifests_cli import main

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_candidate_evaluation_report_key_removes_fixture_suffix() -> None:
    path = CANDIDATE_DIR / "perseverance_candidate_evaluation_report.fixture.json"

    assert candidate_evaluation_report_key(path) == "perseverance"


def test_fixture_only_candidate_evaluation_finds_report_for_manifest() -> None:
    manifest_report = load_candidate_manifest_report("perseverance", CANDIDATE_DIR)
    report_path = find_candidate_evaluation_report_for_manifest(manifest_report["summary"], CANDIDATE_DIR)

    assert report_path.name == "perseverance_candidate_evaluation_report.fixture.json"


def test_fixture_only_candidate_evaluation_summary_preserves_needs_review() -> None:
    payload = build_fixture_only_candidate_evaluation("perseverance", CANDIDATE_DIR)
    summary = payload["summary"]
    metadata = payload["candidate_evaluation"]

    assert metadata["mode"] == "fixture_only"
    assert metadata["image_generation"] == "not_run"
    assert metadata["real_image_ingestion"] == "not_run"
    assert metadata["computer_vision"] == "not_run"
    assert metadata["approval_automation"] == "not_run"
    assert summary["candidate_manifest_key"] == "perseverance"
    assert summary["contract_key"] == "perseverance"
    assert summary["candidate_reference_status"] == "reference_only_not_loaded"
    assert summary["report_key"] == "perseverance"
    assert summary["report_mode"] == "contract_shape_only_no_image_evaluation"
    assert summary["overall_evidence_status"] == "not_observed"
    assert summary["recommended_decision"] == "needs_review"
    assert summary["uncertainty_default"] == "needs_review"
    assert summary["approval_allowed"] is False


def test_fixture_only_candidate_evaluation_resolves_by_bound_contract_key() -> None:
    payload = build_fixture_only_candidate_evaluation("supra_2jz_gte_twin_turbo", CANDIDATE_DIR)
    summary = payload["summary"]

    assert summary["candidate_manifest_key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert summary["report_key"] == "supra_2jz_gte"
    assert summary["recommended_decision"] == "needs_review"


def test_fixture_only_candidate_evaluation_report_summary_exposes_guardrails() -> None:
    report = load_json(CANDIDATE_DIR / "supra_2jz_gte_candidate_evaluation_report.fixture.json")
    summary = summarize_candidate_evaluation_report(CANDIDATE_DIR / "supra_2jz_gte_candidate_evaluation_report.fixture.json", report)

    assert summary["image_generation_ran"] is False
    assert summary["real_image_ingestion_ran"] is False
    assert summary["computer_vision_integration_ran"] is False
    assert summary["candidate_evaluation_ran"] is False
    assert summary["recommended_decision"] == "needs_review"
    assert summary["approval_allowed"] is False


def test_candidate_manifest_cli_evaluates_fixture_only_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "evaluate", "perseverance"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidate evaluation: perseverance" in output
    assert "contract_key: perseverance" in output
    assert "candidate_reference_status: reference_only_not_loaded" in output
    assert "overall_evidence_status: not_observed" in output
    assert "recommended_decision: needs_review" in output
    assert "approval_allowed: False" in output
    assert "image_generation: not run" in output
    assert "real_image_ingestion: not run" in output
    assert "computer_vision: not run" in output
    assert "approval_automation: not run" in output


def test_candidate_manifest_cli_evaluates_fixture_only_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "evaluate", "supra_2jz_gte_twin_turbo"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert exit_code == 0
    assert payload["candidate_evaluation"]["mode"] == "fixture_only"
    assert payload["candidate_evaluation"]["image_generation"] == "not_run"
    assert payload["candidate_evaluation"]["real_image_ingestion"] == "not_run"
    assert payload["summary"]["candidate_manifest_key"] == "supra_2jz_gte"
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_candidate_manifest_cli_writes_fixture_only_json_report(tmp_path) -> None:
    output_path = tmp_path / "candidate-evaluation.json"
    exit_code = main([
        "--project-root",
        str(ROOT),
        "--format",
        "json",
        "--output",
        str(output_path),
        "evaluate",
        "perseverance",
    ])

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_command_reference_includes_fixture_only_candidate_evaluation_commands() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Fixture-only candidate evaluation" in content
    assert "cos-graphics-candidates evaluate perseverance" in content
    assert "cos-graphics-candidates evaluate supra_2jz_gte_twin_turbo" in content
    assert "pytest tests/test_fixture_only_candidate_evaluation.py" in content
