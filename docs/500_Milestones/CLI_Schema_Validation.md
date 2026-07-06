# Milestone: CLI Schema Validation

CLI Schema Validation hardens the command-line boundary for render specifications and Constraint Packs.

## Goal

Command-line tools should reject malformed or wrong-type inputs before they enter the runtime, validation, or applicator layers.

This prevents invalid records from being merged, compiled, validated, or reported as if they were trustworthy.

## Covered commands

```powershell
cos-apply-constraints <render-specification> <constraint-pack...>
```

```powershell
cos-validate <render-specification> --constraint-pack <constraint-pack>
```

```powershell
cos-runtime <render-specification> --render-contract --constraint-pack <constraint-pack> --plan-only
```

## Current guarantees

- Render specifications are checked against the registered render specification schema before use.
- Constraint Packs are checked against the registered Constraint Pack schema before use.
- CLI callers get exit code `2` when schema validation fails.
- Error output includes the schema path and failing field.
- Wrong record types are rejected before pack application or render-contract compilation.
- Reusable schema validation lives in `constraintos.schema_validation`.

## Out of scope

This milestone does not add visual validation, renderer integration, or external image-generation calls. It only hardens structured input boundaries before existing deterministic workflows run.
