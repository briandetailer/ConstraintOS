# Candidate Image Byte Loading Implementation Design v1

## Status

```text
milestone: Candidate Image Byte Loading Implementation Design v1
status: complete
started_on: 2026-07-09
completed_on: 2026-07-09
previous_gate: Byte Loading Foundation Exit Review v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
latest_user_reported_candidate_image_byte_loading_implementation_design_test_result: 9 passed
latest_user_reported_candidate_image_byte_loading_implementation_design_test_result_on: 2026-07-09
```

## Purpose

Define the implementation behavior for future candidate image byte loading before any image byte-loading code is written.

This milestone is design-only. It does not implement image byte loading, local file opening, artifact download, network fetch, image decoding, pixel inspection, computer vision, OCR, image generation, image editing, candidate scoring, report mutation, or approval automation.

## Scope

```text
- Define future implementation entry point boundaries.
- Define allowed-root enforcement behavior.
- Define path normalization behavior.
- Define artifact registry lookup behavior.
- Define checksum computation behavior.
- Define size limit enforcement behavior.
- Define media-type sniffing behavior.
- Define safe failure reporting behavior.
- Confirm byte loading alone cannot approve candidates.
- Add machine-readable implementation design fixture.
- Add tests for implementation-design guardrails.
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
docs/500_Milestones/Candidate_Image_Byte_Loading_Implementation_Design_v1.md
examples/graphics/candidate_evaluation/candidate_image_byte_loading_implementation.design.json
tests/test_candidate_image_byte_loading_implementation_design.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Future implementation entry point boundaries

```text
entry_point_name: load_candidate_image_bytes
allowed_input:
- validated candidate image byte-loading record fixture
- repository-local candidate directory path
- explicit artifact registry adapter
- explicit allowed root policy

forbidden_input:
- arbitrary URL
- arbitrary absolute path
- implicit cloud storage pointer
- shell-expanded path
- unvalidated manifest data

entry_point_output:
- immutable byte-loading result object
- safe failure record when loading cannot proceed
- no mutation of source fixtures
- no candidate approval
```

## Allowed-root enforcement behavior

```text
local_file_path:
- normalize candidate path before loading
- resolve against configured allowed roots
- reject traversal outside allowed roots
- reject absolute paths unless explicitly allowlisted by policy
- fail closed on ambiguity

file_uri:
- parse URI before path conversion
- allow only empty host or localhost
- normalize decoded path
- resolve against configured file URI roots
- reject traversal outside allowed roots
- fail closed on ambiguity
```

## Path normalization behavior

```text
normalization_order:
1. Read reference type and raw reference string.
2. Reject empty, whitespace-only, or control-character references.
3. Parse by reference type.
4. Normalize separators.
5. Collapse dot segments.
6. Resolve symlink behavior according to platform policy before byte open.
7. Confirm normalized path remains inside an allowed root.
8. Refuse loading if normalized path is ambiguous or outside policy.
```

## Artifact registry lookup behavior

```text
artifact_uri:
- use explicit artifact registry adapter only
- allow artifact:// scheme only
- reject http and https
- reject implicit cloud download
- resolve to an internal immutable artifact descriptor
- descriptor must include byte source, expected media type, expected sha256, and expected byte count
- missing artifact produces intake_failed
```

## Checksum computation behavior

```text
checksum_order:
1. Load bytes only after reference policy passes.
2. Compute sha256 over exact loaded byte sequence.
3. Compare computed sha256 to manifest image_sha256.
4. Record computed sha256.
5. Fail intake on mismatch.
6. Do not decode image until checksum passes.
7. Checksum match cannot approve a candidate.
```

## Size limit enforcement behavior

```text
max_candidate_image_bytes: 25000000
size_order:
1. Enforce expected_byte_count before byte loading when present.
2. Refuse expected byte count above max_candidate_image_bytes.
3. Track bytes read during loading.
4. Stop loading when the maximum is exceeded.
5. Record actual_loaded_byte_count only after safe completion.
6. Oversize candidate produces intake_failed.
7. Size compliance cannot approve a candidate.
```

## Media-type sniffing behavior

```text
accepted_media_types:
- image/png
- image/jpeg
- image/webp

sniffing_order:
1. Require declared media_type before loading.
2. Sniff media type from loaded bytes only after checksum passes.
3. Record sniffed_media_type.
4. Require declared media_type and sniffed_media_type to match.
5. Fail intake on unsupported or mismatched media type.
6. Media-type match cannot approve a candidate.
```

## Safe failure reporting behavior

```text
safe_failure_record_required_fields:
- failure_code
- failure_reason
- reference_type
- candidate_id
- contract_key
- image_bytes_loaded
- image_decoded
- candidate_scoring_ran
- approval_allowed

safe_failure_defaults:
image_bytes_loaded: false unless bytes safely loaded
image_decoded: false
candidate_scoring_ran: false
approval_allowed: false
initial_decision: needs_review or intake_failed
```

## Required next gate

```text
recommended_next_milestone: Candidate Image Byte Loading Implementation Contract v1
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
pytest tests/test_candidate_image_byte_loading_implementation_design.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_candidate_image_byte_loading_implementation_design.py
result: 9 passed
reported_on: 2026-07-09
assistant_ran_tests: false
```

## Guardrails

```text
- Implementation design only.
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

## Done criteria

```text
[x] Candidate image byte-loading implementation design doc exists.
[x] Machine-readable implementation design fixture exists.
[x] Future implementation entry point boundaries are defined.
[x] Allowed-root enforcement behavior is defined.
[x] Path normalization behavior is defined.
[x] Artifact registry lookup behavior is defined.
[x] Checksum computation behavior is defined.
[x] Size limit enforcement behavior is defined.
[x] Media-type sniffing behavior is defined.
[x] Safe failure reporting behavior is defined.
[x] Byte loading alone cannot approve candidates.
[x] Command reference updated with verification command.
[x] Verification test result recorded.
```

## Handoff notes

```text
- Candidate Image Byte Loading Implementation Design v1 is complete.
- Future implementation behavior is defined for entry point boundaries, allowed-root enforcement, path normalization, artifact registry lookup, checksum computation, size-limit enforcement, media-type sniffing, and safe failure reporting.
- This milestone did not implement image byte loading, local file opening, artifact download, network fetch, image decoding, pixel inspection, CV/OCR integration, image generation, image editing, candidate scoring, report mutation, or approval automation.
- The next milestone should be Candidate Image Byte Loading Implementation Contract v1.
- Image byte loading must not begin until implementation contract behavior is defined and verified.
```
