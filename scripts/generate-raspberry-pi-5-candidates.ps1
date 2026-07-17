param(
    [string]$OutputRoot,
    [switch]$Generate,
    [switch]$OpenResult
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

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

$Timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmss")
$RunRoot = Join-Path $OutputRoot $Timestamp
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
$PlanPath = Join-Path $RunRoot "research-to-render-plan.json"
$GenerationPackagePath = Join-Path $RunRoot "generation-package.json"

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
}
finally {
    Pop-Location
}

Write-Host "ConstraintOS generation run: $RunRoot" -ForegroundColor Green
Write-Host "Generation package: $GenerationPackagePath"
if ($Generate) {
    Write-Host "Candidate manifest: $(Join-Path $RunRoot 'generated-candidate-manifest.json')"
}
else {
    Write-Host "No image-provider call was made. Re-run with -Generate to create the candidate artwork."
}

if ($OpenResult) {
    if ($Generate) {
        $Candidate = Join-Path $RunRoot "generated-candidates\candidate-01.png"
        if (Test-Path $Candidate) {
            Start-Process $Candidate
        }
        else {
            Start-Process $RunRoot
        }
    }
    else {
        Start-Process $GenerationPackagePath
    }
}
