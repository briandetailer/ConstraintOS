# Current Evidence-Harness POC Demo Guide

## Status

```text
demo: Current Evidence-Harness POC Demo
status: guide
track: Business Demo Visibility Track
current_script: scripts/watch-constraintos-poc.ps1
future_target_bank: Constraint-Driven Graphic Output Permutation POC v1
```

## Purpose

This guide explains the current demo that exists now, without confusing it with the later product-shaped demo that will output constraint-driven graphic permutations.

The current demo is an evidence-harness POC. It shows ConstraintOS moving a named fixture scenario through the deterministic validation and review pipeline that exists today.

It does not yet generate a series of new graphics. That later output-permutation goal is intentionally banked for a future milestone.

## One-command demo

Run from the repository root:

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
```

Optional variants:

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario supra_2jz_gte_twin_turbo
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance -WatchDelayMs 750
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance -OpenRunFolder
```

## What to say before running it

```text
This is the current ConstraintOS POC demo. It does not generate final graphics yet. It demonstrates the validation and traceability layer that will eventually govern generated graphic outputs.

The point of this demo is to show the system loading a scenario, loading constraints, loading candidate metadata, validating intake, loading deterministic fixture bytes, collecting observation evidence, merging evidence, evaluating the fixture, and producing a final review packet.

The important part is that every stage leaves evidence behind. The system does not approve anything automatically.
```

## What the demo shows

```text
1. The scenario is selected.
2. The contract/specification is loaded.
3. The candidate manifest and intake evidence are loaded.
4. Intake boundaries are reviewed.
5. Deterministic fixture bytes are loaded.
6. Byte-loading and registry evidence are generated.
7. Fixture registry failure-matrix evidence is reviewed.
8. Manual observation evidence is loaded and bound.
9. Evidence is merged and evaluated against the fixture report.
10. A final review packet and demo summary are produced.
```

## What the demo writes

The script writes a run folder under:

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

## What to open after the demo

Start with:

```text
watch-output.txt
demo-summary.json
final-review-packet.json
run-metadata.json
```

Then open the evidence files if someone wants to inspect a specific stage.

## Intended current result

```text
final_decision: needs_review
approval_allowed: false
```

This is expected. The current POC is proving traceability and review boundaries, not automatic approval.

## What this demo intentionally does not do

```text
- It does not generate a new series of graphics.
- It does not derive graphic-output permutations from constraints yet.
- It does not accept arbitrary local image files.
- It does not load local_file_path references.
- It does not load file_uri references.
- It does not download artifacts.
- It does not fetch network resources.
- It does not decode images.
- It does not inspect pixels.
- It does not run CV/OCR providers.
- It does not run unrestricted image generation or editing.
- It does not automatically approve candidates.
```

## How to explain the future target

```text
The next product-shaped demo will add the missing output layer: loaded constraints and scenario instructions should produce a controlled set of graphic-output permutations, then the same evidence pipeline should validate those outputs.

That future target is banked as Constraint-Driven Graphic Output Permutation POC v1. The current demo proves the evidence harness that future output generation will plug into.
```

## Reviewer questions

```text
1. Could you follow the stages as the demo ran?
2. Did the run folder make the system feel auditable?
3. Was the final needs_review result clear?
4. Which evidence file was most useful?
5. Was it obvious that this is not yet the final graphics-output demo?
6. What would you expect the generated graphic permutations to look like later?
```

## Local verification

```powershell
git pull --rebase origin phase-1-cli-tooling
pytest tests/test_end_to_end_fixture_poc_demo.py
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
```
