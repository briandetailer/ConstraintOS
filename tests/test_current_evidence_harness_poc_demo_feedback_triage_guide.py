from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIAGE_GUIDE = ROOT / "docs" / "800_Demos" / "Current_Evidence_Harness_POC_Demo_Feedback_Triage_Guide.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_feedback_triage_guide_exists_and_identifies_inputs() -> None:
    content = TRIAGE_GUIDE.read_text(encoding="utf-8")

    assert "# Current Evidence-Harness POC Demo Feedback Triage Guide" in content
    assert "status: triage-guide" in content
    assert "docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Packet.md" in content
    assert ".github/ISSUE_TEMPLATE/demo-feedback.md" in content
    assert "future_target_bank: Constraint-Driven Graphic Output Permutation POC v1" in content


def test_feedback_triage_guide_records_categories_and_severity() -> None:
    content = TRIAGE_GUIDE.read_text(encoding="utf-8")

    expected = [
        "product_clarity",
        "demo_flow",
        "evidence_quality",
        "technical_trust",
        "future_output_expectations",
        "ux_readability",
        "risk_or_gap",
        "next_step",
        "blocking",
        "high",
        "medium",
        "low",
        "later",
    ]
    for item in expected:
        assert item in content


def test_feedback_triage_guide_distinguishes_current_polish_from_later_milestones() -> None:
    content = TRIAGE_GUIDE.read_text(encoding="utf-8")

    current_demo_items = [
        "clearer README wording",
        "clearer demo narration",
        "better inspection order",
        "clearer explanation of needs_review",
        "better GitHub issue template wording",
    ]
    for item in current_demo_items:
        assert item in content

    later_items = [
        "generated final graphics",
        "constraint-derived graphic output permutations",
        "real local image file input",
        "image decoding",
        "CV/OCR provider integration",
        "unrestricted image generation",
        "automatic approval",
    ]
    for item in later_items:
        assert item in content


def test_feedback_triage_guide_preserves_guardrails_and_note_format() -> None:
    content = TRIAGE_GUIDE.read_text(encoding="utf-8")

    expected = [
        "Do not treat requests for generated graphics as a failure of the current evidence-harness demo.",
        "Do not treat needs_review as a negative outcome.",
        "Do not add new processing capabilities in response to feedback without a separate milestone.",
        "source:",
        "primary_category:",
        "secondary_categories:",
        "severity:",
        "current_demo_or_later_track:",
        "actionable_follow_up:",
        "recommended_next_step:",
    ]
    for item in expected:
        assert item in content


def test_feedback_triage_guide_command_reference_entry_exists() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Current evidence-harness POC demo feedback triage guide" in content
    assert "docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Triage_Guide.md" in content
    assert "pytest tests/test_current_evidence_harness_poc_demo_feedback_triage_guide.py" in content
