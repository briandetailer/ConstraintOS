# Runtime Release / Packaging Readiness

## Purpose

This note opens the Runtime Release / Packaging Readiness track without reopening Runtime Milestone 3 or the closed Runtime approval-gate tracks.

The first slices verify that Runtime workflows exposed through module execution also have installable package entry points where appropriate, normalize top-level Runtime help behavior for package/source usage, add a broader release packaging checklist, add executable help coverage for dedicated Runtime evidence and approval CLIs, add executable package discovery metadata coverage, and add executable Runtime CLI dependency coverage.

## Status

Current status:

```text
Slice 1 implemented: Runtime packaged CLI entry points verified and documented
Slice 2 implemented: Runtime module help exits successfully and writes usage to stdout
Slice 3 implemented: Runtime release packaging checklist added
Slice 4 implemented: Runtime evidence and approval CLI help coverage added
Slice 5 implemented: Runtime package discovery metadata coverage added
Slice 6 implemented: Runtime CLI dependency coverage added
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

Top-level Runtime module help behaves as a successful help request:

```text
python -m runtime --help
```

Expected behavior:

```text
exit code 0
usage text on stdout
no stderr output
```

Dedicated Runtime evidence and approval CLI help behavior is covered by tests:

```text
run_evidence_cli(["--help"])
run_approval_cli(["--help"])
```

Both help requests are expected to return success and advertise their required inputs.

Missing commands and unknown commands remain usage errors.

## Package discovery metadata

Runtime package discovery is covered by tests in:

```text
runtime/tests/test_runtime_approval_cli_packaging.py
```

The coverage verifies that package discovery includes Runtime packages and excludes Runtime tests from packaged distributions.

## Runtime CLI dependency metadata

Runtime CLI dependency declarations are covered by tests in:

```text
runtime/tests/test_runtime_approval_cli_packaging.py
```

The coverage verifies that the package metadata keeps the dependency declarations needed by current Runtime CLI workflows.

## Release checklist

Broader packaging validation is tracked in:

```text
docs/600_Guides/Runtime_Release_Packaging_Checklist.md
```

The checklist covers package metadata, console script registration, installed command smoke checks, source-tree command parity, Runtime artifacts, documentation, and validation evidence.

## Readiness checklist

```text
[x] Runtime package includes the runtime package tree
[x] Runtime execution console script is registered
[x] Runtime evidence console script is registered
[x] Runtime approval console script is registered
[x] Packaging registration has test coverage
[x] Approval workflow guide documents installed evidence and approval commands
[x] CLI help/usage consistency audited across Runtime commands
[x] Release checklist expanded for broader packaging validation
[x] Runtime evidence CLI help has executable coverage
[x] Runtime approval CLI help has executable coverage
[x] Runtime package discovery metadata has executable coverage
[x] Runtime CLI dependency metadata has executable coverage
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

## Files updated in Slice 3

```text
docs/600_Guides/Runtime_Release_Packaging_Checklist.md
docs/500_Milestones/Runtime_Release_Packaging_Readiness.md
```

## Files updated in Slice 4

```text
runtime/tests/test_runtime_evidence_cli.py
runtime/tests/test_runtime_approval_cli.py
docs/600_Guides/Runtime_Release_Packaging_Checklist.md
docs/500_Milestones/Runtime_Release_Packaging_Readiness.md
```

## Files updated in Slice 5

```text
runtime/tests/test_runtime_approval_cli_packaging.py
docs/600_Guides/Runtime_Release_Packaging_Checklist.md
docs/500_Milestones/Runtime_Release_Packaging_Readiness.md
```

## Files updated in Slice 6

```text
runtime/tests/test_runtime_approval_cli_packaging.py
docs/600_Guides/Runtime_Release_Packaging_Checklist.md
docs/500_Milestones/Runtime_Release_Packaging_Readiness.md
```

## Validation target

User-confirmed full-suite baseline after validating Slice 5:

```text
478 passed
```

Expected test delta from Slice 6:

```text
+1 test
```

Expected full-suite baseline after validation:

```text
479 passed
```

This note records the user-confirmed baseline and the Slice 6 expected baseline. It does not claim local validation was run.
