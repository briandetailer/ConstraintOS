from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from runtime import ArtifactStore, RuntimeContext, RuntimeEngine, RuntimeReportWriter
from runtime.execution import create_default_plugin_executor
from runtime.planner import DependencyResolver, RuntimePlanner
from runtime.scheduler import RuntimeScheduler, WorkerCapability

DEFAULT_WORKERS = ["WORKER-0001:generic,echo,dry_run"]


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


def parse_worker(value: str) -> WorkerCapability:
    worker_id, separator, plugins = value.partition(":")
    if not worker_id or not separator:
        raise argparse.ArgumentTypeError("workers must use WORKER-ID:plugin-a,plugin-b format")
    plugin_list = [plugin.strip() for plugin in plugins.split(",") if plugin.strip()]
    if not plugin_list:
        raise argparse.ArgumentTypeError("workers must declare at least one plugin")
    return WorkerCapability(worker_id=worker_id, plugins=plugin_list)


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
        plugins = raw_worker.get("plugins")
        if not worker_id:
            raise ValueError(f"{path} worker {index} is missing worker_id")
        if not isinstance(plugins, list) or not plugins:
            raise ValueError(f"{path} worker {index} must declare plugins")
        workers.append(WorkerCapability(worker_id=str(worker_id), plugins=[str(plugin) for plugin in plugins], status=str(raw_worker.get("status", "available"))))
    return workers


def workers_from_args(raw_workers: list[str] | None, workers_file: str | None = None) -> list[WorkerCapability]:
    workers: list[WorkerCapability] = []
    if workers_file:
        workers.extend(load_workers_file(Path(workers_file)))
    if raw_workers:
        workers.extend(parse_worker(worker) for worker in raw_workers)
    return workers or [parse_worker(worker) for worker in DEFAULT_WORKERS]


def plan_runtime(specification: dict[str, Any], workers: list[WorkerCapability]) -> dict[str, Any]:
    planner = RuntimePlanner()
    resolver = DependencyResolver()
    scheduler = RuntimeScheduler()
    plan = planner.build(specification)
    resolver.validate(plan)
    schedule = scheduler.schedule(plan, workers)
    return {"plan": plan.to_dict(), "schedule": schedule.to_dict()}


def summarize_payload(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    runtime_result = payload.get("runtime_result")
    if isinstance(runtime_result, dict):
        lines.append(f"Runtime {runtime_result.get('id', 'unknown')}: {runtime_result.get('status', 'unknown')} (success={runtime_result.get('success', False)})")
    plan = payload.get("plan")
    if isinstance(plan, dict):
        plan_header = plan.get("execution_plan", {})
        required_plugins = ",".join(plan.get("required_plugins", [])) or "none"
        lines.append(f"Plan {plan_header.get('id', 'unknown')}: {plan_header.get('status', 'unknown')} | nodes={len(plan.get('nodes', []))} | stages={len(plan.get('stages', []))} | plugins={required_plugins}")
    schedule = payload.get("schedule")
    if isinstance(schedule, dict):
        schedule_header = schedule.get("schedule_result", {})
        lines.append(f"Schedule {schedule_header.get('id', 'unknown')}: {schedule_header.get('status', 'unknown')} | assignments={len(schedule.get('assignments', []))} | unscheduled={len(schedule.get('unscheduled_nodes', []))}")
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


def run_runtime(args: argparse.Namespace) -> int:
    workers = workers_from_args(args.worker, args.workers_file)
    specification = load_specification(Path(args.specification))
    if args.plan_only:
        payload = plan_runtime(specification, workers)
        write_output(payload, args.output, "runtime plan", args.format)
        return 0 if not payload["schedule"].get("unscheduled_nodes") else 1
    artifact_store = ArtifactStore(Path(args.artifact_root))
    executor = create_default_plugin_executor() if args.plugin_executor else None
    engine = RuntimeEngine(executor=executor, artifact_store=artifact_store)
    result = engine.run(specification, workers, RuntimeContext(workspace=Path(args.workspace), variables={"specification": args.specification}), runtime_id=args.runtime_id)
    payload = result.to_dict()
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
