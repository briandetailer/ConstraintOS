import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from constraintos.cli import validate_against_schema
from constraintos.schema_registry import detect_record_type, detect_schema


def test_render_specification_schema_detects_contract() -> None:
    data = {"render_specification": {}}

    assert detect_schema(data) == "schemas/render-specification.schema.json"
    assert detect_record_type(data) == "render_specification"


def test_lf4_render_specification_example_validates() -> None:
    repo_root = Path.cwd()
    source = repo_root / "examples" / "render" / "lf4_engine_render_specification.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))

    assert validate_against_schema(source, data, repo_root) == []


def test_render_specification_schema_requires_validation_gates() -> None:
    schema = json.loads(Path("schemas/render-specification.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    data = {
        "render_specification": {"id": "RSPEC-0001", "title": "Test", "status": "draft", "version": "0.1"},
        "subject": {"id": "SUBJECT-0001", "name": "Subject", "type": "engine"},
        "requirements": [{"id": "REQ-0001", "statement": "Must be specific.", "severity": "blocker", "validation_method": "human_review"}],
        "validation": {"gates": []},
    }

    errors = list(validator.iter_errors(data))

    assert any("should be non-empty" in error.message for error in errors)
