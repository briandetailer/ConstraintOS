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


def load_specification(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        if yaml is None:
            raise RuntimeError("PyYAML is required")
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
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


def workers_from_args(raw_workers: list[str] | None) -> list[WorkerCapability]:
    return [parse_worker(worker) for worker in (raw_workers or DEFAULT_WORKERS)]


def plan_runtime(specification: dict[str, Any], workers: list[WorkerCapability]) -> dict[str, Any]:
    planner = RuntimePlanner()
    resolver = DependencyResolver()
    scheduler = RuntimeScheduler()
    plan = planner.build(specification)
    resolver.validate(plan)
    schedule = scheduler.schedule(plan, workers)
    return {
        "plan": plan.to_dict(),
        "schedule": schedule.to_dict(),
    }


def write_json_output(payload: dict[str, Any], output_path: str | None, label: str) -> None:
    output = json.dumps(payload, indent=2, sort_keys=True)
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output + "\n", encoding="utf-8")
        print(f"Wrote {label}: {target}")
    else:
        print(output)


def run_runtime(args: argparse.Namespace) -> int:
    workers = workers_from_args(args.worker)
    specification = load_specification(Path(args.specification))
    if args.plan_only:
        payload = plan_runtime(specification, workers)
        write_json_output(payload, args.output, "runtime plan")
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
    payload = result.to_dict()
    if args.report:
        RuntimeReportWriter(artifact_store).write_report(result)
        payload["artifacts"] = artifact_store.to_dict()
    write_json_output(payload, args.output, "runtime result")
    return 0 if result.success else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cos-runtime")
    parser.add_argument("specification")
    parser.add_argument("--worker", action="append")
    parser.add_argument("--runtime-id", default="RUNTIME-0001")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--artifact-root", default=".constraintos/runtime/artifacts")
    parser.add_argument("--plugin-executor", action="store_true")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--report", action="store_true")
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
