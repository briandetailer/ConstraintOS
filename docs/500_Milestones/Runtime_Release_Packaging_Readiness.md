# Runtime Release / Packaging Readiness

## Purpose

This note opens the Runtime Release / Packaging Readiness track without reopening Runtime Milestone 3 or the closed Runtime approval-gate tracks.

The first slices verify that Runtime workflows exposed through module execution also have installable package entry points where appropriate, then normalize top-level Runtime help behavior for package/source usage.

## Status

Current status:

```text
Slice 1 implemented: Runtime packaged CLI entry points verified and documented
Slice 2 implemented: Runtime module help exits successfully and writes usage to stdout
```

Closed tracks remain closed:

```text
Runtime Milestone 3
Post-Milestone 3 Approval Gates
Approval CLI follow-up
Approval policy examples
Approval policy enforcement
Approval workflow guide
```

## Packaged Runtime commands

Registered Runtime-facing console scripts:

```text
cos-runtime = constraintos.runtime_cli:main
cos-runtime-evidence = runtime.cli:main
cos-runtime-approval = runtime.approval_cli:main
```

The dedicated evidence script mirrors the source-tree module command:

```text
python -m runtime evidence --spec SPEC --workers WORKERS --output-dir OUTPUT_DIR [--format json|text]
```

The approval script mirrors the source-tree module command:

```text
python -m runtime approval --evidence-manifest MANIFEST --evidence-artifact-id ID --policy POLICY --decided-by NAME --decided-at TIMESTAMP --output-dir OUTPUT_DIR [--format json|text]
```

## CLI help behavior

Top-level Runtime module help now behaves as a successful help request:

```text
python -m runtime --help
```

Expected behavior:

```text
exit code 0
usage text on stdout
no stderr output
```

Missing commands and unknown commands remain usage errors.

## Readiness checklist

```text
[x] Runtime package includes the runtime package tree
[x] Runtime execution console script is registered
[x] Runtime evidence console script is registered
[x] Runtime approval console script is registered
[x] Packaging registration has test coverage
[x] Approval workflow guide documents installed evidence and approval commands
[x] CLI help/usage consistency audited across Runtime commands
[ ] Release checklist expanded for broader packaging validation
```

## Files updated in Slice 1

```text
pyproject.toml
runtime/tests/test_runtime_approval_cli_packaging.py
docs/600_Guides/Runtime_Approval_Workflow.md
docs/500_Milestones/Runtime_Release_Packaging_Readiness.md
```

## Files updated in Slice 2

```text
runtime/__main__.py
runtime/tests/test_runtime_module_cli.py
docs/500_Milestones/Runtime_Release_Packaging_Readiness.md
```

## Validation target

User-confirmed full-suite baseline after Slice 1:

```text
473 passed
```

Expected test delta from Slice 2:

```text
+1 test
```

Expected full-suite baseline after validation:

```text
474 passed
```

This note records the expected baseline only. It does not claim local validation was run.
