# Real Candidate Image Intake Design v1

## Status

```text
milestone: Real Candidate Image Intake Design v1
status: implementation-complete-pending-test
started_on: 2026-07-09
previous_gate: Foundation Exit Review v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Define the boundaries for future real candidate image intake before any image bytes are loaded or decoded.

This milestone is design-only. It does not implement image loading, image decoding, pixel inspection, computer vision, OCR, image generation, image editing, candidate scoring, report mutation, or approval automation.

## Scope

```text
- Define accepted candidate image reference types.
- Define forbidden reference behaviors.
- Define intake states.
- Define checksum expectations.
- Define media-type expectations.
- Define byte-handling policy.
- Define failure states for missing, unreadable, unsupported, or mismatched candidates.
- Confirm intake-only work cannot approve candidates.
- Add machine-readable intake design fixture.
- Add tests for intake design guardrails.
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
docs/500_Milestones/Real_Candidate_Image_Intake_Design_v1.md
examples/graphics/candidate_evaluation/real_candidate_image_intake.design.json
tests/test_real_candidate_image_intake_design.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Accepted reference types for future intake

```text
artifact_uri:
  status: accepted_for_future_intake
  example: artifact://external-candidates/perseverance/candidate-0001.png
  notes: Preferred internal reference shape for managed artifacts.

local_file_path:
  status: accepted_for_future_intake_with_policy
  example: ./external-candidates/perseverance/candidate-0001.png
  notes: Future implementation must restrict path traversal and workspace boundaries.

file_uri:
  status: accepted_for_future_intake_with_policy
  example: file:///workspace/external-candidates/perseverance/candidate-0001.png
  notes: Future implementation must normalize and restrict file access.
```

## Forbidden reference behavior

```text
- No http:// image fetching during intake.
- No https:// image fetching during intake.
- No arbitrary network retrieval.
- No following redirects.
- No implicit cloud-provider downloads.
- No shelling out to open files.
- No path traversal outside approved workspace/artifact roots.
```

## Intake states

```text
reference_only_not_loaded:
  description: Candidate is known only by manifest reference.
  approval_allowed: false

intake_design_only:
  description: Intake policy exists, but no bytes have been loaded.
  approval_allowed: false

intake_pending:
  description: Candidate is eligible for future intake but has not been loaded.
  approval_allowed: false

intake_failed:
  description: Candidate failed future intake validation.
  approval_allowed: false

intake_loaded_not_evaluated:
  description: Future state where bytes were loaded but no evaluation has run.
  approval_allowed: false
```

## Checksum expectations

```text
- Candidate manifests should provide image_sha256 before intake.
- Missing checksum must produce needs_review.
- Checksum mismatch must produce rejected or intake_failed, depending on future policy stage.
- Checksum validation alone cannot approve a candidate.
```

## Media-type expectations

```text
accepted_media_types:
- image/png
- image/jpeg
- image/webp

unsupported_media_type_behavior:
  decision: needs_review
  approval_allowed: false
```

## Byte-handling policy

```text
- Intake must treat image bytes as untrusted input.
- Intake must not execute embedded content.
- Intake must not infer approval from successful loading.
- Intake must preserve original reference metadata.
- Intake must record byte count and checksum in future implementation.
- Intake must keep decoded pixel inspection separate from intake.
```

## Failure states

```text
missing_reference:
  decision: needs_review
  approval_allowed: false

missing_checksum:
  decision: needs_review
  approval_allowed: false

unreadable_candidate:
  decision: needs_review
  approval_allowed: false

unsupported_media_type:
  decision: needs_review
  approval_allowed: false

checksum_mismatch:
  decision: rejected_or_intake_failed_after_policy_confirmation
  approval_allowed: false

outside_allowed_root:
  decision: rejected_or_intake_failed_after_policy_confirmation
  approval_allowed: false
```

## Required next gate

```text
recommended_next_milestone: Candidate Intake Manifest Contract v1
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

## Verification command

```powershell
pytest tests/test_real_candidate_image_intake_design.py
```

## Guardrails

```text
- Design only.
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
[x] Real candidate image intake design doc exists.
[x] Machine-readable real candidate image intake design fixture exists.
[x] Accepted reference types are defined.
[x] Forbidden reference behaviors are defined.
[x] Intake states are defined and cannot approve.
[x] Checksum expectations are defined.
[x] Media-type expectations are defined.
[x] Byte-handling policy is defined.
[x] Failure states are defined and cannot approve.
[x] Next gate is Candidate Intake Manifest Contract v1.
[x] Command reference updated in the same implementation slice.
[ ] Verification test result recorded.
```
