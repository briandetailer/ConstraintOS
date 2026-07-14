from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "open-latest-output-poc-graphics.ps1"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_open_latest_output_poc_graphics_script_exists_and_targets_supra() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "param(",
        '[string]$Scenario = "supra_2jz_gte_twin_turbo"',
        "Unsupported scenario",
        "runs\\output-poc\\$Scenario",
        "Run .\\scripts\\watch-constraintos-output-poc.ps1 -Scenario $Scenario first.",
    ]
    for item in expected:
        assert item in content


def test_open_latest_output_poc_graphics_script_finds_latest_run_and_graphics_dir() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "Get-ChildItem -Path $ScenarioRoot -Directory",
        "Sort-Object LastWriteTime -Descending",
        "Select-Object -First 1",
        '$GraphicsDir = Join-Path $LatestRun.FullName "graphics"',
        "Latest output POC run does not contain a graphics directory",
    ]
    for item in expected:
        assert item in content


def test_open_latest_output_poc_graphics_script_checks_expected_svg_files() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        '$ExpectedGraphics = @(',
        '"turbo_system_focus.svg"',
        '"inline_six_engine_identity_focus.svg"',
        '"technical_label_density_focus.svg"',
        '"reviewer_safe_minimal_focus.svg"',
        "Expected deterministic SVG graphic missing",
    ]
    for item in expected:
        assert item in content


def test_open_latest_output_poc_graphics_script_prints_paths_and_opens_folder() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "Latest ConstraintOS output graphics folder:",
        "Generated deterministic SVG graphics:",
        "Write-Host (Join-Path $GraphicsDir $Graphic)",
        "Start-Process $GraphicsDir",
    ]
    for item in expected:
        assert item in content


def test_open_latest_output_poc_graphics_script_is_in_command_reference() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    expected = [
        ".\\scripts\\open-latest-output-poc-graphics.ps1",
        "opens the latest generated deterministic SVG graphics folder",
        "pytest tests/test_open_latest_output_poc_graphics_script.py",
    ]
    for item in expected:
        assert item in content
