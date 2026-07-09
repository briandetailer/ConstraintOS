import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN_FIXTURE = ROOT / "examples" / "graphics" / "candidate_evaluation" / "candidate_image_byte_loading.design.json"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Design_v1.md"
README = ROOT / "examples" / "graphics" / "candidate_evaluation" / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def load_design() -> dict:
    return json.loads(DESIGN_FIXTURE.read_text(encoding="utf-8"))


def test_candidate_image_byte_loading_design_is_design_only() -> None:
    design = load_design()["candidate_image_byte_loading_design"]

    assert design["status"] == "design_only"
    assert design["image_byte_loading_implemented"] is False
    assert design["local_file_opening_implemented"] is False
    assert design["artifact_download_implemented"] is False
    assert design["network_fetch_implemented"] is False
    assert design["image_decoding_implemented"] is False
    assert design["pixel_inspection_implemented"] is False
    assert design["computer_vision_implemented"] is False
    assert design["ocr_implemented"] is False
    assert design["candidate_scoring_implemented"] is False
    assert design["approval_automation_changed"] is False


def test_candidate_image_byte_loading_design_defines_allowed_roots_policy() -> None:
    policy = load_design()["allowed_roots_policy"]
    local = policy["local_file_path"]
    file_uri = policy["file_uri"]

    assert local["allowed_roots"] == ["./external-candidates/", "./runs/manual-candidates/"]
    assert local["normalize_before_loading"] is True
    assert local["reject_path_traversal"] is True
    assert local["reject_absolute_paths_unless_allowlisted_later"] is True
    assert local["reject_outside_allowed_roots"] is True
    assert file_uri["allowed_roots"] == [
        "file:///workspace/external-candidates/",
        "file:///workspace/runs/manual-candidates/",
    ]
    assert file_uri["allowed_hosts"] == ["", "localhost"]
    assert file_uri["reject_path_traversal"] is True
    assert file_uri["reject_outside_allowed_roots"] is True


def test_candidate_image_byte_loading_design_blocks_network_artifact_downloads() -> None:
    artifact = load_design()["artifact_uri_policy"]

    assert artifact["status"] == "design_only"
    assert artifact["allowed_scheme"] == "artifact://"
    assert artifact["resolution"] == "internal_artifact_registry_required_later"
    assert artifact["network_fetch_allowed"] is False
    assert artifact["implicit_cloud_download_allowed"] is False
    assert artifact["missing_artifact_behavior"] == "intake_failed"


def test_candidate_image_byte_loading_design_sets_size_checksum_and_decode_order() -> None:
    design = load_design()
    size_policy = design["maximum_byte_size_policy"]
    order = design["checksum_verification_order"]

    assert size_policy["max_candidate_image_bytes"] == 25000000
    assert size_policy["oversize_behavior"] == "intake_failed"
    assert size_policy["approval_allowed"] is False
    assert order == [
        "resolve_reference_metadata_without_loading_bytes",
        "confirm_reference_type_is_allowed",
        "confirm_image_sha256_metadata_is_present",
        "load_bytes_only_in_future_implementation",
        "compute_sha256_from_loaded_bytes",
        "compare_computed_sha256_to_manifest_image_sha256",
        "fail_intake_on_checksum_mismatch",
        "do_not_decode_until_checksum_passes",
    ]


def test_candidate_image_byte_loading_design_media_type_and_byte_count_policy_cannot_approve() -> None:
    design = load_design()
    media = design["media_type_sniffing_policy"]
    byte_count = design["byte_count_recording_policy"]

    assert media["accepted_media_types"] == ["image/png", "image/jpeg", "image/webp"]
    assert media["declared_media_type_required_before_loading"] is True
    assert media["record_sniffed_media_type_after_future_loading"] is True
    assert media["declared_and_sniffed_media_types_must_agree"] is True
    assert media["unsupported_or_mismatched_media_type_behavior"] == "intake_failed"
    assert media["media_type_validation_can_approve"] is False
    assert byte_count["required_future_records"] == [
        "declared_expected_byte_count",
        "actual_loaded_byte_count",
        "max_candidate_image_bytes",
        "byte_count_within_limit",
    ]
    assert byte_count["byte_count_success_can_approve"] is False


def test_candidate_image_byte_loading_design_failure_states_cannot_approve() -> None:
    failure_states = {item["state"]: item for item in load_design()["failure_states"]}

    assert failure_states["reference_type_not_allowed"]["decision"] == "intake_failed"
    assert failure_states["outside_allowed_root"]["decision"] == "intake_failed"
    assert failure_states["path_traversal_detected"]["decision"] == "intake_failed"
    assert failure_states["artifact_not_found"]["decision"] == "intake_failed"
    assert failure_states["missing_checksum"]["decision"] == "needs_review"
    assert failure_states["checksum_mismatch"]["decision"] == "intake_failed"
    assert failure_states["oversize_candidate"]["decision"] == "intake_failed"
    assert failure_states["unsupported_media_type"]["decision"] == "intake_failed"
    assert failure_states["media_type_mismatch"]["decision"] == "intake_failed"
    assert failure_states["unreadable_candidate"]["decision"] == "needs_review"
    assert all(item["approval_allowed"] is False for item in failure_states.values())


def test_candidate_image_byte_loading_design_sets_next_gate() -> None:
    next_gate = load_design()["next_gate"]

    assert next_gate["recommended_next_milestone"] == "Candidate Image Byte Loading Contract v1"
    assert "image_byte_loading_implementation" in next_gate["blocked_until_later"]
    assert "image_decoding_implementation" in next_gate["blocked_until_later"]
    assert "pixel_inspection" in next_gate["blocked_until_later"]
    assert "approval_automation_change" in next_gate["blocked_until_later"]


def test_candidate_image_byte_loading_design_milestone_matches_fixture_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Design v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "No image bytes loaded." in content
    assert "No local file opening." in content
    assert "No artifact download." in content
    assert "No remote/network fetch." in content
    assert "No image decoding." in content
    assert "recommended_next_milestone: Candidate Image Byte Loading Contract v1" in content
    assert "pytest tests/test_candidate_image_byte_loading_design.py" in content


def test_readme_and_command_reference_include_candidate_image_byte_loading_design() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_byte_loading.design.json" in readme
    assert "candidate_image_byte_loading_status: design_only" in readme
    assert "Candidate image byte loading design" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_design.py" in command_reference
