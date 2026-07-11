from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS_LOG = ROOT / "docs" / "800_Demos" / "Business_Demo_UI_Toyota_Supra_Feedback_Synthesis_Log.md"


def test_business_demo_feedback_synthesis_log_records_scope() -> None:
    content = SYNTHESIS_LOG.read_text(encoding="utf-8")

    assert "# Business Demo UI Toyota Supra Feedback Synthesis Log" in content
    assert "status: implementation-complete-pending-test" in content
    assert "Business Demo UI Toyota Supra" in content
    assert "Business Demo UI_Toyota_Supra_Viewer_Feedback_Card".replace("UI_", "UI_") not in content
    assert "viewer_feedback_card: docs/800_Demos/Business_Demo_UI_Toyota_Supra_Viewer_Feedback_Card.md" in content
    assert "scenario_key: supra_2jz_gte_twin_turbo" in content


def test_business_demo_feedback_synthesis_log_tracks_business_signals() -> None:
    content = SYNTHESIS_LOG.read_text(encoding="utf-8")

    expected = [
        "whether viewers understood the ConstraintOS product idea",
        "whether the trust / auditability value was clear",
        "whether the needs_review decision made sense",
        "whether viewers asked to see output permutations next",
        "reviewer connects the product to a real review, publishing, compliance, brand, engineering, or documentation workflow",
        "strong_business_signal",
        "mixed_business_signal",
        "weak_business_signal",
    ]
    for item in expected:
        assert item in content


def test_business_demo_feedback_synthesis_log_has_synthesis_template_and_decision_rule() -> None:
    content = SYNTHESIS_LOG.read_text(encoding="utf-8")

    expected = [
        "review_session:",
        "reviewer_count:",
        "strong_signal_count:",
        "mixed_signal_count:",
        "weak_signal_count:",
        "business_workflows_named:",
        "requests_for_next_demo:",
        "recommended_next_action:",
        "Constraint-Driven Graphic Output Permutation POC v1",
        "pending_viewer_feedback",
    ]
    for item in expected:
        assert item in content


def test_business_demo_feedback_synthesis_log_preserves_guardrails() -> None:
    content = SYNTHESIS_LOG.read_text(encoding="utf-8")

    expected = [
        "documentation-only",
        "does not authorize generated final graphics",
        "does not authorize real local image input",
        "does not authorize image decoding, pixel inspection, CV/OCR, or automatic approval",
        "does not implement new runtime capability",
    ]
    for item in expected:
        assert item in content
