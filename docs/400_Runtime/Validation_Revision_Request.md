# Validation Revision Request

The Validation Revision Request converts a remediation plan into a renderer-agnostic request to revise an artifact.

It is the handoff object between validation/approval policy and a future renderer, prompt-revision, or human correction workflow.

## Purpose

```text
Remediation Plan
  ↓
Revision Planner
  ↓
Revision Request
```

The remediation plan says what needs to happen. The revision request packages those actions for the next production attempt.

## Current behavior

The planner currently:

- Accepts a `ValidationRemediationPlan` object or remediation plan dictionary.
- Produces `not_required` when there are no remediation actions.
- Produces `revision_required` when one or more revision steps exist.
- Preserves remediation action ID, gate ID, issue code, severity, instruction, and source reason.
- Does not perform the revision itself.

## Example

```json
{
  "revision_request": {
    "id": "REVISION-REQUEST-0001",
    "artifact_id": "ARTIFACT-0001",
    "remediation_plan_id": "REMEDIATION-PLAN-0001",
    "status": "revision_required",
    "step_count": 1
  },
  "steps": [
    {
      "id": "REVISION-STEP-0001",
      "remediation_action_id": "REMEDIATION-0001",
      "gate_id": "GATE-0001",
      "issue_code": "VAL-0001",
      "severity": "blocker",
      "instruction": "Supply evidence for the required validation gate.",
      "source_reason": "No evidence was supplied for this gate."
    }
  ]
}
```

## Design note

This does not regenerate images, edit prompts, or change files. It defines the deterministic request shape that future revision loops will consume.
