# Candidate Evaluation Fixtures

This directory contains design-only, contract-only, read-only, fixture-only, helper-only, and review artifacts for future graphics candidate evaluation.

## Current fixtures and artifacts

```text
candidate_evaluation_adapter.design.json
observation_adapter.design.json
real_candidate_image_intake.design.json
candidate_image_byte_loading.design.json
candidate_image_byte_loading_implementation.design.json
candidate_image_byte_loading_implementation_contract.schema.json
candidate_image_byte_loading_implementation_contract.fixture.json
candidate_image_byte_loading_record.schema.json
candidate_manifest.schema.json
candidate_intake_manifest.schema.json
candidate_evaluation_report.schema.json
manual_observation.schema.json
perseverance_candidate_manifest.fixture.json
supra_2jz_gte_candidate_manifest.fixture.json
perseverance_candidate_intake_manifest.fixture.json
supra_2jz_gte_candidate_intake_manifest.fixture.json
perseverance_candidate_image_byte_loading_record.fixture.json
supra_2jz_gte_candidate_image_byte_loading_record.fixture.json
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
candidate_image_byte_loading_status: design_only
candidate_image_byte_loading_implementation_design_status: design_only
candidate_image_byte_loading_implementation_contract_status: contract_only
candidate_image_byte_loading_minimal_implementation_status: helper_only
candidate_image_byte_loading_minimal_cli_status: helper_only
candidate_image_byte_loading_minimal_cli_review_packet_status: helper_only
candidate_image_byte_loading_contract_status: static_fixture_only
candidate_image_byte_loading_discovery_status: read_only
candidate_image_byte_loading_review_packet_status: fixture_only
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
implementation_status: byte_loading_minimal_cli_review_packet_helper_only
image_generation_allowed: false
image_editing_allowed: false
real_candidate_image_ingestion_allowed: false
image_byte_loading_allowed: explicit_fixture_controlled_artifact_registry_only
local_file_opening_allowed: false
artifact_download_allowed: false
network_fetch_allowed: false
image_decoding_allowed: false
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

The candidate image byte-loading design fixture defines future allowed roots, artifact resolution policy, maximum byte size, checksum order, media-type sniffing, byte-count recording, and safe failure states before any file is opened or image byte is loaded.

The candidate image byte-loading implementation design fixture defines future implementation entry point boundaries, allowed-root enforcement, path normalization, artifact registry lookup, checksum computation, size-limit enforcement, media-type sniffing, and safe failure reporting before byte-loading code is written.

The candidate image byte-loading implementation contract schema and fixture define the future byte-loading attempt result contract before byte-loading code is written.

The candidate image byte-loading minimal implementation helper loads bytes only from an explicit in-memory artifact registry adapter, computes checksum, compares byte count and media type, and never decodes, scores, mutates, or approves candidates.

The candidate image byte-loading minimal CLI exposes that helper through `cos-graphics-byte-loader minimal` using explicit fixture hex bytes bound to an explicit `artifact://` URI. It does not open local image files, download artifacts, fetch network resources, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

The candidate image byte-loading minimal CLI review packet exposes the same helper-only path through `cos-graphics-byte-loader review-packet`, adding review sections and approval blockers without expanding byte-source permissions.

The candidate image byte-loading contract defines the future byte-loading record shape with reference metadata, policy snapshot, not-run byte-loading result fields, post-load boundaries, and non-approval expectations.

Candidate image byte-loading discovery lists and shows static byte-loading record fixtures without opening files, downloading artifacts, fetching network resources, loading bytes, decoding images, inspecting pixels, scoring candidates, mutating reports, or approving candidates.

Candidate image byte-loading review packets summarize record identity, intake binding, reference metadata, byte-loading policy, not-run results, post-load boundaries, and approval blockers for human review.

Candidate intake manifests and review packets summarize intake metadata only. Manual observations, observation binding, evidence merge, and review packets remain fixture-only and cannot approve candidates.

## Real candidate image intake design

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

