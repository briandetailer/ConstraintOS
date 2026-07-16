# Graphics Validation Command Reference

## Purpose

This document gathers user-facing commands and local verification commands introduced across the graphics-validation milestones.

## Maintenance rule

Whenever a future milestone, script, CLI entry point, or workflow makes new user-facing commands available, update this document in the same implementation slice.

Include:

```text
- the exact command
- what the command does
- whether it is plan-only, dry-run, fixture-only, helper-only, contract-only, read-only, or writes files
- any relevant output path
- any related verification command
```

## Branch sync

```powershell
git pull --rebase origin phase-1-cli-tooling
```

## Public demo reviewer entry point

Start with the root README for the public reviewer path:

```text
README.md
```

Verify the public reviewer entry point:

```powershell
pytest tests/test_public_demo_reviewer_entry_point.py
```

The README explains the current public POC status, the current evidence-harness demo command, the expected run folder, reviewer docs, current limitations, and the banked future target: Constraint-Driven Graphic Output Permutation POC v1.

## Business demo watch commands

### End-to-end fixture POC demo

Run the full fixture-based POC demo as a visible staged product walkthrough:

```powershell
.\scripts\watch-constraintos-poc.ps1
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
.\scripts\watch-constraintos-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -WatchDelayMs 750
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance -OpenRunFolder
pytest tests/test_end_to_end_fixture_poc_demo.py
```

This is a fixture-based, business-demo-friendly dry run. It shows scenario selection, contract/specification loading, candidate manifest/intake evidence, intake review, deterministic fixture byte loading, byte-loading review, fixture registry review, failure-matrix review, manual observation evidence, observation binding, evidence merge, fixture-only evaluation, final review packet, and demo summary. It writes run artifacts under `runs/poc-demo/<scenario>/<timestamp>/` and preserves no local image file opening, artifact download, network fetch, image decoding, CV/OCR provider integration, image generation/editing, source report mutation, or automatic approval.

### Business demo UI - Toyota Supra

Use this browser-based UI when the audience is business-focused and should not need to inspect terminal output, JSON files, or internal milestone documents:

```powershell
.\scripts\watch-business-demo-ui.ps1
.\scripts\watch-business-demo-ui.ps1 -Scenario supra_2jz_gte_twin_turbo
.\scripts\watch-business-demo-ui.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser
pytest tests/test_business_demo_ui_toyota_supra.py
```

Output paths:

```text
runs/business-demo-ui/<scenario>/<timestamp>/index.html
runs/business-demo-ui/<scenario>/<timestamp>/demo-data.json
runs/business-demo-ui/<scenario>/<timestamp>/run-metadata.json
```

This is a static fixture-only browser walkthrough for the Toyota Supra A80 2JZ-GTE twin-turbo use case. It shows a business-friendly staged flow from request, to loaded constraints, to candidate evidence, to deterministic review, to `needs_review`. It does not generate final graphics, decode images, fetch network resources, run CV/OCR, or approve candidates automatically.

### Constraint-driven output permutation POC - Toyota Supra

Use this fixture-safe watch script when the audience needs to see the next product-shaped demo: constraints define controlled output permutations, each permutation gets deterministic validation evidence, deterministic fixture-safe placeholder panels, evidence summary cards, traceability labels, deterministic SVG graphics, and approval remains blocked:

```powershell
.\scripts\run-validated-output-poc-demo.ps1
.\scripts\run-validated-output-poc-demo.ps1 -NoOpenBrowser
.\scripts\watch-constraintos-output-poc.ps1
.\scripts\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo
.\scripts\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser
.\scripts\open-latest-output-poc-graphics.ps1
.\scripts\open-latest-output-poc-browser.ps1
.\scripts\validate-output-poc-svg-graphics.ps1
pytest tests/test_run_validated_output_poc_demo_script.py
pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py
pytest tests/test_open_latest_output_poc_graphics_script.py
pytest tests/test_open_latest_output_poc_browser_script.py
pytest tests/test_validate_output_poc_svg_graphics_script.py
```

