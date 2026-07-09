from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from constraintos.candidate_evaluation import build_fixture_only_candidate_evaluation
from constraintos.candidate_image_byte_loading_records import (
    list_candidate_image_byte_loading_record_summaries,
    load_candidate_image_byte_loading_record_report,
)
from constraintos.candidate_intake_manifests import (
    list_candidate_intake_manifest_summaries,
    load_candidate_intake_manifest_report,
)
from constraintos.candidate_intake_review_packet import build_candidate_intake_review_packet_payload
from constraintos.candidate_manifests import (
    CandidateManifestError,
    discover_project_root,
    list_candidate_manifest_summaries,
    load_candidate_manifest_report,
    resolve_candidate_manifests_dir,
)
from constraintos.candidate_review_packet import build_candidate_review_packet_payload
from constraintos.manual_observations import build_manual_observation_payload
from constraintos.observation_evidence_merge import build_observation_evidence_merge_payload
from constraintos.observation_report_binding import build_observation_report_binding_payload


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
    if args.command == "intake-list":
        manifests = list_candidate_intake_manifest_summaries(candidate_dir)
        return 0, {
            "candidate_intake_manifests": {
                "count": len(manifests),
                "candidate_dir": str(candidate_dir),
                "read_only": True,
                "image_bytes_loaded": "not_run",
                "image_decoding": "not_run",
                "network_fetch": "not_run",
                "candidate_scoring": "not_run",
                "approval_automation": "not_run",
            },
            "manifests": manifests,
        }
    if args.command == "intake-show":
        report = load_candidate_intake_manifest_report(args.manifest, candidate_dir)
        report["candidate_intake_manifests"] = {
            "candidate_dir": str(candidate_dir),
            "selected": report["summary"]["key"],
            "read_only": True,
            "image_bytes_loaded": "not_run",
            "image_decoding": "not_run",
            "network_fetch": "not_run",
            "candidate_scoring": "not_run",
            "approval_automation": "not_run",
        }
        return 0, report
    if args.command == "byte-loading-list":
        records = list_candidate_image_byte_loading_record_summaries(candidate_dir)
        return 0, {
            "candidate_image_byte_loading_records": {
                "count": len(records),
                "candidate_dir": str(candidate_dir),
                "read_only": True,
                "image_bytes_loaded": "not_run",
                "local_file_opening": "not_run",
                "artifact_download": "not_run",
                "network_fetch": "not_run",
                "image_decoding": "not_run",
                "candidate_scoring": "not_run",
                "approval_automation": "not_run",
            },
            "records": records,
        }
    if args.command == "byte-loading-show":
        report = load_candidate_image_byte_loading_record_report(args.manifest, candidate_dir)
        report["candidate_image_byte_loading_records"] = {
            "candidate_dir": str(candidate_dir),
            "selected": report["summary"]["key"],
            "read_only": True,
            "image_bytes_loaded": "not_run",
            "local_file_opening": "not_run",
            "artifact_download": "not_run",
            "network_fetch": "not_run",
            "image_decoding": "not_run",
            "candidate_scoring": "not_run",
            "approval_automation": "not_run",
        }
        return 0, report
    if args.command == "intake-review-packet":
        payload = build_candidate_intake_review_packet_payload(args.manifest, candidate_dir)
        return 0, payload
    if args.command == "evaluate":
        payload = build_fixture_only_candidate_evaluation(args.manifest, candidate_dir)
        return 0, payload
    if args.command == "observe":
        payload = build_manual_observation_payload(args.manifest, candidate_dir)
        return 0, payload
    if args.command == "bind-observations":
        payload = build_observation_report_binding_payload(args.manifest, candidate_dir)
        return 0, payload
    if args.command == "merge-evidence":
        payload = build_observation_evidence_merge_payload(args.manifest, candidate_dir)
        return 0, payload
    if args.command == "review-packet":
        payload = build_candidate_review_packet_payload(args.manifest, candidate_dir)
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


def format_intake_list_text(payload: dict[str, Any]) -> str:
    header = payload.get("candidate_intake_manifests", {})
    manifests = payload.get("manifests", [])
    lines = [f"Candidate intake manifests: {header.get('count', 0)}"]
    if isinstance(manifests, list):
        for item in manifests:
            if not isinstance(item, dict):
                continue
            lines.append(
                "- "
                + f"{item.get('key', 'unknown')} | "
                + f"contract={item.get('contract_key', 'unknown')} | "
                + f"intake_state={item.get('intake_state', 'unknown')} | "
                + f"reference_type={item.get('reference_type', 'unknown')} | "
                + f"media_type={item.get('media_type', 'unknown')} | "
                + f"approval_allowed={item.get('approval_allowed', 'unknown')}"
            )
    lines.extend([
        "image_bytes_loaded: not run",
        "image_decoding: not run",
        "network_fetch: not run",
        "candidate_scoring: not run",
        "approval_automation: not run",
    ])
    return "\n".join(lines) + "\n"


