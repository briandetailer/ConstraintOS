from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from constraintos.graphics_contracts import (
    GraphicsContractError,
    discover_project_root,
    list_contract_summaries,
    load_contract_report,
    resolve_contracts_dir,
)


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root).resolve() if args.project_root else discover_project_root()
    contracts_dir = resolve_contracts_dir(project_root, args.contracts_dir)
    if args.command == "list":
        contracts = list_contract_summaries(contracts_dir)
        return {
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
        return report
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


def format_payload(payload: dict[str, Any], output_format: str, command: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if command == "list":
        return format_list_text(payload)
    return format_show_text(payload)


def write_output(output: str, output_path: str | None) -> None:
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
        print(f"Wrote graphics contract report: {target}")
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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        payload = build_payload(args)
        write_output(format_payload(payload, args.format, args.command), args.output)
        return 0
    except SystemExit:
        raise
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
