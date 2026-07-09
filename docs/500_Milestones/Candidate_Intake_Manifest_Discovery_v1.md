# Candidate Intake Manifest Discovery v1

## Status

```text
milestone: Candidate Intake Manifest Discovery v1
status: active
started_on: 2026-07-09
previous_gate: Candidate Intake Manifest Contract v1 complete
track: Real Candidate Intake Track
baseline: 487 passed
```

## Purpose

Add read-only discovery for fixture-only candidate intake manifests.

This milestone lets users list and inspect intake-ready candidate manifest fixtures without loading, opening, downloading, decoding, inspecting, scoring, mutating, or approving candidate images.

## Scope

```text
- Add candidate intake manifest helper module.
- Add cos-graphics-candidates intake-list.
- Add cos-graphics-candidates intake-show.
- Support text and JSON output.
- Support JSON file output.
- Preserve no image byte loading.
- Preserve no network fetch.
- Preserve no decoding, inspection, scoring, mutation, or approval.
- Add tests for discovery, CLI output, and guardrails.
- Update candidate evaluation README.
- Update command reference with new available commands.
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

## Verification command

```powershell
pytest tests/test_candidate_intake_manifest_discovery_cli.py
```

## CLI commands

```powershell
cos-graphics-candidates intake-list
cos-graphics-candidates intake-show perseverance
cos-graphics-candidates intake-show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-intake-manifests.json intake-list
```

## Required next gate

```text
recommended_next_milestone: Candidate Intake Review Packet v1
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
- Read-only discovery only.
- Fixture-only intake manifests.
- No image bytes loaded.
- No image decoding.
- No network fetch.
- No CV/OCR provider choice.
- No candidate scoring.
- No approval automation change.
- Do not claim tests passed unless actually run.
```
