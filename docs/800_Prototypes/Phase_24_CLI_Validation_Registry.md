# Phase 24: CLI Validation Registry Refactor

Status: Complete Baseline
Version: 1.0.0-alpha.24

## Purpose
Phase 24 introduces a central schema registry so artifact detection and schema lookup no longer need to be repeatedly encoded inside the CLI.

## Implemented Scope

- Schema registry module
- Schema registration model
- Central schema registry tuple
- Special schema detection rules
- Registry-driven schema detection
- Registry-driven record type detection
- Registry report generator
- Schema registry report schema
- Schema registry tests
- Schema registry report example
- Package version bumped to `1.0.0-alpha.24`

## Registry Philosophy

Artifact families should be registered once. CLI validation, traceability, diagnostics, and future API tooling should consume a shared registry rather than each maintaining separate detection logic.

## Design Rules

1. Schema detection must be centralized.
2. Special-case detection must be explicit.
3. Registry output must be auditable.
4. Future artifact families should extend the registry rather than expanding CLI conditionals.
5. The registry must not redefine schema semantics; it only maps artifact keys to schemas and record types.

## Deferred

- Full CLI replacement of legacy internal detection tables.
- Registry-backed duplicate ID audit command.
- Full repository validation from the connector environment.

## Recommended Phase 25

Phase 25 should complete registry adoption in the CLI:

1. Replace CLI `detect_schema` with registry import.
2. Replace CLI record type mapping with registry helper.
3. Add `constraintos registry-report` command.
4. Add duplicate ID audit diagnostics.
5. Add validation regression tests against examples.
