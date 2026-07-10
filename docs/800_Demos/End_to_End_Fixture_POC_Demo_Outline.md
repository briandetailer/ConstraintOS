# End-to-End Fixture POC Demo Outline

## Status

```text
demo: End-to-End Fixture POC Demo
status: outline
track: Business Demo Visibility Track
current_demo_script: scripts/watch-candidate-byte-loader.ps1
current_demo_type: staged byte-loader evidence demo
recommended_next_demo_milestone: Constraint-Driven Graphic Output Permutation POC v1
```

## Purpose

This document defines the demo we want friends, reviewers, and early stakeholders to understand.

The current project is still in POC mode. Nothing in this demo should require proprietary data, private customer data, private credentials, or sensitive assets.

The goal is to show ConstraintOS as a product workflow, not just a test suite. A viewer should be able to understand what input goes in, how the system derives intended graphic outputs from loaded constraints, what deterministic validation steps run, what evidence is produced, and why the system reaches its final result.

## Product charter reminder

```text
ConstraintOS is an open architecture for deterministic, auditable, specification-driven publishing using probabilistic AI systems.

Structured specifications, validation, and traceability — not AI model behavior — are the source of truth.
```

For demo purposes, this means the system should visibly prefer constraints, output specifications, evidence, review packets, and traceable outputs over opaque model confidence.

## Product correction

The POC demo target is not only an evidence-review system.

The intended product workflow is:

```text
input_constraints + scenario instructions -> graphic output permutations -> validation evidence -> reviewable result
```

The POC should demonstrate that ConstraintOS can define output from input. It should load scenario constraints, derive a series of graphic-output permutations from those constraints, and then show evidence that each proposed output meets, fails, or needs review against the loaded requirements.

In other words, the review packets are not the product output by themselves. They are the traceability layer around the intended output: a controlled set of graphics or graphic-output specifications generated from the loaded constraints.

## Demo audience

```text
primary_audience: friends and early reviewers
secondary_audience: future collaborators, technical peers, potential users
viewer_context: curious but not expected to know the codebase
viewer_question: What have you built, what does it do, and where is it going?
```

## Corrected demo promise

The demo should answer this in one sentence:

```text
ConstraintOS takes a constrained graphic-production request, derives a series of compliant graphic output permutations, and produces traceable validation evidence showing how each output relates to the loaded requirements.
```

## What the current demo can show now

The current script can already show the byte-loading evidence path in motion:

```powershell
.\scripts\watch-candidate-byte-loader.ps1 -Record perseverance
```

It demonstrates:

```text
1. Select a candidate record.
2. Load deterministic fixture bytes for that selected record.
3. Build a selected-record byte-loading review packet.
4. Review deterministic fixture registry descriptors.
5. Review fixture registry failure-matrix evidence.
6. Capture JSON evidence files.
7. End with a needs_review / non-approval guardrail.
```

This is useful because it shows the safety foundation moving, but it is not yet the corrected full product workflow.

## What the current demo does not yet show

```text
- It does not derive new graphic-output permutations from loaded constraints.
- It does not output a series of graphics.
- It does not output graphic-output specifications ready for rendering.
- It does not compare multiple generated/derived output variants.
- It does not accept a real local image file as input.
- It does not decode images.
- It does not inspect pixels.
- It does not run computer vision.
- It does not run OCR.
- It does not score a candidate automatically.
- It does not mutate source reports.
- It does not approve candidates.
```

Those are intentional constraints at this phase. The current POC is proving traceable validation before broader real-input and real-render processing.

## Target end-to-end fixture demo

The next full demo should be fixture-based, not real-file-based.

That means it should use controlled, non-sensitive fixture data but behave like the product workflow:

```text
Input:
  A named demo scenario, such as perseverance or supra_2jz_gte_twin_turbo.

Loaded constraints:
  Contract/specification requirements for the selected graphic scenario.

Output derivation:
  A controlled set of graphic-output permutations based on the loaded constraints.

Pipeline:
  1. Load the graphics validation contract.
  2. Load scenario instructions and output requirements.
  3. Derive graphic-output permutations from those requirements.
  4. Emit each output as a fixture-safe graphic-output specification or placeholder artifact record.
  5. Validate each output specification against the loaded constraints.
  6. Load candidate manifest or intake records for selected fixture artifacts.
  7. Validate candidate intake boundaries.
  8. Load deterministic fixture bytes when artifact bytes are part of the scenario.
  9. Produce byte-loading evidence.
  10. Load manual observation fixtures.
  11. Bind observations to the expected report structure.
  12. Merge evidence.
  13. Evaluate outputs against the contract/report expectations.
  14. Produce a final review packet.

Output:
  A set of graphic-output permutations, validation evidence for each permutation, a demo summary with final status, evidence paths, and non-approval guardrails.
```

## Recommended command shape

The corrected demo should run with one command:

```powershell
.\scripts\watch-constraintos-output-poc.ps1 -Scenario perseverance
```

Optional variants:

