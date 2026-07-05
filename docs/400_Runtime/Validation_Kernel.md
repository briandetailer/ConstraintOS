# Validation Kernel

The Validation Kernel evaluates whether a produced artifact has evidence for every required validation gate.

This is intentionally separate from rendering. Renderers produce candidate outputs; validators decide whether those outputs satisfy the contract.

## Purpose

The kernel converts validation gates and evidence into a structured validation report.

```text
Render Specification
  ↓
Validation Gates
  ↓
Evidence
  ↓
Validation Kernel
  ↓
Validation Report
```

## Current behavior

The first implementation supports deterministic gate evaluation:

- A required gate passes only when supplied evidence has a passing status.
- A required gate fails when evidence is missing or failing.
- An optional gate can fail without failing the whole report.
- Render specifications can be evaluated directly by reading their `validation.gates` section.

## Passing evidence statuses

The kernel currently treats these evidence statuses as passing:

```text
pass
passed
complete
approved
```

## Example result

```json
{
  "validation_report": {
    "id": "VALIDATION-REPORT-0001",
    "subject_id": "LF4-ENGINE",
    "status": "passed"
  },
  "results": [
    {
      "gate_id": "GATE-0001",
      "name": "LF4 Specificity Gate",
      "status": "passed",
      "required_pass": true,
      "reason": "LF4 specificity passed."
    }
  ]
}
```

## Design note

This does not yet inspect images or generated files. It defines the reporting structure and pass/fail semantics that future validators will use.
