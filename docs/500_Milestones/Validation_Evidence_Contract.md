# Milestone: Validation Evidence Contract

Validation Evidence Contract defines how externally supplied evidence is shaped, validated, and aligned to render specification gates.

## Goal

Evidence should be a deterministic input to validation, not an informal note that can be silently ignored, duplicated, or applied to the wrong gate.

## Current guarantees

- Evidence files have a registered JSON Schema at `schemas/validation-evidence.schema.json`.
- Evidence files are discovered by the schema registry using the `evidence` key.
- `constraintos validate` checks evidence files during repository/file validation.
- `cos-validate` checks evidence files before running the validation approval pipeline.
- Each evidence entry must include a `gate_id` and `status`.
- Gate IDs must use `GATE-0000` format.
- Evidence status must use the registered status vocabulary.
- Evidence referencing an unknown gate is rejected.
- Duplicate evidence for the same gate is rejected.

## Runtime boundary

```text
Render Specification Gates
  ↓
Validation Evidence Schema
  ↓
Evidence Status Vocabulary
  ↓
Evidence-to-Gate Alignment
  ↓
Validation Kernel
  ↓
Validation Report
```

## Out of scope

This milestone does not automate image inspection or renderer output analysis. Evidence is still supplied externally, but it now has a durable contract for future automated validators to produce.
