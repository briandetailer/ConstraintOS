from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


ID_PATTERN = re.compile(r"^[A-Z]+-[0-9]{4}$")


@dataclass
class ValidationResult:
    path: Path
    status: str
    messages: list[str]


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required. Install with: pip install pyyaml")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is required. Install with: pip install pyyaml")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False)


def new_artifact(args: argparse.Namespace) -> int:
    artifact_id = args.id.upper()
    artifact_type = args.type
    if not ID_PATTERN.match(artifact_id):
        print(f"Invalid artifact id: {artifact_id}. Expected format like CPE-0007.", file=sys.stderr)
        return 2

    target = Path(args.output or f"docs/{artifact_type}/{artifact_id}.yaml")
    data = {
        "artifact": {
            "id": artifact_id,
            "title": args.title,
            "type": artifact_type,
            "status": "draft",
            "version": "0.1",
            "created": date.today().isoformat(),
        },
        "traceability": {
            "depends_on": [],
            "related_failures": [],
            "related_requirements": [],
            "related_adrs": [],
        },
        "content": {
            "summary": "",
            "notes": [],
        },
    }
    write_yaml(target, data)
    print(f"Created artifact: {target}")
    return 0


def new_failure(args: argparse.Namespace) -> int:
    failure_id = args.id.upper()
    if not failure_id.startswith("FR-") or not ID_PATTERN.match(failure_id):
        print(f"Invalid failure id: {failure_id}. Expected format like FR-0001.", file=sys.stderr)
        return 2

    target = Path(args.output or f"docs/100_Discovery/Failure_Registry/{failure_id}.yaml")
    data = {
        "failure": {
            "id": failure_id,
            "title": args.title,
            "family": args.family,
            "severity": args.severity,
            "status": "draft",
            "created": date.today().isoformat(),
        },
        "description": "",
        "observed_behavior": "",
        "impact": "",
        "root_cause_hypotheses": [],
        "mitigations": [],
        "future_tests": [],
        "traceability": {
            "requirements": [],
            "validators": [],
            "adrs": [],
        },
    }
    write_yaml(target, data)
    print(f"Created failure record: {target}")
    return 0


def validate_artifact(path: Path) -> ValidationResult:
    messages: list[str] = []
    try:
        data = load_yaml(path)
    except Exception as exc:
        return ValidationResult(path, "fail", [str(exc)])

    artifact = data.get("artifact") or data.get("failure")
    if not isinstance(artifact, dict):
        messages.append("Missing artifact or failure object.")
    else:
        artifact_id = artifact.get("id")
        if not artifact_id or not ID_PATTERN.match(str(artifact_id)):
            messages.append("Missing or invalid id.")
        for field in ["title", "status", "version"]:
            if field not in artifact and data.get("artifact") is not None:
                messages.append(f"Missing artifact.{field}.")

    if "traceability" not in data:
        messages.append("Missing traceability section.")

    status = "pass" if not messages else "fail"
    return ValidationResult(path, status, messages)


def validate(args: argparse.Namespace) -> int:
    root = Path(args.path)
    files = [root] if root.is_file() else sorted(root.rglob("*.yaml"))
    if not files:
        print("No YAML files found.")
        return 0

    results = [validate_artifact(path) for path in files]
    for result in results:
        print(f"{result.status.upper()}: {result.path}")
        for message in result.messages:
            print(f"  - {message}")

    failures = [r for r in results if r.status == "fail"]
    return 1 if failures else 0


def trace(args: argparse.Namespace) -> int:
    root = Path(args.path)
    rows: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.yaml")):
        try:
            data = load_yaml(path)
        except Exception:
            continue
        artifact = data.get("artifact") or data.get("failure") or {}
        traceability = data.get("traceability", {})
        rows.append({
            "path": str(path),
            "id": artifact.get("id"),
            "title": artifact.get("title"),
            "depends_on": traceability.get("depends_on", []),
            "failures": traceability.get("related_failures", traceability.get("requirements", [])),
            "adrs": traceability.get("related_adrs", traceability.get("adrs", [])),
        })
    print(json.dumps(rows, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="constraintos")
    sub = parser.add_subparsers(dest="command", required=True)

    artifact = sub.add_parser("new-artifact", help="Create a new artifact YAML scaffold")
    artifact.add_argument("id")
    artifact.add_argument("title")
    artifact.add_argument("--type", default="artifact")
    artifact.add_argument("--output")
    artifact.set_defaults(func=new_artifact)

    failure = sub.add_parser("new-failure", help="Create a new failure record YAML scaffold")
    failure.add_argument("id")
    failure.add_argument("title")
    failure.add_argument("--family", default="F100")
    failure.add_argument("--severity", default="major", choices=["blocker", "major", "minor", "advisory"])
    failure.add_argument("--output")
    failure.set_defaults(func=new_failure)

    val = sub.add_parser("validate", help="Validate metadata and traceability scaffolds")
    val.add_argument("path", nargs="?", default="docs")
    val.set_defaults(func=validate)

    tr = sub.add_parser("trace", help="Generate a traceability JSON report")
    tr.add_argument("path", nargs="?", default="docs")
    tr.set_defaults(func=trace)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
