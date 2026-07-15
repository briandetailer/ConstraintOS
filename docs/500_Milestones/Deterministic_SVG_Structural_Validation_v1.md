# Deterministic SVG Structural Validation v1

## Status

```text
milestone: Deterministic SVG Structural Validation v1
status: complete
phase_1_svg_structural_validator_status: complete
phase_1_svg_runtime_validation_status: complete
phase_2_svg_validation_report_status: complete
phase_3_review_packet_surfacing_status: complete
post_closeout_browser_evidence_surfacing_status: complete
completed_on: 2026-07-14
started_on: 2026-07-13
track: Business Demo Visibility Track
previous_milestone: docs/500_Milestones/Deterministic_SVG_Graphics_Renderer_v1.md
renderer_script: scripts/watch-constraintos-output-poc.ps1
validator_script: scripts/validate-output-poc-svg-graphics.ps1
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: deterministic-svg-structural-validation-only
latest_user_reported_svg_validator_static_test_result: 8 passed
latest_user_reported_svg_validator_static_test_result_on: 2026-07-14
latest_user_reported_svg_runtime_validator_result: success message received
latest_user_reported_svg_runtime_validator_result_on: 2026-07-14
latest_user_reported_svg_validation_report_and_review_packet_test_result: 10 passed
latest_user_reported_svg_validation_report_and_review_packet_test_result_on: 2026-07-14
latest_user_reported_svg_validation_report_and_review_packet_runtime_result: success message received with validation report and review packet paths
latest_user_reported_svg_validation_report_and_review_packet_runtime_result_on: 2026-07-14
latest_user_reported_svg_browser_evidence_surfacing_static_test_result: 10 passed
latest_user_reported_svg_browser_evidence_surfacing_static_test_result_on: 2026-07-14
latest_user_reported_svg_browser_evidence_surfacing_runtime_result: proper response received
latest_user_reported_svg_browser_evidence_surfacing_runtime_result_on: 2026-07-15
assistant_ran_tests: false
assistant_ran_demo: false
```

## Purpose

Add a deterministic structural validation layer for the generated SVG artifacts so the system can prove the latest output run contains expected SVG graphics with required metadata, browser links, and approval-blocking semantics.

```text
output permutations -> deterministic SVG graphics -> structural SVG validation -> needs_review
```

## Product promise for this milestone

```text
- Validate the latest generated output-poc run.
- Confirm the graphics directory exists.
- Confirm all four SVG graphics exist.
- Confirm each SVG contains required structural metadata.
- Confirm each SVG is referenced in run-metadata.json.
- Confirm each SVG is linked from index.html.
- Confirm forbidden external image references are absent.
- Write svg-structural-validation.json as a durable validation report.
- Surface svg_structural_validation in graphic-output-review-packet.json.
- Preserve needs_review and approval_allowed: false.
```

## Target validator command

```powershell
.\scripts\validate-output-poc-svg-graphics.ps1
```

## Target SVG artifacts

```text
graphics/turbo_system_focus.svg
graphics/inline_six_engine_identity_focus.svg
graphics/technical_label_density_focus.svg
graphics/reviewer_safe_minimal_focus.svg
```

## Required SVG markers

```text
<svg xmlns="http://www.w3.org/2000/svg"
permutation_id
svg_artifact
review_decision: needs_review
approval_allowed: false
renderer: deterministic-svg-output-only
id="deterministic-graphic-core"
id="traceability-labels"
id="evidence-summary"
Toyota Supra A80
2JZ-GTE
```

## Forbidden SVG markers

```text
<image
href="http
href="file:
xlink:href="http
xlink:href="file:
auto_approved
production approval
final production artwork approved
```

## Static validator test record

```text
source: user-reported local test run
command: pytest tests/test_validate_output_poc_svg_graphics_script.py
result: 8 passed
reported_on: 2026-07-14
assistant_ran_tests: false
```

## Runtime validator record

```text
source: user-reported local runtime validation
command: .\scripts\validate-output-poc-svg-graphics.ps1
result: success message received
reported_on: 2026-07-14
assistant_ran_demo: false
```

## Validation report and review packet surfacing record

```text
source: user-reported local verification
commands:
- pytest tests/test_validate_output_poc_svg_graphics_script.py
- .\scripts\validate-output-poc-svg-graphics.ps1
results:
- test_validate_output_poc_svg_graphics_script: 10 passed
- runtime_validator: success message received with Validation report and Review packet paths
validation_report: runs/output-poc/supra_2jz_gte_twin_turbo/20260714-100414/svg-structural-validation.json
review_packet: runs/output-poc/supra_2jz_gte_twin_turbo/20260714-100414/graphic-output-review-packet.json
reported_on: 2026-07-14
assistant_ran_tests: false
assistant_ran_demo: false
```

## Post-closeout browser evidence surfacing record

```text
source: user-reported local verification
commands:
- pytest tests/test_validate_output_poc_svg_graphics_script.py
- .\scripts\validate-output-poc-svg-graphics.ps1
results:
- test_validate_output_poc_svg_graphics_script: 10 passed
- runtime_browser_summary: proper response received
browser_summary_target: svg-structural-validation-summary in index.html
runtime_browser_summary_status: complete
browser_ui: runs/output-poc/supra_2jz_gte_twin_turbo/20260714-100414/index.html
reported_on: 2026-07-15
assistant_ran_tests: false
assistant_ran_demo: false
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

## Done criteria

```text
[x] Milestone exists.
[x] Previous deterministic SVG renderer milestone is referenced.
[x] Validator command is defined.
[x] Expected SVG artifacts are listed.
[x] Required SVG markers are listed.
[x] Forbidden SVG markers are listed.
[x] Blocked scope is preserved.
[x] Validator script exists.
[x] Static validator test result recorded.
[x] Runtime validator result recorded.
[x] Validation report artifact implemented.
[x] Review packet surfacing implemented.
[x] Validation report and review packet verification recorded.
[x] Browser evidence surfacing static test recorded.
[x] Browser evidence surfacing runtime update recorded.
```

## Verification command

```powershell
pytest tests/test_deterministic_svg_structural_validation_milestone.py
pytest tests/test_validate_output_poc_svg_graphics_script.py
.\scripts\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser
.\scripts\validate-output-poc-svg-graphics.ps1
```
