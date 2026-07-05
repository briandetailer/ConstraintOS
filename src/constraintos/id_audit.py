from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


@dataclass
class IdAuditFinding:
    finding_type: str
    identifier: str
    path: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_type": self.finding_type,
            "identifier": self.identifier,
            "path": self.path,
            "message": self.message,
        }


def load_yaml_file(path: Path) -> dict[str, Any] | None:
    if yaml is None:
        raise RuntimeError("PyYAML is required. Install with: pip install pyyaml")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def extract_ids(data: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for value in data.values():
        if isinstance(value, dict) and isinstance(value.get("id"), str):
            ids.append(value["id"])
    if isinstance(data.get("artifact"), dict) and isinstance(data["artifact"].get("id"), str):
        artifact_id = data["artifact"]["id"]
        if artifact_id not in ids:
            ids.append(artifact_id)
    return ids


def collect_yaml_paths(repo_root: str | Path = ".") -> list[Path]:
    root = Path(repo_root)
    paths: list[Path] = []
    for folder in ["docs", "examples", "reports", "patches", "baselines"]:
        target = root / folder
        if target.exists():
            paths.extend(target.rglob("*.yaml"))
            paths.extend(target.rglob("*.yml"))
    return sorted(set(paths))


def audit_ids(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    seen: dict[str, str] = {}
    findings: list[IdAuditFinding] = []
    checked = 0
    for path in collect_yaml_paths(root):
        data = load_yaml_file(path)
        if data is None:
            continue
        for identifier in extract_ids(data):
            checked += 1
            rel = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
            if identifier in seen:
                findings.append(IdAuditFinding("duplicate_id", identifier, rel, f"Duplicate of {seen[identifier]}"))
            else:
                seen[identifier] = rel
    return {
        "id_audit_report": {
            "id": "ID-AUDIT-0001",
            "status": "pass" if not findings else "fail",
            "created": date.today().isoformat(),
            "checked": checked,
            "findings": len(findings),
        },
        "findings": [finding.to_dict() for finding in findings],
    }