```powershell
.\scripts\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo
.\scripts\watch-constraintos-output-poc.ps1 -Scenario perseverance -PermutationCount 4
.\scripts\watch-constraintos-output-poc.ps1 -Scenario perseverance -WatchDelayMs 750
.\scripts\watch-constraintos-output-poc.ps1 -Scenario perseverance -OpenRunFolder
```

The existing `scripts/watch-constraintos-poc.ps1` remains useful as an evidence-harness demo, but it should not be treated as the complete corrected product demo because it does not yet produce output permutations.

## Recommended demo stages

```text
[1/12] Load scenario
[2/12] Load contract/specification constraints
[3/12] Load output-generation instructions
[4/12] Derive graphic-output permutations
[5/12] Emit graphic-output specification files
[6/12] Validate each output specification against constraints
[7/12] Load candidate manifest/intake records
[8/12] Load deterministic fixture bytes where applicable
[9/12] Generate byte-loading and registry evidence
[10/12] Load, bind, and merge observation evidence
[11/12] Evaluate output permutations against contract expectations
[12/12] Produce final review packet and demo summary
```

## Intended result for corrected POC demo

The intended POC result should be:

```text
graphic_outputs_created: true
graphic_output_type: fixture-safe graphic-output specifications or placeholder artifacts
permutation_count: scenario-defined
final_decision: needs_review
approval_allowed: false
reason: The system produced constraint-derived output permutations and traceable validation evidence, but automatic approval is intentionally blocked in the POC.
```

This is not a weakness. It demonstrates the product charter: ConstraintOS should define and validate output through evidence before allowing higher-risk automation.

## Demo outputs

The corrected fixture demo should write files under:

```text
runs/poc-demo/<scenario>/<timestamp>/
```

Recommended output files:

```text
terminal-transcript.txt
watch-output.txt
scenario.json
contract.json
output-instructions.json
graphic-output-permutation-001.json
graphic-output-permutation-002.json
graphic-output-permutation-003.json
graphic-output-permutation-004.json
graphic-output-manifest.json
permutation-validation-report.json
candidate-manifest.json
candidate-intake.json
byte-loading.json
byte-loading-review-packet.json
fixture-registry-review-packet.json
failure-review-packet.json
manual-observations.json
observation-binding.json
merged-evidence.json
evaluation-report.json
final-review-packet.json
demo-summary.json
run-metadata.json
```

## Reviewer walkthrough script

Use this simple spoken walkthrough:

```text
This is ConstraintOS. The goal is not to make AI magically correct. The goal is to wrap probabilistic AI work in deterministic specs, validation, traceability, and review gates.

For this POC, I am using safe fixture data instead of private or proprietary inputs.

The demo starts with a named scenario. It loads the constraints, derives several graphic-output permutations from those constraints, writes those output specifications, validates each one against the requirements, and then produces reviewable evidence explaining what each output satisfies or still needs reviewed.

The important thing to notice is that output is defined from input. The system does not approve anything just because a model says it looks right. The output is generated or specified from constraints, and the evidence remains traceable.
```

## What to ask reviewers

```text
1. Could you understand what the system was trying to produce?
2. Did the output permutations feel like meaningful variations based on the instructions?
3. Could you understand what constraints each output was supposed to satisfy?
4. Did the staged output make the workflow feel real?
5. Was the final result clear?
6. Did the evidence files make sense?
7. What felt like product value versus engineering plumbing?
8. What kinds of graphic outputs would you expect the next demo to render visibly?
9. Would this be easier to understand with a web UI, generated HTML report, image contact sheet, or terminal demo?
```

## Success criteria

The demo is successful when a reviewer can say:

```text
- I understand the input constraints.
- I understand the intended graphic outputs.
- I understand why there are multiple output permutations.
- I understand the major validation stages.
- I understand what evidence was produced for each output.
- I understand why the final decision is needs_review.
- I understand what is intentionally blocked.
- I can see how this becomes a real input-to-graphics product later.
```

## Next milestone recommendation

```text
recommended_next_milestone: Constraint-Driven Graphic Output Permutation POC v1
primary_output: scripts/watch-constraintos-output-poc.ps1
supporting_output: runs/poc-demo/<scenario>/<timestamp>/graphic-output-manifest.json
supporting_output: runs/poc-demo/<scenario>/<timestamp>/demo-summary.json
verification: pytest tests/test_constraint_driven_graphic_output_permutation_poc.py
```

## Guardrails for the next demo

```text
- Keep the next demo fixture-based.
- Output graphic specifications or controlled placeholder artifacts first.
- Do not add arbitrary local image file opening yet.
- Do not add file_uri loading yet.
- Do not add artifact download yet.
- Do not add network fetch yet.
- Do not add image decoding yet.
- Do not add pixel inspection yet.
- Do not add CV/OCR provider integration yet.
- Do not add unrestricted image generation or editing.
- Do not add automatic candidate scoring.
- Do not mutate source reports.
- Do not enable approval automation.
```

## Later real-output demo

A later demo can render actual image files only after the project has explicit gates for:

```text
- controlled rendering provider boundary
- allowed output directories
- output manifest schema
- deterministic prompt/spec construction
- variant/permutation tracking
- generated artifact checksums
- image decoding or inspection boundary if needed
- human review gate
- no automatic approval without explicit approval milestone
```
