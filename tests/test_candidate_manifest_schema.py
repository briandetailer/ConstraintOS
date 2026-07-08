import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
CONTRACT_DIR = ROOT / "examples" / "graphics" / "contracts"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"
SCHEMA_PATH = CANDIDATE_DIR / "candidate_manifest.schema.json"
MANIFEST_FILES = [
    "perseverance_candidate_manifest.fixture.json",
    "supra_2jz_gte_candidate_manifest.fixture.json",
]
EXPECTED_CONTRACT_KEYS = {
    "perseverance",
    "wind_turbine_nacelle",
    "hydroelectric_dam_powerhouse",
    "supra_2jz_gte_twin_turbo",
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def validate_manifest(manifest: dict) -> None:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.path))
    assert errors == []


@pytest.mark.parametrize("manifest_file", MANIFEST_FILES)
def test_candidate_manifest_fixture_satisfies_schema(manifest_file: str) -> None:
    validate_manifest(load_json(CANDIDATE_DIR / manifest_file))


@pytest.mark.parametrize("manifest_file", MANIFEST_FILES)
def test_candidate_manifest_is_static_external_reference_only(manifest_file: str) -> None:
    manifest = load_json(CANDIDATE_DIR / manifest_file)

    assert manifest["candidate_manifest"]["domain"] == "graphics_validation"
    assert manifest["candidate_manifest"]["status"] == "static_fixture_only"
    assert manifest["candidate_reference"]["reference_status"] == "reference_only_not_loaded"
    assert manifest["candidate_source"]["candidate_source_type"] == "external"
    assert manifest["candidate_source"]["generated_by_constraintos"] is False


@pytest.mark.parametrize("manifest_file", MANIFEST_FILES)
def test_candidate_manifest_blocks_generation_ingestion_and_evaluation(manifest_file: str) -> None:
    manifest = load_json(CANDIDATE_DIR / manifest_file)
    boundary = manifest["evaluation_boundary"]

    assert boundary["image_generation_allowed"] is False
    assert boundary["image_editing_allowed"] is False
    assert boundary["real_image_ingestion_allowed"] is False
    assert boundary["computer_vision_integration_allowed"] is False
    assert boundary["evaluation_status"] == "not_evaluated"
    assert boundary["image_bytes_embedded"] is False


@pytest.mark.parametrize("manifest_file", MANIFEST_FILES)
def test_candidate_manifest_defaults_approval_to_needs_review(manifest_file: str) -> None:
    manifest = load_json(CANDIDATE_DIR / manifest_file)
    approval = manifest["approval_expectation"]

    assert approval["allowed_decisions"] == ["approved", "needs_review", "rejected"]
    assert approval["initial_decision"] == "needs_review"
    assert approval["uncertainty_default"] == "needs_review"
    assert approval["guardrail"] == "Uncertainty must produce needs_review, not approval."


@pytest.mark.parametrize("manifest_file", MANIFEST_FILES)
def test_candidate_manifest_contract_binding_matches_existing_contract_keys(manifest_file: str) -> None:
    manifest = load_json(CANDIDATE_DIR / manifest_file)
    contract_key = manifest["contract_binding"]["contract_key"]
    allowed_contract_keys = set(manifest["contract_binding"]["allowed_contract_keys"])

    assert allowed_contract_keys == EXPECTED_CONTRACT_KEYS
    assert contract_key in EXPECTED_CONTRACT_KEYS
    assert (CONTRACT_DIR / f"{contract_key}.contract.json").exists()


def test_candidate_manifest_schema_rejects_constraintos_generated_candidates() -> None:
    manifest = load_json(CANDIDATE_DIR / "perseverance_candidate_manifest.fixture.json")
    manifest["candidate_source"]["generated_by_constraintos"] = True

    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.path))

    assert errors
    assert any("False was expected" in error.message for error in errors)


def test_candidate_manifest_schema_rejects_approved_initial_decision() -> None:
    manifest = load_json(CANDIDATE_DIR / "perseverance_candidate_manifest.fixture.json")
    manifest["approval_expectation"]["initial_decision"] = "approved"

    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.path))

    assert errors
    assert any("'needs_review' was expected" in error.message for error in errors)


def test_command_reference_includes_candidate_manifest_schema_verification() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Candidate manifest schema" in content
    assert "pytest tests/test_candidate_manifest_schema.py" in content
