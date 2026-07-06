# Validation Approval Pipeline

The Validation Approval Pipeline runs validation, builds a focused failure report, builds a remediation plan, builds a revision request, and then applies approval policy.

It is the first combined workflow for the post-render side of ConstraintOS.

```text
Render Specification
  ↓
Validation Evidence
  ↓
Validation Kernel
  ↓
Validation Report
  ↓
Failure Report
  ↓
Remediation Plan
  ↓
Revision Request
  ↓
Approval Engine
  ↓
Approval Decision
```

## Purpose

The pipeline exists so callers do not need to manually wire the Validation Kernel, Failure Reporter, Remediation Planner, Revision Planner, and Approval Engine together.

It keeps the concerns separated while still providing one deterministic operation:

```text
Evaluate this artifact candidate against this render specification, describe any needed remediation, package any needed revision request, and decide whether it is approved.
```

## Current behavior

The pipeline currently supports render specifications directly:

- Reads `validation.gates` from the render specification.
- Evaluates supplied evidence against those gates.
- Produces a validation report.
- Produces a focused failure report from any non-passing validation results.
- Produces a remediation plan from the failure report.
- Produces a revision request from the remediation plan.
- Applies approval policy.
- Preserves applied constraint pack references through every output layer.
- Returns a root-level `constraint_packs` audit header.
- Returns all outputs together.

## Constraint pack traceability

When a render specification contains `constraint_packs`, the pipeline keeps those references in the root result and every generated object:

- `constraint_packs`
- `validation.validation_report.constraint_packs`
- `failure_report.failure_report.constraint_packs`
- `remediation_plan.remediation_plan.constraint_packs`
- `revision_request.revision_request.constraint_packs`
- `approval.approval.constraint_packs`

This makes the full approval/rejection result auditable against the standards that were applied before validation.

## Result shape

```json
{
  "constraint_packs": [
    {
      "id": "CPACK-0001",
      "version": "0.1",
      "title": "LF4 Engineering Atlas Constraint Pack"
    }
  ],
  "validation": {
    "validation_report": {
      "id": "VALIDATION-REPORT-0001",
      "subject_id": "LF4-ENGINE",
      "status": "failed",
      "constraint_packs": [
        {
          "id": "CPACK-0001",
          "version": "0.1",
          "title": "LF4 Engineering Atlas Constraint Pack"
        }
      ]
    },
    "results": []
  },
  "failure_report": {
    "failure_report": {
      "id": "FAILURE-REPORT-0001",
      "status": "failed",
      "failure_count": 1,
      "constraint_packs": [
        {
          "id": "CPACK-0001",
          "version": "0.1",
          "title": "LF4 Engineering Atlas Constraint Pack"
        }
      ]
    },
    "failures": []
  },
  "remediation_plan": {
    "remediation_plan": {
      "id": "REMEDIATION-PLAN-0001",
      "status": "required",
      "action_count": 1,
      "constraint_packs": [
        {
          "id": "CPACK-0001",
          "version": "0.1",
          "title": "LF4 Engineering Atlas Constraint Pack"
        }
      ]
    },
    "actions": []
  },
  "revision_request": {
    "revision_request": {
      "id": "REVISION-REQUEST-0001",
      "status": "revision_required",
      "step_count": 1,
      "constraint_packs": [
        {
          "id": "CPACK-0001",
          "version": "0.1",
          "title": "LF4 Engineering Atlas Constraint Pack"
        }
      ]
    },
    "steps": []
  },
  "approval": {
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
    "decision": {
      "summary": "Rejected because required validation gates did not pass.",
      "reasons": []
    }
  }
}
```
