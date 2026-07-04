from __future__ import annotations

from typing import Any

from constraintos.atlas_builder import run_volume_dry_build
from constraintos.compiler import compile_to_text
from constraintos.job_queue import InMemoryJobQueue, create_queue_status

try:
    from fastapi import FastAPI, HTTPException
except ImportError:  # pragma: no cover
    FastAPI = None
    HTTPException = None

QUEUE = InMemoryJobQueue()


def health_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "constraintos-api",
        "version": "1.0.0-alpha.16",
    }


def compile_payload(spec: dict[str, Any], renderer: str = "generic") -> dict[str, Any]:
    return compile_to_text(spec, renderer=renderer).to_dict()


def validate_payload(payload: dict[str, Any], repo_root: str = ".") -> dict[str, Any]:
    return {
        "status": "stub",
        "message": "Validation endpoint scaffold is active. Repository-file validation remains CLI-backed.",
        "request": payload,
        "repo_root": repo_root,
    }


def volume_build_payload(volume_plan: dict[str, Any], specs_by_artifact_id: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    return run_volume_dry_build(volume_plan, specs_by_artifact_id or {})


def enqueue_job_payload(job_id: str, job_type: str, payload: dict[str, Any], priority: int = 5) -> dict[str, Any]:
    return QUEUE.enqueue(job_id, job_type, payload, priority=priority).to_dict()


def get_job_payload(job_id: str) -> dict[str, Any]:
    record = QUEUE.get(job_id)
    if record is None:
        if HTTPException is not None:
            raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")
        raise KeyError(f"Job not found: {job_id}")
    return record.to_dict()


def queue_status_payload() -> dict[str, Any]:
    jobs = QUEUE.list_jobs()
    return create_queue_status(
        "default",
        queued=sum(1 for job in jobs if job.status == "queued"),
        running=sum(1 for job in jobs if job.status == "running"),
        complete=sum(1 for job in jobs if job.status == "complete"),
        failed=sum(1 for job in jobs if job.status == "failed"),
    )


def create_app() -> Any:
    if FastAPI is None:
        raise RuntimeError("FastAPI is required to create the API app. Install with: pip install fastapi")

    app = FastAPI(title="ConstraintOS API", version="1.0.0-alpha.16")

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
        if payload.get("queue", False):
            job_id = payload.get("job_id", "JOB-0001")
            return enqueue_job_payload(job_id, "volume_build", payload, priority=payload.get("priority", 5))
        volume_plan = payload.get("volume_plan_payload", payload)
        specs = payload.get("specs_by_artifact_id", {})
        return volume_build_payload(volume_plan, specs)

    @post_jobs_route(app)
    def create_job(payload: dict[str, Any]) -> dict[str, Any]:
        return enqueue_job_payload(
            payload.get("job_id", "JOB-0001"),
            payload.get("job_type", "generic"),
            payload.get("payload", {}),
            priority=payload.get("priority", 5),
        )

    @app.get("/jobs/{job_id}")
    def get_job(job_id: str) -> dict[str, Any]:
        return get_job_payload(job_id)

    @app.get("/queue/status")
    def get_queue_status() -> dict[str, Any]:
        return queue_status_payload()

    return app


def post_jobs_route(app: Any) -> Any:
    return app.post("/jobs")


app = create_app() if FastAPI is not None else None
