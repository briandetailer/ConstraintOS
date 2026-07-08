from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from constraintos.graphics_contract_runtime import build_contract_runtime_payload
from constraintos.graphics_contracts import (
    GraphicsContractError,
    discover_project_root,
    list_contract_summaries,
    load_contract_report,
    resolve_contracts_dir,
)


def build_payload(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    project_root = Path(args.project_root).resolve() if args.project_root else discover_project_root()
    contracts_dir = resolve_contracts_dir(project_root, args.contracts_dir)
    if args.command == "list":
        contracts = list_contract_summaries(contracts_dir)
        return 0, {
            "graphics_contracts": {
                "count": len(contracts),
                "contracts_dir": str(contracts_dir),
            },
            "contracts": contracts,
        }
    if args.command == "show":
        report = load_contract_report(args.contract, contracts_dir)
        report["graphics_contracts"] = {
            "contracts_dir": str(contracts_dir),
            "selected": report["summary"]["key"],
        }
        return 0, report
    if args.command == "run":
        report = load_contract_report(args.contract, contracts_dir)
        exit_code, payload = build_contract_runtime_payload(
            report["summary"]["key"],
            report["contract"],
            plan_only=args.plan_only,
            artifact_root=args.artifact_root,
            workspace=args.workspace,
            runtime_id=args.runtime_id,
        )
        payload["graphics_contracts"] = {
            "contracts_dir": str(contracts_dir),
            "selected": report["summary"]["key"],
            "runtime_bridge": True,
        }
        return exit_code, payload
    raise GraphicsContractError(f"Unsupported command: {args.command}")


def format_list_text(payload: dict[str, Any]) -> str:
    header = payload.get("graphics_contracts", {})
    contracts = payload.get("contracts", [])
    lines = [f"Graphics contracts: {header.get('count', 0)}"]
    if isinstance(contracts, list):
        for item in contracts:
            if not isinstance(item, dict):
                continue
            lines.append(
                "- "
                + f"{item.get('key', 'unknown')} | "
                + f"subject={item.get('subject', 'unknown')} | "
                + f"decision={item.get('expected_initial_decision', 'unknown')} | "
                + f"mode={item.get('mode', 'unknown')} | "
                + f"labels={item.get('required_label_count', 0)}"
            )
    return "\n".join(lines) + "\n"


def format_show_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        f"Graphics contract: {summary.get('key', 'unknown')}",
        f"subject: {summary.get('subject', 'unknown')}",
        f"category: {summary.get('category', 'unknown')}",
        f"mode: {summary.get('mode', 'unknown')}",
        f"view: {summary.get('view', 'unknown')}",
        f"style: {summary.get('style', 'unknown')}",
        f"expected_initial_decision: {summary.get('expected_initial_decision', 'unknown')}",
        f"required_labels: {summary.get('required_label_count', 0)}",
        f"forbidden_substitutions: {summary.get('forbidden_substitution_count', 0)}",
        f"source_use_case: {summary.get('source_use_case', 'unknown')}",
        f"guardrail: {summary.get('guardrail', 'unknown')}",
        "image_generation: not run",
    ]
    return "\n".join(lines) + "\n"


def format_run_text(payload: dict[str, Any]) -> str:
    metadata = payload.get("graphics_contract_runtime", {})
    if not isinstance(metadata, dict):
        metadata = {}
    plan = payload.get("plan", {})
    schedule = payload.get("schedule", {})
    execution = payload.get("execution", {})
    runtime_result = payload.get("runtime_result", {})
    nodes = plan.get("nodes", []) if isinstance(plan, dict) else []
    unscheduled = schedule.get("unscheduled_nodes", []) if isinstance(schedule, dict) else []
    schedule_result = schedule.get("schedule_result", {}) if isinstance(schedule, dict) else {}
    execution_result = execution.get("execution_result", {}) if isinstance(execution, dict) else {}
    lines = [
        f"Graphics contract runtime: {metadata.get('contract_key', 'unknown')}",
        f"subject: {metadata.get('subject', 'unknown')}",
        f"mode: {metadata.get('mode', 'unknown')}",
        f"expected_decision: {metadata.get('expected_decision', 'unknown')}",
        f"plan_nodes: {len(nodes) if isinstance(nodes, list) else 0}",
        f"schedule: {schedule_result.get('status', 'unknown') if isinstance(schedule_result, dict) else 'unknown'}",
        f"unscheduled_nodes: {len(unscheduled) if isinstance(unscheduled, list) else 0}",
        f"execution: {execution_result.get('status', 'not_run_plan_only') if isinstance(execution_result, dict) else 'not_run_plan_only'}",
        f"runtime: {runtime_result.get('status', 'plan_only') if isinstance(runtime_result, dict) else 'plan_only'}",
        "image_generation: not run",
    ]
    return "\n".join(lines) + "\n"


