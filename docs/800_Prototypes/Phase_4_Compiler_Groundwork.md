# Phase 4: Compiler Groundwork and Renderer Adapter Boundaries

Status: Complete Baseline
Version: 0.4

## Purpose
Phase 4 introduces the first compiler layer for ConstraintOS. The compiler transforms CSL-style YAML specifications into deterministic renderer instruction packages without calling any live renderer.

## Implemented Scope

- Compiler framework module
- Generic text compiler
- Unsupported constraint reporting
- CLI `compile` command
- Example compiled instruction
- Compiler tests
- Package version bumped to 0.4.0

## Compiler Philosophy

The compiler is not a prompt-writing convenience. It is a controlled transformation layer from structured specification to renderer-specific instruction package.

## Design Rules

1. The compiler must not silently discard constraints.
2. Unsupported constraint types must be reported.
3. Renderer-specific behavior must be isolated behind compiler targets.
4. Live renderer calls remain out of scope.
5. Generated instructions must preserve blocker constraints clearly.
6. Ambiguity must be surfaced instead of hidden.

## Current Compiler Target

### `generic`
A renderer-agnostic text instruction target used for testing the transformation pipeline.

## CLI Usage

```bash
constraintos compile examples/csl/LF4_TEST_001.yaml --renderer generic --output examples/compiled/LF4_TEST_001_instruction.txt
```

JSON output is also available:

```bash
constraintos compile examples/csl/LF4_TEST_001.yaml --format json
```

## Recommended Phase 5

Phase 5 should define renderer adapter interfaces and compile result contracts more formally:

1. Renderer profile schema
2. Compiler result schema
3. Adapter interface protocol
4. Multiple compiler targets
5. Unsupported constraint test fixtures
6. Patch instruction package format
