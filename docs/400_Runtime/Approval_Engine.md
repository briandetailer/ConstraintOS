# Approval Engine

The Approval Engine converts validation reports into deterministic approval decisions.

It does not inspect images, renderer outputs, or source files directly. It only applies approval policy to structured validation results.

## Purpose

```text
Validation Report
  ↓
Approval Engine
  ↓
Approval Decision
```

This separation keeps validation and approval independent:

- Validators determine whether gates passed.
- The Approval Engine determines what decision follows from those results.

## Current policy

The first policy is intentionally simple:

| Validation result shape | Approval status |
| --- | --- |
| All gates passed | `approved` |
| One or more required gates failed or lacked evidence | `rejected` |
| Only optional gates failed | `approved_with_warnings` |

## Constraint pack traceability

When a validation report includes applied constraint pack references, the approval decision records them under `approval.constraint_packs`.

This keeps final approval or rejection tied to the reusable standards that were active during validation.

## Example rejected decision

```json
{
  "approval": {
    "id": "APPROVAL-0001",
    "status": "rejected",
    "constraint_packs": [
      {
        "id": "CPACK-0001",
        "version": "0.1",
        "title": "LF4 Engineering Atlas Constraint Pack"
      }
    ]
  },
  "artifact": {
    "id": "ARTIFACT-0001",
    "validation_report_id": "VALIDATION-REPORT-0001"
  },
  "decision": {
    "summary": "Rejected because required validation gates did not pass.",
    "reasons": [
      "VAL-0001: No evidence was supplied for this gate."
    ]
  }
}
```

## Design note

Approval is a policy layer, not an inspection layer. This lets the validation system grow more sophisticated without changing approval rules every time a new validator is added. Constraint pack traceability remains visible through the final decision.
