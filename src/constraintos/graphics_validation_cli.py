from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from constraintos.runtime_cli import attach_traceability, load_runtime_specification, load_workers_file, plan_runtime, summarize_payload
from runtime import ArtifactStore, RuntimeContext, RuntimeEngine

DEFAULT_EXAMPLE = "perseverance"
DEFAULT_RUNTIME_ID = "GRAPHICS-PERSEVERANCE-RUNTIME-0001"
DEFAULT_ARTIFACT_ROOT = ".constraintos/runtime/artifacts/graphics/perseverance"


def discover_project_root(start: Path | None = None) -> Path:
    """Find the repository root for example-backed graphics validation runs."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "examples" / "graphics" / "perseverance" / "spec.json").exists():
            return candidate
    return current


def resolve_example_dir(example: str, project_root: Path, explicit_example_dir: str | None = None) -> Path:
    if explicit_example_dir:
        example_dir = Path(explicit_example_dir)
        return example_dir if example_dir.is_absolute() else project_root / example_dir
    if example != DEFAULT_EXAMPLE:
        raise ValueError(f"Unsupported graphics validation example: {example}")
    return project_root / "examples" / "graphics" / "perseverance"


def read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def graphics_metadata(example: str, spec: dict[str, Any], example_dir: Path) -> dict[str, Any]:
    request = spec.get("graphics_request", {})
    artifact = spec.get("artifact", {})
    approval = read_optional_json(example_dir / "expected_approval.json")
    approval_result = approval.get("graphics_approval_result", {}) if isinstance(approval, dict) else {}
    return {
        "example": example,
        "artifact_id": artifact.get("id") if isinstance(artifact, dict) else None,
        "subject": request.get("subject") if isinstance(request, dict) else None,
        "view": request.get("view") if isinstance(request, dict) else None,
        "style": request.get("style") if isinstance(request, dict) else None,
        "mode": approval_result.get("mode", "fixture_only_no_image_generation") if isinstance(approval_result, dict) else "fixture_only_no_image_generation",
        "expected_decision": approval_result.get("decision") if isinstance(approval_result, dict) else None,
        "example_dir": str(example_dir),
        "policy_path": str(example_dir / "policy.json"),
        "expected_prompt_path": str(example_dir / "expected_prompt.json"),
        "expected_evidence_path": str(example_dir / "expected_evidence.json"),
        "expected_approval_path": str(example_dir / "expected_approval.json"),
    }


def build_graphics_validation_payload(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    project_root = Path(args.project_root).resolve() if args.project_root else discover_project_root()
    example_dir = resolve_example_dir(args.example, project_root, args.example_dir)
    spec_path = Path(args.spec) if args.spec else example_dir / "spec.json"
    workers_path = Path(args.workers_file) if args.workers_file else example_dir / "workers.json"
    if not spec_path.is_absolute():
        spec_path = project_root / spec_path
    if not workers_path.is_absolute():
        workers_path = project_root / workers_path

    specification = load_runtime_specification(spec_path)
    workers = load_workers_file(workers_path)

    if args.plan_only:
        payload = plan_runtime(specification, workers)
        exit_code = 0 if not payload["schedule"].get("unscheduled_nodes") else 1
    else:
        artifact_store = ArtifactStore(Path(args.artifact_root))
        result = RuntimeEngine(artifact_store=artifact_store).run(
            specification,
            workers,
            RuntimeContext(
                workspace=Path(args.workspace),
                variables={
                    "graphics_example": args.example,
                    "specification": str(spec_path),
                    "workers_file": str(workers_path),
                },
            ),
            runtime_id=args.runtime_id,
        )
        payload = attach_traceability(result.to_dict(), specification)
        exit_code = 0 if result.success else 1

    payload["graphics_validation"] = graphics_metadata(args.example, specification, example_dir)
    return exit_code, payload


def summarize_graphics_payload(payload: dict[str, Any]) -> str:
    summary = summarize_payload(payload)
    graphics = payload.get("graphics_validation", {})
    if not isinstance(graphics, dict):
        return summary
    return (
        summary
        + "Graphics validation "
        + f"{graphics.get('example', 'unknown')}: "
        + f"subject={graphics.get('subject', 'unknown')} | "
        + f"expected_decision={graphics.get('expected_decision', 'unknown')} | "
        + f"mode={graphics.get('mode', 'unknown')}\n"
    )


def format_graphics_payload(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "text":
        return summarize_graphics_payload(payload)
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def write_graphics_output(payload: dict[str, Any], output_path: str | None, output_format: str) -> None:
    output = format_graphics_payload(payload, output_format)
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
        print(f"Wrote graphics validation result: {target}")
        return
    print(output, end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cos-graphics-validate")
    parser.add_argument("example", nargs="?", default=DEFAULT_EXAMPLE, help="Graphics validation example to run. Default: perseverance.")
    parser.add_argument("--project-root", help="Repository root for resolving default example fixtures.")
    parser.add_argument("--example-dir", help="Directory containing spec.json, workers.json, policy.json, and expected fixtures.")
    parser.add_argument("--spec", help="Override runtime spec path. Defaults to the selected example spec.json.")
    parser.add_argument("--workers-file", help="Override workers file path. Defaults to the selected example workers.json.")
    parser.add_argument("--runtime-id", default=DEFAULT_RUNTIME_ID)
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--artifact-root", default=DEFAULT_ARTIFACT_ROOT)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        exit_code, payload = build_graphics_validation_payload(args)
        write_graphics_output(payload, args.output, args.format)
        return exit_code
    except SystemExit:
        raise
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
