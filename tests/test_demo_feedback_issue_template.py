from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ISSUE_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "demo-feedback.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_demo_feedback_issue_template_exists_and_has_metadata() -> None:
    content = ISSUE_TEMPLATE.read_text(encoding="utf-8")

    assert "name: Current POC Demo Feedback" in content
    assert "about: Share critique after reviewing the current evidence-harness POC demo" in content
    assert "labels: demo-feedback, current-poc, evidence-harness" in content
    assert "title: \"Demo feedback: \"" in content


def test_demo_feedback_issue_template_contains_feedback_form() -> None:
    content = ISSUE_TEMPLATE.read_text(encoding="utf-8")

    expected = [
        "Reviewer name:",
        "Scenario reviewed:",
        "Run folder reviewed:",
        "In one sentence, what do you think ConstraintOS does?",
        "Did the demo feel like a real workflow? Why or why not?",
        "Which stage was easiest to understand?",
        "Which stage was hardest to understand?",
        "Which evidence file was most useful?",
        "Which evidence file was least useful or confusing?",
        "Was the `needs_review` result clear?",
        "Was it clear that the current demo does not generate final graphics yet?",
        "What would you expect the future generated graphic-output permutations to look like?",
        "What would make this demo easier for a non-technical person?",
        "What would make this more convincing to a technical reviewer?",
        "What is the biggest product risk you see?",
        "What is the strongest part of the idea?",
        "What should be built next?",
    ]
    for item in expected:
        assert item in content


def test_demo_feedback_issue_template_preserves_labels_and_guardrails() -> None:
    content = ISSUE_TEMPLATE.read_text(encoding="utf-8")

    expected = [
        "product_clarity",
        "demo_flow",
        "evidence_quality",
        "technical_trust",
        "future_output_expectations",
        "ux_readability",
        "risk_or_gap",
        "next_step",
        "does not yet generate final graphics",
        "derive graphic-output permutations",
        "open arbitrary local images",
        "decode images",
        "run CV/OCR",
        "approve candidates automatically",
    ]
    for item in expected:
        assert item in content


def test_command_reference_includes_demo_feedback_issue_template() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Demo feedback issue template" in content
    assert ".github/ISSUE_TEMPLATE/demo-feedback.md" in content
    assert "pytest tests/test_demo_feedback_issue_template.py" in content
