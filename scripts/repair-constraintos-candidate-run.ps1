param(
    [Parameter(Mandatory = $true)]
    [string]$RunRoot,
    [int]$MaxRepairAttempts = 2,
    [switch]$OpenResult
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($MaxRepairAttempts -lt 1 -or $MaxRepairAttempts -gt 5) {
    throw "MaxRepairAttempts must be between 1 and 5."
}

$CredentialHelper = Join-Path $PSScriptRoot "lib\openai-credential.ps1"
if (-not (Test-Path $CredentialHelper)) {
    throw "Missing ConstraintOS credential helper: $CredentialHelper"
}
. $CredentialHelper
Ensure-ConstraintOSOpenAIKey | Out-Null

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ResolvedRunRoot = (Resolve-Path $RunRoot).Path
$GenerationPackagePath = Join-Path $ResolvedRunRoot "generation-package.json"
$CandidateManifestPath = Join-Path $ResolvedRunRoot "generated-candidate-manifest.json"
$ValidationManifestPath = Join-Path $ResolvedRunRoot "candidate-validation-manifest.json"
$RepairLoopManifestPath = Join-Path $ResolvedRunRoot "candidate-repair-loop-manifest.json"

foreach ($RequiredPath in @(
    $GenerationPackagePath,
    $CandidateManifestPath,
    $ValidationManifestPath
)) {
    if (-not (Test-Path $RequiredPath)) {
        throw "The supplied run is missing a required repair input: $RequiredPath"
    }
}

Push-Location $RepoRoot
try {
    python -m runtime.research_to_render.candidate_repair `
        --generation-package $GenerationPackagePath `
        --candidate-manifest $CandidateManifestPath `
        --validation-manifest $ValidationManifestPath `
        --output-root $ResolvedRunRoot `
        --max-attempts $MaxRepairAttempts
    $RepairExitCode = $LASTEXITCODE
}
finally {
    Pop-Location
}

if (-not (Test-Path $RepairLoopManifestPath)) {
    throw "Candidate repair did not produce its repair-loop manifest."
}

$RepairSummary = Get-Content $RepairLoopManifestPath -Raw | ConvertFrom-Json
$FinalCandidatePath = [string]$RepairSummary.final_candidate_file
$FinalValidationManifestPath = [string]$RepairSummary.final_validation_manifest

Write-Host "ConstraintOS candidate repair completed." -ForegroundColor Green
Write-Host "Repair attempts used: $($RepairSummary.attempts_used) / $($RepairSummary.max_attempts)"
Write-Host "Overall machine decision: $($RepairSummary.overall_machine_decision)"
Write-Host "Final candidate: $FinalCandidatePath"
Write-Host "Final validation manifest: $FinalValidationManifestPath"
Write-Host "Repair-loop manifest: $RepairLoopManifestPath"

if ($RepairExitCode -ne 0) {
    Write-Warning "The bounded repair loop ended without a machine pass. Manual review or additional research is required."
}

if ($OpenResult) {
    if (Test-Path $FinalCandidatePath) {
        Start-Process $FinalCandidatePath
    }
    if (Test-Path $FinalValidationManifestPath) {
        Start-Process $FinalValidationManifestPath
    }
    Start-Process $RepairLoopManifestPath
}
