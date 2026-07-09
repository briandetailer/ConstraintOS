# Candidate Image Byte Loading Design v1

## Status

```text
milestone: Candidate Image Byte Loading Design v1
status: implementation-complete-pending-test
started_on: 2026-07-09
previous_gate: Intake Foundation Exit Review v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Define the policy boundaries for future candidate image byte loading before any bytes are actually loaded.

This milestone is design-only. It does not implement image byte loading, local file opening, artifact download, network fetch, image decoding, pixel inspection, computer vision, OCR, image generation, image editing, candidate scoring, report mutation, or approval automation.

## Scope

```text
- Define allowed roots for future local_file_path and file_uri loading.
- Define artifact_uri resolution policy.
- Define maximum byte size policy.
- Define checksum verification order.
- Define media-type sniffing policy.
- Define byte-count recording policy.
- Define safe failure states.
- Confirm byte loading alone cannot approve candidates.
- Add machine-readable byte-loading design fixture.
- Add tests for byte-loading design guardrails.
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
docs/500_Milestones/Candidate_Image_Byte_Loading_Design_v1.md
examples/graphics/candidate_evaluation/candidate_image_byte_loading.design.json
tests/test_candidate_image_byte_loading_design.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Allowed roots policy

```text
local_file_path:
  allowed_roots:
  - ./external-candidates/
  - ./runs/manual-candidates/
  required_behavior:
  - normalize path before loading
  - reject path traversal
  - reject absolute paths unless explicitly allowlisted later
  - reject paths outside allowed roots

file_uri:
  allowed_roots:
  - file:///workspace/external-candidates/
  - file:///workspace/runs/manual-candidates/
  required_behavior:
  - normalize URI before loading
  - reject path traversal
  - reject hosts other than empty or localhost
  - reject paths outside allowed roots
```

## Artifact URI policy

```text
artifact_uri:
  status: design_only
  allowed_scheme: artifact://
  resolution: internal_artifact_registry_required_later
  network_fetch_allowed: false
  implicit_cloud_download_allowed: false
  missing_artifact_behavior: intake_failed
```

## Maximum byte size policy

```text
max_candidate_image_bytes: 25000000
oversize_behavior: intake_failed
approval_allowed: false
```

## Checksum verification order

```text
1. Resolve reference metadata without loading bytes.
2. Confirm reference type is allowed.
3. Confirm candidate has image_sha256 metadata.
4. Load bytes only in a future implementation.
5. Compute sha256 from loaded bytes.
6. Compare computed sha256 to image_sha256.
7. Reject or fail intake on mismatch.
8. Do not decode image until checksum passes.
```

## Media-type sniffing policy

```text
accepted_media_types:
- image/png
- image/jpeg
- image/webp

required_behavior:
- declared media_type must be present before future loading.
- sniffed media type must be recorded after future loading.
- declared and sniffed media types must agree.
- unsupported or mismatched media type must fail intake.
- media-type validation cannot approve a candidate.
```

## Byte-count recording policy

```text
required_future_records:
- declared_expected_byte_count
- actual_loaded_byte_count
- max_candidate_image_bytes
- byte_count_within_limit

byte_count_success_can_approve: false
```

## Failure states

```text
reference_type_not_allowed:
  decision: intake_failed
  approval_allowed: false

outside_allowed_root:
  decision: intake_failed
  approval_allowed: false

path_traversal_detected:
  decision: intake_failed
  approval_allowed: false

artifact_not_found:
  decision: intake_failed
  approval_allowed: false

missing_checksum:
  decision: needs_review
  approval_allowed: false

checksum_mismatch:
  decision: intake_failed
  approval_allowed: false

oversize_candidate:
  decision: intake_failed
  approval_allowed: false

unsupported_media_type:
  decision: intake_failed
  approval_allowed: false

media_type_mismatch:
  decision: intake_failed
  approval_allowed: false

unreadable_candidate:
  decision: needs_review
  approval_allowed: false
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Contract v1
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

## Verification command

```powershell
pytest tests/test_candidate_image_byte_loading_design.py
```

## Guardrails

```text
- Design only.
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
[x] Candidate image byte loading design doc exists.
[x] Machine-readable byte-loading design fixture exists.
[x] Allowed roots policy is defined.
[x] Artifact URI resolution policy is defined.
[x] Maximum byte size policy is defined.
[x] Checksum verification order is defined.
[x] Media-type sniffing policy is defined.
[x] Byte-count recording policy is defined.
[x] Failure states are defined and cannot approve.
[x] Next gate is Candidate Image Byte Loading Contract v1.
[x] Command reference updated in the same implementation slice.
[ ] Verification test result recorded.
```
