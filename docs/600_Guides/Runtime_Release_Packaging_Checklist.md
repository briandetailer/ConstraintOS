# Runtime Release / Packaging Checklist

## Purpose

This checklist defines release-readiness checks for Runtime packaging without reopening Runtime Milestone 3 or the closed Runtime approval-gate tracks.

Use it before preparing a Runtime-capable package build or release candidate.

## Scope

The checklist covers packaging registration, installed command behavior, source-tree command parity, documentation, and validation evidence.

It does not change Runtime execution semantics, approval policy semantics, or approval-gate closeout status.

## Package metadata checks

```text
[x] Confirm pyproject.toml package discovery includes runtime*
[x] Confirm pyproject.toml excludes runtime.tests*
[x] Confirm runtime dependencies required by CLI workflows are present
[x] Confirm package version is intentionally set for the current alpha release track
```

## Console script registration checks

```text
[x] Confirm cos-runtime is registered
[x] Confirm cos-runtime-evidence is registered
[x] Confirm cos-runtime-approval is registered
[x] Confirm registration coverage exists in runtime/tests/test_runtime_approval_cli_packaging.py
```

## Installed command checks

```text
[x] cos-runtime --help exits successfully
[x] cos-runtime-evidence --help exits successfully
[x] cos-runtime-approval --help exits successfully
[x] cos-runtime-evidence can generate a Runtime evidence package from sample inputs
[x] cos-runtime-approval can generate an approval report from generated evidence and a sample policy
```

## Source-tree command parity checks

```text
[x] python -m runtime --help exits successfully and writes usage to stdout
[x] python -m runtime evidence matches cos-runtime-evidence usage expectations
[x] python -m runtime approval matches cos-runtime-approval usage expectations
[x] Missing Runtime module command arguments remain usage errors
[x] Unknown Runtime module commands remain usage errors
```

## Artifact checks

```text
[x] Runtime evidence run writes reports/{runtime_id}.json
[x] Runtime evidence run writes traces/{runtime_id}.json
[x] Runtime evidence run writes contracts/runtime-contract-registry.json
[x] Runtime evidence run writes evidence/{runtime_id}.json
[x] Runtime approval run writes approvals/{runtime_id}.json
```

## Documentation checks

```text
[x] Runtime approval workflow guide documents source-tree evidence command
[x] Runtime approval workflow guide documents installed evidence command
[x] Runtime approval workflow guide documents source-tree approval command
[x] Runtime approval workflow guide documents installed approval command
[x] Runtime release/packaging readiness note records current status and baseline
```

## Validation evidence checks

```text
[ ] Record the user-confirmed full-suite baseline
[ ] Record any expected test delta for the current slice
[ ] Do not claim local tests passed unless local validation was actually run
[ ] Preserve line-cited final summaries for changed files
```

## Executable coverage added

Current release/packaging readiness coverage includes:

```text
[x] Runtime module help exits successfully and advertises evidence and approval subcommands
[x] Runtime evidence CLI help exits successfully and advertises required inputs
[x] Runtime approval CLI help exits successfully and advertises required inputs
[x] Runtime package discovery includes runtime* and excludes runtime.tests*
[x] Runtime CLI package dependencies are registered
[x] Package version is explicitly declared on the current alpha release track
[x] Runtime console script registrations are covered
[x] Runtime installed command help exits successfully
[x] Runtime installed evidence and approval workflows generate expected artifacts
[x] Runtime source-tree module command parity is covered
[x] Runtime evidence and approval artifact writes are covered
[x] Runtime documentation checklist is covered
```

## Current green baseline

The user-confirmed full-suite baseline after validating Slice 12 is:

```text
487 passed
```

Slice 13 is documentation-only and adds no tests:

```text
+0 tests
```

Expected full-suite baseline after validation:

```text
487 passed
```
