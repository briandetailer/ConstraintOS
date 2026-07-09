import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
SCHEMA = CANDIDATE_DIR / "candidate_image_byte_loading_implementation_contract.schema.json"
FIXTURE = CANDIDATE_DIR / "candidate_image_byte_loading_implementation_contract.fixture.json"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Implementation_Contract_v1.md"
README = CANDIDATE_DIR / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_candidate_image_byte_loading_implementation_contract_schema_requires_core_sections() -> None:
    schema = load_json(SCHEMA)

    assert schema["title"] == "ConstraintOS Candidate Image Byte Loading Implementation Contract"
    assert schema["required"] == [
        "candidate_image_byte_loading_implementation_contract",
        "input_binding",
        "policy_enforcement_result_contract",
        "reference_resolution_result_contract",
        "byte_loading_result_contract",
        "validation_result_contract",
        "safe_failure_contract",
        "post_contract_boundary",
    ]


def test_candidate_image_byte_loading_implementation_contract_fixture_validates_against_schema() -> None:
    schema = load_json(SCHEMA)
    fixture = load_json(FIXTURE)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(fixture), key=lambda error: list(error.path))

    assert errors == []


def test_candidate_image_byte_loading_implementation_contract_remains_not_implemented() -> None:
    fixture = load_json(FIXTURE)
    contract = fixture["candidate_image_byte_loading_implementation_contract"]

    assert contract["id"] == "CANDIDATE-IMAGE-BYTE-LOADING-IMPLEMENTATION-CONTRACT-V1"
    assert contract["version"] == "v1"
    assert contract["domain"] == "graphics_validation"
    assert contract["status"] == "contract_only"
    assert contract["contract_state"] == "not_implemented"
    assert contract["implementation_allowed"] is False


def test_candidate_image_byte_loading_implementation_contract_requires_validated_inputs() -> None:
    binding = load_json(FIXTURE)["input_binding"]

    assert binding["source_byte_loading_record_schema"] == "candidate_image_byte_loading_record.schema.json"
    assert binding["source_byte_loading_record_fixture_required"] is True
    assert binding["source_intake_manifest_required"] is True
    assert binding["explicit_artifact_registry_adapter_required"] is True
    assert binding["explicit_allowed_root_policy_required"] is True
    assert binding["unvalidated_manifest_data_allowed"] is False


def test_candidate_image_byte_loading_implementation_contract_blocks_network_and_cloud_resolution() -> None:
    fixture = load_json(FIXTURE)
    policy = fixture["policy_enforcement_result_contract"]
    resolution = fixture["reference_resolution_result_contract"]

    assert policy["reference_type_allowed"] == "future_boolean"
    assert policy["allowed_root_checked"] == "future_boolean"
    assert policy["path_normalized"] == "future_boolean"
    assert policy["traversal_rejected"] == "future_boolean"
    assert policy["network_fetch_allowed"] is False
    assert policy["implicit_cloud_download_allowed"] is False
    assert resolution["reference_resolved"] == "future_boolean"
    assert resolution["resolved_reference_kind"] == ["local_file_path", "file_uri", "artifact_descriptor", "safe_failure"]
    assert resolution["artifact_descriptor_required"] is True
    assert resolution["resolved_byte_source_mutable"] is False
    assert resolution["http_resolution_allowed"] is False
    assert resolution["https_resolution_allowed"] is False


def test_candidate_image_byte_loading_implementation_contract_result_envelope_cannot_approve() -> None:
    fixture = load_json(FIXTURE)
    result = fixture["byte_loading_result_contract"]
    validation = fixture["validation_result_contract"]

    assert result["image_bytes_loaded"] == "future_boolean"
    assert result["local_file_opened"] == "future_boolean"
    assert result["artifact_downloaded"] is False
    assert result["network_fetch_ran"] is False
    assert result["actual_loaded_byte_count"] == "future_integer_or_null"
    assert result["computed_sha256"] == "future_sha256_or_null"
    assert result["sniffed_media_type"] == "future_media_type_or_null"
    assert validation["byte_count_within_limit"] == "future_boolean_or_null"
    assert validation["checksum_matches"] == "future_boolean_or_null"
    assert validation["media_type_matches"] == "future_boolean_or_null"
    assert validation["safe_to_decode"] == "future_boolean"
    assert validation["approval_allowed"] is False


def test_candidate_image_byte_loading_implementation_contract_safe_failure_fields() -> None:
    failure = load_json(FIXTURE)["safe_failure_contract"]

    assert failure["failure_code"] == "future_string_or_null"
    assert failure["failure_reason"] == "future_string_or_null"
    assert failure["initial_decision"] == "needs_review"
    assert failure["approval_allowed"] is False
    assert set(failure["failure_codes"]) >= {
        "reference_type_not_allowed",
        "outside_allowed_root",
        "path_traversal_detected",
        "artifact_not_found",
        "checksum_mismatch",
        "oversize_candidate",
        "unsupported_media_type",
        "media_type_mismatch",
        "unreadable_candidate",
    }


def test_candidate_image_byte_loading_implementation_contract_keeps_post_contract_work_blocked() -> None:
    boundary = load_json(FIXTURE)["post_contract_boundary"]

    assert boundary["image_decoding_implemented"] is False
    assert boundary["pixel_inspection_implemented"] is False
    assert boundary["computer_vision_implemented"] is False
    assert boundary["ocr_implemented"] is False
    assert boundary["candidate_scoring_implemented"] is False
    assert boundary["approval_automation_changed"] is False


def test_candidate_image_byte_loading_implementation_contract_milestone_records_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Implementation Contract v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "No image bytes loaded." in content
    assert "No local file opening." in content
    assert "No artifact download." in content
    assert "No remote/network fetch." in content
    assert "No image decoding." in content
    assert "recommended_next_milestone: Candidate Image Byte Loading Pre-Implementation Exit Review v1" in content
    assert "pytest tests/test_candidate_image_byte_loading_implementation_contract.py" in content


def test_readme_and_command_reference_include_candidate_image_byte_loading_implementation_contract() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_byte_loading_implementation_contract.schema.json" in readme
    assert "candidate_image_byte_loading_implementation_contract_status: contract_only" in readme
    assert "Candidate image byte loading implementation contract" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_implementation_contract.py" in command_reference
