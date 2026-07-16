# Validated Output POC Demo Launcher v1

## Status

```text
milestone: Validated Output POC Demo Launcher v1
status: active
phase_1_validated_demo_launcher_status: ready-for-verification
phase_2_validated_demo_summary_status: ready-for-verification
phase_3_validated_demo_browser_summary_status: ready-for-verification
phase_4_validated_demo_reviewer_handoff_status: ready-for-verification
phase_5_validated_demo_feedback_card_status: ready-for-use
started_on: 2026-07-15
track: Business Demo Visibility Track
previous_milestone: docs/500_Milestones/Deterministic_SVG_Structural_Validation_v1.md
launcher_script: scripts/run-validated-output-poc-demo.ps1
generator_script: scripts/watch-constraintos-output-poc.ps1
validator_script: scripts/validate-output-poc-svg-graphics.ps1
browser_helper_script: scripts/open-latest-output-poc-browser.ps1
reviewer_handoff: docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md
feedback_card: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only
assistant_ran_tests: false
assistant_ran_demo: false
```

## Purpose

Provide a single user-facing command that runs the validated output POC demo path end to end: generate deterministic output artifacts, validate SVG structural evidence, update reviewer-facing evidence artifacts, write a launcher-level summary, surface launcher evidence in the browser UI, provide a reviewer handoff and feedback card, and open the generated browser UI.

```text
one command -> generate output POC -> validate SVG evidence -> write launcher summary -> update browser evidence -> reviewer handoff -> feedback card -> open latest browser UI
```

## Product promise for this milestone

```text
- Run the fixture-safe output POC generator.
- Run the deterministic SVG structural validator.
- Write validated-output-poc-demo-summary.json for the latest run.
- Add validated-output-poc-demo-summary to the latest browser UI.
- Provide a reviewer handoff for the validated one-command demo path.
- Provide a reviewer feedback card for structured product signal.
- Open the latest output POC browser UI by default.
- Allow a NoOpenBrowser mode for terminal-only verification.
- Preserve needs_review and approval_allowed: false.
- Preserve deterministic fixture-safe scope.
```

## Target launcher command

```powershell
.\scripts\run-validated-output-poc-demo.ps1
```

## Optional terminal-only command

```powershell
.\scripts\run-validated-output-poc-demo.ps1 -NoOpenBrowser
```

## Launcher summary artifact

```text
runs/output-poc/<scenario>/<timestamp>/validated-output-poc-demo-summary.json
```

Expected summary fields:

```text
launcher
scenario_key
run_dir
browser_ui
validation_report
review_packet
generated_at_local
generator_script
validator_script
browser_helper_script
final_decision: needs_review
approval_allowed: false
blocked_scope_preserved
```

## Browser summary target

```text
id="validated-output-poc-demo-summary"
validated-output-poc-demo-summary.json
svg-structural-validation.json
graphic-output-review-packet.json
final_decision: needs_review
approval_allowed: false
```

## Reviewer handoff

```text
docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md
```

The handoff defines the reviewer entry point, expected terminal evidence, expected browser evidence, expected run artifacts, the ready-to-show decision rule, and blocked scope.

## Reviewer feedback card

```text
docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md
```

The feedback card captures reviewer signal about product clarity, evidence confidence, browser usability, approval safety, and product gaps without authorizing real image generation, real image input, or automatic approval.

## Implementation under verification

```text
script: scripts/run-validated-output-poc-demo.ps1
test: tests/test_run_validated_output_poc_demo_script.py
command_reference_update: docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
summary_artifact: validated-output-poc-demo-summary.json
browser_summary_target: validated-output-poc-demo-summary in index.html
reviewer_handoff: docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md
reviewer_handoff_test: tests/test_validated_output_poc_demo_reviewer_handoff.py
feedback_card: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md
feedback_card_test: tests/test_validated_output_poc_demo_feedback_card.py
status: ready-for-verification
```

## Explicitly blocked scope

```text
- Real generated final graphics.
- Production artwork generation.
- Real local image input.
- local_file_path loading.
- file_uri loading.
- Artifact download.
- Network fetch.
- Image decoding.
- Pixel inspection.
- CV/OCR provider integration.
- Automatic approval.
```

## Done criteria

```text
[x] Milestone exists.
[x] Previous deterministic SVG structural validation milestone is referenced.
[x] Launcher command is defined.
[x] Generator script dependency is defined.
[x] Validator script dependency is defined.
[x] Browser helper script dependency is defined.
[x] NoOpenBrowser mode is defined.
[x] Launcher summary artifact is defined.
[x] Browser summary target is defined.
[x] Reviewer handoff is defined.
[x] Reviewer feedback card is defined.
[x] Blocked scope is preserved.
[x] Launcher script exists.
[ ] Verification result recorded.
```

## Verification command

```powershell
pytest tests/test_validated_output_poc_demo_launcher_milestone.py
pytest tests/test_run_validated_output_poc_demo_script.py
pytest tests/test_validated_output_poc_demo_reviewer_handoff.py
pytest tests/test_validated_output_poc_demo_feedback_card.py
.\scripts\run-validated-output-poc-demo.ps1
```
