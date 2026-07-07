# Runtime Release / Packaging Checklist

## Purpose

This checklist defines the release-readiness checks for Runtime packaging without reopening Runtime Milestone 3 or the closed Runtime approval-gate tracks.

Use it before cutting a Runtime-capable package build or release candidate.

## Scope

The checklist covers packaging registration, installed command behavior, source-tree command parity, documentation, and validation evidence.

It does not change Runtime execution semantics, approval policy semantics, or approval-gate closeout status.

## Package metadata checks

```text
[ ] Confirm pyproject.toml package discovery includes runtime*
[ ] Confirm pyproject.toml excludes runtime.tests*
[ ] Confirm runtime dependencies required by CLI workflows are present
[ ] Confirm package version is intentionally set for the release candidate
```

## Console script registration checks

```text
[ ] Confirm cos-runtime is registered
[ ] Confirm cos-runtime-evidence is registered
[ ] Confirm cos-runtime-approval is registered
[ ] Confirm registration coverage exists in runtime/tests/test_runtime_approval_cli_packaging.py
```

## Installed command smoke checks

```text
[ ] cos-runtime --help exits successfully
[ ] cos-runtime-evidence --help exits successfully
[ ] cos-runtime-approval --help exits successfully
[ ] cos-runtime-evidence can generate a Runtime evidence package from sample inputs
[ ] cos-runtime-approval can generate an approval report from generated evidence and a sample policy
```

## Source-tree command parity checks

```text
[ ] python -m runtime --help exits successfully and writes usage to stdout
[ ] python -m runtime evidence matches cos-runtime-evidence usage expectations
[ ] python -m runtime approval matches cos-runtime-approval usage expectations
[ ] Missing Runtime module command arguments remain usage errors
[ ] Unknown Runtime module commands remain usage errors
```

## Artifact checks

```text
[ ] Runtime evidence run writes reports/{runtime_id}.json
[ ] Runtime evidence run writes traces/{runtime_id}.json
[ ] Runtime evidence run writes contracts/runtime-contract-registry.json
[ ] Runtime evidence run writes evidence/{runtime_id}.json
[ ] Runtime approval run writes approvals/{runtime_id}.json
```

## Documentation checks

```text
[ ] Runtime approval workflow guide documents source-tree evidence command
[ ] Runtime approval workflow guide documents installed evidence command
[ ] Runtime approval workflow guide documents source-tree approval command
[ ] Runtime approval workflow guide documents installed approval command
[ ] Runtime release/packaging readiness note records current status and baseline
```

## Validation evidence checks

```text
[ ] Record the user-confirmed full-suite baseline
[ ] Record any expected test delta for the current slice
[ ] Do not claim local tests passed unless local validation was actually run
[ ] Preserve line-cited final summaries for changed files
```

## Current green baseline

The user-confirmed full-suite baseline after pulling the latest Runtime release/packaging readiness changes is:

```text
475 passed
```
