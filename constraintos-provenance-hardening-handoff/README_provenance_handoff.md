# ConstraintOS Provenance Hardening Handoff

This handoff is for the provenance schema hardening work that the ChatGPT GitHub connector blocked.

## What this handoff changes

- Replaces `schemas/provenance-manifest.schema.json` with a stricter schema.
- Adds `examples/traceability/PROVENANCE-0002-rejected.yaml`.
- Adds `tests/test_provenance_manifest_schema.py`.

## Apply from PowerShell

From your local repo root:

```powershell
git status
git checkout phase-1-cli-tooling
git pull
Expand-Archive -Force .\constraintos-provenance-hardening-handoff.zip .\constraintos-provenance-hardening-handoff
Copy-Item -Force .\constraintos-provenance-hardening-handoff\schemas\provenance-manifest.schema.json .\schemas\provenance-manifest.schema.json
Copy-Item -Force .\constraintos-provenance-hardening-handoff\examples\traceability\PROVENANCE-0002-rejected.yaml .\examples\traceability\PROVENANCE-0002-rejected.yaml
Copy-Item -Force .\constraintos-provenance-hardening-handoff\tests\test_provenance_manifest_schema.py .\tests\test_provenance_manifest_schema.py
git diff -- schemas/provenance-manifest.schema.json examples/traceability/PROVENANCE-0002-rejected.yaml tests/test_provenance_manifest_schema.py
```

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_provenance_manifest_schema.py
.\.venv\Scripts\python.exe -m pytest
```

Expected result, if your current baseline is 341 passed:

```text
345 passed
```

## Commit

Only commit after the tests pass:

```powershell
git add schemas/provenance-manifest.schema.json examples/traceability/PROVENANCE-0002-rejected.yaml tests/test_provenance_manifest_schema.py
git commit -m "Harden provenance manifest schema"
git push
```

## Roll back before committing

```powershell
git restore schemas/provenance-manifest.schema.json
git clean -f examples/traceability/PROVENANCE-0002-rejected.yaml tests/test_provenance_manifest_schema.py
```
