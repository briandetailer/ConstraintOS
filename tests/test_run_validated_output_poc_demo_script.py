from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run-validated-output-poc-demo.ps1"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_run_validated_output_poc_demo_script_exists_and_targets_supra() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "param(",
        '[string]$Scenario = "supra_2jz_gte_twin_turbo"',
        "[switch]$NoOpenBrowser",
        "Unsupported scenario",
        "Set-StrictMode -Version Latest",
    ]
    for item in expected:
        assert item in content


def test_run_validated_output_poc_demo_script_declares_required_scripts() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "$GeneratorScript = Join-Path $PSScriptRoot \"watch-constraintos-output-poc.ps1\"",
        "$ValidatorScript = Join-Path $PSScriptRoot \"validate-output-poc-svg-graphics.ps1\"",
        "$BrowserHelperScript = Join-Path $PSScriptRoot \"open-latest-output-poc-browser.ps1\"",
        "Required validated output POC demo script is missing",
    ]
    for item in expected:
        assert item in content


def test_run_validated_output_poc_demo_script_runs_generate_validate_open_in_order() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    generate = "& $GeneratorScript -Scenario $Scenario"
    validate = "& $ValidatorScript -Scenario $Scenario"
    open_browser = "& $BrowserHelperScript -Scenario $Scenario"

    assert generate in content
    assert validate in content
    assert open_browser in content
    assert content.index(generate) < content.index(validate) < content.index(open_browser)


def test_run_validated_output_poc_demo_script_writes_launcher_summary() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "$ScenarioRoot = Join-Path $RepoRoot \"runs\\output-poc\\$Scenario\"",
        "$LatestRun = Get-ChildItem -Path $ScenarioRoot -Directory",
        "$LauncherSummaryPath = Join-Path $LatestRun.FullName \"validated-output-poc-demo-summary.json\"",
        "$LauncherSummary = [ordered]@{",
        "launcher = \"validated-output-poc-demo\"",
        "browser_ui = $IndexPath",
        "validation_report = $ValidationReportPath",
        "review_packet = $ReviewPacketPath",
        "final_decision = \"needs_review\"",
        "approval_allowed = $false",
        "$LauncherSummary | ConvertTo-Json -Depth 8 | Set-Content -Path $LauncherSummaryPath -Encoding UTF8",
        "Launcher summary:",
    ]
    for item in expected:
        assert item in content


def test_run_validated_output_poc_demo_script_supports_terminal_only_mode() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "if ($NoOpenBrowser)",
        "NoOpenBrowser was provided. Skipping latest browser UI launch.",
        "Opening latest validated output POC browser UI...",
    ]
    for item in expected:
        assert item in content


def test_run_validated_output_poc_demo_script_reports_final_blocking_semantics() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "Validated ConstraintOS output POC demo complete.",
        "Run directory:",
        "Browser UI:",
        "Validation report:",
        "Review packet:",
        "Launcher summary:",
        "Final decision remains: needs_review",
        "Approval allowed remains: false",
    ]
    for item in expected:
        assert item in content


def test_run_validated_output_poc_demo_script_is_in_command_reference() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    expected = [
        "Constraint-driven output permutation POC - Toyota Supra",
        ".\\scripts\\run-validated-output-poc-demo.ps1",
        ".\\scripts\\run-validated-output-poc-demo.ps1 -NoOpenBrowser",
        "pytest tests/test_run_validated_output_poc_demo_script.py",
        "runs the output POC generator",
        "runs SVG structural validation",
        "opens the latest validated browser UI",
        "validated-output-poc-demo-summary.json",
    ]
    for item in expected:
        assert item in content
