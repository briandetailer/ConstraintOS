# Runtime Evidence CLI Target

## Purpose

This document records the Runtime Milestone 3 CLI packaging target for evidence bundle generation.

A repository search during Milestone 3 packaging did not locate an existing runtime CLI entry point for evidence bundle generation using the expected CLI, runtime report, or evidence bundle terms. This document defines the target contract so implementation can be added deliberately instead of inventing behavior ad hoc.

## Status

Current status:

```text
Python module command implemented / packaged console command wiring pending
```

The Runtime evidence package exists through Python APIs and can now be generated through `python -m runtime evidence` or `python -m runtime.cli`.

The next packaging step is to decide whether to wire this module into a public console command such as `constraintos runtime evidence` or `constraintos evidence`.

## Implemented module command

Current preferred module invocation target:

```powershell
python -m runtime evidence \
  --spec path/to/runtime-spec.json \
  --workers path/to/workers.json \
  --output-dir artifacts/runtime-evidence \
  --format json
```

Direct module entry point:

```powershell
python -m runtime.cli \
  --spec path/to/runtime-spec.json \
  --workers path/to/workers.json \
  --output-dir artifacts/runtime-evidence \
  --format json
```

Implemented behavior:

- reads a runtime specification JSON file
- reads a worker capability JSON file
- runs `RuntimeEngine`
- writes runtime report JSON
- writes runtime trace report JSON
- writes runtime contract registry JSON
- writes runtime evidence manifest JSON
- verifies the written evidence manifest before returning success
- prints a JSON or text summary

## Future console command shape

```powershell
constraintos runtime evidence \
  --spec path/to/runtime-spec.json \
  --workers path/to/workers.json \
  --output-dir artifacts/runtime-evidence \
  --format json
```

Alternative shorter command:

```powershell
constraintos evidence \
  --spec path/to/runtime-spec.json \
  --workers path/to/workers.json \
  --output-dir artifacts/runtime-evidence
```

## Required inputs

| Option | Required | Purpose |
| --- | --- | --- |
| `--spec` | yes | Runtime specification JSON file. |
| `--workers` | yes | Worker capability JSON file. |
| `--output-dir` | yes | Directory where evidence artifacts should be written. |
| `--format` | no | Output summary format, initially `json` or `text`. |

## Required outputs

The command writes:

- runtime report JSON
- runtime trace report JSON
- runtime contract registry JSON
- runtime evidence manifest JSON

The command prints a machine-readable summary when `--format json` is used.

Example summary:

```json
{
  "runtime_evidence_cli": {
    "successful": true,
    "runtime_id": "RUNTIME-0001",
    "runtime_status": "completed",
    "evidence_manifest_uri": "file:///.../evidence/RUNTIME-0001.json",
    "evidence_manifest_path": "/.../evidence/RUNTIME-0001.json",
    "contract_registry_version": "runtime-contracts/v1",
    "issue_count": 0
  },
  "issues": []
}
```

## Exit codes

| Exit code | Meaning |
| --- | --- |
| `0` | Evidence package was generated and manifest verification passed. |
| `1` | Runtime completed but evidence manifest verification failed. |
| `2` | Runtime execution failed or produced an unacceptable terminal status. |
| `3` | CLI usage, input parsing, or file-loading error. |

## Required verification before success

The CLI calls the Runtime evidence manifest verifier before returning success.

A successful CLI run requires:

- evidence manifest is readable
- manifest runtime id is present
- artifact count matches artifact list length
- artifact roles are ordered as runtime report, trace report, contract registry
- artifact ids match the manifest header ids
- contract registry version matches the active runtime contract version
- every package artifact has a URI

## External-consumer contract

The CLI does not expose Python object internals. Its public contract is:

- input files
- output evidence package JSON artifacts
- command exit code
- stdout summary
- stderr usage or failure details

## Implemented test coverage

Initial tests verify:

1. CLI generates all four expected artifacts.
2. CLI summary points to the evidence manifest.
3. CLI exits `0` when manifest verification passes and runtime execution succeeds.
4. CLI exits `2` when runtime execution is not successful.
5. CLI exits `3` for malformed worker input.
6. CLI preserves deterministic artifact roles, manifest location, and contract registry version.
7. `python -m runtime evidence` dispatches to the evidence command.
8. Unknown module commands return usage errors.

## Remaining packaging target

Future packaging should add a public console command wrapper if the project adopts packaged CLI entry points.

The module-level CLI is sufficient for Milestone 3 Runtime development because it proves the public evidence package can be generated from input files without direct Python object usage by callers.
