import json
from pathlib import Path

from constraintos.candidate_image_byte_loading_review_packet import build_candidate_image_byte_loading_review_packet_payload
from constraintos.candidate_manifests_cli import main

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
README = CANDIDATE_DIR / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_candidate_image_byte_loading_review_packet_payload_preserves_safe_defaults() -> None:
    payload = build_candidate_image_byte_loading_review_packet_payload("perseverance", CANDIDATE_DIR)
    metadata = payload["candidate_image_byte_loading_review_packet"]
    summary = payload["summary"]

    assert metadata["mode"] == "fixture_only"
    assert metadata["image_bytes_loaded"] == "not_run"
    assert metadata["local_file_opening"] == "not_run"
    assert metadata["artifact_download"] == "not_run"
    assert metadata["network_fetch"] == "not_run"
    assert metadata["image_decoding"] == "not_run"
    assert metadata["pixel_inspection"] == "not_run"
    assert metadata["computer_vision"] == "not_run"
    assert metadata["ocr"] == "not_run"
    assert metadata["candidate_scoring"] == "not_run"
    assert metadata["source_report_mutation"] == "not_run"
    assert metadata["approval_automation"] == "not_run"
    assert summary["byte_loading_record_key"] == "perseverance"
    assert summary["byte_loading_state"] == "not_run_contract_only"
    assert summary["image_bytes_loaded"] is False
    assert summary["local_file_opened"] is False
    assert summary["artifact_downloaded"] is False
    assert summary["network_fetch_ran"] is False
    assert summary["image_decoded"] is False
    assert summary["candidate_scoring_ran"] is False
    assert summary["initial_decision"] == "needs_review"
    assert summary["approval_allowed"] is False
    assert summary["byte_loading_review_packet_ready"] is True


def test_candidate_image_byte_loading_review_packet_includes_human_facing_sections() -> None:
    payload = build_candidate_image_byte_loading_review_packet_payload("perseverance", CANDIDATE_DIR)
    sections = payload["review_sections"]

    assert set(sections) == {
        "byte_loading_record_identity",
        "intake_manifest_binding",
        "reference_metadata",
        "byte_loading_policy_snapshot",
        "byte_loading_result",
        "post_load_boundaries",
        "decision_guardrails",
    }
    assert sections["byte_loading_record_identity"]["record_key"] == "perseverance"
    assert sections["intake_manifest_binding"]["contract_key"] == "perseverance"
    assert sections["reference_metadata"]["reference_type"] == "artifact_uri"
    assert sections["reference_metadata"]["media_type"] == "image/png"
    assert sections["byte_loading_policy_snapshot"]["network_fetch_allowed"] is False
    assert sections["byte_loading_result"]["image_bytes_loaded"] is False
    assert sections["post_load_boundaries"]["image_decoded"] is False
    assert sections["decision_guardrails"]["approval_allowed"] is False


def test_candidate_image_byte_loading_review_packet_lists_approval_blockers() -> None:
    payload = build_candidate_image_byte_loading_review_packet_payload("perseverance", CANDIDATE_DIR)
    blockers = payload["review_sections"]["decision_guardrails"]["approval_blockers"]

    assert "byte-loading review packet is fixture-only" in blockers
    assert "image bytes have not been loaded" in blockers
    assert "local files have not been opened" in blockers
    assert "artifacts have not been downloaded" in blockers
    assert "network fetch has not run" in blockers
    assert "image decoding has not run" in blockers
    assert "candidate scoring has not run" in blockers
    assert "approval automation has not run" in blockers


def test_candidate_image_byte_loading_review_packet_resolves_by_contract_key() -> None:
    payload = build_candidate_image_byte_loading_review_packet_payload("supra_2jz_gte_twin_turbo", CANDIDATE_DIR)
    summary = payload["summary"]
    binding = payload["review_sections"]["intake_manifest_binding"]

    assert summary["byte_loading_record_key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert binding["candidate_intake_manifest_id"] == "GRAPHICS-CANDIDATE-INTAKE-MANIFEST-SUPRA-2JZ-GTE-0001"
    assert summary["initial_decision"] == "needs_review"
    assert summary["approval_allowed"] is False


def test_candidate_manifest_cli_byte_loading_review_packet_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "byte-loading-review-packet", "perseverance"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidate image byte-loading review packet: perseverance" in output
    assert "candidate_id: GRAPHICS-CANDIDATE-PERSEVERANCE-0001" in output
    assert "contract_key: perseverance" in output
    assert "byte_loading_state: not_run_contract_only" in output
    assert "reference_type: artifact_uri" in output
    assert "media_type: image/png" in output
    assert "image_bytes_loaded: False" in output
    assert "local_file_opened: False" in output
    assert "artifact_downloaded: False" in output
    assert "network_fetch_ran: False" in output
    assert "image_decoded: False" in output
    assert "approval_allowed: False" in output
    assert "approval_blockers:" in output
    assert "- image bytes have not been loaded" in output
    assert "source_report_mutation: not run" in output


def test_candidate_manifest_cli_byte_loading_review_packet_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "byte-loading-review-packet", "supra_2jz_gte_twin_turbo"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert exit_code == 0
    assert payload["candidate_image_byte_loading_review_packet"]["mode"] == "fixture_only"
    assert payload["candidate_image_byte_loading_review_packet"]["image_bytes_loaded"] == "not_run"
    assert payload["summary"]["byte_loading_record_key"] == "supra_2jz_gte"
    assert payload["summary"]["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert payload["summary"]["approval_allowed"] is False


def test_candidate_manifest_cli_byte_loading_review_packet_writes_json(tmp_path) -> None:
    output_path = tmp_path / "byte-loading-review-packet.json"
    exit_code = main([
        "--project-root",
        str(ROOT),
        "--format",
        "json",
        "--output",
        str(output_path),
        "byte-loading-review-packet",
        "perseverance",
    ])

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["summary"]["byte_loading_review_packet_ready"] is True
    assert payload["summary"]["initial_decision"] == "needs_review"
    assert payload["summary"]["approval_allowed"] is False


def test_readme_and_command_reference_include_candidate_image_byte_loading_review_packet_commands() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "cos-graphics-candidates byte-loading-review-packet perseverance" in readme
    assert "cos-graphics-candidates byte-loading-review-packet supra_2jz_gte_twin_turbo" in readme
    assert "Candidate image byte loading review packet" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_review_packet.py" in command_reference
