# Validation Remediation Plan

The Validation Remediation Plan converts a validation failure report into deterministic next actions.

It is the first step toward an approval and revision loop.

## Purpose

```text
Failure Report
  ↓
Remediation Planner
  ↓
Remediation Plan
```

The failure report explains what did not pass. The remediation plan converts those failures into actions that can be assigned to a human reviewer, renderer adapter, prompt revision step, or future automated repair workflow.

## Current behavior

The planner currently:

- Accepts a `ValidationFailureReport` object or failure report dictionary.
- Creates one remediation action per failure.
- Preserves gate ID, gate name, issue code, severity, source reason, and remediation instruction.
- Preserves applied constraint pack references from the failure report.
- Produces `not_required` when there are no failures.
- Produces `required` when at least one remediation action exists.

## Example

```json
{
  "remediation_plan": {
    "id": "REMEDIATION-PLAN-0001",
    "failure_report_id": "FAILURE-REPORT-0001",
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
  "actions": [
    {
      "id": "REMEDIATION-0001",
      "gate_id": "GATE-0001",
      "gate_name": "LF4 Specificity Gate",
      "issue_code": "VAL-0001",
      "severity": "blocker",
      "instruction": "Supply evidence for the required validation gate.",
      "source_reason": "No evidence was supplied for this gate."
    }
  ]
}
```

## Design note

This still does not modify artifacts or regenerate outputs. It defines the handoff object that future revision loops will consume while preserving the standards context that produced the remediation work.
