import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN_FIXTURE = ROOT / "examples" / "graphics" / "candidate_evaluation" / "candidate_image_byte_loading_implementation.design.json"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Implementation_Design_v1.md"
README = ROOT / "examples" / "graphics" / "candidate_evaluation" / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def load_design() -> dict:
    return json.loads(DESIGN_FIXTURE.read_text(encoding="utf-8"))


def test_candidate_image_byte_loading_implementation_design_is_design_only() -> None:
    design = load_design()["candidate_image_byte_loading_implementation_design"]

    assert design["status"] == "design_only"
    assert design["image_byte_loading_implemented"] is False
    assert design["local_file_opening_implemented"] is False
    assert design["artifact_download_implemented"] is False
    assert design["network_fetch_implemented"] is False
    assert design["image_decoding_implemented"] is False
    assert design["pixel_inspection_implemented"] is False
    assert design["computer_vision_implemented"] is False
    assert design["ocr_implemented"] is False
    assert design["image_generation_implemented"] is False
    assert design["image_editing_implemented"] is False
    assert design["candidate_scoring_implemented"] is False
    assert design["approval_automation_changed"] is False


def test_candidate_image_byte_loading_implementation_design_entry_point_boundary() -> None:
    boundary = load_design()["entry_point_boundary"]

    assert boundary["entry_point_name"] == "load_candidate_image_bytes"
    assert boundary["allowed_input"] == [
        "validated_candidate_image_byte_loading_record_fixture",
        "repository_local_candidate_directory_path",
        "explicit_artifact_registry_adapter",
        "explicit_allowed_root_policy",
    ]
    assert "arbitrary_url" in boundary["forbidden_input"]
    assert "arbitrary_absolute_path" in boundary["forbidden_input"]
    assert "implicit_cloud_storage_pointer" in boundary["forbidden_input"]
    assert "unvalidated_manifest_data" in boundary["forbidden_input"]
    assert "no_mutation_of_source_fixtures" in boundary["entry_point_output"]
    assert "no_candidate_approval" in boundary["entry_point_output"]


def test_candidate_image_byte_loading_implementation_design_allowed_root_enforcement() -> None:
    behavior = load_design()["allowed_root_enforcement_behavior"]

    assert behavior["local_file_path"] == [
        "normalize_candidate_path_before_loading",
        "resolve_against_configured_allowed_roots",
        "reject_traversal_outside_allowed_roots",
        "reject_absolute_paths_unless_explicitly_allowlisted_by_policy",
        "fail_closed_on_ambiguity",
    ]
    assert behavior["file_uri"] == [
        "parse_uri_before_path_conversion",
        "allow_only_empty_host_or_localhost",
        "normalize_decoded_path",
        "resolve_against_configured_file_uri_roots",
        "reject_traversal_outside_allowed_roots",
        "fail_closed_on_ambiguity",
    ]


def test_candidate_image_byte_loading_implementation_design_path_normalization_and_artifact_lookup() -> None:
    design = load_design()
    normalization = design["path_normalization_behavior"]["normalization_order"]
    artifact = design["artifact_registry_lookup_behavior"]

    assert normalization == [
        "read_reference_type_and_raw_reference_string",
        "reject_empty_whitespace_only_or_control_character_references",
        "parse_by_reference_type",
        "normalize_separators",
        "collapse_dot_segments",
        "resolve_symlink_behavior_according_to_platform_policy_before_byte_open",
        "confirm_normalized_path_remains_inside_allowed_root",
        "refuse_loading_if_normalized_path_is_ambiguous_or_outside_policy",
    ]
    assert artifact["scheme"] == "artifact://"
    assert artifact["explicit_artifact_registry_adapter_required"] is True
    assert artifact["http_allowed"] is False
    assert artifact["https_allowed"] is False
    assert artifact["implicit_cloud_download_allowed"] is False
    assert artifact["descriptor_required_fields"] == [
        "byte_source",
        "expected_media_type",
        "expected_sha256",
        "expected_byte_count",
    ]
    assert artifact["missing_artifact_behavior"] == "intake_failed"


def test_candidate_image_byte_loading_implementation_design_checksum_size_and_media_behavior_cannot_approve() -> None:
    design = load_design()
    checksum = design["checksum_computation_behavior"]["checksum_order"]
    size = design["size_limit_enforcement_behavior"]
    media = design["media_type_sniffing_behavior"]

    assert checksum == [
        "load_bytes_only_after_reference_policy_passes",
        "compute_sha256_over_exact_loaded_byte_sequence",
        "compare_computed_sha256_to_manifest_image_sha256",
        "record_computed_sha256",
        "fail_intake_on_mismatch",
        "do_not_decode_until_checksum_passes",
        "checksum_match_cannot_approve_candidate",
    ]
    assert size["max_candidate_image_bytes"] == 25000000
    assert "oversize_candidate_produces_intake_failed" in size["size_order"]
    assert "size_compliance_cannot_approve_candidate" in size["size_order"]
    assert media["accepted_media_types"] == ["image/png", "image/jpeg", "image/webp"]
    assert "fail_intake_on_unsupported_or_mismatched_media_type" in media["sniffing_order"]
    assert "media_type_match_cannot_approve_candidate" in media["sniffing_order"]


def test_candidate_image_byte_loading_implementation_design_safe_failure_reporting_cannot_approve() -> None:
    failure = load_design()["safe_failure_reporting_behavior"]

    assert failure["required_fields"] == [
        "failure_code",
        "failure_reason",
        "reference_type",
        "candidate_id",
        "contract_key",
        "image_bytes_loaded",
        "image_decoded",
        "candidate_scoring_ran",
        "approval_allowed",
    ]
    assert failure["defaults"]["image_bytes_loaded"] is False
    assert failure["defaults"]["image_decoded"] is False
    assert failure["defaults"]["candidate_scoring_ran"] is False
    assert failure["defaults"]["approval_allowed"] is False
    assert failure["defaults"]["initial_decision"] == "needs_review_or_intake_failed"


def test_candidate_image_byte_loading_implementation_design_next_gate_blocks_implementation() -> None:
    next_gate = load_design()["next_gate"]

    assert next_gate["recommended_next_milestone"] == "Candidate Image Byte Loading Implementation Contract v1"
    assert "image_byte_loading_implementation" in next_gate["blocked_until_later"]
    assert "image_decoding_implementation" in next_gate["blocked_until_later"]
    assert "pixel_inspection" in next_gate["blocked_until_later"]
    assert "candidate_scoring" in next_gate["blocked_until_later"]
    assert "approval_automation_change" in next_gate["blocked_until_later"]


def test_candidate_image_byte_loading_implementation_design_milestone_matches_fixture_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Implementation Design v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "No image bytes loaded." in content
    assert "No local file opening." in content
    assert "No artifact download." in content
    assert "No remote/network fetch." in content
    assert "No image decoding." in content
    assert "recommended_next_milestone: Candidate Image Byte Loading Implementation Contract v1" in content
    assert "pytest tests/test_candidate_image_byte_loading_implementation_design.py" in content


def test_readme_and_command_reference_include_candidate_image_byte_loading_implementation_design() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_byte_loading_implementation.design.json" in readme
    assert "candidate_image_byte_loading_implementation_design_status: design_only" in readme
    assert "Candidate image byte loading implementation design" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_implementation_design.py" in command_reference
