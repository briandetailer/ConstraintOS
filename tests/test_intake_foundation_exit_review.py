from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXIT_REVIEW = ROOT / "docs" / "500_Milestones" / "Intake_Foundation_Exit_Review_v1.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_intake_foundation_exit_review_exists_and_is_pending_verification() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "milestone: Intake Foundation Exit Review v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "previous_gate: Candidate Intake Review Packet v1 complete" in content
    assert "baseline: 487 passed" in content


def test_intake_foundation_exit_review_records_fixture_ready_status() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "intake_foundation_status: fixture_only_intake_metadata_ready" in content
    assert "real_image_byte_loading_status: not_started" in content
    assert "image_decoding_status: not_started" in content
    assert "pixel_inspection_status: not_started" in content
    assert "network_fetch_status: blocked" in content
    assert "candidate_scoring_status: not_started" in content
    assert "approval_automation_status: not_changed" in content


def test_intake_foundation_exit_review_lists_completed_intake_capabilities() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "[x] Real candidate image intake design exists.",
        "[x] Candidate intake manifest contract exists.",
        "[x] Candidate intake manifest fixtures exist.",
        "[x] Candidate intake manifest discovery exists.",
        "[x] Candidate intake review packet exists.",
        "[x] Accepted reference types are limited to artifact_uri, local_file_path, and file_uri.",
        "[x] HTTP/HTTPS and arbitrary network fetching remain blocked.",
        "[x] Intake metadata cannot approve candidates.",
        "[x] Intake review packets cannot approve candidates.",
    ]
    for item in expected:
        assert item in content


def test_intake_foundation_exit_review_lists_intake_commands() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "cos-graphics-candidates intake-list",
        "cos-graphics-candidates intake-show perseverance",
        "cos-graphics-candidates intake-show supra_2jz_gte_twin_turbo",
        "cos-graphics-candidates intake-review-packet perseverance",
        "cos-graphics-candidates intake-review-packet supra_2jz_gte_twin_turbo",
        "cos-graphics-candidates --format json --output reports/perseverance-intake-review-packet.json intake-review-packet perseverance",
    ]
    for command in expected:
        assert command in content


def test_intake_foundation_exit_review_blocks_image_handling_work() -> None:
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


def test_intake_foundation_exit_review_sets_byte_loading_design_as_next_gate() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "next_allowed_milestone: Candidate Image Byte Loading Design v1" in content
    assert "decision: exit_fixture_only_intake_metadata_after_verification" in content
    assert "The next safe step is to design image byte loading boundaries, not implement image byte loading directly." in content


def test_intake_foundation_exit_review_defines_required_byte_loading_boundaries() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "Candidate Image Byte Loading Design v1",
        "explicit allowed roots for local_file_path and file_uri",
        "artifact_uri resolution policy",
        "maximum byte size policy",
        "checksum verification order",
        "media-type sniffing policy",
        "byte-count recording policy",
        "safe failure states",
        "confirmation that byte loading alone cannot approve candidates",
    ]
    for item in expected:
        assert item in content


def test_command_reference_includes_intake_foundation_exit_review_verification() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Intake foundation exit review" in content
    assert "pytest tests/test_intake_foundation_exit_review.py" in content
