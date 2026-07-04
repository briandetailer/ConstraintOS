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
    schema_map = [
        ("failure", "schemas/failure.schema.json"), ("registry", "schemas/id-registry.schema.json"),
        ("patch", "schemas/patch-package.schema.json"), ("baseline", "schemas/regression-baseline.schema.json"),
        ("approval", "schemas/approval-record.schema.json"), ("review_checklist", "schemas/review-checklist.schema.json"),
        ("build_plan", "schemas/build-plan.schema.json"), ("render_job", "schemas/render-job.schema.json"),
        ("output_reference", "schemas/output-reference.schema.json"), ("renderer_registry", "schemas/renderer-registry.schema.json"),
        ("stored_object", "schemas/stored-object.schema.json"), ("storage_backend", "schemas/storage-backend.schema.json"),
        ("volume_plan", "schemas/volume-plan.schema.json"), ("volume_build", "schemas/volume-build.schema.json"),
        ("volume_completion_report", "schemas/volume-completion-report.schema.json"),
        ("runtime_config", "schemas/runtime-config.schema.json"), ("runtime_job", "schemas/runtime-job.schema.json"),
        ("worker_profile", "schemas/worker-profile.schema.json"), ("worker_result", "schemas/worker-result.schema.json"),
        ("worker_job_types", "schemas/worker-job-type.schema.json"), ("worker_heartbeat", "schemas/worker-heartbeat.schema.json"),
        ("job_lease", "schemas/job-lease.schema.json"), ("lease_decision", "schemas/lease-decision.schema.json"),
        ("metric_event", "schemas/metric-event.schema.json"), ("api_catalog", "schemas/api-catalog.schema.json"),
        ("api_error", "schemas/api-error.schema.json"), ("service_boundary", "schemas/service-boundary.schema.json"),
        ("validation_request", "schemas/kernel-validation-request.schema.json"),
        ("queue_record", "schemas/queue-record.schema.json"), ("queue_status", "schemas/queue-status.schema.json"),
        ("retry_policy", "schemas/retry-policy.schema.json"), ("retry_decision", "schemas/retry-decision.schema.json"),
        ("failed_job", "schemas/failed-job.schema.json"),
    ]
    for key, schema in schema_map:
        if key in data:
            return schema
    if "status" in data and "service" in data and "version" in data:
        return "schemas/api-health.schema.json"
    if "status" in data and "message" in data and "request" in data and "repo_root" in data:
        return "schemas/api-validation-stub-response.schema.json"
    if "report" in data and "constraint_results" in data:
        return "schemas/compliance-report.schema.json"
    if "manifest" in data and "history" in data:
        return "schemas/artifact-manifest.schema.json"
    if "gate" in data and "blocked_items" in data:
        return "schemas/review-gate.schema.json"
    if "iteration" in data and "stage" in data and "artifact_id" in data:
        return "schemas/iteration-record.schema.json"
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
    return [f"schema:{schema_path}:{'.'.join(str(p) for p in error.path) or '<root>'}: {error.message}" for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))]


