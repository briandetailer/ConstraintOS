# Constraint-Driven Graphic Output Permutation POC Reviewer Handoff

## Status

```text
demo: Constraint-Driven Graphic Output Permutation POC
status: ready-to-show
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Constraint_Driven_Graphic_Output_Permutation_POC_v1.md
contract: docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Contract.md
fixture_data: docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Toyota_Fixtures.md
watch_script: scripts/watch-constraintos-output-poc.ps1
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
latest_user_reported_constraint_driven_graphic_output_permutation_watch_script_test_result: 8 passed
latest_user_reported_constraint_driven_graphic_output_permutation_watch_script_test_result_on: 2026-07-10
assistant_ran_tests: false
```

## The file to show a reviewer

The reviewer-facing file is the generated browser page:

```text
runs/output-poc/supra_2jz_gte_twin_turbo/<timestamp>/index.html
```

Do not point a non-technical reviewer directly at the PowerShell script, JSON files, or source documents unless they specifically want implementation details.

## How to generate the reviewer-facing file

Run:

```powershell
git pull --rebase origin phase-1-cli-tooling
.\scripts\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser
```

The `-OpenBrowser` flag opens the generated `index.html` automatically.

## What the reviewer should see

```text
- A browser page titled around the ConstraintOS output permutation POC.
- The Toyota Supra A80 / 2JZ-GTE twin-turbo use case.
- Four fixture-safe output permutations:
  - turbo_system_focus
  - inline_six_engine_identity_focus
  - technical_label_density_focus
  - reviewer_safe_minimal_focus
- A clear final_decision: needs_review.
- A clear approval_allowed: false.
- A guardrail statement that this demo does not generate final graphics or inspect real images.
```

## Generated files in the same run folder

```text
graphic-output-manifest.json
graphic-output-permutations.json
graphic-output-validation.json
graphic-output-review-packet.json
index.html
run-metadata.json
```

The `index.html` is the business-viewable page. The JSON files are supporting evidence artifacts for technical reviewers.

## How to present it

```text
1. Run the watch script with -OpenBrowser.
2. Let the reviewer look at the generated index.html page.
3. Explain that this is the controlled output layer: constraints define multiple output specifications.
4. Point out that all variants remain needs_review.
5. Explain that approval stays blocked because this is still fixture-safe and not final generated artwork.
6. Use the JSON files only if the reviewer asks how the page is grounded.
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py
result: 8 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```

## Guardrails

```text
- Fixture-safe output specifications only.
- No generated final graphics.
- No production artwork generation.
- No real local image input.
- No local_file_path loading.
- No file_uri loading.
- No artifact download.
- No network fetch.
- No image decoding.
- No pixel inspection.
- No CV/OCR provider integration.
- No automatic approval.
```

## Local verification

```powershell
pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py
```
