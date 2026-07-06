from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


CSL_CONTRACT_VERSION = "csl/v1"
TOP_LEVEL_REQUIRED_FIELDS = (
    "csl_version",
    "id",
    "name",
    "entities",
    "constraints",
    "groups",
    "root_group_id",
)
ENTITY_REQUIRED_FIELDS = ("id", "type", "selector")
CONSTRAINT_REQUIRED_FIELDS = ("id", "type", "operator", "expected", "severity")
GROUP_REQUIRED_FIELDS = ("id", "operator", "children")
VALID_GROUP_OPERATORS = {"AND", "OR", "NOT"}
VALID_CHILD_TYPES = {"constraint", "group"}
VALID_CONSTRAINT_TYPES = {"dimensional", "geometric_relation"}


@dataclass(frozen=True)
class CSLContractVerification:
    issues: list[str] = field(default_factory=list)

    def successful(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "csl_contract_verification": {
                "successful": self.successful(),
                "issue_count": len(self.issues),
            },
            "issues": self.issues,
        }


def verify_csl_document_contract(document: dict[str, Any]) -> CSLContractVerification:
    issues: list[str] = []
    if not isinstance(document, dict):
        return CSLContractVerification(["CSL document must be a dictionary."])

    for field_name in TOP_LEVEL_REQUIRED_FIELDS:
        if field_name not in document:
            issues.append(f"CSL document requires {field_name}.")

    if document.get("csl_version") != CSL_CONTRACT_VERSION:
        issues.append(f"CSL document csl_version must be {CSL_CONTRACT_VERSION}.")

    entities = document.get("entities", [])
    constraints = document.get("constraints", [])
    groups = document.get("groups", [])

    if not isinstance(entities, list):
        issues.append("CSL document entities must be a list.")
        entities = []
    if not isinstance(constraints, list):
        issues.append("CSL document constraints must be a list.")
        constraints = []
    if not isinstance(groups, list):
        issues.append("CSL document groups must be a list.")
        groups = []

    entity_ids = _ids_for_records(entities, "entity", issues)
    constraint_ids = _ids_for_records(constraints, "constraint", issues)
    group_ids = _ids_for_records(groups, "group", issues)

    _verify_entities(entities, issues)
    _verify_constraints(constraints, entity_ids, issues)
    _verify_groups(groups, constraint_ids, group_ids, issues)

    root_group_id = document.get("root_group_id")
    if root_group_id and root_group_id not in group_ids:
        issues.append("CSL document root_group_id must reference an existing group.")

    return CSLContractVerification(issues)


def _ids_for_records(records: list[Any], label: str, issues: list[str]) -> set[str]:
    ids: list[str] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            issues.append(f"CSL {label} {index} must be a dictionary.")
            continue
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            issues.append(f"CSL {label} {index} requires id.")
            continue
        ids.append(record_id)
    if len(ids) != len(set(ids)):
        issues.append(f"CSL {label} ids must be unique.")
    return set(ids)


def _verify_entities(entities: list[Any], issues: list[str]) -> None:
    for index, entity in enumerate(entities, start=1):
        if not isinstance(entity, dict):
            continue
        for field_name in ENTITY_REQUIRED_FIELDS:
            if field_name not in entity:
                issues.append(f"CSL entity {index} requires {field_name}.")
        selector = entity.get("selector", {})
        if not isinstance(selector, dict):
            issues.append(f"CSL entity {index} selector must be a dictionary.")
        elif not selector.get("kind") or not selector.get("value"):
            issues.append(f"CSL entity {index} selector requires kind and value.")


def _verify_constraints(constraints: list[Any], entity_ids: set[str], issues: list[str]) -> None:
    for index, constraint in enumerate(constraints, start=1):
        if not isinstance(constraint, dict):
            continue
        for field_name in CONSTRAINT_REQUIRED_FIELDS:
            if field_name not in constraint:
                issues.append(f"CSL constraint {index} requires {field_name}.")
        constraint_type = constraint.get("type")
        if constraint_type not in VALID_CONSTRAINT_TYPES:
            issues.append(f"CSL constraint {index} type must be dimensional or geometric_relation.")
        if constraint_type == "dimensional":
            _verify_dimensional_constraint(index, constraint, entity_ids, issues)
        if constraint_type == "geometric_relation":
            _verify_geometric_relation_constraint(index, constraint, entity_ids, issues)


def _verify_dimensional_constraint(
    index: int,
    constraint: dict[str, Any],
    entity_ids: set[str],
    issues: list[str],
) -> None:
    entity_id = constraint.get("entity_id")
    if not entity_id:
        issues.append(f"CSL dimensional constraint {index} requires entity_id.")
    elif entity_id not in entity_ids:
        issues.append(f"CSL dimensional constraint {index} entity_id must reference an existing entity.")
    if not constraint.get("measurement"):
        issues.append(f"CSL dimensional constraint {index} requires measurement.")


def _verify_geometric_relation_constraint(
    index: int,
    constraint: dict[str, Any],
    entity_ids: set[str],
    issues: list[str],
) -> None:
    referenced_entities = constraint.get("entity_ids", [])
    if not isinstance(referenced_entities, list) or len(referenced_entities) < 2:
        issues.append(f"CSL geometric relation constraint {index} requires at least two entity_ids.")
    else:
        missing_entities = [entity_id for entity_id in referenced_entities if entity_id not in entity_ids]
        if missing_entities:
            issues.append(f"CSL geometric relation constraint {index} entity_ids must reference existing entities.")
    if not constraint.get("relation"):
        issues.append(f"CSL geometric relation constraint {index} requires relation.")


def _verify_groups(
    groups: list[Any],
    constraint_ids: set[str],
    group_ids: set[str],
    issues: list[str],
) -> None:
    for index, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            continue
        for field_name in GROUP_REQUIRED_FIELDS:
            if field_name not in group:
                issues.append(f"CSL group {index} requires {field_name}.")
        operator = group.get("operator")
        if operator not in VALID_GROUP_OPERATORS:
            issues.append(f"CSL group {index} operator must be AND, OR, or NOT.")
        children = group.get("children", [])
        if not isinstance(children, list):
            issues.append(f"CSL group {index} children must be a list.")
            continue
        if operator in {"AND", "OR"} and not children:
            issues.append(f"CSL group {index} operator {operator} requires at least one child.")
        if operator == "NOT" and len(children) != 1:
            issues.append(f"CSL group {index} operator NOT requires exactly one child.")
        for child_index, child in enumerate(children, start=1):
            _verify_group_child(index, child_index, child, constraint_ids, group_ids, issues)


def _verify_group_child(
    group_index: int,
    child_index: int,
    child: Any,
    constraint_ids: set[str],
    group_ids: set[str],
    issues: list[str],
) -> None:
    if not isinstance(child, dict):
        issues.append(f"CSL group {group_index} child {child_index} must be a dictionary.")
        return
    child_type = child.get("type")
    child_id = child.get("id")
    if child_type not in VALID_CHILD_TYPES:
        issues.append(f"CSL group {group_index} child {child_index} type must be constraint or group.")
        return
    if child_type == "constraint" and child_id not in constraint_ids:
        issues.append(f"CSL group {group_index} child {child_index} constraint id must reference an existing constraint.")
    if child_type == "group" and child_id not in group_ids:
        issues.append(f"CSL group {group_index} child {child_index} group id must reference an existing group.")
