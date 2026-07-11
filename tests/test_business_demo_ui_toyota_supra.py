from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Business_Demo_UI_Toyota_Supra_v1.md"
SCRIPT = ROOT / "scripts" / "watch-business-demo-ui.ps1"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_business_demo_ui_milestone_records_business_viewer_need() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "# Business Demo UI Toyota Supra v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "Current Evidence-Harness POC Demo package complete" in content
    assert "Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic" in content
    assert "business request -> constraints -> candidate evidence -> deterministic review -> needs_review decision" in content
    assert "business_viewer_can_follow_without_json: true" in content


def test_business_demo_ui_script_defaults_to_toyota_supra_use_case() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert "$Scenario = \"supra_2jz_gte_twin_turbo\"" in content
    assert "Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic" in content
    assert "Supra Mk IV / A80" in content
    assert "2JZ-GTE inline-six" in content
    assert "sequential twin-turbo" in content
    assert "Business Demo UI" in content or "business-demo-ui" in content


def test_business_demo_ui_script_writes_browser_artifacts() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "runs",
        "business-demo-ui",
        "index.html",
        "demo-data.json",
        "run-metadata.json",
        "Start-Process $IndexPath",
    ]
    for item in expected:
        assert item in content


def test_business_demo_ui_script_autoplays_workflow_in_browser() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "function play()",
        "setInterval",
        "play();",
        "Replay demo",
        "Next stage",
        "showStage(current + 1",
    ]
    for item in expected:
        assert item in content


def test_business_demo_ui_script_shows_business_workflow_and_decision() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "Business request",
        "Loaded constraints",
        "Candidate evidence",
        "Deterministic review",
        "Decision",
        "Next product step",
        "needs_review",
        "approval_allowed",
        "Approval allowed: false",
        "Constraint-Driven Graphic Output Permutation POC v1",
    ]
    for item in expected:
        assert item in content


def test_business_demo_ui_preserves_evidence_harness_guardrails() -> None:
    script_content = SCRIPT.read_text(encoding="utf-8")
    milestone_content = MILESTONE.read_text(encoding="utf-8")
    combined = script_content + "\n" + milestone_content

    expected = [
        "No generated final graphics",
        "No constraint-derived graphic output permutations yet",
        "No real local image input",
        "No local_file_path loading",
        "No file_uri loading",
        "No artifact download",
        "No network fetch",
        "No image decoding",
        "No pixel inspection",
        "No CV/OCR provider integration",
        "No unrestricted image generation",
        "No unrestricted image editing",
        "No automatic approval",
    ]
    for item in expected:
        assert item in combined


def test_command_reference_includes_business_demo_ui() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Business demo UI - Toyota Supra" in content
    assert ".\\scripts\\watch-business-demo-ui.ps1" in content
    assert ".\\scripts\\watch-business-demo-ui.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser" in content
    assert "pytest tests/test_business_demo_ui_toyota_supra.py" in content
    assert "runs/business-demo-ui/<scenario>/<timestamp>/index.html" in content
