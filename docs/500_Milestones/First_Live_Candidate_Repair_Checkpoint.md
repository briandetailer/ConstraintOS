# First Live Candidate Repair Checkpoint

## Status

```text
milestone: Research-to-Render Orchestration
checkpoint: first live reference-conditioned candidate validation
recorded_on: 2026-07-20
branch: phase-1-cli-tooling
result: rejected_with_actionable_repairs
next_action: bounded_validator_directed_repair_and_revalidation
```

## Observed live result

The Raspberry Pi 5 reference-conditioned image-generation worker produced a new candidate PNG and a generated-candidate manifest. The independent visual validator rejected the candidate and kept `approval_allowed`, `production_ready`, and automatic approval false.

The validator identified two concrete failures:

```text
1. The two USB 2.0 receptacles were not unambiguously rendered as a stacked pair.
2. The RTC battery connector was not clearly depicted as the correct two-pin keyed header at the correct location and orientation relative to the fan connector.
```

The validation manifest returned:

```text
overall_machine_decision: rejected
next_action: repair_or_reject
manual_review_required: true
```

This is valid ConstraintOS behavior. Generation did not approve itself, the validator checked the candidate against the researched reference and requested features, and the failed artifact was stopped before publication finishing.

## Implemented repair behavior

The new bounded repair worker:

```text
failed candidate + authoritative reference + original constraints
        ↓
validator repair instructions
        ↓
reference-conditioned edit request
        ↓
repaired candidate with parent lineage and SHA-256
        ↓
independent validation
        ↓
stop on machine pass or configured attempt limit
```

Repair rules:

```text
- the first image remains the authoritative reference
- the second image is the rejected candidate to revise
- every validator repair instruction is included verbatim
- already-correct areas must be preserved
- unrelated regions may not be redesigned or restyled
- generated text and callouts remain prohibited
- every repair candidate is revalidated independently
- maximum attempts are bounded from 0 through 5
- default automatic repair attempts: 2
- approval remains manual after a machine pass
```

## New artifacts

```text
runtime/research_to_render/candidate_repair.py
scripts/repair-constraintos-candidate-run.ps1
tests/test_reference_conditioned_candidate_repair.py
```

The normal Raspberry Pi generation script now runs the repair loop automatically after validation unless `-DisableAutoRepair` is supplied. Existing rejected runs can be resumed without regenerating the initial candidate.

## Current acceptance state

```text
[x] live reference-conditioned candidate generated
[x] independent visual validation completed
[x] invalid candidate rejected
[x] actionable repair instructions produced
[x] bounded repair package implemented
[x] repaired candidate lineage and digests recorded
[x] independent revalidation after every repair
[ ] execute repair against the first live rejected candidate
[ ] review repaired candidate and final validation evidence
[ ] add deterministic annotation after human approval
```
