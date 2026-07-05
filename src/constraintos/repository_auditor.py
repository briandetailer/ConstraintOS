from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from constraintos.repository_introspection import RepositoryInventory, create_repository_health_summary, create_repository_inventory
from constraintos.schema_registry import SCHEMA_REGISTRY, SPECIAL_SCHEMA_RULES, detect_schema


@dataclass
class RepositoryAudit:
    repo_root: str
    inventory: dict[str, Any]
    schema_coverage: dict[str, Any]
    artifact_coverage: dict[str, Any]
    technical_debt: dict[str, Any]
    beta_readiness: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "repository_audit": {
                "id": "REPO-AUDIT-0001",
                "created": date.today().isoformat(),
                "repo_root": self.repo_root,
                "status": self.beta_readiness.get("beta_readiness_report", {}).get("status", "review"),
            },
            "inventory": self.inventory,
            "schema_coverage": self.schema_coverage,
            "artifact_coverage": self.artifact_coverage,
            "technical_debt": self.technical_debt,
            "beta_readiness": self.beta_readiness,
        }


def _relative_files(root: Path, pattern: str) -> list[str]:
    return sorted(str(path.relative_to(root)) for path in root.rglob(pattern) if path.is_file())


def _load_yaml(path: Path) -> dict[str, Any] | None:
    if yaml is None:
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def create_schema_coverage_report(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    schema_files = set(_relative_files(root, "schemas/*.json"))
    registered_schema_paths = {registration.schema_path for registration in SCHEMA_REGISTRY}
    special_schema_paths = {schema_path for _keys, schema_path, _record_type in SPECIAL_SCHEMA_RULES}
    referenced_schema_paths = registered_schema_paths | special_schema_paths
    missing_registered = sorted(schema for schema in referenced_schema_paths if schema not in schema_files)
    orphaned_schemas = sorted(schema for schema in schema_files if schema not in referenced_schema_paths)
    invalid_json = sorted(schema for schema in schema_files if _load_json(root / schema) is None)
    return {
        "schema_coverage_report": {
            "id": "SCHEMA-COVERAGE-0001",
            "created": date.today().isoformat(),
            "status": "pass" if not missing_registered and not invalid_json else "fail",
            "schema_count": len(schema_files),
            "registered_count": len(registered_schema_paths),
            "special_rule_count": len(special_schema_paths),
            "orphaned_count": len(orphaned_schemas),
            "missing_registered_count": len(missing_registered),
            "invalid_json_count": len(invalid_json),
        },
        "missing_registered_schemas": missing_registered,
        "orphaned_schemas": orphaned_schemas,
        "invalid_json_schemas": invalid_json,
    }


def create_artifact_coverage_report(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    example_files = _relative_files(root, "examples/**/*.yaml") + _relative_files(root, "examples/**/*.yml")
    detected: dict[str, int] = {}
    undetected: list[str] = []
    duplicate_ids: list[str] = []
    seen_ids: dict[str, str] = {}
    invalid_yaml: list[str] = []
    for relative in example_files:
        data = _load_yaml(root / relative)
        if data is None:
            invalid_yaml.append(relative)
            continue
        schema = detect_schema(data)
        if schema is None:
            undetected.append(relative)
        else:
            detected[schema] = detected.get(schema, 0) + 1
        object_id = _extract_candidate_id(data, fallback=Path(relative).stem)
        if object_id:
            if object_id in seen_ids:
                duplicate_ids.append(f"duplicate id {object_id}: {seen_ids[object_id]} and {relative}")
            else:
                seen_ids[object_id] = relative
    return {
        "artifact_coverage_report": {
            "id": "ARTIFACT-COVERAGE-0001",
            "created": date.today().isoformat(),
            "status": "pass" if not undetected and not duplicate_ids and not invalid_yaml else "fail",
            "example_count": len(example_files),
            "detected_count": len(example_files) - len(undetected) - len(invalid_yaml),
            "undetected_count": len(undetected),
            "duplicate_id_count": len(duplicate_ids),
            "invalid_yaml_count": len(invalid_yaml),
        },
        "detected_by_schema": detected,
        "undetected_examples": undetected,
        "duplicate_ids": duplicate_ids,
        "invalid_yaml_examples": invalid_yaml,
    }


def _extract_candidate_id(data: dict[str, Any], fallback: str | None = None) -> str | None:
    for value in data.values():
        if isinstance(value, dict):
            for field in ("id", "name"):
                if value.get(field):
                    return str(value[field])
    if "artifact" in data and isinstance(data["artifact"], dict):
        return data["artifact"].get("id")
    return fallback


def create_technical_debt_report(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    source_files = _relative_files(root, "src/**/*.py")
    docs = _relative_files(root, "docs/**/*.md")
    todo_hits: list[str] = []
    placeholder_hits: list[str] = []
    for relative in source_files + docs:
        text = (root / relative).read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        if "todo" in lower:
            todo_hits.append(relative)
        if "placeholder" in lower or "stub" in lower:
            placeholder_hits.append(relative)
    return {
        "technical_debt_report": {
            "id": "TECH-DEBT-0001",
            "created": date.today().isoformat(),
            "status": "review" if todo_hits or placeholder_hits else "pass",
            "todo_file_count": len(todo_hits),
            "placeholder_file_count": len(placeholder_hits),
        },
        "todo_files": todo_hits,
        "placeholder_or_stub_files": placeholder_hits,
    }


def create_beta_readiness_report(schema_report: dict[str, Any], artifact_report: dict[str, Any], debt_report: dict[str, Any], health_summary: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    if schema_report["schema_coverage_report"]["status"] != "pass":
        blockers.append("schema coverage is not passing")
    if artifact_report["artifact_coverage_report"]["status"] != "pass":
        blockers.append("artifact coverage is not passing")
    if health_summary["repository_health_summary"]["status"] not in {"pass", "review"}:
        blockers.append("repository health summary is not acceptable")
    warnings: list[str] = []
    if debt_report["technical_debt_report"]["status"] != "pass":
        warnings.append("technical debt report requires review")
    status = "ready" if not blockers else "blocked"
    return {
        "beta_readiness_report": {
            "id": "BETA-READY-0001",
            "created": date.today().isoformat(),
            "status": status,
        },
        "blockers": blockers,
        "warnings": warnings,
        "recommendation": "prepare_beta_candidate" if status == "ready" else "resolve_blockers",
    }


def run_repository_audit(repo_root: str | Path = ".") -> RepositoryAudit:
    root = Path(repo_root)
    inventory = create_repository_inventory(root)
    health = create_repository_health_summary(inventory)
    schema_report = create_schema_coverage_report(root)
    artifact_report = create_artifact_coverage_report(root)
    debt_report = create_technical_debt_report(root)
    beta_report = create_beta_readiness_report(schema_report, artifact_report, debt_report, health)
    return RepositoryAudit(
        repo_root=str(root),
        inventory=inventory.to_dict(),
        schema_coverage=schema_report,
        artifact_coverage=artifact_report,
        technical_debt=debt_report,
        beta_readiness=beta_report,
    )


def audit_to_markdown(audit: RepositoryAudit | dict[str, Any]) -> str:
    data = audit.to_dict() if isinstance(audit, RepositoryAudit) else audit
    repo = data["repository_audit"]
    inventory = data["inventory"]["repository_inventory"]
    schema = data["schema_coverage"]["schema_coverage_report"]
    artifacts = data["artifact_coverage"]["artifact_coverage_report"]
    debt = data["technical_debt"]["technical_debt_report"]
    beta = data["beta_readiness"]["beta_readiness_report"]
    lines = [
        "# ConstraintOS Repository Audit",
        "",
        f"- **Audit ID:** {repo['id']}",
        f"- **Status:** {repo['status']}",
        f"- **Created:** {repo['created']}",
        "",
        "## Inventory",
        "",
        f"- Schemas: {inventory['schema_count']}",
        f"- Examples: {inventory['example_count']}",
        f"- Tests: {inventory['test_count']}",
        f"- Documentation files: {inventory['doc_count']}",
        f"- Source files: {inventory['source_count']}",
        "",
        "## Schema Coverage",
        "",
        f"- Status: {schema['status']}",
        f"- Registered schemas missing: {schema['missing_registered_count']}",
        f"- Orphaned schemas: {schema['orphaned_count']}",
        f"- Invalid JSON schemas: {schema['invalid_json_count']}",
        "",
        "## Artifact Coverage",
        "",
        f"- Status: {artifacts['status']}",
        f"- Examples: {artifacts['example_count']}",
        f"- Undetected examples: {artifacts['undetected_count']}",
        f"- Duplicate IDs: {artifacts['duplicate_id_count']}",
        f"- Invalid YAML examples: {artifacts['invalid_yaml_count']}",
        "",
        "## Technical Debt",
        "",
        f"- Status: {debt['status']}",
        f"- TODO files: {debt['todo_file_count']}",
        f"- Placeholder/stub files: {debt['placeholder_file_count']}",
        "",
        "## Beta Readiness",
        "",
        f"- Status: {beta['status']}",
        f"- Recommendation: {data['beta_readiness']['recommendation']}",
    ]
    blockers = data["beta_readiness"].get("blockers", [])
    if blockers:
        lines.extend(["", "### Blockers", ""])
        lines.extend(f"- {item}" for item in blockers)
    return "\n".join(lines) + "\n"
