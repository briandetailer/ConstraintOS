# Candidate Manifest Schema v1

## Status

```text
milestone: Candidate Manifest Schema v1
status: active
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
[ ] Add candidate manifest schema
[ ] Add static candidate manifest examples
[ ] Add schema and guardrail tests
[ ] Update candidate evaluation README
[ ] Update command reference
[ ] Run tests and record verified result
```

## Verification command

```powershell
pytest tests/test_candidate_manifest_schema.py
```

## Guardrails

```text
- Candidate manifests reference external candidates only.
- Candidate manifests must not contain image bytes.
- Candidate manifests must not claim ConstraintOS generated the candidate.
- Candidate manifests must not mark candidates evaluated or approved.
- Do not claim tests passed unless actually run.
```
