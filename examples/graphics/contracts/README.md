# Graphics Validation Contracts

This directory contains reusable graphics-validation contract fixtures.

The contracts define the validation shape shared across engineering-graphics examples:

```text
- subject identity
- rendering requirements
- required labels
- geometry constraints
- component-location constraints
- forbidden substitutions
- decision policy
- evidence report expectations
- approval guardrails
```

## Current contract

```text
perseverance.contract.json
```

This contract was extracted from the NASA Perseverance graphics-validation fixture.

## Schema

```text
graphics_validation_contract.schema.json
```

The schema describes the reusable structure expected by graphics-validation contract instances.

## Follow-on contract instances

```text
wind_turbine_nacelle.contract.json
hydroelectric_dam_powerhouse.contract.json
supra_2jz_gte_twin_turbo.contract.json
```

These should be added after the Perseverance contract is verified.

## Guardrail

Contracts are validation fixtures only. They do not generate images.
