# NASA Perseverance Graphics Validation Example

This example is the first product-facing graphics validation fixture for ConstraintOS.

It does not generate an image yet. It runs the documented NASA Perseverance rover technical-graphic use case through the current Runtime Planner, Scheduler, and DryRun execution layer.

## Files

```text
spec.json
workers.json
policy.json
expected_prompt.json
expected_evidence.json
expected_approval.json
```

## Graphics-validation wrapper smoke check

From the repository root:

```bash
cos-graphics-validate perseverance --plan-only --format text
```

Expected summary shape:

```text
Plan PLAN-0001: planned | nodes=6 | stages=6 | plugins=approval_reviewer,constraint_builder,evidence_manifest_generator,image_evaluator,image_prompt_generator,reference_collector
Schedule SCHEDULE-0001: scheduled | assignments=6 | unscheduled=0
Graphics validation perseverance: subject=NASA Perseverance rover | expected_decision=needs_review | mode=fixture_only_no_image_generation
```

## Graphics-validation dry-run smoke check

From the repository root:

```bash
cos-graphics-validate perseverance --format text
```

Expected summary shape:

```text
Runtime GRAPHICS-PERSEVERANCE-RUNTIME-0001: completed (success=True)
Plan PLAN-0001: planned | nodes=6 | stages=6 | plugins=approval_reviewer,constraint_builder,evidence_manifest_generator,image_evaluator,image_prompt_generator,reference_collector
Schedule SCHEDULE-0001: scheduled | assignments=6 | unscheduled=0
Execution GRAPHICS-PERSEVERANCE-RUNTIME-0001-EXEC-RESULT-0001: complete | nodes=6
Artifacts: 6
Graphics validation perseverance: subject=NASA Perseverance rover | expected_decision=needs_review | mode=fixture_only_no_image_generation
```

## Generic runtime smoke check

The underlying runtime path remains available:

```bash
cos-runtime examples/graphics/perseverance/spec.json \
  --workers-file examples/graphics/perseverance/workers.json \
  --runtime-id GRAPHICS-PERSEVERANCE-RUNTIME-0001 \
  --format text
```

## Fixture tests

```bash
pytest runtime/tests/test_graphics_perseverance_example.py
pytest tests/test_graphics_validation_cli.py
```

Do not record these tests as passed until they have actually been run.

## Product intent

The expected output fixtures define the intended graphics validation behavior:

```text
- generate a constrained prompt
- evaluate the candidate against subject, geometry, instrument, label, style, and forbidden-substitution rules
- produce evidence
- mark uncertainty as needs_review rather than approval
```

The first real graphics adapter should preserve this behavior rather than bypass it.
