param(
    [string]$OutputRoot,
    [switch]$OpenResult
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$RequestPath = Join-Path $RepoRoot "config\research-to-render-examples\raspberry-pi-5-io-plate-request.json"
$SourcesPath = Join-Path $RepoRoot "config\research-to-render-examples\raspberry-pi-5-discovered-sources.json"

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $RepoRoot "runs\research-to-render\raspberry-pi-5-io-plate"
}

if (-not (Test-Path $RequestPath)) {
    throw "Missing request fixture: $RequestPath"
}
if (-not (Test-Path $SourcesPath)) {
    throw "Missing discovered-source fixture: $SourcesPath"
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH."
}

$Timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmss")
$RunRoot = Join-Path $OutputRoot $Timestamp
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
$OutputPath = Join-Path $RunRoot "research-to-render-plan.json"

Push-Location $RepoRoot
try {
    python -m runtime.research_to_render.cli `
        --request $RequestPath `
        --sources $SourcesPath `
        --output $OutputPath
    if ($LASTEXITCODE -ne 0) {
        throw "Research-to-render planning failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

Write-Host "Research-to-render plan created." -ForegroundColor Green
Write-Host "Output: $OutputPath"

if ($OpenResult) {
    Start-Process $OutputPath
}
