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
from constraintos.patching import create_patch_package, create_regression_baseline

ID_PATTERN = re.compile(r"^[A-Z]+-[0-9]{4}$")
FR_PATTERN = re.compile(r"^FR-[0-9]{4}$")


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
    if "failure" in data:
        return "schemas/failure.schema.json"
    if "report" in data and "constraint_results" in data:
        return "schemas/compliance-report.schema.json"
    if "registry" in data:
        return "schemas/id-registry.schema.json"
    if "patch" in data:
        return "schemas/patch-package.schema.json"
    if "baseline" in data:
        return "schemas/regression-baseline.schema.json"
    if "manifest" in data and "history" in data:
        return "schemas/artifact-manifest.schema.json"
    if "approval" in data:
        return "schemas/approval-record.schema.json"
    if "review_checklist" in data:
        return "schemas/review-checklist.schema.json"
    if "gate" in data and "blocked_items" in data:
        return "schemas/review-gate.schema.json"
    if "build_plan" in data:
        return "schemas/build-plan.schema.json"
    if "iteration" in data and "stage" in data and "artifact_id" in data:
        return "schemas/iteration-record.schema.json"
    if "render_job" in data:
        return "schemas/render-job.schema.json"
    if "output_reference" in data:
        return "schemas/output-reference.schema.json"
    if "renderer_registry" in data:
        return "schemas/renderer-registry.schema.json"
    if "name" in data and "supported_constraint_types" in data:
        return "schemas/renderer-profile.schema.json"
    if "renderer" in data and "instruction" in data and "unsupported_constraints" in data:
        return "schemas/compiler-result.schema.json"
    if "artifact" in data and "constraints" in data and "validation" in data:
        return "schemas/csl.schema.json"
    return None


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
    return [f"schema:{schema_path}:{'.'.join(str(p) for p in e.path) or '<root>'}: {e.message}" for e in sorted(validator.iter_errors(data), key=lambda error: list(error.path))]


def record_from_data(path: Path, data: dict[str, Any]) -> dict[str, Any] | None:
    if "artifact" in data and "constraints" in data:
        obj = data["artifact"]
        return {"id": obj.get("id"), "title": obj.get("title", obj.get("id")), "type": obj.get("type", "csl_artifact"), "status": obj.get("status", "unknown"), "traceability": data.get("traceability", {})}
    if "artifact" in data and "traceability" in data:
        obj = data["artifact"]
        return {"id": obj.get("id"), "title": obj.get("title", obj.get("id")), "type": obj.get("type", "artifact"), "status": obj.get("status", "unknown"), "traceability": data.get("traceability", {})}
    if "failure" in data:
        obj = data["failure"]
        return {"id": obj.get("id"), "title": obj.get("title", obj.get("id")), "type": "failure", "status": obj.get("status", "unknown"), "traceability": data.get("traceability", {})}
    if "report" in data:
        obj = data["report"]
        return {"id": obj.get("id"), "title": obj.get("id"), "type": "compliance_report", "status": obj.get("status", "unknown"), "traceability": {}}
    if "patch" in data:
        obj = data["patch"]
        return {"id": obj.get("id"), "title": obj.get("id"), "type": "patch_package", "status": obj.get("status", "unknown"), "traceability": {}}
    if "baseline" in data:
        obj = data["baseline"]
        baseline_id = f"BASELINE-{obj.get('artifact_id', path.stem)}-{obj.get('artifact_version', 'unknown')}"
        return {"id": baseline_id, "title": baseline_id, "type": "regression_baseline", "status": obj.get("status", "unknown"), "traceability": {}}
    if "manifest" in data:
        obj = data["manifest"]
        artifact = data.get("artifact", {})
        return {"id": obj.get("id"), "title": artifact.get("title", obj.get("id")), "type": "artifact_manifest", "status": data.get("state", "unknown"), "traceability": {}}
    if "approval" in data:
        obj = data["approval"]
        return {"id": obj.get("id"), "title": obj.get("id"), "type": "approval_record", "status": obj.get("status", "unknown"), "traceability": {}}
    if "review_checklist" in data:
        obj = data["review_checklist"]
        return {"id": obj.get("id"), "title": obj.get("id"), "type": "review_checklist", "status": obj.get("status", "unknown"), "traceability": {}}
    if "gate" in data and "blocked_items" in data:
        return {"id": path.stem, "title": path.stem, "type": "review_gate", "status": data.get("gate", "unknown"), "traceability": {}}
    if "build_plan" in data:
        obj = data["build_plan"]
        return {"id": obj.get("id"), "title": obj.get("id"), "type": "build_plan", "status": obj.get("status", "unknown"), "traceability": {}}
    if "iteration" in data and "stage" in data and "artifact_id" in data:
        return {"id": path.stem, "title": path.stem, "type": "iteration_record", "status": data.get("status", "unknown"), "traceability": {}}
    if "render_job" in data:
        obj = data["render_job"]
        return {"id": obj.get("id"), "title": obj.get("id"), "type": "render_job", "status": obj.get("status", "unknown"), "traceability": {}}
    if "output_reference" in data:
        obj = data["output_reference"]
        return {"id": obj.get("id"), "title": obj.get("id"), "type": "output_reference", "status": "stored", "traceability": {}}
    if "renderer_registry" in data:
        return {"id": "RENDERER-REGISTRY", "title": "Renderer Registry", "type": "renderer_registry", "status": "active", "traceability": {}}
    if "name" in data and "supported_constraint_types" in data:
        renderer_id = f"RENDERER-{data.get('name', path.stem)}"
        return {"id": renderer_id, "title": data.get("name", renderer_id), "type": "renderer_profile", "status": "active", "traceability": {}}
    if "renderer" in data and "instruction" in data:
        compiler_id = f"COMPILER-RESULT-{data.get('artifact_id', path.stem)}"
        return {"id": compiler_id, "title": compiler_id, "type": "compiler_result", "status": "generated", "traceability": {}}
    return None


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
    data = {"report": {"id": report_id, "version": "0.1", "created": date.today().isoformat(), "validator_version": "constraintos-1.0.0-alpha.10"}, "artifact": {"id": args.artifact_id, "version": args.artifact_version, "specification_id": args.specification_id}, "summary": {"blocker_failures": 0, "major_failures": 0, "minor_failures": 0, "uncertain_results": 0}, "constraint_results": [], "recommendation": "escalate"}
    write_yaml(target, data)
    print(f"Created compliance report: {target}")
    return 0


