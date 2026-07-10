param(
    [string]$Scenario = "perseverance",
    [int]$WatchDelayMs = 500,
    [switch]$OpenRunFolder
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$RunDir = Join-Path $RepoRoot "runs\poc-demo\$Scenario\$Timestamp"

New-Item -ItemType Directory -Force -Path $RunDir | Out-Null

$TranscriptPath = Join-Path $RunDir "terminal-transcript.txt"
$WatchOutputPath = Join-Path $RunDir "watch-output.txt"
$ContractJsonPath = Join-Path $RunDir "contract.json"
$CandidateManifestJsonPath = Join-Path $RunDir "candidate-manifest.json"
$CandidateIntakeJsonPath = Join-Path $RunDir "candidate-intake.json"
$CandidateIntakeReviewPacketJsonPath = Join-Path $RunDir "candidate-intake-review-packet.json"
$ByteLoadingJsonPath = Join-Path $RunDir "byte-loading.json"
$ByteLoadingReviewPacketJsonPath = Join-Path $RunDir "byte-loading-review-packet.json"
$RegistryReviewPacketJsonPath = Join-Path $RunDir "fixture-registry-review-packet.json"
$FailureReviewPacketJsonPath = Join-Path $RunDir "fixture-registry-failure-review-packet.json"
$ManualObservationsJsonPath = Join-Path $RunDir "manual-observations.json"
$ObservationBindingJsonPath = Join-Path $RunDir "observation-binding.json"
$MergedEvidenceJsonPath = Join-Path $RunDir "merged-evidence.json"
$EvaluationReportJsonPath = Join-Path $RunDir "evaluation-report.json"
$FinalReviewPacketJsonPath = Join-Path $RunDir "final-review-packet.json"
$DemoSummaryPath = Join-Path $RunDir "demo-summary.json"
$MetadataPath = Join-Path $RunDir "run-metadata.json"

$Status = "success"
$ExitCode = 0
$StartedAt = Get-Date -Format "o"

function Set-DemoPythonPath {
    param([string]$RepoRootPath)

    $existingPythonPath = $env:PYTHONPATH
    if ([string]::IsNullOrWhiteSpace($existingPythonPath)) {
        $env:PYTHONPATH = "$RepoRootPath\src;$RepoRootPath"
    }
    elseif ($existingPythonPath -notlike "*$RepoRootPath\src*") {
        $env:PYTHONPATH = "$RepoRootPath\src;$RepoRootPath;$existingPythonPath"
    }
}

function Invoke-GraphicsContracts {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    if (Get-Command cos-graphics-contracts -ErrorAction SilentlyContinue) {
        & cos-graphics-contracts @Arguments
        return
    }

    Set-DemoPythonPath $RepoRoot
    & python -m constraintos.graphics_contracts_cli @Arguments
}

function Invoke-GraphicsCandidates {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    if (Get-Command cos-graphics-candidates -ErrorAction SilentlyContinue) {
        & cos-graphics-candidates @Arguments
        return
    }

    Set-DemoPythonPath $RepoRoot
    & python -m constraintos.candidate_manifests_cli @Arguments
}

function Invoke-CandidateByteLoader {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    if (Get-Command cos-graphics-byte-loader -ErrorAction SilentlyContinue) {
        & cos-graphics-byte-loader @Arguments
        return
    }

    Set-DemoPythonPath $RepoRoot
    & python -m constraintos.candidate_image_byte_loader_cli @Arguments
}

function Assert-LastCommandSucceeded {
    param([string]$Description)

    $script:ExitCode = $LASTEXITCODE
    if ($script:ExitCode -ne 0) {
        throw "$Description failed with exit code $script:ExitCode."
    }
}

function Invoke-DemoStage {
    param(
        [string]$StageNumber,
        [string]$Title,
        [scriptblock]$Action
    )

    Write-Host ""
    Write-Host "[$StageNumber] $Title" -ForegroundColor Cyan
    & $Action
    Assert-LastCommandSucceeded $Title
    if ($WatchDelayMs -gt 0) {
        Start-Sleep -Milliseconds $WatchDelayMs
    }
}

Push-Location $RepoRoot
Start-Transcript -Path $TranscriptPath | Out-Null

try {
    Write-Host "ConstraintOS end-to-end fixture POC demo"
    Write-Host "scenario: $Scenario"
    Write-Host "run directory: $RunDir"
    Write-Host "watch output: $WatchOutputPath"
    Write-Host ""
    Write-Host "Demo principle: structured specifications, validation, and traceability are the source of truth."
    Write-Host "Boundary: fixture-based POC only; no local image file opening, download, network fetch, image decoding, CV/OCR, image generation/editing, automatic approval, or private data."

    {
        Invoke-DemoStage "1/10" "Load scenario" {
            Write-Host "scenario_key: $Scenario"
            Write-Host "demo_mode: fixture_based_poc"
            Write-Host "final_decision_target: needs_review"
            $global:LASTEXITCODE = 0
        }

        Invoke-DemoStage "2/10" "Load contract/specification" {
            Write-Host "command: cos-graphics-contracts show $Scenario"
            Invoke-GraphicsContracts @("show", $Scenario)
        }

        Invoke-DemoStage "3/10" "Load candidate manifest and intake evidence" {
            Write-Host "command: cos-graphics-candidates show $Scenario"
            Invoke-GraphicsCandidates @("show", $Scenario)
            Write-Host ""
            Write-Host "command: cos-graphics-candidates intake-show $Scenario"
            Invoke-GraphicsCandidates @("intake-show", $Scenario)
        }

        Invoke-DemoStage "4/10" "Validate intake boundaries through review packet evidence" {
            Write-Host "command: cos-graphics-candidates intake-review-packet $Scenario"
            Invoke-GraphicsCandidates @("intake-review-packet", $Scenario)
        }

        Invoke-DemoStage "5/10" "Load deterministic fixture bytes" {
            Write-Host "command: cos-graphics-byte-loader minimal $Scenario"
            Invoke-CandidateByteLoader @("minimal", $Scenario)
        }

        Invoke-DemoStage "6/10" "Generate byte-loading and registry evidence" {
            Write-Host "command: cos-graphics-byte-loader review-packet $Scenario"
            Invoke-CandidateByteLoader @("review-packet", $Scenario)
            Write-Host ""
            Write-Host "command: cos-graphics-byte-loader registry-review-packet"
            Invoke-CandidateByteLoader @("registry-review-packet")
        }

        Invoke-DemoStage "7/10" "Review fixture registry failure matrix" {
            Write-Host "command: cos-graphics-byte-loader failure-review-packet"
            Invoke-CandidateByteLoader @("failure-review-packet")
        }

        Invoke-DemoStage "8/10" "Load and bind observation evidence" {
            Write-Host "command: cos-graphics-candidates observe $Scenario"
            Invoke-GraphicsCandidates @("observe", $Scenario)
            Write-Host ""
            Write-Host "command: cos-graphics-candidates bind-observations $Scenario"
            Invoke-GraphicsCandidates @("bind-observations", $Scenario)
        }

        Invoke-DemoStage "9/10" "Merge evidence and evaluate candidate fixture report" {
            Write-Host "command: cos-graphics-candidates merge-evidence $Scenario"
            Invoke-GraphicsCandidates @("merge-evidence", $Scenario)
            Write-Host ""
            Write-Host "command: cos-graphics-candidates evaluate $Scenario"
            Invoke-GraphicsCandidates @("evaluate", $Scenario)
        }

        Invoke-DemoStage "10/10" "Produce final review packet and demo summary" {
            Write-Host "command: cos-graphics-candidates review-packet $Scenario"
            Invoke-GraphicsCandidates @("review-packet", $Scenario)

            $DemoSummary = [ordered]@{
                scenario = $Scenario
                demo = "End-to-End Fixture POC Demo"
                final_decision = "needs_review"
                approval_allowed = $false
                reason = "The system produced traceable fixture evidence and review packets, but automatic approval remains intentionally blocked in the POC."
                run_directory = $RunDir
                evidence_files = [ordered]@{
                    contract = $ContractJsonPath
                    candidate_manifest = $CandidateManifestJsonPath
                    candidate_intake = $CandidateIntakeJsonPath
                    candidate_intake_review_packet = $CandidateIntakeReviewPacketJsonPath
                    byte_loading = $ByteLoadingJsonPath
                    byte_loading_review_packet = $ByteLoadingReviewPacketJsonPath
                    fixture_registry_review_packet = $RegistryReviewPacketJsonPath
                    fixture_registry_failure_review_packet = $FailureReviewPacketJsonPath
                    manual_observations = $ManualObservationsJsonPath
                    observation_binding = $ObservationBindingJsonPath
                    merged_evidence = $MergedEvidenceJsonPath
                    evaluation_report = $EvaluationReportJsonPath
                    final_review_packet = $FinalReviewPacketJsonPath
                }
                blocked_capabilities = @(
                    "local_file_path loading",
                    "file_uri loading",
                    "artifact download",
                    "network fetch",
                    "image decoding",
                    "pixel inspection",
                    "computer vision",
                    "OCR",
                    "image generation",
                    "image editing",
                    "automatic approval"
                )
            }
            $DemoSummary | ConvertTo-Json -Depth 6 | Set-Content -Path $DemoSummaryPath -Encoding UTF8
            Write-Host "demo_summary: $DemoSummaryPath"
            $global:LASTEXITCODE = 0
        }

        Write-Host ""
        Write-Host "[Evidence capture] Writing JSON evidence files" -ForegroundColor Cyan
        Invoke-GraphicsContracts @( "--format", "json", "--output", $ContractJsonPath, "show", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing contract JSON evidence." }
        Invoke-GraphicsCandidates @( "--format", "json", "--output", $CandidateManifestJsonPath, "show", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing candidate manifest JSON evidence." }
        Invoke-GraphicsCandidates @( "--format", "json", "--output", $CandidateIntakeJsonPath, "intake-show", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing candidate intake JSON evidence." }
        Invoke-GraphicsCandidates @( "--format", "json", "--output", $CandidateIntakeReviewPacketJsonPath, "intake-review-packet", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing candidate intake review packet JSON evidence." }
        Invoke-CandidateByteLoader @( "--format", "json", "--output", $ByteLoadingJsonPath, "minimal", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing byte-loading JSON evidence." }
        Invoke-CandidateByteLoader @( "--format", "json", "--output", $ByteLoadingReviewPacketJsonPath, "review-packet", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing byte-loading review packet JSON evidence." }
        Invoke-CandidateByteLoader @( "--format", "json", "--output", $RegistryReviewPacketJsonPath, "registry-review-packet" )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing fixture registry review packet JSON evidence." }
        Invoke-CandidateByteLoader @( "--format", "json", "--output", $FailureReviewPacketJsonPath, "failure-review-packet" )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing fixture registry failure review packet JSON evidence." }
        Invoke-GraphicsCandidates @( "--format", "json", "--output", $ManualObservationsJsonPath, "observe", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing manual observations JSON evidence." }
        Invoke-GraphicsCandidates @( "--format", "json", "--output", $ObservationBindingJsonPath, "bind-observations", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing observation binding JSON evidence." }
        Invoke-GraphicsCandidates @( "--format", "json", "--output", $MergedEvidenceJsonPath, "merge-evidence", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing merged evidence JSON evidence." }
        Invoke-GraphicsCandidates @( "--format", "json", "--output", $EvaluationReportJsonPath, "evaluate", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing evaluation report JSON evidence." }
        Invoke-GraphicsCandidates @( "--format", "json", "--output", $FinalReviewPacketJsonPath, "review-packet", $Scenario )
        if ($LASTEXITCODE -ne 0) { throw "Failed writing final review packet JSON evidence." }

        Write-Host ""
        Write-Host "Final POC result" -ForegroundColor Green
        Write-Host "final_decision: needs_review"
        Write-Host "approval_allowed: false"
        Write-Host "reason: traceable fixture evidence exists; automatic approval remains blocked."
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
        scenario = $Scenario
        status = $Status
        exit_code = $ExitCode
        started_at = $StartedAt
        completed_at = $CompletedAt
        run_directory = $RunDir
        transcript_path = $TranscriptPath
        watch_output_path = $WatchOutputPath
        demo_summary_path = $DemoSummaryPath
        metadata_path = $MetadataPath
        watch_delay_ms = $WatchDelayMs
        local_image_file_opening = "not_run"
        artifact_download = "not_run"
        network_fetch = "not_run"
        image_decoding = "not_run"
        candidate_scoring_automation = "not_run"
        source_report_mutation = "not_run"
        approval_automation = "not_run"
        approval_allowed = $false
        generated_by = "scripts/watch-constraintos-poc.ps1"
    }
    $Metadata | ConvertTo-Json -Depth 6 | Set-Content -Path $MetadataPath -Encoding UTF8

    Write-Host ""
    Write-Host "POC demo recording complete."
    Write-Host "Run directory: $RunDir"
    Write-Host "Terminal transcript: $TranscriptPath"
    Write-Host "Watch output: $WatchOutputPath"
    Write-Host "Demo summary: $DemoSummaryPath"
    Write-Host "Run metadata: $MetadataPath"

    if ($OpenRunFolder) {
        Invoke-Item $RunDir
    }

    Stop-Transcript | Out-Null
    Pop-Location
}

exit $ExitCode
