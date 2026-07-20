param(
    [string]$OutputRoot,
    [switch]$LiveWebSearch,
    [string]$ResearchModel,
    [switch]$OpenResult
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$CredentialHelper = Join-Path $PSScriptRoot "lib\openai-credential.ps1"
if (-not (Test-Path $CredentialHelper)) {
    throw "Missing ConstraintOS credential helper: $CredentialHelper"
}
. $CredentialHelper

$RepoRoot = Split-Path -Parent $PSScriptRoot
$RequestPath = Join-Path $RepoRoot "config\research-to-render-examples\raspberry-pi-5-io-plate-request.json"
$SourcesPath = Join-Path $RepoRoot "config\research-to-render-examples\raspberry-pi-5-discovered-sources.json"

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $RepoRoot "runs\research-to-render\raspberry-pi-5-io-plate"
}

if (-not (Test-Path $RequestPath)) {
    throw "Missing request fixture: $RequestPath"
}
if (-not $LiveWebSearch -and -not (Test-Path $SourcesPath)) {
    throw "Missing discovered-source fixture: $SourcesPath"
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH."
}
if ($LiveWebSearch) {
    Ensure-ConstraintOSOpenAIKey | Out-Null
}

$Timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmss")
$RunRoot = Join-Path $OutputRoot $Timestamp
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
$OutputPath = Join-Path $RunRoot "research-to-render-plan.json"

$Arguments = @(
    "-m",
    "runtime.research_to_render.cli",
    "--request",
    $RequestPath,
    "--output",
    $OutputPath
)
if ($LiveWebSearch) {
    $Arguments += "--live-web-search"
    if (-not [string]::IsNullOrWhiteSpace($ResearchModel)) {
        $Arguments += @("--research-model", $ResearchModel)
    }
}
else {
    $Arguments += @("--sources", $SourcesPath)
}

Push-Location $RepoRoot
try {
    python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Research-to-render planning failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

$DiscoveryMode = if ($LiveWebSearch) { "live OpenAI web search" } else { "recorded source fixture" }
Write-Host "Research-to-render plan created." -ForegroundColor Green
Write-Host "Discovery mode: $DiscoveryMode"
Write-Host "Output: $OutputPath"

if ($OpenResult) {
    Start-Process $OutputPath
}
