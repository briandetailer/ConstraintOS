from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    Draft202012Validator = None

from constraintos.schema_registry import detect_record_type, detect_schema


def load_json_schema(schema_path: Path) -> dict[str, Any]:
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{schema_path} must contain a schema object")
    return data


def validate_against_registered_schema(
    path: Path,
    data: dict[str, Any],
    repo_root: Path | None = None,
) -> list[str]:
    schema_path = detect_schema(data)
    if schema_path is None:
        return [f"schema:unknown:<root>: no registered schema detected"]
    if Draft202012Validator is None:
        return ["jsonschema is required. Install with: pip install jsonschema"]
    root = repo_root or Path.cwd()
    full_schema_path = root / schema_path
    if not full_schema_path.exists():
        return [f"schema:{schema_path}:<root>: schema not found"]
    validator = Draft202012Validator(load_json_schema(full_schema_path))
    return [
        f"schema:{schema_path}:{'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    ]


def require_registered_schema(
    path: Path,
    data: dict[str, Any],
    expected_record_type: str | None = None,
    repo_root: Path | None = None,
) -> None:
    if expected_record_type is not None:
        record_type = detect_record_type(data)
        if record_type != expected_record_type:
            raise ValueError(f"{path}: expected {expected_record_type}, got {record_type or 'unknown'}")
    errors = validate_against_registered_schema(path, data, repo_root=repo_root)
    if errors:
        raise ValueError(f"{path}: " + "; ".join(errors))
