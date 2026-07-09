# Candidate Evaluation Fixtures

This directory contains design-only, schema-only, read-only discovery, fixture-only report contract, fixture-only evaluation, observation-adapter design, manual-observation fixture, observation-to-report binding, fixture-only evidence merge, fixture-only candidate review packet, real-candidate-image intake design, candidate-intake manifest contract, candidate-intake manifest discovery, and candidate-intake review packet artifacts for future candidate graphics evaluation.

## Current fixtures

```text
candidate_evaluation_adapter.design.json
observation_adapter.design.json
real_candidate_image_intake.design.json
candidate_manifest.schema.json
candidate_intake_manifest.schema.json
candidate_evaluation_report.schema.json
manual_observation.schema.json
perseverance_candidate_manifest.fixture.json
supra_2jz_gte_candidate_manifest.fixture.json
perseverance_candidate_intake_manifest.fixture.json
supra_2jz_gte_candidate_intake_manifest.fixture.json
perseverance_candidate_evaluation_report.fixture.json
supra_2jz_gte_candidate_evaluation_report.fixture.json
perseverance_manual_observation.fixture.json
supra_2jz_gte_manual_observation.fixture.json
```

## Status

```text
adapter_status: design_only
observation_adapter_status: design_only
real_candidate_image_intake_status: design_only
manifest_status: static_fixture_only
candidate_intake_manifest_status: static_fixture_only
candidate_intake_discovery_status: read_only
candidate_intake_review_packet_status: fixture_only
discovery_status: read_only
report_contract_status: fixture_only
fixture_only_evaluation_status: available
manual_observation_status: fixture_only
observation_report_binding_status: fixture_only
observation_evidence_merge_status: fixture_only
candidate_review_packet_status: fixture_only
implementation_status: intake_review_packet_only
image_generation_allowed: false
image_editing_allowed: false
real_candidate_image_ingestion_allowed: false
computer_vision_integration_allowed: false
candidate_evaluation_source: static_report_fixture
manual_observation_source: static_manual_fixture
initial_decision: needs_review
uncertainty_default: needs_review
approval_allowed: false
```

## Purpose

The adapter design fixture defines the boundary between reusable graphics-validation contracts and future externally produced candidate graphics.

The observation adapter design fixture defines the future boundary for collecting observations without starting real image ingestion or selecting machine-observation providers.

The real candidate image intake design fixture defines accepted future reference types, forbidden network/path behaviors, checksum and media-type expectations, byte-handling policy, and failure states before any image bytes are loaded.

The candidate intake manifest contract defines a future intake-ready manifest shape with accepted reference type, reference URI, media type, checksum, policy snapshot, and non-approval intake boundary.

Candidate intake manifest discovery lists and shows intake-ready metadata fixtures without loading, opening, downloading, decoding, inspecting, scoring, mutating, or approving candidate images.

Candidate intake review packets summarize intake candidate identity, reference metadata, policy snapshot, intake boundaries, and approval blockers for human review.

The manual observation fixtures define the first allowed observation source path, but they remain fixture-only and do not inspect images.

Observation-to-report binding compares candidate manifests, manual observation fixtures, and fixture-only evaluation reports for the same candidate before any real image ingestion work begins.

Fixture-only evidence merge creates a derived view of manual observations aligned to report evidence items without mutating source reports or scoring candidates.

Fixture-only candidate review packets summarize candidate identity, manual observations, report binding, merged evidence, and approval blockers for human review.

The candidate manifest schema defines the static manifest shape required before any future candidate-evaluation command can exist.

The candidate manifest discovery CLI lists and shows static manifest summaries without evaluating candidate images.

The candidate evaluation report contract defines the future report shape before any real candidate evaluation behavior is implemented.

The fixture-only candidate evaluation command loads a static manifest fixture and its matching static report fixture, validates their binding, and reports the fixture recommendation.

## Real candidate image intake design

The real candidate image intake design defines policy boundaries for future image intake.

```text
accepted_reference_types:
  artifact_uri
  local_file_path
  file_uri

forbidden_reference_behaviors:
  http_image_fetch
  https_image_fetch
  arbitrary_network_retrieval
  redirect_following
  implicit_cloud_provider_download
  shell_open_file
  path_traversal_outside_allowed_roots

accepted_media_types:
  image/png
  image/jpeg
  image/webp

next_gate:
  Candidate Intake Manifest Contract v1
```

