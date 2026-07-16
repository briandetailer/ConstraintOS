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
$ValidatedDemoScript = Join-Path $PSScriptRoot "run-validated-output-poc-demo.ps1"
$ScenarioRoot = Join-Path $RepoRoot "runs\output-poc\$Scenario"

if (-not (Test-Path $ValidatedDemoScript)) {
    throw "Required validated demo launcher is missing: $ValidatedDemoScript"
}

Write-Host "Exercising ConstraintOS locally..." -ForegroundColor Cyan
& $ValidatedDemoScript -Scenario $Scenario -NoOpenBrowser

$LatestRun = Get-ChildItem -Path $ScenarioRoot -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($null -eq $LatestRun) {
    throw "No output POC run directories found after exercise launch for scenario '$Scenario'."
}

$RunDir = $LatestRun.FullName
$WorkbenchPath = Join-Path $RunDir "exercise-workbench.html"
$IndexPath = Join-Path $RunDir "index.html"
$MetadataPath = Join-Path $RunDir "run-metadata.json"
$ValidationReportPath = Join-Path $RunDir "svg-structural-validation.json"
$ReviewPacketPath = Join-Path $RunDir "graphic-output-review-packet.json"
$LauncherSummaryPath = Join-Path $RunDir "validated-output-poc-demo-summary.json"
$GraphicsDir = Join-Path $RunDir "graphics"

$ExpectedArtifacts = @(
    $IndexPath,
    $MetadataPath,
    $ValidationReportPath,
    $ReviewPacketPath,
    $LauncherSummaryPath,
    (Join-Path $GraphicsDir "turbo_system_focus.svg"),
    (Join-Path $GraphicsDir "inline_six_engine_identity_focus.svg"),
    (Join-Path $GraphicsDir "technical_label_density_focus.svg"),
    (Join-Path $GraphicsDir "reviewer_safe_minimal_focus.svg")
)

foreach ($ExpectedArtifact in $ExpectedArtifacts) {
    if (-not (Test-Path $ExpectedArtifact)) {
        throw "Exercise Mode expected artifact missing: $ExpectedArtifact"
    }
}