def format_byte_loading_list_text(payload: dict[str, Any]) -> str:
    header = payload.get("candidate_image_byte_loading_records", {})
    records = payload.get("records", [])
    lines = [f"Candidate image byte-loading records: {header.get('count', 0)}"]
    if isinstance(records, list):
        for item in records:
            if not isinstance(item, dict):
                continue
            lines.append(
                "- "
                + f"{item.get('key', 'unknown')} | "
                + f"contract={item.get('contract_key', 'unknown')} | "
                + f"byte_loading_state={item.get('byte_loading_state', 'unknown')} | "
                + f"reference_type={item.get('reference_type', 'unknown')} | "
                + f"media_type={item.get('media_type', 'unknown')} | "
                + f"image_bytes_loaded={item.get('image_bytes_loaded', 'unknown')} | "
                + f"approval_allowed={item.get('approval_allowed', 'unknown')}"
            )
    lines.extend([
        "image_bytes_loaded: not run",
        "local_file_opening: not run",
        "artifact_download: not run",
        "network_fetch: not run",
        "image_decoding: not run",
        "candidate_scoring: not run",
        "approval_automation: not run",
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


def format_intake_show_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        f"Candidate intake manifest: {summary.get('key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"status: {summary.get('status', 'unknown')}",
        f"intake_state: {summary.get('intake_state', 'unknown')}",
        f"reference_type: {summary.get('reference_type', 'unknown')}",
        f"reference_status: {summary.get('reference_status', 'unknown')}",
        f"media_type: {summary.get('media_type', 'unknown')}",
        f"image_sha256: {summary.get('image_sha256', 'unknown')}",
        f"network_fetch_allowed: {summary.get('network_fetch_allowed', 'unknown')}",
        f"successful_intake_can_approve: {summary.get('successful_intake_can_approve', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "image_bytes_loaded: not run",
        "image_decoding: not run",
        "network_fetch: not run",
        "candidate_scoring: not run",
        "source_report_mutation: not run",
        "approval_automation: not run",
    ]
    return "\n".join(lines) + "\n"


def format_byte_loading_show_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        f"Candidate image byte-loading record: {summary.get('key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"candidate_intake_manifest_id: {summary.get('candidate_intake_manifest_id', 'unknown')}",
        f"status: {summary.get('status', 'unknown')}",
        f"byte_loading_state: {summary.get('byte_loading_state', 'unknown')}",
        f"reference_type: {summary.get('reference_type', 'unknown')}",
        f"media_type: {summary.get('media_type', 'unknown')}",
        f"image_sha256: {summary.get('image_sha256', 'unknown')}",
        f"expected_byte_count: {summary.get('expected_byte_count', 'unknown')}",
        f"max_candidate_image_bytes: {summary.get('max_candidate_image_bytes', 'unknown')}",
        f"network_fetch_allowed: {summary.get('network_fetch_allowed', 'unknown')}",
        f"implicit_cloud_download_allowed: {summary.get('implicit_cloud_download_allowed', 'unknown')}",
        f"byte_loading_success_can_approve: {summary.get('byte_loading_success_can_approve', 'unknown')}",
        f"image_bytes_loaded: {summary.get('image_bytes_loaded', 'unknown')}",
        f"local_file_opened: {summary.get('local_file_opened', 'unknown')}",
        f"artifact_downloaded: {summary.get('artifact_downloaded', 'unknown')}",
        f"network_fetch_ran: {summary.get('network_fetch_ran', 'unknown')}",
        f"actual_loaded_byte_count: {summary.get('actual_loaded_byte_count', 'unknown')}",
        f"computed_sha256: {summary.get('computed_sha256', 'unknown')}",
        f"sniffed_media_type: {summary.get('sniffed_media_type', 'unknown')}",
        f"image_decoded: {summary.get('image_decoded', 'unknown')}",
        f"candidate_scoring_ran: {summary.get('candidate_scoring_ran', 'unknown')}",
        f"source_report_mutation_ran: {summary.get('source_report_mutation_ran', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "image_bytes_loaded: not run",
        "local_file_opening: not run",
        "artifact_download: not run",
        "network_fetch: not run",
        "image_decoding: not run",
        "pixel_inspection: not run",
        "computer_vision: not run",
        "ocr: not run",
        "candidate_scoring: not run",
        "source_report_mutation: not run",
        "approval_automation: not run",
    ]
    return "\n".join(lines) + "\n"