Successful intake will not approve a candidate. Image byte loading, image decoding, pixel inspection, CV/OCR provider integration, scoring, and approval automation remain blocked.

## Candidate intake manifest contract

The candidate intake manifest contract defines static intake-ready metadata fixtures for future image intake.

```text
candidate_intake_manifest.schema.json:
  required_sections:
    candidate_intake_manifest
    contract_binding
    candidate_reference
    candidate_source
    intake_policy_snapshot
    intake_boundary
    approval_expectation

perseverance_candidate_intake_manifest.fixture.json:
  candidate_manifest_key: perseverance
  contract_key: perseverance
  reference_type: artifact_uri
  reference_status: intake_pending
  approval_allowed: false

supra_2jz_gte_candidate_intake_manifest.fixture.json:
  candidate_manifest_key: supra_2jz_gte
  contract_key: supra_2jz_gte_twin_turbo
  reference_type: artifact_uri
  reference_status: intake_pending
  approval_allowed: false
```

Candidate intake manifest fixtures do not load, open, download, decode, inspect, score, mutate, or approve candidate images.

## Candidate intake manifest discovery commands

```powershell
cos-graphics-candidates intake-list
cos-graphics-candidates intake-show perseverance
cos-graphics-candidates intake-show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-intake-manifests.json intake-list
```

These commands are read-only. They discover intake manifest metadata only and do not load, open, download, decode, inspect, score, mutate, or approve candidate images.

## Candidate intake review packet commands

```powershell
cos-graphics-candidates intake-review-packet perseverance
cos-graphics-candidates intake-review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-intake-review-packet.json intake-review-packet perseverance
```

These commands produce human-facing intake review packets from fixture-only intake manifest metadata. They do not load, open, download, decode, inspect, score, mutate, or approve candidate images.

## Observation adapter design

The observation adapter design defines source types and normalization rules for future evidence collection.

```text
source_types:
  manual_human_review
  metadata_only
  machine_assisted_placeholder
  external_claim

next_gate:
  Manual Observation Fixture Adapter v1

blocked_until_later:
  real_image_ingestion
  computer_vision_provider_integration
  ocr_provider_integration
  image_generation_integration
  approval_automation_change
```

No observation source can approve alone. Low-confidence or incomplete observations default to `needs_review`.

## Manual observation fixtures

The manual observation fixtures bind static, manually recorded observation placeholders to existing candidate manifests.

```text
perseverance_manual_observation.fixture.json:
  candidate_manifest_key: perseverance
  contract_key: perseverance
  source_type: manual_human_review
  recommended_decision: needs_review
  approval_allowed: false

supra_2jz_gte_manual_observation.fixture.json:
  candidate_manifest_key: supra_2jz_gte
  contract_key: supra_2jz_gte_twin_turbo
  source_type: manual_human_review
  recommended_decision: needs_review
  approval_allowed: false
```

The manual observation fixtures do not claim that any real image was loaded, decoded, inspected, or evaluated.

## Observation-to-report binding

Observation-to-report binding verifies that the manifest, manual observation fixture, and candidate evaluation report fixture agree on candidate identity and decision guardrails.

```text
binding_inputs:
  candidate_manifest.fixture.json
  manual_observation.fixture.json
  candidate_evaluation_report.fixture.json

binding_output:
  fixture_only binding report
  recommended_decision: needs_review
  approval_allowed: false
```

Binding does not mutate report fixtures, score candidates, inspect image bytes, or approve candidates.

## Fixture-only observation evidence merge

Fixture-only observation evidence merge aligns manual observation items to report evidence items by `constraint_id`.

```text
merge_inputs:
  manual_observation.fixture.json
  candidate_evaluation_report.fixture.json

merge_output:
  matched_constraint_count
  manual_only_constraint_count
  report_only_constraint_count
  merged_evidence_items
  recommended_decision: needs_review
  approval_allowed: false
```

Merged evidence is derived output only. It does not mutate report fixtures, score candidates, inspect image bytes, or approve candidates.

## Fixture-only candidate review packet

Fixture-only candidate review packets package the current candidate state into a human-facing review summary.

