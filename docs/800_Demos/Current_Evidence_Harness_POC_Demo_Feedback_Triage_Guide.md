# Current Evidence-Harness POC Demo Feedback Triage Guide

## Status

```text
demo: Current Evidence-Harness POC Demo
status: complete
track: Business Demo Visibility Track
feedback_packet: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Packet.md
issue_template: .github/ISSUE_TEMPLATE/demo-feedback.md
future_target_bank: Constraint-Driven Graphic Output Permutation POC v1
latest_user_reported_current_evidence_harness_poc_demo_feedback_triage_guide_test_result: 5 passed
latest_user_reported_current_evidence_harness_poc_demo_feedback_triage_guide_test_result_on: 2026-07-10
```

## Purpose

This guide explains how to sort feedback from friends, early reviewers, and technical peers after they review the current evidence-harness POC demo.

The goal is to turn comments into actionable categories without accidentally expanding scope beyond the current POC guardrails.

## Triage inputs

```text
- GitHub issues created from .github/ISSUE_TEMPLATE/demo-feedback.md
- Notes copied from docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Packet.md
- Direct messages or verbal feedback from demo reviewers
```

## Feedback categories

Use these categories when sorting feedback:

```text
product_clarity: reviewer understood or misunderstood what ConstraintOS is trying to do
demo_flow: reviewer could or could not follow the staged terminal run
evidence_quality: reviewer found evidence files useful, noisy, missing, or confusing
technical_trust: reviewer trusted or questioned the deterministic validation approach
future_output_expectations: reviewer described expected graphic-output permutations
ux_readability: reviewer commented on non-technical readability or presentation
risk_or_gap: reviewer identified missing capabilities, product risks, or trust gaps
next_step: reviewer suggested what should be built next
```

## Severity scale

```text
blocking: feedback reveals the demo cannot be understood or run
high: feedback reveals a major trust, clarity, or product-positioning gap
medium: feedback identifies a useful improvement but does not block critique
low: feedback is cosmetic, preference-based, or wording-only
later: feedback belongs to the banked output-permutation or real-input tracks
```

## Triage workflow

```text
1. Read the reviewer context and scenario reviewed.
2. Confirm whether feedback applies to the current evidence-harness demo or the later output-permutation target.
3. Assign one primary feedback category.
4. Add any secondary categories if useful.
5. Assign severity.
6. Extract one actionable follow-up.
7. Mark whether the follow-up belongs to current-demo polish or a later gated milestone.
8. Do not expand scope automatically from feedback.
```

## Current-demo polish examples

These can be considered within the current evidence-harness track:

```text
- clearer README wording
- clearer demo narration
- better inspection order
- better run-folder explanation
- clearer explanation of needs_review
- clearer distinction between current evidence harness and future output generation
- better reviewer-facing docs
- better GitHub issue template wording
```

## Later-milestone examples

These should be banked for later gated milestones:

```text
- generated final graphics
- constraint-derived graphic output permutations
- real local image file input
- arbitrary local file loading
- image decoding
- pixel inspection
- CV/OCR provider integration
- unrestricted image generation
- unrestricted image editing
- automatic scoring
- automatic approval
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_current_evidence_harness_poc_demo_feedback_triage_guide.py
result: 5 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```

## Do not over-correct

```text
- Do not treat requests for generated graphics as a failure of the current evidence-harness demo.
- Do not treat needs_review as a negative outcome.
- Do not add new processing capabilities in response to feedback without a separate milestone.
- Do not add local image loading, network fetch, image decoding, CV/OCR, unrestricted generation, or automatic approval from triage alone.
```

## Suggested triage note format

```text
source:
reviewer:
scenario:
primary_category:
secondary_categories:
severity:
current_demo_or_later_track:
summary:
actionable_follow_up:
recommended_next_step:
```

## Local verification

```powershell
git pull --rebase origin phase-1-cli-tooling
pytest tests/test_current_evidence_harness_poc_demo_feedback_triage_guide.py
```
