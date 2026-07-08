# Reusable Graphics Validation Contracts v1

## Status

```text
milestone: Reusable Graphics Validation Contracts v1
status: active
started_on: 2026-07-08
previous_gate: Graphics Validation Watch Mode v1 complete
baseline: 487 passed
```

## Purpose

Extract the repeated graphics-validation structure from the NASA Perseverance example into reusable contracts that can support multiple engineering-graphics subjects.

This milestone keeps image generation out of scope. It focuses on reusable validation shape, evidence expectations, approval behavior, and fixture consistency.

## Source baseline

```text
examples/graphics/perseverance/spec.json
examples/graphics/perseverance/policy.json
examples/graphics/perseverance/expected_evidence.json
examples/graphics/perseverance/expected_approval.json
```

## Initial supported examples

```text
1. NASA Perseverance rover
2. NREL 5MW wind turbine nacelle / drivetrain cutaway
3. Hydroelectric dam powerhouse cross section
4. Toyota Supra A80 / 2JZ-GTE sequential twin turbo technical graphic
```

## Contract goals

```text
- Define reusable subject identity fields.
- Define reusable required geometry checks.
- Define reusable required label trace structure.
- Define reusable forbidden substitution handling.
- Define reusable uncertainty behavior.
- Define reusable evidence report shape.
- Define reusable approval decision behavior.
- Keep fixture-only mode explicit until generated-candidate adapters exist.
```

## Implementation slices

```text
[x] Create milestone doc
[ ] Create reusable graphics contract schema fixture
[ ] Create Perseverance contract instance from existing fixture
[ ] Add contract validation helper
[ ] Add tests for required contract fields
[ ] Add tests for Perseverance contract consistency with existing fixture
[ ] Document next contract instances for wind turbine, hydro dam, and Supra
[ ] Run tests and record verified result
```

## Guardrails

```text
- Do not introduce image generation in this milestone.
- Do not change the completed Perseverance runtime behavior unless needed for contract compatibility.
- Do not archive generated runs or screen recordings unless explicitly approved.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[ ] Reusable contract schema exists.
[ ] Perseverance contract instance exists.
[ ] Tests confirm the contract captures identity, geometry, labels, forbidden substitutions, evidence, approval, and uncertainty behavior.
[ ] Existing Perseverance runtime fixture remains compatible.
[ ] Next contract subjects are documented as follow-on work.
```
