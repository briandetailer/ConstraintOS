param(
    [string]$Example = "perseverance",
    [int]$WatchDelayMs = 250
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$RunDir = Join-Path $RepoRoot "runs\graphics\$Example\$Timestamp"

New-Item -ItemType Directory -Force -Path $RunDir | Out-Null

$TranscriptPath = Join-Path $RunDir "terminal-transcript.txt"
$WatchOutputPath = Join-Path $RunDir "watch-output.txt"
$JsonResultPath = Join-Path $RunDir "graphics-validation-result.json"
$MetadataPath = Join-Path $RunDir "run-metadata.json"

$Status = "success"
$ExitCode = 0
$StartedAt = Get-Date -Format "o"

function Invoke-GraphicsValidate {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    if (Get-Command cos-graphics-validate -ErrorAction SilentlyContinue) {
        & cos-graphics-validate @Arguments
        return
    }

    $existingPythonPath = $env:PYTHONPATH
    $env:PYTHONPATH = "$RepoRoot\src;$RepoRoot;$existingPythonPath"
    & python -m constraintos.graphics_validation_cli @Arguments
}

Push-Location $RepoRoot
Start-Transcript -Path $TranscriptPath | Out-Null

try {
    Write-Host "ConstraintOS graphics validation recording"
    Write-Host "example: $Example"
    Write-Host "run directory: $RunDir"
    Write-Host "watch output: $WatchOutputPath"
    Write-Host "json result: $JsonResultPath"
    Write-Host ""

    Invoke-GraphicsValidate $Example --watch --watch-delay-ms $WatchDelayMs 2>&1 | Tee-Object -FilePath $WatchOutputPath
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) {
        throw "Graphics validation watch command failed with exit code $ExitCode."
    }

    Invoke-GraphicsValidate $Example --output $JsonResultPath
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) {
        throw "Graphics validation JSON result command failed with exit code $ExitCode."
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
        example = $Example
        status = $Status
        exit_code = $ExitCode
        started_at = $StartedAt
        completed_at = $CompletedAt
        run_directory = $RunDir
        transcript_path = $TranscriptPath
        watch_output_path = $WatchOutputPath
        json_result_path = $JsonResultPath
        metadata_path = $MetadataPath
        watch_delay_ms = $WatchDelayMs
        generated_by = "scripts/watch-perseverance.ps1"
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
