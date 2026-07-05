from __future__ import annotations

from typing import Any


def _render_specification(specification: dict[str, Any]) -> dict[str, Any]:
    render_specification = specification.get("render_specification")
    if not isinstance(render_specification, dict):
        raise ValueError("render specification contract must include render_specification")
    return render_specification


def _required_list(specification: dict[str, Any], key: str) -> list[Any]:
    value = specification.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"render specification contract must include non-empty {key}")
    return value


def _required_mapping(specification: dict[str, Any], key: str) -> dict[str, Any]:
    value = specification.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"render specification contract must include {key}")
    return value


def compile_render_contract_to_runtime(specification: dict[str, Any]) -> dict[str, Any]:
    render_specification = _render_specification(specification)
    subject = _required_mapping(specification, "subject")
    requirements = _required_list(specification, "requirements")
    negative_constraints = specification.get("negative_constraints", [])
    validation = _required_mapping(specification, "validation")
    gates = validation.get("gates")
    if not isinstance(gates, list) or not gates:
        raise ValueError("render specification contract must include validation gates")

    render_specification_id = str(render_specification.get("id", "RSPEC-UNKNOWN"))
    return {
        "artifact": {
            "id": render_specification_id,
            "title": str(render_specification.get("title", render_specification_id)),
            "type": "render_contract_runtime",
            "status": "planned",
        },
        "execution_steps": [
            {
                "id": "NODE-0001",
                "plugin": "render_contract",
                "action": "load_subject",
                "inputs": {"subject": subject},
            },
            {
                "id": "NODE-0002",
                "plugin": "render_contract",
                "action": "check_requirements",
                "depends_on": ["NODE-0001"],
                "inputs": {"requirements": requirements},
            },
            {
                "id": "NODE-0003",
                "plugin": "render_contract",
                "action": "check_negative_constraints",
                "depends_on": ["NODE-0002"],
                "inputs": {"negative_constraints": negative_constraints},
            },
            {
                "id": "NODE-0004",
                "plugin": "render_contract",
                "action": "check_validation_gates",
                "depends_on": ["NODE-0003"],
                "inputs": {"gates": gates},
            },
        ],
    }
