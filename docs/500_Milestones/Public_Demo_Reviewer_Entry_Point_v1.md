# Public Demo Reviewer Entry Point v1

## Status

```text
milestone: Public Demo Reviewer Entry Point v1
status: complete
started_on: 2026-07-10
completed_on: 2026-07-10
track: Business Demo Visibility Track
previous_context: Current Evidence-Harness POC Demo Readiness Packet exists
baseline: 487 passed
latest_user_reported_public_demo_reviewer_entry_point_test_result: 7 passed
latest_user_reported_public_demo_reviewer_entry_point_test_result_on: 2026-07-10
latest_user_reported_demo_recording_status: recording completed
latest_user_reported_demo_recording_status_on: 2026-07-10
```

## Purpose

Make the public GitHub repository easier for friends, reviewers, and early collaborators to understand.

The repository is now suitable for critique in POC mode, but the root README previously only exposed the charter seed. This milestone adds a clear public entry point to the current evidence-harness demo, while preserving the banked future product target: constraint-driven graphic output permutations.

## Scope

```text
- Update root README with current POC status.
- Add public demo entry point.
- Link current evidence-harness POC demo guide.
- Link current evidence-harness POC demo readiness packet.
- Link end-to-end fixture POC demo outline.
- Document one-command demo invocation.
- Document local verification commands.
- Explain what the current demo does and does not do.
- Preserve future target as banked, not active.
- Add tests.
- Update command reference.
```

## Public README boundary

```text
current_demo_type: evidence-harness POC demo
current_script: scripts/watch-constraintos-poc.ps1
current_demo_result: needs_review
approval_allowed: false
future_target_bank: Constraint-Driven Graphic Output Permutation POC v1
not_currently_supported:
- generated final graphics
- constraint-derived graphic output permutations
- arbitrary local image input
- image decoding
- CV/OCR provider integration
- unrestricted image generation/editing
- automatic approval
```

## Reviewer command

```powershell
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
```

## Verification command

```powershell
pytest tests/test_public_demo_reviewer_entry_point.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_public_demo_reviewer_entry_point.py
result: 7 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```

## Demo recording record

```text
source: user-reported local demo run
command: .\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
result: recording completed
reported_on: 2026-07-10
assistant_ran_demo: false
```

## Guardrails

```text
- README entry point only.
- No new processing capability added.
- No new byte-loading source added.
- No local image file opening.
- No artifact download.
- No network fetch.
- No image decoding.
- No CV/OCR provider choice.
- No image generation.
- No image editing.
- No automatic candidate approval.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Root README has a current POC status section.
[x] Root README has a current demo section.
[x] Root README links the demo guide.
[x] Root README links the readiness packet.
[x] Root README links the end-to-end fixture demo outline.
[x] Root README includes one-command demo invocation.
[x] Root README includes local verification commands.
[x] Root README explains current limitations.
[x] Root README preserves banked output-permutation target.
[x] Tests added.
[x] Command reference updated.
[x] Verification test result recorded.
[x] Demo recording status recorded.
```

## Handoff notes

```text
- Public Demo Reviewer Entry Point v1 is complete.
- Root README now exposes the current evidence-harness POC demo.
- The current evidence-harness POC demo recording has been reported complete by the user.
- The reviewer-facing docs are available under docs/800_Demos/.
- The next public-demo support step should focus on collecting structured reviewer feedback.
- Constraint-Driven Graphic Output Permutation POC v1 remains banked for later.
```