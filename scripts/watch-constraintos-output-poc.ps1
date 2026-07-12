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
    viewer_summary = "ConstraintOS defined four fixture-safe Toyota Supra / 2JZ-GTE output permutations and kept each one in needs_review."
    recommended_reviewer_path = @(
        "Review graphic-output-manifest.json to see the controlled variants.",
        "Review graphic-output-validation.json to see why approval remains blocked.",
        "Open index.html for the business-facing walkthrough."
    )
    final_decision = $FinalDecision
    approval_allowed = $ApprovalAllowed
    why_approval_is_blocked = "The current POC defines controlled output specifications only; it does not generate production artwork or inspect real images."
    next_recommended_action = "Review business feedback and continue toward the browser output-permutation demo if the trust-layer story is understood."
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
$Metadata | ConvertTo-Json -Depth 8 | Set-Content -Path $MetadataPath -Encoding UTF8

$Html = @'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ConstraintOS Output Permutation POC - Toyota Supra</title>
  <style>
    body { margin: 0; font-family: Segoe UI, Roboto, Arial, sans-serif; background: #f5f7fb; color: #172033; }
    main { max-width: 1120px; margin: 0 auto; padding: 36px; }
    .card { background: white; border: 1px solid #d9e1ef; border-radius: 22px; padding: 24px; box-shadow: 0 18px 45px rgba(20, 34, 66, 0.10); margin-bottom: 18px; }
    .eyebrow { color: #2458d3; font-size: 12px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
    h1 { font-size: 40px; margin: 12px 0; }
    h2 { margin: 0 0 10px; }
    p { color: #5d6a7f; line-height: 1.55; }
    .grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
    .variant { border: 1px solid #d9e1ef; border-radius: 18px; padding: 18px; background: #fbfcff; }
    .tag { display: inline-block; border-radius: 999px; padding: 7px 10px; background: #fff6df; color: #995f00; font-weight: 800; font-size: 12px; }
    .artifact { font-family: Consolas, monospace; background: #111827; color: #dbeafe; border-radius: 12px; padding: 10px; font-size: 13px; }
    ul { color: #5d6a7f; }
    @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <main>
    <section class="card">
      <div class="eyebrow">ConstraintOS output permutation POC</div>
      <h1>Toyota Supra / 2JZ-GTE fixture-safe output permutations</h1>
      <p>This static page shows the controlled output layer: constraints define multiple output specifications, each specification is validated, and approval remains blocked.</p>
      <p><strong>Final decision:</strong> needs_review. <strong>Approval allowed:</strong> false.</p>
    </section>

    <section class="grid">
      <article class="variant"><span class="tag">needs_review</span><h2>turbo_system_focus</h2><p>Emphasizes the sequential twin-turbo system without claiming final artwork or image verification.</p><div class="artifact">fixture-placeholder://output-poc/supra/turbo-system-focus</div></article>
      <article class="variant"><span class="tag">needs_review</span><h2>inline_six_engine_identity_focus</h2><p>Emphasizes Toyota Supra A80 / 2JZ-GTE inline-six identity and wrong-engine exclusions.</p><div class="artifact">fixture-placeholder://output-poc/supra/inline-six-identity-focus</div></article>
      <article class="variant"><span class="tag">needs_review</span><h2>technical_label_density_focus</h2><p>Emphasizes dense technical publishing callouts while keeping uncertainty visible.</p><div class="artifact">fixture-placeholder://output-poc/supra/technical-label-density-focus</div></article>
      <article class="variant"><span class="tag">needs_review</span><h2>reviewer_safe_minimal_focus</h2><p>Emphasizes a conservative reviewer-safe specification that only exposes validated claims.</p><div class="artifact">fixture-placeholder://output-poc/supra/reviewer-safe-minimal-focus</div></article>
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
