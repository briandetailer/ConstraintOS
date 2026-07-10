# End-to-End Fixture POC Demo v1

## Status

```text
milestone: End-to-End Fixture POC Demo v1
status: implementation-complete-pending-test
started_on: 2026-07-10
previous_demo_outline: docs/800_Demos/End_to_End_Fixture_POC_Demo_Outline.md
track: Business Demo Visibility Track
baseline: 487 passed
product_correction_recorded_on: 2026-07-10
corrected_next_demo_target: Constraint-Driven Graphic Output Permutation POC v1
```

## Purpose

Implement a one-command fixture-based POC demo harness that shows ConstraintOS processing a named scenario through the current deterministic graphics validation and candidate evidence pipeline.

This milestone exists so friends, reviewers, and early stakeholders can see the current product workflow in motion: scenario selection, contract/specification loading, candidate intake review, deterministic byte-loading evidence, registry review, failure-matrix review, observation evidence, evidence merge, candidate evaluation, final review packet, and demo summary.

## Product correction

A product correction was recorded after implementation: the full POC should not stop at evidence and review packets.

The corrected POC target is:

```text
input_constraints + scenario instructions -> graphic output permutations -> validation evidence -> reviewable result
```

The intended product output should be a series of graphic outputs, or fixture-safe graphic-output specifications/placeholders, derived from loaded constraints. The evidence and review packets should explain whether each output satisfies, fails, or needs review against the loaded requirements.

This milestone remains useful as an evidence-harness demo, but it is not the full corrected product-shaped demo. The next demo milestone should add constraint-driven output permutations.

## Product charter alignment

```text
product_charter_seed: ConstraintOS is an open architecture for deterministic, auditable, specification-driven publishing using probabilistic AI systems.
mission_seed: Structured specifications, validation, and traceability — not AI model behavior — are the source of truth.
demo_principle: Show the validation path in motion without weakening constraints.
business_demo_goal: Make the current POC feel like an input-to-result product workflow while identifying the next missing output-permutation layer.
```

## Scope

```text
- Add scripts/watch-constraintos-poc.ps1.
- Provide one command that demos the fixture-based end-to-end POC evidence path.
- Support -Scenario perseverance by default.
- Support alternate scenarios such as supra_2jz_gte_twin_turbo.
- Show stage-by-stage terminal output.
- Load the graphics validation contract/specification.
- Load candidate manifest/intake evidence.
- Generate candidate intake review evidence.
- Load deterministic fixture bytes.
- Generate byte-loading evidence.
- Generate byte-loading review packet evidence.
- Generate fixture registry review evidence.
- Generate fixture registry failure review evidence.
- Load manual observation evidence.
- Bind observations to report structure.
- Merge evidence into candidate report evidence.
- Evaluate candidate fixture evidence.
- Generate final candidate review packet.
- Generate demo-summary.json.
- Capture terminal transcript and watch output.
- Capture JSON evidence files under runs/poc-demo/<scenario>/<timestamp>/.
- Preserve no local image file opening.
- Preserve no artifact download.
- Preserve no network fetch.
- Preserve no image decoding.
- Preserve no candidate scoring automation beyond existing fixture-only evaluation.
- Preserve no source report mutation.
- Preserve no approval automation.
- Update tests.
- Update command reference.
```

## Out of scope

```text
- No real local image file input.
- No local_file_path byte loading.
- No file_uri byte loading.
- No artifact download.
- No network fetch.
- No implicit cloud download.
- No image decoding.
- No pixel inspection.
- No computer-vision provider integration.
- No OCR provider integration.
- No unrestricted image generation.
- No unrestricted image editing.
- No automatic candidate approval.
```

## Implemented files

