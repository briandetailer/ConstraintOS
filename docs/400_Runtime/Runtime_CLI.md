# Runtime CLI

The runtime CLI runs a ConstraintOS runtime specification through the planner, dependency resolver, scheduler, executor, and artifact collector.

## Command

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --plugin-executor --workers-file examples/runtime/workers.yaml --report
```

## Worker input

Inline worker format:

```text
WORKER-ID:plugin-a,plugin-b
```

Example:

```text
WORKER-0001:generic,echo,dry_run
```

Workers can also be supplied from YAML or JSON using `--workers-file`.

```yaml
workers:
  - worker_id: WORKER-0001
    plugins:
      - echo
      - dry_run
    status: available
```

When no worker input is supplied, the CLI uses `WORKER-0001:generic,echo,dry_run`.

In render-contract mode, when no worker input is supplied, the CLI uses `WORKER-0001:render_contract`.

## Render contract mode

Render contract mode compiles a render specification into a runtime specification before planning or execution:

```powershell
cos-runtime examples/render/lf4_engine_render_specification.yaml --render-contract --plan-only
```

Constraint packs can be applied before the render contract is compiled:

```powershell
cos-runtime examples/render/lf4_engine_render_specification.yaml --render-contract --constraint-pack examples/constraint_packs/lf4_engine_constraint_pack.yaml --plan-only
```

`--constraint-pack` requires `--render-contract` because packs apply to render specifications, not already-compiled runtime specifications.

Applied constraint pack references are preserved in render-contract runtime output under:

- `artifact.constraint_packs`
- `render_contract.constraint_packs`

Text summary output includes `Constraint packs: N` when pack references are present.

## Output formats

The default output format is JSON. Use text format when you only need a quick summary:

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --plan-only --format text --workers-file examples/runtime/workers.yaml
```

## Useful local commands

Preview the plan and schedule without execution:

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --plan-only --workers-file examples/runtime/workers.yaml
```

Run with the dry-run executor:

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --workers-file examples/runtime/workers.yaml
```

Run with the plugin executor and write a report:

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --plugin-executor --workers-file examples/runtime/workers.yaml --report
```

Write the runtime result to a specific file:

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --plugin-executor --workers-file examples/runtime/workers.yaml --output .constraintos/runtime/results/RUNTIME-0001.json
```

Write a human-readable text result:

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --format text --output .constraintos/runtime/results/RUNTIME-0001.txt
```

## Generated files

Local runtime outputs are written under `.constraintos/`, which is ignored by Git.
