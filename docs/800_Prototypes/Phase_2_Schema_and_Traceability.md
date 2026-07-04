# Phase 2: Schema Hardening and Automated Traceability

Status: Complete Baseline
Version: 0.2

## Purpose
Phase 2 hardens ConstraintOS from a simple repository CLI into a schema-aware documentation system. The objective is to make repository artifacts machine-checkable before renderer integration begins.

## Completed Scope

- CSL schema baseline
- Failure record schema
- Compliance report schema
- ID registry schema
- Schema-validation dependency
- Traceability hardening plan

## Phase 2 Design Rules

1. YAML artifacts are the canonical editable format.
2. JSON Schema provides machine-verifiable structure.
3. Markdown remains the human-readable documentation layer.
4. IDs must be stable, unique, and traceable.
5. Compliance reports must remain renderer-independent.
6. Renderer integration remains deferred until schemas and traceability are reliable.

## Canonical Schema Set

- `schemas/csl.schema.json`
- `schemas/failure.schema.json`
- `schemas/compliance-report.schema.json`
- `schemas/id-registry.schema.json`

## Traceability Targets

Every artifact should eventually report:

- ID
- title
- type
- status
- path
- related failures
- related requirements
- related ADRs
- related validators
- related tests

## Phase 2 Acceptance Criteria

- Repository contains schemas for the core data objects.
- CLI package includes schema validation dependency.
- Phase 3 can implement deeper validation without redesigning Phase 1.
- Renderer work remains intentionally blocked until schema-driven validation matures.

## Recommended Phase 3
Phase 3 should implement the validator runtime:

1. Wire JSON Schema validation into the CLI.
2. Add ID registry generation.
3. Add duplicate ID detection.
4. Add Markdown export from YAML.
5. Add traceability matrix generation.
6. Add compliance report stubs.
7. Add tests for schema validation and traceability outputs.
