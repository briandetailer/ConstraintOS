# Candidate Manifest Schema v1

## Status

```text
milestone: Candidate Manifest Schema v1
status: implementation-complete-pending-test
started_on: 2026-07-08
previous_gate: Candidate Evaluation Adapter Design v1 complete
baseline: 487 passed
```

## Purpose

Define a static manifest schema for externally produced candidate graphics.

This milestone creates the fixture-only boundary required before any future candidate-evaluation command can exist.

## Scope

```text
- Add a candidate manifest JSON Schema.
- Add static candidate manifest examples.
- Bind examples to existing graphics contract keys.
- Preserve external-candidate-only behavior.
- Preserve no image generation, no image editing, and no real image ingestion.
- Preserve not_evaluated / needs_review defaults.
- Add schema and guardrail tests.
- Update the command reference with new verification commands.
```

## Out of scope

```text
- No candidate-evaluation CLI command.
- No real image loading or decoding.
- No computer-vision integration.
- No image generation.
- No image editing.
- No approval automation change.
```

## Implementation slices

```text
[x] Create milestone doc
[x] Add candidate manifest schema
[x] Add static candidate manifest examples
[x] Add schema and guardrail tests
[x] Update candidate evaluation README
[x] Update command reference
[ ] Run tests and record verified result
```

## Implemented files

```text
examples/graphics/candidate_evaluation/candidate_manifest.schema.json
examples/graphics/candidate_evaluation/perseverance_candidate_manifest.fixture.json
examples/graphics/candidate_evaluation/supra_2jz_gte_candidate_manifest.fixture.json
examples/graphics/candidate_evaluation/README.md
tests/test_candidate_manifest_schema.py
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Verification command

```powershell
pytest tests/test_candidate_manifest_schema.py
```

## Schema boundaries

```text
- Manifest status is static_fixture_only.
- Candidate source type is external.
- generated_by_constraintos must be false.
- Candidate reference status is reference_only_not_loaded.
- Evaluation status is not_evaluated.
- Initial decision is needs_review.
- Uncertainty default is needs_review.
```

## Guardrails

```text
- Candidate manifests reference external candidates only.
- Candidate manifests must not contain image bytes.
- Candidate manifests must not claim ConstraintOS generated the candidate.
- Candidate manifests must not mark candidates evaluated or approved.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Candidate manifest JSON Schema exists.
[x] Static Perseverance candidate manifest fixture exists.
[x] Static Supra 2JZ-GTE candidate manifest fixture exists.
[x] Fixtures validate against the schema.
[x] Tests reject ConstraintOS-generated candidate claims.
[x] Tests reject approved initial decisions.
[x] Command reference updated in the same implementation slice.
[ ] Verification test result recorded.
```
