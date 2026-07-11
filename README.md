# ConstraintOS

ConstraintOS is an open architecture for deterministic, auditable, specification-driven publishing using probabilistic AI systems.

## Mission

Build a constraint-first platform where structured specifications, validation, and traceability — not AI model behavior — are the source of truth.

## Current POC status

ConstraintOS is currently in public POC mode.

The current working demo is an **evidence-harness POC**. It does not generate final graphics yet. It shows the validation and traceability layer that will eventually govern generated or derived graphic outputs.

Current demo shape:

```text
scenario + constraints + fixture candidate evidence
-> deterministic validation and review stages
-> auditable evidence files
-> final review packet
-> needs_review result
```

The banked future target is a product-shaped demo where loaded constraints and scenario instructions produce a controlled set of graphic-output permutations, and the evidence pipeline validates those outputs.

## Current demo

Run from the repository root:

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
```

Optional alternate scenario:

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario supra_2jz_gte_twin_turbo
```

Open the generated run folder automatically:

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance -OpenRunFolder
```

## What the current demo shows

```text
1. Scenario selection.
2. Contract/specification loading.
3. Candidate manifest and intake evidence loading.
4. Intake review boundaries.
5. Deterministic fixture byte loading.
6. Byte-loading and registry evidence.
7. Fixture registry failure-matrix evidence.
8. Manual observation evidence loading and binding.
9. Evidence merge and fixture evaluation.
10. Final review packet and demo summary.
```

The current expected result is:

```text
final_decision: needs_review
approval_allowed: false
```

That result is intentional. The current POC proves traceable evidence and review boundaries; it does not approve automatically.

## Demo artifacts

Each demo run writes a timestamped folder under:

```text
runs/poc-demo/<scenario>/<timestamp>/
```

Start review with:

```text
watch-output.txt
demo-summary.json
final-review-packet.json
run-metadata.json
```

## Reviewer docs

Start here if you are reviewing or critiquing the project:

```text
docs/800_Demos/Current_Evidence_Harness_POC_Demo_Readiness_Packet.md
docs/800_Demos/Current_Evidence_Harness_POC_Demo_Guide.md
docs/800_Demos/End_to_End_Fixture_POC_Demo_Outline.md
```

The readiness packet is the shortest reviewer checklist. The guide explains how to talk through the current demo. The outline records the future product-shaped demo target.

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
- No unrestricted image generation or editing.
- No automatic candidate approval.
```

## Local verification

```powershell
git pull --rebase origin phase-1-cli-tooling
pytest tests/test_public_demo_reviewer_entry_point.py
pytest tests/test_current_evidence_harness_poc_demo_readiness_packet.py
pytest tests/test_current_evidence_harness_poc_demo_guide.py
pytest tests/test_end_to_end_fixture_poc_demo.py
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
```

## Current branches

Active development is on:

```text
phase-1-cli-tooling
```

## Future target

The future product-shaped POC is banked as:

```text
Constraint-Driven Graphic Output Permutation POC v1
```

That future milestone should demonstrate:

```text
input constraints + scenario instructions
-> controlled graphic-output permutations
-> validation evidence for each output
-> reviewable result
```
