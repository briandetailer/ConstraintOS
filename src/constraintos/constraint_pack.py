from __future__ import annotations

from copy import deepcopy
from typing import Any


def apply_constraint_pack(render_specification: dict[str, Any], constraint_pack: dict[str, Any]) -> dict[str, Any]:
    """Apply reusable constraints to a render specification without mutating inputs."""

    if not isinstance(render_specification, dict):
        raise ValueError("render_specification must be an object")
    if not isinstance(constraint_pack, dict):
        raise ValueError("constraint_pack must be an object")
    if "render_specification" not in render_specification:
        raise ValueError("render_specification object is required")
    if "constraint_pack" not in constraint_pack:
        raise ValueError("constraint_pack object is required")

    applied = deepcopy(render_specification)
    applied["requirements"] = _merge_by_id(
        applied.get("requirements", []),
        constraint_pack.get("requirements", []),
        "requirements",
    )
    applied["negative_constraints"] = _merge_by_id(
        applied.get("negative_constraints", []),
        constraint_pack.get("negative_constraints", []),
        "negative_constraints",
    )
    applied_validation = applied.setdefault("validation", {})
    applied_validation["gates"] = _merge_by_id(
        applied_validation.get("gates", []),
        constraint_pack.get("validation", {}).get("gates", []),
        "validation.gates",
    )
    applied.setdefault("constraint_packs", [])
    applied["constraint_packs"] = _append_pack_reference(applied["constraint_packs"], constraint_pack["constraint_pack"])
    return applied


def _merge_by_id(existing: Any, additions: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(existing, list):
        raise ValueError(f"{label} must be a list")
    if not isinstance(additions, list):
        raise ValueError(f"constraint pack {label} must be a list")
    merged = deepcopy(existing)
    seen = {_required_id(item, label) for item in merged}
    for item in additions:
        item_id = _required_id(item, label)
        if item_id in seen:
            continue
        merged.append(deepcopy(item))
        seen.add(item_id)
    return merged


def _required_id(item: Any, label: str) -> str:
    if not isinstance(item, dict):
        raise ValueError(f"{label} entries must be objects")
    item_id = item.get("id")
    if not isinstance(item_id, str) or not item_id:
        raise ValueError(f"{label} entries must have an id")
    return item_id


def _append_pack_reference(existing: Any, pack_header: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(existing, list):
        raise ValueError("constraint_packs must be a list")
    pack_id = pack_header.get("id")
    if not isinstance(pack_id, str) or not pack_id:
        raise ValueError("constraint_pack.id is required")
    references = deepcopy(existing)
    if any(isinstance(item, dict) and item.get("id") == pack_id for item in references):
        return references
    references.append({"id": pack_id, "version": pack_header.get("version"), "title": pack_header.get("title")})
    return references
