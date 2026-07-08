param(
    [string]$Contract = "perseverance",
    [int]$WatchDelayMs = 250,
    [switch]$PlanOnly
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$RunMode = if ($PlanOnly) { "plan-only" } else { "dry-run" }
$RunDir = Join-Path $RepoRoot "runs\graphics-contracts\$Contract\$Timestamp"

New-Item -ItemType Directory -Force -Path $RunDir | Out-Null

$TranscriptPath = Join-Path $RunDir "terminal-transcript.txt"
$WatchOutputPath = Join-Path $RunDir "watch-output.txt"
$JsonResultPath = Join-Path $RunDir "graphics-contract-runtime-result.json"
$MetadataPath = Join-Path $RunDir "run-metadata.json"

$Status = "success"
$ExitCode = 0
$StartedAt = Get-Date -Format "o"

function Invoke-GraphicsContracts {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    if (Get-Command cos-graphics-contracts -ErrorAction SilentlyContinue) {
        & cos-graphics-contracts @Arguments
        return
    }

    $existingPythonPath = $env:PYTHONPATH
    $env:PYTHONPATH = "$RepoRoot\src;$RepoRoot;$existingPythonPath"
    & python -m constraintos.graphics_contracts_cli @Arguments
}

$RunArgs = @("run", $Contract)
if ($PlanOnly) {
    $RunArgs += "--plan-only"
}

$WatchArgs = @($RunArgs + @("--watch", "--watch-delay-ms", "$WatchDelayMs"))
$JsonArgs = @("--format", "json", "--output", $JsonResultPath) + $RunArgs

Push-Location $RepoRoot
Start-Transcript -Path $TranscriptPath | Out-Null

try {
    Write-Host "ConstraintOS graphics contract runtime recording"
    Write-Host "contract: $Contract"
    Write-Host "run mode: $RunMode"
    Write-Host "run directory: $RunDir"
    Write-Host "watch output: $WatchOutputPath"
    Write-Host "json result: $JsonResultPath"
    Write-Host ""

    Invoke-GraphicsContracts @WatchArgs 2>&1 | Tee-Object -FilePath $WatchOutputPath
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) {
        throw "Graphics contract watch command failed with exit code $ExitCode."
    }

    Invoke-GraphicsContracts @JsonArgs
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) {
        throw "Graphics contract JSON result command failed with exit code $ExitCode."
    }
}
catch {
    $Status = "failed"
    if ($ExitCode -eq 0) {
        $ExitCode = 1
    }
    Write-Host "ERROR: $_" -ForegroundColor Red
}
finally {
    $CompletedAt = Get-Date -Format "o"
    $Metadata = [ordered]@{
        contract = $Contract
        status = $Status
        exit_code = $ExitCode
        run_mode = $RunMode
        started_at = $StartedAt
        completed_at = $CompletedAt
        run_directory = $RunDir
        transcript_path = $TranscriptPath
        watch_output_path = $WatchOutputPath
        json_result_path = $JsonResultPath
        metadata_path = $MetadataPath
        watch_delay_ms = $WatchDelayMs
        generated_by = "scripts/watch-graphics-contract.ps1"
    }
    $Metadata | ConvertTo-Json -Depth 4 | Set-Content -Path $MetadataPath -Encoding UTF8

    Write-Host ""
    Write-Host "Recording complete."
    Write-Host "Run directory: $RunDir"
    Write-Host "Terminal transcript: $TranscriptPath"
    Write-Host "Watch output: $WatchOutputPath"
    Write-Host "JSON result: $JsonResultPath"
    Write-Host "Run metadata: $MetadataPath"

    Stop-Transcript | Out-Null
    Pop-Location
}

exit $ExitCode
