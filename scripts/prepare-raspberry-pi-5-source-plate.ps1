param(
    [string]$PackageRoot,
    [string]$OutputRoot,
    [switch]$OpenResult
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ContractPath = Join-Path $RepoRoot "config\research-source-plate-extraction\raspberry-pi-5-product-brief-v1.json"
if ([string]::IsNullOrWhiteSpace($PackageRoot)) {
    $PackageRoot = Join-Path $RepoRoot "reference-sources\raspberry_pi_5_io_plate"
}
if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $PackageRoot "derived"
}

$PackageManifest = Join-Path $PackageRoot "source-package-manifest.json"
if (-not (Test-Path $PackageManifest)) {
    throw "Missing Raspberry Pi source package manifest: $PackageManifest. Run prepare-technical-reference-source-package.ps1 first."
}
if (-not (Test-Path $ContractPath)) {
    throw "Missing Raspberry Pi source-plate extraction contract: $ContractPath"
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH."
}

Push-Location $RepoRoot
try {
    python -m runtime.research_to_render.source_plate `
        --package-root $PackageRoot `
        --contract $ContractPath `
        --output-root $OutputRoot
    if ($LASTEXITCODE -ne 0) {
        throw "Raspberry Pi source-plate extraction failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

$DerivedManifest = Join-Path $OutputRoot "source-plate-extraction-manifest.json"
if (-not (Test-Path $DerivedManifest)) {
    throw "Source-plate extraction completed without a derived manifest: $DerivedManifest"
}

$Result = Get-Content -Raw -Encoding UTF8 $DerivedManifest | ConvertFrom-Json
Write-Host "Raspberry Pi source plate extracted." -ForegroundColor Green
Write-Host "Status: $($Result.status)"
Write-Host "Output: $($Result.output_file)"
Write-Host "SHA-256: $($Result.output_sha256)"
Write-Host "Dimensions: $($Result.selected_raster.extracted_width) x $($Result.selected_raster.extracted_height)"
Write-Host "Approval allowed: $($Result.approval_allowed)"

if ($OpenResult) {
    Start-Process ([string]$Result.output_file)
}