```text
docs/500_Milestones/End_to_End_Fixture_POC_Demo_v1.md
scripts/watch-constraintos-poc.ps1
tests/test_end_to_end_fixture_poc_demo.py
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Demo command

```powershell
.\scripts\watch-constraintos-poc.ps1
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
.\scripts\watch-constraintos-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -WatchDelayMs 750
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance -OpenRunFolder
```

## Demo stages

```text
1. Load scenario.
2. Load contract/specification.
3. Load candidate manifest and intake evidence.
4. Validate intake boundaries through review packet evidence.
5. Load deterministic fixture bytes.
6. Generate byte-loading and registry evidence.
7. Review fixture registry failure matrix.
8. Load and bind observation evidence.
9. Merge evidence and evaluate candidate fixture report.
10. Produce final review packet and demo summary.
```

## Demo outputs

```text
runs/poc-demo/<scenario>/<timestamp>/terminal-transcript.txt
runs/poc-demo/<scenario>/<timestamp>/watch-output.txt
runs/poc-demo/<scenario>/<timestamp>/contract.json
runs/poc-demo/<scenario>/<timestamp>/candidate-manifest.json
runs/poc-demo/<scenario>/<timestamp>/candidate-intake.json
runs/poc-demo/<scenario>/<timestamp>/candidate-intake-review-packet.json
runs/poc-demo/<scenario>/<timestamp>/byte-loading.json
runs/poc-demo/<scenario>/<timestamp>/byte-loading-review-packet.json
runs/poc-demo/<scenario>/<timestamp>/fixture-registry-review-packet.json
runs/poc-demo/<scenario>/<timestamp>/fixture-registry-failure-review-packet.json
runs/poc-demo/<scenario>/<timestamp>/manual-observations.json
runs/poc-demo/<scenario>/<timestamp>/observation-binding.json
runs/poc-demo/<scenario>/<timestamp>/merged-evidence.json
runs/poc-demo/<scenario>/<timestamp>/evaluation-report.json
runs/poc-demo/<scenario>/<timestamp>/final-review-packet.json
runs/poc-demo/<scenario>/<timestamp>/demo-summary.json
runs/poc-demo/<scenario>/<timestamp>/run-metadata.json
```

## Intended result for this evidence-harness POC

```text
final_decision: needs_review
approval_allowed: false
reason: The system produced traceable evidence and review packets, but automatic approval remains intentionally blocked in the POC.
```

## Corrected intended result for the next product-shaped POC

```text
graphic_outputs_created: true
graphic_output_type: fixture-safe graphic-output specifications or controlled placeholder artifacts
permutation_count: scenario-defined
final_decision: needs_review
approval_allowed: false
reason: The system produced constraint-derived output permutations and traceable validation evidence, but automatic approval remains intentionally blocked in the POC.
```

## Required next milestone

```text
recommended_next_milestone: Constraint-Driven Graphic Output Permutation POC v1
primary_output: scripts/watch-constraintos-output-poc.ps1
supporting_output: graphic-output-manifest.json
verification: pytest tests/test_constraint_driven_graphic_output_permutation_poc.py
```

## Verification command

```powershell
pytest tests/test_end_to_end_fixture_poc_demo.py
```

## Guardrails

```text
- Fixture-based POC demo only.
- No new byte-loading source added.
- No local image file opening.
- No local_file_path loading.
- No file_uri loading.
- No artifact download.
- No network fetch.
- No image decoding.
- No CV/OCR provider choice.
- No unrestricted image generation.
- No unrestricted image editing.
- No automatic candidate approval.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] End-to-end fixture POC demo script exists.
[x] Demo defaults to perseverance.
[x] Demo supports alternate scenarios.
[x] Demo shows stage-by-stage terminal output.
[x] Demo loads contract/specification evidence.
[x] Demo loads candidate manifest/intake evidence.
[x] Demo generates intake review evidence.
[x] Demo loads deterministic fixture bytes.
[x] Demo generates byte-loading and registry evidence.
[x] Demo reviews fixture registry failure matrix evidence.
[x] Demo loads and binds observation evidence.
[x] Demo merges evidence and evaluates candidate fixture report.
[x] Demo produces final review packet and demo summary.
[x] Demo captures terminal transcript and watch output.
[x] Demo captures JSON evidence files.
[x] Demo writes run metadata.
[x] Demo preserves no local image file opening.
[x] Demo preserves no artifact download.
[x] Demo preserves no network fetch.
[x] Demo preserves no image decoding.
[x] Demo preserves no automatic candidate approval.
[x] Product correction recorded: corrected POC should output constraint-driven graphic permutations.
[x] Corrected next demo milestone identified.
[x] Command reference updated.
[ ] Verification test result recorded.
```
