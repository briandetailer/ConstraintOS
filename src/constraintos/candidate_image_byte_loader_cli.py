from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from constraintos.candidate_image_byte_loader import InMemoryArtifactRegistry, load_candidate_image_bytes_minimal
from constraintos.candidate_image_byte_loading_records import load_candidate_image_byte_loading_record_report
from constraintos.candidate_manifests import CandidateManifestError, discover_project_root, resolve_candidate_manifests_dir


def parse_fixture_hex(value: str) -> bytes:
    normalized = "".join(value.split()).lower()
    if not normalized:
        raise CandidateManifestError("--fixture-artifact-hex must not be empty")
    try:
        return bytes.fromhex(normalized)
    except ValueError as error:
        raise CandidateManifestError("--fixture-artifact-hex must be valid hexadecimal bytes") from error


def build_fixture_artifact_registry(fixture_artifact_uri: str | None, fixture_artifact_hex: str | None) -> InMemoryArtifactRegistry:
    if fixture_artifact_uri is None and fixture_artifact_hex is None:
        return InMemoryArtifactRegistry({})
    if not fixture_artifact_uri or fixture_artifact_hex is None:
        raise CandidateManifestError("--fixture-artifact-uri and --fixture-artifact-hex must be provided together")
    if not fixture_artifact_uri.startswith("artifact://"):
        raise CandidateManifestError("--fixture-artifact-uri must use artifact://")
    return InMemoryArtifactRegistry({fixture_artifact_uri: parse_fixture_hex(fixture_artifact_hex)})


