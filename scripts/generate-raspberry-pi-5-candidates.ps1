param(
    [string]$OutputRoot,
    [switch]$Generate,
    [switch]$Validate,
    [int]$MaxRepairAttempts = 2,
    [switch]$DisableAutoRepair,
    [switch]$OpenResult
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($MaxRepairAttempts -lt 0 -or $MaxRepairAttempts -gt 5) {
    throw "MaxRepairAttempts must be between 0 and 5."
}

$CredentialHelper = Join-Path $PSScriptRoot "lib\openai-credential.ps1"
if (-not (Test-Path $CredentialHelper)) {
    throw "Missing ConstraintOS credential helper: $CredentialHelper"
}
. $CredentialHelper

$RepoRoot = Split-Path -Parent $PSScriptRoot
$RequestPath = Join-Path $RepoRoot "config\research-to-render-examples\raspberry-pi-5-io-plate-request.json"
$SourcesPath = Join-Path $RepoRoot "config\research-to-render-examples\raspberry-pi-5-discovered-sources.json"
$SourcePlateManifest = Join-Path $RepoRoot "reference-sources\raspberry_pi_5_io_plate\derived\source-plate-extraction-manifest.json"

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $RepoRoot "runs\research-to-render\raspberry-pi-5-candidate-generation"
}

foreach ($RequiredPath in @($RequestPath, $SourcesPath, $SourcePlateManifest)) {
    if (-not (Test-Path $RequiredPath)) {
        throw "Required generation input is missing: $RequiredPath"
    }
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH."
}
if ($Validate -and -not $Generate) {
    throw "-Validate requires -Generate because candidate images must exist first."
}
if ($Generate -or $Validate) {
    Ensure-ConstraintOSOpenAIKey | Out-Null
}

$Timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmss")
$RunRoot = Join-Path $OutputRoot $Timestamp
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
$PlanPath = Join-Path $RunRoot "research-to-render-plan.json"
$GenerationPackagePath = Join-Path $RunRoot "generation-package.json"
$CandidateManifestPath = Join-Path $RunRoot "generated-candidate-manifest.json"
$ValidationManifestPath = Join-Path $RunRoot "candidate-validation-manifest.json"
$RepairLoopManifestPath = Join-Path $RunRoot "candidate-repair-loop-manifest.json"
$CandidatePath = Join-Path $RunRoot "generated-candidates\candidate-01.png"
$FinalCandidatePath = $CandidatePath
$FinalValidationManifestPath = $ValidationManifestPath

Push-Location $RepoRoot
try {
    python -m runtime.research_to_render.cli `
        --request $RequestPath `
        --sources $SourcesPath `
        --output $PlanPath
    if ($LASTEXITCODE -ne 0) {
        throw "Research-to-render planning failed with exit code $LASTEXITCODE."
    }

    $Arguments = @(
        "-m", "runtime.research_to_render.candidate_generation",
        "--request", $RequestPath,
        "--plan", $PlanPath,
        "--source-plate-manifest", $SourcePlateManifest,
        "--output-root", $RunRoot
    )
    if ($Generate) {
        $Arguments += "--generate"
    }
    python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Reference-conditioned candidate generation failed with exit code $LASTEXITCODE."
    }

    if ($Validate) {
        python -m runtime.research_to_render.candidate_validation `
            --generation-package $GenerationPackagePath `
            --candidate-manifest $CandidateManifestPath `
            --output-root $RunRoot
        $InitialValidationExitCode = $LASTEXITCODE
        if ($InitialValidationExitCode -ne 0) {
            Write-Warning "Initial candidate validation rejected the output. Starting bounded repair when enabled."
        }

        if (-not $DisableAutoRepair -and $MaxRepairAttempts -gt 0) {
            python -m runtime.research_to_render.candidate_repair `
                --generation-package $GenerationPackagePath `
                --candidate-manifest $CandidateManifestPath `
                --validation-manifest $ValidationManifestPath `
                --output-root $RunRoot `
                --max-attempts $MaxRepairAttempts
            $RepairExitCode = $LASTEXITCODE
            if ($RepairExitCode -ne 0) {
                Write-Warning "The bounded repair loop ended without a machine pass. Manual review or additional research is required."
            }
            if (Test-Path $RepairLoopManifestPath) {
                $RepairSummary = Get-Content $RepairLoopManifestPath -Raw | ConvertFrom-Json
                if (-not [string]::IsNullOrWhiteSpace([string]$RepairSummary.final_candidate_file)) {
                    $FinalCandidatePath = [string]$RepairSummary.final_candidate_file
                }
                if (-not [string]::IsNullOrWhiteSpace([string]$RepairSummary.final_validation_manifest)) {
                    $FinalValidationManifestPath = [string]$RepairSummary.final_validation_manifest
                }
            }
        }
    }
}
finally {
    Pop-Location
}

Write-Host "ConstraintOS generation run: $RunRoot" -ForegroundColor Green
Write-Host "Generation package: $GenerationPackagePath"
if ($Generate) {
    Write-Host "Initial candidate: $CandidatePath"
    Write-Host "Initial candidate manifest: $CandidateManifestPath"
}
else {
    Write-Host "No image-provider call was made. Re-run with -Generate to create the candidate artwork."
}
if ($Validate) {
    Write-Host "Initial validation manifest: $ValidationManifestPath"
    if (Test-Path $RepairLoopManifestPath) {
        Write-Host "Repair-loop manifest: $RepairLoopManifestPath"
        Write-Host "Final candidate: $FinalCandidatePath"
        Write-Host "Final validation manifest: $FinalValidationManifestPath"
    }
}

if ($OpenResult) {
    if ($Generate -and (Test-Path $FinalCandidatePath)) {
        Start-Process $FinalCandidatePath
    }
    if ($Validate -and (Test-Path $FinalValidationManifestPath)) {
        Start-Process $FinalValidationManifestPath
    }
    if ($Validate -and (Test-Path $RepairLoopManifestPath)) {
        Start-Process $RepairLoopManifestPath
    }
    elseif (-not $Generate) {
        Start-Process $GenerationPackagePath
    }
}