def _index_by_key(items: list[Any], key: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        value = item.get(key)
        if isinstance(value, str):
            indexed[value] = item
    return indexed


def format_run_watch(payload: dict[str, Any]) -> str:
    metadata = payload.get("graphics_contract_runtime", {})
    if not isinstance(metadata, dict):
        metadata = {}
    plan = payload.get("plan", {})
    schedule = payload.get("schedule", {})
    execution = payload.get("execution", {})
    runtime_result = payload.get("runtime_result", {})
    nodes = plan.get("nodes", []) if isinstance(plan, dict) else []
    assignments = schedule.get("assignments", []) if isinstance(schedule, dict) else []
    node_results = execution.get("node_results", []) if isinstance(execution, dict) else []
    assignments_by_node = _index_by_key(assignments if isinstance(assignments, list) else [], "node_id")
    results_by_node = _index_by_key(node_results if isinstance(node_results, list) else [], "node_id")
    node_count = len(nodes) if isinstance(nodes, list) else 0

    lines = [
        "ConstraintOS Graphics Contract Runtime Watch",
        f"contract: {metadata.get('contract_key', 'unknown')}",
        f"subject: {metadata.get('subject', 'unknown')}",
        f"expected_decision: {metadata.get('expected_decision', 'unknown')}",
        f"mode: {metadata.get('mode', 'unknown')}",
        "image_generation: not run",
        "",
    ]

    if isinstance(nodes, list):
        for index, node in enumerate(nodes, start=1):
            if not isinstance(node, dict):
                continue
            node_id = str(node.get("id", "unknown"))
            assignment = assignments_by_node.get(node_id, {})
            result = results_by_node.get(node_id, {})
            worker_id = assignment.get("worker_id") or result.get("worker_id") or "unassigned"
            result_status = result.get("status", "not_run_plan_only")
            lines.extend(
                [
                    f"[{index}/{node_count}] {node.get('action', 'unknown')}",
                    f"  node: {node_id}",
                    f"  plugin: {node.get('plugin', 'unknown')}",
                    f"  worker: {worker_id}",
                    "  schedule: assigned" if assignment else "  schedule: unassigned",
                    f"  result: {result_status}",
                    "",
                ]
            )

    schedule_result = schedule.get("schedule_result", {}) if isinstance(schedule, dict) else {}
    execution_result = execution.get("execution_result", {}) if isinstance(execution, dict) else {}
    lines.extend(
        [
            "Final result:",
            f"  runtime: {runtime_result.get('status', 'plan_only') if isinstance(runtime_result, dict) else 'plan_only'}",
            f"  schedule: {schedule_result.get('status', 'unknown') if isinstance(schedule_result, dict) else 'unknown'}",
            f"  execution: {execution_result.get('status', 'not_run_plan_only') if isinstance(execution_result, dict) else 'not_run_plan_only'}",
            f"  approval expectation: {metadata.get('expected_decision', 'unknown')}",
            "  image generation: not run",
            "",
        ]
    )
    return "\n".join(lines)


def format_payload(payload: dict[str, Any], output_format: str, command: str, watch: bool = False) -> str:
    if watch:
        return format_run_watch(payload)
    if output_format == "json":
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if command == "list":
        return format_list_text(payload)
    if command == "run":
        return format_run_text(payload)
    return format_show_text(payload)


def write_output(output: str, output_path: str | None, watch: bool = False, watch_delay_ms: int = 0) -> None:
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
        print(f"Wrote graphics contract report: {target}")
        return
    if watch and watch_delay_ms > 0:
        for line in output.splitlines():
            print(line, flush=True)
            time.sleep(watch_delay_ms / 1000)
        return
    print(output, end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cos-graphics-contracts")
    parser.add_argument("--project-root", help="Repository root for resolving default graphics contracts.")
    parser.add_argument("--contracts-dir", help="Directory containing graphics validation contract fixtures.")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    parser.add_argument("--output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available graphics validation contracts.")

    show_parser = subparsers.add_parser("show", help="Show a graphics validation contract summary.")
    show_parser.add_argument("contract", help="Contract key, filename, or path.")

    run_parser = subparsers.add_parser("run", help="Run a contract-backed dry-run runtime bridge.")
    run_parser.add_argument("contract", help="Contract key, filename, or path.")
    run_parser.add_argument("--plan-only", action="store_true")
    run_parser.add_argument("--watch", action="store_true", help="Print a step-by-step contract runtime trace suitable for recording.")
    run_parser.add_argument("--watch-delay-ms", type=int, default=0, help="Delay between watch-output lines, useful for screen recording.")
    run_parser.add_argument("--workspace", default=".")
    run_parser.add_argument("--artifact-root", default=".constraintos/runtime/artifacts/graphics/contracts")
    run_parser.add_argument("--runtime-id")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        exit_code, payload = build_payload(args)
        watch = bool(getattr(args, "watch", False))
        watch_delay_ms = int(getattr(args, "watch_delay_ms", 0) or 0)
        write_output(format_payload(payload, args.format, args.command, watch=watch), args.output, watch=watch, watch_delay_ms=watch_delay_ms)
        return exit_code
    except SystemExit:
        raise
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
