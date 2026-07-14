param(
    [string]$Scenario = "supra_2jz_gte_twin_turbo"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($Scenario -ne "supra_2jz_gte_twin_turbo") {
    throw "Unsupported scenario '$Scenario'. Supported scenario: supra_2jz_gte_twin_turbo."
}

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ScenarioRoot = Join-Path $RepoRoot "runs\output-poc\$Scenario"

if (-not (Test-Path $ScenarioRoot)) {
    throw "No output POC runs found for scenario '$Scenario'. Run .\scripts\watch-constraintos-output-poc.ps1 -Scenario $Scenario first."
}

$LatestRun = Get-ChildItem -Path $ScenarioRoot -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($null -eq $LatestRun) {
    throw "No output POC run directories found for scenario '$Scenario'. Run .\scripts\watch-constraintos-output-poc.ps1 -Scenario $Scenario first."
}

$GraphicsDir = Join-Path $LatestRun.FullName "graphics"
$MetadataPath = Join-Path $LatestRun.FullName "run-metadata.json"
$IndexPath = Join-Path $LatestRun.FullName "index.html"
$ReviewPacketPath = Join-Path $LatestRun.FullName "graphic-output-review-packet.json"
$ValidationReportPath = Join-Path $LatestRun.FullName "svg-structural-validation.json"

if (-not (Test-Path $GraphicsDir)) {
    throw "Latest output POC run does not contain a graphics directory: $GraphicsDir"
}

if (-not (Test-Path $MetadataPath)) {
    throw "Latest output POC run does not contain run-metadata.json: $MetadataPath"
}

if (-not (Test-Path $IndexPath)) {
    throw "Latest output POC run does not contain index.html: $IndexPath"
}

if (-not (Test-Path $ReviewPacketPath)) {
    throw "Latest output POC run does not contain graphic-output-review-packet.json: $ReviewPacketPath"
}

$MetadataContent = Get-Content -Path $MetadataPath -Raw
$IndexContent = Get-Content -Path $IndexPath -Raw

$ExpectedGraphics = @(
    "turbo_system_focus.svg",
    "inline_six_engine_identity_focus.svg",
    "technical_label_density_focus.svg",
    "reviewer_safe_minimal_focus.svg"
)

$ValidatedGraphics = @()

foreach ($Graphic in $ExpectedGraphics) {
    $GraphicPath = Join-Path $GraphicsDir $Graphic
    if (-not (Test-Path $GraphicPath)) {
        throw "Expected deterministic SVG graphic missing: $GraphicPath"
    }

    $SvgContent = Get-Content -Path $GraphicPath -Raw
    $PermutationId = [System.IO.Path]::GetFileNameWithoutExtension($Graphic)
    $RelativePath = "graphics/$Graphic"

    $RequiredSvgMarkers = @(
        '<svg xmlns="http://www.w3.org/2000/svg"',
        "permutation_id: $PermutationId",
        "svg_artifact: $RelativePath",
        'review_decision: needs_review',
        'approval_allowed: false',
        'renderer: deterministic-svg-output-only',
        'id="deterministic-graphic-core"',
        'id="traceability-labels"',
        'id="evidence-summary"',
        'Toyota Supra A80',
        '2JZ-GTE'
    )

    foreach ($Marker in $RequiredSvgMarkers) {
        if ($SvgContent -notlike "*$Marker*") {
            throw "SVG validation failed for $GraphicPath. Missing marker: $Marker"
        }
    }

    $ForbiddenSvgMarkers = @(
        '<image',
        'href="http',
        'href="file:',
        'xlink:href="http',
        'xlink:href="file:',
        'auto_approved',
        'production approval',
        'final production artwork approved'
    )

    foreach ($Marker in $ForbiddenSvgMarkers) {
        if ($SvgContent -like "*$Marker*") {
            throw "SVG validation failed for $GraphicPath. Forbidden marker found: $Marker"
        }
    }

    if ($MetadataContent -notlike "*$RelativePath*") {
        throw "Metadata validation failed. Missing SVG artifact reference: $RelativePath"
    }

    if ($IndexContent -notlike "*$RelativePath*") {
        throw "Browser validation failed. Missing SVG artifact link: $RelativePath"
    }

    $ValidatedGraphics += [ordered]@{
        permutation_id = $PermutationId
        svg_artifact = $RelativePath
        svg_path = $GraphicPath
        required_markers_present = $true
        forbidden_markers_absent = $true
        metadata_reference_present = $true
        browser_link_present = $true
        review_decision = "needs_review"
        approval_allowed = $false
    }
}

$ValidationReport = [ordered]@{
    validator = "deterministic-svg-structural-validation"
    scenario_key = $Scenario
    run_dir = $LatestRun.FullName
    graphics_dir = $GraphicsDir
    validated_at_local = (Get-Date).ToString("o")
    result = "passed"
    final_decision = "needs_review"
    approval_allowed = $false
    validated_graphics_count = $ValidatedGraphics.Count
    validated_graphics = $ValidatedGraphics
    blocked_scope_preserved = @(
        "No real generated final graphics",
        "No production artwork generation",
        "No real local image input",
        "No external image references",
        "No image decoding",
        "No pixel inspection",
        "No CV/OCR provider integration",
        "No automatic approval"
    )
}

$ValidationReport | ConvertTo-Json -Depth 8 | Set-Content -Path $ValidationReportPath -Encoding UTF8

$ReviewPacket = Get-Content -Path $ReviewPacketPath -Raw | ConvertFrom-Json
$ReviewPacket | Add-Member -NotePropertyName "svg_structural_validation" -NotePropertyValue ([ordered]@{
    validator = "deterministic-svg-structural-validation"
    result = "passed"
    report = "svg-structural-validation.json"
    validated_graphics_count = $ValidatedGraphics.Count
    final_decision = "needs_review"
    approval_allowed = $false
}) -Force
$ReviewPacket | ConvertTo-Json -Depth 12 | Set-Content -Path $ReviewPacketPath -Encoding UTF8

$ValidationSummaryHtml = @"
    <section class="card" id="svg-structural-validation-summary">
      <div class="eyebrow">SVG structural validation</div>
      <h2>Deterministic SVG validation passed</h2>
      <p>The latest validator run confirmed all four generated SVG graphics exist, contain required deterministic metadata, are linked from this browser page, are referenced in run-metadata.json, and preserve approval blocking.</p>
      <div class="decision">
        <div class="metric"><div class="value">passed</div><p>svg_structural_validation</p></div>
        <div class="metric"><div class="value">4</div><p>validated SVG graphics</p></div>
        <div class="metric"><div class="value">false</div><p>approval_allowed</p></div>
      </div>
      <p><strong>Validation report:</strong> <span class="artifact">svg-structural-validation.json</span></p>
      <p><strong>Review packet:</strong> <span class="artifact">graphic-output-review-packet.json</span></p>
    </section>
"@

if ($IndexContent -like '*id="svg-structural-validation-summary"*') {
    $UpdatedIndexContent = $IndexContent
} else {
    $UpdatedIndexContent = $IndexContent.Replace("  </main>", "$ValidationSummaryHtml`r`n  </main>")
}
$UpdatedIndexContent | Set-Content -Path $IndexPath -Encoding UTF8

Write-Host "Deterministic SVG graphics validation passed." -ForegroundColor Green
Write-Host "Run directory: $($LatestRun.FullName)"
Write-Host "Graphics directory: $GraphicsDir"
Write-Host "Validation report: $ValidationReportPath"
Write-Host "Review packet: $ReviewPacketPath"
Write-Host "Browser UI updated: $IndexPath"
foreach ($Graphic in $ExpectedGraphics) {
    Write-Host (Join-Path $GraphicsDir $Graphic)
}
