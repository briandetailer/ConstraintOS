from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SUCCESSFUL_RUNTIME_EVENT_ORDER = (
    "runtime_started",
    "runtime_planned",
    "runtime_scheduled",
    "runtime_execution_started",
    "runtime_completed",
)


@dataclass(frozen=True)
class RuntimeReplayVerification:
    """Result of replay-oriented runtime event verification."""

    event_types: list[str]
    expected_event_types: list[str]
    issues: list[str] = field(default_factory=list)

    def successful(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_replay_verification": {
                "successful": self.successful(),
                "issue_count": len(self.issues),
            },
            "event_types": self.event_types,
            "expected_event_types": self.expected_event_types,
            "issues": self.issues,
        }


def verify_successful_runtime_events(result: Any) -> RuntimeReplayVerification:
    """Verify the event order for a completed runtime result payload."""

    data = result.to_dict() if hasattr(result, "to_dict") else result
    expected_event_types = list(SUCCESSFUL_RUNTIME_EVENT_ORDER)
    issues: list[str] = []

    if not isinstance(data, dict):
        return RuntimeReplayVerification(
            event_types=[],
            expected_event_types=expected_event_types,
            issues=["Runtime replay input must be a dictionary or expose to_dict()."],
        )

    events = data.get("events", [])
    if not isinstance(events, list):
        return RuntimeReplayVerification(
            event_types=[],
            expected_event_types=expected_event_types,
            issues=["Runtime replay events must be a list."],
        )

    event_types = [str(event.get("event_type", "")) for event in events if isinstance(event, dict)]
    if event_types != expected_event_types:
        issues.append(
            "Successful runtime event order mismatch: "
            f"expected {expected_event_types}, received {event_types}."
        )

    if len(event_types) != len(events):
        issues.append("Runtime replay events must all be dictionaries with event_type values.")

    return RuntimeReplayVerification(
        event_types=event_types,
        expected_event_types=expected_event_types,
        issues=issues,
    )
