# Validation Evidence

Validation Evidence is the structured input supplied to `cos-validate` to indicate whether validation gates passed.

It is separate from the render specification. The render specification defines gates; evidence records what happened for each gate.

## Shape

```yaml
evidence:
  - gate_id: GATE-0001
    status: passed
    message: LF4 specificity passed.
```

Each evidence item must include:

- `gate_id`: the validation gate ID, using `GATE-0000` format.
- `status`: the supplied result status.

Optional fields include:

- `message`: human-readable context.
- `details`: structured machine-readable context.

## CLI validation

`cos-validate` validates evidence files against the registered Validation Evidence schema before running the validation pipeline.

Invalid evidence files return exit code `2` and include the schema path and failing field in stderr.

## Design note

Evidence is still externally supplied. ConstraintOS does not yet inspect images or renderer outputs directly. This schema defines the contract future automated validators will write to.
