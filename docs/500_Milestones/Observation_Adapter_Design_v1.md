# Observation Adapter Design v1

## Status

```text
milestone: Observation Adapter Design v1
status: complete
started_on: 2026-07-08
completed_on: 2026-07-08
previous_gate: Foundation Readiness Review v1 complete
track: Foundation Completion Track
baseline: 487 passed
latest_user_reported_observation_adapter_design_test_result: 8 passed
latest_user_reported_observation_adapter_design_test_result_on: 2026-07-08
```

## Purpose

Define the design boundary for collecting observations that may eventually support candidate graphics evaluation.

This milestone does not implement real candidate image ingestion, computer vision, image generation, image editing, or approval automation. It defines how future observation sources must be classified, normalized, and downgraded safely when confidence is low.

## Scope

```text
- Define observation adapter boundary.
- Define observation source taxonomy.
- Define manual/human-review observation path.
- Define future machine-assisted observation path without choosing providers.
- Define evidence normalization rules.
- Define failure and uncertainty handling.
- Preserve needs_review as the non-approval default for low-confidence observations.
- Add machine-readable design fixture.
- Add tests for design guardrails.
- Update candidate evaluation README.
- Update command reference with verification command.
```

## Out of scope

```text
- No real image loading or decoding.
- No computer-vision provider integration.
- No OCR provider integration.
- No image generation.
- No image editing.
- No automatic approval.
- No candidate-evaluation scoring behavior change.
```

## Implemented files

```text
docs/500_Milestones/Observation_Adapter_Design_v1.md
examples/graphics/candidate_evaluation/observation_adapter.design.json
tests/test_observation_adapter_design.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Observation source taxonomy

```text
manual_human_review:
  description: A human reviewer records observations against known contract constraints.
  availability: allowed_first
  approval_capability: cannot_approve_alone

metadata_only:
  description: File/path/manifest metadata, not pixel/image evidence.
  availability: allowed_with_manifest_only
  approval_capability: cannot_approve_alone

machine_assisted_placeholder:
  description: Future machine-assisted observations such as CV or OCR.
  availability: design_only_not_implemented
  approval_capability: cannot_approve_alone

external_claim:
  description: Producer or submitter claims about the candidate.
  availability: allowed_as_claim_only
  approval_capability: cannot_approve_alone
```

## Normalized observation item

```text
observation_id: required stable id
constraint_id: required mapped constraint id
constraint_group: required mapped constraint group
source_type: required observation source taxonomy value
claim: required observation claim
observed_status: one of satisfied, missing, ambiguous, contradicted, not_observed
confidence: number from 0 to 1
reviewer_or_agent: required source label
notes: required text field
```

## Decision safety rules

```text
- Low-confidence satisfied observations do not permit approval.
- Ambiguous observations produce needs_review.
- Missing required evidence produces needs_review.
- Contradicted required constraints produce rejected only after the contradiction source is explicit.
- Manual observations cannot approve alone.
- Machine-assisted observations cannot approve alone.
- Metadata-only observations cannot approve alone.
- External claims cannot approve alone.
```

## Required next gate

Before real candidate image ingestion, the project must add an observation adapter implementation milestone that still starts with manual/fixture observations before any automated provider integration.

```text
recommended_next_milestone: Manual Observation Fixture Adapter v1
blocked_until_later:
- real image ingestion
- computer-vision provider integration
- OCR provider integration
- image generation integration
- approval automation change
```

## Verification command

```powershell
pytest tests/test_observation_adapter_design.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_observation_adapter_design.py
result: 8 passed
reported_on: 2026-07-08
assistant_ran_tests: false
```

## Guardrails

```text
- Design only.
- No real candidate image loading.
- No CV/OCR provider choice.
- No generated candidate approval.
- Low-confidence or incomplete observations default to needs_review.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Observation adapter design doc exists.
[x] Machine-readable observation adapter design fixture exists.
[x] Observation source taxonomy is defined.
[x] Normalized observation item shape is defined.
[x] Non-approval decision safety rules are defined.
[x] Next gate is Manual Observation Fixture Adapter v1.
[x] Real image ingestion remains blocked.
[x] Command reference updated in the same implementation slice.
[x] Verification test result recorded.
```

## Handoff notes

```text
- Observation Adapter Design v1 is complete.
- Observation source taxonomy and normalized observation item shape are defined.
- Manual/human-review observation is the first allowed source path.
- Machine-assisted observation remains a placeholder and no provider was selected.
- Real image ingestion, computer-vision integration, OCR integration, image generation, image editing, approval automation, and candidate-evaluation scoring changes remain blocked.
- The next milestone should be Manual Observation Fixture Adapter v1.
```
