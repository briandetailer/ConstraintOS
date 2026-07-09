# Fixture-only Observation Evidence Merge v1

## Status

```text
milestone: Fixture-only Observation Evidence Merge v1
status: implementation-complete-pending-test
started_on: 2026-07-08
previous_gate: Observation-to-Report Binding v1 complete
track: Foundation Completion Track
baseline: 487 passed
```

## Purpose

Merge fixture-only manual observations with fixture-only candidate evaluation report evidence into a combined evidence view.

This milestone does not load real candidate images, score candidates, mutate report fixtures, or approve candidates. It only produces a derived fixture-only merge report that shows how manual observation items align with report evidence items.

## Scope

```text
- Add fixture-only observation evidence merge helper module.
- Add cos-graphics-candidates merge-evidence.
- Merge manual observation fixture items with candidate evaluation report evidence items by constraint_id.
- Preserve unmatched report evidence and unmatched manual observation items.
- Preserve needs_review for merged evidence.
- Preserve approval_allowed false.
- Support text and JSON output.
- Add tests for merge behavior, CLI output, and guardrails.
- Update candidate evaluation README.
- Update command reference with new available commands.
```

## Out of scope

```text
- No real image loading or decoding.
- No computer-vision provider integration.
- No OCR provider integration.
- No image generation.
- No image editing.
- No automatic approval.
- No candidate-evaluation scoring behavior change.
- No mutation of existing report fixtures.
```

## Implemented files

```text
docs/500_Milestones/Fixture_Only_Observation_Evidence_Merge_v1.md
src/constraintos/observation_evidence_merge.py
src/constraintos/candidate_manifests_cli.py
tests/test_observation_evidence_merge.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Verification command

```powershell
pytest tests/test_observation_evidence_merge.py
```

## CLI commands

```powershell
cos-graphics-candidates merge-evidence perseverance
cos-graphics-candidates merge-evidence supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-merged-evidence.json merge-evidence perseverance
```

## Merge boundaries

```text
- Merge mode is fixture_only.
- Candidate image references remain reference_only_not_loaded.
- Real image ingestion is not run.
- Computer vision is not run.
- OCR is not run.
- Image generation is not run.
- Approval automation is not run.
- Candidate scoring is not run.
- Source report mutation is not run.
- Recommendation remains needs_review.
- Approval remains disallowed.
```

## Guardrails

```text
- Merge behavior is fixture-only.
- Candidate image references remain reference_only_not_loaded.
- Manual observations cannot approve alone.
- Merged evidence cannot approve candidates.
- Source report fixtures are not mutated.
- Candidate scoring is not run.
- Recommendation remains needs_review.
- Approval remains disallowed.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Fixture-only observation evidence merge helper module exists.
[x] CLI exposes cos-graphics-candidates merge-evidence.
[x] Manual observation fixture items merge with report evidence items by constraint_id.
[x] Matched, manual-only, and report-only constraints are surfaced.
[x] Text output is supported.
[x] JSON output is supported.
[x] JSON file output is supported.
[x] Command reference updated in the same implementation slice.
[ ] Verification test result recorded.
```
