# Runtime CLI

The runtime CLI runs a ConstraintOS runtime specification through the planner, dependency resolver, scheduler, executor, and artifact collector.

## Command

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --plugin-executor --worker WORKER-0001:echo --report
```

## What it does

1. Loads a YAML or JSON runtime specification.
2. Builds an execution plan from `execution_steps`.
3. Validates dependency references and cycle safety.
4. Schedules nodes against worker plugin capabilities.
5. Executes scheduled assignments using either the default dry-run executor or the built-in plugin executor.
6. Collects produced output URIs into the runtime artifact store.
7. Optionally writes a JSON runtime report under `.constraintos/runtime/artifacts/reports/`.

## Worker format

Workers use this format:

```text
WORKER-ID:plugin-a,plugin-b
```

Example:

```text
WORKER-0001:generic,echo,dry_run
```

## Useful local commands

Run with the dry-run executor:

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --worker WORKER-0001:echo
```

Run with the plugin executor and write a report:

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --plugin-executor --worker WORKER-0001:echo --report
```

Write the runtime result to a specific file:

```powershell
cos-runtime examples/runtime/echo_pipeline.yaml --plugin-executor --worker WORKER-0001:echo --output .constraintos/runtime/results/RUNTIME-0001.json
```

## Generated files

Local runtime outputs are written under `.constraintos/`, which is ignored by Git.
