param(
    [string]$Scenario = "supra_2jz_gte_twin_turbo",
    [switch]$NoOpenBrowser
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($Scenario -ne "supra_2jz_gte_twin_turbo") {
    throw "Unsupported scenario '$Scenario'. Supported scenario: supra_2jz_gte_twin_turbo."
}

$RepoRoot = Split-Path -Parent $PSScriptRoot
$GeneratorScript = Join-Path $PSScriptRoot "watch-constraintos-output-poc.ps1"
$ValidatorScript = Join-Path $PSScriptRoot "validate-output-poc-svg-graphics.ps1"
$BrowserHelperScript = Join-Path $PSScriptRoot "open-latest-output-poc-browser.ps1"
$ScenarioRoot = Join-Path $RepoRoot "runs\output-poc\$Scenario"

foreach ($RequiredScript in @($GeneratorScript, $ValidatorScript, $BrowserHelperScript)) {
    if (-not (Test-Path $RequiredScript)) {
        throw "Required validated output POC demo script is missing: $RequiredScript"
    }
}

Write-Host "Generating ConstraintOS output POC run..." -ForegroundColor Cyan
& $GeneratorScript -Scenario $Scenario

Write-Host "Validating deterministic SVG evidence and updating reviewer artifacts..." -ForegroundColor Cyan
& $ValidatorScript -Scenario $Scenario

$LatestRun = Get-ChildItem -Path $ScenarioRoot -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($null -eq $LatestRun) {
    throw "No output POC run directories found after validated demo launch for scenario '$Scenario'."
}

$IndexPath = Join-Path $LatestRun.FullName "index.html"
$ValidationReportPath = Join-Path $LatestRun.FullName "svg-structural-validation.json"
$ReviewPacketPath = Join-Path $LatestRun.FullName "graphic-output-review-packet.json"
$LauncherSummaryPath = Join-Path $LatestRun.FullName "validated-output-poc-demo-summary.json"

foreach ($ExpectedArtifact in @($IndexPath, $ValidationReportPath, $ReviewPacketPath)) {
    if (-not (Test-Path $ExpectedArtifact)) {
        throw "Validated output POC demo expected artifact missing: $ExpectedArtifact"
    }
}

$LauncherSummary = [ordered]@{
    launcher = "validated-output-poc-demo"
    scenario_key = $Scenario
    run_dir = $LatestRun.FullName
    browser_ui = $IndexPath
    validation_report = $ValidationReportPath
    review_packet = $ReviewPacketPath
    generated_at_local = (Get-Date).ToString("o")
    generator_script = "scripts/watch-constraintos-output-poc.ps1"
    validator_script = "scripts/validate-output-poc-svg-graphics.ps1"
    browser_helper_script = "scripts/open-latest-output-poc-browser.ps1"
    final_decision = "needs_review"
    approval_allowed = $false
    blocked_scope_preserved = @(
        "No real generated final graphics",
        "No production artwork generation",
        "No real local image input",
        "No external image references",
        "No image decoding",
        "No pixel inspection",
        "No CV/OCR provider integration",
        "No automatic approval"
    )
}

$LauncherSummary | ConvertTo-Json -Depth 8 | Set-Content -Path $LauncherSummaryPath -Encoding UTF8

$IndexContent = Get-Content -Path $IndexPath -Raw
$LauncherSummaryHtml = @"
    <section class="card" id="validated-output-poc-demo-summary">
      <div class="eyebrow">Validated demo launcher</div>
      <h2>One-command validated output POC complete</h2>
      <p>The validated launcher generated the output POC, ran deterministic SVG structural validation, wrote reviewer evidence artifacts, and preserved manual review blocking.</p>
      <div class="decision">
        <div class="metric"><div class="value">needs_review</div><p>final decision</p></div>
        <div class="metric"><div class="value">false</div><p>approval_allowed</p></div>
        <div class="metric"><div class="value">passed</div><p>SVG validation</p></div>
      </div>
      <p><strong>Launcher summary:</strong> <span class="artifact">validated-output-poc-demo-summary.json</span></p>
      <p><strong>Validation report:</strong> <span class="artifact">svg-structural-validation.json</span></p>
      <p><strong>Review packet:</strong> <span class="artifact">graphic-output-review-packet.json</span></p>
    </section>
"@

if ($IndexContent -like '*id="validated-output-poc-demo-summary"*') {
    $UpdatedIndexContent = $IndexContent
} else {
    $UpdatedIndexContent = $IndexContent.Replace("  </main>", "$LauncherSummaryHtml`r`n  </main>")
}
$UpdatedIndexContent | Set-Content -Path $IndexPath -Encoding UTF8

if ($NoOpenBrowser) {
    Write-Host "NoOpenBrowser was provided. Skipping latest browser UI launch." -ForegroundColor Yellow
} else {
    Write-Host "Opening latest validated output POC browser UI..." -ForegroundColor Cyan
    & $BrowserHelperScript -Scenario $Scenario
}

Write-Host "Validated ConstraintOS output POC demo complete." -ForegroundColor Green
Write-Host "Scenario: $Scenario"
Write-Host "Run directory: $($LatestRun.FullName)"
Write-Host "Browser UI: $IndexPath"
Write-Host "Validation report: $ValidationReportPath"
Write-Host "Review packet: $ReviewPacketPath"
Write-Host "Launcher summary: $LauncherSummaryPath"
Write-Host "Browser summary updated: $IndexPath"
Write-Host "Final decision remains: needs_review"
Write-Host "Approval allowed remains: false"
