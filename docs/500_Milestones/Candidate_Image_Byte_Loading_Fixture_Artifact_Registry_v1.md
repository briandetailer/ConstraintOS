# Candidate Image Byte Loading Fixture Artifact Registry v1

## Status

```text
milestone: Candidate Image Byte Loading Fixture Artifact Registry v1
status: complete
started_on: 2026-07-09
completed_on: 2026-07-09
previous_gate: Candidate Image Byte Loading Minimal CLI Exit Review v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
latest_user_reported_candidate_image_byte_loading_fixture_artifact_registry_test_result: 9 passed
latest_user_reported_candidate_image_byte_loading_fixture_artifact_registry_test_result_on: 2026-07-09
```

## Purpose

Add a deterministic fixture artifact registry for candidate image byte-loading tests and CLI runs before any filesystem or network byte source is allowed.

This milestone replaces ad hoc fixture hex arguments as the default byte source with a schema-validated fixture registry. It keeps byte sources fixture-controlled and does not open local image files, download artifacts, fetch network resources, decode images, inspect pixels, run computer vision, run OCR, score candidates, mutate reports, or approve candidates.

## Scope

```text
- Add fixture artifact registry schema.
- Add deterministic fixture artifact registry fixture.
- Add fixture artifact registry loader module.
- Require deterministic artifact IDs.
- Require artifact:// URIs.
- Require immutable fixture byte descriptors.
- Require expected sha256 before byte exposure.
- Require expected byte count before byte exposure.
- Require declared media type before byte exposure.
- Validate fixture bytes against byte count, sha256, and signature-based media type before exposing bytes.
- Convert validated fixture registry entries into the existing InMemoryArtifactRegistry adapter.
- Update byte-loading record fixtures to align with deterministic fixture artifact metadata.
- Update byte-loading record schema to allow deterministic fixture registry metadata.
- Update dedicated byte-loader CLI to use the default fixture artifact registry when explicit fixture hex is not supplied.
- Preserve explicit fixture hex override for focused tests.
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
docs/500_Milestones/Candidate_Image_Byte_Loading_Fixture_Artifact_Registry_v1.md
examples/graphics/candidate_evaluation/candidate_image_fixture_artifact_registry.schema.json
examples/graphics/candidate_evaluation/candidate_image_fixture_artifact_registry.fixture.json
src/constraintos/candidate_image_fixture_artifact_registry.py
examples/graphics/candidate_evaluation/perseverance_candidate_image_byte_loading_record.fixture.json
examples/graphics/candidate_evaluation/supra_2jz_gte_candidate_image_byte_loading_record.fixture.json
examples/graphics/candidate_evaluation/candidate_image_byte_loading_record.schema.json
src/constraintos/candidate_image_byte_loader_cli.py
tests/test_candidate_image_byte_loading_contract.py
tests/test_candidate_image_byte_loading_fixture_artifact_registry.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Fixture registry boundary

```text
registry_source: schema-validated JSON fixture
artifact_source: inline deterministic fixture hex bytes
accepted_reference_type: artifact_uri
required_uri_scheme: artifact://
local_image_file_opening: false
artifact_download: false
network_fetch: false
image_decoding: false
candidate_scoring: false
approval_allowed: false
```

## CLI boundary

```text
command: cos-graphics-byte-loader minimal
new_default_byte_source: candidate_image_fixture_artifact_registry.fixture.json
explicit_fixture_hex_override: still_allowed
local_image_file_opening: false
artifact_download: false
network_fetch: false
image_decoding: false
candidate_scoring: false
approval_allowed: false
```

## User-facing commands

```powershell
cos-graphics-byte-loader minimal perseverance
cos-graphics-byte-loader review-packet perseverance
cos-graphics-byte-loader --format json minimal perseverance
cos-graphics-byte-loader --format json review-packet perseverance
cos-graphics-byte-loader --format json --output reports/perseverance-byte-loader.json minimal perseverance
cos-graphics-byte-loader --format json --output reports/perseverance-byte-loader-review-packet.json review-packet perseverance
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Fixture Registry Review Packet v1
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
pytest tests/test_candidate_image_byte_loading_fixture_artifact_registry.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_candidate_image_byte_loading_fixture_artifact_registry.py
result: 9 passed
reported_on: 2026-07-09
assistant_ran_tests: false
```

## Guardrails

```text
- Fixture artifact registry only.
- Deterministic fixture artifact IDs only.
- Immutable fixture byte descriptors only.
- Expected sha256 required before byte exposure.
- Expected byte count required before byte exposure.
- Declared media type required before byte exposure.
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

## Done criteria

```text
[x] Fixture artifact registry schema exists.
[x] Deterministic fixture artifact registry fixture exists.
[x] Fixture artifact registry loader module exists.
[x] Deterministic artifact IDs are required.
[x] artifact:// URIs are required.
[x] Immutable fixture byte descriptors are required.
[x] Expected sha256 is required before byte exposure.
[x] Expected byte count is required before byte exposure.
[x] Declared media type is required before byte exposure.
[x] Fixture bytes are validated against byte count, sha256, and signature-based media type before exposure.
[x] Validated fixture registry entries convert into InMemoryArtifactRegistry.
[x] Byte-loading record fixtures align with deterministic fixture artifact metadata.
[x] Byte-loading record schema allows deterministic fixture registry metadata.
[x] Dedicated byte-loader CLI uses the default fixture artifact registry when explicit fixture hex is not supplied.
[x] Explicit fixture hex override remains available.
[x] README updated.
[x] Command reference updated.
[x] Verification test result recorded.
```

## Handoff notes

```text
- Candidate Image Byte Loading Fixture Artifact Registry v1 is complete.
- The default byte source for cos-graphics-byte-loader minimal and review-packet is candidate_image_fixture_artifact_registry.fixture.json.
- The registry remains fixture-only and exposes bytes only after descriptor validation.
- Registry descriptors require deterministic artifact IDs, artifact:// URIs, immutable descriptors, expected sha256, expected byte count, declared media type, no local file opening, no artifact download, no network fetch, no image decoding, and no approval from byte-loading success.
- Explicit fixture hex override remains available for focused tests.
- The next milestone should be Candidate Image Byte Loading Fixture Registry Review Packet v1.
- local_file_path byte loading, file_uri byte loading, artifact download, network fetch, image decoding, pixel inspection, CV/OCR integration, image generation, image editing, candidate scoring, source report mutation, and approval automation remain blocked until later milestones.
```