def build_minimal_byte_loading_cli_payload(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    project_root = Path(args.project_root).resolve() if args.project_root else discover_project_root()
    candidate_dir = resolve_candidate_manifests_dir(project_root, args.candidate_dir)
    report = load_candidate_image_byte_loading_record_report(args.record, candidate_dir)
    registry = build_fixture_artifact_registry(args.fixture_artifact_uri, args.fixture_artifact_hex)
    result = dict(load_candidate_image_bytes_minimal(report["candidate_image_byte_loading_record"], registry))
    summary = report.get("summary", {}) if isinstance(report.get("summary", {}), dict) else {}
    return 0, {
        "candidate_image_byte_loading_minimal_cli": {
            "mode": "helper_only",
            "candidate_dir": str(candidate_dir),
            "selected": summary.get("key"),
            "fixture_artifact_uri_provided": args.fixture_artifact_uri is not None,
            "fixture_artifact_hex_provided": args.fixture_artifact_hex is not None,
            "local_image_file_opening": "not_run",
            "artifact_download": "not_run",
            "network_fetch": "not_run",
            "image_decoding": "not_run",
            "candidate_scoring": "not_run",
            "source_report_mutation": "not_run",
            "approval_automation": "not_run",
        },
        "summary": {
            "record_key": summary.get("key"),
            "candidate_id": result.get("candidate_id"),
            "contract_key": result.get("contract_key"),
            "reference_type": result.get("reference_type"),
            "reference": result.get("reference"),
            "status": result.get("status"),
            "failure_code": result.get("failure_code"),
            "image_bytes_loaded": result.get("image_bytes_loaded"),
            "local_file_opened": result.get("local_file_opened"),
            "artifact_downloaded": result.get("artifact_downloaded"),
            "network_fetch_ran": result.get("network_fetch_ran"),
            "actual_loaded_byte_count": result.get("actual_loaded_byte_count"),
            "computed_sha256": result.get("computed_sha256"),
            "sniffed_media_type": result.get("sniffed_media_type"),
            "checksum_matches": result.get("checksum_matches"),
            "media_type_matches": result.get("media_type_matches"),
            "image_decoded": result.get("image_decoded"),
            "candidate_scoring_ran": result.get("candidate_scoring_ran"),
            "source_report_mutation_ran": result.get("source_report_mutation_ran"),
            "approval_automation_ran": result.get("approval_automation_ran"),
            "initial_decision": result.get("initial_decision"),
            "approval_allowed": result.get("approval_allowed"),
        },
        "byte_loading_result": result,
    }


def build_minimal_byte_loading_cli_review_packet_payload(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    exit_code, payload = build_minimal_byte_loading_cli_payload(args)
    summary = payload.get("summary", {}) if isinstance(payload.get("summary", {}), dict) else {}
    cli = payload.get("candidate_image_byte_loading_minimal_cli", {}) if isinstance(payload.get("candidate_image_byte_loading_minimal_cli", {}), dict) else {}
    result = payload.get("byte_loading_result", {}) if isinstance(payload.get("byte_loading_result", {}), dict) else {}
    review_packet = {
        "candidate_image_byte_loading_minimal_cli_review_packet": {
            "mode": "helper_only_review_packet",
            "review_packet_ready": True,
            "selected": summary.get("record_key"),
            "local_image_file_opening": "not_run",
            "artifact_download": "not_run",
            "network_fetch": "not_run",
            "image_decoding": "not_run",
            "candidate_scoring": "not_run",
            "source_report_mutation": "not_run",
            "approval_automation": "not_run",
        },
        "summary": {
            "record_key": summary.get("record_key"),
            "candidate_id": summary.get("candidate_id"),
            "contract_key": summary.get("contract_key"),
            "reference_type": summary.get("reference_type"),
            "status": summary.get("status"),
            "failure_code": summary.get("failure_code"),
            "image_bytes_loaded": summary.get("image_bytes_loaded"),
            "image_decoded": summary.get("image_decoded"),
            "candidate_scoring_ran": summary.get("candidate_scoring_ran"),
            "source_report_mutation_ran": summary.get("source_report_mutation_ran"),
            "approval_automation_ran": summary.get("approval_automation_ran"),
            "initial_decision": summary.get("initial_decision"),
            "approval_allowed": summary.get("approval_allowed"),
        },
        "review_sections": {
            "cli_invocation_boundary": {
                "command": "cos-graphics-byte-loader review-packet",
                "byte_source": "explicit fixture hex argument",
                "artifact_binding": "explicit --fixture-artifact-uri",
                "fixture_artifact_uri_provided": cli.get("fixture_artifact_uri_provided"),
                "fixture_artifact_hex_provided": cli.get("fixture_artifact_hex_provided"),
                "local_image_file_opening": "not_run",
                "artifact_download": "not_run",
                "network_fetch": "not_run",
            },
            "byte_loading_result": {
                "status": result.get("status"),
                "failure_code": result.get("failure_code"),
                "actual_loaded_byte_count": result.get("actual_loaded_byte_count"),
                "computed_sha256": result.get("computed_sha256"),
                "sniffed_media_type": result.get("sniffed_media_type"),
                "checksum_matches": result.get("checksum_matches"),
                "media_type_matches": result.get("media_type_matches"),
            },
            "safety_boundaries": {
                "local_file_opened": result.get("local_file_opened"),
                "artifact_downloaded": result.get("artifact_downloaded"),
                "network_fetch_ran": result.get("network_fetch_ran"),
                "image_decoded": result.get("image_decoded"),
                "pixel_inspection_ran": result.get("pixel_inspection_ran"),
                "computer_vision_ran": result.get("computer_vision_ran"),
                "ocr_ran": result.get("ocr_ran"),
                "candidate_scoring_ran": result.get("candidate_scoring_ran"),
                "source_report_mutation_ran": result.get("source_report_mutation_ran"),
                "approval_automation_ran": result.get("approval_automation_ran"),
            },
            "decision_guardrails": {
                "approval_allowed": result.get("approval_allowed"),
                "initial_decision": result.get("initial_decision"),
                "approval_blockers": [
                    "Byte loading alone cannot approve a candidate.",
                    "Image decoding has not run.",
                    "Candidate scoring has not run.",
                    "Source report mutation has not run.",
                    "Approval automation has not run.",
                ],
            },
        },
        "candidate_image_byte_loading_minimal_cli_payload": payload,
    }
    return exit_code, review_packet


def format_minimal_byte_loading_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        f"Candidate image byte-loading minimal CLI: {summary.get('record_key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"reference_type: {summary.get('reference_type', 'unknown')}",
        f"reference: {summary.get('reference', 'unknown')}",
        f"status: {summary.get('status', 'unknown')}",
        f"failure_code: {summary.get('failure_code', 'unknown')}",
        f"image_bytes_loaded: {summary.get('image_bytes_loaded', 'unknown')}",
        f"local_file_opened: {summary.get('local_file_opened', 'unknown')}",
        f"artifact_downloaded: {summary.get('artifact_downloaded', 'unknown')}",
        f"network_fetch_ran: {summary.get('network_fetch_ran', 'unknown')}",
        f"actual_loaded_byte_count: {summary.get('actual_loaded_byte_count', 'unknown')}",
        f"computed_sha256: {summary.get('computed_sha256', 'unknown')}",
        f"sniffed_media_type: {summary.get('sniffed_media_type', 'unknown')}",
        f"checksum_matches: {summary.get('checksum_matches', 'unknown')}",
        f"media_type_matches: {summary.get('media_type_matches', 'unknown')}",
        f"image_decoded: {summary.get('image_decoded', 'unknown')}",
        f"candidate_scoring_ran: {summary.get('candidate_scoring_ran', 'unknown')}",
        f"source_report_mutation_ran: {summary.get('source_report_mutation_ran', 'unknown')}",
        f"approval_automation_ran: {summary.get('approval_automation_ran', 'unknown')}",
        f"initial_decision: {summary.get('initial_decision', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "local_image_file_opening: not run",
        "artifact_download: not run",
        "network_fetch: not run",
        "image_decoding: not run",
        "candidate_scoring: not run",
        "source_report_mutation: not run",
        "approval_automation: not run",
    ]
    return "\n".join(lines) + "\n"


def format_minimal_byte_loading_review_packet_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    sections = payload.get("review_sections", {})
    if not isinstance(summary, dict):
        summary = {}
    if not isinstance(sections, dict):
        sections = {}
    guardrails = sections.get("decision_guardrails", {}) if isinstance(sections.get("decision_guardrails", {}), dict) else {}
    blockers = guardrails.get("approval_blockers", [])
    lines = [
        f"Candidate image byte-loading minimal CLI review packet: {summary.get('record_key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"reference_type: {summary.get('reference_type', 'unknown')}",
        f"status: {summary.get('status', 'unknown')}",
        f"failure_code: {summary.get('failure_code', 'unknown')}",
        f"image_bytes_loaded: {summary.get('image_bytes_loaded', 'unknown')}",
        f"image_decoded: {summary.get('image_decoded', 'unknown')}",
        f"candidate_scoring_ran: {summary.get('candidate_scoring_ran', 'unknown')}",
        f"source_report_mutation_ran: {summary.get('source_report_mutation_ran', 'unknown')}",
        f"approval_automation_ran: {summary.get('approval_automation_ran', 'unknown')}",
        f"initial_decision: {summary.get('initial_decision', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "approval_blockers:",
    ]
    if isinstance(blockers, list):
        lines.extend(f"- {blocker}" for blocker in blockers)
    lines.extend([
        "local_image_file_opening: not run",
        "artifact_download: not run",
        "network_fetch: not run",
        "image_decoding: not run",
        "candidate_scoring: not run",
        "source_report_mutation: not run",
        "approval_automation: not run",
    ])
    return "\n".join(lines) + "\n"


def format_payload(payload: dict[str, Any], output_format: str, command: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if command == "review-packet":
        return format_minimal_byte_loading_review_packet_text(payload)
    return format_minimal_byte_loading_text(payload)


def write_output(output: str, output_path: str | None, label: str = "report") -> None:
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
        print(f"Wrote candidate image byte-loading {label}: {target}")
        return
    print(output, end="")


def add_fixture_artifact_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("record", help="Record key, contract key, candidate id, record id, intake manifest id, filename, or path.")
    parser.add_argument("--fixture-artifact-uri", help="Explicit artifact:// URI to bind to the provided fixture bytes.")
    parser.add_argument("--fixture-artifact-hex", help="Hex-encoded fixture bytes for the explicit artifact URI.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cos-graphics-byte-loader")
    parser.add_argument("--project-root", help="Repository root for resolving default candidate fixtures.")
    parser.add_argument("--candidate-dir", help="Directory containing candidate byte-loading record fixtures.")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    parser.add_argument("--output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    minimal_parser = subparsers.add_parser("minimal", help="Run helper-only minimal byte loading from explicit fixture bytes.")
    add_fixture_artifact_arguments(minimal_parser)

    review_packet_parser = subparsers.add_parser("review-packet", help="Build a helper-only review packet for minimal byte loading.")
    add_fixture_artifact_arguments(review_packet_parser)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        if args.command == "minimal":
            exit_code, payload = build_minimal_byte_loading_cli_payload(args)
            write_output(format_payload(payload, args.format, args.command), args.output)
            return exit_code
        if args.command == "review-packet":
            exit_code, payload = build_minimal_byte_loading_cli_review_packet_payload(args)
            write_output(format_payload(payload, args.format, args.command), args.output, label="review packet")
            return exit_code
        raise CandidateManifestError(f"Unsupported command: {args.command}")
    except SystemExit:
        raise
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
