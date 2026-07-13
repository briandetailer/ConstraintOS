# Fixture-Safe Placeholder Browser Implementation v1

## Status

```text
milestone: Fixture-Safe Placeholder Browser Implementation v1
status: active
kickoff_status: complete
phase_1_browser_placeholder_contract_activation_status: complete
phase_2_watch_script_browser_update_status: ready-for-verification
started_on: 2026-07-13
track: Business Demo Visibility Track
previous_milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md
previous_contract: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Refinement_Contract.md
previous_panel_design: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Panel_Design.md
previous_evidence_summary_cards: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Evidence_Summary_Cards.md
previous_reviewer_handoff: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Reviewer_Handoff.md
previous_closeout: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Closeout.md
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: deterministic-browser-placeholders-only
latest_user_reported_fixture_safe_placeholder_browser_implementation_milestone_test_result: 6 passed
latest_user_reported_fixture_safe_placeholder_browser_implementation_milestone_test_result_on: 2026-07-13
assistant_ran_tests: false
assistant_ran_demo: false
```

## Purpose

Implement the completed fixture-safe visual placeholder refinement into the existing output-permutation browser demo so reviewers can see deterministic placeholder panels and evidence summary cards in the generated `index.html`.

This milestone moves from specification to browser-visible artifact while keeping the same safety boundary:

```text
output permutations -> deterministic placeholder panels -> evidence summary cards -> needs_review
```

## Product promise for this milestone

```text
- Add browser-visible placeholder panels for the four Toyota Supra permutations.
- Add evidence summary cards beside or inside each placeholder panel.
- Preserve the existing generated run artifact structure.
- Preserve needs_review for every variant.
- Preserve approval_allowed: false.
- Keep every visual element deterministic and fixture-defined.
- Update tests and command reference when the watch script behavior changes.
```

## Target implementation area

```text
script: scripts/watch-constraintos-output-poc.ps1
browser_artifact: runs/output-poc/<scenario>/<timestamp>/index.html
supporting_json_artifacts:
- graphic-output-manifest.json
- graphic-output-permutations.json
- graphic-output-validation.json
- graphic-output-review-packet.json
- run-metadata.json
command_reference: docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Required browser additions

```text
1. Placeholder panel section
   - one panel for each permutation_id
   - fixture-safe visual tokens only
   - visible statement that panel is not final artwork

2. Evidence summary card section
   - one evidence card for each permutation_id
   - satisfied constraints
   - visible uncertainty
   - blocked claims
   - review decision and approval state

3. Traceability labels
   - engine_identity
   - vehicle_identity
   - turbo_identity
   - wrong_engine_exclusion
   - review_safety

4. Guardrail copy
   - no generated final graphics
   - no real local image input
   - no image decoding
   - no pixel inspection
   - no CV/OCR provider integration
   - no automatic approval
```

## Implementation changes now under verification

```text
script_update: scripts/watch-constraintos-output-poc.ps1
command_reference_update: docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
verification: pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py
status: ready-for-verification
```

The watch script now writes browser-visible deterministic placeholder panels and evidence summary cards into `index.html`, and records placeholder/evidence metadata in `run-metadata.json`.

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

## Proposed implementation phases

```text
Phase 1: browser placeholder contract activation
- Map prior placeholder contracts into expected browser output terms.
- Define testable HTML markers before changing script behavior.

Phase 2: watch script browser update
- Add deterministic placeholder panels to generated index.html.
- Add deterministic evidence summary cards to generated index.html.

Phase 3: artifact metadata update
- Include placeholder/evidence section metadata in run-metadata.json if needed.
- Keep all metadata fixture-safe and deterministic.

Phase 4: command reference update
- Update the graphics validation command reference if the watch script output contract changes.

Phase 5: verification and closeout
- Record user-reported local verification.
- Complete the milestone only after tests pass.
```

## Kickoff verification record

```text
source: user-reported local test run
command: pytest tests/test_fixture_safe_placeholder_browser_implementation_milestone.py
result: 6 passed
reported_on: 2026-07-13
assistant_ran_tests: false
```

## Done criteria for kickoff slice

```text
[x] Milestone exists.
[x] Previous fixture-safe refinement milestone is referenced.
[x] Browser implementation target is defined.
[x] Required browser additions are scoped.
[x] Existing run artifact structure is preserved.
[x] Command reference maintenance is called out.
[x] Blocked scope is preserved.
[x] Proposed implementation phases are defined.
[x] Verification test result recorded.
```

## Verification command

```powershell
pytest tests/test_fixture_safe_placeholder_browser_implementation_milestone.py
pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py
```
