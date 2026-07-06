from pathlib import Path

import pytest
import yaml

from constraintos.schema_validation import require_registered_schema, validate_against_registered_schema


RENDER_SPECIFICATION = Path("examples/render/lf4_engine_render_specification.yaml")
CONSTRAINT_PACK = Path("examples/constraint_packs/lf4_engine_constraint_pack.yaml")


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_require_registered_schema_accepts_expected_render_specification() -> None:
    payload = load_yaml(RENDER_SPECIFICATION)

    require_registered_schema(RENDER_SPECIFICATION, payload, expected_record_type="render_specification")


def test_validate_against_registered_schema_reports_schema_errors() -> None:
    payload = load_yaml(CONSTRAINT_PACK)
    payload["validation"]["gates"] = []

    errors = validate_against_registered_schema(CONSTRAINT_PACK, payload)

    assert errors
    assert "schema:schemas/constraint-pack.schema.json:validation.gates" in errors[0]


def test_require_registered_schema_rejects_wrong_record_type() -> None:
    payload = load_yaml(CONSTRAINT_PACK)

    with pytest.raises(ValueError, match="expected render_specification, got constraint_pack"):
        require_registered_schema(CONSTRAINT_PACK, payload, expected_record_type="render_specification")
