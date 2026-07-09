# Intake Foundation Exit Review v1

## Status

```text
milestone: Intake Foundation Exit Review v1
status: implementation-complete-pending-test
started_on: 2026-07-09
previous_gate: Candidate Intake Review Packet v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Review the completed fixture-only real-candidate intake metadata foundation before any image bytes are loaded or decoded.

This milestone does not implement image loading, file opening, artifact download, network fetch, image decoding, pixel inspection, computer vision, OCR, image generation, image editing, candidate scoring, report mutation, or approval automation.

## Review conclusion

```text
intake_foundation_status: fixture_only_intake_metadata_ready
real_image_byte_loading_status: not_started
image_decoding_status: not_started
pixel_inspection_status: not_started
network_fetch_status: blocked
computer_vision_integration_status: not_started
ocr_integration_status: not_started
candidate_scoring_status: not_started
approval_automation_status: not_changed
next_allowed_milestone: Candidate Image Byte Loading Design v1
```

## Completed intake capabilities

```text
[x] Real candidate image intake design exists.
[x] Candidate intake manifest contract exists.
[x] Candidate intake manifest fixtures exist.
[x] Candidate intake manifest discovery exists.
[x] Candidate intake review packet exists.
[x] Accepted reference types are limited to artifact_uri, local_file_path, and file_uri.
[x] HTTP/HTTPS and arbitrary network fetching remain blocked.
[x] Checksum and media-type expectations are documented.
[x] Intake metadata cannot approve candidates.
[x] Intake review packets cannot approve candidates.
```

## Current intake commands

```powershell
cos-graphics-candidates intake-list
cos-graphics-candidates intake-show perseverance
cos-graphics-candidates intake-show supra_2jz_gte_twin_turbo
cos-graphics-candidates intake-review-packet perseverance
cos-graphics-candidates intake-review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-intake-review-packet.json intake-review-packet perseverance
```

## What intake metadata can safely do

```text
- Represent future candidate image intake metadata.
- Validate static intake manifest fixtures.
- Discover intake manifest summaries.
- Resolve intake manifests by manifest key, contract key, candidate id, or manifest id.
- Summarize reference type, media type, checksum metadata, and source metadata.
- Summarize no-network and non-approval policy guardrails.
- Produce human-facing intake review packets.
- Preserve needs_review as the default decision.
- Preserve approval_allowed false.
```

## What remains blocked

```text
- Real image byte loading.
- Local file opening.
- Artifact download.
- Remote or network fetch.
- Image decoding.
- Pixel inspection.
- Computer-vision provider integration.
- OCR provider integration.
- Image generation integration.
- Image editing integration.
- Candidate scoring.
- Source report mutation.
- Automatic approval.
```

## Exit decision

```text
decision: exit_fixture_only_intake_metadata_after_verification
rationale: The project now has a complete fixture-only intake metadata path from intake design to manifest contract, manifest fixtures, read-only discovery, and human-facing intake review packets. The next safe step is to design image byte loading boundaries, not implement image byte loading directly.
```

## Required next gate

Before any image bytes are loaded or decoded, the project must define byte-loading boundaries.

```text
required_before_image_byte_loading:
- Candidate Image Byte Loading Design v1
- explicit allowed roots for local_file_path and file_uri
- artifact_uri resolution policy
- maximum byte size policy
- checksum verification order
- media-type sniffing policy
- byte-count recording policy
- safe failure states
- confirmation that byte loading alone cannot approve candidates
```

## Verification command

```powershell
pytest tests/test_intake_foundation_exit_review.py
```

## Guardrails

```text
- Exit review only.
- No image bytes loaded.
- No image decoding.
- No network fetch.
- No CV/OCR provider choice.
- No image generation.
- No image editing.
- No candidate scoring.
- No approval automation change.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Intake foundation exit review doc exists.
[x] Fixture-only intake metadata-ready status is recorded.
[x] Completed intake capabilities are listed.
[x] Current intake commands are listed.
[x] Safe intake metadata capabilities are listed.
[x] Blocked image-handling and provider work is listed.
[x] Next allowed milestone is Candidate Image Byte Loading Design v1.
[x] Command reference updated with verification command.
[ ] Verification test result recorded.
```
