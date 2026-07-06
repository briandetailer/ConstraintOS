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

from constraintos.constraint_pack import apply_constraint_pack
from constraintos.validation.pipeline import ValidationApprovalPipeline


def load_data_file(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if yaml is None:
        raise RuntimeError("PyYAML is required")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_evidence(path: str | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    data = load_data_file(Path(path))
    raw_evidence = data.get("evidence") if isinstance(data, dict) else data
    if not isinstance(raw_evidence, list):
        raise ValueError(f"{path} must contain an evidence list")
    for index, entry in enumerate(raw_evidence, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"{path} evidence {index} must be an object")
    return raw_evidence


def apply_constraint_pack_files(render_specification: dict[str, Any], constraint_pack_paths: list[str] | None) -> dict[str, Any]:
    applied = render_specification
    for constraint_pack_path in constraint_pack_paths or []:
        constraint_pack = load_data_file(Path(constraint_pack_path))
        if not isinstance(constraint_pack, dict):
            raise ValueError(f"{constraint_pack_path} must contain an object")
        applied = apply_constraint_pack(applied, constraint_pack)
    return applied


def summarize_payload(payload: dict[str, Any]) -> str:
    validation = payload.get("validation", {}).get("validation_report", {})
    approval = payload.get("approval", {}).get("approval", {})
    results = payload.get("validation", {}).get("results", [])
    failure_report = payload.get("failure_report", {}).get("failure_report", {})
    remediation_plan = payload.get("remediation_plan", {}).get("remediation_plan", {})
    revision_request = payload.get("revision_request", {}).get("revision_request", {})
    decision = payload.get("approval", {}).get("decision", {})
    return "\n".join(
        [
            f"Validation {validation.get('id', 'unknown')}: {validation.get('status', 'unknown')} | results={len(results)}",
            f"Failure report {failure_report.get('id', 'unknown')}: {failure_report.get('status', 'unknown')} | failures={failure_report.get('failure_count', 0)}",
            f"Remediation plan {remediation_plan.get('id', 'unknown')}: {remediation_plan.get('status', 'unknown')} | actions={remediation_plan.get('action_count', 0)}",
            f"Revision request {revision_request.get('id', 'unknown')}: {revision_request.get('status', 'unknown')} | steps={revision_request.get('step_count', 0)}",
            f"Approval {approval.get('id', 'unknown')}: {approval.get('status', 'unknown')}",
            f"Decision: {decision.get('summary', '')}",
        ]
    ) + "\n"


def format_payload(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "text":
        return summarize_payload(payload)
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def write_output(payload: dict[str, Any], output_path: str | None, output_format: str) -> None:
    output = format_payload(payload, output_format)
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
        print(f"Wrote validation approval result: {target}")
    else:
        print(output, end="")


def run_validation(args: argparse.Namespace) -> int:
    render_specification = load_data_file(Path(args.render_specification))
    if not isinstance(render_specification, dict):
        raise ValueError(f"{args.render_specification} must contain an object")
    render_specification = apply_constraint_pack_files(render_specification, args.constraint_pack)
    evidence = load_evidence(args.evidence)
    result = ValidationApprovalPipeline().evaluate_render_specification(
        render_specification,
        evidence=evidence,
        artifact_id=args.artifact_id,
        validation_report_id=args.validation_report_id,
        failure_report_id=args.failure_report_id,
        remediation_plan_id=args.remediation_plan_id,
        revision_request_id=args.revision_request_id,
        approval_decision_id=args.approval_id,
    )
    payload = result.to_dict()
    write_output(payload, args.output, args.format)
    return 0 if result.approved() else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cos-validate")
    parser.add_argument("render_specification")
    parser.add_argument("--evidence")
    parser.add_argument("--constraint-pack", action="append")
    parser.add_argument("--artifact-id", default="UNKNOWN-ARTIFACT")
    parser.add_argument("--validation-report-id", default="VALIDATION-REPORT-0001")
    parser.add_argument("--failure-report-id", default="FAILURE-REPORT-0001")
    parser.add_argument("--remediation-plan-id", default="REMEDIATION-PLAN-0001")
    parser.add_argument("--revision-request-id", default="REVISION-REQUEST-0001")
    parser.add_argument("--approval-id", default="APPROVAL-0001")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        return run_validation(args)
    except SystemExit:
        raise
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
