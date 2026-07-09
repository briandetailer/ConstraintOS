import json
from pathlib import Path

from constraintos.candidate_image_byte_loading_records import (
    candidate_image_byte_loading_record_key,
    list_candidate_image_byte_loading_record_summaries,
    load_candidate_image_byte_loading_record_report,
)
from constraintos.candidate_manifests_cli import main

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
README = CANDIDATE_DIR / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_candidate_image_byte_loading_record_key_removes_fixture_suffix() -> None:
    path = CANDIDATE_DIR / "perseverance_candidate_image_byte_loading_record.fixture.json"

    assert candidate_image_byte_loading_record_key(path) == "perseverance"


def test_candidate_image_byte_loading_record_summaries_are_read_only_and_safe() -> None:
    summaries = list_candidate_image_byte_loading_record_summaries(CANDIDATE_DIR)

    assert {summary["key"] for summary in summaries} == {"perseverance", "supra_2jz_gte"}
    for summary in summaries:
        assert summary["status"] == "static_fixture_only"
        assert summary["byte_loading_state"] == "not_run_contract_only"
        assert summary["reference_type"] == "artifact_uri"
        assert summary["media_type"] == "image/png"
        assert len(summary["image_sha256"]) == 64
        assert summary["expected_byte_count"] == 1
        assert summary["max_candidate_image_bytes"] == 25000000
        assert summary["network_fetch_allowed"] is False
        assert summary["implicit_cloud_download_allowed"] is False
        assert summary["byte_loading_success_can_approve"] is False
        assert summary["image_bytes_loaded"] is False
        assert summary["local_file_opened"] is False
        assert summary["artifact_downloaded"] is False
        assert summary["network_fetch_ran"] is False
        assert summary["actual_loaded_byte_count"] is None
        assert summary["computed_sha256"] is None
        assert summary["sniffed_media_type"] is None
        assert summary["image_decoded"] is False
        assert summary["candidate_scoring_ran"] is False
        assert summary["source_report_mutation_ran"] is False
        assert summary["approval_automation_ran"] is False
        assert summary["approval_allowed"] is False


def test_candidate_image_byte_loading_record_report_resolves_by_contract_key() -> None:
    report = load_candidate_image_byte_loading_record_report("supra_2jz_gte_twin_turbo", CANDIDATE_DIR)
    summary = report["summary"]

    assert summary["key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert summary["candidate_id"] == "GRAPHICS-CANDIDATE-SUPRA-2JZ-GTE-0001"
    assert summary["candidate_intake_manifest_id"] == "GRAPHICS-CANDIDATE-INTAKE-MANIFEST-SUPRA-2JZ-GTE-0001"
    assert summary["approval_allowed"] is False


def test_candidate_manifest_cli_byte_loading_list_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "byte-loading-list"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidate image byte-loading records: 2" in output
    assert "perseverance | contract=perseverance | byte_loading_state=not_run_contract_only" in output
    assert "supra_2jz_gte | contract=supra_2jz_gte_twin_turbo | byte_loading_state=not_run_contract_only" in output
    assert "image_bytes_loaded: not run" in output
    assert "local_file_opening: not run" in output
    assert "artifact_download: not run" in output
    assert "network_fetch: not run" in output
    assert "image_decoding: not run" in output
    assert "candidate_scoring: not run" in output
    assert "approval_automation: not run" in output


def test_candidate_manifest_cli_byte_loading_show_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "byte-loading-show", "perseverance"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidate image byte-loading record: perseverance" in output
    assert "candidate_id: GRAPHICS-CANDIDATE-PERSEVERANCE-0001" in output
    assert "contract_key: perseverance" in output
    assert "byte_loading_state: not_run_contract_only" in output
    assert "reference_type: artifact_uri" in output
    assert "media_type: image/png" in output
    assert "network_fetch_allowed: False" in output
    assert "implicit_cloud_download_allowed: False" in output
    assert "byte_loading_success_can_approve: False" in output
    assert "image_bytes_loaded: False" in output
    assert "local_file_opened: False" in output
    assert "artifact_downloaded: False" in output
    assert "network_fetch_ran: False" in output
    assert "actual_loaded_byte_count: None" in output
    assert "approval_allowed: False" in output
    assert "source_report_mutation: not run" in output


def test_candidate_manifest_cli_byte_loading_list_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "byte-loading-list"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert exit_code == 0
    assert payload["candidate_image_byte_loading_records"]["count"] == 2
    assert payload["candidate_image_byte_loading_records"]["read_only"] is True
    assert payload["candidate_image_byte_loading_records"]["image_bytes_loaded"] == "not_run"
    assert payload["candidate_image_byte_loading_records"]["local_file_opening"] == "not_run"
    assert payload["candidate_image_byte_loading_records"]["artifact_download"] == "not_run"
    assert payload["candidate_image_byte_loading_records"]["network_fetch"] == "not_run"
    assert {record["key"] for record in payload["records"]} == {"perseverance", "supra_2jz_gte"}


def test_candidate_manifest_cli_byte_loading_show_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "byte-loading-show", "supra_2jz_gte_twin_turbo"])
    output = capsys.readouterr().out
    payload = json.loads(output)
    summary = payload["summary"]

    assert exit_code == 0
    assert summary["key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert summary["image_bytes_loaded"] is False
    assert summary["local_file_opened"] is False
    assert summary["artifact_downloaded"] is False
    assert summary["network_fetch_ran"] is False
    assert summary["image_decoded"] is False
    assert summary["candidate_scoring_ran"] is False
    assert summary["approval_allowed"] is False


def test_candidate_manifest_cli_byte_loading_list_writes_json(tmp_path) -> None:
    output_path = tmp_path / "candidate-byte-loading-records.json"
    exit_code = main([
        "--project-root",
        str(ROOT),
        "--format",
        "json",
        "--output",
        str(output_path),
        "byte-loading-list",
    ])

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["candidate_image_byte_loading_records"]["count"] == 2
    assert payload["candidate_image_byte_loading_records"]["candidate_scoring"] == "not_run"


def test_readme_and_command_reference_include_candidate_image_byte_loading_discovery_commands() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "cos-graphics-candidates byte-loading-list" in readme
    assert "cos-graphics-candidates byte-loading-show perseverance" in readme
    assert "cos-graphics-candidates byte-loading-show supra_2jz_gte_twin_turbo" in readme
    assert "Candidate image byte loading discovery" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_discovery_cli.py" in command_reference