Successful intake will not approve a candidate. Image byte loading, image decoding, pixel inspection, CV/OCR provider integration, scoring, and approval automation remain blocked except for the narrow helper-only byte-loading path documented below.

## Candidate image byte-loading design

```text
candidate_image_byte_loading.design.json:
  status: design_only
  allowed_local_roots:
    ./external-candidates/
    ./runs/manual-candidates/
  allowed_file_uri_roots:
    file:///workspace/external-candidates/
    file:///workspace/runs/manual-candidates/
  max_candidate_image_bytes: 25000000
  checksum_required_before_decoding: true
  media_type_sniffing_required_after_future_loading: true
  byte_loading_success_can_approve: false
  next_gate: Candidate Image Byte Loading Contract v1
```

Candidate image byte-loading design does not open files, download artifacts, fetch network resources, load bytes, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate image byte-loading implementation design

```text
candidate_image_byte_loading_implementation.design.json:
  status: design_only
  entry_point_name: load_candidate_image_bytes
  allowed_inputs:
    validated_candidate_image_byte_loading_record_fixture
    repository_local_candidate_directory_path
    explicit_artifact_registry_adapter
    explicit_allowed_root_policy
  forbidden_inputs:
    arbitrary_url
    arbitrary_absolute_path
    implicit_cloud_storage_pointer
    shell_expanded_path
    unvalidated_manifest_data
  max_candidate_image_bytes: 25000000
  artifact_registry_adapter_required: true
  checksum_match_cannot_approve_candidate: true
  media_type_match_cannot_approve_candidate: true
  next_gate: Candidate Image Byte Loading Implementation Contract v1
```

Candidate image byte-loading implementation design does not implement file opening, artifact download, network fetch, byte loading, image decoding, pixel inspection, scoring, report mutation, or approval.

## Candidate image byte-loading implementation contract

```text
candidate_image_byte_loading_implementation_contract.schema.json:
  status: contract_only
  required_sections:
    candidate_image_byte_loading_implementation_contract
    input_binding
    policy_enforcement_result_contract
    reference_resolution_result_contract
    byte_loading_result_contract
    validation_result_contract
    safe_failure_contract
    post_contract_boundary

candidate_image_byte_loading_implementation_contract.fixture.json:
  contract_state: not_implemented
  implementation_allowed: false
  artifact_downloaded: false
  network_fetch_ran: false
  approval_allowed: false
  next_gate: Candidate Image Byte Loading Pre-Implementation Exit Review v1
```

Candidate image byte-loading implementation contract fixtures do not open files, download artifacts, fetch network resources, load bytes, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate image byte-loading minimal implementation

```text
helper: load_candidate_image_bytes_minimal
artifact_registry: InMemoryArtifactRegistry
accepted_reference_type: artifact_uri
byte_source: explicit in-memory artifact registry only
local_file_opened: false
artifact_downloaded: false
network_fetch_ran: false
image_decoded: false
candidate_scoring_ran: false
approval_allowed: false
```

The minimal implementation helper can load fixture-controlled artifact bytes and validate byte count, checksum, and signature-based media type. It does not open local files, download artifacts, fetch network resources, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate image byte-loading minimal CLI

```powershell
cos-graphics-byte-loader minimal perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
cos-graphics-byte-loader --format json minimal perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
cos-graphics-byte-loader --format json --output reports/perseverance-byte-loader.json minimal perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
```

The minimal CLI is helper-only. It accepts fixture bytes as explicit hex input and binds them to an explicit `artifact://` URI. It does not open local image files, download artifacts, fetch network resources, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate image byte-loading minimal CLI review packet

```powershell
cos-graphics-byte-loader review-packet perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
cos-graphics-byte-loader --format json review-packet perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
cos-graphics-byte-loader --format json --output reports/perseverance-byte-loader-review-packet.json review-packet perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
```

The minimal CLI review packet is helper-only. It accepts fixture bytes as explicit hex input, binds them to an explicit `artifact://` URI, and reports CLI invocation boundaries, byte-loading result, safety boundaries, and decision guardrails. It does not open local image files, download artifacts, fetch network resources, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate image byte-loading contract

