# Candidate Image Byte Loading Implementation Contract v1

## Status

```text
milestone: Candidate Image Byte Loading Implementation Contract v1
status: active
started_on: 2026-07-09
previous_gate: Candidate Image Byte Loading Implementation Design v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Define the future runtime contract for candidate image byte-loading attempts before any byte-loading implementation is written.

This milestone converts the implementation design into a schema and static contract fixture for future byte-loading attempt results. It does not implement image byte loading, local file opening, artifact download, network fetch, image decoding, pixel inspection, computer vision, OCR, image generation, image editing, candidate scoring, report mutation, or approval automation.

## Scope

```text
- Add candidate image byte-loading implementation contract schema.
- Add static implementation contract fixture.
- Define future input binding fields.
- Define future policy enforcement result fields.
- Define future reference resolution result fields.
- Define future byte-loading result envelope.
- Define future checksum, size, and media-type result fields.
- Define safe failure result fields.
- Preserve design-only and approval_allowed false.
- Add tests for implementation contract guardrails.
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

## Contract sections

```text
candidate_image_byte_loading_implementation_contract:
  id
  version
  domain
  status
  contract_state

input_binding:
  source_byte_loading_record_schema
  source_byte_loading_record_fixture_required
  source_intake_manifest_required
  explicit_artifact_registry_adapter_required
  explicit_allowed_root_policy_required

policy_enforcement_result_contract:
  reference_type_allowed
  allowed_root_checked
  path_normalized
  traversal_rejected
  absolute_path_policy_checked
  network_fetch_allowed
  implicit_cloud_download_allowed

reference_resolution_result_contract:
  reference_resolved
  resolved_reference_kind
  artifact_descriptor_required
  resolved_byte_source_mutable

byte_loading_result_contract:
  image_bytes_loaded
  local_file_opened
  artifact_downloaded
  network_fetch_ran
  actual_loaded_byte_count
  computed_sha256
  sniffed_media_type

validation_result_contract:
  byte_count_within_limit
  checksum_matches
  media_type_matches
  safe_to_decode

safe_failure_contract:
  failure_code
  failure_reason
  initial_decision
  approval_allowed
```

## Verification command

```powershell
pytest tests/test_candidate_image_byte_loading_implementation_contract.py
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Pre-Implementation Exit Review v1
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
- Implementation contract only.
- Static contract fixture only.
- No image bytes loaded.
- No local file opening.
- No artifact download.
- No network fetch.
- No image decoding.
- No CV/OCR provider choice.
- No image generation.
- No image editing.
- No candidate scoring.
- No approval automation change.
- Do not claim tests passed unless actually run.
```
