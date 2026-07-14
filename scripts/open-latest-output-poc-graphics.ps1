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

if (-not (Test-Path $GraphicsDir)) {
    throw "Latest output POC run does not contain a graphics directory: $GraphicsDir"
}

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
}

Write-Host "Latest ConstraintOS output graphics folder:" -ForegroundColor Green
Write-Host $GraphicsDir
Write-Host ""
Write-Host "Generated deterministic SVG graphics:"
foreach ($Graphic in $ExpectedGraphics) {
    Write-Host (Join-Path $GraphicsDir $Graphic)
}

Start-Process $GraphicsDir