```text
candidate_image_byte_loading_record.schema.json:
  required_sections:
    candidate_image_byte_loading_record
    contract_binding
    reference_snapshot
    byte_loading_policy_snapshot
    byte_loading_result
    post_load_boundary
    approval_expectation

perseverance_candidate_image_byte_loading_record.fixture.json:
  contract_key: perseverance
  byte_loading_state: not_run_contract_only
  image_bytes_loaded: false
  approval_allowed: false

supra_2jz_gte_candidate_image_byte_loading_record.fixture.json:
  contract_key: supra_2jz_gte_twin_turbo
  byte_loading_state: not_run_contract_only
  image_bytes_loaded: false
  approval_allowed: false
```

Candidate image byte-loading contract fixtures do not open files, download artifacts, fetch network resources, load bytes, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate image byte-loading discovery commands

```powershell
cos-graphics-candidates byte-loading-list
cos-graphics-candidates byte-loading-show perseverance
cos-graphics-candidates byte-loading-show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-byte-loading-records.json byte-loading-list
```

These commands are read-only. They discover static byte-loading record metadata only and do not open files, download artifacts, fetch network resources, load bytes, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate image byte-loading review packet commands

```powershell
cos-graphics-candidates byte-loading-review-packet perseverance
cos-graphics-candidates byte-loading-review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-byte-loading-review-packet.json byte-loading-review-packet perseverance
```

These commands produce human-facing fixture-only byte-loading review packets. They do not open files, download artifacts, fetch network resources, load bytes, decode images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate intake manifest contract

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

## Candidate intake review packet commands

```powershell
cos-graphics-candidates intake-review-packet perseverance
cos-graphics-candidates intake-review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-intake-review-packet.json intake-review-packet perseverance
```

## Manual observation and review commands

```powershell
cos-graphics-candidates list
cos-graphics-candidates show perseverance
cos-graphics-candidates show supra_2jz_gte_twin_turbo
cos-graphics-candidates evaluate perseverance
cos-graphics-candidates evaluate supra_2jz_gte_twin_turbo
cos-graphics-candidates observe perseverance
cos-graphics-candidates observe supra_2jz_gte_twin_turbo
cos-graphics-candidates bind-observations perseverance
cos-graphics-candidates bind-observations supra_2jz_gte_twin_turbo
cos-graphics-candidates merge-evidence perseverance
cos-graphics-candidates merge-evidence supra_2jz_gte_twin_turbo
cos-graphics-candidates review-packet perseverance
cos-graphics-candidates review-packet supra_2jz_gte_twin_turbo
```

These commands remain fixture-only/read-only and cannot approve candidates.

## Verification

```powershell
pytest tests/test_candidate_evaluation_adapter_design.py
pytest tests/test_observation_adapter_design.py
pytest tests/test_real_candidate_image_intake_design.py
pytest tests/test_candidate_image_byte_loading_design.py
pytest tests/test_candidate_image_byte_loading_implementation_design.py
pytest tests/test_candidate_image_byte_loading_implementation_contract.py
pytest tests/test_candidate_image_byte_loading_pre_implementation_exit_review.py
pytest tests/test_candidate_image_byte_loading_minimal_implementation.py
pytest tests/test_candidate_image_byte_loading_minimal_cli.py
pytest tests/test_candidate_image_byte_loading_minimal_cli_review_packet.py
pytest tests/test_candidate_image_byte_loading_contract.py
pytest tests/test_candidate_image_byte_loading_discovery_cli.py
pytest tests/test_candidate_image_byte_loading_review_packet.py
pytest tests/test_byte_loading_foundation_exit_review.py
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

Candidate graphics are external inputs. ConstraintOS does not generate, edit, inspect, score, or approve images in these milestones. Candidate image byte-loading minimal implementation, minimal CLI, and minimal CLI review packet are helper-only and limited to explicit in-memory artifact registry / fixture hex bytes; they do not enable local image file opening, artifact download, network fetch, image decoding, pixel inspection, scoring, report mutation, or approval.
