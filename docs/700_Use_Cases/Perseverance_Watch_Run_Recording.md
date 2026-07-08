# Perseverance Watch Run Recording

## One-command run

From the repository root:

```powershell
.\scripts\watch-perseverance.ps1
```

This command creates a timestamped folder under:

```text
runs/graphics/perseverance/<timestamp>/
```

## Output files

The run folder contains:

```text
terminal-transcript.txt
watch-output.txt
graphics-validation-result.json
run-metadata.json
```

File meanings:

```text
terminal-transcript.txt: text capture of the PowerShell session
watch-output.txt: clean step-by-step ConstraintOS watch output
graphics-validation-result.json: machine-readable runtime result
run-metadata.json: timestamps, status, exit code, and output paths
```

There is no save prompt. Files are written automatically.

## Slower watch output

Use a longer delay when the terminal output should move more slowly:

```powershell
.\scripts\watch-perseverance.ps1 -WatchDelayMs 500
```

## Direct watch command

The script wraps this command:

```powershell
cos-graphics-validate perseverance --watch --watch-delay-ms 250
```

The direct command is useful for checking the watch view without writing a run folder.
