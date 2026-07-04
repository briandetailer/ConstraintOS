# Phase 9: Multi-Pass Repair Loop

Status: Complete Baseline
Version: 0.9

## Purpose
Phase 9 introduces the first formal repair-loop model. ConstraintOS can now represent a deterministic build plan, create iteration records, run a dry-run compile-render-validate-review-patch flow, and stop based on explicit gate conditions.

## Implemented Scope

- Repair loop engine module
- Build plan schema
- Iteration record schema
- Build plan generation
- Iteration record generation
- Dry-run repair loop execution
- Patch creation from validation results
- Review gate integration
- Repair loop tests
- Example build plan
- Example iteration record
- Package version bumped to 0.9.0

## Loop Model

```text
Specification
  -> Compile
  -> Render
  -> Validate
  -> Review
  -> Patch
  -> Iterate or Stop
```

## Stop Conditions

1. Review gate passes.
2. Maximum iteration count is reached.
3. Unsupported constraints block compilation.
4. Future policy may stop on repeated failures or low confidence.

## Design Rules

1. The loop must be explicit and traceable.
2. Each iteration must produce a record.
3. Patch packages must be generated from failed or uncertain results.
4. Review gates are deterministic stop signals.
5. Dry-run execution must not call live renderers.
6. Live renderer integration remains deferred until adapter and storage contracts mature.

## Recommended Phase 10
Phase 10 should introduce renderer plugin execution boundaries and artifact output storage:

1. Output reference schema
2. Render job schema
3. Dry-run render job execution
4. Artifact output manifest updates
5. Storage backend abstraction
6. Renderer plugin registry
