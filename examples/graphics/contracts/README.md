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

## Schema

```text
graphics_validation_contract.schema.json
```

The schema describes the reusable structure expected by graphics-validation contract instances.

## Current contract instances

```text
perseverance.contract.json
wind_turbine_nacelle.contract.json
hydroelectric_dam_powerhouse.contract.json
supra_2jz_gte_twin_turbo.contract.json
```

## CLI discovery

List available contracts:

```powershell
cos-graphics-contracts list
```

Show a contract summary:

```powershell
cos-graphics-contracts show perseverance
cos-graphics-contracts show wind_turbine_nacelle
cos-graphics-contracts show hydroelectric_dam_powerhouse
cos-graphics-contracts show supra_2jz_gte_twin_turbo
```

Run a contract-backed runtime bridge without image generation:

```powershell
cos-graphics-contracts run perseverance --plan-only
cos-graphics-contracts run wind_turbine_nacelle
cos-graphics-contracts run hydroelectric_dam_powerhouse
cos-graphics-contracts run supra_2jz_gte_twin_turbo
```

Write JSON reports:

```powershell
cos-graphics-contracts --format json --output reports/graphics-contracts.json list
cos-graphics-contracts --format json --output reports/supra-contract-runtime.json run supra_2jz_gte_twin_turbo
```

## Source use cases

```text
perseverance.contract.json:
  docs/700_Use_Cases/Use_Case_1_NASA_Perseverance_Rover_Technical_Graphic.md

wind_turbine_nacelle.contract.json:
  docs/700_Use_Cases/Use_Case_2_NREL_5MW_Wind_Turbine_Nacelle_Drivetrain_Cutaway.md

hydroelectric_dam_powerhouse.contract.json:
  docs/700_Use_Cases/Use_Case_3_Hydroelectric_Dam_Powerhouse_Cross_Section.md

supra_2jz_gte_twin_turbo.contract.json:
  docs/700_Use_Cases/Use_Case_4_Toyota_Supra_A80_2JZ_GTE_Twin_Turbo_Technical_Graphic.md
```

## Verification

```powershell
pytest tests/test_graphics_contracts.py
pytest tests/test_graphics_contracts_cli.py
pytest tests/test_graphics_contract_runtime_bridge.py
```

## Guardrail

Contracts are validation fixtures only. They do not generate images.
