# Current Evidence-Harness POC Demo Feedback Action Backlog

## Status

```text
demo: Current Evidence-Harness POC Demo
status: complete
track: Business Demo Visibility Track
synthesis_log: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Synthesis_Log.md
triage_guide: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Triage_Guide.md
future_target_bank: Constraint-Driven Graphic Output Permutation POC v1
latest_user_reported_current_evidence_harness_poc_demo_feedback_action_backlog_test_result: 5 passed
latest_user_reported_current_evidence_harness_poc_demo_feedback_action_backlog_test_result_on: 2026-07-10
```

## Purpose

This backlog turns synthesized reviewer feedback into scoped action items.

The goal is to keep current-demo polish actionable while keeping later product capabilities banked behind separate gated milestones.

## Intake rule

```text
Only add an item here after feedback has been triaged and synthesized.
Do not add raw reviewer comments directly.
Do not expand processing capability from this backlog alone.
```

## Current-demo polish backlog

These items can improve the current evidence-harness demo without adding new processing capabilities.

| ID | Source synthesis ID | Action | Category | Severity | Owner | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-001 | _pending synthesis_ | _pending reviewer-driven polish action_ | _pending_ | _pending_ | _unassigned_ | open | _awaiting reviewer feedback_ |

## Banked later-work backlog

These items require a separate gated milestone before implementation.

| ID | Source synthesis ID | Banked work | Target track | Reason banked | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| BANK-001 | _pending synthesis_ | Constraint-driven graphic output permutations | Constraint-Driven Graphic Output Permutation POC v1 | Requires explicit output-generation milestone | banked | Product target already identified |

## Status values

```text
open: not started
accepted: ready for a scoped current-demo polish slice
in_progress: actively being worked
complete: implemented and verified
banked: intentionally held for later gated milestone
closed: not actionable, duplicate, or outside current direction
```

## Current-demo allowed actions

```text
- README clarification
- reviewer guide clarification
- readiness packet clarification
- feedback form wording
- issue template wording
- triage guide wording
- synthesis log organization
- command reference discoverability
- demo narration wording
- run-folder inspection guidance
```

## Later gated actions

```text
- generated final graphics
- constraint-derived graphic output permutations
- real local image input
- local_file_path loading
- file_uri loading
- artifact download
- network fetch
- image decoding
- pixel inspection
- CV/OCR provider integration
- unrestricted image generation
- unrestricted image editing
- automatic scoring
- automatic approval
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_current_evidence_harness_poc_demo_feedback_action_backlog.py
result: 5 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```

## Prioritization rule

```text
1. Resolve blocking current-demo comprehension issues first.
2. Resolve high-severity trust or clarity issues second.
3. Batch medium and low polish items into small documentation slices.
4. Bank output-generation and real-input requests instead of implementing them here.
5. Close duplicate or non-actionable feedback explicitly.
```

## Action item template

```text
id:
source_synthesis_id:
action:
category:
severity:
current_demo_or_later_track:
status:
notes:
```

## Guardrails

```text
- This backlog is documentation-only.
- This backlog does not authorize new processing capability.
- This backlog does not authorize local image loading.
- This backlog does not authorize artifact download.
- This backlog does not authorize network fetch.
- This backlog does not authorize image decoding.
- This backlog does not authorize CV/OCR provider integration.
- This backlog does not authorize unrestricted image generation or editing.
- This backlog does not authorize automatic approval.
```

## Local verification

```powershell
git pull --rebase origin phase-1-cli-tooling
pytest tests/test_current_evidence_harness_poc_demo_feedback_action_backlog.py
```
