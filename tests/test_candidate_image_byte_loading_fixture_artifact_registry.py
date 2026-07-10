import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from constraintos.candidate_image_byte_loader_cli import main
from constraintos.candidate_image_fixture_artifact_registry import (
    CandidateImageFixtureArtifactRegistryError,
    build_fixture_artifact_registry_report,
    build_in_memory_artifact_registry_from_fixture,
    load_fixture_artifact_registry,
    validate_fixture_artifact_registry,
)

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
SCHEMA = CANDIDATE_DIR / "candidate_image_fixture_artifact_registry.schema.json"
REGISTRY = CANDIDATE_DIR / "candidate_image_fixture_artifact_registry.fixture.json"
PERSEVERANCE_RECORD = CANDIDATE_DIR / "perseverance_candidate_image_byte_loading_record.fixture.json"
SUPRA_RECORD = CANDIDATE_DIR / "supra_2jz_gte_candidate_image_byte_loading_record.fixture.json"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Fixture_Artifact_Registry_v1.md"
README = CANDIDATE_DIR / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"
PNG_SHA256 = "4c4b6a3be1314ab86138bef4314dde022e600960d8689a2c8f8631802d20dab6"
PNG_HEX = "89504e470d0a1a0a"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_fixture_artifact_registry_schema_and_fixture_validate() -> None:
    schema = load_json(SCHEMA)
    fixture = load_json(REGISTRY)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(fixture), key=lambda error: list(error.path))

    assert errors == []
    assert schema["title"] == "ConstraintOS Graphics Candidate Image Fixture Artifact Registry"
    assert fixture["candidate_image_fixture_artifact_registry"]["status"] == "fixture_only"
    assert fixture["candidate_image_fixture_artifact_registry"]["registry_state"] == "deterministic_fixture_bytes"
    assert fixture["candidate_image_fixture_artifact_registry"]["artifact_count"] == 2


def test_fixture_artifact_registry_descriptors_are_deterministic_and_guarded() -> None:
    fixture = load_json(REGISTRY)

    for artifact in fixture["artifacts"]:
        assert artifact["artifact_uri"].startswith("artifact://")
        assert artifact["reference_type"] == "artifact_uri"
        assert artifact["media_type"] == "image/png"
        assert artifact["sha256"] == PNG_SHA256
        assert artifact["byte_count"] == 8
        assert artifact["data_encoding"] == "hex"
        assert artifact["data_hex"] == PNG_HEX
        assert artifact["descriptor_immutable"] is True
        assert artifact["local_file_opened"] is False
        assert artifact["artifact_downloaded"] is False
        assert artifact["network_fetch_ran"] is False
        assert artifact["image_decoded"] is False
        assert artifact["approval_allowed"] is False


def test_fixture_artifact_registry_loader_validates_before_exposing_bytes() -> None:
    registry = load_fixture_artifact_registry(REGISTRY)
    report = build_fixture_artifact_registry_report(registry, REGISTRY)
    adapter = build_in_memory_artifact_registry_from_fixture(registry)

    assert report["candidate_image_fixture_artifact_registry"]["mode"] == "fixture_only"
    assert report["candidate_image_fixture_artifact_registry"]["artifact_count"] == 2
    assert report["candidate_image_fixture_artifact_registry"]["local_file_opening"] == "not_run"
    assert report["candidate_image_fixture_artifact_registry"]["network_fetch"] == "not_run"
    assert adapter.read_artifact_bytes("artifact://external-candidates/perseverance/candidate-0001.png") == bytes.fromhex(PNG_HEX)
    assert adapter.read_artifact_bytes("artifact://external-candidates/supra-2jz-gte/candidate-0001.png") == bytes.fromhex(PNG_HEX)


def test_fixture_artifact_registry_rejects_bad_sha_before_byte_exposure() -> None:
    fixture = load_json(REGISTRY)
    fixture["artifacts"][0]["sha256"] = "0" * 64

    with pytest.raises(CandidateImageFixtureArtifactRegistryError, match="sha256"):
        validate_fixture_artifact_registry(fixture)


def test_byte_loading_records_align_with_fixture_registry_metadata_but_remain_not_loaded() -> None:
    for path in [PERSEVERANCE_RECORD, SUPRA_RECORD]:
        record = load_json(path)
        reference = record["reference_snapshot"]
        result = record["byte_loading_result"]

        assert reference["image_sha256"] == PNG_SHA256
        assert reference["expected_byte_count"] == 8
        assert record["byte_loading_policy_snapshot"]["artifact_uri_resolution"] == "deterministic_fixture_artifact_registry_only"
        assert result["image_bytes_loaded"] is False
        assert result["local_file_opened"] is False
        assert result["artifact_downloaded"] is False
        assert result["network_fetch_ran"] is False


def test_minimal_cli_uses_default_fixture_registry_without_explicit_hex(capsys) -> None:
    exit_code = main(["--format", "json", "minimal", "perseverance"])

    payload = json.loads(capsys.readouterr().out)
    cli = payload["candidate_image_byte_loading_minimal_cli"]
    summary = payload["summary"]
    assert exit_code == 0
    assert cli["byte_source"] == "fixture artifact registry"
    assert cli["fixture_artifact_registry_used"] is True
    assert cli["fixture_artifact_registry_artifact_count"] == 2
    assert summary["status"] == "bytes_loaded"
    assert summary["image_bytes_loaded"] is True
    assert summary["computed_sha256"] == PNG_SHA256
    assert summary["sniffed_media_type"] == "image/png"
    assert summary["local_file_opened"] is False
    assert summary["artifact_downloaded"] is False
    assert summary["network_fetch_ran"] is False
    assert summary["image_decoded"] is False
    assert summary["candidate_scoring_ran"] is False
    assert summary["source_report_mutation_ran"] is False
    assert summary["approval_automation_ran"] is False
    assert summary["approval_allowed"] is False


def test_review_packet_uses_default_fixture_registry_without_explicit_hex(capsys) -> None:
    exit_code = main(["--format", "json", "review-packet", "perseverance"])

    payload = json.loads(capsys.readouterr().out)
    boundary = payload["review_sections"]["cli_invocation_boundary"]
    safety = payload["review_sections"]["safety_boundaries"]
    guardrails = payload["review_sections"]["decision_guardrails"]
    assert exit_code == 0
    assert boundary["byte_source"] == "fixture artifact registry"
    assert boundary["fixture_artifact_registry_used"] is True
    assert safety["local_file_opened"] is False
    assert safety["artifact_downloaded"] is False
    assert safety["network_fetch_ran"] is False
    assert safety["image_decoded"] is False
    assert guardrails["approval_allowed"] is False
    assert "Byte loading alone cannot approve a candidate." in guardrails["approval_blockers"]


def test_fixture_artifact_registry_milestone_records_scope_and_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Fixture Artifact Registry v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "registry_source: schema-validated JSON fixture" in content
    assert "artifact_source: inline deterministic fixture hex bytes" in content
    assert "No local image file opening." in content
    assert "No artifact download." in content
    assert "No network fetch." in content
    assert "No image decoding." in content
    assert "No candidate scoring." in content
    assert "pytest tests/test_candidate_image_byte_loading_fixture_artifact_registry.py" in content


def test_readme_and_command_reference_include_fixture_artifact_registry() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_fixture_artifact_registry.schema.json" in readme
    assert "candidate_image_byte_loading_fixture_artifact_registry_status: fixture_only" in readme
    assert "cos-graphics-byte-loader minimal perseverance" in readme
    assert "Candidate image byte loading fixture artifact registry" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_fixture_artifact_registry.py" in command_reference
