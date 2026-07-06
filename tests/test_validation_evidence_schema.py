import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from constraintos.cli import validate_against_schema
from constraintos.schema_registry import detect_record_type, detect_schema
from constraintos.validation.models import ALLOWED_EVIDENCE_STATUSES, PASSING_EVIDENCE_STATUSES, ValidationEvidence

EVIDENCE = Path("examples/validation/lf4_passing_evidence.yaml")
REPO_ROOT = Path(".")


def test_detect_validation_evidence_schema() -> None:
    data = {"evidence": []}

    assert detect_schema(data) == "schemas/validation-evidence.schema.json"
    assert detect_record_type(data) == "validation_evidence"


def test_lf4_validation_evidence_example_validates() -> None:
    payload = yaml.safe_load(EVIDENCE.read_text(encoding="utf-8"))

    assert validate_against_schema(EVIDENCE, payload, REPO_ROOT) == []


def test_validation_evidence_requires_gate_id() -> None:
    schema = json.loads(Path("schemas/validation-evidence.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    payload = {"evidence": [{"status": "passed"}]}

    errors = list(validator.iter_errors(payload))

    assert any("gate_id" in error.message for error in errors)


def test_validation_evidence_gate_id_must_use_gate_pattern() -> None:
    schema = json.loads(Path("schemas/validation-evidence.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    payload = {"evidence": [{"gate_id": "BAD-GATE", "status": "passed"}]}

    errors = list(validator.iter_errors(payload))

    assert any("does not match" in error.message for error in errors)


def test_validation_evidence_status_must_use_known_vocabulary() -> None:
    schema = json.loads(Path("schemas/validation-evidence.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    payload = {"evidence": [{"gate_id": "GATE-0001", "status": "maybe"}]}

    errors = list(validator.iter_errors(payload))

    assert any("is not one of" in error.message for error in errors)


def test_validation_evidence_status_vocabulary_matches_model() -> None:
    assert ALLOWED_EVIDENCE_STATUSES == {
        "pass",
        "passed",
        "complete",
        "approved",
        "fail",
        "failed",
        "rejected",
    }
    assert PASSING_EVIDENCE_STATUSES == {"pass", "passed", "complete", "approved"}


def test_validation_evidence_passed_uses_status_vocabulary() -> None:
    assert ValidationEvidence("GATE-0001", "approved").passed() is True
    assert ValidationEvidence("GATE-0001", "rejected").passed() is False
