from pathlib import Path

import yaml

from constraintos.cli import main
from constraintos.compiler import compile_to_text


def test_compile_to_text_basic() -> None:
    spec = {
        "artifact": {"id": "PLATE-0001", "title": "Test", "type": "technical_plate"},
        "subject": {"type": "engine", "family": "LF4"},
        "constraints": [
            {"id": "C-0001", "statement": "Must be V6", "severity": "blocker", "acceptance": "V6 visible"}
        ],
    }
    result = compile_to_text(spec)
    assert result.artifact_id == "PLATE-0001"
    assert "Must be V6" in result.instruction
    assert result.unsupported_constraints == []


def test_compile_reports_unsupported_constraint_type() -> None:
    spec = {
        "artifact": {"id": "PLATE-0001", "title": "Test", "type": "technical_plate"},
        "constraints": [
            {"id": "C-9999", "type": "unknown", "statement": "Unsupported", "severity": "major", "acceptance": "N/A"}
        ],
    }
    result = compile_to_text(spec)
    assert result.unsupported_constraints
    assert result.warnings


def test_cli_compile(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec.yaml"
    output = tmp_path / "instruction.txt"
    spec_path.write_text(yaml.safe_dump({
        "artifact": {"id": "PLATE-0001", "title": "Test", "type": "technical_plate"},
        "constraints": [
            {"id": "C-0001", "statement": "Must be V6", "severity": "blocker", "acceptance": "V6 visible"}
        ],
    }))
    rc = main(["compile", str(spec_path), "--output", str(output)])
    assert rc == 0
    assert "Must be V6" in output.read_text()
