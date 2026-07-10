# Candidate Image Byte Loading Minimal CLI v1

## Status

```text
milestone: Candidate Image Byte Loading Minimal CLI v1
status: active
started_on: 2026-07-09
previous_gate: Candidate Image Byte Loading Minimal Implementation v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Expose the minimal candidate image byte-loading helper through a narrow CLI without expanding byte-source permissions.

This milestone adds a dedicated helper-only CLI entry point for fixture-controlled `artifact://` bytes. It does not open local image files, download artifacts, fetch network resources, decode images, inspect pixels, run computer vision, run OCR, score candidates, mutate reports, or approve candidates.

## Scope

```text
- Add dedicated minimal byte-loading CLI module.
- Add console script for the minimal byte-loading CLI.
- Accept a byte-loading record reference.
- Accept fixture artifact bytes only through explicit hex input.
- Bind fixture bytes only to an explicit artifact URI.
- Reuse load_candidate_image_bytes_minimal.
- Emit JSON and text output.
- Support --output file writing for reports.
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
command: cos-graphics-byte-loader minimal
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

## User-facing commands

```powershell
cos-graphics-byte-loader minimal perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
cos-graphics-byte-loader --format json minimal perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
cos-graphics-byte-loader --format json --output reports/perseverance-byte-loader.json minimal perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Minimal CLI Review Packet v1
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
pytest tests/test_candidate_image_byte_loading_minimal_cli.py
```

## Guardrails

```text
- Dedicated minimal CLI only.
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
