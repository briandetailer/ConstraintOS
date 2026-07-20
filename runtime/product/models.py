from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class JobEvent:
    event_id: str
    job_id: str
    timestamp: str
    stage: str
    event_type: str
    message: str
    data: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "JobEvent":
        return cls(
            event_id=str(payload["event_id"]),
            job_id=str(payload["job_id"]),
            timestamp=str(payload["timestamp"]),
            stage=str(payload["stage"]),
            event_type=str(payload["event_type"]),
            message=str(payload["message"]),
            data=dict(payload.get("data", {})),
        )


@dataclass(frozen=True)
class ImageJob:
    job_id: str
    created_at: str
    updated_at: str
    status: str
    current_stage: str
    request_text: str
    title: str
    subject: str | None = None
    workspace: str | None = None
    artifacts: Mapping[str, str] = field(default_factory=dict)
    blockers: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    error: str | None = None
    approval_allowed: bool = False
    production_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        payload["warnings"] = list(self.warnings)
        return payload

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ImageJob":
        return cls(
            job_id=str(payload["job_id"]),
            created_at=str(payload["created_at"]),
            updated_at=str(payload["updated_at"]),
            status=str(payload["status"]),
            current_stage=str(payload["current_stage"]),
            request_text=str(payload["request_text"]),
            title=str(payload.get("title") or payload["job_id"]),
            subject=(
                str(payload["subject"]).strip()
                if payload.get("subject") is not None
                else None
            ),
            workspace=(
                str(payload["workspace"]).strip()
                if payload.get("workspace") is not None
                else None
            ),
            artifacts=dict(payload.get("artifacts", {})),
            blockers=tuple(str(item) for item in payload.get("blockers", [])),
            warnings=tuple(str(item) for item in payload.get("warnings", [])),
            error=str(payload["error"]) if payload.get("error") else None,
            approval_allowed=bool(payload.get("approval_allowed", False)),
            production_ready=bool(payload.get("production_ready", False)),
        )

    def with_updates(self, **changes: Any) -> "ImageJob":
        payload = self.to_dict()
        payload.update(changes)
        payload["updated_at"] = utc_now()
        return ImageJob.from_dict(payload)
