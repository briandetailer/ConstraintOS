from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, TextIO

from runtime.approval_gate import create_runtime_approval_decision
from runtime.artifacts import ArtifactStore, RuntimeApprovalReportWriter


APPROVAL_CLI_SUCCESS = 0
APPROVAL_CLI_REJECTED = 1
APPROVAL_CLI_USAGE_ERROR = 3


def run_approval_cli(
    argv: list[str] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Create and persist a Runtime approval decision from CLI-style arguments."""
    output = stdout or sys.stdout
    errors = stderr or sys.stderr
    parser = _approval_parser()
    try:
        args = parser.parse_args(argv)
        evidence_manifest_path = Path(args.evidence_manifest)
        policy = _read_json(Path(args.policy))
        evidence_artifact = _evidence_manifest_artifact(evidence_manifest_path, args.evidence_artifact_id)
        decision = create_runtime_approval_decision(
            evidence_artifact,
            policy,
            decided_by=args.decided_by,
            decided_at=args.decided_at,
        )
        report_artifact = RuntimeApprovalReportWriter(ArtifactStore(Path(args.output_dir))).write_approval(decision)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else APPROVAL_CLI_USAGE_ERROR
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Runtime approval CLI error: {exc}", file=errors)
        return APPROVAL_CLI_USAGE_ERROR

    summary = _summary(decision, report_artifact.to_dict())
    _write_summary(summary, args.format, output)
    if decision.get("runtime_approval", {}).get("decision") != "approved":
        return APPROVAL_CLI_REJECTED
    return APPROVAL_CLI_SUCCESS


def main(argv: list[str] | None = None) -> None:
    raise SystemExit(run_approval_cli(argv))


def _approval_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a Runtime approval report from evidence and policy.")
    parser.add_argument("--evidence-manifest", required=True, help="Path to a Runtime evidence manifest JSON file.")
    parser.add_argument("--evidence-artifact-id", required=True, help="Artifact id of the Runtime evidence manifest.")
    parser.add_argument("--policy", required=True, help="Path to a Runtime approval policy JSON file.")
    parser.add_argument("--decided-by", required=True, help="Approval decision authority.")
    parser.add_argument("--decided-at", required=True, help="Approval decision timestamp.")
    parser.add_argument("--output-dir", required=True, help="Directory where approval artifacts should be written.")
    parser.add_argument("--format", choices=("json", "text"), default="json", help="Summary output format.")
    return parser


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return value


def _evidence_manifest_artifact(path: Path, artifact_id: str) -> dict[str, Any]:
    if not artifact_id:
        raise ValueError("Runtime approval CLI requires evidence_artifact_id.")
    resolved_path = path.resolve()
    return {
        "id": artifact_id,
        "uri": resolved_path.as_uri(),
        "kind": "file",
        "producer": "runtime-approval-cli",
        "metadata": {
            "path": str(resolved_path),
            "artifact_role": "runtime_evidence_manifest",
            "content_type": "application/json",
        },
    }


def _summary(decision: dict[str, Any], report_artifact: dict[str, Any]) -> dict[str, Any]:
    approval = decision.get("runtime_approval", {})
    checks = decision.get("checks", [])
    notes = decision.get("notes", [])
    metadata = report_artifact.get("metadata", {})
    return {
        "runtime_approval_cli": {
            "successful": approval.get("decision") == "approved",
            "runtime_id": approval.get("runtime_id"),
            "decision": approval.get("decision"),
            "approval_policy": approval.get("approval_policy"),
            "evidence_manifest_artifact_id": approval.get("evidence_manifest_artifact_id"),
            "approval_report_uri": report_artifact.get("uri"),
            "approval_report_path": metadata.get("path"),
            "issue_count": len(notes) if isinstance(notes, list) else 0,
        },
        "checks": checks if isinstance(checks, list) else [],
        "issues": notes if isinstance(notes, list) else [],
    }


def _write_summary(summary: dict[str, Any], format_name: str, output: TextIO) -> None:
    if format_name == "json":
        print(json.dumps(summary, indent=2, sort_keys=True), file=output)
        return
    header = summary.get("runtime_approval_cli", {})
    print(f"Runtime approval successful: {header.get('successful')}", file=output)
    print(f"Runtime id: {header.get('runtime_id')}", file=output)
    print(f"Decision: {header.get('decision')}", file=output)
    print(f"Approval policy: {header.get('approval_policy')}", file=output)
    print(f"Approval report: {header.get('approval_report_uri')}", file=output)
    print(f"Issue count: {header.get('issue_count')}", file=output)


if __name__ == "__main__":
    main()