$GeneratedAt = (Get-Date).ToString("o")
$WorkbenchHtml = @"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ConstraintOS Exercise Workbench</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, Segoe UI, Arial, sans-serif; background: #0b1020; color: #e8eefc; }
    body { margin: 0; background: radial-gradient(circle at top left, #1b2b52 0, #0b1020 42%, #070a13 100%); }
    header { padding: 32px 40px 20px; border-bottom: 1px solid rgba(255,255,255,.12); }
    main { padding: 28px 40px 48px; display: grid; gap: 24px; }
    h1 { margin: 0 0 8px; font-size: 42px; letter-spacing: -0.03em; }
    h2 { margin: 0 0 14px; font-size: 24px; }
    h3 { margin: 0 0 8px; }
    p { color: #bdc7df; line-height: 1.55; }
    .subhead { font-size: 18px; max-width: 980px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
    .card { background: rgba(13, 21, 42, .82); border: 1px solid rgba(255,255,255,.14); border-radius: 18px; padding: 20px; box-shadow: 0 18px 40px rgba(0,0,0,.28); }
    .hero { display: grid; grid-template-columns: 1.15fr .85fr; gap: 18px; }
    .metric { background: rgba(255,255,255,.07); border-radius: 14px; padding: 14px; }
    .metric strong { display: block; font-size: 24px; color: white; }
    .pill { display: inline-block; margin: 4px 6px 4px 0; padding: 7px 10px; border-radius: 999px; background: rgba(123, 180, 255, .14); border: 1px solid rgba(123, 180, 255, .28); color: #d9e8ff; font-size: 13px; }
    .blocked { background: rgba(255, 99, 132, .12); border-color: rgba(255, 99, 132, .35); color: #ffd9e3; }
    .ok { background: rgba(95, 214, 157, .12); border-color: rgba(95, 214, 157, .35); color: #d9ffe9; }
    .outputs { display: grid; grid-template-columns: repeat(2, minmax(320px, 1fr)); gap: 18px; }
    .output-card object { width: 100%; min-height: 280px; background: white; border-radius: 12px; }
    code { color: #9bd4ff; }
    ul { margin: 0; padding-left: 20px; color: #c7d2ea; line-height: 1.65; }
    .artifact-list { columns: 2; }
    @media (max-width: 900px) { .hero, .outputs { grid-template-columns: 1fr; } .artifact-list { columns: 1; } }
  </style>
</head>
<body>
  <header>
    <div class="pill ok">Exercise Mode v1</div>
    <div class="pill">scenario: $Scenario</div>
    <h1>ConstraintOS Exercise Workbench</h1>
    <p class="subhead">A local, visible app exercise path: input constraints generate controlled output permutations, deterministic SVG graphics, validation evidence, and a manual review decision.</p>
  </header>
  <main>
    <section class="hero">
      <div class="card">
        <h2>Loaded scenario</h2>
        <h3>Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic</h3>
        <p>This workbench is generated from the latest validated output POC run and is intended for hands-on app exercise, not invisible CI validation.</p>
        <span class="pill">Toyota Supra A80</span>
        <span class="pill">2JZ-GTE</span>
        <span class="pill">inline-six</span>
        <span class="pill">twin turbo</span>
        <span class="pill blocked">not final artwork</span>
      </div>
      <div class="card">
        <h2>Current decision</h2>
        <div class="grid">
          <div class="metric"><strong>needs_review</strong><span>final decision</span></div>
          <div class="metric"><strong>false</strong><span>approval_allowed</span></div>
          <div class="metric"><strong>passed</strong><span>SVG structural validation</span></div>
          <div class="metric"><strong>4</strong><span>generated SVG outputs</span></div>
        </div>
      </div>
    </section>

    <section class="card">
      <h2>Input constraints being exercised</h2>
      <div>
        <span class="pill ok">Must be Supra Mk IV / A80</span>
        <span class="pill ok">Must be 2JZ-GTE</span>
        <span class="pill ok">Must show inline-six identity</span>
        <span class="pill ok">Must show twin-turbo architecture</span>
        <span class="pill blocked">Must not be V6</span>
        <span class="pill blocked">Must not be V8</span>
        <span class="pill blocked">Must not be rotary</span>
        <span class="pill blocked">Must not be RB26 / B58 / LF4</span>
      </div>
    </section>

    <section class="card">
      <h2>Generated output permutations</h2>
      <p>Each output is deterministic and fixture-safe. The goal is to exercise the app loop from input constraints to controlled outputs and evidence, not to produce final production artwork.</p>
      <div class="outputs">
        <div class="output-card card"><h3>Turbo system focus</h3><object data="graphics/turbo_system_focus.svg" type="image/svg+xml"></object></div>
        <div class="output-card card"><h3>Inline-six identity focus</h3><object data="graphics/inline_six_engine_identity_focus.svg" type="image/svg+xml"></object></div>
        <div class="output-card card"><h3>Technical label density focus</h3><object data="graphics/technical_label_density_focus.svg" type="image/svg+xml"></object></div>
        <div class="output-card card"><h3>Reviewer-safe minimal focus</h3><object data="graphics/reviewer_safe_minimal_focus.svg" type="image/svg+xml"></object></div>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>Validation evidence</h2>
        <ul>
          <li>All four expected SVG graphics exist.</li>
          <li>SVG structural metadata is validated.</li>
          <li>External image references are blocked.</li>
          <li>Review packet remains manual-review only.</li>
          <li>Approval remains blocked.</li>
        </ul>
      </div>
      <div class="card">
        <h2>What to inspect next</h2>
        <ul>
          <li>Compare the four SVG outputs side by side.</li>
          <li>Check whether the scenario and constraints are understandable.</li>
          <li>Decide whether the output permutations feel useful.</li>
          <li>Use the feedback card for product signal.</li>
        </ul>
      </div>
    </section>

    <section class="card">
      <h2>Generated artifacts in this run</h2>
      <ul class="artifact-list">
        <li><code>exercise-workbench.html</code></li>
        <li><code>index.html</code></li>
        <li><code>run-metadata.json</code></li>
        <li><code>graphic-output-manifest.json</code></li>
        <li><code>graphic-output-permutations.json</code></li>
        <li><code>graphic-output-validation.json</code></li>
        <li><code>graphic-output-review-packet.json</code></li>
        <li><code>svg-structural-validation.json</code></li>
        <li><code>validated-output-poc-demo-summary.json</code></li>
        <li><code>graphics/turbo_system_focus.svg</code></li>
        <li><code>graphics/inline_six_engine_identity_focus.svg</code></li>
        <li><code>graphics/technical_label_density_focus.svg</code></li>
        <li><code>graphics/reviewer_safe_minimal_focus.svg</code></li>
      </ul>
    </section>

    <section class="card">
      <h2>Scope guardrails</h2>
      <span class="pill blocked">No real generated final graphics</span>
      <span class="pill blocked">No production artwork approval</span>
      <span class="pill blocked">No local image input</span>
      <span class="pill blocked">No image decoding</span>
      <span class="pill blocked">No pixel inspection</span>
      <span class="pill blocked">No CV/OCR integration</span>
      <span class="pill blocked">No automatic approval</span>
    </section>

    <section class="card">
      <h2>Run metadata</h2>
      <p><strong>Run directory:</strong> <code>$RunDir</code></p>
      <p><strong>Generated at:</strong> <code>$GeneratedAt</code></p>
      <p><strong>Source browser UI:</strong> <code>index.html</code></p>
      <p><strong>Exercise workbench:</strong> <code>exercise-workbench.html</code></p>
    </section>
  </main>
</body>
</html>
"@

$WorkbenchHtml | Set-Content -Path $WorkbenchPath -Encoding UTF8

if ($NoOpenBrowser) {
    Write-Host "NoOpenBrowser was provided. Skipping exercise workbench launch." -ForegroundColor Yellow
} else {
    Start-Process $WorkbenchPath
}

Write-Host "ConstraintOS Exercise Workbench ready." -ForegroundColor Green
Write-Host "Scenario: $Scenario"
Write-Host "Run directory: $RunDir"
Write-Host "Exercise workbench: $WorkbenchPath"
Write-Host "Generated outputs: 4 SVG graphics"
Write-Host "Validation: passed"
Write-Host "Final decision remains: needs_review"
Write-Host "Approval allowed remains: false"
