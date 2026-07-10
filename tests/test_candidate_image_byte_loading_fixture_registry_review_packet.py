import json
from pathlib import Path

from constraintos.candidate_image_byte_loader_cli import main

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Fixture_Registry_Review_Packet_v1.md"
README = ROOT / "examples" / "graphics" / "candidate_evaluation" / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_fixture_registry_review_packet_text_output_preserves_guardrails(capsys) -> None:
    exit_code = main(["registry-review-packet"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Candidate image fixture registry review packet" in output
    assert "registry_state: deterministic_fixture_bytes" in output
    assert "artifact_count: 2" in output
    assert "artifact_bytes_exposed_in_packet: False" in output
    assert "local_file_opening_allowed: False" in output
    assert "artifact_download_allowed: False" in output
    assert "network_fetch_allowed: False" in output
    assert "image_decoding_allowed: False" in output
    assert "approval_allowed: False" in output
    assert "local_image_file_opening: not run" in output
    assert "artifact_download: not run" in output
    assert "network_fetch: not run" in output
    assert "image_decoding: not run" in output


def test_fixture_registry_review_packet_json_output_contains_review_sections(capsys) -> None:
    exit_code = main(["--format", "json", "registry-review-packet"])

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    payload = json.loads(captured.out)
    sections = payload["review_sections"]
    assert payload["candidate_image_fixture_registry_review_packet"]["mode"] == "fixture_registry_review_packet"
    assert payload["candidate_image_fixture_registry_review_packet"]["review_packet_ready"] is True
    assert set(sections) == {
        "registry_identity",
        "artifact_descriptors",
        "validation_boundaries",
        "decision_guardrails",
    }
    assert sections["registry_identity"]["registry_state"] == "deterministic_fixture_bytes"
    assert sections["registry_identity"]["artifact_count"] == 2
    assert sections["validation_boundaries"]["artifact_bytes_exposed_in_packet"] is False
    assert sections["validation_boundaries"]["local_file_opening"] == "not_run"
    assert sections["validation_boundaries"]["network_fetch"] == "not_run"
    assert sections["validation_boundaries"]["image_decoding"] == "not_run"
    assert sections["decision_guardrails"]["approval_allowed"] is False
    assert "Registry validation alone cannot approve a candidate." in sections["decision_guardrails"]["approval_blockers"]


def test_fixture_registry_review_packet_artifact_descriptors_do_not_expose_bytes(capsys) -> None:
    exit_code = main(["--format", "json", "registry-review-packet"])

    payload = json.loads(capsys.readouterr().out)
    descriptors = payload["review_sections"]["artifact_descriptors"]
    assert exit_code == 0
    assert len(descriptors) == 2
    for descriptor in descriptors:
        assert descriptor["artifact_uri"].startswith("artifact://")
        assert descriptor["descriptor_immutable"] is True
        assert descriptor["local_file_opened"] is False
        assert descriptor["artifact_downloaded"] is False
        assert descriptor["network_fetch_ran"] is False
        assert descriptor["image_decoded"] is False
        assert descriptor["approval_allowed"] is False
        assert "data_hex" not in descriptor


def test_fixture_registry_review_packet_writes_json_output_file(tmp_path, capsys) -> None:
    output_path = tmp_path / "reports" / "candidate-image-fixture-registry-review-packet.json"

    exit_code = main(["--format", "json", "--output", str(output_path), "registry-review-packet"])

    stdout = capsys.readouterr().out
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert "Wrote candidate image byte-loading fixture registry review packet" in stdout
    assert payload["summary"]["registry_state"] == "deterministic_fixture_bytes"
    assert payload["summary"]["approval_allowed"] is False


def test_fixture_registry_review_packet_supports_explicit_fixture_registry_path(capsys) -> None:
    registry_path = ROOT / "examples" / "graphics" / "candidate_evaluation" / "candidate_image_fixture_artifact_registry.fixture.json"

    exit_code = main(["--format", "json", "registry-review-packet", "--fixture-registry", str(registry_path)])

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    payload = json.loads(captured.out)
    assert payload["review_sections"]["registry_identity"]["registry_path"] == str(registry_path.resolve())
    assert payload["summary"]["artifact_count"] == 2


def test_fixture_registry_review_packet_milestone_records_scope_and_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Fixture Registry Review Packet v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "command: cos-graphics-byte-loader registry-review-packet" in content
    assert "artifact_bytes_exposed_in_packet: false" in content
    assert "No local image file opening." in content
    assert "No artifact download." in content
    assert "No network fetch." in content
    assert "No image decoding." in content
    assert "No candidate scoring." in content
    assert "pytest tests/test_candidate_image_byte_loading_fixture_registry_review_packet.py" in content


def test_readme_and_command_reference_include_fixture_registry_review_packet() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_byte_loading_fixture_registry_review_packet_status: fixture_only" in readme
    assert "cos-graphics-byte-loader registry-review-packet" in readme
    assert "Candidate image byte loading fixture registry review packet" in command_reference
    assert "cos-graphics-byte-loader registry-review-packet" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_fixture_registry_review_packet.py" in command_reference