def new_patch(args: argparse.Namespace) -> int:
    patch_id = args.id.upper()
    if not patch_id.startswith("PATCH-") or not ID_PATTERN.match(patch_id):
        print(f"Invalid patch id: {patch_id}. Expected format like PATCH-0001.", file=sys.stderr)
        return 2
    package = create_patch_package(load_yaml(Path(args.report)), patch_id)
    target = Path(args.output or f"patches/{patch_id}.yaml")
    write_yaml(target, package.to_dict())
    print(f"Created patch package: {target}")
    return 0


def new_baseline(args: argparse.Namespace) -> int:
    constraints = [item for item in args.constraints.split(",") if item]
    data = create_regression_baseline(args.artifact_id, args.artifact_version, args.approved_report_id, constraints)
    target = Path(args.output or f"baselines/{args.artifact_id}_{args.artifact_version}.yaml")
    write_yaml(target, data)
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
    schema_exempt = ["report", "patch", "baseline", "manifest", "approval", "review_checklist", "gate", "build_plan", "iteration", "render_job", "output_reference", "renderer_registry", "name", "renderer"]
    if "traceability" not in data and not any(key in data for key in schema_exempt):
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


def export_markdown(args: argparse.Namespace) -> int:
    source = Path(args.source)
    data = load_yaml(source)
    record = record_from_data(source, data) or {}
    lines = [f"# {record.get('title') or source.stem}", ""]
    for key, value in record.items():
        if key != "traceability":
            lines.append(f"- **{key}:** {value}")
    lines.append("")
    for section in ["description", "content", "traceability", "failed_constraints", "instruction", "approved_constraints", "regression_policy", "items", "summary", "history", "outputs", "approvals", "stages", "stop_conditions", "metadata"]:
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
    md = sub.add_parser("export-md"); md.add_argument("source"); md.add_argument("--output"); md.set_defaults(func=export_markdown)
    comp = sub.add_parser("compile"); comp.add_argument("source"); comp.add_argument("--renderer", default="generic"); comp.add_argument("--format", choices=["text", "json"], default="text"); comp.add_argument("--output"); comp.add_argument("--fail-on-unsupported", action="store_true"); comp.set_defaults(func=compile_spec)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