```text
review_packet_sections:
  candidate_identity
  manual_observations
  candidate_evaluation_report
  merged_evidence
  decision_guardrails

review_packet_output:
  review_packet_ready: true
  recommended_decision: needs_review
  approval_allowed: false
```

Review packets do not inspect images, score candidates, mutate report fixtures, or approve candidates.

## Candidate manifest fixtures

The manifest fixtures bind externally produced candidate references to existing graphics-validation contract keys.

```text
perseverance_candidate_manifest.fixture.json:
  manifest_key: perseverance
  contract_key: perseverance

supra_2jz_gte_candidate_manifest.fixture.json:
  manifest_key: supra_2jz_gte
  contract_key: supra_2jz_gte_twin_turbo
```

The fixture references are placeholders only. They do not load, decode, inspect, or evaluate image bytes.

## Candidate evaluation report fixtures

The report fixtures bind to the static candidate manifests and describe the fixture-only evidence/report shape.

```text
perseverance_candidate_evaluation_report.fixture.json:
  candidate_manifest_key: perseverance
  contract_key: perseverance
  recommended_decision: needs_review
  evidence_status: not_observed

supra_2jz_gte_candidate_evaluation_report.fixture.json:
  candidate_manifest_key: supra_2jz_gte
  contract_key: supra_2jz_gte_twin_turbo
  recommended_decision: needs_review
  evidence_status: not_observed
```

The report fixtures do not claim that real candidate evaluation has run. They exist to lock the report contract before real image ingestion.

## Read-only discovery commands

```powershell
cos-graphics-candidates list
cos-graphics-candidates show perseverance
cos-graphics-candidates show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-manifests.json list
```

## Fixture-only evaluation commands

```powershell
cos-graphics-candidates evaluate perseverance
cos-graphics-candidates evaluate supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-candidate-evaluation.json evaluate perseverance
```

These commands load static manifest and report fixtures only. They do not load, decode, inspect, or evaluate image bytes.

## Manual observation fixture commands

```powershell
cos-graphics-candidates observe perseverance
cos-graphics-candidates observe supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-observations.json observe perseverance
```

These commands load static manifest and manual observation fixtures only. They do not load, decode, inspect, or evaluate image bytes.

## Observation-to-report binding commands

```powershell
cos-graphics-candidates bind-observations perseverance
cos-graphics-candidates bind-observations supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-observation-binding.json bind-observations perseverance
```

These commands bind static manifest, manual observation, and candidate evaluation report fixtures only. They do not mutate report fixtures, score candidates, or inspect image bytes.

## Fixture-only evidence merge commands

```powershell
cos-graphics-candidates merge-evidence perseverance
cos-graphics-candidates merge-evidence supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-merged-evidence.json merge-evidence perseverance
```

These commands merge static manual observation and candidate evaluation report evidence only. They do not mutate report fixtures, score candidates, or inspect image bytes.

## Fixture-only candidate review packet commands

```powershell
cos-graphics-candidates review-packet perseverance
cos-graphics-candidates review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-review-packet.json review-packet perseverance
```

These commands produce human-facing fixture-only review packets. They do not mutate report fixtures, score candidates, inspect image bytes, or approve candidates.

## Verification

```powershell
pytest tests/test_candidate_evaluation_adapter_design.py
pytest tests/test_observation_adapter_design.py
pytest tests/test_real_candidate_image_intake_design.py
pytest tests/test_candidate_intake_manifest_contract.py
pytest tests/test_candidate_intake_manifest_discovery_cli.py
pytest tests/test_candidate_intake_review_packet.py
pytest tests/test_candidate_manifest_schema.py
pytest tests/test_candidate_manifest_discovery_cli.py
pytest tests/test_candidate_evaluation_report_contract.py
pytest tests/test_fixture_only_candidate_evaluation.py
pytest tests/test_manual_observation_fixture_adapter.py
pytest tests/test_observation_report_binding.py
pytest tests/test_observation_evidence_merge.py
pytest tests/test_candidate_review_packet.py
```

## Guardrail

Candidate graphics are external inputs. ConstraintOS does not generate, edit, load, inspect, or approve images in these milestones. Candidate intake review packets do not enable image byte loading, image decoding, pixel inspection, scoring, report mutation, or approval.
