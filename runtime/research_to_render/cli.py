from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .discovery import DiscoveryError, OpenAIWebDiscoveryProvider
from .models import ConstraintRequest
from .orchestrator import ResearchToRenderOrchestrator


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cos-research-render",
        description="Plan a constraint-driven, source-backed research-to-render workflow.",
    )
    parser.add_argument("--request", type=Path, required=True)
    discovery = parser.add_mutually_exclusive_group(required=True)
    discovery.add_argument("--sources", type=Path)
    discovery.add_argument("--live-web-search", action="store_true")
    parser.add_argument("--research-model")
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    request_payload = _read_json(args.request)
    request = ConstraintRequest.from_payload(request_payload)
    orchestrator = ResearchToRenderOrchestrator()

    if args.live_web_search:
        research_plan = orchestrator.build_research_plan(request)
        provider = OpenAIWebDiscoveryProvider(model=args.research_model)
        try:
            candidates = provider.discover(request, research_plan)
        except DiscoveryError as exc:
            raise SystemExit(str(exc)) from exc
        result = orchestrator.orchestrate(request, candidates)
        discovery_manifest = provider.last_manifest
    else:
        source_payload = _read_json(args.sources)
        if not isinstance(source_payload, list):
            raise SystemExit("--sources must contain a JSON array")
        result = orchestrator.orchestrate_payload(request_payload, source_payload)
        discovery_manifest = {
            "provider": "recorded_source_fixture",
            "source_file": str(args.sources),
            "candidate_count": len(source_payload),
            "queries": list(result.research_plan.queries),
        }

    output_payload = result.to_dict()
    output_payload["discovery"] = discovery_manifest
    rendered = json.dumps(output_payload, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result.status == "planned" else 2


if __name__ == "__main__":
    raise SystemExit(main())
