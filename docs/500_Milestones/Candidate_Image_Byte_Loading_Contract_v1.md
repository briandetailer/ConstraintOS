# Candidate Image Byte Loading Contract v1

## Status

```text
milestone: Candidate Image Byte Loading Contract v1
status: active
started_on: 2026-07-09
previous_gate: Candidate Image Byte Loading Design v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Define the static contract for future candidate image byte-loading records before any byte-loading implementation exists.

This milestone turns the byte-loading design into a schema and static fixture records. It does not implement image byte loading, local file opening, artifact download, network fetch, image decoding, pixel inspection, computer vision, OCR, image generation, image editing, candidate scoring, report mutation, or approval automation.

## Scope

```text
- Add candidate image byte-loading record schema.
- Add Perseverance byte-loading record fixture.
- Add Supra 2JZ-GTE byte-loading record fixture.
- Require reference metadata snapshot.
- Require byte-loading policy snapshot.
- Require byte-loading result to remain not_run_contract_only.
- Require checksum, media-type, and byte-count result fields to be not_run or null.
- Require all byte-loading fixtures to keep approval_allowed false.
- Add tests for schema, fixtures, and guardrails.
- Update candidate evaluation README.
- Update command reference with verification command.
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

## Contract fields

```text
candidate_image_byte_loading_record:
  id
  version
  domain
  status
  candidate_id
  byte_loading_state
  recorded_at

contract_binding:
  contract_key
  source_contract_id
  candidate_intake_manifest_id

reference_snapshot:
  reference_type
  reference
  media_type
  image_sha256
  expected_byte_count

byte_loading_policy_snapshot:
  allowed_local_roots
  allowed_file_uri_roots
  artifact_uri_resolution
  max_candidate_image_bytes
  network_fetch_allowed
  implicit_cloud_download_allowed

byte_loading_result:
  image_bytes_loaded
  local_file_opened
  artifact_downloaded
  network_fetch_ran
  actual_loaded_byte_count
  computed_sha256
  sniffed_media_type
  byte_count_within_limit
  checksum_matches
  media_type_matches

post_load_boundary:
  image_decoded
  pixel_inspection_ran
  computer_vision_ran
  ocr_ran
  candidate_scoring_ran
  source_report_mutation_ran
  approval_automation_ran

approval_expectation:
  initial_decision
  uncertainty_default
  approval_allowed
```

## Verification command

```powershell
pytest tests/test_candidate_image_byte_loading_contract.py
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Discovery v1
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
- Contract only.
- Static fixture records only.
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
