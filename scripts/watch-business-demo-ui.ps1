param(
    [string]$Scenario = "supra_2jz_gte_twin_turbo",
    [int]$StageDelayMs = 900,
    [switch]$OpenBrowser
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$RunRoot = Join-Path $RepoRoot "runs"
$DemoRoot = Join-Path $RunRoot "business-demo-ui"
$ScenarioRoot = Join-Path $DemoRoot $Scenario
$RunDir = Join-Path $ScenarioRoot $Timestamp

New-Item -ItemType Directory -Force -Path $RunDir | Out-Null

$IndexPath = Join-Path $RunDir "index.html"
$DataPath = Join-Path $RunDir "demo-data.json"
$MetadataPath = Join-Path $RunDir "run-metadata.json"

$BusinessTitle = "ConstraintOS Business Demo"
$UseCaseTitle = "Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic"
$Decision = "needs_review"
$ApprovalAllowed = $false

$Stages = @(
    [ordered]@{
        id = "request"
        label = "Business request"
        headline = "Create a technical graphic for the Toyota Supra Mk IV / A80 twin-turbo use case."
        detail = "The viewer sees the request in business terms before any technical files appear."
    },
    [ordered]@{
        id = "constraints"
        label = "Loaded constraints"
        headline = "The system checks for Supra A80, 2JZ-GTE inline-six, and sequential twin-turbo requirements."
        detail = "ConstraintOS treats the specification as the source of truth instead of trusting a generated image blindly."
    },
    [ordered]@{
        id = "candidate"
        label = "Candidate evidence"
        headline = "Fixture candidate evidence is reviewed against the loaded constraints."
        detail = "This demo is fixture-only and evidence-harness-only; it does not generate final graphics yet."
    },
    [ordered]@{
        id = "review"
        label = "Deterministic review"
        headline = "Traceability, guardrails, and review packets explain what was checked."
        detail = "The business point is auditability: every result should be explainable before approval is allowed."
    },
    [ordered]@{
        id = "decision"
        label = "Decision"
        headline = "Final decision: needs_review. Approval allowed: false."
        detail = "This is intentional. The POC proves the review path and refuses automatic approval without sufficient validated evidence."
    },
    [ordered]@{
        id = "next"
        label = "Next product step"
        headline = "Next: Constraint-Driven Graphic Output Permutation POC v1."
        detail = "The next milestone should show generated or fixture-safe output permutations derived from constraints, then validate each one."
    }
)

$DemoData = [ordered]@{
    demo = "business-demo-ui"
    scenario = $Scenario
    title = $BusinessTitle
    use_case = $UseCaseTitle
    final_decision = $Decision
    approval_allowed = $ApprovalAllowed
    stage_delay_ms = $StageDelayMs
    stages = $Stages
    guardrails = @(
        "no_generated_final_graphics",
        "no_constraint_derived_graphic_output_permutations_yet",
        "no_real_local_image_input",
        "no_local_file_path_loading",
        "no_file_uri_loading",
        "no_artifact_download",
        "no_network_fetch",
        "no_image_decoding",
        "no_pixel_inspection",
        "no_cv_ocr_provider_integration",
        "no_unrestricted_image_generation",
        "no_unrestricted_image_editing",
        "no_automatic_approval"
    )
}

$DemoData | ConvertTo-Json -Depth 8 | Set-Content -Path $DataPath -Encoding UTF8

$Metadata = [ordered]@{
    demo = "business-demo-ui"
    scenario = $Scenario
    run_dir = $RunDir
    index_html = $IndexPath
    demo_data = $DataPath
    run_metadata = $MetadataPath
    created_at_local = (Get-Date).ToString("o")
    final_decision = $Decision
    approval_allowed = $ApprovalAllowed
    guardrail_summary = "Static fixture-only browser walkthrough; no image generation, image decoding, network fetch, or automatic approval."
}

$Metadata | ConvertTo-Json -Depth 6 | Set-Content -Path $MetadataPath -Encoding UTF8

$StagesJson = $Stages | ConvertTo-Json -Depth 6
$GuardrailsJson = $DemoData.guardrails | ConvertTo-Json -Depth 4

$Html = @"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>$BusinessTitle - Toyota Supra Demo</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --ink: #172033;
      --muted: #5d6a7f;
      --line: #d9e1ef;
      --accent: #2458d3;
      --warning: #b7791f;
      --good: #1f7a4d;
      --shadow: 0 18px 45px rgba(20, 34, 66, 0.12);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
      background: radial-gradient(circle at top left, #e9f0ff 0, #f5f7fb 36%, #eef3f9 100%);
      color: var(--ink);
    }
    .shell { max-width: 1180px; margin: 0 auto; padding: 34px; }
    .hero {
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 24px;
      align-items: stretch;
      margin-bottom: 24px;
    }
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 24px;
      box-shadow: var(--shadow);
      padding: 28px;
    }
    .eyebrow { color: var(--accent); font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; font-size: 12px; }
    h1 { font-size: 42px; line-height: 1.05; margin: 12px 0; }
    h2 { font-size: 24px; margin: 0 0 12px; }
    p { color: var(--muted); font-size: 16px; line-height: 1.55; }
    .badges { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
    .badge { border-radius: 999px; padding: 9px 12px; font-weight: 700; font-size: 13px; background: #edf3ff; color: #244eac; }
    .badge.warning { background: #fff6df; color: var(--warning); }
    .badge.good { background: #eaf8f0; color: var(--good); }
    .dashboard { display: grid; grid-template-columns: 310px 1fr; gap: 24px; }
    .timeline { display: flex; flex-direction: column; gap: 12px; }
    .step {
      border: 1px solid var(--line);
      background: #fbfcff;
      border-radius: 16px;
      padding: 14px 16px;
      cursor: pointer;
      transition: 150ms ease;
    }
    .step.active { border-color: var(--accent); background: #eef4ff; transform: translateX(4px); }
    .step.done { border-color: #b7dfca; background: #f1fbf5; }
    .step .label { font-weight: 800; }
    .step .id { color: var(--muted); font-size: 12px; margin-top: 4px; }
    .stage-view { min-height: 420px; display: grid; grid-template-rows: auto 1fr auto; }
    .big-stage { border: 1px dashed #b8c5dc; border-radius: 22px; padding: 28px; background: linear-gradient(135deg, #ffffff, #f2f6ff); }
    .stage-label { color: var(--accent); font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; font-size: 13px; }
    .stage-headline { font-size: 32px; line-height: 1.12; margin: 12px 0; font-weight: 850; }
    .stage-detail { font-size: 18px; }
    .engine-card {
      margin-top: 22px;
      border-radius: 22px;
      border: 1px solid var(--line);
      background: #111827;
      color: #fff;
      padding: 20px;
      overflow: hidden;
      position: relative;
      min-height: 158px;
    }
    .engine-title { font-weight: 800; margin-bottom: 14px; }
    .engine-graphic { display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; align-items: center; }
    .cylinder, .turbo, .pipe { border-radius: 10px; height: 44px; background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.28); }
    .turbo { border-radius: 999px; background: rgba(96,165,250,0.35); }
    .pipe { height: 10px; background: rgba(251,191,36,0.6); }
    .controls { display: flex; gap: 12px; margin-top: 20px; }
    button { border: 0; border-radius: 12px; padding: 12px 16px; font-weight: 800; background: var(--accent); color: white; cursor: pointer; }
    button.secondary { background: #e7ecf7; color: var(--ink); }
    .decision { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 24px; }
    .metric { border: 1px solid var(--line); border-radius: 18px; padding: 18px; background: #fff; }
    .metric .value { font-size: 24px; font-weight: 900; }
    .metric .caption { color: var(--muted); font-size: 13px; margin-top: 4px; }
    .footer-note { margin-top: 20px; font-size: 13px; color: var(--muted); }
    @media (max-width: 900px) { .hero, .dashboard, .decision { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="card">
        <div class="eyebrow">ConstraintOS business demo</div>
        <h1>Can an AI-generated technical graphic be trusted?</h1>
        <p>This browser demo shows the current evidence-harness workflow using the Toyota Supra A80 2JZ-GTE twin-turbo use case. It is designed for business viewers: no JSON, no terminal output, no implementation details required.</p>
        <div class="badges">
          <span class="badge">Use case: Toyota Supra A80</span>
          <span class="badge">Engine: 2JZ-GTE inline-six</span>
          <span class="badge warning">Decision: needs_review</span>
          <span class="badge good">Approval blocked by design</span>
        </div>
      </div>
      <div class="card">
        <h2>What this proves</h2>
        <p>ConstraintOS makes the requirements, evidence, and decision visible before anyone trusts the output. The current demo does not generate final graphics yet; it proves the audit path that future output generation must pass through.</p>
        <div class="decision">
          <div class="metric"><div class="value">6</div><div class="caption">business-visible stages</div></div>
          <div class="metric"><div class="value">false</div><div class="caption">approval_allowed</div></div>
          <div class="metric"><div class="value">next</div><div class="caption">output permutations</div></div>
        </div>
      </div>
    </section>

    <section class="dashboard">
      <aside class="card timeline" id="timeline"></aside>
      <section class="card stage-view">
        <div class="big-stage">
          <div class="stage-label" id="stageLabel"></div>
          <div class="stage-headline" id="stageHeadline"></div>
          <p class="stage-detail" id="stageDetail"></p>
          <div class="engine-card" aria-label="abstract technical graphic placeholder">
            <div class="engine-title">Abstract placeholder: inline-six + twin turbo requirement</div>
            <div class="engine-graphic">
              <div class="cylinder"></div><div class="cylinder"></div><div class="cylinder"></div><div class="cylinder"></div><div class="cylinder"></div><div class="cylinder"></div>
              <div class="turbo"></div><div class="pipe"></div><div class="pipe"></div><div class="pipe"></div><div class="pipe"></div><div class="turbo"></div>
            </div>
          </div>
        </div>
        <div class="controls">
          <button id="playBtn">Replay demo</button>
          <button class="secondary" id="nextBtn">Next stage</button>
        </div>
        <div class="footer-note">Guardrail: this page is a static fixture-only UI. It does not generate images, decode images, fetch the network, inspect pixels, run CV/OCR, or approve candidates automatically.</div>
      </section>
    </section>
  </main>

  <script>
    const stages = $StagesJson;
    const guardrails = $GuardrailsJson;
    const delay = $StageDelayMs;
    let current = 0;
    let timer = null;

    const timeline = document.getElementById('timeline');
    const label = document.getElementById('stageLabel');
    const headline = document.getElementById('stageHeadline');
    const detail = document.getElementById('stageDetail');

    function renderTimeline() {
      timeline.innerHTML = '<h2>Workflow</h2>' + stages.map((stage, index) => {
        const state = index === current ? 'active' : index < current ? 'done' : '';
        return `<div class="step ${state}" data-index="${index}"><div class="label">${index + 1}. ${stage.label}</div><div class="id">${stage.id}</div></div>`;
      }).join('');
      document.querySelectorAll('.step').forEach(el => {
        el.addEventListener('click', () => showStage(Number(el.dataset.index), false));
      });
    }

    function showStage(index, keepPlaying = true) {
      current = Math.max(0, Math.min(stages.length - 1, index));
      const stage = stages[current];
      label.textContent = stage.label;
      headline.textContent = stage.headline;
      detail.textContent = stage.detail;
      renderTimeline();
      if (!keepPlaying && timer) {
        clearInterval(timer);
        timer = null;
      }
    }

    function play() {
      if (timer) clearInterval(timer);
      current = 0;
      showStage(current);
      timer = setInterval(() => {
        if (current >= stages.length - 1) {
          clearInterval(timer);
          timer = null;
          return;
        }
        showStage(current + 1);
      }, delay);
    }

    document.getElementById('playBtn').addEventListener('click', play);
    document.getElementById('nextBtn').addEventListener('click', () => showStage(current + 1, false));
    play();
  </script>
</body>
</html>
"@

$Html | Set-Content -Path $IndexPath -Encoding UTF8

Write-Host "ConstraintOS business demo UI created."
Write-Host "Scenario: $Scenario"
Write-Host "Use case: $UseCaseTitle"
Write-Host "Decision: $Decision"
Write-Host "Approval allowed: $ApprovalAllowed"
Write-Host "Run folder: $RunDir"
Write-Host "Open: $IndexPath"

if ($OpenBrowser) {
    Start-Process $IndexPath
}
