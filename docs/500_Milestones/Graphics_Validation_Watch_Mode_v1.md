# Graphics Validation Watch Mode v1

## Status

```text
milestone: Graphics Validation Watch Mode v1
status: implementation-complete-pending-test
started_on: 2026-07-07
previous_gate: Graphics Validation Pipeline - NASA Perseverance v1 complete
baseline: 487 passed
```

## Purpose

Add a one-command, recordable watch path for the Perseverance graphics-validation example.

The goal is to let a user start a single command and capture the run as it moves through the runtime stages, without manually starting and stopping a transcript.

## Implementation slices

```text
[x] Add --watch output mode to cos-graphics-validate
[x] Add optional --watch-delay-ms for readable terminal recording
[x] Add tests for watch output
[x] Add scripts/watch-perseverance.ps1 one-command runner
[x] Save timestamped run folder
[x] Save terminal transcript
[x] Save clean watch output
[x] Save machine-readable JSON result
[x] Save run metadata
[x] Add watch recording guide
[ ] Run tests and record verified result
[ ] Run watch script and record verified output files
```

## Commands

```powershell
pytest tests/test_graphics_validation_cli.py

.\scripts\watch-perseverance.ps1
```

## Output files

```text
runs/graphics/perseverance/<timestamp>/terminal-transcript.txt
runs/graphics/perseverance/<timestamp>/watch-output.txt
runs/graphics/perseverance/<timestamp>/graphics-validation-result.json
runs/graphics/perseverance/<timestamp>/run-metadata.json
```

## Watch behavior

```text
- Shows graphics-validation header.
- Shows example, subject, expected decision, and fixture-only mode.
- Shows each runtime node in order.
- Shows node id, plugin, worker, schedule assignment, and result.
- Shows final runtime, schedule, execution, and approval expectation summary.
- Keeps image generation explicitly marked as not run.
```

## Guardrails

```text
- Do not claim tests passed unless actually run.
- Do not claim the watch script produced files until the script has actually been run.
- Keep this fixture-only until real image generation/evaluation adapters are deliberately introduced.
```
