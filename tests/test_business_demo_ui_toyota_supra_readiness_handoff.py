from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "800_Demos" / "Business_Demo_UI_Toyota_Supra_Readiness_Handoff.md"


def test_business_demo_ui_toyota_supra_readiness_handoff_exists_and_is_ready_to_show() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    assert "# Business Demo UI Toyota Supra Readiness Handoff" in content
    assert "status: ready-to-show" in content
    assert "scenario_key: supra_2jz_gte_twin_turbo" in content
    assert "primary_audience: business reviewers" in content


def test_business_demo_ui_toyota_supra_readiness_handoff_has_one_command_demo_path() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    assert "git pull --rebase origin phase-1-cli-tooling" in content
    assert ".\\scripts\\watch-business-demo-ui.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser" in content
    assert "Let auto-play run once" in content
    assert "Ask the viewer whether they want to see output permutations next" in content


def test_business_demo_ui_toyota_supra_readiness_handoff_records_verification_status() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "business_demo_ui_test: 8 passed",
        "presenter_runbook_test: 5 passed",
        "viewer_feedback_card_test: 5 passed",
        "feedback_synthesis_log_test: 4 passed",
        "assistant_ran_tests: false",
    ]
    for item in expected:
        assert item in content


def test_business_demo_ui_toyota_supra_readiness_handoff_preserves_guardrails() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "No generated final graphics",
        "No constraint-derived graphic output permutations yet",
        "No real local image input",
        "No image decoding",
        "No pixel inspection",
        "No CV/OCR provider integration",
        "No network fetch",
        "No automatic approval",
    ]
    for item in expected:
        assert item in content
