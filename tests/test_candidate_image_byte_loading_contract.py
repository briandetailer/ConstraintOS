import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
SCHEMA = CANDIDATE_DIR / "candidate_image_byte_loading_record.schema.json"
PERSEVERANCE = CANDIDATE_DIR / "perseverance_candidate_image_byte_loading_record.fixture.json"
SUPRA = CANDIDATE_DIR / "supra_2jz_gte_candidate_image_byte_loading_record.fixture.json"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Contract_v1.md"
README = CANDIDATE_DIR / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"
FIXTURE_PNG_SHA256 = "4c4b6a3be1314ab86138bef4314dde022e600960d8689a2c8f8631802d20dab6"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_fixture(path: Path) -> dict:
    schema = load_json(SCHEMA)
    fixture = load_json(path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(fixture), key=lambda error: list(error.path))
    assert errors == []
    return fixture


def test_candidate_image_byte_loading_record_schema_exists_and_requires_core_sections() -> None:
    schema = load_json(SCHEMA)

    assert schema["title"] == "ConstraintOS Graphics Candidate Image Byte Loading Record"
    assert schema["required"] == [
        "candidate_image_byte_loading_record",
        "contract_binding",
        "reference_snapshot",
        "byte_loading_policy_snapshot",
        "byte_loading_result",
        "post_load_boundary",
        "approval_expectation",
    ]


def test_candidate_image_byte_loading_record_fixtures_validate_against_schema() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        assert fixture["candidate_image_byte_loading_record"]["status"] == "static_fixture_only"
        assert fixture["candidate_image_byte_loading_record"]["byte_loading_state"] == "not_run_contract_only"


def test_candidate_image_byte_loading_records_bind_to_intake_manifests() -> None:
    perseverance = validate_fixture(PERSEVERANCE)
    supra = validate_fixture(SUPRA)

    assert perseverance["contract_binding"]["candidate_intake_manifest_required"] is True
    assert perseverance["contract_binding"]["candidate_intake_manifest_id"] == "GRAPHICS-CANDIDATE-INTAKE-MANIFEST-PERSEVERANCE-0001"
    assert perseverance["contract_binding"]["contract_key"] == "perseverance"
    assert supra["contract_binding"]["candidate_intake_manifest_required"] is True
    assert supra["contract_binding"]["candidate_intake_manifest_id"] == "GRAPHICS-CANDIDATE-INTAKE-MANIFEST-SUPRA-2JZ-GTE-0001"
    assert supra["contract_binding"]["contract_key"] == "supra_2jz_gte_twin_turbo"


def test_candidate_image_byte_loading_records_preserve_reference_metadata() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        reference = fixture["reference_snapshot"]

        assert reference["reference_type"] == "artifact_uri"
        assert reference["media_type"] == "image/png"
        assert reference["image_sha256"] == FIXTURE_PNG_SHA256
        assert reference["expected_byte_count"] == 8


def test_candidate_image_byte_loading_policy_snapshot_blocks_fetch_and_approval() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        policy = fixture["byte_loading_policy_snapshot"]

        assert policy["allowed_local_roots"] == ["./external-candidates/", "./runs/manual-candidates/"]
        assert policy["allowed_file_uri_roots"] == [
            "file:///workspace/external-candidates/",
            "file:///workspace/runs/manual-candidates/",
        ]
        assert policy["artifact_uri_resolution"] == "deterministic_fixture_artifact_registry_only"
        assert policy["max_candidate_image_bytes"] == 25000000
        assert policy["network_fetch_allowed"] is False
        assert policy["implicit_cloud_download_allowed"] is False
        assert policy["byte_loading_success_can_approve"] is False


def test_candidate_image_byte_loading_result_does_not_load_anything() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        result = fixture["byte_loading_result"]

        assert result["image_bytes_loaded"] is False
        assert result["local_file_opened"] is False
        assert result["artifact_downloaded"] is False
        assert result["network_fetch_ran"] is False
        assert result["actual_loaded_byte_count"] is None
        assert result["computed_sha256"] is None
        assert result["sniffed_media_type"] is None
        assert result["byte_count_within_limit"] is None
        assert result["checksum_matches"] is None
        assert result["media_type_matches"] is None


def test_candidate_image_byte_loading_post_load_boundary_remains_disabled() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        boundary = fixture["post_load_boundary"]

        assert boundary["image_decoded"] is False
        assert boundary["pixel_inspection_ran"] is False
        assert boundary["computer_vision_ran"] is False
        assert boundary["ocr_ran"] is False
        assert boundary["candidate_scoring_ran"] is False
        assert boundary["source_report_mutation_ran"] is False
        assert boundary["approval_automation_ran"] is False


def test_candidate_image_byte_loading_contract_cannot_approve() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        approval = fixture["approval_expectation"]

        assert approval["initial_decision"] == "needs_review"
        assert approval["uncertainty_default"] == "needs_review"
        assert approval["approval_allowed"] is False
        assert "cannot approve" in approval["guardrail"]


def test_candidate_image_byte_loading_contract_milestone_records_boundaries() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Contract v1" in content
    assert "status: complete" in content
    assert "No image bytes loaded." in content
    assert "No local file opening." in content
    assert "No artifact download." in content
    assert "No remote/network fetch." in content
    assert "recommended_next_milestone: Candidate Image Byte Loading Discovery v1" in content
    assert "pytest tests/test_candidate_image_byte_loading_contract.py" in content


def test_readme_and_command_reference_include_candidate_image_byte_loading_contract() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_byte_loading_record.schema.json" in readme
    assert "candidate_image_byte_loading_contract_status: static_fixture_only" in readme
    assert "Candidate image byte loading contract" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_contract.py" in command_reference
