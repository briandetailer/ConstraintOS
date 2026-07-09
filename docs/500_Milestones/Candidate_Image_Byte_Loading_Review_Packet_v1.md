# Candidate Image Byte Loading Review Packet v1

## Status

```text
milestone: Candidate Image Byte Loading Review Packet v1
status: active
started_on: 2026-07-09
previous_gate: Candidate Image Byte Loading Discovery v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Create a human-facing fixture-only review packet for candidate image byte-loading record metadata and guardrails.

This milestone packages byte-loading record discovery into a readable review packet. It does not open files, download artifacts, fetch network resources, load image bytes, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Scope

```text
- Add candidate image byte-loading review packet helper module.
- Add cos-graphics-candidates byte-loading-review-packet.
- Summarize byte-loading record identity.
- Summarize intake manifest binding.
- Summarize reference metadata.
- Summarize byte-loading policy snapshot.
- Summarize not-run byte-loading result fields.
- Summarize post-load boundaries.
- Summarize approval blockers.
- Preserve needs_review and approval_allowed false.
- Support text and JSON output.
- Support JSON file output.
- Add tests for packet content, CLI output, and guardrails.
- Update candidate evaluation README.
- Update command reference with new available command.
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
pytest tests/test_candidate_image_byte_loading_review_packet.py
```

## CLI commands

```powershell
cos-graphics-candidates byte-loading-review-packet perseverance
cos-graphics-candidates byte-loading-review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-byte-loading-review-packet.json byte-loading-review-packet perseverance
```

## Review packet sections

```text
- byte_loading_record_identity
- intake_manifest_binding
- reference_metadata
- byte_loading_policy_snapshot
- byte_loading_result
- post_load_boundaries
- decision_guardrails
```

## Required next gate

```text
recommended_next_milestone: Byte Loading Foundation Exit Review v1
blocked_until_later:
- image byte loading implementation
- image decoding implementation
- pixel inspection
- computer-vision provider integration
- OCR provider integration
- image generation integration
- image editing integration
- candidate scoring
- approval automation change
```

## Guardrails

```text
- Fixture-only byte-loading review packet.
- No image bytes loaded.
- No local file opening.
- No artifact download.
- No network fetch.
- No image decoding.
- No CV/OCR provider choice.
- No candidate scoring.
- No approval automation change.
- Do not claim tests passed unless actually run.
```
