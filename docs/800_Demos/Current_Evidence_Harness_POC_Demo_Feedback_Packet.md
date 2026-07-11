# Current Evidence-Harness POC Demo Feedback Packet

## Status

```text
demo: Current Evidence-Harness POC Demo
status: complete
track: Business Demo Visibility Track
current_script: scripts/watch-constraintos-poc.ps1
current_readiness_packet: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Readiness_Packet.md
future_target_bank: Constraint-Driven Graphic Output Permutation POC v1
latest_user_reported_current_evidence_harness_poc_demo_feedback_packet_test_result: 7 passed
latest_user_reported_current_evidence_harness_poc_demo_feedback_packet_test_result_on: 2026-07-10
```

## Purpose

This packet turns the current POC demo into a structured critique loop.

It is designed for friends, early reviewers, and technical peers who watched the evidence-harness demo and want to give useful feedback without needing to understand every implementation detail.

## Context for reviewers

```text
This is not the final graphics-output demo yet.

The current demo shows the validation and traceability layer that will eventually govern generated or derived graphic outputs. It loads a scenario, loads constraints, loads fixture candidate metadata, validates intake and byte-loading boundaries, collects observation evidence, merges evidence, evaluates a fixture report, and produces a reviewable final packet.

The expected result is needs_review, not approval.
```

## What reviewers should review

```text
1. Can you tell what the system is trying to do?
2. Can you follow the staged terminal output?
3. Does the run folder make the result feel auditable?
4. Are the key output files easy to find?
5. Does final_decision: needs_review make sense?
6. Is it clear what is intentionally not implemented yet?
7. Does the future output-permutation direction make sense?
```

## Suggested evidence files to inspect

Start with:

```text
watch-output.txt
demo-summary.json
final-review-packet.json
run-metadata.json
```

Then inspect any stage-specific files that raise questions:

```text
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
```

## Feedback form

Copy this section into a message, issue, pull request comment, or shared note.

```text
Reviewer name:
Date:
Scenario reviewed:
Run folder reviewed:

1. In one sentence, what do you think ConstraintOS does?

2. Did the demo feel like a real workflow? Why or why not?

3. Which stage was easiest to understand?

4. Which stage was hardest to understand?

5. Which evidence file was most useful?

6. Which evidence file was least useful or confusing?

7. Was the needs_review result clear?

8. Was it clear that the current demo does not generate final graphics yet?

9. What would you expect the future generated graphic-output permutations to look like?

10. What would make this demo easier for a non-technical person?

11. What would make this more convincing to a technical reviewer?

12. What is the biggest product risk you see?

13. What is the strongest part of the idea?

14. What should be built next?
```

## Feedback classification

Use these labels when sorting feedback:

```text
product_clarity: reviewer did or did not understand the product promise
demo_flow: reviewer did or did not follow the staged run
evidence_quality: reviewer found evidence files useful or confusing
technical_trust: reviewer trusted or questioned the deterministic pipeline
future_output_expectations: reviewer commented on graphic-output permutations
ux_readability: reviewer commented on non-technical readability
risk_or_gap: reviewer identified a missing capability or risk
next_step: reviewer suggested what to build next
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_current_evidence_harness_poc_demo_feedback_packet.py
result: 7 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```

## What not to over-interpret

```text
- Do not treat requests for final generated graphics as a failure of the current demo; that capability is banked for a later milestone.
- Do not treat needs_review as a negative outcome; it is the expected POC result.
- Do not add arbitrary local file loading, image decoding, network fetch, CV/OCR, unrestricted generation, or automatic approval in response to feedback without a separate gated milestone.
```

## Current guardrails

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

## Local verification

```powershell
git pull --rebase origin phase-1-cli-tooling
pytest tests/test_current_evidence_harness_poc_demo_feedback_packet.py
```
