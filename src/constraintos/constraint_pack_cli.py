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


def load_data_file(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        if yaml is None:
            raise RuntimeError("PyYAML is required")
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain an object")
    return data


def format_payload(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if yaml is None:
        raise RuntimeError("PyYAML is required")
    return yaml.safe_dump(payload, sort_keys=False)


def write_output(payload: dict[str, Any], output_path: str | None, output_format: str) -> None:
    output = format_payload(payload, output_format)
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
        print(f"Wrote render specification: {target}")
    else:
        print(output, end="")


def run_apply(args: argparse.Namespace) -> int:
    render_specification = load_data_file(Path(args.render_specification))
    constraint_pack = load_data_file(Path(args.constraint_pack))
    applied = apply_constraint_pack(render_specification, constraint_pack)
    write_output(applied, args.output, args.format)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cos-apply-constraints")
    parser.add_argument("render_specification")
    parser.add_argument("constraint_pack")
    parser.add_argument("--format", choices=["yaml", "json"], default="yaml")
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        return run_apply(args)
    except SystemExit:
        raise
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
