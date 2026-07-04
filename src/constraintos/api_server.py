from __future__ import annotations

from typing import Any

from constraintos.atlas_builder import run_volume_dry_build
from constraintos.compiler import compile_to_text
from constraintos.cli import validate_artifact
from pathlib import Path

try:
    from fastapi import FastAPI
except ImportError:  # pragma: no cover
    FastAPI = None


def health_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "constraintos-api",
        "version": "1.0.0-alpha.15",
    }


def compile_payload(spec: dict[str, Any], renderer: str = "generic") -> dict[str, Any]:
    return compile_to_text(spec, renderer=renderer).to_dict()


def validate_payload(payload: dict[str, Any], repo_root: str = ".") -> dict[str, Any]:
    # Phase 15 keeps validation as a stub because full API validation will need
    # persisted artifacts or uploaded files. This preserves the endpoint contract
    # without pretending an API payload is already a repository file.
    return {
        "status": "stub",
        "message": "Validation endpoint scaffold is active. Repository-file validation remains CLI-backed.",
        "request": payload,
        "repo_root": repo_root,
    }


def volume_build_payload(volume_plan: dict[str, Any], specs_by_artifact_id: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    return run_volume_dry_build(volume_plan, specs_by_artifact_id or {})


def create_app() -> Any:
    if FastAPI is None:
        raise RuntimeError("FastAPI is required to create the API app. Install with: pip install fastapi")

    app = FastAPI(title="ConstraintOS API", version="1.0.0-alpha.15")

    @app.get("/health")
    def get_health() -> dict[str, Any]:
        return health_payload()

    @app.post("/compile")
    def compile_specification(payload: dict[str, Any]) -> dict[str, Any]:
        renderer = payload.get("renderer", "generic")
        spec = payload.get("spec", payload)
        return compile_payload(spec, renderer=renderer)

    @app.post("/validate")
    def validate_artifact_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        return validate_payload(payload)

    @app.post("/builds/volume")
    def create_volume_build(payload: dict[str, Any]) -> dict[str, Any]:
        volume_plan = payload.get("volume_plan_payload", payload)
        specs = payload.get("specs_by_artifact_id", {})
        return volume_build_payload(volume_plan, specs)

    return app


app = create_app() if FastAPI is not None else None
