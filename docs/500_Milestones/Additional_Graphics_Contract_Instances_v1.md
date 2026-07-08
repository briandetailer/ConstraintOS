# Additional Graphics Contract Instances v1

## Status

```text
milestone: Additional Graphics Contract Instances v1
status: active
started_on: 2026-07-08
previous_gate: Reusable Graphics Validation Contracts v1 complete
baseline: 487 passed
```

## Purpose

Add reusable graphics-validation contract instances for the remaining documented engineering-graphics use cases.

This milestone keeps the system fixture-only. It does not introduce image generation or generated-candidate evaluation.

## Source use cases

```text
docs/700_Use_Cases/Use_Case_2_NREL_5MW_Wind_Turbine_Nacelle_Drivetrain_Cutaway.md
docs/700_Use_Cases/Use_Case_3_Hydroelectric_Dam_Powerhouse_Cross_Section.md
docs/700_Use_Cases/Use_Case_4_Toyota_Supra_A80_2JZ_GTE_Twin_Turbo_Technical_Graphic.md
```

## Contract instances

```text
examples/graphics/contracts/wind_turbine_nacelle.contract.json
examples/graphics/contracts/hydroelectric_dam_powerhouse.contract.json
examples/graphics/contracts/supra_2jz_gte_twin_turbo.contract.json
```

## Implementation slices

```text
[x] Create milestone doc
[ ] Add wind turbine contract instance
[ ] Add hydroelectric dam contract instance
[ ] Add Supra 2JZ-GTE contract instance
[ ] Update graphics contracts README
[ ] Extend contract tests across all contract instances
[ ] Run tests and record verified result
```

## Guardrails

```text
- Keep all new contracts in fixture_only_no_image_generation mode.
- Use needs_review as the initial fixture-only decision until real candidate evaluation exists.
- Do not introduce image generation.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[ ] All three new contract instances exist.
[ ] All contract instances satisfy the reusable schema.
[ ] Tests confirm each contract preserves the key subject identity and forbidden substitution guardrails.
[ ] README documents all contract instances.
[ ] Verification test result recorded.
```
