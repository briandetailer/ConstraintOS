import json
from pathlib import Path

from constraintos.candidate_manifests_cli import main
from constraintos.candidate_review_packet import build_candidate_review_packet_payload

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_candidate_review_packet_payload_preserves_safe_defaults() -> None:
    payload = build_candidate_review_packet_payload("perseverance", CANDIDATE_DIR)
    summary = payload["summary"]
    metadata = payload["candidate_review_packet"]

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
    assert summary["recommended_decision"] == "needs_review"
    assert summary["approval_allowed"] is False
    assert summary["review_packet_ready"] is True


def test_candidate_review_packet_includes_human_facing_sections() -> None:
    payload = build_candidate_review_packet_payload("perseverance", CANDIDATE_DIR)
    sections = payload["review_sections"]

    assert set(sections) == {
        "candidate_identity",
        "manual_observations",
        "candidate_evaluation_report",
        "merged_evidence",
        "decision_guardrails",
    }
    assert sections["candidate_identity"]["candidate_manifest_key"] == "perseverance"
    assert sections["manual_observations"]["observation_source_type"] == "manual_human_review"
    assert sections["candidate_evaluation_report"]["overall_evidence_status"] == "not_observed"
    assert sections["merged_evidence"]["overall_merged_evidence_status"] == "not_observed"
    assert sections["decision_guardrails"]["recommended_decision"] == "needs_review"
    assert sections["decision_guardrails"]["approval_allowed"] is False


def test_candidate_review_packet_lists_approval_blockers() -> None:
    payload = build_candidate_review_packet_payload("perseverance", CANDIDATE_DIR)
    blockers = payload["review_sections"]["decision_guardrails"]["approval_blockers"]

    assert "candidate_reference_status is reference_only_not_loaded" in blockers
    assert "real image ingestion has not run" in blockers
    assert "computer vision has not run" in blockers
    assert "manual observations cannot approve alone" in blockers
    assert "merged evidence cannot approve candidates" in blockers
    assert "candidate scoring has not run" in blockers


def test_candidate_review_packet_resolves_by_contract_key() -> None:
    payload = build_candidate_review_packet_payload("supra_2jz_gte_twin_turbo", CANDIDATE_DIR)
    summary = payload["summary"]
    identity = payload["review_sections"]["candidate_identity"]

    assert summary["candidate_manifest_key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert identity["subject_name"] == "Toyota Supra Mk IV / A80 Turbo 2JZ-GTE sequential twin-turbo system"
    assert summary["recommended_decision"] == "needs_review"
    assert summary["approval_allowed"] is False


def test_candidate_manifest_cli_review_packet_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "review-packet", "perseverance"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidate review packet: perseverance" in output
    assert "candidate_reference_status: reference_only_not_loaded" in output
    assert "overall_merged_evidence_status: not_observed" in output
    assert "recommended_decision: needs_review" in output
    assert "approval_allowed: False" in output
    assert "approval_blockers:" in output
    assert "- real image ingestion has not run" in output
    assert "candidate_scoring: not run" in output
    assert "source_report_mutation: not run" in output


def test_candidate_manifest_cli_review_packet_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "review-packet", "supra_2jz_gte_twin_turbo"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert exit_code == 0
    assert payload["candidate_review_packet"]["mode"] == "fixture_only"
    assert payload["candidate_review_packet"]["candidate_scoring"] == "not_run"
    assert payload["summary"]["candidate_manifest_key"] == "supra_2jz_gte"
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_candidate_manifest_cli_review_packet_writes_json(tmp_path) -> None:
    output_path = tmp_path / "review-packet.json"
    exit_code = main([
        "--project-root",
        str(ROOT),
        "--format",
        "json",
        "--output",
        str(output_path),
        "review-packet",
        "perseverance",
    ])

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["summary"]["review_packet_ready"] is True
    assert payload["summary"]["recommended_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_command_reference_includes_candidate_review_packet_commands() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Fixture-only candidate review packet" in content
    assert "cos-graphics-candidates review-packet perseverance" in content
    assert "cos-graphics-candidates review-packet supra_2jz_gte_twin_turbo" in content
    assert "pytest tests/test_candidate_review_packet.py" in content
