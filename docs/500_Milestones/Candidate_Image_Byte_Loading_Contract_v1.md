# Candidate Image Byte Loading Contract v1

## Status

```text
milestone: Candidate Image Byte Loading Contract v1
status: complete
started_on: 2026-07-09
completed_on: 2026-07-09
previous_gate: Candidate Image Byte Loading Design v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
latest_user_reported_candidate_image_byte_loading_contract_test_result: 10 passed
latest_user_reported_candidate_image_byte_loading_contract_test_result_on: 2026-07-09
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

## Implemented files

```text
docs/500_Milestones/Candidate_Image_Byte_Loading_Contract_v1.md
examples/graphics/candidate_evaluation/candidate_image_byte_loading_record.schema.json
examples/graphics/candidate_evaluation/perseverance_candidate_image_byte_loading_record.fixture.json
examples/graphics/candidate_evaluation/supra_2jz_gte_candidate_image_byte_loading_record.fixture.json
tests/test_candidate_image_byte_loading_contract.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
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

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_candidate_image_byte_loading_contract.py
result: 10 passed
reported_on: 2026-07-09
assistant_ran_tests: false
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

## Done criteria

```text
[x] Candidate image byte-loading record schema exists.
[x] Perseverance byte-loading record fixture exists.
[x] Supra 2JZ-GTE byte-loading record fixture exists.
[x] Reference metadata snapshot is required.
[x] Byte-loading policy snapshot is required.
[x] Byte-loading result remains not_run_contract_only.
[x] Checksum, media-type, and byte-count result fields are null until implementation.
[x] Approval expectation keeps approval_allowed false.
[x] Command reference updated in the same implementation slice.
[x] Verification test result recorded.
```

## Handoff notes

```text
- Candidate Image Byte Loading Contract v1 is complete.
- Static byte-loading record schema and fixtures now exist for Perseverance and Supra 2JZ-GTE.
- Byte-loading records bind to candidate intake manifests and preserve reference metadata, byte-loading policy, not-run result fields, post-load boundaries, and non-approval expectations.
- Image byte loading, local file opening, artifact download, network fetch, image decoding, pixel inspection, CV/OCR integration, image generation, image editing, candidate scoring, report mutation, and approval automation remain blocked.
- The next milestone should be Candidate Image Byte Loading Discovery v1.
```