def format_intake_review_packet_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    sections = payload.get("review_sections", {})
    if not isinstance(summary, dict):
        summary = {}
    if not isinstance(sections, dict):
        sections = {}
    blockers = sections.get("decision_guardrails", {}).get("approval_blockers", []) if isinstance(sections.get("decision_guardrails", {}), dict) else []
    lines = [
        f"Candidate intake review packet: {summary.get('candidate_intake_manifest_key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"intake_state: {summary.get('intake_state', 'unknown')}",
        f"reference_type: {summary.get('reference_type', 'unknown')}",
        f"reference_status: {summary.get('reference_status', 'unknown')}",
        f"media_type: {summary.get('media_type', 'unknown')}",
        f"network_fetch_allowed: {summary.get('network_fetch_allowed', 'unknown')}",
        f"successful_intake_can_approve: {summary.get('successful_intake_can_approve', 'unknown')}",
        f"initial_decision: {summary.get('initial_decision', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "approval_blockers:",
    ]
    if isinstance(blockers, list):
        lines.extend(f"- {blocker}" for blocker in blockers)
    lines.extend([
        "image_bytes_loaded: not run",
        "image_decoding: not run",
        "network_fetch: not run",
        "pixel_inspection: not run",
        "computer_vision: not run",
        "ocr: not run",
        "candidate_scoring: not run",
        "source_report_mutation: not run",
        "approval_automation: not run",
    ])
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


def format_observe_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        f"Manual observation: {summary.get('candidate_manifest_key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"observation_key: {summary.get('observation_key', 'unknown')}",
        f"observation_mode: {summary.get('observation_mode', 'unknown')}",
        f"source_type: {summary.get('source_type', 'unknown')}",
        f"candidate_reference_status: {summary.get('candidate_reference_status', 'unknown')}",
        f"total_observations: {summary.get('total_observations', 'unknown')}",
        f"not_observed_count: {summary.get('not_observed_count', 'unknown')}",
        f"lowest_confidence: {summary.get('lowest_confidence', 'unknown')}",
        f"overall_observation_status: {summary.get('overall_observation_status', 'unknown')}",
        f"recommended_decision: {summary.get('recommended_decision', 'unknown')}",
        f"uncertainty_default: {summary.get('uncertainty_default', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "real_image_ingestion: not run",
        "computer_vision: not run",
        "ocr: not run",
        "image_generation: not run",
        "approval_automation: not run",
    ]
    return "\n".join(lines) + "\n"


def format_bind_observations_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        f"Observation/report binding: {summary.get('candidate_manifest_key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"observation_key: {summary.get('observation_key', 'unknown')}",
        f"report_key: {summary.get('report_key', 'unknown')}",
        f"candidate_reference_status: {summary.get('candidate_reference_status', 'unknown')}",
        f"overall_observation_status: {summary.get('overall_observation_status', 'unknown')}",
        f"overall_evidence_status: {summary.get('overall_evidence_status', 'unknown')}",
        f"recommended_decision: {summary.get('recommended_decision', 'unknown')}",
        f"uncertainty_default: {summary.get('uncertainty_default', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "real_image_ingestion: not run",
        "computer_vision: not run",
        "ocr: not run",
        "image_generation: not run",
        "approval_automation: not run",
        "candidate_scoring: not run",
    ]
    return "\n".join(lines) + "\n"


def format_merge_evidence_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        f"Observation evidence merge: {summary.get('candidate_manifest_key', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"observation_key: {summary.get('observation_key', 'unknown')}",
        f"report_key: {summary.get('report_key', 'unknown')}",
        f"merged_evidence_count: {summary.get('merged_evidence_count', 'unknown')}",
        f"matched_constraint_count: {summary.get('matched_constraint_count', 'unknown')}",
        f"report_only_constraint_count: {summary.get('report_only_constraint_count', 'unknown')}",
        f"manual_only_constraint_count: {summary.get('manual_only_constraint_count', 'unknown')}",
        f"overall_merged_evidence_status: {summary.get('overall_merged_evidence_status', 'unknown')}",
        f"recommended_decision: {summary.get('recommended_decision', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "real_image_ingestion: not run",
        "computer_vision: not run",
        "ocr: not run",
        "image_generation: not run",
        "approval_automation: not run",
        "candidate_scoring: not run",
        "source_report_mutation: not run",
    ]
    return "\n".join(lines) + "\n"


