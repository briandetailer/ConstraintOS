from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXIT_REVIEW = ROOT / "docs" / "500_Milestones" / "Byte_Loading_Foundation_Exit_Review_v1.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"
README = ROOT / "examples" / "graphics" / "candidate_evaluation" / "README.md"


def test_byte_loading_foundation_exit_review_exists_and_is_pending_verification() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "milestone: Byte Loading Foundation Exit Review v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "previous_gate: Candidate Image Byte Loading Review Packet v1 complete" in content
    assert "baseline: 487 passed" in content


def test_byte_loading_foundation_exit_review_records_fixture_ready_status() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "byte_loading_foundation_status: fixture_only_byte_loading_metadata_ready" in content
    assert "image_byte_loading_implementation_status: not_started" in content
    assert "local_file_opening_status: blocked" in content
    assert "artifact_download_status: blocked" in content
    assert "network_fetch_status: blocked" in content
    assert "image_decoding_status: not_started" in content
    assert "candidate_scoring_status: not_started" in content
    assert "approval_automation_status: not_changed" in content


def test_byte_loading_foundation_exit_review_lists_completed_capabilities() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "[x] Candidate image byte-loading design exists.",
        "[x] Candidate image byte-loading record schema exists.",
        "[x] Candidate image byte-loading record fixtures exist.",
        "[x] Candidate image byte-loading record discovery exists.",
        "[x] Candidate image byte-loading review packets exist.",
        "[x] byte-loading-list is documented.",
        "[x] byte-loading-show is documented.",
        "[x] byte-loading-review-packet is documented.",
        "[x] Static record fixtures preserve image_bytes_loaded false.",
        "[x] Static record fixtures preserve approval_allowed false.",
    ]
    for item in expected:
        assert item in content


def test_byte_loading_foundation_exit_review_lists_current_commands() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "cos-graphics-candidates byte-loading-list",
        "cos-graphics-candidates byte-loading-show perseverance",
        "cos-graphics-candidates byte-loading-show supra_2jz_gte_twin_turbo",
        "cos-graphics-candidates --format json --output reports/candidate-byte-loading-records.json byte-loading-list",
        "cos-graphics-candidates byte-loading-review-packet perseverance",
        "cos-graphics-candidates byte-loading-review-packet supra_2jz_gte_twin_turbo",
        "cos-graphics-candidates --format json --output reports/perseverance-byte-loading-review-packet.json byte-loading-review-packet perseverance",
    ]
    for command in expected:
        assert command in content


def test_byte_loading_foundation_exit_review_blocks_real_loading_work() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    blocked_items = [
        "Real image byte loading.",
        "Local file opening.",
        "Artifact download.",
        "Remote or network fetch.",
        "Image decoding.",
        "Pixel inspection.",
        "Computer-vision provider integration.",
        "OCR provider integration.",
        "Candidate scoring.",
        "Source report mutation.",
        "Automatic approval.",
    ]
    for item in blocked_items:
        assert item in content


def test_byte_loading_foundation_exit_review_sets_implementation_design_as_next_gate() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "next_allowed_milestone: Candidate Image Byte Loading Implementation Design v1" in content
    assert "decision: exit_fixture_only_byte_loading_metadata_after_verification" in content
    assert "The next safe step is an implementation design milestone, not image byte-loading implementation directly." in content


def test_byte_loading_foundation_exit_review_defines_required_implementation_boundaries() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "Candidate Image Byte Loading Implementation Design v1",
        "explicit implementation entry point boundaries",
        "allowed-root enforcement behavior",
        "path normalization behavior",
        "artifact registry lookup behavior",
        "checksum computation behavior",
        "size limit enforcement behavior",
        "media-type sniffing behavior",
        "safe failure reporting behavior",
        "confirmation that byte loading alone cannot approve candidates",
    ]
    for item in expected:
        assert item in content


def test_command_reference_and_readme_include_byte_loading_foundation_exit_context() -> None:
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert "Byte loading foundation exit review" in command_reference
    assert "pytest tests/test_byte_loading_foundation_exit_review.py" in command_reference
    assert "candidate_image_byte_loading_review_packet_status: fixture_only" in readme
    assert "byte-loading-review-packet" in readme
