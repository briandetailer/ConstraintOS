import json
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate

from runtime import runtime_contract_registry


SCHEMA_ROOT = Path("schemas/runtime/v1")


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def test_runtime_contract_registry_matches_json_schema() -> None:
    schema = _schema("runtime-contract-registry.schema.json")

    validate(instance=runtime_contract_registry(), schema=schema)


def test_runtime_contract_registry_schema_rejects_missing_required_contract_fields() -> None:
    schema = _schema("runtime-contract-registry.schema.json")
    registry = runtime_contract_registry()
    registry["contracts"][0].pop("produced_by")

    with pytest.raises(ValidationError):
        validate(instance=registry, schema=schema)


def test_runtime_contract_registry_schema_rejects_unknown_contract_type() -> None:
    schema = _schema("runtime-contract-registry.schema.json")
    registry = runtime_contract_registry()
    registry["contracts"][0]["contract_type"] = "unknown"

    with pytest.raises(ValidationError):
        validate(instance=registry, schema=schema)
