from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from .service import ConstraintOSProductService, ProductServiceError
from .store import FileJobStore, JobStoreError


def _job_root(value: str | None = None) -> Path:
    configured = value or os.environ.get("CONSTRAINTOS_JOB_ROOT", "runs/product-jobs")
    return Path(configured).resolve()


def _read_request_text(args: argparse.Namespace) -> str:
    if args.request_file:
        return Path(args.request_file).read_text(encoding="utf-8-sig").strip()
    return str(args.request or "").strip()


def _load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.structured_json:
        loaded = json.loads(Path(args.structured_json).read_text(encoding="utf-8-sig"))
        if not isinstance(loaded, dict):
            raise ValueError("--structured-json must contain a JSON object")
        payload.update(loaded)
    request_text = _read_request_text(args)
    if request_text:
        payload["request_text"] = request_text
    if args.title:
        payload["title"] = args.title
    if args.job_id:
        payload["job_id"] = args.job_id
    if not str(payload.get("request_text", "")).strip():
        raise ValueError("Provide --request, --request-file, or request_text in --structured-json")
    return payload


def create_job(args: argparse.Namespace) -> int:
    service = ConstraintOSProductService(FileJobStore(_job_root(args.job_root)))
    job = service.create_job(_load_payload(args), run_research=args.run_research)
    print(json.dumps(service.get_job(job.job_id, include_events=True), indent=2, sort_keys=True))
    return 0 if job.status not in {"failed", "research_failed"} else 2


def show_job(args: argparse.Namespace) -> int:
    service = ConstraintOSProductService(FileJobStore(_job_root(args.job_root)))
    print(
        json.dumps(
            service.get_job(args.job_id, include_events=args.events),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def list_jobs(args: argparse.Namespace) -> int:
    service = ConstraintOSProductService(FileJobStore(_job_root(args.job_root)))
    print(json.dumps(service.list_jobs(limit=args.limit), indent=2, sort_keys=True))
    return 0


def run_research(args: argparse.Namespace) -> int:
    service = ConstraintOSProductService(FileJobStore(_job_root(args.job_root)))
    job = service.run_research(args.job_id)
    print(json.dumps(service.get_job(job.job_id, include_events=True), indent=2, sort_keys=True))
    return 0 if job.status != "research_failed" else 2


def resume_job(args: argparse.Namespace) -> int:
    payload = json.loads(Path(args.structured_json).read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("--structured-json must contain a JSON object")
    service = ConstraintOSProductService(FileJobStore(_job_root(args.job_root)))
    job = service.resume_after_clarification(
        args.job_id,
        payload,
        run_research=args.run_research,
    )
    print(json.dumps(service.get_job(job.job_id, include_events=True), indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cos-image-job",
        description="Create and manage persistent ConstraintOS technical image jobs.",
    )
    parser.add_argument(
        "--job-root",
        help="Persistent job workspace root. Defaults to CONSTRAINTOS_JOB_ROOT or runs/product-jobs.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser(
        "create",
        help="Create a job from natural language or a structured request JSON file.",
    )
    create.add_argument("--request")
    create.add_argument("--request-file")
    create.add_argument("--structured-json")
    create.add_argument("--title")
    create.add_argument("--job-id")
    create.add_argument("--run-research", action="store_true")
    create.set_defaults(func=create_job)

    show = subparsers.add_parser("show", help="Show a persistent image job.")
    show.add_argument("job_id")
    show.add_argument("--events", action="store_true")
    show.set_defaults(func=show_job)

    listing = subparsers.add_parser("list", help="List recent image jobs.")
    listing.add_argument("--limit", type=int, default=100)
    listing.set_defaults(func=list_jobs)

    research = subparsers.add_parser(
        "research",
        help="Run live authoritative source discovery for an existing research-ready job.",
    )
    research.add_argument("job_id")
    research.set_defaults(func=run_research)

    resume = subparsers.add_parser(
        "resume",
        help="Resolve clarification blockers with a structured request and continue the job.",
    )
    resume.add_argument("job_id")
    resume.add_argument("--structured-json", required=True)
    resume.add_argument("--run-research", action="store_true")
    resume.set_defaults(func=resume_job)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (ProductServiceError, JobStoreError, ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
