# Current Evidence-Harness POC Demo Readiness Packet

## Status

```text
demo: Current Evidence-Harness POC Demo
status: readiness-packet
track: Business Demo Visibility Track
current_script: scripts/watch-constraintos-poc.ps1
current_guide: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Guide.md
future_target_bank: Constraint-Driven Graphic Output Permutation POC v1
```

## Purpose

This packet is the reviewer-facing checklist for the current ConstraintOS POC demo.

It is meant for friends, early reviewers, and technical peers who want to critique what exists now without confusing it with the later constraint-driven graphic output permutation demo.

The current demo is not the final product-shaped graphics-output demo. It is the evidence harness that future output generation will plug into.

## One-sentence framing

```text
ConstraintOS currently demonstrates a fixture-based evidence pipeline: it loads a scenario, loads constraints and candidate metadata, validates intake and byte-loading boundaries, collects observation evidence, merges evidence, evaluates a fixture report, and produces a reviewable final packet without automatic approval.
```

## What to run

From the repository root:

```powershell
git pull --rebase origin phase-1-cli-tooling
pytest tests/test_current_evidence_harness_poc_demo_guide.py
pytest tests/test_end_to_end_fixture_poc_demo.py
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
```

Optional alternate scenario:

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario supra_2jz_gte_twin_turbo
```

Open the generated run folder after the demo:

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance -OpenRunFolder
```

## What reviewers should see

```text
1. A visible staged terminal run.
2. A named scenario being selected.
3. Contract/specification evidence being loaded.
4. Candidate manifest and intake evidence being loaded.
5. Intake review boundaries being shown.
6. Deterministic fixture byte-loading evidence being generated.
7. Fixture registry and failure-matrix review evidence being generated.
8. Manual observation evidence being loaded and bound.
9. Evidence being merged and evaluated.
10. A final review packet and demo summary being produced.
```

## Expected run folder

The script should write a timestamped folder under:

```text
runs/poc-demo/<scenario>/<timestamp>/
```

Expected files:

```text
terminal-transcript.txt
watch-output.txt
contract.json
candidate-manifest.json
candidate-intake.json
candidate-intake-review-packet.json
byte-loading.json
byte-loading-review-packet.json
fixture-registry-review-packet.json
fixture-registry-failure-review-packet.json
manual-observations.json
observation-binding.json
merged-evidence.json
evaluation-report.json
final-review-packet.json
demo-summary.json
run-metadata.json
```

## Suggested inspection order

Start here:

```text
1. watch-output.txt
2. demo-summary.json
3. final-review-packet.json
4. run-metadata.json
```

Then inspect stage-specific evidence files if the reviewer wants to go deeper.

## Current intended result

```text
final_decision: needs_review
approval_allowed: false
```

This is expected.

The current POC is proving traceable evidence and review boundaries. It is not trying to approve, generate unrestricted graphics, inspect real image pixels, or replace human review.

## What is intentionally not included yet

```text
- No generated series of final graphics yet.
- No constraint-derived graphic output permutations yet.
- No arbitrary local image file input.
- No local_file_path loading.
- No file_uri loading.
- No artifact download.
- No network fetch.
- No image decoding.
- No pixel inspection.
- No CV/OCR provider integration.
- No unrestricted image generation.
- No unrestricted image editing.
- No automatic candidate approval.
```

## How to explain the banked future target

```text
The later product-shaped POC should add the missing output layer: loaded constraints and scenario instructions should produce a controlled set of graphic-output permutations. Then this same evidence pipeline should validate those outputs.

That later milestone is banked as Constraint-Driven Graphic Output Permutation POC v1.
```

## Reviewer critique prompts

```text
1. Could you follow what the system was doing as it ran?
2. Did the staged terminal output make the workflow feel real?
3. Did the run folder make the result feel auditable?
4. Which evidence files were most useful?
5. Was the final needs_review decision understandable?
6. Was it clear that this is the current evidence harness, not the final graphics-output demo?
7. What would make this easier to demo to a non-technical viewer?
8. What should the future generated graphic permutations look like?
```

## Demo readiness checklist

```text
[x] One-command demo script exists.
[x] Current guide exists.
[x] Readiness packet exists.
[x] Reviewer-facing framing exists.
[x] Expected run folder and files are documented.
[x] Suggested inspection order is documented.
[x] Current limitations are documented.
[x] Future output-permutation target is banked.
[ ] Local verification result recorded.
```

## Local verification

```powershell
git pull --rebase origin phase-1-cli-tooling
pytest tests/test_current_evidence_harness_poc_demo_readiness_packet.py
pytest tests/test_current_evidence_harness_poc_demo_guide.py
pytest tests/test_end_to_end_fixture_poc_demo.py
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
```
