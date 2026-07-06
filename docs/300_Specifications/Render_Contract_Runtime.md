# Render Contract Runtime

The render contract compiler converts a render specification into a runtime specification that can be planned, scheduled, and executed by `cos-runtime`.

## Compiler flow

```text
Render Specification
  ↓
Optional Constraint Packs
  ↓
Render Contract Runtime Specification
  ↓
Runtime Planner / Scheduler / Executor
```

## Generated runtime steps

The compiler produces four deterministic runtime steps:

1. `load_subject`
2. `check_requirements`
3. `check_negative_constraints`
4. `check_validation_gates`

Each step uses the `render_contract` plugin.

## Constraint pack traceability

When a render specification has applied constraint pack references, the compiler preserves those references in the generated runtime specification.

They are recorded in:

- `artifact.constraint_packs`
- `render_contract.constraint_packs`

This keeps pack provenance visible after the render specification is compiled into runtime form.
