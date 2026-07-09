# Candidate Image Byte Loading Discovery v1

## Status

```text
milestone: Candidate Image Byte Loading Discovery v1
status: active
started_on: 2026-07-09
previous_gate: Candidate Image Byte Loading Contract v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Add read-only discovery for static candidate image byte-loading record fixtures.

This milestone lets users list and inspect byte-loading contract records without opening files, downloading artifacts, fetching network resources, loading image bytes, decoding images, inspecting pixels, scoring candidates, mutating reports, or approving candidates.

## Scope

```text
- Add candidate image byte-loading record helper module.
- Add cos-graphics-candidates byte-loading-list.
- Add cos-graphics-candidates byte-loading-show.
- Support text and JSON output.
- Support JSON file output.
- Preserve no image byte loading.
- Preserve no local file opening.
- Preserve no artifact download.
- Preserve no network fetch.
- Preserve no decoding, inspection, scoring, mutation, or approval.
- Add tests for discovery, CLI output, and guardrails.
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
pytest tests/test_candidate_image_byte_loading_discovery_cli.py
```

## CLI commands

```powershell
cos-graphics-candidates byte-loading-list
cos-graphics-candidates byte-loading-show perseverance
cos-graphics-candidates byte-loading-show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-byte-loading-records.json byte-loading-list
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Review Packet v1
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
- Read-only discovery only.
- Static byte-loading record fixtures only.
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
