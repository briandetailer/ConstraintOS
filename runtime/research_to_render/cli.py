from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .orchestrator import ResearchToRenderOrchestrator


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cos-research-render",
        description="Plan a constraint-driven, source-backed research-to-render workflow.",
    )
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    request_payload = _read_json(args.request)
    source_payload = _read_json(args.sources)
    if not isinstance(source_payload, list):
        raise SystemExit("--sources must contain a JSON array")
    result = ResearchToRenderOrchestrator().orchestrate_payload(
        request_payload,
        source_payload,
    )
    rendered = json.dumps(result.to_dict(), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result.status == "planned" else 2


if __name__ == "__main__":
    raise SystemExit(main())
