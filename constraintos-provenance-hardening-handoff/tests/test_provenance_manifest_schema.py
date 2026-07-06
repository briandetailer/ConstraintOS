from pathlib import Path

import pytest

from constraintos.cli import load_json, load_yaml, validate_against_schema

Draft202012Validator = pytest.importorskip("jsonschema").Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas/provenance-manifest.schema.json"
APPROVED_EXAMPLE = REPO_ROOT / "examples/traceability/PROVENANCE-0001.yaml"
REJECTED_EXAMPLE = REPO_ROOT / "examples/traceability/PROVENANCE-0002-rejected.yaml"


def _errors(payload: dict) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    return [error.message for error in validator.iter_errors(payload)]


def test_provenance_manifest_schema_accepts_approved_example() -> None:
    assert validate_against_schema(APPROVED_EXAMPLE, load_yaml(APPROVED_EXAMPLE), REPO_ROOT) == []


def test_provenance_manifest_schema_accepts_rejected_example() -> None:
    assert validate_against_schema(REJECTED_EXAMPLE, load_yaml(REJECTED_EXAMPLE), REPO_ROOT) == []


def test_provenance_manifest_schema_rejects_unknown_manifest_status() -> None:
    payload = load_yaml(APPROVED_EXAMPLE)
    payload["provenance_manifest"]["status"] = "unknown"

    assert any("'unknown' is not one of" in message for message in _errors(payload))


def test_provenance_manifest_schema_rejects_unknown_node_type() -> None:
    payload = load_yaml(APPROVED_EXAMPLE)
    payload["traceability"]["nodes"][0]["type"] = "unexpected_node"

    assert any("'unexpected_node' is not one of" in message for message in _errors(payload))