Output paths:

```text
runs/output-poc/<scenario>/<timestamp>/graphic-output-manifest.json
runs/output-poc/<scenario>/<timestamp>/graphic-output-permutations.json
runs/output-poc/<scenario>/<timestamp>/graphic-output-validation.json
runs/output-poc/<scenario>/<timestamp>/graphic-output-review-packet.json
runs/output-poc/<scenario>/<timestamp>/index.html
runs/output-poc/<scenario>/<timestamp>/run-metadata.json
runs/output-poc/<scenario>/<timestamp>/svg-structural-validation.json
runs/output-poc/<scenario>/<timestamp>/validated-output-poc-demo-summary.json
runs/output-poc/<scenario>/<timestamp>/graphics/turbo_system_focus.svg
runs/output-poc/<scenario>/<timestamp>/graphics/inline_six_engine_identity_focus.svg
runs/output-poc/<scenario>/<timestamp>/graphics/technical_label_density_focus.svg
runs/output-poc/<scenario>/<timestamp>/graphics/reviewer_safe_minimal_focus.svg
```

This is a static fixture-safe output-specification demo for the Toyota Supra A80 2JZ-GTE twin-turbo use case. It writes controlled permutation specs for `turbo_system_focus`, `inline_six_engine_identity_focus`, `technical_label_density_focus`, and `reviewer_safe_minimal_focus`; writes deterministic SVG graphics for each permutation; validates each as `needs_review`; and preserves `approval_allowed: false`. The generated `index.html` now includes browser-visible deterministic SVG graphics, deterministic fixture-safe placeholder panels, evidence summary cards, traceability labels, SVG structural validation evidence, and validated-demo launcher evidence so reviewers can compare output intent without treating the page as final artwork. The generated `run-metadata.json` records `placeholder_panels`, `evidence_summary_cards`, `traceability_labels`, and `svg_graphics`.

The one-command launcher `scripts/run-validated-output-poc-demo.ps1` runs the output POC generator, runs SVG structural validation, writes `validated-output-poc-demo-summary.json`, adds a browser-visible `validated-output-poc-demo-summary` section to `index.html`, and opens the latest validated browser UI by default. Use `-NoOpenBrowser` for terminal-only verification. The helper command `scripts/open-latest-output-poc-graphics.ps1` opens the latest generated `graphics/` folder and prints the full paths to the expected SVG files. The helper command `scripts/open-latest-output-poc-browser.ps1` opens the latest generated browser UI and warns if the SVG structural validation summary has not been added yet. The validator command `scripts/validate-output-poc-svg-graphics.ps1` checks that the latest generated SVG graphics exist, contain required deterministic metadata, are linked from `index.html`, are referenced in `run-metadata.json`, do not contain external image references or approval claims, writes `svg-structural-validation.json` as a durable validation report, adds a `svg_structural_validation` summary to `graphic-output-review-packet.json`, and adds a browser-visible `svg-structural-validation-summary` section to `index.html`. This flow does not generate final production graphics, load local images, decode images, inspect pixels, fetch network resources, run CV/OCR, or approve automatically.

### Business demo UI - Toyota Supra presenter and feedback workflow

Use these documents after opening the browser UI with business reviewers:

```powershell
pytest tests/test_business_demo_ui_toyota_supra_presenter_runbook.py
pytest tests/test_business_demo_ui_toyota_supra_viewer_feedback_card.py
pytest tests/test_business_demo_ui_toyota_supra_feedback_synthesis_log.py
pytest tests/test_business_demo_ui_toyota_supra_readiness_handoff.py
```

Document paths:

```text
docs/800_Demos/Business_Demo_UI_Toyota_Supra_Presenter_Runbook.md
docs/800_Demos/Business_Demo_UI_Toyota_Supra_Viewer_Feedback_Card.md
docs/800_Demos/Business_Demo_UI_Toyota_Supra_Feedback_Synthesis_Log.md
docs/800_Demos/Business_Demo_UI_Toyota_Supra_Readiness_Handoff.md
```

