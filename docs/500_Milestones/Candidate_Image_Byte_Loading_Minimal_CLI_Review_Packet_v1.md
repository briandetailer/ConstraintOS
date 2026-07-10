# Candidate Image Byte Loading Minimal CLI Review Packet v1

## Status

```text
milestone: Candidate Image Byte Loading Minimal CLI Review Packet v1
status: active
started_on: 2026-07-09
previous_gate: Candidate Image Byte Loading Minimal CLI v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Add a human-facing review packet for the dedicated minimal byte-loading CLI result.

This milestone adds a review-packet subcommand to the dedicated `cos-graphics-byte-loader` CLI. The review packet wraps the helper-only byte-loading result with explicit safety sections and approval blockers. It does not open local image files, download artifacts, fetch network resources, decode images, inspect pixels, run computer vision, run OCR, score candidates, mutate reports, or approve candidates.

## Scope

```text
- Add review-packet mode to the dedicated minimal byte-loader CLI.
- Reuse the minimal CLI payload path.
- Accept fixture artifact bytes only through explicit hex input.
- Bind fixture bytes only to an explicit artifact URI.
- Preserve JSON and text output.
- Support --output file writing for review packets.
- Add review sections for CLI invocation boundary.
- Add review sections for byte-loading result.
- Add review sections for safety boundaries.
- Add review sections for decision guardrails.
- Preserve no local image file opening.
- Preserve no artifact download.
- Preserve no network fetch.
- Preserve no image decoding.
- Preserve no candidate scoring.
- Preserve no source report mutation.
- Preserve no approval automation.
- Update README.
- Update command reference.
```

## Out of scope

```text
- No integration into broad candidate CLI.
- No local_file_path byte loading.
- No file_uri byte loading.
- No local image file opening.
- No artifact download.
- No network fetch.
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

## CLI boundary

```text
command: cos-graphics-byte-loader review-packet
byte_source: explicit fixture hex argument
artifact_binding: explicit --fixture-artifact-uri
record_source: validated byte-loading record fixture
local_image_file_opening: false
artifact_download: false
network_fetch: false
image_decoding: false
candidate_scoring: false
approval_allowed: false
```

## Review packet sections

```text
- cli_invocation_boundary
- byte_loading_result
- safety_boundaries
- decision_guardrails
```

## User-facing commands

```powershell
cos-graphics-byte-loader review-packet perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
cos-graphics-byte-loader --format json review-packet perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
cos-graphics-byte-loader --format json --output reports/perseverance-byte-loader-review-packet.json review-packet perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Minimal CLI Exit Review v1
blocked_until_later:
- local_file_path byte loading
- file_uri byte loading
- artifact download
- network fetch
- image decoding implementation
- pixel inspection
- computer-vision provider integration
- OCR provider integration
- image generation integration
- image editing integration
- candidate scoring
- approval automation change
```

## Verification command

```powershell
pytest tests/test_candidate_image_byte_loading_minimal_cli_review_packet.py
```

## Guardrails

```text
- Dedicated minimal CLI review packet only.
- Explicit fixture hex bytes only.
- Explicit fixture artifact URI only.
- No local image file opening.
- No artifact download.
- No network fetch.
- No image decoding.
- No CV/OCR provider choice.
- No image generation.
- No image editing.
- No candidate scoring.
- No report mutation.
- No approval automation change.
- Do not claim tests passed unless actually run.
```
