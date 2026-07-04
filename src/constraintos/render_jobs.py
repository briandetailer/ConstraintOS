from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from constraintos.adapters import DryRunRendererAdapter, RenderRequest, RenderResponse


@dataclass
class OutputReference:
    id: str
    artifact_id: str
    renderer: str
    uri: str
    media_type: str
    created: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_reference": {
                "id": self.id,
                "artifact_id": self.artifact_id,
                "renderer": self.renderer,
                "uri": self.uri,
                "media_type": self.media_type,
                "created": self.created,
            },
            "metadata": self.metadata,
        }


@dataclass
class RenderJob:
    id: str
    artifact_id: str
    renderer: str
    instruction: str
    status: str
    created: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "render_job": {
                "id": self.id,
                "artifact_id": self.artifact_id,
                "renderer": self.renderer,
                "status": self.status,
                "created": self.created,
            },
            "instruction": self.instruction,
            "metadata": self.metadata,
        }


def create_render_job(job_id: str, artifact_id: str, renderer: str, instruction: str, metadata: dict[str, Any] | None = None) -> RenderJob:
    return RenderJob(
        id=job_id,
        artifact_id=artifact_id,
        renderer=renderer,
        instruction=instruction,
        status="queued",
        created=date.today().isoformat(),
        metadata=metadata or {},
    )


def create_output_reference(output_id: str, artifact_id: str, renderer: str, uri: str, media_type: str = "application/octet-stream", metadata: dict[str, Any] | None = None) -> OutputReference:
    return OutputReference(
        id=output_id,
        artifact_id=artifact_id,
        renderer=renderer,
        uri=uri,
        media_type=media_type,
        created=date.today().isoformat(),
        metadata=metadata or {},
    )


def run_dry_render_job(job: RenderJob) -> dict[str, Any]:
    adapter = DryRunRendererAdapter()
    request: RenderRequest = adapter.prepare(job.instruction, job.artifact_id, job.metadata)
    response: RenderResponse = adapter.render(request)
    output = create_output_reference(
        output_id=f"OUTPUT-{job.artifact_id}",
        artifact_id=job.artifact_id,
        renderer=response.renderer,
        uri=f"dry-run://{job.artifact_id}",
        media_type="text/plain",
        metadata=response.metadata,
    )
    return {
        "render_job": dict(job.to_dict()["render_job"], status=response.status),
        "request": request.__dict__,
        "response": response.__dict__,
        "output": output.to_dict(),
    }


def update_manifest_with_output(manifest: dict[str, Any], output_reference: dict[str, Any]) -> dict[str, Any]:
    updated = dict(manifest)
    outputs = list(updated.get("outputs", []))
    outputs.append(output_reference)
    updated["outputs"] = outputs
    return updated
