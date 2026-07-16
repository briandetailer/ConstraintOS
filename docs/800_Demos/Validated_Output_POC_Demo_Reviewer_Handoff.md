# Validated Output POC Demo Reviewer Handoff

## Status

```text
handoff: Validated Output POC Demo Reviewer Handoff
status: ready-for-use
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
launcher_script: scripts/run-validated-output-poc-demo.ps1
implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only
```

## Reviewer entry point

Use the one-command validated demo launcher:

```powershell
.\scripts\run-validated-output-poc-demo.ps1
```

For terminal-only verification without opening the browser:

```powershell
.\scripts\run-validated-output-poc-demo.ps1 -NoOpenBrowser
```

## What the launcher does

```text
1. Runs the fixture-safe output POC generator.
2. Runs deterministic SVG structural validation.
3. Writes svg-structural-validation.json.
4. Updates graphic-output-review-packet.json with svg_structural_validation.
5. Writes validated-output-poc-demo-summary.json.
6. Adds SVG structural validation evidence to index.html.
7. Adds validated demo launcher evidence to index.html.
8. Opens the latest generated browser UI by default.
```

## Expected terminal evidence

The final launcher output should include:

```text
Validated ConstraintOS output POC demo complete.
Run directory:
Browser UI:
Validation report:
Review packet:
Launcher summary:
Browser summary updated:
Final decision remains: needs_review
Approval allowed remains: false
```

## Expected browser evidence

The generated `index.html` should include these reviewer-visible sections:

```text
Deterministic SVG graphics
SVG structural validation
Validated demo launcher
```

The browser-visible launcher summary should include:

```text
One-command validated output POC complete
needs_review
approval_allowed: false
validated-output-poc-demo-summary.json
svg-structural-validation.json
graphic-output-review-packet.json
```

## Expected run artifacts

Inspect the latest folder under:

```text
runs/output-poc/supra_2jz_gte_twin_turbo/<timestamp>/
```

Expected files:

```text
index.html
run-metadata.json
graphic-output-manifest.json
graphic-output-permutations.json
graphic-output-validation.json
graphic-output-review-packet.json
svg-structural-validation.json
validated-output-poc-demo-summary.json
graphics/turbo_system_focus.svg
graphics/inline_six_engine_identity_focus.svg
graphics/technical_label_density_focus.svg
graphics/reviewer_safe_minimal_focus.svg
```

## Reviewer decision rule

```text
If the browser opens, the SVG validation summary is visible, the validated launcher summary is visible, and the terminal output preserves needs_review and approval_allowed: false, then the validated output POC demo is ready to show as a fixture-safe product demonstration.
```

## Explicitly blocked scope

```text
- Real generated final graphics.
- Production artwork generation.
- Real local image input.
- local_file_path loading.
- file_uri loading.
- Artifact download.
- Network fetch.
- Image decoding.
- Pixel inspection.
- CV/OCR provider integration.
- Automatic approval.
```

## Verification command

```powershell
pytest tests/test_validated_output_poc_demo_reviewer_handoff.py
```
