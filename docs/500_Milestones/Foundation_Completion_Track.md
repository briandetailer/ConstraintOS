# Foundation Completion Track

## Status

```text
track: Foundation Completion Track
status: active
started_on: 2026-07-08
previous_gate: Candidate Manifest Schema v1 complete
```

## Purpose

Explicitly finish the graphics-validation foundation before moving into real candidate evaluation, image ingestion, computer vision, image generation, or UI work.

This track exists to prevent scope drift.

## Why this track exists

ConstraintOS started from a practical failure mode: generated technical graphics can look plausible while violating required subject identity, geometry, labels, placement, and style rules.

The foundation must therefore prove that ConstraintOS can define, discover, run, report, and review constraints before any real generated candidate image is evaluated or generated.

## Foundation completion sequence

```text
1. Candidate Manifest Discovery v1
2. Candidate Evaluation Report Contract v1
3. Fixture-only Candidate Evaluation v1
4. Foundation Readiness Review v1
```

## Explicitly deferred until after this track

```text
- real image loading or decoding
- computer-vision integration
- image generation integration
- image editing integration
- approval automation changes
- end-user UI / ConstraintOS Console
- registry/public distribution decisions
```

## Guardrails

```text
- Keep new work read-only or fixture-only unless the milestone explicitly says otherwise.
- Keep candidate images external until real ingestion is deliberately approved.
- Default uncertainty and missing evidence to needs_review.
- Update docs/700_Use_Cases/Graphics_Validation_Command_Reference.md whenever new user-facing commands are introduced.
- Do not claim tests passed unless actually run or user reports exact results.
```
