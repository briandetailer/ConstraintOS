from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from constraintos.candidate_evaluation import build_fixture_only_candidate_evaluation
from constraintos.candidate_manifests import (
    CandidateManifestError,
    discover_project_root,
    list_candidate_manifest_summaries,
    load_candidate_manifest_report,
    resolve_candidate_manifests_dir,
)


def build_payload(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    project_root = Path(args.project_root).resolve() if args.project_root else discover_project_root()
    candidate_dir = resolve_candidate_manifests_dir(project_root, args.candidate_dir)
    if args.command == "list":
        manifests = list_candidate_manifest_summaries(candidate_dir)
        return 0, {
            "candidate_manifests": {
                "count": len(manifests),
                "candidate_dir": str(candidate_dir),
                "read_only": True,
                "image_generation": "not_run",
                "candidate_evaluation": "not_run",
            },
            "manifests": manifests,
        }
    if args.command == "show":
        report = load_candidate_manifest_report(args.manifest, candidate_dir)
        report["candidate_manifests"] = {
            "candidate_dir": str(candidate_dir),
            "selected": report["summary"]["key"],
            "read_only": True,
            "image_generation": "not_run",
            "candidate_evaluation": "not_run",
        }
        return 0, report
    if args.command == "evaluate":
        payload = build_fixture_only_candidate_evaluation(args.manifest, candidate_dir)
        return 0, payload
    raise CandidateManifestError(f"Unsupported command: {args.command}")


def format_list_text(payload: dict[str, Any]) -> str:
    header = payload.get("candidate_manifests", {})
    manifests = payload.get("manifests", [])
    lines = [f"Candidate manifests: {header.get('count', 0)}"]
    if isinstance(manifests, list):
        for item in manifests:
            if not isinstance(item, dict):
                continue
            lines.append(
                "- "
                + f"{item.get('key', 'unknown')} | "
                + f"contract={item.get('contract_key', 'unknown')} | "
                + f"status={item.get('status', 'unknown')} | "
                + f"evaluation={item.get('evaluation_status', 'unknown')} | "
                + f"initial_decision={item.get('initial_decision', 'unknown')}"
            )
    lines.extend([
        "image_generation: not run",
        "candidate_evaluation: not run",
    ])
    return "\n".join(lines) + "\n"


def format_show_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        f"Candidate manifest: {summary.get('key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"status: {summary.get('status', 'unknown')}",
        f"reference_type: {summary.get('reference_type', 'unknown')}",
        f"reference_status: {summary.get('reference_status', 'unknown')}",
        f"candidate_source_type: {summary.get('candidate_source_type', 'unknown')}",
        f"generated_by_constraintos: {summary.get('generated_by_constraintos', 'unknown')}",
        f"evaluation_status: {summary.get('evaluation_status', 'unknown')}",
        f"initial_decision: {summary.get('initial_decision', 'unknown')}",
        f"uncertainty_default: {summary.get('uncertainty_default', 'unknown')}",
        "image_generation: not run",
        "candidate_evaluation: not run",
    ]
    return "\n".join(lines) + "\n"


def format_evaluate_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        f"Candidate evaluation: {summary.get('candidate_manifest_key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"report_key: {summary.get('report_key', 'unknown')}",
        f"report_mode: {summary.get('report_mode', 'unknown')}",
        f"candidate_reference_status: {summary.get('candidate_reference_status', 'unknown')}",
        f"overall_evidence_status: {summary.get('overall_evidence_status', 'unknown')}",
        f"not_observed_count: {summary.get('not_observed_count', 'unknown')}",
        f"recommended_decision: {summary.get('recommended_decision', 'unknown')}",
        f"uncertainty_default: {summary.get('uncertainty_default', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "image_generation: not run",
        "real_image_ingestion: not run",
        "computer_vision: not run",
        "approval_automation: not run",
    ]
    return "\n".join(lines) + "\n"


def format_payload(payload: dict[str, Any], output_format: str, command: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if command == "list":
        return format_list_text(payload)
    if command == "evaluate":
        return format_evaluate_text(payload)
    return format_show_text(payload)


def write_output(output: str, output_path: str | None) -> None:
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
        print(f"Wrote candidate manifest report: {target}")
        return
    print(output, end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cos-graphics-candidates")
    parser.add_argument("--project-root", help="Repository root for resolving default candidate manifests.")
    parser.add_argument("--candidate-dir", help="Directory containing candidate manifest fixtures.")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    parser.add_argument("--output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List static graphics candidate manifest fixtures.")

    show_parser = subparsers.add_parser("show", help="Show a static candidate manifest summary.")
    show_parser.add_argument("manifest", help="Manifest key, contract key, candidate id, filename, or path.")

    evaluate_parser = subparsers.add_parser("evaluate", help="Run fixture-only candidate evaluation from static report fixtures.")
    evaluate_parser.add_argument("manifest", help="Manifest key, contract key, candidate id, filename, or path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        exit_code, payload = build_payload(args)
        write_output(format_payload(payload, args.format, args.command), args.output)
        return exit_code
    except SystemExit:
        raise
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
