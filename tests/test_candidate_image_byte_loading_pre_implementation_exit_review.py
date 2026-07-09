from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXIT_REVIEW = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Pre_Implementation_Exit_Review_v1.md"
IMPLEMENTATION_CONTRACT = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Implementation_Contract_v1.md"
IMPLEMENTATION_DESIGN = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Implementation_Design_v1.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_pre_implementation_exit_review_exists_and_is_pending_verification() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Pre-Implementation Exit Review v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "previous_gate: Candidate Image Byte Loading Implementation Contract v1 complete" in content
    assert "baseline: 487 passed" in content


def test_pre_implementation_exit_review_confirms_readiness_but_blocks_loading_until_verified() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "pre_implementation_readiness_status: ready_after_verification" in content
    assert "image_byte_loading_implementation_status: not_started" in content
    assert "local_file_opening_status: blocked" in content
    assert "artifact_download_status: blocked" in content
    assert "network_fetch_status: blocked" in content
    assert "image_decoding_status: not_started" in content
    assert "candidate_scoring_status: not_started" in content
    assert "approval_automation_status: not_changed" in content


def test_pre_implementation_exit_review_lists_completed_prerequisites() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "[x] Candidate Image Byte Loading Design v1 complete.",
        "[x] Candidate Image Byte Loading Contract v1 complete.",
        "[x] Candidate Image Byte Loading Discovery v1 complete.",
        "[x] Candidate Image Byte Loading Review Packet v1 complete.",
        "[x] Byte Loading Foundation Exit Review v1 complete.",
        "[x] Candidate Image Byte Loading Implementation Design v1 complete.",
        "[x] Candidate Image Byte Loading Implementation Contract v1 complete.",
        "[x] Future implementation entry point boundaries are defined.",
        "[x] Future byte-loading result contract is defined.",
        "[x] Future post-contract boundaries keep decoding, CV/OCR, scoring, and approval blocked.",
    ]
    for item in expected:
        assert item in content


def test_pre_implementation_exit_review_sets_minimal_implementation_as_next_allowed_milestone() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    assert "next_allowed_milestone: Candidate Image Byte Loading Minimal Implementation v1" in content
    assert "decision: exit_to_minimal_byte_loading_implementation_after_verification" in content
    assert "minimal byte-loading implementation milestone with narrow boundaries" in content


def test_pre_implementation_exit_review_sets_minimum_next_constraints() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "Implement the smallest possible byte-loading path only.",
        "Do not add HTTP or HTTPS fetch.",
        "Do not add implicit cloud download.",
        "Do not decode images.",
        "Do not inspect pixels.",
        "Do not integrate CV/OCR providers.",
        "Do not score candidates.",
        "Do not mutate source reports.",
        "Do not allow byte-loading success to approve candidates.",
        "Preserve safe failure records for all rejected references.",
    ]
    for item in expected:
        assert item in content


def test_pre_implementation_exit_review_requires_implementation_guardrails() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    expected = [
        "explicit entry point only",
        "validated byte-loading record input only",
        "explicit allowed root policy",
        "explicit artifact registry adapter boundary",
        "path normalization before any open attempt",
        "allowed-root confirmation before any open attempt",
        "size enforcement during read",
        "sha256 computation over exact loaded bytes",
        "declared/sniffed media-type comparison after checksum pass",
        "no decode until checksum and media-type pass",
        "no approval from byte loading alone",
    ]
    for item in expected:
        assert item in content


def test_pre_implementation_exit_review_keeps_later_work_blocked() -> None:
    content = EXIT_REVIEW.read_text(encoding="utf-8")

    blocked = [
        "Image decoding implementation.",
        "Pixel inspection.",
        "Computer-vision provider integration.",
        "OCR provider integration.",
        "Image generation integration.",
        "Image editing integration.",
        "Candidate scoring.",
        "Source report mutation.",
        "Automatic approval.",
    ]
    for item in blocked:
        assert item in content


def test_pre_implementation_exit_review_depends_on_completed_design_and_contract() -> None:
    implementation_contract = IMPLEMENTATION_CONTRACT.read_text(encoding="utf-8")
    implementation_design = IMPLEMENTATION_DESIGN.read_text(encoding="utf-8")

    assert "status: complete" in implementation_contract
    assert "latest_user_reported_candidate_image_byte_loading_implementation_contract_test_result: 10 passed" in implementation_contract
    assert "recommended_next_milestone: Candidate Image Byte Loading Pre-Implementation Exit Review v1" in implementation_contract
    assert "status: complete" in implementation_design
    assert "latest_user_reported_candidate_image_byte_loading_implementation_design_test_result: 9 passed" in implementation_design


def test_command_reference_includes_pre_implementation_exit_review_verification_command() -> None:
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Candidate image byte loading pre-implementation exit review" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_pre_implementation_exit_review.py" in command_reference
