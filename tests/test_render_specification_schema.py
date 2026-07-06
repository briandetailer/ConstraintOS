import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from constraintos.cli import validate_against_schema
from constraintos.constraint_pack import apply_constraint_pack
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


def test_applied_constraint_pack_reference_validates_in_render_specification() -> None:
    repo_root = Path.cwd()
    render_source = repo_root / "examples" / "render" / "lf4_engine_render_specification.yaml"
    pack_source = repo_root / "examples" / "constraint_packs" / "lf4_engine_constraint_pack.yaml"
    render_specification = yaml.safe_load(render_source.read_text(encoding="utf-8"))
    constraint_pack = yaml.safe_load(pack_source.read_text(encoding="utf-8"))

    applied = apply_constraint_pack(render_specification, constraint_pack)

    assert validate_against_schema(render_source, applied, repo_root) == []


def test_render_specification_constraint_pack_reference_requires_cpack_id() -> None:
    schema = json.loads(Path("schemas/render-specification.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    data = {
        "render_specification": {"id": "RSPEC-0001", "title": "Test", "status": "draft", "version": "0.1"},
        "constraint_packs": [{"id": "PACK-0001"}],
        "subject": {"id": "SUBJECT-0001", "name": "Subject", "type": "engine"},
        "requirements": [{"id": "REQ-0001", "statement": "Must be specific.", "severity": "blocker", "validation_method": "human_review"}],
        "validation": {"gates": [{"id": "GATE-0001", "name": "Gate", "required_pass": True}]},
    }

    errors = list(validator.iter_errors(data))

    assert any("does not match" in error.message for error in errors)
