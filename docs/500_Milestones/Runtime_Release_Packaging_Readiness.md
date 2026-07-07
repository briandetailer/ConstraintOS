# Runtime Release / Packaging Readiness

## Purpose

This note opens the Runtime Release / Packaging Readiness track without reopening Runtime Milestone 3 or the closed Runtime approval-gate tracks.

The first slice verifies that Runtime workflows exposed through module execution also have installable package entry points where appropriate.

## Status

Current status:

```text
Slice 1 implemented: Runtime packaged CLI entry points verified and documented
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

## Readiness checklist

```text
[x] Runtime package includes the runtime package tree
[x] Runtime execution console script is registered
[x] Runtime evidence console script is registered
[x] Runtime approval console script is registered
[x] Packaging registration has test coverage
[x] Approval workflow guide documents installed evidence and approval commands
[ ] CLI help/usage consistency audited across Runtime commands
[ ] Release checklist expanded for broader packaging validation
```

## Files updated in Slice 1

```text
pyproject.toml
runtime/tests/test_runtime_approval_cli_packaging.py
docs/600_Guides/Runtime_Approval_Workflow.md
docs/500_Milestones/Runtime_Release_Packaging_Readiness.md
```

## Validation target

Expected test delta from the user-confirmed 473-pass baseline:

```text
+1 test
```

Expected full-suite baseline after validation:

```text
474 passed
```

This note records the expected baseline only. It does not claim local validation was run.