def record_from_data(path: Path, data: dict[str, Any]) -> dict[str, Any] | None:
    if "artifact" in data and "constraints" in data:
        obj = data["artifact"]
        return {"id": obj.get("id"), "title": obj.get("title", obj.get("id")), "type": obj.get("type", "csl_artifact"), "status": obj.get("status", "unknown"), "traceability": data.get("traceability", {})}
    if "artifact" in data and "traceability" in data:
        obj = data["artifact"]
        return {"id": obj.get("id"), "title": obj.get("title", obj.get("id")), "type": obj.get("type", "artifact"), "status": obj.get("status", "unknown"), "traceability": data.get("traceability", {})}
    simple_objects = [
        ("failure", "failure"), ("report", "compliance_report"), ("patch", "patch_package"), ("approval", "approval_record"),
        ("review_checklist", "review_checklist"), ("build_plan", "build_plan"), ("render_job", "render_job"),
        ("output_reference", "output_reference"), ("stored_object", "stored_object"), ("storage_backend", "storage_backend"),
        ("volume_plan", "volume_plan"), ("volume_build", "volume_build"), ("volume_completion_report", "volume_completion_report"),
        ("runtime_config", "runtime_config"), ("runtime_job", "runtime_job"), ("worker_profile", "worker_profile"),
        ("worker_result", "worker_result"), ("worker_job_types", "worker_job_type_registry"),
        ("worker_heartbeat", "worker_heartbeat"), ("job_lease", "job_lease"), ("lease_decision", "lease_decision"),
        ("metric_event", "metric_event"), ("api_catalog", "api_catalog"), ("api_error", "api_error"),
        ("service_boundary", "service_boundary"), ("validation_request", "validation_request"),
        ("queue_record", "queue_record"), ("queue_status", "queue_status"),
        ("retry_policy", "retry_policy"), ("retry_decision", "retry_decision"), ("failed_job", "failed_job"),
    ]
    for key, record_type in simple_objects:
        if key in data:
            obj = data[key]
            object_id = obj.get("id") if isinstance(obj, dict) else None
            object_id = object_id or (obj.get("name") if isinstance(obj, dict) else None) or (obj.get("worker_id") if isinstance(obj, dict) else None) or path.stem
            status = obj.get("status", "unknown") if isinstance(obj, dict) else "active"
            title = obj.get("title", object_id) if isinstance(obj, dict) else object_id
            return {"id": object_id, "title": title, "type": record_type, "status": status, "traceability": {}}
    if "status" in data and "service" in data and "version" in data:
        return {"id": path.stem, "title": path.stem, "type": "api_health_response", "status": data.get("status", "unknown"), "traceability": {}}
    if "status" in data and "message" in data and "request" in data and "repo_root" in data:
        return {"id": path.stem, "title": path.stem, "type": "api_validation_stub_response", "status": data.get("status", "unknown"), "traceability": {}}
    if "baseline" in data:
        obj = data["baseline"]
        baseline_id = f"BASELINE-{obj.get('artifact_id', path.stem)}-{obj.get('artifact_version', 'unknown')}"
        return {"id": baseline_id, "title": baseline_id, "type": "regression_baseline", "status": obj.get("status", "unknown"), "traceability": {}}
    if "manifest" in data:
        obj = data["manifest"]
        artifact = data.get("artifact", {})
        return {"id": obj.get("id"), "title": artifact.get("title", obj.get("id")), "type": "artifact_manifest", "status": data.get("state", "unknown"), "traceability": {}}
    if "gate" in data and "blocked_items" in data:
        return {"id": path.stem, "title": path.stem, "type": "review_gate", "status": data.get("gate", "unknown"), "traceability": {}}
    if "iteration" in data and "stage" in data and "artifact_id" in data:
        return {"id": path.stem, "title": path.stem, "type": "iteration_record", "status": data.get("status", "unknown"), "traceability": {}}
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
    data = {"report": {"id": report_id, "version": "0.1", "created": date.today().isoformat(), "validator_version": "constraintos-1.0.0-alpha.19"}, "artifact": {"id": args.artifact_id, "version": args.artifact_version, "specification_id": args.specification_id}, "summary": {"blocker_failures": 0, "major_failures": 0, "minor_failures": 0, "uncertain_results": 0}, "constraint_results": [], "recommendation": "escalate"}
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
    schema_exempt = ["report", "patch", "baseline", "manifest", "approval", "review_checklist", "gate", "build_plan", "iteration", "render_job", "output_reference", "renderer_registry", "stored_object", "storage_backend", "volume_plan", "volume_build", "volume_completion_report", "runtime_config", "runtime_job", "worker_profile", "worker_result", "worker_job_types", "worker_heartbeat", "job_lease", "lease_decision", "metric_event", "api_catalog", "api_error", "service_boundary", "validation_request", "queue_record", "queue_status", "retry_policy", "retry_decision", "failed_job", "status", "name", "renderer"]
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
    for section in ["description", "content", "traceability", "failed_constraints", "instruction", "approved_constraints", "regression_policy", "items", "summary", "history", "outputs", "approvals", "stages", "stop_conditions", "metadata", "plates", "build_policy", "results", "recommendation", "endpoints", "owns", "does_not_own", "request", "payload", "output", "messages", "worker_job_types"]:
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
