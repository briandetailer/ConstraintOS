# Phase 3: Validator Runtime and Repository Automation

Status: Complete Baseline
Version: 0.3

## Purpose
Phase 3 turns ConstraintOS from a scaffold generator into an operational repository validation runtime. The CLI can now validate schemas, detect duplicate IDs, generate ID registries, export traceability, create compliance report stubs, and export YAML artifacts to Markdown.

## Implemented Commands

### `constraintos validate`
Validates YAML artifacts for metadata completeness, applicable JSON Schema conformance, and duplicate IDs.

### `constraintos registry`
Generates a YAML ID registry from repository artifacts.

### `constraintos trace`
Generates a JSON traceability report from repository artifacts.

### `constraintos export-md`
Exports one YAML artifact into a basic Markdown representation.

### `constraintos new-compliance`
Creates a compliance report scaffold.

## Runtime Validation Layers

1. YAML parsing
2. Metadata shape checks
3. Schema detection
4. JSON Schema validation
5. Duplicate ID detection
6. Traceability extraction

## Design Constraints

- Validation remains repository-local.
- Renderer integration remains deferred.
- Schema validation is strict only where schemas exist.
- Markdown export is intentionally simple and will mature in later phases.

## Acceptance Criteria

- CLI supports schema-aware validation.
- CLI can generate an ID registry.
- CLI can create compliance report stubs.
- CLI can export YAML artifacts to Markdown.
- GitHub Actions runs tests, validation, trace generation, and registry generation.

## Recommended Phase 4
Phase 4 should implement compiler groundwork:

1. Renderer adapter interface.
2. Prompt compiler prototype.
3. CSL-to-instruction transformation.
4. Unsupported constraint reporting.
5. Compiler fixtures and tests.
6. No live renderer calls yet.
