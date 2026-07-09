import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
SCHEMA = CANDIDATE_DIR / "candidate_intake_manifest.schema.json"
PERSEVERANCE = CANDIDATE_DIR / "perseverance_candidate_intake_manifest.fixture.json"
SUPRA = CANDIDATE_DIR / "supra_2jz_gte_candidate_intake_manifest.fixture.json"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Intake_Manifest_Contract_v1.md"
README = CANDIDATE_DIR / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_fixture(path: Path) -> dict:
    schema = load_json(SCHEMA)
    fixture = load_json(path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(fixture), key=lambda error: list(error.path))
    assert errors == []
    return fixture


def test_candidate_intake_manifest_schema_exists_and_requires_core_sections() -> None:
    schema = load_json(SCHEMA)

    assert schema["title"] == "ConstraintOS Graphics Candidate Intake Manifest"
    assert schema["required"] == [
        "candidate_intake_manifest",
        "contract_binding",
        "candidate_reference",
        "candidate_source",
        "intake_policy_snapshot",
        "intake_boundary",
        "approval_expectation",
    ]


def test_candidate_intake_manifest_fixtures_validate_against_schema() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        assert fixture["candidate_intake_manifest"]["status"] == "static_fixture_only"


def test_candidate_intake_manifest_reference_types_are_limited() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        reference = fixture["candidate_reference"]
        policy = fixture["intake_policy_snapshot"]

        assert reference["reference_type"] in {"artifact_uri", "local_file_path", "file_uri"}
        assert set(policy["accepted_reference_types"]) == {"artifact_uri", "local_file_path", "file_uri"}
        assert reference["reference_status"] == "intake_pending"


def test_candidate_intake_manifest_requires_checksum_and_media_type() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        reference = fixture["candidate_reference"]
        policy = fixture["intake_policy_snapshot"]

        assert len(reference["image_sha256"]) == 64
        assert reference["media_type"] in {"image/png", "image/jpeg", "image/webp"}
        assert set(policy["accepted_media_types"]) == {"image/png", "image/jpeg", "image/webp"}
        assert policy["checksum_required"] is True


def test_candidate_intake_manifest_blocks_network_fetches() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        policy = fixture["intake_policy_snapshot"]
        forbidden = set(policy["forbidden_reference_behaviors"])

        assert policy["network_fetch_allowed"] is False
        assert "http_image_fetch" in forbidden
        assert "https_image_fetch" in forbidden
        assert "arbitrary_network_retrieval" in forbidden
        assert "redirect_following" in forbidden
        assert "path_traversal_outside_allowed_roots" in forbidden


def test_candidate_intake_manifest_boundary_keeps_runtime_work_disabled() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        boundary = fixture["intake_boundary"]

        assert boundary["image_bytes_loaded"] is False
        assert boundary["image_decoded"] is False
        assert boundary["pixel_inspection_ran"] is False
        assert boundary["computer_vision_ran"] is False
        assert boundary["ocr_ran"] is False
        assert boundary["candidate_scoring_ran"] is False
        assert boundary["approval_automation_ran"] is False
        assert boundary["source_report_mutation_ran"] is False


def test_candidate_intake_manifest_cannot_approve() -> None:
    for path in [PERSEVERANCE, SUPRA]:
        fixture = validate_fixture(path)
        approval = fixture["approval_expectation"]
        policy = fixture["intake_policy_snapshot"]

        assert approval["initial_decision"] == "needs_review"
        assert approval["uncertainty_default"] == "needs_review"
        assert approval["approval_allowed"] is False
        assert policy["successful_intake_can_approve"] is False


def test_candidate_intake_manifest_milestone_records_contract_boundaries() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Intake Manifest Contract v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "No image bytes loaded." in content
    assert "No remote/network fetch." in content
    assert "recommended_next_milestone: Candidate Intake Manifest Discovery v1" in content
    assert "pytest tests/test_candidate_intake_manifest_contract.py" in content


def test_readme_and_command_reference_include_candidate_intake_manifest_contract() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_intake_manifest.schema.json" in readme
    assert "candidate_intake_manifest_status: static_fixture_only" in readme
    assert "Candidate intake manifest contract" in command_reference
    assert "pytest tests/test_candidate_intake_manifest_contract.py" in command_reference
