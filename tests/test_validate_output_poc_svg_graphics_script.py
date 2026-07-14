from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-output-poc-svg-graphics.ps1"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_validate_output_poc_svg_graphics_script_exists_and_targets_supra() -> None:
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


def test_validate_output_poc_svg_graphics_script_finds_latest_run_and_artifacts() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "$LatestRun = Get-ChildItem -Path $ScenarioRoot -Directory",
        "Sort-Object LastWriteTime -Descending",
        "Select-Object -First 1",
        "$GraphicsDir = Join-Path $LatestRun.FullName \"graphics\"",
        "$MetadataPath = Join-Path $LatestRun.FullName \"run-metadata.json\"",
        "$IndexPath = Join-Path $LatestRun.FullName \"index.html\"",
        "$ReviewPacketPath = Join-Path $LatestRun.FullName \"graphic-output-review-packet.json\"",
        "$ValidationReportPath = Join-Path $LatestRun.FullName \"svg-structural-validation.json\"",
    ]
    for item in expected:
        assert item in content


def test_validate_output_poc_svg_graphics_script_checks_expected_svg_files() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "turbo_system_focus.svg",
        "inline_six_engine_identity_focus.svg",
        "technical_label_density_focus.svg",
        "reviewer_safe_minimal_focus.svg",
        "Expected deterministic SVG graphic missing",
    ]
    for item in expected:
        assert item in content


def test_validate_output_poc_svg_graphics_script_checks_required_svg_markers() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "<svg xmlns=\"http://www.w3.org/2000/svg\"",
        "permutation_id: $PermutationId",
        "svg_artifact: $RelativePath",
        "review_decision: needs_review",
        "approval_allowed: false",
        "renderer: deterministic-svg-output-only",
        "id=\"deterministic-graphic-core\"",
        "id=\"traceability-labels\"",
        "id=\"evidence-summary\"",
        "Toyota Supra A80",
        "2JZ-GTE",
        "SVG validation failed",
    ]
    for item in expected:
        assert item in content


def test_validate_output_poc_svg_graphics_script_blocks_external_images_and_approval_claims() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    blocked = [
        "<image",
        "href=\"http",
        "href=\"file:",
        "xlink:href=\"http",
        "xlink:href=\"file:",
        "auto_approved",
        "production approval",
        "final production artwork approved",
        "Forbidden marker found",
    ]
    for item in blocked:
        assert item in content


def test_validate_output_poc_svg_graphics_script_checks_metadata_and_browser_links() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "$MetadataContent = Get-Content -Path $MetadataPath -Raw",
        "$IndexContent = Get-Content -Path $IndexPath -Raw",
        "Metadata validation failed. Missing SVG artifact reference",
        "Browser validation failed. Missing SVG artifact link",
    ]
    for item in expected:
        assert item in content


def test_validate_output_poc_svg_graphics_script_writes_validation_report() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "svg-structural-validation.json",
        "$ValidationReport = [ordered]@{",
        "validator = \"deterministic-svg-structural-validation\"",
        "result = \"passed\"",
        "validated_graphics_count = $ValidatedGraphics.Count",
        "blocked_scope_preserved = @(",
        "$ValidationReport | ConvertTo-Json -Depth 8 | Set-Content -Path $ValidationReportPath -Encoding UTF8",
        "Validation report:",
    ]
    for item in expected:
        assert item in content


def test_validate_output_poc_svg_graphics_script_surfaces_validation_in_review_packet() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "$ReviewPacket = Get-Content -Path $ReviewPacketPath -Raw | ConvertFrom-Json",
        "Add-Member -NotePropertyName \"svg_structural_validation\"",
        "report = \"svg-structural-validation.json\"",
        "validated_graphics_count = $ValidatedGraphics.Count",
        "$ReviewPacket | ConvertTo-Json -Depth 12 | Set-Content -Path $ReviewPacketPath -Encoding UTF8",
        "Review packet:",
    ]
    for item in expected:
        assert item in content


def test_validate_output_poc_svg_graphics_script_reports_success() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "Deterministic SVG graphics validation passed.",
        "Run directory:",
        "Graphics directory:",
        "Validation report:",
        "Review packet:",
    ]
    for item in expected:
        assert item in content


def test_validate_output_poc_svg_graphics_script_is_in_command_reference() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    expected = [
        "Constraint-driven output permutation POC - Toyota Supra",
        ".\\scripts\\validate-output-poc-svg-graphics.ps1",
        "pytest tests/test_validate_output_poc_svg_graphics_script.py",
        "checks that the latest generated SVG graphics exist",
        "contain required deterministic metadata",
        "are linked from `index.html`",
        "are referenced in `run-metadata.json`",
        "do not contain external image references or approval claims",
        "writes `svg-structural-validation.json` as a durable validation report",
        "adds a `svg_structural_validation` summary to `graphic-output-review-packet.json`",
    ]
    for item in expected:
        assert item in content
