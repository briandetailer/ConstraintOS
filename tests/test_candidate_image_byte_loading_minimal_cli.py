import json
from pathlib import Path

from constraintos.candidate_image_byte_loader_cli import main

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Minimal_CLI_v1.md"
README = ROOT / "examples" / "graphics" / "candidate_evaluation" / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"
PYPROJECT = ROOT / "pyproject.toml"
ARTIFACT_URI = "artifact://external-candidates/perseverance/candidate-0001.png"
PNG_HEX = "89504e470d0a1a0a"


def test_minimal_byte_loader_cli_text_output_uses_explicit_fixture_bytes(capsys) -> None:
    exit_code = main([
        "minimal",
        "perseverance",
        "--fixture-artifact-uri",
        ARTIFACT_URI,
        "--fixture-artifact-hex",
        PNG_HEX,
    ])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Candidate image byte-loading minimal CLI: perseverance" in output
    assert "reference_type: artifact_uri" in output
    assert "local_file_opened: False" in output
    assert "artifact_downloaded: False" in output
    assert "network_fetch_ran: False" in output
    assert "image_decoded: False" in output
    assert "candidate_scoring_ran: False" in output
    assert "source_report_mutation_ran: False" in output
    assert "approval_automation_ran: False" in output
    assert "approval_allowed: False" in output
    assert "local_image_file_opening: not run" in output
    assert "artifact_download: not run" in output
    assert "network_fetch: not run" in output


def test_minimal_byte_loader_cli_json_output_preserves_non_approval(capsys) -> None:
    exit_code = main([
        "--format",
        "json",
        "minimal",
        "perseverance",
        "--fixture-artifact-uri",
        ARTIFACT_URI,
        "--fixture-artifact-hex",
        PNG_HEX,
    ])

    payload = json.loads(capsys.readouterr().out)
    summary = payload["summary"]
    assert exit_code == 0
    assert payload["candidate_image_byte_loading_minimal_cli"]["mode"] == "helper_only"
    assert payload["candidate_image_byte_loading_minimal_cli"]["fixture_artifact_uri_provided"] is True
    assert payload["candidate_image_byte_loading_minimal_cli"]["fixture_artifact_hex_provided"] is True
    assert payload["candidate_image_byte_loading_minimal_cli"]["local_image_file_opening"] == "not_run"
    assert payload["candidate_image_byte_loading_minimal_cli"]["artifact_download"] == "not_run"
    assert payload["candidate_image_byte_loading_minimal_cli"]["network_fetch"] == "not_run"
    assert summary["record_key"] == "perseverance"
    assert summary["reference_type"] == "artifact_uri"
    assert summary["local_file_opened"] is False
    assert summary["artifact_downloaded"] is False
    assert summary["network_fetch_ran"] is False
    assert summary["image_decoded"] is False
    assert summary["candidate_scoring_ran"] is False
    assert summary["source_report_mutation_ran"] is False
    assert summary["approval_automation_ran"] is False
    assert summary["approval_allowed"] is False


def test_minimal_byte_loader_cli_writes_json_output_file(tmp_path, capsys) -> None:
    output_path = tmp_path / "reports" / "perseverance-byte-loader.json"

    exit_code = main([
        "--format",
        "json",
        "--output",
        str(output_path),
        "minimal",
        "perseverance",
        "--fixture-artifact-uri",
        ARTIFACT_URI,
        "--fixture-artifact-hex",
        PNG_HEX,
    ])

    stdout = capsys.readouterr().out
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert "Wrote candidate image byte-loading report" in stdout
    assert payload["summary"]["record_key"] == "perseverance"
    assert payload["summary"]["approval_allowed"] is False


def test_minimal_byte_loader_cli_requires_fixture_uri_and_hex_together(capsys) -> None:
    exit_code = main([
        "minimal",
        "perseverance",
        "--fixture-artifact-uri",
        ARTIFACT_URI,
    ])

    stderr = capsys.readouterr().err
    assert exit_code == 2
    assert "--fixture-artifact-uri and --fixture-artifact-hex must be provided together" in stderr


def test_minimal_byte_loader_cli_rejects_non_artifact_fixture_uri(capsys) -> None:
    exit_code = main([
        "minimal",
        "perseverance",
        "--fixture-artifact-uri",
        "https://example.com/candidate.png",
        "--fixture-artifact-hex",
        PNG_HEX,
    ])

    stderr = capsys.readouterr().err
    assert exit_code == 2
    assert "--fixture-artifact-uri must use artifact://" in stderr


def test_minimal_byte_loader_cli_rejects_invalid_hex(capsys) -> None:
    exit_code = main([
        "minimal",
        "perseverance",
        "--fixture-artifact-uri",
        ARTIFACT_URI,
        "--fixture-artifact-hex",
        "not-hex",
    ])

    stderr = capsys.readouterr().err
    assert exit_code == 2
    assert "--fixture-artifact-hex must be valid hexadecimal bytes" in stderr


def test_minimal_byte_loader_cli_milestone_records_scope_and_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Minimal CLI v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "command: cos-graphics-byte-loader minimal" in content
    assert "byte_source: explicit fixture hex argument" in content
    assert "No local image file opening." in content
    assert "No artifact download." in content
    assert "No network fetch." in content
    assert "No image decoding." in content
    assert "No candidate scoring." in content
    assert "pytest tests/test_candidate_image_byte_loading_minimal_cli.py" in content


def test_minimal_byte_loader_cli_documentation_and_packaging_are_updated() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")
    pyproject = PYPROJECT.read_text(encoding="utf-8")

    assert "candidate_image_byte_loading_minimal_cli_status: helper_only" in readme
    assert "cos-graphics-byte-loader minimal perseverance" in readme
    assert "Candidate image byte loading minimal CLI" in command_reference
    assert "cos-graphics-byte-loader minimal perseverance" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_minimal_cli.py" in command_reference
    assert "cos-graphics-byte-loader = \"constraintos.candidate_image_byte_loader_cli:main\"" in pyproject
