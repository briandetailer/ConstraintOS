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

## Plan-only smoke check

From the repository root:

```bash
cos-runtime examples/graphics/perseverance/spec.json \
  --workers-file examples/graphics/perseverance/workers.json \
  --plan-only \
  --format text
```

Expected summary shape:

```text
Plan PLAN-0001: planned | nodes=6 | stages=6 | plugins=approval_reviewer,constraint_builder,evidence_manifest_generator,image_evaluator,image_prompt_generator,reference_collector
Schedule SCHEDULE-0001: scheduled | assignments=6 | unscheduled=0
```

## Dry-run runtime smoke check

From the repository root:

```bash
cos-runtime examples/graphics/perseverance/spec.json \
  --workers-file examples/graphics/perseverance/workers.json \
  --runtime-id GRAPHICS-PERSEVERANCE-RUNTIME-0001 \
  --format text
```

Expected summary shape:

```text
Runtime GRAPHICS-PERSEVERANCE-RUNTIME-0001: completed (success=True)
Plan PLAN-0001: planned | nodes=6 | stages=6 | plugins=approval_reviewer,constraint_builder,evidence_manifest_generator,image_evaluator,image_prompt_generator,reference_collector
Schedule SCHEDULE-0001: scheduled | assignments=6 | unscheduled=0
Execution GRAPHICS-PERSEVERANCE-RUNTIME-0001-EXEC-RESULT-0001: complete | nodes=6
Artifacts: 6
```

## Fixture tests

```bash
pytest runtime/tests/test_graphics_perseverance_example.py
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
