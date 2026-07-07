# Runtime Approval CLI Initial Implementation

## Purpose

This note records the first packaged CLI follow-up after Runtime approval gates were closed.

The approval-gate core remains complete. This track exposes the approval workflow through direct module execution, an installable console script, and reusable policy examples.

## Status

Current status:

```text
initial Runtime approval CLI and policy examples implemented
```

Implemented module:

```text
runtime/approval_cli.py
```

Module dispatcher:

```text
python -m runtime approval --evidence-manifest MANIFEST --evidence-artifact-id ID --policy POLICY --decided-by NAME --decided-at TIMESTAMP --output-dir OUTPUT_DIR [--format json|text]
```

Console script:

```text
cos-runtime-approval
```

## CLI behavior

The approval CLI currently:

1. Reads a Runtime evidence manifest JSON file.
2. Accepts the evidence manifest artifact id explicitly.
3. Reads a Runtime approval policy JSON file.
4. Creates an approval decision with `create_runtime_approval_decision`.
5. Persists the decision through `RuntimeApprovalReportWriter`.
6. Emits JSON or text summary output.
7. Returns success when the decision is `approved`.
8. Returns rejected when the decision is not `approved`.
9. Returns usage error for malformed inputs.

## Exit codes

```text
0 = approval CLI success
1 = approval decision rejected
3 = usage/input error
```

## Package entry point

Implemented in:

```text
pyproject.toml
```

Registered script:

```text
cos-runtime-approval = "runtime.approval_cli:main"
```

## Example policies

Implemented in:

```text
examples/runtime/approval-policies/default-runtime-approval-v1.json
examples/runtime/approval-policies/manual-review-runtime-approval-v1.json
```

The example policies are verified by both the Python policy verifier and the Runtime approval policy JSON Schema.

## Test files

```text
runtime/tests/test_runtime_approval_cli.py
runtime/tests/test_runtime_module_approval_cli.py
runtime/tests/test_runtime_approval_cli_packaging.py
runtime/tests/test_runtime_approval_policy_examples.py
```

## Validation target

Expected test delta from the previous 465-pass baseline:

```text
+3 tests
```

Expected full-suite baseline after validation:

```text
468 passed
```
