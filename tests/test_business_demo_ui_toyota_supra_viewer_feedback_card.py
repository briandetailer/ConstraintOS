from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_CARD = ROOT / "docs" / "800_Demos" / "Business_Demo_UI_Toyota_Supra_Viewer_Feedback_Card.md"


def test_viewer_feedback_card_records_business_demo_context() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    assert "# Business Demo UI Toyota Supra Viewer Feedback Card" in content
    assert "status: viewer-feedback-card" in content
    assert "Business Demo UI Toyota Supra" in content
    assert "Toyota Supra A80 / 2JZ-GTE twin-turbo" in content
    assert "business reviewers" in content
    assert "without asking the reviewer to inspect terminal output, JSON files, source code, or internal milestone documents" in content


def test_viewer_feedback_card_collects_business_signal() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    expected = [
        "I understood the product idea.",
        "The demo made the business value clear.",
        "The Toyota Supra / 2JZ-GTE example helped me understand why constraints matter.",
        "The needs_review decision made sense.",
        "I would want to see the next demo showing constraint-derived output permutations.",
        "What business problem did this seem closest to solving?",
        "What would you need to see before believing this could be useful in a real workflow?",
    ]
    for item in expected:
        assert item in content


def test_viewer_feedback_card_defines_signal_classification() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    expected = [
        "strong_business_signal:",
        "weak_business_signal:",
        "next_demo_signal:",
        "reviewer understands trust / auditability value",
        "reviewer asks to see output permutations next",
        "reviewer asks how constraints change the output",
        "reviewer asks whether this can be used outside automotive examples",
    ]
    for item in expected:
        assert item in content


def test_viewer_feedback_card_preserves_current_demo_boundaries() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    expected = [
        "Do not promise generated final graphics in the current demo.",
        "Do not promise real local image input in the current demo.",
        "Do not promise image decoding, pixel inspection, CV/OCR, or automatic approval in the current demo.",
        "Do not describe the fixture-only browser UI as production software.",
        "Constraint-Driven Graphic Output Permutation POC v1",
    ]
    for item in expected:
        assert item in content


def test_viewer_feedback_card_has_local_verification_command() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    assert "pytest tests/test_business_demo_ui_toyota_supra_viewer_feedback_card.py" in content