def format_review_packet_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    sections = payload.get("review_sections", {})
    if not isinstance(summary, dict):
        summary = {}
    if not isinstance(sections, dict):
        sections = {}
    identity = sections.get("candidate_identity", {}) if isinstance(sections.get("candidate_identity", {}), dict) else {}
    blockers = sections.get("decision_guardrails", {}).get("approval_blockers", []) if isinstance(sections.get("decision_guardrails", {}), dict) else []
    lines = [
        f"Candidate review packet: {summary.get('candidate_manifest_key', 'unknown')}",
        f"subject_name: {identity.get('subject_name', 'unknown')}",
        f"candidate_id: {summary.get('candidate_id', 'unknown')}",
        f"contract_key: {summary.get('contract_key', 'unknown')}",
        f"candidate_reference_status: {summary.get('candidate_reference_status', 'unknown')}",
        f"merged_evidence_count: {summary.get('merged_evidence_count', 'unknown')}",
        f"matched_constraint_count: {summary.get('matched_constraint_count', 'unknown')}",
        f"overall_merged_evidence_status: {summary.get('overall_merged_evidence_status', 'unknown')}",
        f"recommended_decision: {summary.get('recommended_decision', 'unknown')}",
        f"approval_allowed: {summary.get('approval_allowed', 'unknown')}",
        "approval_blockers:",
    ]
    if isinstance(blockers, list):
        lines.extend(f"- {blocker}" for blocker in blockers)
    lines.extend([
        "real_image_ingestion: not run",
        "computer_vision: not run",
        "ocr: not run",
        "image_generation: not run",
        "approval_automation: not run",
        "candidate_scoring: not run",
        "source_report_mutation: not run",
    ])
    return "\n".join(lines) + "\n"


def format_payload(payload: dict[str, Any], output_format: str, command: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if command == "list":
        return format_list_text(payload)
    if command == "intake-list":
        return format_intake_list_text(payload)
    if command == "intake-show":
        return format_intake_show_text(payload)
    if command == "byte-loading-list":
        return format_byte_loading_list_text(payload)
    if command == "byte-loading-show":
        return format_byte_loading_show_text(payload)
    if command == "intake-review-packet":
        return format_intake_review_packet_text(payload)
    if command == "evaluate":
        return format_evaluate_text(payload)
    if command == "observe":
        return format_observe_text(payload)
    if command == "bind-observations":
        return format_bind_observations_text(payload)
    if command == "merge-evidence":
        return format_merge_evidence_text(payload)
    if command == "review-packet":
        return format_review_packet_text(payload)
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

    subparsers.add_parser("intake-list", help="List fixture-only candidate intake manifest fixtures.")

    intake_show_parser = subparsers.add_parser("intake-show", help="Show a fixture-only candidate intake manifest summary.")
    intake_show_parser.add_argument("manifest", help="Manifest key, contract key, candidate id, filename, or path.")

    subparsers.add_parser("byte-loading-list", help="List fixture-only candidate image byte-loading record fixtures.")

    byte_loading_show_parser = subparsers.add_parser("byte-loading-show", help="Show a fixture-only candidate image byte-loading record summary.")
    byte_loading_show_parser.add_argument("manifest", help="Record key, contract key, candidate id, record id, intake manifest id, filename, or path.")

    intake_review_parser = subparsers.add_parser("intake-review-packet", help="Build a fixture-only candidate intake review packet.")
    intake_review_parser.add_argument("manifest", help="Manifest key, contract key, candidate id, filename, or path.")

    evaluate_parser = subparsers.add_parser("evaluate", help="Run fixture-only candidate evaluation from static report fixtures.")
    evaluate_parser.add_argument("manifest", help="Manifest key, contract key, candidate id, filename, or path.")

    observe_parser = subparsers.add_parser("observe", help="Load fixture-only manual observations for a candidate manifest.")
    observe_parser.add_argument("manifest", help="Manifest key, contract key, candidate id, filename, or path.")

    bind_parser = subparsers.add_parser("bind-observations", help="Bind fixture-only manual observations to fixture-only evaluation reports.")
    bind_parser.add_argument("manifest", help="Manifest key, contract key, candidate id, filename, or path.")

    merge_parser = subparsers.add_parser("merge-evidence", help="Merge fixture-only manual observations with fixture-only report evidence.")
    merge_parser.add_argument("manifest", help="Manifest key, contract key, candidate id, filename, or path.")

    review_parser = subparsers.add_parser("review-packet", help="Build a fixture-only human-facing candidate review packet.")
    review_parser.add_argument("manifest", help="Manifest key, contract key, candidate id, filename, or path.")
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
