import json
from pathlib import Path

from constraintos.candidate_intake_manifests import (
    candidate_intake_manifest_key,
    list_candidate_intake_manifest_summaries,
    load_candidate_intake_manifest_report,
)
from constraintos.candidate_manifests_cli import main

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
README = CANDIDATE_DIR / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_candidate_intake_manifest_key_removes_fixture_suffix() -> None:
    path = CANDIDATE_DIR / "perseverance_candidate_intake_manifest.fixture.json"

    assert candidate_intake_manifest_key(path) == "perseverance"


def test_candidate_intake_manifest_summaries_are_read_only_and_safe() -> None:
    summaries = list_candidate_intake_manifest_summaries(CANDIDATE_DIR)

    assert {summary["key"] for summary in summaries} == {"perseverance", "supra_2jz_gte"}
    for summary in summaries:
        assert summary["status"] == "static_fixture_only"
        assert summary["intake_state"] == "intake_pending"
        assert summary["reference_type"] == "artifact_uri"
        assert summary["reference_status"] == "intake_pending"
        assert summary["media_type"] == "image/png"
        assert len(summary["image_sha256"]) == 64
        assert summary["network_fetch_allowed"] is False
        assert summary["successful_intake_can_approve"] is False
        assert summary["image_bytes_loaded"] is False
        assert summary["image_decoded"] is False
        assert summary["pixel_inspection_ran"] is False
        assert summary["candidate_scoring_ran"] is False
        assert summary["source_report_mutation_ran"] is False
        assert summary["approval_allowed"] is False


def test_candidate_intake_manifest_report_resolves_by_contract_key() -> None:
    report = load_candidate_intake_manifest_report("supra_2jz_gte_twin_turbo", CANDIDATE_DIR)
    summary = report["summary"]

    assert summary["key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert summary["candidate_id"] == "GRAPHICS-CANDIDATE-SUPRA-2JZ-GTE-0001"
    assert summary["approval_allowed"] is False


def test_candidate_manifest_cli_intake_list_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "intake-list"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidate intake manifests: 2" in output
    assert "perseverance | contract=perseverance | intake_state=intake_pending" in output
    assert "supra_2jz_gte | contract=supra_2jz_gte_twin_turbo | intake_state=intake_pending" in output
    assert "image_bytes_loaded: not run" in output
    assert "image_decoding: not run" in output
    assert "network_fetch: not run" in output
    assert "candidate_scoring: not run" in output
    assert "approval_automation: not run" in output


def test_candidate_manifest_cli_intake_show_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "intake-show", "perseverance"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidate intake manifest: perseverance" in output
    assert "candidate_id: GRAPHICS-CANDIDATE-PERSEVERANCE-0001" in output
    assert "contract_key: perseverance" in output
    assert "intake_state: intake_pending" in output
    assert "reference_type: artifact_uri" in output
    assert "media_type: image/png" in output
    assert "network_fetch_allowed: False" in output
    assert "successful_intake_can_approve: False" in output
    assert "approval_allowed: False" in output
    assert "image_bytes_loaded: not run" in output
    assert "source_report_mutation: not run" in output


def test_candidate_manifest_cli_intake_list_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "intake-list"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert exit_code == 0
    assert payload["candidate_intake_manifests"]["count"] == 2
    assert payload["candidate_intake_manifests"]["read_only"] is True
    assert payload["candidate_intake_manifests"]["image_bytes_loaded"] == "not_run"
    assert payload["candidate_intake_manifests"]["network_fetch"] == "not_run"
    assert {manifest["key"] for manifest in payload["manifests"]} == {"perseverance", "supra_2jz_gte"}


def test_candidate_manifest_cli_intake_show_json(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "intake-show", "supra_2jz_gte_twin_turbo"])
    output = capsys.readouterr().out
    payload = json.loads(output)
    summary = payload["summary"]

    assert exit_code == 0
    assert summary["key"] == "supra_2jz_gte"
    assert summary["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert summary["image_bytes_loaded"] is False
    assert summary["image_decoded"] is False
    assert summary["candidate_scoring_ran"] is False
    assert summary["approval_allowed"] is False


def test_candidate_manifest_cli_intake_list_writes_json(tmp_path) -> None:
    output_path = tmp_path / "candidate-intake-manifests.json"
    exit_code = main([
        "--project-root",
        str(ROOT),
        "--format",
        "json",
        "--output",
        str(output_path),
        "intake-list",
    ])

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["candidate_intake_manifests"]["count"] == 2
    assert payload["candidate_intake_manifests"]["candidate_scoring"] == "not_run"


def test_readme_and_command_reference_include_candidate_intake_discovery_commands() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "cos-graphics-candidates intake-list" in readme
    assert "cos-graphics-candidates intake-show perseverance" in readme
    assert "cos-graphics-candidates intake-show supra_2jz_gte_twin_turbo" in readme
    assert "Candidate intake manifest discovery" in command_reference
    assert "pytest tests/test_candidate_intake_manifest_discovery_cli.py" in command_reference
