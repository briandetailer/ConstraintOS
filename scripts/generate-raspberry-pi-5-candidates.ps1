param(
    [string]$OutputRoot,
    [switch]$Generate,
    [switch]$Validate,
    [switch]$OpenResult
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Import-PersistedOpenAIKey {
    $ProcessValue = [Environment]::GetEnvironmentVariable(
        "OPENAI_API_KEY",
        [EnvironmentVariableTarget]::Process
    )
    if (-not [string]::IsNullOrWhiteSpace($ProcessValue)) {
        return $true
    }

    $PersistedValue = [Environment]::GetEnvironmentVariable(
        "OPENAI_API_KEY",
        [EnvironmentVariableTarget]::User
    )
    if ([string]::IsNullOrWhiteSpace($PersistedValue)) {
        return $false
    }

    $env:OPENAI_API_KEY = $PersistedValue
    return $true
}

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
if (($Generate -or $Validate) -and -not (Import-PersistedOpenAIKey)) {
    throw "No persisted OpenAI API key was found. Run .\scripts\set-openai-api-key.ps1 once, then rerun this command."
}

$Timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmss")
$RunRoot = Join-Path $OutputRoot $Timestamp
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
$PlanPath = Join-Path $RunRoot "research-to-render-plan.json"
$GenerationPackagePath = Join-Path $RunRoot "generation-package.json"
$CandidateManifestPath = Join-Path $RunRoot "generated-candidate-manifest.json"
$ValidationManifestPath = Join-Path $RunRoot "candidate-validation-manifest.json"
$CandidatePath = Join-Path $RunRoot "generated-candidates\candidate-01.png"

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
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Candidate validation completed with rejected output. Review the evidence manifest."
        }
    }
}
finally {
    Pop-Location
}

Write-Host "ConstraintOS generation run: $RunRoot" -ForegroundColor Green
Write-Host "Generation package: $GenerationPackagePath"
if ($Generate) {
    Write-Host "Generated candidate: $CandidatePath"
    Write-Host "Candidate manifest: $CandidateManifestPath"
}
else {
    Write-Host "No image-provider call was made. Re-run with -Generate to create the candidate artwork."
}
if ($Validate) {
    Write-Host "Validation manifest: $ValidationManifestPath"
}

if ($OpenResult) {
    if ($Generate -and (Test-Path $CandidatePath)) {
        Start-Process $CandidatePath
    }
    if ($Validate -and (Test-Path $ValidationManifestPath)) {
        Start-Process $ValidationManifestPath
    }
    elseif (-not $Generate) {
        Start-Process $GenerationPackagePath
    }
}
