# Business Demo UI Toyota Supra v1

## Status

```text
milestone: Business Demo UI Toyota Supra v1
status: implementation-complete-pending-test
started_on: 2026-07-10
track: Business Demo Visibility Track
previous_track_status: Current Evidence-Harness POC Demo package complete
previous_progress_snapshot: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Progress_Snapshot.md
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
scenario_key: supra_2jz_gte_twin_turbo
```

## Purpose

Create a business-person-friendly browser demo that shows the current ConstraintOS evidence-harness workflow without requiring the viewer to read terminal output, JSON files, or internal milestone documents.

The demo should make the product idea visible as a staged flow:

```text
business request -> constraints -> candidate evidence -> deterministic review -> needs_review decision
```

## Why this is needed

The current evidence-harness package is technically complete and shareable, but the raw run files are still too technical for business reviewers.

Business viewers need to see:

```text
- what was requested
- what rules were loaded
- what the system checked
- what decision came out
- why automatic approval is blocked
- what the next product-shaped milestone will add
```

They should not need to understand fixture files, JSON schemas, command-line stages, or implementation guardrails to follow the story.

## Scope

```text
- Add scripts/watch-business-demo-ui.ps1.
- Default the demo to the Toyota Supra A80 / 2JZ-GTE use case.
- Generate a static browser UI under runs/business-demo-ui/<scenario>/<timestamp>/.
- Create index.html for the business-facing walkthrough.
- Create demo-data.json for the deterministic UI data.
- Create run-metadata.json for traceability.
- Include auto-play stage progression in the browser page.
- Include business-friendly cards for request, constraints, evidence, decision, and next step.
- Preserve final_decision: needs_review.
- Preserve approval_allowed: false.
- Preserve no generated final graphics.
- Preserve no image decoding, pixel inspection, CV/OCR, network fetch, or automatic approval.
- Add tests.
- Update command reference.
```

## Out of scope

```text
- No generated final graphics.
- No constraint-derived graphic output permutations yet.
- No real local image input.
- No local_file_path loading.
- No file_uri loading.
- No artifact download.
- No network fetch.
- No image decoding.
- No pixel inspection.
- No CV/OCR provider integration.
- No unrestricted image generation.
- No unrestricted image editing.
- No automatic scoring.
- No automatic approval.
```

## Business demo command

```powershell
.\scripts\watch-business-demo-ui.ps1
.\scripts\watch-business-demo-ui.ps1 -Scenario supra_2jz_gte_twin_turbo
.\scripts\watch-business-demo-ui.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser
```

## Generated output

```text
runs/business-demo-ui/<scenario>/<timestamp>/index.html
runs/business-demo-ui/<scenario>/<timestamp>/demo-data.json
runs/business-demo-ui/<scenario>/<timestamp>/run-metadata.json
```

## Business-viewer story

```text
1. A requester asks for a Toyota Supra A80 2JZ-GTE twin-turbo technical graphic.
2. ConstraintOS loads the important requirements: Supra Mk IV/A80, 2JZ-GTE inline-six, sequential twin-turbo, not a generic engine.
3. The current evidence harness reviews fixture candidate evidence against those requirements.
4. The system produces a visible decision: needs_review.
5. The UI explains why needs_review is good: the system is proving traceability and refuses automatic approval until the evidence is sufficient.
6. The UI points to the next product-shaped milestone: Constraint-Driven Graphic Output Permutation POC v1.
```

## Intended result

```text
business_demo_ui_created: true
business_viewer_can_follow_without_json: true
scenario: supra_2jz_gte_twin_turbo
final_decision: needs_review
approval_allowed: false
next_product_track: Constraint-Driven Graphic Output Permutation POC v1
```

## Verification command

```powershell
pytest tests/test_business_demo_ui_toyota_supra.py
```

## Guardrails

```text
- Browser UI only.
- Static fixture-only walkthrough.
- No new runtime processing authority.
- No new candidate-generation capability.
- No generated final graphics.
- No real local image input.
- No image decoding.
- No CV/OCR provider integration.
- No automatic candidate approval.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Milestone exists.
[x] Browser demo script exists.
[x] Toyota Supra / 2JZ-GTE scenario is the default.
[x] Script writes index.html.
[x] Script writes demo-data.json.
[x] Script writes run-metadata.json.
[x] UI shows business-friendly workflow stages.
[x] UI exposes needs_review and approval_allowed: false.
[x] UI explains the next product-shaped milestone.
[x] Guardrails are preserved.
[x] Tests added.
[x] Command reference updated.
[ ] Verification test result recorded.
```
