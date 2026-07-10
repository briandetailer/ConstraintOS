param(
    [string]$Record = "perseverance",
    [int]$WatchDelayMs = 500
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$RunDir = Join-Path $RepoRoot "runs\candidate-byte-loader\$Record\$Timestamp"

New-Item -ItemType Directory -Force -Path $RunDir | Out-Null

$TranscriptPath = Join-Path $RunDir "terminal-transcript.txt"
$WatchOutputPath = Join-Path $RunDir "watch-output.txt"
$MinimalJsonPath = Join-Path $RunDir "minimal-byte-loading.json"
$ReviewPacketJsonPath = Join-Path $RunDir "minimal-review-packet.json"
$RegistryReviewPacketJsonPath = Join-Path $RunDir "fixture-registry-review-packet.json"
$FailureReviewPacketJsonPath = Join-Path $RunDir "fixture-registry-failure-review-packet.json"
$MetadataPath = Join-Path $RunDir "run-metadata.json"

$Status = "success"
$ExitCode = 0
$StartedAt = Get-Date -Format "o"

function Invoke-CandidateByteLoader {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    if (Get-Command cos-graphics-byte-loader -ErrorAction SilentlyContinue) {
        & cos-graphics-byte-loader @Arguments
        return
    }

    $existingPythonPath = $env:PYTHONPATH
    $env:PYTHONPATH = "$RepoRoot\src;$RepoRoot;$existingPythonPath"
    & python -m constraintos.candidate_image_byte_loader_cli @Arguments
}

function Invoke-DemoStage {
    param(
        [string]$StageNumber,
        [string]$Title,
        [string[]]$Arguments
    )

    Write-Host ""
    Write-Host "[$StageNumber] $Title" -ForegroundColor Cyan
    Write-Host "command: cos-graphics-byte-loader $($Arguments -join ' ')"
    Invoke-CandidateByteLoader @Arguments
    $script:ExitCode = $LASTEXITCODE
    if ($script:ExitCode -ne 0) {
        throw "Candidate byte-loader demo stage '$Title' failed with exit code $script:ExitCode."
    }
    if ($WatchDelayMs -gt 0) {
        Start-Sleep -Milliseconds $WatchDelayMs
    }
}

Push-Location $RepoRoot
Start-Transcript -Path $TranscriptPath | Out-Null

try {
    Write-Host "ConstraintOS candidate byte-loader demo watch"
    Write-Host "record: $Record"
    Write-Host "run directory: $RunDir"
    Write-Host "watch output: $WatchOutputPath"
    Write-Host ""
    Write-Host "Demo principle: structured specifications, validation, and traceability are the source of truth."
    Write-Host "Boundary: deterministic fixture bytes only; no local file opening, download, network fetch, image decoding, scoring, mutation, or approval."

    {
        Invoke-DemoStage "1/6" "Load deterministic fixture bytes for selected record" @("minimal", $Record)
        Invoke-DemoStage "2/6" "Build selected record byte-loading review packet" @("review-packet", $Record)
        Invoke-DemoStage "3/6" "Review deterministic fixture registry descriptors" @("registry-review-packet")
        Invoke-DemoStage "4/6" "Review fixture registry failure matrix" @("failure-review-packet")

        Write-Host ""
        Write-Host "[5/6] Capture JSON evidence files" -ForegroundColor Cyan
        Invoke-CandidateByteLoader @("--format", "json", "--output", $MinimalJsonPath, "minimal", $Record)
        if ($LASTEXITCODE -ne 0) { throw "Failed writing minimal byte-loading JSON evidence." }
        Invoke-CandidateByteLoader @("--format", "json", "--output", $ReviewPacketJsonPath, "review-packet", $Record)
        if ($LASTEXITCODE -ne 0) { throw "Failed writing minimal review-packet JSON evidence." }
        Invoke-CandidateByteLoader @("--format", "json", "--output", $RegistryReviewPacketJsonPath, "registry-review-packet")
        if ($LASTEXITCODE -ne 0) { throw "Failed writing fixture registry review-packet JSON evidence." }
        Invoke-CandidateByteLoader @("--format", "json", "--output", $FailureReviewPacketJsonPath, "failure-review-packet")
        if ($LASTEXITCODE -ne 0) { throw "Failed writing fixture registry failure-review-packet JSON evidence." }

        Write-Host ""
        Write-Host "[6/6] Final demo decision" -ForegroundColor Cyan
        Write-Host "initial_decision: needs_review"
        Write-Host "approval_allowed: false"
        Write-Host "reason: byte loading, registry validation, and failure-matrix review are evidence only; they cannot approve a candidate."
        Write-Host "blocked: local_file_path loading, file_uri loading, artifact download, network fetch, image decoding, pixel inspection, CV/OCR, image generation/editing, candidate scoring, report mutation, approval automation"
    } 2>&1 | Tee-Object -FilePath $WatchOutputPath
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
        record = $Record
        status = $Status
        exit_code = $ExitCode
        started_at = $StartedAt
        completed_at = $CompletedAt
        run_directory = $RunDir
        transcript_path = $TranscriptPath
        watch_output_path = $WatchOutputPath
        minimal_json_path = $MinimalJsonPath
        review_packet_json_path = $ReviewPacketJsonPath
        registry_review_packet_json_path = $RegistryReviewPacketJsonPath
        failure_review_packet_json_path = $FailureReviewPacketJsonPath
        metadata_path = $MetadataPath
        watch_delay_ms = $WatchDelayMs
        local_image_file_opening = "not_run"
        artifact_download = "not_run"
        network_fetch = "not_run"
        image_decoding = "not_run"
        candidate_scoring = "not_run"
        source_report_mutation = "not_run"
        approval_automation = "not_run"
        approval_allowed = $false
        generated_by = "scripts/watch-candidate-byte-loader.ps1"
    }
    $Metadata | ConvertTo-Json -Depth 4 | Set-Content -Path $MetadataPath -Encoding UTF8

    Write-Host ""
    Write-Host "Demo recording complete."
    Write-Host "Run directory: $RunDir"
    Write-Host "Terminal transcript: $TranscriptPath"
    Write-Host "Watch output: $WatchOutputPath"
    Write-Host "Minimal JSON: $MinimalJsonPath"
    Write-Host "Review packet JSON: $ReviewPacketJsonPath"
    Write-Host "Registry review packet JSON: $RegistryReviewPacketJsonPath"
    Write-Host "Failure review packet JSON: $FailureReviewPacketJsonPath"
    Write-Host "Run metadata: $MetadataPath"

    Stop-Transcript | Out-Null
    Pop-Location
}

exit $ExitCode
