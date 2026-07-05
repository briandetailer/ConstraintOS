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

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    Draft202012Validator = None

from constraintos.compiler import compile_to_text
from constraintos.id_audit import audit_ids
from constraintos.patching import create_patch_package, create_regression_baseline
from constraintos.repository_auditor import audit_to_markdown, run_repository_audit
from constraintos.repository_introspection import create_repository_health_summary, create_repository_inventory
from constraintos.schema_registry import SCHEMA_REGISTRY, SPECIAL_SCHEMA_RULES, detect_record_type, detect_schema as registry_detect_schema, registry_report

ID_PATTERN = re.compile(r"^[A-Z]+-[0-9]{4}$")
FR_PATTERN = re.compile(r"^FR-[0-9]{4}$")
SCHEMA_EXEMPT_KEYS = {registration.key for registration in SCHEMA_REGISTRY} | {"status", "name", "renderer", "gate", "iteration", "artifact"}


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def detect_schema(data: dict[str, Any]) -> str | None:
    return registry_detect_schema(data)


def validate_against_schema(path: Path, data: dict[str, Any], repo_root: Path) -> list[str]:
    schema_path = detect_schema(data)
    if schema_path is None:
        return []
    if Draft202012Validator is None:
        return ["jsonschema is required. Install with: pip install jsonschema"]
    full_schema_path = repo_root / schema_path
    if not full_schema_path.exists():
        return [f"Schema not found: {schema_path}"]
    schema = load_json(full_schema_path)
    validator = Draft202012Validator(schema)
    return [
        f"schema:{schema_path}:{'.'.join(str(p) for p in error.path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    ]


def _record_from_registered_key(path: Path, data: dict[str, Any]) -> dict[str, Any] | None:
    for registration in SCHEMA_REGISTRY:
        if registration.key not in data:
            continue
        obj = data[registration.key]
        if isinstance(obj, dict):
            object_id = obj.get("id") or obj.get("name") or obj.get("worker_id") or path.stem
            title = obj.get("title") or obj.get("name") or object_id
            status = obj.get("status", "unknown")
        else:
            object_id = path.stem
            title = path.stem
            status = "active"
        if registration.key == "baseline" and isinstance(obj, dict):
            object_id = object_id or f"BASELINE-{obj.get('artifact_id', path.stem)}-{obj.get('artifact_version', 'unknown')}"
        return {"id": object_id, "title": title, "type": registration.record_type, "status": status, "traceability": data.get("traceability", {})}
    return None


def _record_from_special_rule(path: Path, data: dict[str, Any]) -> dict[str, Any] | None:
    record_type = detect_record_type(data)
    if record_type is None:
        return None
    if record_type == "csl_artifact" and "artifact" in data:
        obj = data["artifact"]
        return {"id": obj.get("id"), "title": obj.get("title", obj.get("id")), "type": obj.get("type", "csl_artifact"), "status": obj.get("status", "unknown"), "traceability": data.get("traceability", {})}
    if record_type == "artifact_manifest" and "manifest" in data:
        obj = data["manifest"]
        artifact = data.get("artifact", {})
        return {"id": obj.get("id", path.stem), "title": artifact.get("title", obj.get("id", path.stem)), "type": record_type, "status": data.get("state", "unknown"), "traceability": {}}
    if record_type == "compliance_report" and "report" in data:
        obj = data["report"]
        return {"id": obj.get("id", path.stem), "title": obj.get("id", path.stem), "type": record_type, "status": obj.get("status", "unknown"), "traceability": {}}
    return {"id": path.stem, "title": path.stem, "type": record_type, "status": data.get("status", data.get("gate", "unknown")), "traceability": data.get("traceability", {})}


def record_from_data(path: Path, data: dict[str, Any]) -> dict[str, Any] | None:
    if "artifact" in data and "constraints" in data:
        obj = data["artifact"]
        return {"id": obj.get("id"), "title": obj.get("title", obj.get("id")), "type": obj.get("type", "csl_artifact"), "status": obj.get("status", "unknown"), "traceability": data.get("traceability", {})}
    if "artifact" in data and "traceability" in data:
        obj = data["artifact"]
        return {"id": obj.get("id"), "title": obj.get("title", obj.get("id")), "type": obj.get("type", "artifact"), "status": obj.get("status", "unknown"), "traceability": data.get("traceability", {})}
    return _record_from_registered_key(path, data) or _record_from_special_rule(path, data)


def new_artifact(args: argparse.Namespace) -> int:
    artifact_id = args.id.upper()
    if not ID_PATTERN.match(artifact_id):
        print(f"Invalid artifact id: {artifact_id}. Expected format like CPE-0007.", file=sys.stderr)
        return 2
    target = Path(args.output or f"docs/{args.type}/{artifact_id}.yaml")
    data = {"artifact": {"id": artifact_id, "title": args.title, "type": args.type, "status": "draft", "version": "0.1", "created": date.today().isoformat()}, "traceability": {"depends_on": [], "related_failures": [], "related_requirements": [], "related_adrs": []}, "content": {"summary": "", "notes": []}}
    write_yaml(target, data)
    print(f"Created artifact: {target}")
    return 0


def new_failure(args: argparse.Namespace) -> int:
    failure_id = args.id.upper()
    if not FR_PATTERN.match(failure_id):
        print(f"Invalid failure id: {failure_id}. Expected format like FR-0001.", file=sys.stderr)
        return 2
    target = Path(args.output or f"docs/100_Discovery/Failure_Registry/{failure_id}.yaml")
    data = {"failure": {"id": failure_id, "title": args.title, "family": args.family, "severity": args.severity, "status": "draft", "created": date.today().isoformat()}, "description": "", "observed_behavior": "", "impact": "", "root_cause_hypotheses": [], "mitigations": [], "future_tests": [], "traceability": {"requirements": [], "validators": [], "adrs": []}}
    write_yaml(target, data)
    print(f"Created failure record: {target}")
    return 0


def new_compliance(args: argparse.Namespace) -> int:
    report_id = args.id.upper()
    if not ID_PATTERN.match(report_id) or not report_id.startswith("VAL-"):
        print(f"Invalid compliance report id: {report_id}. Expected format like VAL-0001.", file=sys.stderr)
        return 2
    target = Path(args.output or f"reports/compliance/{report_id}.yaml")
    data = {"report": {"id": report_id, "version": "0.1", "created": date.today().isoformat(), "validator_version": "constraintos-1.0.0-alpha.26"}, "artifact": {"id": args.artifact_id, "version": args.artifact_version, "specification_id": args.specification_id}, "summary": {"blocker_failures": 0, "major_failures": 0, "minor_failures": 0, "uncertain_results": 0}, "constraint_results": [], "recommendation": "escalate"}
    write_yaml(target, data)
    print(f"Created compliance report: {target}")
    return 0


def new_patch(args: argparse.Namespace) -> int:
    patch_id = args.id.upper()
    if not patch_id.startswith("PATCH-") or not ID_PATTERN.match(patch_id):
        print(f"Invalid patch id: {patch_id}. Expected format like PATCH-0001.", file=sys.stderr)
        return 2
    target = Path(args.output or f"patches/{patch_id}.yaml")
    write_yaml(target, create_patch_package(load_yaml(Path(args.report)), patch_id).to_dict())
    print(f"Created patch package: {target}")
    return 0


def new_baseline(args: argparse.Namespace) -> int:
    constraints = [item for item in args.constraints.split(",") if item]
    target = Path(args.output or f"baselines/{args.artifact_id}_{args.artifact_version}.yaml")
    write_yaml(target, create_regression_baseline(args.artifact_id, args.artifact_version, args.approved_report_id, constraints))
    print(f"Created regression baseline: {target}")
    return 0


def validate_artifact(path: Path, repo_root: Path) -> ValidationResult:
    messages: list[str] = []
    try:
        data = load_yaml(path)
    except Exception as exc:
        return ValidationResult(path, "fail", [str(exc)])
    record = record_from_data(path, data)
    if not record:
        messages.append("Unrecognized YAML artifact type.")
    elif not record.get("id"):
        messages.append("Missing record id.")
    if data.get("artifact") is not None and data.get("constraints") is None:
        for field in ["title", "status", "version"]:
            if field not in data["artifact"]:
                messages.append(f"Missing artifact.{field}.")
    if "traceability" not in data and not any(key in data for key in SCHEMA_EXEMPT_KEYS):
        messages.append("Missing traceability section.")
    messages.extend(validate_against_schema(path, data, repo_root))
    return ValidationResult(path, "pass" if not messages else "fail", messages)


def collect_yaml_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        root = Path(raw)
        if root.is_file() and root.suffix in {".yaml", ".yml"}:
            files.append(root)
        elif root.is_dir():
            files.extend(sorted(root.rglob("*.yaml")))
            files.extend(sorted(root.rglob("*.yml")))
    return sorted(set(files))


def extract_record(path: Path) -> dict[str, Any] | None:
    try:
        data = load_yaml(path)
    except Exception:
        return None
    record = record_from_data(path, data)
    if not record:
        return None
    traceability = record.get("traceability", {}) or {}
    return {"path": str(path), "id": record.get("id"), "title": record.get("title"), "type": record.get("type"), "status": record.get("status", "unknown"), "depends_on": traceability.get("depends_on", []), "failures": traceability.get("related_failures", traceability.get("requirements", [])), "requirements": traceability.get("related_requirements", traceability.get("requirements", [])), "adrs": traceability.get("related_adrs", traceability.get("adrs", [])), "validators": traceability.get("validators", [])}


def find_duplicate_ids(files: list[Path]) -> list[str]:
    seen: dict[str, Path] = {}
    duplicates: list[str] = []
    for path in files:
        record = extract_record(path)
        if not record or not record.get("id"):
            continue
        record_id = str(record["id"])
        if record_id in seen:
            duplicates.append(f"duplicate id {record_id}: {seen[record_id]} and {path}")
        else:
            seen[record_id] = path
    return duplicates


def validate(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    files = collect_yaml_files(args.paths)
    if not files:
        print("No YAML files found.")
        return 0
    results = [validate_artifact(path, repo_root) for path in files]
    duplicate_messages = find_duplicate_ids(files)
    for result in results:
        print(f"{result.status.upper()}: {result.path}")
        for message in result.messages:
            print(f"  - {message}")
    for message in duplicate_messages:
        print(f"FAIL: {message}")
    return 1 if any(r.status == "fail" for r in results) or duplicate_messages else 0


def trace(args: argparse.Namespace) -> int:
    print(json.dumps([record for path in collect_yaml_files(args.paths) if (record := extract_record(path))], indent=2))
    return 0


def registry(args: argparse.Namespace) -> int:
    registry_data = {"registry": [record for path in collect_yaml_files(args.paths) if (record := extract_record(path))]}
    if args.output:
        write_yaml(Path(args.output), registry_data)
        print(f"Wrote ID registry: {args.output}")
    else:
        print(yaml.safe_dump(registry_data, sort_keys=False))
    return 0


def registry_report_cmd(args: argparse.Namespace) -> int:
    report = registry_report()
    if args.output:
        write_yaml(Path(args.output), report)
        print(f"Wrote schema registry report: {args.output}")
    else:
        print(yaml.safe_dump(report, sort_keys=False))
    return 0


def registry_check(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    missing = [registration.schema_path for registration in SCHEMA_REGISTRY if not (repo_root / registration.schema_path).exists()]
    for required_keys, schema_path, _record_type in SPECIAL_SCHEMA_RULES:
        if not (repo_root / schema_path).exists():
            missing.append(schema_path)
    if missing:
        print("FAIL: missing registered schemas")
        for schema in sorted(set(missing)):
            print(f"  - {schema}")
        return 1
    print(f"PASS: {len(SCHEMA_REGISTRY)} registered schemas and {len(SPECIAL_SCHEMA_RULES)} special rules are available")
    return 0


def id_audit_cmd(args: argparse.Namespace) -> int:
    report = audit_ids(args.repo_root)
    if args.output:
        write_yaml(Path(args.output), report)
        print(f"Wrote ID audit report: {args.output}")
    else:
        print(yaml.safe_dump(report, sort_keys=False))
    return 0 if report["id_audit_report"]["status"] == "pass" else 1


def repo_inventory_cmd(args: argparse.Namespace) -> int:
    inventory = create_repository_inventory(args.repo_root).to_dict()
    if args.output:
        write_yaml(Path(args.output), inventory)
        print(f"Wrote repository inventory: {args.output}")
    else:
        print(yaml.safe_dump(inventory, sort_keys=False))
    return 0


def repo_health_cmd(args: argparse.Namespace) -> int:
    inventory = create_repository_inventory(args.repo_root)
    summary = create_repository_health_summary(inventory)
    if args.output:
        write_yaml(Path(args.output), summary)
        print(f"Wrote repository health summary: {args.output}")
    else:
        print(yaml.safe_dump(summary, sort_keys=False))
    return 0 if summary["repository_health_summary"]["status"] == "pass" else 1


def repo_audit_cmd(args: argparse.Namespace) -> int:
    audit = run_repository_audit(args.repo_root)
    if args.format == "markdown":
        output = audit_to_markdown(audit)
        if args.output:
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8")
            print(f"Wrote repository audit markdown: {args.output}")
        else:
            print(output)
    elif args.format == "json":
        output = json.dumps(audit.to_dict(), indent=2)
        if args.output:
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8")
            print(f"Wrote repository audit JSON: {args.output}")
        else:
            print(output)
    else:
        report = audit.to_dict()
        if args.output:
            write_yaml(Path(args.output), report)
            print(f"Wrote repository audit YAML: {args.output}")
        else:
            print(yaml.safe_dump(report, sort_keys=False))
    return 0 if audit.beta_readiness["beta_readiness_report"]["status"] == "ready" else 1


def export_markdown(args: argparse.Namespace) -> int:
    source = Path(args.source)
    data = load_yaml(source)
    record = record_from_data(source, data) or {}
    lines = [f"# {record.get('title') or source.stem}", ""]
    for key, value in record.items():
        if key != "traceability":
            lines.append(f"- **{key}:** {value}")
    lines.append("")
    sections = ["description", "content", "traceability", "failed_constraints", "instruction", "approved_constraints", "regression_policy", "items", "summary", "history", "outputs", "approvals", "stages", "stop_conditions", "metadata", "plates", "build_policy", "results", "recommendation", "endpoints", "owns", "does_not_own", "request", "payload", "output", "messages", "worker_job_types", "queue_status", "worker_status", "failure_status", "schemas", "registrations"]
    for section in sections:
        if section in data:
            lines.extend([f"## {section.replace('_', ' ').title()}", "", "```yaml", yaml.safe_dump(data[section], sort_keys=False).strip(), "```", ""])
    target = Path(args.output or source.with_suffix(".md"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote markdown: {target}")
    return 0


def compile_spec(args: argparse.Namespace) -> int:
    result = compile_to_text(load_yaml(Path(args.source)), renderer=args.renderer)
    payload = result.to_dict()
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2) if args.format == "json" else result.instruction, encoding="utf-8")
        print(f"Wrote compiled instruction: {target}")
    else:
        print(json.dumps(payload, indent=2) if args.format == "json" else result.instruction)
    return 1 if result.unsupported_constraints and args.fail_on_unsupported else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="constraintos")
    sub = parser.add_subparsers(dest="command", required=True)
    artifact = sub.add_parser("new-artifact"); artifact.add_argument("id"); artifact.add_argument("title"); artifact.add_argument("--type", default="artifact"); artifact.add_argument("--output"); artifact.set_defaults(func=new_artifact)
    failure = sub.add_parser("new-failure"); failure.add_argument("id"); failure.add_argument("title"); failure.add_argument("--family", default="F100"); failure.add_argument("--severity", default="major", choices=["blocker", "major", "minor", "advisory"]); failure.add_argument("--output"); failure.set_defaults(func=new_failure)
    compliance = sub.add_parser("new-compliance"); compliance.add_argument("id"); compliance.add_argument("artifact_id"); compliance.add_argument("specification_id"); compliance.add_argument("--artifact-version", default="0.1"); compliance.add_argument("--output"); compliance.set_defaults(func=new_compliance)
    patch = sub.add_parser("new-patch"); patch.add_argument("id"); patch.add_argument("report"); patch.add_argument("--output"); patch.set_defaults(func=new_patch)
    baseline = sub.add_parser("new-baseline"); baseline.add_argument("artifact_id"); baseline.add_argument("artifact_version"); baseline.add_argument("approved_report_id"); baseline.add_argument("--constraints", default=""); baseline.add_argument("--output"); baseline.set_defaults(func=new_baseline)
    val = sub.add_parser("validate"); val.add_argument("paths", nargs="*", default=["docs", "examples", "reports", "patches", "baselines"]); val.add_argument("--repo-root", default="."); val.set_defaults(func=validate)
    tr = sub.add_parser("trace"); tr.add_argument("paths", nargs="*", default=["docs", "examples", "reports", "patches", "baselines"]); tr.set_defaults(func=trace)
    reg = sub.add_parser("registry"); reg.add_argument("paths", nargs="*", default=["docs", "examples", "reports", "patches", "baselines"]); reg.add_argument("--output"); reg.set_defaults(func=registry)
    reg_report = sub.add_parser("registry-report"); reg_report.add_argument("--output"); reg_report.set_defaults(func=registry_report_cmd)
    reg_check = sub.add_parser("registry-check"); reg_check.add_argument("--repo-root", default="."); reg_check.set_defaults(func=registry_check)
    id_audit_parser = sub.add_parser("id-audit"); id_audit_parser.add_argument("--repo-root", default="."); id_audit_parser.add_argument("--output"); id_audit_parser.set_defaults(func=id_audit_cmd)
    repo_inventory = sub.add_parser("repo-inventory"); repo_inventory.add_argument("--repo-root", default="."); repo_inventory.add_argument("--output"); repo_inventory.set_defaults(func=repo_inventory_cmd)
    repo_health = sub.add_parser("repo-health"); repo_health.add_argument("--repo-root", default="."); repo_health.add_argument("--output"); repo_health.set_defaults(func=repo_health_cmd)
    repo_audit = sub.add_parser("repo-audit"); repo_audit.add_argument("--repo-root", default="."); repo_audit.add_argument("--output"); repo_audit.add_argument("--format", choices=["yaml", "json", "markdown"], default="yaml"); repo_audit.set_defaults(func=repo_audit_cmd)
    md = sub.add_parser("export-md"); md.add_argument("source"); md.add_argument("--output"); md.set_defaults(func=export_markdown)
    comp = sub.add_parser("compile"); comp.add_argument("source"); comp.add_argument("--renderer", default="generic"); comp.add_argument("--format", choices=["text", "json"], default="text"); comp.add_argument("--output"); comp.add_argument("--fail-on-unsupported", action="store_true"); comp.set_defaults(func=compile_spec)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
