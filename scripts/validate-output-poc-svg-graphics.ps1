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

if (-not (Test-Path $GraphicsDir)) {
    throw "Latest output POC run does not contain a graphics directory: $GraphicsDir"
}

if (-not (Test-Path $MetadataPath)) {
    throw "Latest output POC run does not contain run-metadata.json: $MetadataPath"
}

if (-not (Test-Path $IndexPath)) {
    throw "Latest output POC run does not contain index.html: $IndexPath"
}

$MetadataContent = Get-Content -Path $MetadataPath -Raw
$IndexContent = Get-Content -Path $IndexPath -Raw

$ExpectedGraphics = @(
    "turbo_system_focus.svg",
    "inline_six_engine_identity_focus.svg",
    "technical_label_density_focus.svg",
    "reviewer_safe_minimal_focus.svg"
)

foreach ($Graphic in $ExpectedGraphics) {
    $GraphicPath = Join-Path $GraphicsDir $Graphic
    if (-not (Test-Path $GraphicPath)) {
        throw "Expected deterministic SVG graphic missing: $GraphicPath"
    }

    $SvgContent = Get-Content -Path $GraphicPath -Raw
    $PermutationId = [System.IO.Path]::GetFileNameWithoutExtension($Graphic)
    $RelativePath = "graphics/$Graphic"

    $RequiredSvgMarkers = @(
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
        "2JZ-GTE"
    )

    foreach ($Marker in $RequiredSvgMarkers) {
        if ($SvgContent -notlike "*$Marker*") {
            throw "SVG validation failed for $GraphicPath. Missing marker: $Marker"
        }
    }

    $ForbiddenSvgMarkers = @(
        "<image",
        "href=\"http",
        "href=\"file:",
        "xlink:href=\"http",
        "xlink:href=\"file:",
        "auto_approved",
        "production approval",
        "final production artwork approved"
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
}

Write-Host "Deterministic SVG graphics validation passed." -ForegroundColor Green
Write-Host "Run directory: $($LatestRun.FullName)"
Write-Host "Graphics directory: $GraphicsDir"
foreach ($Graphic in $ExpectedGraphics) {
    Write-Host (Join-Path $GraphicsDir $Graphic)
}
