from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXIT_REVIEW = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Minimal_CLI_Exit_Review_v1.md"
MINIMAL_CLI = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Minimal_CLI_v1.md"
REVIEW_PACKET = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Minimal_CLI_Review_Packet_v1.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_minimal_cli_exit_review_exists_and_is_pending_verification() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Minimal CLI Exit Review v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "previous_gate: Candidate Image Byte Loading Minimal CLI Review Packet v1 complete" in content
    assert "baseline: 487 passed" in content


def test_minimal_cli_exit_review_confirms_helper_only_cli_track_status() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "minimal_cli_track_status: complete_after_verification" in content
    assert "minimal_cli_command_status: helper_only" in content
    assert "minimal_cli_review_packet_status: complete_after_verification" in content
    assert "byte_source_status: explicit_fixture_hex_only" in content
    assert "artifact_binding_status: explicit_artifact_uri_only" in content
    assert "approval_automation_status: not_changed" in content


def test_minimal_cli_exit_review_keeps_broader_loading_paths_blocked() -> None:
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


def test_minimal_cli_exit_review_lists_completed_prerequisites() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "[x] Candidate Image Byte Loading Minimal Implementation v1 complete.",
        "[x] Candidate Image Byte Loading Minimal CLI v1 complete.",
        "[x] Candidate Image Byte Loading Minimal CLI Review Packet v1 complete.",
        "[x] Dedicated CLI command exists: cos-graphics-byte-loader minimal.",
        "[x] Dedicated review-packet command exists: cos-graphics-byte-loader review-packet.",
        "[x] CLI accepts fixture bytes only through explicit --fixture-artifact-uri and --fixture-artifact-hex arguments.",
        "[x] CLI binds fixture bytes only to explicit artifact:// URIs.",
        "[x] CLI reuses load_candidate_image_bytes_minimal.",
        "[x] Review packet wraps cli_invocation_boundary, byte_loading_result, safety_boundaries, and decision_guardrails sections.",
        "[x] Review packet preserves approval blockers.",
    ]
    for item in expected:
        assert item in content


def test_minimal_cli_exit_review_sets_fixture_artifact_registry_as_next_allowed_milestone() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "next_allowed_milestone: Candidate Image Byte Loading Fixture Artifact Registry v1" in content
    assert "decision: exit_to_fixture_artifact_registry_after_verification" in content
    assert "deterministic fixture artifact registry" in content
    assert "not broad filesystem or network access" in content


def test_minimal_cli_exit_review_sets_minimum_next_expansion_constraints() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "Keep byte sources fixture-controlled.",
        "Prefer fixture artifact registry hardening before local filesystem expansion.",
        "Do not add arbitrary local file opening.",
        "Do not add file_uri loading.",
        "Do not add artifact download.",
        "Do not add HTTP or HTTPS fetch.",
        "Do not add implicit cloud download.",
        "Do not decode images.",
        "Do not inspect pixels.",
        "Do not score candidates.",
        "Do not mutate source reports.",
        "Do not allow byte-loading success to approve candidates.",
    ]
    for item in expected:
        assert item in content


def test_minimal_cli_exit_review_requires_fixture_registry_guardrails_next() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "explicit artifact registry fixture source only",
        "deterministic fixture artifact IDs",
        "immutable fixture byte descriptors",
        "expected sha256 required before byte exposure",
        "expected byte count required before byte exposure",
        "declared media type required before byte exposure",
        "no local file opening from registry entries",
        "no network fetch from registry entries",
        "no image decoding from registry entries",
        "no approval from byte-loading success",
    ]
    for item in expected:
        assert item in content


def test_minimal_cli_exit_review_depends_on_completed_cli_and_review_packet_milestones() -> None:
    minimal_cli = MINIMAL_CLI.read_text(encoding="utf-8")
    review_packet = REVIEW_PACKET.read_text(encoding="utf-8")

    assert "status: complete" in minimal_cli
    assert "latest_user_reported_candidate_image_byte_loading_minimal_cli_test_result: 8 passed" in minimal_cli
    assert "recommended_next_milestone: Candidate Image Byte Loading Minimal CLI Review Packet v1" in minimal_cli
    assert "status: complete" in review_packet
    assert "latest_user_reported_candidate_image_byte_loading_minimal_cli_review_packet_test_result: 8 passed" in review_packet
    assert "recommended_next_milestone: Candidate Image Byte Loading Minimal CLI Exit Review v1" in review_packet


def test_command_reference_includes_minimal_cli_exit_review_verification_command() -> None:
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Candidate image byte loading minimal CLI exit review" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_minimal_cli_exit_review.py" in command_reference
