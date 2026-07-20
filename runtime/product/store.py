from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Any, Iterable, Mapping

from .models import ImageJob, JobEvent, utc_now


class JobStoreError(RuntimeError):
    pass


def _slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return normalized[:48] or "image-job"


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


class FileJobStore:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def workspace_for(self, job_id: str) -> Path:
        return self.root / job_id

    def _job_path(self, job_id: str) -> Path:
        return self.workspace_for(job_id) / "job.json"

    def _events_path(self, job_id: str) -> Path:
        return self.workspace_for(job_id) / "events.jsonl"

    def create(
        self,
        *,
        request_text: str,
        title: str | None = None,
        requested_job_id: str | None = None,
    ) -> ImageJob:
        request_text = request_text.strip()
        if not request_text:
            raise JobStoreError("request_text is required")
        if requested_job_id:
            job_id = requested_job_id.strip()
            if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]{2,95}", job_id):
                raise JobStoreError("requested_job_id contains unsupported characters")
        else:
            job_id = f"{_slug(title or request_text)}-{uuid.uuid4().hex[:10]}"
        workspace = self.workspace_for(job_id)
        if workspace.exists():
            raise JobStoreError(f"Job already exists: {job_id}")
        workspace.mkdir(parents=True)
        created_at = utc_now()
        job = ImageJob(
            job_id=job_id,
            created_at=created_at,
            updated_at=created_at,
            status="accepted",
            current_stage="request_intake",
            request_text=request_text,
            title=(title or request_text.splitlines()[0][:80]).strip(),
            workspace=str(workspace),
        )
        self.save(job)
        self.append_event(
            job_id,
            stage="request_intake",
            event_type="job_created",
            message="Image job accepted.",
            data={"title": job.title},
        )
        return job

    def save(self, job: ImageJob) -> ImageJob:
        workspace = self.workspace_for(job.job_id)
        workspace.mkdir(parents=True, exist_ok=True)
        if job.workspace != str(workspace):
            job = job.with_updates(workspace=str(workspace))
        _atomic_write_json(self._job_path(job.job_id), job.to_dict())
        return job

    def load(self, job_id: str) -> ImageJob:
        path = self._job_path(job_id)
        if not path.exists():
            raise JobStoreError(f"Job not found: {job_id}")
        return ImageJob.from_dict(json.loads(path.read_text(encoding="utf-8-sig")))

    def update(self, job_id: str, **changes: Any) -> ImageJob:
        job = self.load(job_id).with_updates(**changes)
        return self.save(job)

    def list_jobs(self, *, limit: int = 100) -> list[ImageJob]:
        jobs: list[ImageJob] = []
        for path in self.root.glob("*/job.json"):
            try:
                jobs.append(ImageJob.from_dict(json.loads(path.read_text(encoding="utf-8-sig"))))
            except (OSError, ValueError, KeyError, TypeError):
                continue
        jobs.sort(key=lambda item: item.updated_at, reverse=True)
        return jobs[: max(1, min(limit, 500))]

    def artifact_path(self, job_id: str, name: str) -> Path:
        safe_name = Path(name).name
        if safe_name != name or not safe_name:
            raise JobStoreError("Artifact names must be simple filenames")
        return self.workspace_for(job_id) / safe_name

    def write_artifact(
        self,
        job_id: str,
        name: str,
        payload: Mapping[str, Any] | list[Any] | str,
        *,
        artifact_key: str | None = None,
    ) -> Path:
        path = self.artifact_path(job_id, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(payload, str):
            path.write_text(payload, encoding="utf-8")
        else:
            temporary = path.with_suffix(path.suffix + ".tmp")
            temporary.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            temporary.replace(path)
        if artifact_key:
            job = self.load(job_id)
            artifacts = dict(job.artifacts)
            artifacts[artifact_key] = str(path)
            self.save(job.with_updates(artifacts=artifacts))
        return path

    def append_event(
        self,
        job_id: str,
        *,
        stage: str,
        event_type: str,
        message: str,
        data: Mapping[str, Any] | None = None,
    ) -> JobEvent:
        self.load(job_id)
        event = JobEvent(
            event_id=uuid.uuid4().hex,
            job_id=job_id,
            timestamp=utc_now(),
            stage=stage,
            event_type=event_type,
            message=message,
            data=dict(data or {}),
        )
        path = self._events_path(job_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event.to_dict(), sort_keys=True) + "\n")
        return event

    def read_events(self, job_id: str) -> list[JobEvent]:
        self.load(job_id)
        path = self._events_path(job_id)
        if not path.exists():
            return []
        events: list[JobEvent] = []
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            if not line.strip():
                continue
            events.append(JobEvent.from_dict(json.loads(line)))
        return events

    def artifact_index(self, job_id: str) -> dict[str, str]:
        return dict(self.load(job_id).artifacts)

    def iter_artifact_paths(self, job_id: str) -> Iterable[Path]:
        for value in self.artifact_index(job_id).values():
            yield Path(value)
