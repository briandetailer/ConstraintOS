from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from constraintos.constraint_pack import apply_constraint_pack
from constraintos.render_contract import compile_render_contract_to_runtime
from constraintos.schema_validation import require_registered_schema
from runtime import ArtifactStore, RuntimeContext, RuntimeEngine, RuntimeReportWriter
from runtime.execution import create_default_plugin_executor
from runtime.planner import DependencyResolver, RuntimePlanner
from runtime.scheduler import RuntimeScheduler, WorkerCapability

DEFAULT_WORKERS = ["WORKER-0001:generic,echo,dry_run"]
DEFAULT_RENDER_CONTRACT_WORKERS = ["WORKER-0001:render_contract"]


def load_data_file(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if yaml is None:
        raise RuntimeError("PyYAML is required")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_specification(path: Path) -> dict[str, Any]:
    data = load_data_file(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain an object")
    return data


def apply_constraint_pack_files(
    specification: dict[str, Any],
    constraint_pack_paths: list[str] | None,
    validate_schema: bool = False,
) -> dict[str, Any]:
    applied = specification
    for constraint_pack_path in constraint_pack_paths or []:
        path = Path(constraint_pack_path)
        constraint_pack = load_specification(path)
        if validate_schema:
            require_registered_schema(path, constraint_pack, expected_record_type="constraint_pack")
        applied = apply_constraint_pack(applied, constraint_pack)
    return applied


def load_runtime_specification(
    path: Path,
    render_contract: bool = False,
    constraint_pack_paths: list[str] | None = None,
) -> dict[str, Any]:
    specification = load_specification(path)
    if constraint_pack_paths and not render_contract:
        raise ValueError("--constraint-pack requires --render-contract")
    if render_contract:
        require_registered_schema(path, specification, expected_record_type="render_specification")
        specification = apply_constraint_pack_files(specification, constraint_pack_paths, validate_schema=True)
        return compile_render_contract_to_runtime(specification)
    return specification


def parse_worker(value: str) -> WorkerCapability:
    worker_id, separator, plugins = value.partition(":")
    if not worker_id or not separator:
        raise argparse.ArgumentTypeError("workers must use WORKER-ID:plugin-a,plugin-b format")
    plugin_list = [plugin.strip() for plugin in plugins.split(",") if plugin.strip()]
    if not plugin_list:
        raise argparse.ArgumentTypeError("workers must declare at least one plugin")
    return WorkerCapability(worker_id=worker_id, plugins=plugin_list)


def normalize_plugins(value: Any, source: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{source} must declare plugins")
    plugins: list[str] = []
    for plugin in value:
        if not isinstance(plugin, str) or not plugin.strip():
            raise ValueError(f"{source} plugins must be non-empty strings")
        plugins.append(plugin.strip())
    return plugins


def load_workers_file(path: Path) -> list[WorkerCapability]:
    data = load_data_file(path)
    raw_workers = data.get("workers") if isinstance(data, dict) else data
    if not isinstance(raw_workers, list) or not raw_workers:
        raise ValueError(f"{path} must contain a non-empty workers list")
    workers: list[WorkerCapability] = []
    for index, raw_worker in enumerate(raw_workers, start=1):
        if not isinstance(raw_worker, dict):
            raise ValueError(f"{path} worker {index} must be an object")
        worker_id = raw_worker.get("worker_id") or raw_worker.get("id")
        if not worker_id:
            raise ValueError(f"{path} worker {index} is missing worker_id")
        worker_source = f"{path} worker {index}"
        workers.append(
            WorkerCapability(
                worker_id=str(worker_id),
                plugins=normalize_plugins(raw_worker.get("plugins"), worker_source),
                status=str(raw_worker.get("status", "available")),
            )
        )
    return workers


def workers_from_args(
    raw_workers: list[str] | None,
    workers_file: str | None = None,
    default_workers: list[str] | None = None,
) -> list[WorkerCapability]:
    workers: list[WorkerCapability] = []
    if workers_file:
        workers.extend(load_workers_file(Path(workers_file)))
    if raw_workers:
        workers.extend(parse_worker(worker) for worker in raw_workers)
    return workers or [parse_worker(worker) for worker in (default_workers or DEFAULT_WORKERS)]


def constraint_pack_references(specification: dict[str, Any]) -> list[dict[str, Any]]:
    render_contract = specification.get("render_contract", {})
    if isinstance(render_contract, dict) and isinstance(render_contract.get("constraint_packs"), list):
        return [deepcopy(item) for item in render_contract["constraint_packs"] if isinstance(item, dict)]
    artifact = specification.get("artifact", {})
    if isinstance(artifact, dict) and isinstance(artifact.get("constraint_packs"), list):
        return [deepcopy(item) for item in artifact["constraint_packs"] if isinstance(item, dict)]
    return []


def traceability_payload(specification: dict[str, Any]) -> dict[str, Any]:
    references = constraint_pack_references(specification)
    payload: dict[str, Any] = {}
    artifact = specification.get("artifact", {})
    if isinstance(artifact, dict) and references:
        payload["artifact"] = {"id": artifact.get("id"), "constraint_packs": references}
    render_contract = specification.get("render_contract", {})
    if isinstance(render_contract, dict) and references:
        payload["render_contract"] = {
            "render_specification_id": render_contract.get("render_specification_id"),
            "constraint_packs": references,
        }
    return payload


def attach_traceability(payload: dict[str, Any], specification: dict[str, Any]) -> dict[str, Any]:
    payload.update(traceability_payload(specification))
    return payload


def plan_runtime(specification: dict[str, Any], workers: list[WorkerCapability]) -> dict[str, Any]:
    planner = RuntimePlanner()
    resolver = DependencyResolver()
    scheduler = RuntimeScheduler()
    plan = planner.build(specification)
    resolver.validate(plan)
    schedule = scheduler.schedule(plan, workers)
    return attach_traceability({"plan": plan.to_dict(), "schedule": schedule.to_dict()}, specification)


def constraint_pack_count(payload: dict[str, Any]) -> int:
    render_contract = payload.get("render_contract", {})
    if isinstance(render_contract, dict) and isinstance(render_contract.get("constraint_packs"), list):
        return len(render_contract["constraint_packs"])
    artifact = payload.get("artifact", {})
    if isinstance(artifact, dict) and isinstance(artifact.get("constraint_packs"), list):
        return len(artifact["constraint_packs"])
    return 0


def summarize_payload(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    runtime_result = payload.get("runtime_result")
    if isinstance(runtime_result, dict):
        lines.append(
            f"Runtime {runtime_result.get('id', 'unknown')}: "
            f"{runtime_result.get('status', 'unknown')} (success={runtime_result.get('success', False)})"
        )
    plan = payload.get("plan")
    if isinstance(plan, dict):
        plan_header = plan.get("execution_plan", {})
        required_plugins = ",".join(plan.get("required_plugins", [])) or "none"
        lines.append(
            f"Plan {plan_header.get('id', 'unknown')}: {plan_header.get('status', 'unknown')} | "
            f"nodes={len(plan.get('nodes', []))} | stages={len(plan.get('stages', []))} | plugins={required_plugins}"
        )
    count = constraint_pack_count(payload)
    if count:
        lines.append(f"Constraint packs: {count}")
    schedule = payload.get("schedule")
    if isinstance(schedule, dict):
        schedule_header = schedule.get("schedule_result", {})
        lines.append(
            f"Schedule {schedule_header.get('id', 'unknown')}: {schedule_header.get('status', 'unknown')} | "
            f"assignments={len(schedule.get('assignments', []))} | unscheduled={len(schedule.get('unscheduled_nodes', []))}"
        )
    execution = payload.get("execution")
    if isinstance(execution, dict):
        execution_header = execution.get("execution_result", {})
        lines.append(f"Execution {execution_header.get('id', 'unknown')}: {execution_header.get('status', 'unknown')} | nodes={len(execution.get('node_results', []))}")
    artifacts = payload.get("artifacts")
    if isinstance(artifacts, dict):
        artifact_store = artifacts.get("artifact_store", {})
        lines.append(f"Artifacts: {artifact_store.get('count', 0)}")
    return "\n".join(lines) + "\n"


def format_payload(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "text":
        return summarize_payload(payload)
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def write_output(payload: dict[str, Any], output_path: str | None, label: str, output_format: str) -> None:
    output = format_payload(payload, output_format)
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
        print(f"Wrote {label}: {target}")
    else:
        print(output, end="")


def default_workers_for_mode(render_contract: bool) -> list[str]:
    return DEFAULT_RENDER_CONTRACT_WORKERS if render_contract else DEFAULT_WORKERS


def run_runtime(args: argparse.Namespace) -> int:
    workers = workers_from_args(args.worker, args.workers_file, default_workers_for_mode(args.render_contract))
    specification = load_runtime_specification(
        Path(args.specification),
        render_contract=args.render_contract,
        constraint_pack_paths=args.constraint_pack,
    )
    if args.plan_only:
        payload = plan_runtime(specification, workers)
        write_output(payload, args.output, "runtime plan", args.format)
        return 0 if not payload["schedule"].get("unscheduled_nodes") else 1
    artifact_store = ArtifactStore(Path(args.artifact_root))
    executor = create_default_plugin_executor() if args.plugin_executor else None
    engine = RuntimeEngine(executor=executor, artifact_store=artifact_store)
    result = engine.run(
        specification,
        workers,
        RuntimeContext(workspace=Path(args.workspace), variables={"specification": args.specification}),
        runtime_id=args.runtime_id,
    )
    payload = attach_traceability(result.to_dict(), specification)
    if args.report:
        RuntimeReportWriter(artifact_store).write_report(result)
        payload["artifacts"] = artifact_store.to_dict()
    write_output(payload, args.output, "runtime result", args.format)
    return 0 if result.success else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cos-runtime")
    parser.add_argument("specification")
    parser.add_argument("--worker", action="append")
    parser.add_argument("--workers-file")
    parser.add_argument("--runtime-id", default="RUNTIME-0001")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--artifact-root", default=".constraintos/runtime/artifacts")
    parser.add_argument("--plugin-executor", action="store_true")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--render-contract", action="store_true")
    parser.add_argument("--constraint-pack", action="append")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        return run_runtime(args)
    except SystemExit:
        raise
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