This workflow is documentation-only. It provides a presenter talk track, a business-viewer feedback card, a synthesis log, and a readiness handoff for deciding whether reviewer feedback supports moving to Constraint-Driven Graphic Output Permutation POC v1. It does not authorize generated final graphics, real local image input, image decoding, CV/OCR, or automatic approval.

### Constraint-driven output permutation POC contract and fixture data

Use these verification commands to check the gated output-permutation milestone, contract, and Toyota fixture data:

```powershell
pytest tests/test_constraint_driven_graphic_output_permutation_poc.py
pytest tests/test_constraint_driven_graphic_output_permutation_contract.py
pytest tests/test_constraint_driven_graphic_output_permutation_toyota_fixtures.py
```

Document paths:

```text
docs/500_Milestones/Constraint_Driven_Graphic_Output_Permutation_POC_v1.md
docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Contract.md
docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Toyota_Fixtures.md
```

These documents define the fixture-safe output contract and deterministic Toyota Supra A80 / 2JZ-GTE permutation data. They do not authorize generated final graphics, production artwork, real local image input, image decoding, pixel inspection, CV/OCR, or automatic approval.

### Current evidence-harness POC demo guide

Use this guide to explain the current evidence-harness demo separately from the later constraint-driven graphic output permutation target:

```powershell
pytest tests/test_current_evidence_harness_poc_demo_guide.py
```

Guide path:

```text
docs/800_Demos/Current_Evidence_Harness_POC_Demo_Guide.md
```

This guide is documentation-only. It explains that `scripts/watch-constraintos-poc.ps1` is the current evidence-harness demo and that the future output-permutation demo is intentionally banked for a later milestone.

### Current evidence-harness POC demo readiness packet

Use this packet as the reviewer-facing checklist for the current evidence-harness demo:

```powershell
pytest tests/test_current_evidence_harness_poc_demo_readiness_packet.py
```

Packet path:

```text
docs/800_Demos/Current_Evidence_Harness_POC_Demo_Readiness_Packet.md
```

This packet is documentation-only. It records what to run, what reviewers should see, which run artifacts to inspect first, what is intentionally not included yet, and how the future constraint-driven graphic output permutation demo is banked for later.

### Current evidence-harness POC demo feedback packet

Use this packet to collect structured critique after reviewers watch the current evidence-harness demo:

```powershell
pytest tests/test_current_evidence_harness_poc_demo_feedback_packet.py
```

Packet path:

```text
docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Packet.md
```

This packet is documentation-only. It provides a copyable feedback form, evidence-file inspection prompts, feedback classification labels, current limitations, and the banked future constraint-driven graphic output permutation target.

### Demo feedback issue template

Use this GitHub issue template to collect reviewer feedback directly through GitHub Issues:

```powershell
pytest tests/test_demo_feedback_issue_template.py
```

Template path:

```text
.github/ISSUE_TEMPLATE/demo-feedback.md
```

This template mirrors the current evidence-harness POC demo feedback packet and keeps reviewer critique structured around demo flow, evidence quality, technical trust, current limitations, future output expectations, and next steps.

### Current evidence-harness POC demo feedback triage guide

Use this guide to sort incoming demo-feedback issues and notes without accidentally expanding scope:

```powershell
pytest tests/test_current_evidence_harness_poc_demo_feedback_triage_guide.py
```

Guide path:

```text
docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Triage_Guide.md
```

This guide is documentation-only. It defines feedback categories, severity levels, current-demo polish examples, later-milestone examples, and a triage note format for reviewer feedback.

### Current evidence-harness POC demo feedback synthesis log

Use this log to turn triaged reviewer feedback into prioritized action decisions:

```powershell
pytest tests/test_current_evidence_harness_poc_demo_feedback_synthesis_log.py
```

Log path:

```text
docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Synthesis_Log.md
```

This log is documentation-only. It records feedback themes, categories, severity, current-demo versus later-track decisions, follow-ups, and status without authorizing new processing capabilities.
