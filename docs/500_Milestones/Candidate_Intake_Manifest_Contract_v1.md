# Candidate Intake Manifest Contract v1

## Status

```text
milestone: Candidate Intake Manifest Contract v1
status: complete
started_on: 2026-07-09
completed_on: 2026-07-09
previous_gate: Real Candidate Image Intake Design v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
latest_user_reported_candidate_intake_manifest_contract_test_result: 9 passed
latest_user_reported_candidate_intake_manifest_contract_test_result_on: 2026-07-09
```

## Purpose

Define the fixture-only contract for future intake-ready candidate image manifests.

This milestone turns the image-intake design rules into a manifest schema and static fixtures. It does not load image bytes, open local files, download artifacts, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Scope

```text
- Add candidate intake manifest schema.
- Add Perseverance intake manifest fixture.
- Add Supra 2JZ-GTE intake manifest fixture.
- Require future accepted reference types only.
- Require checksum and media-type metadata before future intake.
- Require intake state to remain intake_pending or reference_only_not_loaded.
- Require all intake fixtures to keep approval_allowed false.
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
docs/500_Milestones/Candidate_Intake_Manifest_Contract_v1.md
examples/graphics/candidate_evaluation/candidate_intake_manifest.schema.json
examples/graphics/candidate_evaluation/perseverance_candidate_intake_manifest.fixture.json
examples/graphics/candidate_evaluation/supra_2jz_gte_candidate_intake_manifest.fixture.json
tests/test_candidate_intake_manifest_contract.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Contract fields

```text
candidate_intake_manifest:
  id
  version
  domain
  status
  candidate_id
  intake_state
  submitted_at

contract_binding:
  contract_key
  contract_required
  source_contract_id

candidate_reference:
  reference_type
  reference
  reference_status
  media_type
  image_sha256

intake_policy_snapshot:
  accepted_reference_types
  accepted_media_types
  forbidden_reference_behaviors
  checksum_required
  network_fetch_allowed

intake_boundary:
  image_bytes_loaded
  image_decoded
  pixel_inspection_ran
  computer_vision_ran
  ocr_ran
  candidate_scoring_ran
  approval_automation_ran

approval_expectation:
  initial_decision
  uncertainty_default
  approval_allowed
```

## Verification command

```powershell
pytest tests/test_candidate_intake_manifest_contract.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_candidate_intake_manifest_contract.py
result: 9 passed
reported_on: 2026-07-09
assistant_ran_tests: false
```

## Required next gate

```text
recommended_next_milestone: Candidate Intake Manifest Discovery v1
blocked_until_later:
- image byte loading implementation
- image decoding implementation
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
- Fixture-only manifests.
- No image bytes loaded.
- No image decoding.
- No network fetch.
- No CV/OCR provider choice.
- No candidate scoring.
- No approval automation change.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Candidate intake manifest schema exists.
[x] Perseverance candidate intake manifest fixture exists.
[x] Supra 2JZ-GTE candidate intake manifest fixture exists.
[x] Accepted reference types are limited to artifact_uri, local_file_path, and file_uri.
[x] Checksum and media-type metadata are required.
[x] Intake boundaries keep image loading, decoding, inspection, scoring, mutation, and approval disabled.
[x] Approval expectation keeps approval_allowed false.
[x] Command reference updated in the same implementation slice.
[x] Verification test result recorded.
```

## Handoff notes

```text
- Candidate Intake Manifest Contract v1 is complete.
- Intake-ready candidate manifest fixtures now exist for Perseverance and Supra 2JZ-GTE.
- Intake manifests require accepted reference type, media type, image_sha256, policy snapshot, intake boundary, and approval expectation.
- Image loading, image decoding, pixel inspection, CV/OCR integration, image generation, image editing, candidate scoring, report mutation, and approval automation remain blocked.
- The next milestone should be Candidate Intake Manifest Discovery v1.
```
