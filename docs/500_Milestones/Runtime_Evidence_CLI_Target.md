# Runtime Evidence CLI Target

## Purpose

This document records the Runtime Milestone 3 CLI packaging target for evidence bundle generation.

A repository search during Milestone 3 packaging did not locate an existing runtime CLI entry point for evidence bundle generation using the expected CLI, runtime report, or evidence bundle terms. This document defines the target contract so a future implementation can be added deliberately instead of inventing behavior ad hoc.

## Status

Current status:

```text
not implemented / not located
```

The Runtime evidence package exists through Python APIs, but the CLI handoff for external consumers still needs to be implemented or explicitly located.

## CLI goal

The CLI should let a user generate the public Runtime evidence package from an input runtime specification and write the package to a deterministic output directory.

The CLI should produce the same public evidence boundary as direct Python API usage:

```text
RuntimeResult
  -> RuntimeReportWriter
  -> RuntimeTraceReportWriter
  -> RuntimeContractRegistryReportWriter
  -> RuntimeEvidenceBundleWriter
  -> verify_runtime_evidence_manifest
```

## Proposed command shape

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

The command should write:

- runtime report JSON
- runtime trace report JSON
- runtime contract registry JSON
- runtime evidence manifest JSON

The command should print a machine-readable summary when `--format json` is used.

Example summary:

```json
{
  "runtime_evidence_cli": {
    "successful": true,
    "runtime_id": "RUNTIME-0001",
    "evidence_manifest_uri": "file:///.../evidence/RUNTIME-0001.json",
    "contract_registry_version": "runtime-contracts/v1"
  }
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

The CLI should call the Runtime evidence manifest verifier before returning success.

A successful CLI run requires:

- evidence manifest is readable
- manifest runtime id is present
- artifact count matches artifact list length
- artifact roles are ordered as runtime report, trace report, contract registry
- artifact ids match the manifest header ids
- contract registry version matches the active runtime contract version
- every package artifact has a URI

## External-consumer contract

The CLI should not expose Python object internals. Its public contract should be:

- input files
- output evidence package JSON artifacts
- command exit code
- stdout summary
- stderr usage or failure details

## Testing target

Future implementation should add tests that verify:

1. CLI generates all four expected artifacts.
2. CLI summary points to the evidence manifest.
3. CLI exits `0` when manifest verification passes.
4. CLI exits nonzero when manifest verification fails.
5. CLI preserves deterministic artifact roles and manifest header ids.
6. CLI output can be consumed by the Node.js and .NET examples documented in `Runtime_Evidence_Consumer_Examples.md`.

## Milestone 3 disposition

This target does not block Runtime Milestone 3 closeout.

It should be treated as the first implementation candidate for the next packaging/integration milestone after Runtime Milestone 3 closes.
