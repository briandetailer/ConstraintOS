# End-to-End Fixture POC Demo Outline

## Status

```text
demo: End-to-End Fixture POC Demo
status: outline
track: Business Demo Visibility Track
current_demo_script: scripts/watch-candidate-byte-loader.ps1
current_demo_type: staged byte-loader evidence demo
recommended_next_demo_milestone: End-to-End Fixture POC Demo v1
```

## Purpose

This document defines the demo we want friends, reviewers, and early stakeholders to understand.

The current project is still in POC mode. Nothing in this demo should require proprietary data, private customer data, private credentials, or sensitive assets.

The goal is to show ConstraintOS as a product workflow, not just a test suite. A viewer should be able to understand what input goes in, what deterministic validation steps run, what evidence is produced, and why the system reaches its final result.

## Product charter reminder

```text
ConstraintOS is an open architecture for deterministic, auditable, specification-driven publishing using probabilistic AI systems.

Structured specifications, validation, and traceability — not AI model behavior — are the source of truth.
```

For demo purposes, this means the system should visibly prefer evidence, contracts, review packets, and traceable outputs over opaque model confidence.

## Demo audience

```text
primary_audience: friends and early reviewers
secondary_audience: future collaborators, technical peers, potential users
viewer_context: curious but not expected to know the codebase
viewer_question: What have you built, what does it do, and where is it going?
```

## Demo promise

The demo should answer this in one sentence:

```text
ConstraintOS takes a candidate artifact, runs it through a deterministic validation and evidence pipeline, and produces a reviewable result with traceable reasons instead of trusting AI output directly.
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

This is useful because it shows the safety foundation moving, but it is not yet the full product workflow.

## What the current demo does not yet show

```text
- It does not accept a real local image file as input.
- It does not decode images.
- It does not inspect pixels.
- It does not run computer vision.
- It does not run OCR.
- It does not score a candidate automatically.
- It does not mutate source reports.
- It does not approve candidates.
- It does not yet run the full contract-to-final-review flow in one command.
```

Those are intentional constraints at this phase. The POC is proving traceable validation before broader real-input processing.

## Target end-to-end fixture demo

The next full demo should be fixture-based, not real-file-based.

That means it should use controlled, non-sensitive fixture data but behave like the product workflow:

```text
Input:
  A named demo scenario, such as perseverance or supra_2jz_gte_twin_turbo.

Pipeline:
  1. Load the graphics validation contract.
  2. Load the candidate manifest or intake record.
  3. Validate candidate intake boundaries.
  4. Load deterministic fixture bytes.
  5. Produce byte-loading evidence.
  6. Load manual observation fixtures.
  7. Bind observations to the expected report structure.
  8. Merge evidence.
  9. Evaluate the candidate against the contract/report expectations.
  10. Produce a final review packet.

Output:
  A demo summary with final status, reasons, evidence paths, and non-approval guardrails.
```

## Recommended command shape

The next demo should run with one command:

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
```

Optional variants:

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario supra_2jz_gte_twin_turbo
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance -WatchDelayMs 750
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance -OpenRunFolder
```

## Recommended demo stages

```text
[1/10] Load scenario
[2/10] Load contract/specification
[3/10] Load candidate manifest/intake record
[4/10] Validate intake boundaries
[5/10] Load deterministic fixture bytes
[6/10] Generate byte-loading evidence packet
[7/10] Load and bind observation evidence
[8/10] Merge evidence into candidate report
[9/10] Evaluate against contract expectations
[10/10] Produce final review packet and demo summary
```

## Intended result for POC demo

The intended POC result should be:

```text
final_decision: needs_review
approval_allowed: false
reason: The system produced traceable evidence and review packets, but automatic approval is intentionally blocked in the POC.
```

This is not a weakness. It demonstrates the product charter: ConstraintOS should make the evidence visible before allowing higher-risk automation.

## Demo outputs

The full fixture demo should write files under:

```text
runs/poc-demo/<scenario>/<timestamp>/
```

Recommended output files:

```text
terminal-transcript.txt
watch-output.txt
scenario.json
contract.json
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

The demo starts with a named scenario. It loads the contract, loads the candidate metadata, validates the intake rules, loads deterministic fixture bytes, binds observations, merges evidence, evaluates the candidate against expectations, and produces a final review packet.

The important thing to notice is that every step leaves evidence behind. The system does not approve anything just because bytes loaded or because a model says it looks right. The output is reviewable and traceable.
```

## What to ask reviewers

```text
1. Could you understand what the system was doing without reading the code?
2. Did the staged output make the workflow feel real?
3. Was the final result clear?
4. Did the evidence files make sense?
5. What felt like product value versus engineering plumbing?
6. What would you expect the next demo to process?
7. Would this be easier to understand with a web UI, generated HTML report, or terminal demo?
```

## Success criteria

The demo is successful when a reviewer can say:

```text
- I understand the input.
- I understand the major validation stages.
- I understand what evidence was produced.
- I understand why the final decision is needs_review.
- I understand what is intentionally blocked.
- I can see how this becomes a real input-processing product later.
```

## Next milestone recommendation

```text
recommended_next_milestone: End-to-End Fixture POC Demo v1
primary_output: scripts/watch-constraintos-poc.ps1
supporting_output: runs/poc-demo/<scenario>/<timestamp>/demo-summary.json
verification: pytest tests/test_end_to_end_fixture_poc_demo.py
```

## Guardrails for the next demo

```text
- Keep the next demo fixture-based.
- Do not add arbitrary local image file opening yet.
- Do not add file_uri loading yet.
- Do not add artifact download yet.
- Do not add network fetch yet.
- Do not add image decoding yet.
- Do not add pixel inspection yet.
- Do not add CV/OCR provider integration yet.
- Do not add image generation or editing.
- Do not add automatic candidate scoring.
- Do not mutate source reports.
- Do not enable approval automation.
```

## Later real-input demo

A later demo can accept a real local candidate image only after the project has explicit gates for:

```text
- allowed local roots
- path normalization
- size limits
- checksum verification
- media-type sniffing
- safe image decoding boundaries
- no network fallback
- clear failure states
- review packet generation
- explicit non-approval defaults
```

That later demo should feel like:

```powershell
.\scripts\watch-constraintos-real-input.ps1 -Contract perseverance -CandidatePath .\demo-inputs\candidate.png
```

but that is not the next safest POC step.
