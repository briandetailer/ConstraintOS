from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "exercise-constraintos.ps1"


def test_exercise_constraintos_script_exists_and_targets_supra() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "param(",
        '[string]$Scenario = "supra_2jz_gte_twin_turbo"',
        "[switch]$NoOpenBrowser",
        "Unsupported scenario",
        "Set-StrictMode -Version Latest",
        "Exercising ConstraintOS locally...",
    ]
    for item in expected:
        assert item in content


def test_exercise_constraintos_wraps_validated_demo_and_uses_latest_run() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        '$ValidatedDemoScript = Join-Path $PSScriptRoot "run-validated-output-poc-demo.ps1"',
        "& $ValidatedDemoScript -Scenario $Scenario -NoOpenBrowser",
        "$LatestRun = Get-ChildItem -Path $ScenarioRoot -Directory",
        "$WorkbenchPath = Join-Path $RunDir \"exercise-workbench.html\"",
        "$LauncherSummaryPath = Join-Path $RunDir \"validated-output-poc-demo-summary.json\"",
    ]
    for item in expected:
        assert item in content


def test_exercise_constraintos_requires_expected_artifacts() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "index.html",
        "run-metadata.json",
        "svg-structural-validation.json",
        "graphic-output-review-packet.json",
        "validated-output-poc-demo-summary.json",
        "turbo_system_focus.svg",
        "inline_six_engine_identity_focus.svg",
        "technical_label_density_focus.svg",
        "reviewer_safe_minimal_focus.svg",
        "Exercise Mode expected artifact missing",
    ]
    for item in expected:
        assert item in content


def test_exercise_constraintos_creates_visible_workbench() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "ConstraintOS Exercise Workbench",
        "Exercise Mode v1",
        "Loaded scenario",
        "Input constraints being exercised",
        "Generated output permutations",
        "Validation evidence",
        "What to inspect next",
        "Generated artifacts in this run",
        "Scope guardrails",
    ]
    for item in expected:
        assert item in content


def test_exercise_constraintos_embeds_all_four_svg_outputs() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        'object data="graphics/turbo_system_focus.svg"',
        'object data="graphics/inline_six_engine_identity_focus.svg"',
        'object data="graphics/technical_label_density_focus.svg"',
        'object data="graphics/reviewer_safe_minimal_focus.svg"',
        "Turbo system focus",
        "Inline-six identity focus",
        "Technical label density focus",
        "Reviewer-safe minimal focus",
    ]
    for item in expected:
        assert item in content


def test_exercise_constraintos_prints_short_exercise_summary() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "ConstraintOS Exercise Workbench ready.",
        "Run directory:",
        "Exercise workbench:",
        "Generated outputs: 4 SVG graphics",
        "Validation: passed",
        "Final decision remains: needs_review",
        "Approval allowed remains: false",
    ]
    for item in expected:
        assert item in content


def test_exercise_constraintos_preserves_scope_guardrails() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    blocked = [
        "No real generated final graphics",
        "No production artwork approval",
        "No local image input",
        "No image decoding",
        "No pixel inspection",
        "No CV/OCR integration",
        "No automatic approval",
    ]
    for item in blocked:
        assert item in content
