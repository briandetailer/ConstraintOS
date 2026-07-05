# Validation Approval Pipeline

The Validation Approval Pipeline runs validation, builds a focused failure report, builds a remediation plan, and then applies approval policy.

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
Approval Engine
  ↓
Approval Decision
```

## Purpose

The pipeline exists so callers do not need to manually wire the Validation Kernel, Failure Reporter, Remediation Planner, and Approval Engine together.

It keeps the concerns separated while still providing one deterministic operation:

```text
Evaluate this artifact candidate against this render specification, describe any needed remediation, and decide whether it is approved.
```

## Current behavior

The pipeline currently supports render specifications directly:

- Reads `validation.gates` from the render specification.
- Evaluates supplied evidence against those gates.
- Produces a validation report.
- Produces a focused failure report from any non-passing validation results.
- Produces a remediation plan from the failure report.
- Applies approval policy.
- Returns all outputs together.

## Result shape

```json
{
  "validation": {
    "validation_report": {
      "id": "VALIDATION-REPORT-0001",
      "subject_id": "LF4-ENGINE",
      "status": "failed"
    },
    "results": []
  },
  "failure_report": {
    "failure_report": {
      "id": "FAILURE-REPORT-0001",
      "status": "failed",
      "failure_count": 1
    },
    "failures": []
  },
  "remediation_plan": {
    "remediation_plan": {
      "id": "REMEDIATION-PLAN-0001",
      "status": "required",
      "action_count": 1
    },
    "actions": []
  },
  "approval": {
    "approval": {
      "id": "APPROVAL-0001",
      "status": "rejected"
    },
    "decision": {
      "summary": "Rejected because required validation gates did not pass.",
      "reasons": []
    }
  }
}
```

## Design note

This pipeline still does not perform image inspection or artifact revision. It is the orchestration layer that future validators and revision loops will use once visual, geometry, reference-image, or renderer-specific evidence is available.
