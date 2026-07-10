# Candidate Image Byte Loading Fixture Registry Failure Matrix v1

## Status

```text
milestone: Candidate Image Byte Loading Fixture Registry Failure Matrix v1
status: implementation-complete-pending-test
started_on: 2026-07-10
previous_gate: Candidate Image Byte Loading Fixture Registry Exit Review v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Add fixture-only failure coverage for the deterministic candidate image fixture artifact registry before any broader candidate image byte-source expansion begins.

This milestone confirms that invalid registry descriptors fail closed and do not open local image files, load arbitrary filesystem paths, download artifacts, fetch network resources, decode images, inspect pixels, run computer vision, run OCR, score candidates, mutate reports, or approve candidates.

## Scope

```text
- Add fixture registry failure matrix fixture.
- Cover invalid sha256.
- Cover invalid byte count.
- Cover invalid media type.
- Cover invalid artifact URI.
- Cover duplicate artifact ID.
- Cover duplicate artifact URI.
- Cover descriptor mutability violation.
- Cover local file opening guardrail violation.
- Cover network fetch guardrail violation.
- Cover image decoding guardrail violation.
- Cover approval guardrail violation.
- Assert failure cases do not expose bytes through InMemoryArtifactRegistry.
- Assert success cases still cannot approve candidates.
- Update tests.
- Update README.
- Update command reference.
```

## Out of scope

```text
- No local image file opening.
- No local_file_path byte loading.
- No file_uri byte loading.
- No artifact download.
- No network fetch.
- No implicit cloud download.
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
docs/500_Milestones/Candidate_Image_Byte_Loading_Fixture_Registry_Failure_Matrix_v1.md
examples/graphics/candidate_evaluation/candidate_image_fixture_artifact_registry_failure_matrix.fixture.json
tests/test_candidate_image_byte_loading_fixture_registry_failure_matrix.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Failure matrix boundary

```text
matrix_source: fixture-only JSON case list
base_registry_source: deterministic fixture artifact registry
failure_execution: in-memory mutation only
bytes_exposed_on_failure: false
local_image_file_opening: false
artifact_download: false
network_fetch: false
image_decoding: false
candidate_scoring: false
approval_allowed: false
```

## Failure cases

```text
- invalid_sha256
- invalid_byte_count
- invalid_media_type
- invalid_artifact_uri
- duplicate_artifact_id
- duplicate_artifact_uri
- descriptor_mutability_violation
- local_file_opening_guardrail_violation
- network_fetch_guardrail_violation
- image_decoding_guardrail_violation
- approval_guardrail_violation
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Fixture Registry Failure Review Packet v1
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
pytest tests/test_candidate_image_byte_loading_fixture_registry_failure_matrix.py
```

## Guardrails

```text
- Fixture registry failure matrix only.
- In-memory fixture mutations only.
- No new byte-loading source added.
- No local image file opening.
- No local_file_path loading.
- No file_uri loading.
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
[x] Fixture registry failure matrix fixture exists.
[x] Invalid sha256 is covered.
[x] Invalid byte count is covered.
[x] Invalid media type is covered.
[x] Invalid artifact URI is covered.
[x] Duplicate artifact ID is covered.
[x] Duplicate artifact URI is covered.
[x] Descriptor mutability violation is covered.
[x] Local file opening guardrail violation is covered.
[x] Network fetch guardrail violation is covered.
[x] Image decoding guardrail violation is covered.
[x] Approval guardrail violation is covered.
[x] Failure cases do not expose bytes through InMemoryArtifactRegistry.
[x] Success case still cannot approve candidates.
[x] README updated.
[x] Command reference updated.
[ ] Verification test result recorded.
```
