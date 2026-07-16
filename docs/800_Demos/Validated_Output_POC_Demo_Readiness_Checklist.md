# Validated Output POC Demo Readiness Checklist

## Status

```text
readiness_checklist: Validated Output POC Demo Readiness Checklist
status: ready-for-use
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
launcher_script: scripts/run-validated-output-poc-demo.ps1
reviewer_handoff: docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md
feedback_card: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md
feedback_synthesis_log: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Synthesis_Log.md
implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only
```

## Purpose

Use this checklist after local verification and reviewer walkthroughs to decide whether the validated one-command output POC demo is ready to show.

```text
local verification + browser evidence + reviewer handoff + feedback synthesis -> ready-to-show decision
```

## Required local verification

Run:

```powershell
pytest tests/test_validated_output_poc_demo_launcher_milestone.py
pytest tests/test_run_validated_output_poc_demo_script.py
pytest tests/test_validated_output_poc_demo_reviewer_handoff.py
pytest tests/test_validated_output_poc_demo_feedback_card.py
pytest tests/test_validated_output_poc_demo_feedback_synthesis_log.py
.\scripts\run-validated-output-poc-demo.ps1
```

Expected terminal evidence:

```text
Validated ConstraintOS output POC demo complete.
Run directory:
Browser UI:
Validation report:
Review packet:
Launcher summary:
Browser summary updated:
Final decision remains: needs_review
Approval allowed remains: false
```

## Required browser evidence

The generated browser UI must visibly include:

```text
Deterministic SVG graphics
SVG structural validation
Validated demo launcher
```

The browser must show or reference:

```text
validated-output-poc-demo-summary.json
svg-structural-validation.json
graphic-output-review-packet.json
needs_review
approval_allowed: false
```

## Required run artifacts

The latest run folder must include:

```text
index.html
run-metadata.json
graphic-output-manifest.json
graphic-output-permutations.json
graphic-output-validation.json
graphic-output-review-packet.json
svg-structural-validation.json
validated-output-poc-demo-summary.json
graphics/turbo_system_focus.svg
graphics/inline_six_engine_identity_focus.svg
graphics/technical_label_density_focus.svg
graphics/reviewer_safe_minimal_focus.svg
```

## Reviewer package readiness

These reviewer documents must be available:

```text
docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md
docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md
docs/800_Demos/Validated_Output_POC_Demo_Feedback_Synthesis_Log.md
```

## Ready-to-show decision rule

```text
ready_to_show = true only when:
- all listed tests pass locally;
- the launcher runs successfully;
- the browser opens the latest generated output POC page;
- the browser contains SVG structural validation evidence;
- the browser contains validated launcher summary evidence;
- the run folder contains the expected JSON and SVG artifacts;
- the terminal preserves needs_review and approval_allowed: false;
- reviewer handoff, feedback card, and synthesis log are available.
```

## Not-ready conditions

```text
Do not mark ready-to-show if:
- any listed test fails;
- the launcher does not complete;
- the browser does not open;
- validated-output-poc-demo-summary.json is missing;
- svg-structural-validation.json is missing;
- graphic-output-review-packet.json is missing;
- the browser summary sections are missing;
- final decision is anything other than needs_review;
- approval_allowed is anything other than false.
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

## Current readiness state

```text
readiness_state: pending-local-verification
ready_to_show: false
assistant_ran_tests: false
assistant_ran_demo: false
```
