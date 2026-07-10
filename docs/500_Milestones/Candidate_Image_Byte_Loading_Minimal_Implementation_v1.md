# Candidate Image Byte Loading Minimal Implementation v1

## Status

```text
milestone: Candidate Image Byte Loading Minimal Implementation v1
status: complete
started_on: 2026-07-09
completed_on: 2026-07-09
previous_gate: Candidate Image Byte Loading Pre-Implementation Exit Review v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
latest_user_reported_candidate_image_byte_loading_minimal_implementation_test_result: 10 passed
latest_user_reported_candidate_image_byte_loading_minimal_implementation_test_result_on: 2026-07-09
```

## Purpose

Implement the smallest safe candidate image byte-loading path after the pre-implementation exit review.

This milestone implements an explicit, fixture-controlled byte-loading helper for `artifact_uri` references using an in-memory artifact registry adapter. It does not open local files, download artifacts, fetch network resources, decode images, inspect pixels, run computer vision, run OCR, score candidates, mutate reports, or approve candidates.

## Scope

```text
- Add minimal byte-loading helper module.
- Accept only validated byte-loading record dictionaries.
- Accept only explicit artifact registry byte sources.
- Require artifact:// references for the minimal implementation path.
- Reject HTTP and HTTPS references.
- Reject missing artifacts with safe failure records.
- Enforce expected byte count before reporting success.
- Enforce max_candidate_image_bytes.
- Compute sha256 over exact loaded bytes.
- Compare computed sha256 against manifest image_sha256.
- Sniff media type from bytes without decoding the image.
- Compare declared media_type against sniffed media type.
- Return immutable result dictionaries.
- Preserve approval_allowed false.
- Preserve image_decoded false.
- Preserve candidate_scoring_ran false.
- Preserve source_report_mutation_ran false.
- Preserve approval_automation_ran false.
- Add tests for success and safe failure paths.
- Update candidate evaluation README.
- Update command reference with verification command.
```

## Out of scope

```text
- No local file opening.
- No artifact download.
- No remote/network fetch.
- No file_uri implementation.
- No local_file_path implementation.
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

## Implemented files

```text
docs/500_Milestones/Candidate_Image_Byte_Loading_Minimal_Implementation_v1.md
src/constraintos/candidate_image_byte_loader.py
tests/test_candidate_image_byte_loading_minimal_implementation.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Minimal implementation boundary

```text
entry_point: load_candidate_image_bytes_minimal
accepted_reference_type: artifact_uri
artifact_source: explicit in-memory artifact registry adapter
network_fetch_allowed: false
implicit_cloud_download_allowed: false
local_file_opening_allowed: false
artifact_download_allowed: false
image_decoding_allowed: false
approval_allowed: false
```

## Result states

```text
success:
  image_bytes_loaded: true
  local_file_opened: false
  artifact_downloaded: false
  network_fetch_ran: false
  checksum_matches: true
  media_type_matches: true
  image_decoded: false
  candidate_scoring_ran: false
  approval_allowed: false

safe_failure:
  image_bytes_loaded: false
  local_file_opened: false
  artifact_downloaded: false
  network_fetch_ran: false
  image_decoded: false
  candidate_scoring_ran: false
  approval_allowed: false
  initial_decision: intake_failed
```

## Failure codes

```text
- unsupported_reference_type
- network_reference_rejected
- artifact_not_found
- expected_byte_count_exceeds_limit
- loaded_byte_count_mismatch
- loaded_byte_count_exceeds_limit
- checksum_mismatch
- unsupported_or_unknown_media_type
- media_type_mismatch
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Minimal CLI v1
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
pytest tests/test_candidate_image_byte_loading_minimal_implementation.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_candidate_image_byte_loading_minimal_implementation.py
result: 10 passed
reported_on: 2026-07-09
assistant_ran_tests: false
```

## Guardrails

```text
- Minimal byte-loading helper only.
- Explicit in-memory artifact registry only.
- No local file opening.
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

## Done criteria

```text
[x] Minimal byte-loading helper module exists.
[x] Minimal helper accepts explicit artifact registry byte sources.
[x] Minimal helper rejects HTTP and HTTPS references.
[x] Minimal helper rejects non-artifact references.
[x] Minimal helper rejects missing artifacts safely.
[x] Minimal helper enforces expected byte count.
[x] Minimal helper enforces max_candidate_image_bytes.
[x] Minimal helper computes sha256 over exact loaded bytes.
[x] Minimal helper compares declared and sniffed media type.
[x] Minimal helper returns immutable result dictionaries.
[x] Minimal helper keeps image_decoded false.
[x] Minimal helper keeps candidate_scoring_ran false.
[x] Minimal helper keeps source_report_mutation_ran false.
[x] Minimal helper keeps approval_allowed false.
[x] README updated.
[x] Command reference updated with verification command.
[x] Verification test result recorded.
```

## Handoff notes

```text
- Candidate Image Byte Loading Minimal Implementation v1 is complete.
- The minimal byte-loading helper can load fixture-controlled artifact bytes through an explicit in-memory artifact registry adapter.
- The helper validates byte count, max byte limit, sha256, and signature-based media type without decoding the image.
- The helper rejects network references, non-artifact references, missing artifacts, checksum mismatches, media-type mismatches, and oversize candidates with safe failure records.
- This milestone did not implement local file opening, artifact download, network fetch, file_uri loading, local_file_path loading, image decoding, pixel inspection, CV/OCR integration, image generation, image editing, candidate scoring, report mutation, or approval automation.
- The next milestone should be Candidate Image Byte Loading Minimal CLI v1.
```
