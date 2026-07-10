import json
from pathlib import Path

from constraintos.candidate_image_byte_loader_cli import main

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
FAILURE_MATRIX = CANDIDATE_DIR / "candidate_image_fixture_artifact_registry_failure_matrix.fixture.json"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Fixture_Registry_Failure_Review_Packet_v1.md"
README = CANDIDATE_DIR / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_fixture_registry_failure_review_packet_text_output_preserves_guardrails(capsys) -> None:
    exit_code = main(["failure-review-packet"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Candidate image fixture registry failure review packet" in output
    assert "matrix_state: in_memory_mutation_cases" in output
    assert "failure_case_count: 11" in output
    assert "bytes_exposed_on_failure: False" in output
    assert "local_file_opening_allowed: False" in output
    assert "artifact_download_allowed: False" in output
    assert "network_fetch_allowed: False" in output
    assert "image_decoding_allowed: False" in output
    assert "approval_allowed: False" in output
    assert "- invalid_sha256: sha256" in output
    assert "- duplicate_artifact_uri: artifact_uri values must be unique" in output
    assert "failure_execution: not run" in output
    assert "local_image_file_opening: not run" in output
    assert "network_fetch: not run" in output
    assert "image_decoding: not run" in output


def test_fixture_registry_failure_review_packet_json_output_contains_review_sections(capsys) -> None:
    exit_code = main(["--format", "json", "failure-review-packet"])

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    payload = json.loads(captured.out)
    sections = payload["review_sections"]
    assert payload["candidate_image_fixture_registry_failure_review_packet"]["mode"] == "fixture_registry_failure_review_packet"
    assert payload["candidate_image_fixture_registry_failure_review_packet"]["review_packet_ready"] is True
    assert set(sections) == {
        "failure_matrix_identity",
        "failure_cases",
        "failure_boundaries",
        "decision_guardrails",
    }
    assert sections["failure_matrix_identity"]["matrix_state"] == "in_memory_mutation_cases"
    assert sections["failure_matrix_identity"]["failure_case_count"] == 11
    assert len(sections["failure_cases"]) == 11
    assert sections["failure_boundaries"]["failure_execution"] == "not_run_review_only"
    assert sections["failure_boundaries"]["bytes_exposed_in_packet"] is False
    assert sections["failure_boundaries"]["bytes_exposed_on_failure"] is False
    assert sections["failure_boundaries"]["local_file_opening"] == "not_run"
    assert sections["failure_boundaries"]["network_fetch"] == "not_run"
    assert sections["failure_boundaries"]["image_decoding"] == "not_run"
    assert sections["decision_guardrails"]["approval_allowed"] is False
    assert sections["decision_guardrails"]["failure_can_approve"] is False
    assert sections["decision_guardrails"]["byte_loading_success_can_approve"] is False
    assert "Failure matrix review alone cannot approve a candidate." in sections["decision_guardrails"]["approval_blockers"]


def test_fixture_registry_failure_review_packet_does_not_expose_bytes_or_execute_failures(capsys) -> None:
    exit_code = main(["--format", "json", "failure-review-packet"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["review_sections"]["failure_boundaries"]["failure_execution"] == "not_run_review_only"
    assert payload["review_sections"]["failure_boundaries"]["bytes_exposed_in_packet"] is False
    serialized_cases = json.dumps(payload["review_sections"]["failure_cases"], sort_keys=True)
    assert "data_hex" not in serialized_cases
    assert "89504e470d0a1a0a" not in serialized_cases


def test_fixture_registry_failure_review_packet_writes_json_output_file(tmp_path, capsys) -> None:
    output_path = tmp_path / "reports" / "candidate-image-fixture-registry-failure-review-packet.json"

    exit_code = main(["--format", "json", "--output", str(output_path), "failure-review-packet"])

    stdout = capsys.readouterr().out
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert "Wrote candidate image byte-loading fixture registry failure review packet" in stdout
    assert payload["summary"]["matrix_state"] == "in_memory_mutation_cases"
    assert payload["summary"]["failure_case_count"] == 11
    assert payload["summary"]["approval_allowed"] is False


def test_fixture_registry_failure_review_packet_supports_explicit_failure_matrix_path(capsys) -> None:
    exit_code = main(["--format", "json", "failure-review-packet", "--failure-matrix", str(FAILURE_MATRIX)])

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    payload = json.loads(captured.out)
    assert payload["review_sections"]["failure_matrix_identity"]["failure_matrix_path"] == str(FAILURE_MATRIX.resolve())
    assert payload["summary"]["failure_case_count"] == 11


def test_fixture_registry_failure_review_packet_milestone_records_scope_and_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Fixture Registry Failure Review Packet v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "command: cos-graphics-byte-loader failure-review-packet" in content
    assert "bytes_exposed_in_packet: false" in content
    assert "Failure matrix review only; no failure execution from CLI." in content
    assert "No local image file opening." in content
    assert "No artifact download." in content
    assert "No network fetch." in content
    assert "No image decoding." in content
    assert "No candidate scoring." in content
    assert "pytest tests/test_candidate_image_byte_loading_fixture_registry_failure_review_packet.py" in content


def test_readme_and_command_reference_include_fixture_registry_failure_review_packet() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_byte_loading_fixture_registry_failure_review_packet_status: fixture_only" in readme
    assert "cos-graphics-byte-loader failure-review-packet" in readme
    assert "Candidate image byte loading fixture registry failure review packet" in command_reference
    assert "cos-graphics-byte-loader failure-review-packet" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_fixture_registry_failure_review_packet.py" in command_reference
