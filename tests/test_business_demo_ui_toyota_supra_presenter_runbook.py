from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "800_Demos" / "Business_Demo_UI_Toyota_Supra_Presenter_Runbook.md"


def test_presenter_runbook_exists_and_targets_business_reviewers() -> None:
    content = RUNBOOK.read_text(encoding="utf-8")

    assert "# Business Demo UI Toyota Supra Presenter Runbook" in content
    assert "primary_audience: business reviewers" in content
    assert "without requiring viewers to read terminal output, JSON files, source code, or internal milestone documents" in content
    assert "git pull --rebase origin phase-1-cli-tooling" in content
    assert ".\\scripts\\watch-business-demo-ui.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser" in content


def test_presenter_runbook_includes_plain_english_product_framing() -> None:
    content = RUNBOOK.read_text(encoding="utf-8")

    expected = [
        "not the final generated-graphics demo yet",
        "current evidence-harness demo presented in a business-friendly browser UI",
        "can we make AI-generated technical graphics auditable before anyone trusts them",
        "ConstraintOS turns a creative or technical request into a constraint-governed review process",
    ]
    for item in expected:
        assert item in content


def test_presenter_runbook_covers_business_demo_stages() -> None:
    content = RUNBOOK.read_text(encoding="utf-8")

    expected = [
        "Business request",
        "Loaded constraints",
        "Candidate evidence",
        "Deterministic review",
        "Decision",
        "Next product step",
        "Toyota Supra Mk IV / A80 twin-turbo technical graphic",
        "Supra A80, 2JZ-GTE inline-six, sequential twin-turbo, not a generic engine",
        "needs_review",
        "approval is blocked",
        "Constraint-Driven Graphic Output Permutation POC v1",
    ]
    for item in expected:
        assert item in content


def test_presenter_runbook_answers_likely_business_questions() -> None:
    content = RUNBOOK.read_text(encoding="utf-8")

    expected = [
        "Does it generate the final graphic yet?",
        "Why is needs_review a good result?",
        "Why use the Toyota Supra example?",
        "What is the commercial value?",
        "reducing trust risk in AI-assisted technical publishing",
    ]
    for item in expected:
        assert item in content


def test_presenter_runbook_preserves_guardrails() -> None:
    content = RUNBOOK.read_text(encoding="utf-8")

    expected = [
        "static and fixture-only",
        "does not generate final graphics yet",
        "does not decode or inspect real image files",
        "does not fetch the network",
        "does not use CV/OCR",
        "does not approve candidates automatically",
    ]
    for item in expected:
        assert item in content
