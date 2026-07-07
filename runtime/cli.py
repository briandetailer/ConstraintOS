from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, TextIO

from runtime.artifacts import ArtifactStore, RuntimeEvidenceBundleWriter, verify_runtime_evidence_manifest
from runtime.engine import RuntimeEngine
from runtime.scheduler import WorkerCapability


EVIDENCE_CLI_SUCCESS = 0
EVIDENCE_CLI_VERIFICATION_FAILED = 1
EVIDENCE_CLI_RUNTIME_UNSUCCESSFUL = 2
EVIDENCE_CLI_USAGE_ERROR = 3


def run_evidence_cli(
    argv: list[str] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Generate and verify a Runtime evidence package from CLI-style arguments."""
    output = stdout or sys.stdout
    errors = stderr or sys.stderr
    parser = _evidence_parser()
    try:
        args = parser.parse_args(argv)
        specification = _read_json(Path(args.spec))
        workers = _read_workers(Path(args.workers))
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else EVIDENCE_CLI_USAGE_ERROR
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Runtime evidence CLI error: {exc}", file=errors)
        return EVIDENCE_CLI_USAGE_ERROR

    result = RuntimeEngine().run(specification, workers)
    writer = RuntimeEvidenceBundleWriter(ArtifactStore(Path(args.output_dir)))
    manifest_artifact = writer.write_evidence(result)
    verification = verify_runtime_evidence_manifest(manifest_artifact)
    summary = _summary(result.to_dict(), manifest_artifact.to_dict(), verification.to_dict())
    _write_summary(summary, args.format, output)

    if not verification.successful():
        return EVIDENCE_CLI_VERIFICATION_FAILED
    if not result.successful():
        return EVIDENCE_CLI_RUNTIME_UNSUCCESSFUL
    return EVIDENCE_CLI_SUCCESS


def main(argv: list[str] | None = None) -> None:
    raise SystemExit(run_evidence_cli(argv))


def _evidence_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a Runtime evidence package.")
    parser.add_argument("--spec", required=True, help="Path to a Runtime specification JSON file.")
    parser.add_argument("--workers", required=True, help="Path to a worker capability JSON file.")
    parser.add_argument("--output-dir", required=True, help="Directory where evidence artifacts should be written.")
    parser.add_argument("--format", choices=("json", "text"), default="json", help="Summary output format.")
    return parser


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return value


def _read_workers(path: Path) -> list[WorkerCapability]:
    value = json.loads(path.read_text(encoding="utf-8"))
    records = value.get("workers", []) if isinstance(value, dict) else value
    if not isinstance(records, list):
        raise ValueError(f"{path} must contain a worker list or an object with a workers list.")
    workers: list[WorkerCapability] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Worker {index} must be a JSON object.")
        worker_id = record.get("worker_id") or record.get("id")
        plugins = record.get("plugins")
        if not isinstance(worker_id, str) or not worker_id:
            raise ValueError(f"Worker {index} requires worker_id.")
        if not isinstance(plugins, list) or not all(isinstance(plugin, str) for plugin in plugins):
            raise ValueError(f"Worker {index} requires plugins as a list of strings.")
        status = record.get("status", "available")
        if not isinstance(status, str):
            raise ValueError(f"Worker {index} status must be a string.")
        workers.append(WorkerCapability(worker_id, plugins, status))
    return workers


def _summary(
    runtime_result: dict[str, Any],
    manifest_artifact: dict[str, Any],
    verification: dict[str, Any],
) -> dict[str, Any]:
    result_header = runtime_result.get("runtime_result", {})
    metadata = manifest_artifact.get("metadata", {})
    verification_header = verification.get("runtime_evidence_verification", {})
    issues = verification.get("issues", [])
    return {
        "runtime_evidence_cli": {
            "successful": bool(result_header.get("successful")) and bool(verification_header.get("successful")),
            "runtime_id": result_header.get("id"),
            "runtime_status": result_header.get("status"),
            "evidence_manifest_uri": manifest_artifact.get("uri"),
            "evidence_manifest_path": metadata.get("path"),
            "contract_registry_version": metadata.get("contract_registry_version"),
            "issue_count": verification_header.get("issue_count", 0),
        },
        "issues": issues if isinstance(issues, list) else [],
    }


def _write_summary(summary: dict[str, Any], format_name: str, output: TextIO) -> None:
    if format_name == "json":
        print(json.dumps(summary, indent=2, sort_keys=True), file=output)
        return
    header = summary.get("runtime_evidence_cli", {})
    print(f"Runtime evidence successful: {header.get('successful')}", file=output)
    print(f"Runtime id: {header.get('runtime_id')}", file=output)
    print(f"Runtime status: {header.get('runtime_status')}", file=output)
    print(f"Evidence manifest: {header.get('evidence_manifest_uri')}", file=output)
    print(f"Issue count: {header.get('issue_count')}", file=output)


if __name__ == "__main__":
    main()
