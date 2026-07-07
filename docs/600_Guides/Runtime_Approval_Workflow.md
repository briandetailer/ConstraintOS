# Runtime Approval Workflow Guide

## Purpose

This guide explains how to run the Runtime approval workflow from evidence generation through approval report creation.

The workflow is intended for audit, CI/CD, and enterprise integration scenarios where Runtime execution evidence must be reviewed against an approval policy before downstream use.

## Workflow overview

```text
Runtime specification + workers -> Runtime evidence package -> Runtime approval policy -> Runtime approval decision -> Runtime approval report artifact
```

The public implementation boundary is:

```text
RuntimeEvidenceBundleWriter -> verify_runtime_evidence_manifest -> verify_runtime_approval_policy -> create_runtime_approval_decision -> verify_runtime_approval_decision -> RuntimeApprovalReportWriter
```

## Step 1: Generate Runtime evidence

Use the Runtime evidence CLI to produce an evidence package:

```powershell
python -m runtime evidence --spec path/to/runtime-spec.json --workers path/to/workers.json --output-dir artifacts/runtime-evidence --format json
```

This writes the Runtime report, trace report, contract registry report, and evidence manifest.

The evidence manifest path from the CLI summary is used as the approval input.

## Step 2: Choose an approval policy

Reusable example policies are provided in:

```text
examples/runtime/approval-policies/default-runtime-approval-v1.json
examples/runtime/approval-policies/manual-review-runtime-approval-v1.json
```

Use the default policy for basic evidence verification and policy verification.

Use the manual-review policy when a human review check is required before approval can pass.

## Step 3: Generate an approval report

Use the approval CLI to evaluate Runtime evidence against a policy:

```powershell
python -m runtime approval --evidence-manifest artifacts/runtime-evidence/evidence/RUNTIME-0001.json --evidence-artifact-id ARTIFACT-0004 --policy examples/runtime/approval-policies/default-runtime-approval-v1.json --decided-by policy-owner --decided-at 2026-07-06T00:00:00Z --output-dir artifacts/runtime-approval --format json
```

Installed packages may also use:

```powershell
cos-runtime-approval --evidence-manifest artifacts/runtime-evidence/evidence/RUNTIME-0001.json --evidence-artifact-id ARTIFACT-0004 --policy examples/runtime/approval-policies/default-runtime-approval-v1.json --decided-by policy-owner --decided-at 2026-07-06T00:00:00Z --output-dir artifacts/runtime-approval --format json
```

## Exit codes

```text
0 = approval decision approved
1 = approval decision rejected
3 = usage or input error
```

A rejected decision is still written as an approval report artifact when inputs are structurally valid. The report includes failed checks and explanatory notes.

## Output artifacts

Approval reports are written to:

```text
approvals/{runtime_id}.json
```

The approval report contains:

- `runtime_approval`
- `checks`
- `notes`

The artifact wrapper is described by:

```text
schemas/runtime/v1/runtime-approval-report.schema.json
```

## Policy enforcement

Approval decisions are checked against the supplied policy.

Current enforcement includes:

1. Decision policy name must match the policy name.
2. Decision authority must be listed in policy approvers.
3. Decision value must be allowed by the policy.
4. Required policy checks must be present in approval check sources.
5. Check statuses must be allowed by the policy.

If policy enforcement fails, the approval decision is rejected and a policy-enforcement check is added to the decision.

## Recommended CI/CD usage

A minimal CI/CD approval sequence is:

```powershell
python -m runtime evidence --spec path/to/runtime-spec.json --workers path/to/workers.json --output-dir artifacts/runtime-evidence --format json
python -m runtime approval --evidence-manifest artifacts/runtime-evidence/evidence/RUNTIME-0001.json --evidence-artifact-id ARTIFACT-0004 --policy examples/runtime/approval-policies/default-runtime-approval-v1.json --decided-by policy-owner --decided-at 2026-07-06T00:00:00Z --output-dir artifacts/runtime-approval --format json
```

Treat approval CLI exit code `0` as pass, `1` as rejected evidence or policy, and `3` as an input/configuration failure.

## Related files

```text
runtime/approval.py
runtime/approval_gate.py
runtime/approval_cli.py
runtime/artifacts/approval_reporter.py
schemas/runtime/v1/runtime-approval-decision.schema.json
schemas/runtime/v1/runtime-approval-policy.schema.json
schemas/runtime/v1/runtime-approval-report.schema.json
```
