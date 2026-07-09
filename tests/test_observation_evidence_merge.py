import json
from pathlib import Path

from constraintos.candidate_manifests_cli import main
from constraintos.observation_evidence_merge import build_observation_evidence_merge_payload

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_observation_evidence_merge_payload_preserves_safe_defaults() -> None:
    payload = build_observation_evidence_merge_payload("perseverance", CANDIDATE_DIR)
    summary = payload["summary"]
    metadata = payload["observation_evidence_merge"]

    assert metadata["mode"] == "fixture_only"
    assert metadata["real_image_ingestion"] == "not_run"
    assert metadata["computer_vision"] == "not_run"
    assert metadata["ocr"] == "not_run"
    assert metadata["image_generation"] == "not_run"
    assert metadata["approval_automation"] == "not_run"
    assert metadata["candidate_scoring"] == "not_run"
    assert metadata["source_report_mutation"] == "not_run"
    assert summary["candidate_manifest_key"] == "perseverance"
    assert summary["candidate_reference_status"] == "reference_only_not_loaded"
    assert summary["overall_merged_evidence_status"] == "not_observed"
    assert summary["recommended_decision"] == "needs_review"
    assert summary["approval_allowed"] is False


def test_observation_evidence_merge_counts_matched_and_report_only_constraints() -> None:
    payload = build_observation_evidence_merge_payload("perseverance", CANDIDATE_DIR)
    summary = payload["summary"]

    assert summary["manual_observation_count"] == 3
    assert summary["report_evidence_count"] == 5
    assert summary["merged_evidence_count"] == 5
    assert summary["matched_constraint_count"] == 3
    assert summary["manual_only_constraint_count"] == 0
    assert summary["report_only_constraint_count"] == 2
    assert summary["not_observed_count"] == 5


def test_observation_evidence_merge_resolves_by_contract_key() -> None:
    payload = build_observation_evidence_merge_payload("supra_2jz_gte_twin_turbo", CANDIDATE_DIR)
    summary = payload["summary"]

    assert summary["candidate_manifest_key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert summary["observation_key"] == "supra_2jz_gte"
    assert summary["report_key"] == "supra_2jz_gte"
    assert summary["recommended_decision"] == "needs_review"
    assert summary["approval_allowed"] is False


def test_observation_evidence_merge_items_preserve_presence_flags() -> None:
    payload = build_observation_evidence_merge_payload("perseverance", CANDIDATE_DIR)
    items = payload["merged_evidence_items"]
    by_constraint = {item["constraint_id"]: item for item in items}

    assert by_constraint["perseverance.subject_identity"]["manual_observation_present"] is True
    assert by_constraint["perseverance.subject_identity"]["report_evidence_present"] is True
    assert by_constraint["perseverance.approval_guardrail.uncertainty"]["manual_observation_present"] is False
    assert by_constraint["perseverance.approval_guardrail.uncertainty"]["report_evidence_present"] is True
    assert all(item["merged_status"] == "not_observed" for item in items)


def test_candidate_manifest_cli_merge_evidence_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "merge-evidence", "perseverance"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Observation evidence merge: perseverance" in output
    assert "merged_evidence_count: 5" in output
    assert "matched_constraint_count: 3" in output
    assert "report_only_constraint_count: 2" in output
    assert "overall_merged_evidence_status: not_observed" in output
    assert "recommended_decision: needs_review" in output
    assert "approval_allowed: False" in output
    assert "candidate_scoring: not run" in output
    assert "source_report_mutation: not run" in output


def test_candidate_manifest_cli_merge_evidence_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "merge-evidence", "supra_2jz_gte_twin_turbo"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert exit_code == 0
    assert payload["observation_evidence_merge"]["mode"] == "fixture_only"
    assert payload["observation_evidence_merge"]["source_report_mutation"] == "not_run"
    assert payload["summary"]["candidate_manifest_key"] == "supra_2jz_gte"
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_candidate_manifest_cli_merge_evidence_writes_json(tmp_path) -> None:
    output_path = tmp_path / "merged-evidence.json"
    exit_code = main([
        "--project-root",
        str(ROOT),
        "--format",
        "json",
        "--output",
        str(output_path),
        "merge-evidence",
        "perseverance",
    ])

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_command_reference_includes_observation_evidence_merge_commands() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Fixture-only observation evidence merge" in content
    assert "cos-graphics-candidates merge-evidence perseverance" in content
    assert "cos-graphics-candidates merge-evidence supra_2jz_gte_twin_turbo" in content
    assert "pytest tests/test_observation_evidence_merge.py" in content
