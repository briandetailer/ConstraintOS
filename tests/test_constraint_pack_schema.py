from pathlib import Path

import pytest
import yaml

from constraintos.cli import validate_against_schema
from constraintos.schema_registry import detect_record_type, detect_schema


CONSTRAINT_PACK = Path("examples/constraint_packs/lf4_engine_constraint_pack.yaml")
SCHEMA = Path("schemas/constraint-pack.schema.json")


def test_detect_constraint_pack_schema() -> None:
    assert detect_schema({"constraint_pack": {}}) == "schemas/constraint-pack.schema.json"
    assert detect_record_type({"constraint_pack": {}}) == "constraint_pack"


def test_lf4_constraint_pack_validates_against_schema() -> None:
    payload = yaml.safe_load(CONSTRAINT_PACK.read_text(encoding="utf-8"))
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))

    validate_against_schema(payload, schema)


def test_constraint_pack_requires_validation_gates() -> None:
    payload = yaml.safe_load(CONSTRAINT_PACK.read_text(encoding="utf-8"))
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    payload["validation"]["gates"] = []

    with pytest.raises(Exception):
        validate_against_schema(payload, schema)
