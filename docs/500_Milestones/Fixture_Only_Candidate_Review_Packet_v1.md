# Fixture-only Candidate Review Packet v1

## Status

```text
milestone: Fixture-only Candidate Review Packet v1
status: implementation-complete-pending-test
started_on: 2026-07-08
previous_gate: Fixture-only Observation Evidence Merge v1 complete
track: Foundation Completion Track
baseline: 487 passed
```

## Purpose

Create a human-facing fixture-only candidate review packet that summarizes the manifest, manual observations, report binding, merged evidence, and decision guardrails for a candidate.

This milestone does not load real candidate images, score candidates, mutate report fixtures, or approve candidates. It produces a review packet that is safe to read, export, and hand to a reviewer before any real image ingestion work begins.

## Scope

```text
- Add fixture-only candidate review packet helper module.
- Add cos-graphics-candidates review-packet.
- Summarize candidate manifest identity.
- Summarize manual observation source and observation counts.
- Summarize observation-to-report binding status.
- Summarize merged evidence counts.
- Summarize decision guardrails.
- Preserve needs_review for the review packet.
- Preserve approval_allowed false.
- Support text and JSON output.
- Add tests for packet content, CLI output, and guardrails.
- Update candidate evaluation README.
- Update command reference with new available commands.
```

## Out of scope

```text
- No real image loading or decoding.
- No computer-vision provider integration.
- No OCR provider integration.
- No image generation.
- No image editing.
- No automatic approval.
- No candidate-evaluation scoring behavior change.
- No mutation of existing report fixtures.
```

## Implemented files

```text
docs/500_Milestones/Fixture_Only_Candidate_Review_Packet_v1.md
src/constraintos/candidate_review_packet.py
src/constraintos/candidate_manifests_cli.py
tests/test_candidate_review_packet.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Verification command

```powershell
pytest tests/test_candidate_review_packet.py
```

## CLI commands

```powershell
cos-graphics-candidates review-packet perseverance
cos-graphics-candidates review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-review-packet.json review-packet perseverance
```

## Review packet sections

```text
- candidate_identity
- manual_observations
- candidate_evaluation_report
- merged_evidence
- decision_guardrails
```

## Packet boundaries

```text
- Review packet mode is fixture_only.
- Candidate image references remain reference_only_not_loaded.
- Real image ingestion is not run.
- Computer vision is not run.
- OCR is not run.
- Image generation is not run.
- Approval automation is not run.
- Candidate scoring is not run.
- Source report mutation is not run.
- Recommendation remains needs_review.
- Approval remains disallowed.
```

## Guardrails

```text
- Review packet behavior is fixture-only.
- Candidate image references remain reference_only_not_loaded.
- Review packet cannot approve candidates.
- Source report fixtures are not mutated.
- Candidate scoring is not run.
- Recommendation remains needs_review.
- Approval remains disallowed.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Fixture-only candidate review packet helper module exists.
[x] CLI exposes cos-graphics-candidates review-packet.
[x] Candidate identity is summarized.
[x] Manual observation source and observation counts are summarized.
[x] Observation-to-report binding status is summarized.
[x] Merged evidence counts are summarized.
[x] Decision guardrails are summarized.
[x] Text output is supported.
[x] JSON output is supported.
[x] JSON file output is supported.
[x] Command reference updated in the same implementation slice.
[ ] Verification test result recorded.
```
