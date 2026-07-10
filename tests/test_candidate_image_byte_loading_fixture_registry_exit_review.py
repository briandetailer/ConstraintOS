from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXIT_REVIEW = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Fixture_Registry_Exit_Review_v1.md"
FIXTURE_REGISTRY = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Fixture_Artifact_Registry_v1.md"
REGISTRY_REVIEW_PACKET = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Fixture_Registry_Review_Packet_v1.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_fixture_registry_exit_review_exists_and_is_pending_verification() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Fixture Registry Exit Review v1" in content
    assert "status: active" in content
    assert "previous_gate: Candidate Image Byte Loading Fixture Registry Review Packet v1 complete" in content
    assert "baseline: 487 passed" in content


def test_fixture_registry_exit_review_confirms_registry_track_status() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "fixture_registry_track_status: complete_after_verification" in content
    assert "fixture_artifact_registry_status: complete_after_verification" in content
    assert "fixture_registry_review_packet_status: complete_after_verification" in content
    assert "registry_source_status: schema_validated_deterministic_fixture_json" in content
    assert "artifact_descriptor_status: descriptor_only_review_packet" in content
    assert "artifact_bytes_exposed_in_review_packet: false" in content
    assert "approval_automation_status: not_changed" in content


def test_fixture_registry_exit_review_keeps_broader_loading_paths_blocked() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    blocked = [
        "local_file_path_loading_status: blocked",
        "file_uri_loading_status: blocked",
        "artifact_download_status: blocked",
        "network_fetch_status: blocked",
        "image_decoding_status: blocked",
        "pixel_inspection_status: blocked",
        "computer_vision_integration_status: blocked",
        "ocr_integration_status: blocked",
        "candidate_scoring_status: blocked",
        "source_report_mutation_status: blocked",
    ]
    for item in blocked:
        assert item in content


def test_fixture_registry_exit_review_lists_completed_prerequisites() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "[x] Candidate Image Byte Loading Fixture Artifact Registry v1 complete.",
        "[x] Candidate Image Byte Loading Fixture Registry Review Packet v1 complete.",
        "[x] Deterministic fixture artifact registry schema exists.",
        "[x] Deterministic fixture artifact registry fixture exists.",
        "[x] Fixture artifact registry loader validates descriptors before byte exposure.",
        "[x] Registry descriptors require artifact:// URIs.",
        "[x] Registry descriptors require immutable byte descriptors.",
        "[x] Registry descriptors require expected sha256 before byte exposure.",
        "[x] Registry descriptors require expected byte count before byte exposure.",
        "[x] Registry descriptors require declared media type before byte exposure.",
        "[x] Registry review packet summarizes registry identity, artifact descriptors, validation boundaries, and decision guardrails.",
        "[x] Registry review packet remains descriptor-only and does not expose image bytes.",
    ]
    for item in expected:
        assert item in content


def test_fixture_registry_exit_review_sets_failure_matrix_as_next_allowed_milestone() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "next_allowed_milestone: Candidate Image Byte Loading Fixture Registry Failure Matrix v1" in content
    assert "decision: exit_to_fixture_registry_failure_matrix_after_verification" in content
    assert "fixture-only failure matrix" in content
    assert "not broad filesystem or network access" in content


def test_fixture_registry_exit_review_sets_minimum_next_expansion_constraints() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "Keep byte sources fixture-controlled.",
        "Expand failure coverage before expanding byte sources.",
        "Prefer fixture registry failure matrix hardening before local filesystem expansion.",
        "Do not add arbitrary local file opening.",
        "Do not add local_file_path loading.",
        "Do not add file_uri loading.",
        "Do not add artifact download.",
        "Do not add HTTP or HTTPS fetch.",
        "Do not add implicit cloud download.",
        "Do not decode images.",
        "Do not inspect pixels.",
        "Do not score candidates.",
        "Do not mutate source reports.",
        "Do not allow registry validation or byte-loading success to approve candidates.",
    ]
    for item in expected:
        assert item in content


def test_fixture_registry_exit_review_requires_failure_matrix_guardrails_next() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "fixture-only registry failure matrix",
        "invalid sha256 fixture case",
        "invalid byte count fixture case",
        "invalid media type fixture case",
        "invalid artifact URI fixture case",
        "duplicate artifact ID fixture case",
        "duplicate artifact URI fixture case",
        "descriptor mutability violation fixture case",
        "no local file opening from failure cases",
        "no network fetch from failure cases",
        "no image decoding from failure cases",
        "no approval from failure or success cases",
    ]
    for item in expected:
        assert item in content


def test_fixture_registry_exit_review_depends_on_completed_registry_and_review_packet_milestones() -> None:
    fixture_registry = FIXTURE_REGISTRY.read_text(encoding="utf-8")
    review_packet = REGISTRY_REVIEW_PACKET.read_text(encoding="utf-8")

    assert "status: complete" in fixture_registry
    assert "latest_user_reported_candidate_image_byte_loading_fixture_artifact_registry_test_result: 9 passed" in fixture_registry
    assert "recommended_next_milestone: Candidate Image Byte Loading Fixture Registry Review Packet v1" in fixture_registry
    assert "status: complete" in review_packet
    assert "latest_user_reported_candidate_image_byte_loading_fixture_registry_review_packet_test_result: 7 passed" in review_packet
    assert "recommended_next_milestone: Candidate Image Byte Loading Fixture Registry Exit Review v1" in review_packet


def test_command_reference_includes_fixture_registry_exit_review_verification_command() -> None:
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Candidate image byte loading fixture registry exit review" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_fixture_registry_exit_review.py" in command_reference
