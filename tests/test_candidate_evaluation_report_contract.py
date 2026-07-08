import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"
REPORT_SCHEMA_PATH = CANDIDATE_DIR / "candidate_evaluation_report.schema.json"
REPORT_FILES = [
    "perseverance_candidate_evaluation_report.fixture.json",
    "supra_2jz_gte_candidate_evaluation_report.fixture.json",
]
MANIFEST_BY_REPORT = {
    "perseverance_candidate_evaluation_report.fixture.json": "perseverance_candidate_manifest.fixture.json",
    "supra_2jz_gte_candidate_evaluation_report.fixture.json": "supra_2jz_gte_candidate_manifest.fixture.json",
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def validate_report(report: dict) -> None:
    schema = load_json(REPORT_SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(report), key=lambda error: list(error.path))
    assert errors == []


@pytest.mark.parametrize("report_file", REPORT_FILES)
def test_candidate_evaluation_report_fixture_satisfies_schema(report_file: str) -> None:
    validate_report(load_json(CANDIDATE_DIR / report_file))


@pytest.mark.parametrize("report_file", REPORT_FILES)
def test_candidate_evaluation_report_is_fixture_only(report_file: str) -> None:
    report = load_json(CANDIDATE_DIR / report_file)

    assert report["evaluation_report"]["domain"] == "graphics_validation"
    assert report["evaluation_report"]["status"] == "fixture_only"
    assert report["evaluation_report"]["report_mode"] == "contract_shape_only_no_image_evaluation"


@pytest.mark.parametrize("report_file", REPORT_FILES)
def test_candidate_evaluation_report_blocks_runtime_evaluation_claims(report_file: str) -> None:
    report = load_json(CANDIDATE_DIR / report_file)
    boundary = report["evaluation_boundary"]

    assert boundary == {
        "image_generation_ran": False,
        "image_editing_ran": False,
        "real_image_ingestion_ran": False,
        "computer_vision_integration_ran": False,
        "candidate_evaluation_ran": False,
        "approval_automation_ran": False,
    }


@pytest.mark.parametrize("report_file", REPORT_FILES)
def test_candidate_evaluation_report_keeps_all_evidence_not_observed(report_file: str) -> None:
    report = load_json(CANDIDATE_DIR / report_file)
    summary = report["evidence_summary"]
    evidence_items = report["evidence_items"]

    assert summary["total_items"] == len(evidence_items)
    assert summary["not_observed_count"] == len(evidence_items)
    assert summary["satisfied_count"] == 0
    assert summary["missing_count"] == 0
    assert summary["ambiguous_count"] == 0
    assert summary["contradicted_count"] == 0
    assert summary["overall_evidence_status"] == "not_observed"
    assert all(item["observed_status"] == "not_observed" for item in evidence_items)
    assert all(item["evidence_source"] == "fixture_only_no_image_evidence" for item in evidence_items)
    assert all(item["confidence"] == 0 for item in evidence_items)


@pytest.mark.parametrize("report_file", REPORT_FILES)
def test_candidate_evaluation_report_recommends_needs_review(report_file: str) -> None:
    report = load_json(CANDIDATE_DIR / report_file)
    recommendation = report["recommendation"]

    assert recommendation["allowed_decisions"] == ["approved", "needs_review", "rejected"]
    assert recommendation["recommended_decision"] == "needs_review"
    assert recommendation["uncertainty_default"] == "needs_review"
    assert recommendation["approval_allowed"] is False


@pytest.mark.parametrize("report_file", REPORT_FILES)
def test_candidate_evaluation_report_binding_matches_candidate_manifest(report_file: str) -> None:
    report = load_json(CANDIDATE_DIR / report_file)
    manifest = load_json(CANDIDATE_DIR / MANIFEST_BY_REPORT[report_file])

    assert report["candidate_binding"]["candidate_manifest_id"] == manifest["candidate_manifest"]["id"]
    assert report["candidate_binding"]["candidate_id"] == manifest["candidate_manifest"]["candidate_id"]
    assert report["candidate_binding"]["contract_key"] == manifest["contract_binding"]["contract_key"]
    assert report["candidate_binding"]["candidate_reference_status"] == manifest["candidate_reference"]["reference_status"]


def test_candidate_evaluation_report_schema_rejects_evaluation_claims() -> None:
    report = load_json(CANDIDATE_DIR / "perseverance_candidate_evaluation_report.fixture.json")
    report["evaluation_boundary"]["candidate_evaluation_ran"] = True

    schema = load_json(REPORT_SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(report), key=lambda error: list(error.path))

    assert errors
    assert any("False was expected" in error.message for error in errors)


def test_candidate_evaluation_report_schema_rejects_approved_recommendation() -> None:
    report = load_json(CANDIDATE_DIR / "perseverance_candidate_evaluation_report.fixture.json")
    report["recommendation"]["recommended_decision"] = "approved"

    schema = load_json(REPORT_SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(report), key=lambda error: list(error.path))

    assert errors
    assert any("'needs_review' was expected" in error.message for error in errors)


def test_command_reference_includes_candidate_evaluation_report_contract_verification() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Candidate evaluation report contract" in content
    assert "pytest tests/test_candidate_evaluation_report_contract.py" in content
