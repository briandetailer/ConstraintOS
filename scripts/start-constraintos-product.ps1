param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8765,
    [string]$JobRoot,
    [switch]$NoBrowser,
    [switch]$NoCredentialPrompt
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($Port -lt 1 -or $Port -gt 65535) {
    throw "Port must be between 1 and 65535."
}

$RepoRoot = Split-Path -Parent $PSScriptRoot
$CredentialHelper = Join-Path $PSScriptRoot "lib\openai-credential.ps1"
if (-not (Test-Path $CredentialHelper)) {
    throw "Missing ConstraintOS credential helper: $CredentialHelper"
}
. $CredentialHelper

if (-not $NoCredentialPrompt) {
    Ensure-ConstraintOSOpenAIKey | Out-Null
}
elseif (-not (Import-ConstraintOSOpenAIKey)) {
    Write-Warning "No OpenAI credential is available. Structured jobs can still be created, but natural-language intake and live research will fail until a credential is configured."
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH."
}

if ([string]::IsNullOrWhiteSpace($JobRoot)) {
    $JobRoot = Join-Path $RepoRoot "runs\product-jobs"
}
$ResolvedJobRoot = [IO.Path]::GetFullPath($JobRoot)
New-Item -ItemType Directory -Force -Path $ResolvedJobRoot | Out-Null
$env:CONSTRAINTOS_JOB_ROOT = $ResolvedJobRoot

$Url = "http://$HostAddress`:$Port/"
Write-Host "Starting ConstraintOS Image Jobs" -ForegroundColor Green
Write-Host "URL: $Url"
Write-Host "Job root: $ResolvedJobRoot"
Write-Host "Press Ctrl+C to stop the product server."

if (-not $NoBrowser) {
    Start-Process $Url
}

Push-Location $RepoRoot
try {
    python -m uvicorn runtime.product.api:app `
        --host $HostAddress `
        --port $Port
    if ($LASTEXITCODE -ne 0) {
        throw "ConstraintOS product server exited with code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}
