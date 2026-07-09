# Fixture-only Candidate Review Packet v1

## Status

```text
milestone: Fixture-only Candidate Review Packet v1
status: active
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
