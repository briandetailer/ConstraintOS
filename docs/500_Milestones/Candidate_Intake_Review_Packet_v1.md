# Candidate Intake Review Packet v1

## Status

```text
milestone: Candidate Intake Review Packet v1
status: active
started_on: 2026-07-09
previous_gate: Candidate Intake Manifest Discovery v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Create a human-facing fixture-only intake review packet for candidate intake manifest metadata and guardrails.

This milestone packages intake manifest discovery into a readable review packet. It does not load, open, download, decode, inspect, score, mutate, or approve candidate images.

## Scope

```text
- Add candidate intake review packet helper module.
- Add cos-graphics-candidates intake-review-packet.
- Summarize intake candidate identity.
- Summarize reference metadata.
- Summarize policy snapshot.
- Summarize intake boundaries.
- Summarize approval blockers.
- Preserve needs_review and approval_allowed false.
- Support text and JSON output.
- Support JSON file output.
- Add tests for packet content, CLI output, and guardrails.
- Update candidate evaluation README.
- Update command reference with new available commands.
```

## Out of scope

```text
- No image bytes loaded.
- No local file opening.
- No artifact download.
- No remote/network fetch.
- No image decoding.
- No pixel inspection.
- No computer-vision provider integration.
- No OCR provider integration.
- No image generation.
- No image editing.
- No candidate scoring.
- No report mutation.
- No approval automation change.
```

## Verification command

```powershell
pytest tests/test_candidate_intake_review_packet.py
```

## CLI commands

```powershell
cos-graphics-candidates intake-review-packet perseverance
cos-graphics-candidates intake-review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-intake-review-packet.json intake-review-packet perseverance
```

## Required next gate

```text
recommended_next_milestone: Intake Foundation Exit Review v1
blocked_until_later:
- image byte loading implementation
- image decoding implementation
- computer-vision provider integration
- OCR provider integration
- image generation integration
- image editing integration
- candidate scoring
- approval automation change
```

## Guardrails

```text
- Fixture-only intake review packet.
- No image bytes loaded.
- No image decoding.
- No network fetch.
- No CV/OCR provider choice.
- No candidate scoring.
- No approval automation change.
- Do not claim tests passed unless actually run.
```
