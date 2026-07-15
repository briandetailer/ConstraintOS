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

$IndexPath = Join-Path $LatestRun.FullName "index.html"

if (-not (Test-Path $IndexPath)) {
    throw "Latest output POC run does not contain index.html: $IndexPath"
}

$IndexContent = Get-Content -Path $IndexPath -Raw

$ExpectedBrowserMarkers = @(
    'ConstraintOS output permutation POC',
    'id="deterministic-svg-graphics"',
    'graphics/turbo_system_focus.svg',
    'graphics/inline_six_engine_identity_focus.svg',
    'graphics/technical_label_density_focus.svg',
    'graphics/reviewer_safe_minimal_focus.svg'
)

foreach ($Marker in $ExpectedBrowserMarkers) {
    if ($IndexContent -notlike "*$Marker*") {
        throw "Latest output POC browser UI is missing expected marker: $Marker"
    }
}

if ($IndexContent -notlike '*id="svg-structural-validation-summary"*') {
    Write-Host "Latest browser UI has no SVG structural validation summary yet. Run .\scripts\validate-output-poc-svg-graphics.ps1 to add it." -ForegroundColor Yellow
}

Write-Host "Latest ConstraintOS output browser UI:" -ForegroundColor Green
Write-Host $IndexPath

Start-Process $IndexPath
