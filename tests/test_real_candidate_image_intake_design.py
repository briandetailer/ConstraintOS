import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Real_Candidate_Image_Intake_Design_v1.md"
DESIGN_FIXTURE = ROOT / "examples" / "graphics" / "candidate_evaluation" / "real_candidate_image_intake.design.json"
README = ROOT / "examples" / "graphics" / "candidate_evaluation" / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def load_design() -> dict:
    return json.loads(DESIGN_FIXTURE.read_text(encoding="utf-8"))


def test_real_candidate_image_intake_design_is_design_only() -> None:
    design = load_design()["real_candidate_image_intake_design"]

    assert design["status"] == "design_only"
    assert design["image_loading_implemented"] is False
    assert design["image_decoding_implemented"] is False
    assert design["network_fetch_implemented"] is False
    assert design["computer_vision_implemented"] is False
    assert design["ocr_implemented"] is False
    assert design["candidate_scoring_implemented"] is False
    assert design["approval_automation_changed"] is False


def test_real_candidate_image_intake_design_accepts_limited_reference_types() -> None:
    design = load_design()
    reference_types = {item["reference_type"] for item in design["accepted_reference_types"]}

    assert reference_types == {"artifact_uri", "local_file_path", "file_uri"}
    local_policy_items = [item for item in design["accepted_reference_types"] if item["reference_type"] in {"local_file_path", "file_uri"}]
    assert all(item["requires_workspace_policy"] is True for item in local_policy_items)


def test_real_candidate_image_intake_design_forbids_network_and_path_escape_behavior() -> None:
    design = load_design()
    forbidden = set(design["forbidden_reference_behaviors"])

    assert "http_image_fetch" in forbidden
    assert "https_image_fetch" in forbidden
    assert "arbitrary_network_retrieval" in forbidden
    assert "redirect_following" in forbidden
    assert "implicit_cloud_provider_download" in forbidden
    assert "shell_open_file" in forbidden
    assert "path_traversal_outside_allowed_roots" in forbidden


def test_real_candidate_image_intake_states_cannot_approve() -> None:
    design = load_design()

    for state in design["intake_states"]:
        assert state["approval_allowed"] is False
    assert {state["state"] for state in design["intake_states"]} == {
        "reference_only_not_loaded",
        "intake_design_only",
        "intake_pending",
        "intake_failed",
        "intake_loaded_not_evaluated",
    }


def test_real_candidate_image_intake_checksum_and_media_type_policy() -> None:
    design = load_design()
    checksum = design["checksum_policy"]
    media = design["media_type_policy"]

    assert checksum["preferred_checksum"] == "image_sha256"
    assert checksum["missing_checksum_decision"] == "needs_review"
    assert checksum["checksum_mismatch_decision"] == "rejected_or_intake_failed_after_policy_confirmation"
    assert checksum["checksum_alone_can_approve"] is False
    assert media["accepted_media_types"] == ["image/png", "image/jpeg", "image/webp"]
    assert media["unsupported_media_type_decision"] == "needs_review"
    assert media["approval_allowed_for_unsupported_media_type"] is False


def test_real_candidate_image_intake_byte_handling_keeps_pixels_separate() -> None:
    policy = load_design()["byte_handling_policy"]

    assert policy["treat_bytes_as_untrusted"] is True
    assert policy["execute_embedded_content"] is False
    assert policy["successful_load_can_approve"] is False
    assert policy["preserve_original_reference_metadata"] is True
    assert policy["future_record_byte_count"] is True
    assert policy["future_record_checksum"] is True
    assert policy["decoded_pixel_inspection_separate_from_intake"] is True


def test_real_candidate_image_intake_failure_states_cannot_approve() -> None:
    design = load_design()
    failure_states = {item["state"]: item for item in design["failure_states"]}

    assert failure_states["missing_reference"]["decision"] == "needs_review"
    assert failure_states["missing_checksum"]["decision"] == "needs_review"
    assert failure_states["unreadable_candidate"]["decision"] == "needs_review"
    assert failure_states["unsupported_media_type"]["decision"] == "needs_review"
    assert failure_states["checksum_mismatch"]["decision"] == "rejected_or_intake_failed_after_policy_confirmation"
    assert failure_states["outside_allowed_root"]["decision"] == "rejected_or_intake_failed_after_policy_confirmation"
    assert all(item["approval_allowed"] is False for item in failure_states.values())


def test_real_candidate_image_intake_design_sets_next_gate() -> None:
    design = load_design()
    next_gate = design["next_gate"]

    assert next_gate["recommended_next_milestone"] == "Candidate Intake Manifest Contract v1"
    assert "image_byte_loading_implementation" in next_gate["blocked_until_later"]
    assert "image_decoding_implementation" in next_gate["blocked_until_later"]
    assert "approval_automation_change" in next_gate["blocked_until_later"]


def test_real_candidate_image_intake_milestone_matches_fixture_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "status: implementation-complete-pending-test" in content
    assert "No image bytes loaded." in content
    assert "No remote/network fetch." in content
    assert "No image decoding." in content
    assert "recommended_next_milestone: Candidate Intake Manifest Contract v1" in content
    assert "pytest tests/test_real_candidate_image_intake_design.py" in content


def test_readme_and_command_reference_include_real_candidate_image_intake_design() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "real_candidate_image_intake.design.json" in readme
    assert "real_candidate_image_intake_status: design_only" in readme
    assert "Real candidate image intake design" in command_reference
    assert "pytest tests/test_real_candidate_image_intake_design.py" in command_reference
