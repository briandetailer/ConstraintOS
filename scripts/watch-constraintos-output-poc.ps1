param(
    [string]$Scenario = "supra_2jz_gte_twin_turbo",
    [int]$WatchDelayMs = 750,
    [switch]$OpenBrowser
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($Scenario -ne "supra_2jz_gte_twin_turbo") {
    throw "Unsupported scenario '$Scenario'. Supported scenario: supra_2jz_gte_twin_turbo."
}

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$RunRoot = Join-Path $RepoRoot "runs"
$DemoRoot = Join-Path $RunRoot "output-poc"
$ScenarioRoot = Join-Path $DemoRoot $Scenario
$RunDir = Join-Path $ScenarioRoot $Timestamp

New-Item -ItemType Directory -Force -Path $RunDir | Out-Null

$ManifestPath = Join-Path $RunDir "graphic-output-manifest.json"
$PermutationsPath = Join-Path $RunDir "graphic-output-permutations.json"
$ValidationPath = Join-Path $RunDir "graphic-output-validation.json"
$ReviewPacketPath = Join-Path $RunDir "graphic-output-review-packet.json"
$IndexPath = Join-Path $RunDir "index.html"
$MetadataPath = Join-Path $RunDir "run-metadata.json"

$DemoName = "constraint-driven-graphic-output-permutation-poc"
$UseCaseTitle = "Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic"
$FinalDecision = "needs_review"
$ApprovalAllowed = $false

$BaselineConstraints = @(
    "Toyota Supra Mk IV / A80 identity",
    "2JZ-GTE inline-six identity",
    "sequential twin-turbo system",
    "not generic engine",
    "not V6",
    "not V8",
    "not rotary",
    "not RB26",
    "not LF4",
    "not B58",
    "technical graphic / publishing context",
    "uncertainty defaults to needs_review",
    "approval_allowed remains false"
)

$Permutations = @(
    [ordered]@{
        permutation_id = "turbo_system_focus"
        variant_name = "Sequential twin-turbo system focus"
        business_intent = "Show why the technical graphic must communicate a sequential twin-turbo 2JZ-GTE system rather than a generic forced-induction engine."
        visual_strategy = "Emphasize turbo-system callouts, airflow intent, and the twin-turbo distinction while keeping engine identity visible."
        required_constraints = $BaselineConstraints
        emphasized_constraints = @("sequential twin-turbo system", "2JZ-GTE inline-six identity")
        known_risks = @("turbo routing may be over-implied before real artwork evidence exists", "visual simplification may hide sequential system nuance")
        explicit_non_goals = @("do not claim production artwork was generated", "do not claim pixel-level validation", "do not claim exact factory routing verification")
        placeholder_artifact = "fixture-placeholder://output-poc/supra/turbo-system-focus"
        expected_review_state = "needs_review"
    },
    [ordered]@{
        permutation_id = "inline_six_engine_identity_focus"
        variant_name = "2JZ-GTE inline-six identity focus"
        business_intent = "Show why the output must remain a Toyota Supra A80 / 2JZ-GTE inline-six and must not drift into a V6, V8, rotary, RB26, LF4, or B58 representation."
        visual_strategy = "Emphasize engine-family identity, inline-six layout, and wrong-engine exclusion constraints before turbo-system detail."
        required_constraints = $BaselineConstraints
        emphasized_constraints = @("Toyota Supra Mk IV / A80 identity", "2JZ-GTE inline-six identity", "not V6", "not V8", "not rotary", "not RB26", "not LF4", "not B58")
        known_risks = @("identity focus may under-explain the sequential twin-turbo system", "viewers may expect actual engine artwork in this phase")
        explicit_non_goals = @("do not claim production artwork was generated", "do not use real local image input", "do not represent this as image generation")
        placeholder_artifact = "fixture-placeholder://output-poc/supra/inline-six-identity-focus"
        expected_review_state = "needs_review"
    },
    [ordered]@{
        permutation_id = "technical_label_density_focus"
        variant_name = "Technical label-density focus"
        business_intent = "Show how the same constraints can produce a denser technical publishing variant for reviewers who need more explanation."
        visual_strategy = "Increase specification density, callout density, and constraint traceability while retaining the same Toyota Supra / 2JZ-GTE baseline."
        required_constraints = $BaselineConstraints
        emphasized_constraints = @("technical graphic / publishing context", "uncertainty defaults to needs_review")
        known_risks = @("too much label density may reduce business readability", "dense specification may look more authoritative than evidence supports")
        explicit_non_goals = @("do not claim automatic approval", "do not claim CV/OCR inspection", "do not claim production artwork was generated")
        placeholder_artifact = "fixture-placeholder://output-poc/supra/technical-label-density-focus"
        expected_review_state = "needs_review"
    },
    [ordered]@{
        permutation_id = "reviewer_safe_minimal_focus"
        variant_name = "Reviewer-safe minimal focus"
        business_intent = "Show a conservative output specification that exposes only validated requirements and clearly parks uncertain claims in needs_review."
        visual_strategy = "Keep the variant minimal, highlight only the safest baseline constraints, and make approval blocking visible."
        required_constraints = @("Toyota Supra Mk IV / A80 identity", "2JZ-GTE inline-six identity", "sequential twin-turbo system", "not generic engine", "uncertainty defaults to needs_review", "approval_allowed remains false")
        emphasized_constraints = @("uncertainty defaults to needs_review", "approval_allowed remains false")
        known_risks = @("conservative output may feel less impressive to business reviewers", "minimal display may not satisfy viewers asking for concrete generated output")
        explicit_non_goals = @("do not claim production artwork was generated", "do not imply final approval", "do not imply all technical details are verified")
        placeholder_artifact = "fixture-placeholder://output-poc/supra/reviewer-safe-minimal-focus"
        expected_review_state = "needs_review"
    }
)

$PlaceholderPanels = @(
    [ordered]@{
        permutation_id = "turbo_system_focus"
        panel_title = "Turbo System Focus"
        visual_placeholder_type = "schematic_block_panel"
        deterministic_tokens = @("panel_shell", "title_band", "schematic_block", "constraint_chip", "uncertainty_banner", "review_footer")
        traceability_labels = @("engine_identity", "vehicle_identity", "turbo_identity", "review_safety")
        reviewer_message = "Sequential twin-turbo intent is visible without claiming final artwork."
        review_decision = "needs_review"
        approval_allowed = $false
    },
    [ordered]@{
        permutation_id = "inline_six_engine_identity_focus"
        panel_title = "Inline-Six Identity Focus"
        visual_placeholder_type = "text_first_panel"
        deterministic_tokens = @("panel_shell", "title_band", "identity_block", "exclusion_chip", "constraint_chip", "uncertainty_banner", "review_footer")
        traceability_labels = @("engine_identity", "vehicle_identity", "wrong_engine_exclusion", "review_safety")
        reviewer_message = "2JZ-GTE inline-six identity and wrong-engine exclusions are emphasized before artwork exists."
        review_decision = "needs_review"
        approval_allowed = $false
    },
    [ordered]@{
        permutation_id = "technical_label_density_focus"
        panel_title = "Technical Label Density Focus"
        visual_placeholder_type = "label_density_panel"
        deterministic_tokens = @("panel_shell", "title_band", "density_indicator", "constraint_chip", "evidence_chip", "uncertainty_banner", "review_footer")
        traceability_labels = @("engine_identity", "turbo_identity", "review_safety")
        reviewer_message = "Dense callout intent is visible for comparison, while label placement remains unresolved."
        review_decision = "needs_review"
        approval_allowed = $false
    },
    [ordered]@{
        permutation_id = "reviewer_safe_minimal_focus"
        panel_title = "Reviewer-Safe Minimal Focus"
        visual_placeholder_type = "reviewer_safe_minimal_panel"
        deterministic_tokens = @("panel_shell", "title_band", "identity_block", "constraint_chip", "uncertainty_banner", "review_footer")
        traceability_labels = @("engine_identity", "vehicle_identity", "turbo_identity", "review_safety")
        reviewer_message = "Only validated claims are surfaced; uncertain details are intentionally withheld."
        review_decision = "needs_review"
        approval_allowed = $false
    }
)

$EvidenceSummaryCards = @(
    [ordered]@{
        permutation_id = "turbo_system_focus"
        evidence_card_title = "Turbo System Evidence"
        satisfied_constraints = @("Toyota Supra A80", "2JZ-GTE", "sequential twin-turbo")
        visible_uncertainty = "schematic layout is placeholder-only"
        blocked_claims = @("final artwork", "physical accuracy approval", "image-derived verification")
        review_decision = "needs_review"
        approval_allowed = $false
    },
    [ordered]@{
        permutation_id = "inline_six_engine_identity_focus"
        evidence_card_title = "Inline-Six Identity Evidence"
        satisfied_constraints = @("Toyota Supra A80", "2JZ-GTE inline-six", "wrong-engine exclusions")
        visible_uncertainty = "identity emphasis is placeholder-only"
        blocked_claims = @("final artwork", "hidden mechanical correctness approval", "image-derived verification")
        review_decision = "needs_review"
        approval_allowed = $false
    },
    [ordered]@{
        permutation_id = "technical_label_density_focus"
        evidence_card_title = "Label Density Evidence"
        satisfied_constraints = @("technical graphic context", "label comparison", "fixture-defined tokens")
        visible_uncertainty = "label density requires reviewer judgment"
        blocked_claims = @("final label placement", "production-ready diagram approval", "image-derived verification")
        review_decision = "needs_review"
        approval_allowed = $false
    },
    [ordered]@{
        permutation_id = "reviewer_safe_minimal_focus"
        evidence_card_title = "Reviewer-Safe Evidence"
        satisfied_constraints = @("validated claims only", "visible uncertainty", "approval blocked")
        visible_uncertainty = "withheld details remain unverified"
        blocked_claims = @("final artwork", "automatic approval", "unstated mechanical claims")
        review_decision = "needs_review"
        approval_allowed = $false
    }
)

$PermutationIds = @($Permutations | ForEach-Object { $_.permutation_id })

$Manifest = [ordered]@{
    demo = $DemoName
    scenario_key = $Scenario
    use_case_title = $UseCaseTitle
    run_id = $Timestamp
    created_at_local = (Get-Date).ToString("o")
    final_decision = $FinalDecision
    approval_allowed = $ApprovalAllowed
    permutation_count = $Permutations.Count
    permutation_ids = $PermutationIds
    constraints_source = "docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Toyota_Fixtures.md"
    artifacts = [ordered]@{
        manifest = "graphic-output-manifest.json"
        permutations = "graphic-output-permutations.json"
        validation = "graphic-output-validation.json"
        review_packet = "graphic-output-review-packet.json"
        browser = "index.html"
        metadata = "run-metadata.json"
    }
}

$PermutationSet = [ordered]@{
    demo = $DemoName
    scenario_key = $Scenario
    permutations = $Permutations
}

$PermutationResults = @(
    foreach ($Permutation in $Permutations) {
        [ordered]@{
            permutation_id = $Permutation.permutation_id
            satisfied_constraints = $Permutation.emphasized_constraints
            missing_constraints = @()
            uncertain_constraints = $Permutation.known_risks
            blocked_claims = $Permutation.explicit_non_goals
            review_decision = "needs_review"
            approval_allowed = $false
        }
    }
)

$Validation = [ordered]@{
    demo = $DemoName
    scenario_key = $Scenario
    validation_mode = "deterministic-fixture-safe-specification-review"
    final_decision = $FinalDecision
    approval_allowed = $ApprovalAllowed
    permutation_results = $PermutationResults
}

$ReviewPacket = [ordered]@{
    demo = $DemoName
    scenario_key = $Scenario
    viewer_summary = "ConstraintOS defined four fixture-safe Toyota Supra / 2JZ-GTE output permutations and displays deterministic placeholder panels and evidence cards for each one."
    recommended_reviewer_path = @(
        "Open index.html for the business-facing placeholder panels and evidence cards.",
        "Review graphic-output-manifest.json to see the controlled variants.",
        "Review graphic-output-validation.json to see why approval remains blocked."
    )
    final_decision = $FinalDecision
    approval_allowed = $ApprovalAllowed
    why_approval_is_blocked = "The current POC defines controlled output specifications and deterministic placeholder panels only; it does not generate production artwork or inspect real images."
    next_recommended_action = "Review whether the browser placeholder panels make the four output intents clear enough for business feedback."
}

$Metadata = [ordered]@{
    demo = $DemoName
    scenario_key = $Scenario
    run_dir = $RunDir
    manifest = $ManifestPath
    permutations = $PermutationsPath
    validation = $ValidationPath
    review_packet = $ReviewPacketPath
    index_html = $IndexPath
    run_metadata = $MetadataPath
    created_at_local = (Get-Date).ToString("o")
    final_decision = $FinalDecision
    approval_allowed = $ApprovalAllowed
    browser_walkthrough = "constraints -> permutations -> validation -> needs_review"
    browser_placeholder_walkthrough = "output permutations -> deterministic placeholder panels -> evidence summary cards -> needs_review"
    placeholder_panels = $PlaceholderPanels
    evidence_summary_cards = $EvidenceSummaryCards
    traceability_labels = @("engine_identity", "vehicle_identity", "turbo_identity", "wrong_engine_exclusion", "review_safety")
    guardrails = @(
        "No generated final graphics",
        "No production artwork generation",
        "No real local image input",
        "No artifact download",
        "No network fetch",
        "No image decoding",
        "No pixel inspection",
        "No CV/OCR provider integration",
        "No automatic approval"
    )
}

$Manifest | ConvertTo-Json -Depth 8 | Set-Content -Path $ManifestPath -Encoding UTF8
$PermutationSet | ConvertTo-Json -Depth 10 | Set-Content -Path $PermutationsPath -Encoding UTF8
$Validation | ConvertTo-Json -Depth 10 | Set-Content -Path $ValidationPath -Encoding UTF8
$ReviewPacket | ConvertTo-Json -Depth 8 | Set-Content -Path $ReviewPacketPath -Encoding UTF8
$Metadata | ConvertTo-Json -Depth 12 | Set-Content -Path $MetadataPath -Encoding UTF8

$Html = @'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ConstraintOS Output Permutation POC - Toyota Supra</title>
  <style>
    :root { color-scheme: light; --bg: #f5f7fb; --panel: #ffffff; --ink: #172033; --muted: #5d6a7f; --line: #d9e1ef; --accent: #2458d3; --warn: #a16207; --dark: #111827; --safe: #166534; --soft: #eef4ff; }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Segoe UI, Roboto, Arial, sans-serif; background: radial-gradient(circle at top left, #e9f0ff 0, var(--bg) 38%, #eef3f9 100%); color: var(--ink); }
    main { max-width: 1180px; margin: 0 auto; padding: 36px; }
    .card { background: var(--panel); border: 1px solid var(--line); border-radius: 22px; padding: 24px; box-shadow: 0 18px 45px rgba(20, 34, 66, 0.10); margin-bottom: 18px; }
    .eyebrow { color: var(--accent); font-size: 12px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
    h1 { font-size: 42px; line-height: 1.05; margin: 12px 0; }
    h2 { margin: 0 0 10px; }
    h3 { margin: 0 0 8px; }
    p { color: var(--muted); line-height: 1.55; }
    .flow { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-top: 18px; }
    .flow-step { border: 1px solid var(--line); border-radius: 18px; background: #fbfcff; padding: 16px; }
    .flow-step strong { display: block; margin-bottom: 6px; }
    .grid, .placeholder-grid, .evidence-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
    .variant, .placeholder-panel, .evidence-summary-card { border: 1px solid var(--line); border-radius: 18px; padding: 18px; background: #fbfcff; }
    .placeholder-panel { border-top: 5px solid var(--accent); }
    .evidence-summary-card { border-top: 5px solid var(--safe); }
    .tag, .chip { display: inline-block; border-radius: 999px; padding: 7px 10px; background: #fff6df; color: var(--warn); font-weight: 800; font-size: 12px; margin: 0 6px 8px 0; }
    .chip { background: var(--soft); color: var(--accent); }
    .artifact { font-family: Consolas, monospace; background: var(--dark); color: #dbeafe; border-radius: 12px; padding: 10px; font-size: 13px; overflow-wrap: anywhere; }
    .decision { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
    .metric { border: 1px solid var(--line); border-radius: 18px; background: #fbfcff; padding: 18px; }
    .metric .value { font-size: 24px; font-weight: 900; }
    .placeholder-visual { border: 1px dashed var(--line); border-radius: 16px; padding: 14px; margin: 14px 0; background: #ffffff; }
    .visual-row { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-bottom: 10px; }
    .schematic-block, .identity-block, .density-indicator { border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; background: #f8fbff; font-weight: 800; }
    .density-indicator { min-width: 72px; text-align: center; }
    .uncertainty-banner { border-left: 4px solid var(--warn); background: #fff8e8; border-radius: 12px; padding: 10px 12px; color: #6b4e00; font-weight: 700; }
    .review-footer { margin-top: 12px; font-weight: 900; color: var(--ink); }
    ul { color: var(--muted); }
    @media (max-width: 900px) { .grid, .flow, .decision, .placeholder-grid, .evidence-grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <main>
    <section class="card">
      <div class="eyebrow">ConstraintOS output permutation POC</div>
      <h1>Toyota Supra / 2JZ-GTE fixture-safe output permutations</h1>
      <p>This browser walkthrough shows the controlled output layer: loaded constraints define multiple output specifications, each specification gets deterministic validation evidence, and approval remains blocked.</p>
      <p><strong>Final decision:</strong> needs_review. <strong>Approval allowed:</strong> false.</p>
      <div class="flow" aria-label="demo walkthrough flow">
        <div class="flow-step"><strong>1. Constraints loaded</strong><span>Toyota Supra A80, 2JZ-GTE inline-six, sequential twin-turbo, and wrong-engine exclusions.</span></div>
        <div class="flow-step"><strong>2. Output permutations</strong><span>Four fixture-safe output specifications are defined from the same requirement set.</span></div>
        <div class="flow-step"><strong>3. Deterministic validation</strong><span>Each permutation is checked against explicit constraints and uncertainty is surfaced.</span></div>
        <div class="flow-step"><strong>4. needs_review</strong><span>Approval stays blocked because this is not final generated artwork or image inspection.</span></div>
      </div>
    </section>

    <section class="card">
      <h2>Controlled output permutations</h2>
      <div class="grid">
        <article class="variant"><span class="tag">needs_review</span><h3>turbo_system_focus</h3><p>Emphasizes the sequential twin-turbo system without claiming final artwork or image verification.</p><div class="artifact">fixture-placeholder://output-poc/supra/turbo-system-focus</div></article>
        <article class="variant"><span class="tag">needs_review</span><h3>inline_six_engine_identity_focus</h3><p>Emphasizes Toyota Supra A80 / 2JZ-GTE inline-six identity and wrong-engine exclusions.</p><div class="artifact">fixture-placeholder://output-poc/supra/inline-six-identity-focus</div></article>
        <article class="variant"><span class="tag">needs_review</span><h3>technical_label_density_focus</h3><p>Emphasizes dense technical publishing callouts while keeping uncertainty visible.</p><div class="artifact">fixture-placeholder://output-poc/supra/technical-label-density-focus</div></article>
        <article class="variant"><span class="tag">needs_review</span><h3>reviewer_safe_minimal_focus</h3><p>Emphasizes a conservative reviewer-safe specification that only exposes validated claims.</p><div class="artifact">fixture-placeholder://output-poc/supra/reviewer-safe-minimal-focus</div></article>
      </div>
    </section>

    <section class="card" id="fixture-safe-placeholder-panels">
      <div class="eyebrow">Fixture-safe placeholder panels</div>
      <h2>Browser-visible deterministic placeholder panels</h2>
      <p>These panels are deterministic browser placeholders, not generated final artwork. They make the four output intents visible while every variant remains needs_review and approval_allowed remains false.</p>
      <div class="placeholder-grid">
        <article class="placeholder-panel" data-permutation-id="turbo_system_focus" data-visual-placeholder-type="schematic_block_panel">
          <div class="eyebrow">panel_shell / title_band</div>
          <h3>Turbo System Focus</h3>
          <p>Sequential twin-turbo intent is visible without implying final artwork.</p>
          <div class="placeholder-visual" aria-label="deterministic schematic block panel">
            <div class="visual-row"><span class="schematic-block">engine core</span><span class="schematic-block">twin turbo A</span><span class="schematic-block">twin turbo B</span></div>
            <div class="visual-row"><span class="schematic-block">charge path</span><span class="schematic-block">exhaust path</span></div>
            <span class="chip">engine_identity</span><span class="chip">vehicle_identity</span><span class="chip">turbo_identity</span><span class="chip">review_safety</span>
          </div>
          <div class="uncertainty-banner">This is a deterministic placeholder, not final artwork.</div>
          <div class="review-footer">review_decision: needs_review / approval_allowed: false</div>
        </article>

        <article class="placeholder-panel" data-permutation-id="inline_six_engine_identity_focus" data-visual-placeholder-type="text_first_panel">
          <div class="eyebrow">panel_shell / title_band</div>
          <h3>Inline-Six Identity Focus</h3>
          <p>2JZ-GTE inline-six identity and wrong-engine exclusions are emphasized before artwork exists.</p>
          <div class="placeholder-visual" aria-label="deterministic identity text panel">
            <div class="visual-row"><span class="identity-block">inline-six</span><span class="identity-block">2JZ-GTE</span><span class="identity-block">Mk IV Supra</span></div>
            <span class="chip">not V6</span><span class="chip">not V8</span><span class="chip">not rotary</span><span class="chip">not RB26</span><span class="chip">not LF4</span><span class="chip">not B58</span>
            <div><span class="chip">engine_identity</span><span class="chip">vehicle_identity</span><span class="chip">wrong_engine_exclusion</span><span class="chip">review_safety</span></div>
          </div>
          <div class="uncertainty-banner">This panel is derived from fixture constraints, not image inspection.</div>
          <div class="review-footer">review_decision: needs_review / approval_allowed: false</div>
        </article>

        <article class="placeholder-panel" data-permutation-id="technical_label_density_focus" data-visual-placeholder-type="label_density_panel">
          <div class="eyebrow">panel_shell / title_band</div>
          <h3>Technical Label Density Focus</h3>
          <p>Dense callout intent is visible for comparison, while label placement remains unresolved.</p>
          <div class="placeholder-visual" aria-label="deterministic label density panel">
            <div class="visual-row"><span class="density-indicator">core labels</span><span class="density-indicator">turbo labels</span><span class="density-indicator">flow labels</span><span class="density-indicator">warning labels</span></div>
            <span class="chip">engine_identity</span><span class="chip">turbo_identity</span><span class="chip">review_safety</span><span class="chip">evidence_chip</span>
          </div>
          <div class="uncertainty-banner">Uncertainty remains needs_review.</div>
          <div class="review-footer">review_decision: needs_review / approval_allowed: false</div>
        </article>

        <article class="placeholder-panel" data-permutation-id="reviewer_safe_minimal_focus" data-visual-placeholder-type="reviewer_safe_minimal_panel">
          <div class="eyebrow">panel_shell / title_band</div>
          <h3>Reviewer-Safe Minimal Focus</h3>
          <p>Only validated claims are surfaced; uncertain details are intentionally withheld.</p>
          <div class="placeholder-visual" aria-label="deterministic reviewer-safe minimal panel">
            <div class="visual-row"><span class="identity-block">Toyota Supra A80</span><span class="identity-block">2JZ-GTE</span><span class="identity-block">sequential twin-turbo</span></div>
            <span class="chip">engine_identity</span><span class="chip">vehicle_identity</span><span class="chip">turbo_identity</span><span class="chip">review_safety</span>
          </div>
          <div class="uncertainty-banner">approval_allowed remains false.</div>
          <div class="review-footer">review_decision: needs_review / approval_allowed: false</div>
        </article>
      </div>
    </section>

    <section class="card" id="fixture-safe-evidence-summary-cards">
      <div class="eyebrow">Evidence summary cards</div>
      <h2>Fixture evidence summaries, not scoring cards</h2>
      <p>Each evidence_summary_card summarizes fixture evidence only. These cards do not inspect or grade final artwork, do not score pixels, and do not approve output.</p>
      <div class="evidence-grid">
        <article class="evidence-summary-card" data-permutation-id="turbo_system_focus"><h3>Turbo System Evidence</h3><p><strong>Satisfied:</strong> Toyota Supra A80, 2JZ-GTE, sequential twin-turbo.</p><p><strong>Visible uncertainty:</strong> schematic layout is placeholder-only.</p><p><strong>Blocked claims:</strong> final artwork, physical accuracy approval, image-derived verification.</p><div class="review-footer">needs_review / approval_allowed: false</div></article>
        <article class="evidence-summary-card" data-permutation-id="inline_six_engine_identity_focus"><h3>Inline-Six Identity Evidence</h3><p><strong>Satisfied:</strong> Toyota Supra A80, 2JZ-GTE inline-six, wrong-engine exclusions.</p><p><strong>Visible uncertainty:</strong> identity emphasis is placeholder-only.</p><p><strong>Blocked claims:</strong> final artwork, hidden mechanical correctness approval, image-derived verification.</p><div class="review-footer">needs_review / approval_allowed: false</div></article>
        <article class="evidence-summary-card" data-permutation-id="technical_label_density_focus"><h3>Label Density Evidence</h3><p><strong>Satisfied:</strong> technical graphic context, label comparison, fixture-defined tokens.</p><p><strong>Visible uncertainty:</strong> label density requires reviewer judgment.</p><p><strong>Blocked claims:</strong> final label placement, production-ready diagram approval, image-derived verification.</p><div class="review-footer">needs_review / approval_allowed: false</div></article>
        <article class="evidence-summary-card" data-permutation-id="reviewer_safe_minimal_focus"><h3>Reviewer-Safe Evidence</h3><p><strong>Satisfied:</strong> validated claims only, visible uncertainty, approval blocked.</p><p><strong>Visible uncertainty:</strong> withheld details remain unverified.</p><p><strong>Blocked claims:</strong> final artwork, automatic approval, unstated mechanical claims.</p><div class="review-footer">needs_review / approval_allowed: false</div></article>
      </div>
    </section>

    <section class="card">
      <h2>Validation outcome</h2>
      <div class="decision">
        <div class="metric"><div class="value">4</div><p>fixture-safe permutations</p></div>
        <div class="metric"><div class="value">needs_review</div><p>final_decision</p></div>
        <div class="metric"><div class="value">false</div><p>approval_allowed</p></div>
      </div>
    </section>

    <section class="card">
      <h2>Generated fixture-safe artifacts</h2>
      <ul>
        <li>graphic-output-manifest.json</li>
        <li>graphic-output-permutations.json</li>
        <li>graphic-output-validation.json</li>
        <li>graphic-output-review-packet.json</li>
        <li>run-metadata.json</li>
      </ul>
      <p>Guardrail: this demo does not generate final graphics, open local images, decode images, inspect pixels, fetch the network, use CV/OCR, or approve automatically.</p>
    </section>
  </main>
</body>
</html>
'@

$Html | Set-Content -Path $IndexPath -Encoding UTF8

Write-Host "ConstraintOS output permutation POC run created." -ForegroundColor Green
Write-Host "Scenario: $Scenario"
Write-Host "Run directory: $RunDir"
Write-Host "Manifest: $ManifestPath"
Write-Host "Permutations: $PermutationsPath"
Write-Host "Validation: $ValidationPath"
Write-Host "Review packet: $ReviewPacketPath"
Write-Host "Browser UI: $IndexPath"
Write-Host "Final decision: $FinalDecision"
Write-Host "Approval allowed: $ApprovalAllowed"

if ($OpenBrowser) {
    Start-Process $IndexPath
}
