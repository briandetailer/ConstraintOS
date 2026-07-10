import json
from pathlib import Path

from constraintos.candidate_image_byte_loader_cli import main

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Minimal_CLI_Review_Packet_v1.md"
README = ROOT / "examples" / "graphics" / "candidate_evaluation" / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"
ARTIFACT_URI = "artifact://external-candidates/perseverance/candidate-0001.png"
PNG_HEX = "89504e470d0a1a0a"


def review_packet_args() -> list[str]:
    return [
        "review-packet",
        "perseverance",
        "--fixture-artifact-uri",
        ARTIFACT_URI,
        "--fixture-artifact-hex",
        PNG_HEX,
    ]


def test_minimal_byte_loader_review_packet_text_output_preserves_guardrails(capsys) -> None:
    exit_code = main(review_packet_args())

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Candidate image byte-loading minimal CLI review packet: perseverance" in output
    assert "approval_blockers:" in output
    assert "- Byte loading alone cannot approve a candidate." in output
    assert "image_decoded: False" in output
    assert "candidate_scoring_ran: False" in output
    assert "source_report_mutation_ran: False" in output
    assert "approval_automation_ran: False" in output
    assert "approval_allowed: False" in output
    assert "local_image_file_opening: not run" in output
    assert "artifact_download: not run" in output
    assert "network_fetch: not run" in output


def test_minimal_byte_loader_review_packet_json_output_contains_review_sections(capsys) -> None:
    exit_code = main(["--format", "json", *review_packet_args()])

    payload = json.loads(capsys.readouterr().out)
    sections = payload["review_sections"]
    assert exit_code == 0
    assert payload["candidate_image_byte_loading_minimal_cli_review_packet"]["mode"] == "helper_only_review_packet"
    assert payload["candidate_image_byte_loading_minimal_cli_review_packet"]["review_packet_ready"] is True
    assert set(sections) == {
        "cli_invocation_boundary",
        "byte_loading_result",
        "safety_boundaries",
        "decision_guardrails",
    }
    assert sections["cli_invocation_boundary"]["command"] == "cos-graphics-byte-loader review-packet"
    assert sections["cli_invocation_boundary"]["byte_source"] == "explicit fixture hex argument"
    assert sections["safety_boundaries"]["local_file_opened"] is False
    assert sections["safety_boundaries"]["artifact_downloaded"] is False
    assert sections["safety_boundaries"]["network_fetch_ran"] is False
    assert sections["safety_boundaries"]["image_decoded"] is False
    assert sections["decision_guardrails"]["approval_allowed"] is False
    assert "Byte loading alone cannot approve a candidate." in sections["decision_guardrails"]["approval_blockers"]


def test_minimal_byte_loader_review_packet_writes_json_output_file(tmp_path, capsys) -> None:
    output_path = tmp_path / "reports" / "perseverance-byte-loader-review-packet.json"

    exit_code = main(["--format", "json", "--output", str(output_path), *review_packet_args()])

    stdout = capsys.readouterr().out
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert "Wrote candidate image byte-loading review packet" in stdout
    assert payload["summary"]["record_key"] == "perseverance"
    assert payload["summary"]["approval_allowed"] is False


def test_minimal_byte_loader_review_packet_reuses_fixture_argument_validation(capsys) -> None:
    exit_code = main([
        "review-packet",
        "perseverance",
        "--fixture-artifact-uri",
        ARTIFACT_URI,
    ])

    stderr = capsys.readouterr().err
    assert exit_code == 2
    assert "--fixture-artifact-uri and --fixture-artifact-hex must be provided together" in stderr


def test_minimal_byte_loader_review_packet_rejects_non_artifact_fixture_uri(capsys) -> None:
    exit_code = main([
        "review-packet",
        "perseverance",
        "--fixture-artifact-uri",
        "https://example.com/candidate.png",
        "--fixture-artifact-hex",
        PNG_HEX,
    ])

    stderr = capsys.readouterr().err
    assert exit_code == 2
    assert "--fixture-artifact-uri must use artifact://" in stderr


def test_minimal_byte_loader_minimal_command_still_works_after_review_packet_addition(capsys) -> None:
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
    assert "approval_allowed: False" in output


def test_minimal_byte_loader_review_packet_milestone_records_scope_and_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Minimal CLI Review Packet v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "command: cos-graphics-byte-loader review-packet" in content
    assert "byte_source: explicit fixture hex argument" in content
    assert "No local image file opening." in content
    assert "No artifact download." in content
    assert "No network fetch." in content
    assert "No image decoding." in content
    assert "No candidate scoring." in content
    assert "pytest tests/test_candidate_image_byte_loading_minimal_cli_review_packet.py" in content


def test_minimal_byte_loader_review_packet_documentation_is_updated() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_byte_loading_minimal_cli_review_packet_status: helper_only" in readme
    assert "cos-graphics-byte-loader review-packet perseverance" in readme
    assert "Candidate image byte loading minimal CLI review packet" in command_reference
    assert "cos-graphics-byte-loader review-packet perseverance" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_minimal_cli_review_packet.py" in command_reference
