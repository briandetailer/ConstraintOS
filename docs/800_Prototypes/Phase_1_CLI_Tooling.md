# Phase 1: CLI and Repository Tooling

Status: Implemented Baseline
Version: 0.1

## Purpose
Phase 1 establishes the first executable layer of ConstraintOS: repository tooling that creates structured artifacts, failure records, validates metadata, and emits traceability reports.

## Commands

### `constraintos new-artifact`
Creates a YAML scaffold for an artifact.

Example:

```bash
constraintos new-artifact CPE-0007 "Compiler Framework" --type architecture
```

### `constraintos new-failure`
Creates a YAML scaffold for a failure record.

Example:

```bash
constraintos new-failure FR-0036 "Renderer ignores negative constraint" --family F100 --severity major
```

### `constraintos validate`
Validates YAML metadata scaffolds.

Example:

```bash
constraintos validate docs
```

### `constraintos trace`
Generates a JSON traceability report.

Example:

```bash
constraintos trace docs
```

## Phase 1 Scope
This phase intentionally does not integrate renderers. The goal is to harden the repository as a structured source of truth before allowing probabilistic systems into the workflow.

## Implemented Baseline

- Python package scaffold
- Console entry points: `constraintos` and `cos`
- Artifact creation
- Failure record creation
- Metadata validation
- Traceability report generation
- Initial CSL JSON Schema
- Example CSL artifact

## Next Work

- Add automated tests
- Add GitHub Actions validation
- Expand CSL schema validation
- Add ID registry
- Add markdown generation from YAML
- Add compliance report scaffolds
