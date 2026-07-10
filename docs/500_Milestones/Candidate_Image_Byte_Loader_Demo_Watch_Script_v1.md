# Candidate Image Byte Loader Demo Watch Script v1

## Status

```text
milestone: Candidate Image Byte Loader Demo Watch Script v1
status: active
started_on: 2026-07-10
previous_gate: Candidate Image Byte Loading Fixture Registry Failure Matrix v1 complete
track: Business Demo Visibility Track
baseline: 487 passed
```

## Purpose

Add a business-demo-friendly watch script for the current candidate image byte-loading evidence path.

This milestone exists because tests and static review packets are not enough for stakeholder confidence. A business user should be able to run one command and watch ConstraintOS march through the current byte-loading safety pipeline: selected candidate record, deterministic fixture byte loading, review packet generation, registry descriptor review, failure-matrix review, JSON evidence capture, and final non-approval guardrails.

## Product charter alignment

```text
product_charter_seed: ConstraintOS is an open architecture for deterministic, auditable, specification-driven publishing using probabilistic AI systems.
mission_seed: Structured specifications, validation, and traceability — not AI model behavior — are the source of truth.
demo_principle: Show the validation path in motion without weakening constraints.
business_demo_goal: Make effort visible as auditable evidence, not hidden test output.
```

## Scope

```text
- Add scripts/watch-candidate-byte-loader.ps1.
- Provide one command that demos the current byte-loading evidence path.
- Show stage-by-stage terminal output.
- Run cos-graphics-byte-loader minimal for the selected record.
- Run cos-graphics-byte-loader review-packet for the selected record.
- Run cos-graphics-byte-loader registry-review-packet.
- Run cos-graphics-byte-loader failure-review-packet.
- Capture JSON evidence files under runs/candidate-byte-loader/<record>/<timestamp>/.
- Capture terminal transcript and watch output.
- Write run metadata.
- Preserve no local image file opening.
- Preserve no artifact download.
- Preserve no network fetch.
- Preserve no image decoding.
- Preserve no candidate scoring.
- Preserve no source report mutation.
- Preserve no approval automation.
- Update tests.
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

## Demo command

```powershell
.\scripts\watch-candidate-byte-loader.ps1
.\scripts\watch-candidate-byte-loader.ps1 -Record perseverance
.\scripts\watch-candidate-byte-loader.ps1 -Record supra_2jz_gte_twin_turbo -WatchDelayMs 750
```

## Demo stages

```text
1. Load deterministic fixture bytes for the selected record.
2. Build the selected record byte-loading review packet.
3. Review deterministic fixture registry descriptors.
4. Review fixture registry failure matrix.
5. Capture JSON evidence files.
6. Record final non-approval guardrails.
```

## Demo boundary

```text
demo_source: scripts/watch-candidate-byte-loader.ps1
execution_style: visible staged dry-run demonstration
byte_source: deterministic fixture artifact registry
failure_matrix_source: fixture-only JSON case list
local_image_file_opening: false
artifact_download: false
network_fetch: false
image_decoding: false
candidate_scoring: false
approval_allowed: false
```

## Verification command

```powershell
pytest tests/test_candidate_image_byte_loader_demo_watch_script.py
```

## Guardrails

```text
- Demo watch script only.
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
