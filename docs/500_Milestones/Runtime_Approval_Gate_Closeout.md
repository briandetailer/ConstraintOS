# Runtime Approval Gate Closeout

## Purpose

This note closes the first post-Milestone 3 Runtime approval-gate track.

Runtime Milestone 3 remains closed. Approval gates are a downstream governance layer over Runtime evidence, policies, approval decisions, and persisted approval reports.

## Final status

Current status:

```text
Runtime approval gates complete
```

Final user-reported full-suite baseline:

```text
460 passed
```

## Completed capabilities

### Approval decision verifier

Implemented in:

```text
runtime/approval.py
```

Public export:

```python
verify_runtime_approval_decision(payload)
```

The decision verifier validates approval payload structure, required fields, allowed decisions, check status values, rejected/waived decision explanation rules, and immutability of supplied payloads.

### Approval decision JSON Schema

Implemented in:

```text
schemas/runtime/v1/runtime-approval-decision.schema.json
```

The schema defines the portable JSON shape for Runtime approval decisions.

### Approval report writer

Implemented in:

```text
runtime/artifacts/approval_reporter.py
```

Public export:

```python
RuntimeApprovalReportWriter
```

The writer verifies approval decisions before persisting them, writes approval JSON to `approvals/{runtime_id}.json`, and registers a `runtime_approval_report` artifact.

### Approval report JSON Schema

Implemented in:

```text
schemas/runtime/v1/runtime-approval-report.schema.json
```

The schema defines the artifact wrapper contract for persisted Runtime approval reports.

### Approval policy verifier

Implemented in:

```text
runtime/approval.py
```

Public export:

```python
verify_runtime_approval_policy(payload)
```

The policy verifier validates policy headers, required evidence artifacts, required checks, allowed decision and check status values, approvers, waiver rules, rejection rules, and immutability of supplied payloads.

### Approval policy JSON Schema

Implemented in:

```text
schemas/runtime/v1/runtime-approval-policy.schema.json
```

The schema defines the portable JSON shape for Runtime approval policies.

### Evidence-linked approval helper

Implemented in:

```text
runtime/approval_gate.py
```

Public export:

```python
create_runtime_approval_decision(evidence_manifest_artifact, policy, decided_by, decided_at)
```

The helper consumes a Runtime evidence manifest artifact and approval policy, verifies both, and creates an approval decision without mutating the evidence artifact wrapper or policy input.

### Contract registry promotion

Implemented in:

```text
runtime/contracts.py
```

The Runtime contract registry now includes public approval contracts for:

```text
runtime_approval_decision
runtime_approval_policy
runtime_approval_report
```

Artifact-writer coverage now includes:

```text
RuntimeApprovalReportWriter -> runtime_approval_report
```

## Public approval boundary

The approval-gate public boundary is:

```text
RuntimeEvidenceBundleWriter
  -> verify_runtime_evidence_manifest
  -> verify_runtime_approval_policy
  -> create_runtime_approval_decision
  -> verify_runtime_approval_decision
  -> RuntimeApprovalReportWriter
  -> runtime_contract_registry
  -> schemas/runtime/v1
```

## Schemas implemented

```text
runtime-approval-decision.schema.json
runtime-approval-policy.schema.json
runtime-approval-report.schema.json
```

## Test files

```text
runtime/tests/test_runtime_approval.py
runtime/tests/test_runtime_approval_gate.py
runtime/tests/test_runtime_approval_contracts.py
runtime/tests/test_contracts.py
runtime/tests/test_contract_registry_report.py
```

## Final validation

User-reported final validation:

```text
460 passed
```

## Disposition

Runtime approval gates are complete for the current post-Milestone 3 scope.

The packaged approval CLI follow-up was later implemented as a separate track and is recorded in:

```text
docs/500_Milestones/Runtime_Approval_CLI_Initial_Implementation.md
```

Remaining optional follow-ups should be handled as separate tracks:

1. Add policy fixtures/examples for common approval modes.
2. Add richer policy enforcement beyond the initial structural checks.
3. Add external documentation for approval workflows.
