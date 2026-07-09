import hashlib
from pathlib import Path

import pytest

from constraintos.candidate_image_byte_loader import InMemoryArtifactRegistry, load_candidate_image_bytes_minimal

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Minimal_Implementation_v1.md"
README = ROOT / "examples" / "graphics" / "candidate_evaluation" / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"

PNG_BYTES = b"\x89PNG\r\n\x1a\n"
JPEG_BYTES = b"\xff\xd8\xff\x00"
ARTIFACT_URI = "artifact://external-candidates/perseverance/candidate-0001.png"


def build_record(data: bytes = PNG_BYTES, media_type: str = "image/png", reference_type: str = "artifact_uri", reference: str = ARTIFACT_URI) -> dict:
    return {
        "candidate_image_byte_loading_record": {
            "id": "TEST-BYTE-LOADING-RECORD",
            "candidate_id": "TEST-CANDIDATE",
        },
        "contract_binding": {
            "contract_key": "test_contract",
        },
        "reference_snapshot": {
            "reference_type": reference_type,
            "reference": reference,
            "media_type": media_type,
            "image_sha256": hashlib.sha256(data).hexdigest(),
            "expected_byte_count": len(data),
        },
        "byte_loading_policy_snapshot": {
            "max_candidate_image_bytes": 25_000_000,
            "network_fetch_allowed": False,
            "implicit_cloud_download_allowed": False,
            "byte_loading_success_can_approve": False,
        },
    }


def test_minimal_byte_loader_loads_fixture_controlled_artifact_bytes_without_decoding_or_approval() -> None:
    record = build_record()
    registry = InMemoryArtifactRegistry({ARTIFACT_URI: PNG_BYTES})

    result = load_candidate_image_bytes_minimal(record, registry)

    assert result["status"] == "bytes_loaded"
    assert result["failure_code"] is None
    assert result["candidate_id"] == "TEST-CANDIDATE"
    assert result["contract_key"] == "test_contract"
    assert result["image_bytes_loaded"] is True
    assert result["local_file_opened"] is False
    assert result["artifact_downloaded"] is False
    assert result["network_fetch_ran"] is False
    assert result["actual_loaded_byte_count"] == len(PNG_BYTES)
    assert result["computed_sha256"] == hashlib.sha256(PNG_BYTES).hexdigest()
    assert result["sniffed_media_type"] == "image/png"
    assert result["byte_count_within_limit"] is True
    assert result["checksum_matches"] is True
    assert result["media_type_matches"] is True
    assert result["image_decoded"] is False
    assert result["pixel_inspection_ran"] is False
    assert result["computer_vision_ran"] is False
    assert result["ocr_ran"] is False
    assert result["candidate_scoring_ran"] is False
    assert result["source_report_mutation_ran"] is False
    assert result["approval_automation_ran"] is False
    assert result["initial_decision"] == "needs_review"
    assert result["approval_allowed"] is False


def test_minimal_byte_loader_result_is_immutable() -> None:
    result = load_candidate_image_bytes_minimal(build_record(), InMemoryArtifactRegistry({ARTIFACT_URI: PNG_BYTES}))

    with pytest.raises(TypeError):
        result["approval_allowed"] = True


def test_minimal_byte_loader_rejects_missing_artifact_safely() -> None:
    result = load_candidate_image_bytes_minimal(build_record(), InMemoryArtifactRegistry({}))

    assert result["status"] == "intake_failed"
    assert result["failure_code"] == "artifact_not_found"
    assert result["image_bytes_loaded"] is False
    assert result["local_file_opened"] is False
    assert result["artifact_downloaded"] is False
    assert result["network_fetch_ran"] is False
    assert result["image_decoded"] is False
    assert result["candidate_scoring_ran"] is False
    assert result["approval_allowed"] is False
    assert result["initial_decision"] == "intake_failed"


