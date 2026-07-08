# Reusable Graphics Validation Contracts v1

## Status

```text
milestone: Reusable Graphics Validation Contracts v1
status: implementation-complete-pending-test
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
[x] Create reusable graphics contract schema fixture
[x] Create Perseverance contract instance from existing fixture
[x] Add contract validation helper
[x] Add tests for required contract fields
[x] Add tests for Perseverance contract consistency with existing fixture
[x] Document next contract instances for wind turbine, hydro dam, and Supra
[ ] Run tests and record verified result
```

## Implemented files

```text
examples/graphics/contracts/README.md
examples/graphics/contracts/graphics_validation_contract.schema.json
examples/graphics/contracts/perseverance.contract.json
src/constraintos/graphics_contracts.py
tests/test_graphics_contracts.py
```

## Verification command

```powershell
pytest tests/test_graphics_contracts.py
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
[x] Reusable contract schema exists.
[x] Perseverance contract instance exists.
[x] Tests confirm the contract captures identity, geometry, labels, forbidden substitutions, evidence, approval, and uncertainty behavior.
[x] Existing Perseverance runtime fixture remains compatible by contract consistency checks.
[x] Next contract subjects are documented as follow-on work.
[ ] Verification test result recorded.
```
