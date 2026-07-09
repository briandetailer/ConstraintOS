from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXIT_REVIEW = ROOT / "docs" / "500_Milestones" / "Foundation_Exit_Review_v1.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_foundation_exit_review_exists_and_is_pending_verification() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "milestone: Foundation Exit Review v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "previous_gate: Fixture-only Candidate Review Packet v1 complete" in content
    assert "baseline: 487 passed" in content


def test_foundation_exit_review_records_fixture_ready_status() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "foundation_track_status: fixture_only_foundation_ready" in content
    assert "real_image_ingestion_status: not_started" in content
    assert "candidate_scoring_status: not_started" in content
    assert "approval_automation_status: not_changed" in content


def test_foundation_exit_review_lists_completed_foundation_capabilities() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "[x] Reusable graphics-validation contracts exist.",
        "[x] Candidate manifest schema exists.",
        "[x] Fixture-only candidate evaluation exists.",
        "[x] Manual observation fixture adapter exists.",
        "[x] Observation-to-report binding exists.",
        "[x] Fixture-only observation evidence merge exists.",
        "[x] Fixture-only candidate review packet exists.",
    ]
    for item in expected:
        assert item in content


def test_foundation_exit_review_blocks_real_image_work() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    blocked_items = [
        "Real candidate image loading or decoding.",
        "Pixel inspection.",
        "Computer-vision provider integration.",
        "OCR provider integration.",
        "Image generation integration.",
        "Candidate scoring.",
        "Automatic approval.",
    ]
    for item in blocked_items:
        assert item in content


def test_foundation_exit_review_sets_real_image_intake_design_as_next_gate() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "next_allowed_milestone: Real Candidate Image Intake Design v1" in content
    assert "decision: exit_fixture_only_foundation_after_verification" in content
    assert "The next safe step is to design real candidate image intake boundaries, not implement image loading directly." in content


def test_foundation_exit_review_defines_required_intake_boundaries() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "Real Candidate Image Intake Design v1",
        "explicit accepted reference types",
        "allowed local/file/artifact URI states",
        "forbidden remote/network loading behavior",
        "image byte handling policy",
        "checksum and media-type expectations",
        "failure states for missing/unreadable images",
        "confirmation that approval remains blocked after intake-only work",
    ]
    for item in expected:
        assert item in content


def test_foundation_exit_review_lists_candidate_commands() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "cos-graphics-candidates list",
        "cos-graphics-candidates show perseverance",
        "cos-graphics-candidates evaluate perseverance",
        "cos-graphics-candidates observe perseverance",
        "cos-graphics-candidates bind-observations perseverance",
        "cos-graphics-candidates merge-evidence perseverance",
        "cos-graphics-candidates review-packet perseverance",
    ]
    for command in expected:
        assert command in content


def test_command_reference_includes_foundation_exit_review_verification() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Foundation exit review" in content
    assert "pytest tests/test_foundation_exit_review.py" in content