def test_minimal_byte_loader_rejects_network_references_before_registry_lookup() -> None:
    record = build_record(reference="https://example.com/candidate.png")
    result = load_candidate_image_bytes_minimal(record, InMemoryArtifactRegistry({"https://example.com/candidate.png": PNG_BYTES}))

    assert result["status"] == "intake_failed"
    assert result["failure_code"] == "network_reference_rejected"
    assert result["image_bytes_loaded"] is False
    assert result["network_fetch_ran"] is False
    assert result["approval_allowed"] is False


def test_minimal_byte_loader_rejects_non_artifact_reference_types() -> None:
    record = build_record(reference_type="local_file_path", reference="external-candidates/candidate.png")
    result = load_candidate_image_bytes_minimal(record, InMemoryArtifactRegistry({ARTIFACT_URI: PNG_BYTES}))

    assert result["status"] == "intake_failed"
    assert result["failure_code"] == "unsupported_reference_type"
    assert result["local_file_opened"] is False
    assert result["image_bytes_loaded"] is False
    assert result["approval_allowed"] is False


def test_minimal_byte_loader_rejects_checksum_mismatch_without_approval() -> None:
    record = build_record(data=PNG_BYTES)
    registry = InMemoryArtifactRegistry({ARTIFACT_URI: JPEG_BYTES[: len(PNG_BYTES)]})
    record["reference_snapshot"]["expected_byte_count"] = len(JPEG_BYTES[: len(PNG_BYTES)])

    result = load_candidate_image_bytes_minimal(record, registry)

    assert result["status"] == "intake_failed"
    assert result["failure_code"] == "checksum_mismatch"
    assert result["actual_loaded_byte_count"] == len(JPEG_BYTES[: len(PNG_BYTES)])
    assert result["checksum_matches"] is False
    assert result["image_decoded"] is False
    assert result["candidate_scoring_ran"] is False
    assert result["approval_allowed"] is False


def test_minimal_byte_loader_rejects_media_type_mismatch_after_checksum_pass() -> None:
    record = build_record(data=PNG_BYTES, media_type="image/jpeg")
    registry = InMemoryArtifactRegistry({ARTIFACT_URI: PNG_BYTES})

    result = load_candidate_image_bytes_minimal(record, registry)

    assert result["status"] == "intake_failed"
    assert result["failure_code"] == "media_type_mismatch"
    assert result["computed_sha256"] == hashlib.sha256(PNG_BYTES).hexdigest()
    assert result["sniffed_media_type"] == "image/png"
    assert result["checksum_matches"] is True
    assert result["media_type_matches"] is False
    assert result["image_decoded"] is False
    assert result["approval_allowed"] is False


def test_minimal_byte_loader_rejects_oversize_expected_byte_count_before_loading_success() -> None:
    record = build_record()
    record["reference_snapshot"]["expected_byte_count"] = 25_000_001
    result = load_candidate_image_bytes_minimal(record, InMemoryArtifactRegistry({ARTIFACT_URI: PNG_BYTES}))

    assert result["status"] == "intake_failed"
    assert result["failure_code"] == "expected_byte_count_exceeds_limit"
    assert result["image_bytes_loaded"] is False
    assert result["actual_loaded_byte_count"] is None
    assert result["approval_allowed"] is False


def test_minimal_byte_loader_milestone_records_scope_and_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Minimal Implementation v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "accepted_reference_type: artifact_uri" in content
    assert "artifact_source: explicit in-memory artifact registry adapter" in content
    assert "No local file opening." in content
    assert "No artifact download." in content
    assert "No network fetch." in content
    assert "No image decoding." in content
    assert "No candidate scoring." in content
    assert "pytest tests/test_candidate_image_byte_loading_minimal_implementation.py" in content


def test_readme_and_command_reference_include_minimal_implementation_verification() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_byte_loading_minimal_implementation_status: helper_only" in readme
    assert "Candidate image byte loading minimal implementation" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_minimal_implementation.py" in command_reference
