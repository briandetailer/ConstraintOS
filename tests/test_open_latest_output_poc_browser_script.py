from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "open-latest-output-poc-browser.ps1"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_open_latest_output_poc_browser_script_exists_and_targets_supra() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "param(",
        '[string]$Scenario = "supra_2jz_gte_twin_turbo"',
        "Unsupported scenario",
        'runs\\output-poc\\$Scenario',
        "Run .\\scripts\\watch-constraintos-output-poc.ps1 -Scenario $Scenario first.",
    ]
    for item in expected:
        assert item in content


def test_open_latest_output_poc_browser_script_finds_latest_run_and_index() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "$LatestRun = Get-ChildItem -Path $ScenarioRoot -Directory",
        "Sort-Object LastWriteTime -Descending",
        "Select-Object -First 1",
        "$IndexPath = Join-Path $LatestRun.FullName \"index.html\"",
        "Latest output POC run does not contain index.html",
    ]
    for item in expected:
        assert item in content


def test_open_latest_output_poc_browser_script_checks_expected_browser_markers() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "$ExpectedBrowserMarkers = @(",
        "ConstraintOS output permutation POC",
        "id=\"deterministic-svg-graphics\"",
        "graphics/turbo_system_focus.svg",
        "graphics/inline_six_engine_identity_focus.svg",
        "graphics/technical_label_density_focus.svg",
        "graphics/reviewer_safe_minimal_focus.svg",
        "Latest output POC browser UI is missing expected marker",
    ]
    for item in expected:
        assert item in content


def test_open_latest_output_poc_browser_script_warns_when_validation_summary_missing() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "id=\"svg-structural-validation-summary\"",
        "Latest browser UI has no SVG structural validation summary yet.",
        "Run .\\scripts\\validate-output-poc-svg-graphics.ps1 to add it.",
        "ForegroundColor Yellow",
    ]
    for item in expected:
        assert item in content


def test_open_latest_output_poc_browser_script_reports_and_opens_index() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "Latest ConstraintOS output browser UI:",
        "Write-Host $IndexPath",
        "Start-Process $IndexPath",
    ]
    for item in expected:
        assert item in content


def test_open_latest_output_poc_browser_script_is_in_command_reference() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    expected = [
        "Constraint-driven output permutation POC - Toyota Supra",
        ".\\scripts\\open-latest-output-poc-browser.ps1",
        "pytest tests/test_open_latest_output_poc_browser_script.py",
        "opens the latest generated browser UI",
        "warns if the SVG structural validation summary has not been added yet",
    ]
    for item in expected:
        assert item in content
