param(
    [string]$Scenario = "supra_2jz_gte_twin_turbo",
    [switch]$NoOpenBrowser
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($Scenario -ne "supra_2jz_gte_twin_turbo") {
    throw "Unsupported scenario '$Scenario'. Supported scenario: supra_2jz_gte_twin_turbo."
}

$GeneratorScript = Join-Path $PSScriptRoot "watch-constraintos-output-poc.ps1"
$ValidatorScript = Join-Path $PSScriptRoot "validate-output-poc-svg-graphics.ps1"
$BrowserHelperScript = Join-Path $PSScriptRoot "open-latest-output-poc-browser.ps1"

foreach ($RequiredScript in @($GeneratorScript, $ValidatorScript, $BrowserHelperScript)) {
    if (-not (Test-Path $RequiredScript)) {
        throw "Required validated output POC demo script is missing: $RequiredScript"
    }
}

Write-Host "Generating ConstraintOS output POC run..." -ForegroundColor Cyan
& $GeneratorScript -Scenario $Scenario

Write-Host "Validating deterministic SVG evidence and updating reviewer artifacts..." -ForegroundColor Cyan
& $ValidatorScript -Scenario $Scenario

if ($NoOpenBrowser) {
    Write-Host "NoOpenBrowser was provided. Skipping latest browser UI launch." -ForegroundColor Yellow
} else {
    Write-Host "Opening latest validated output POC browser UI..." -ForegroundColor Cyan
    & $BrowserHelperScript -Scenario $Scenario
}

Write-Host "Validated ConstraintOS output POC demo complete." -ForegroundColor Green
Write-Host "Scenario: $Scenario"
Write-Host "Final decision remains: needs_review"
Write-Host "Approval allowed remains: false"
