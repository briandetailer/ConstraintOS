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

PARTIAL_SCHEDULE_RUNTIME_EVENT_ORDER = (
    "runtime_started",
    "runtime_planned",
    "runtime_scheduled",
    "runtime_failed",
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

    data = _runtime_data(result)
    expected_event_types = list(SUCCESSFUL_RUNTIME_EVENT_ORDER)
    input_issue = _input_issue(data)
    if input_issue:
        return RuntimeReplayVerification(event_types=[], expected_event_types=expected_event_types, issues=[input_issue])

    events = data.get("events", [])
    events_issue = _events_issue(events)
    if events_issue:
        return RuntimeReplayVerification(event_types=[], expected_event_types=expected_event_types, issues=[events_issue])

    event_types = _event_types(events)
    issues = _event_order_issues(
        label="Successful runtime",
        event_types=event_types,
        expected_event_types=expected_event_types,
        raw_events=events,
    )

    return RuntimeReplayVerification(
        event_types=event_types,
        expected_event_types=expected_event_types,
        issues=issues,
    )


def verify_partial_schedule_runtime_events(result: Any) -> RuntimeReplayVerification:
    """Verify event order and required payloads for a partial schedule runtime result."""

    data = _runtime_data(result)
    expected_event_types = list(PARTIAL_SCHEDULE_RUNTIME_EVENT_ORDER)
    input_issue = _input_issue(data)
    if input_issue:
        return RuntimeReplayVerification(event_types=[], expected_event_types=expected_event_types, issues=[input_issue])

    events = data.get("events", [])
    events_issue = _events_issue(events)
    if events_issue:
        return RuntimeReplayVerification(event_types=[], expected_event_types=expected_event_types, issues=[events_issue])

    event_types = _event_types(events)
    issues = _event_order_issues(
        label="Partial schedule runtime",
        event_types=event_types,
        expected_event_types=expected_event_types,
        raw_events=events,
    )
    issues.extend(_partial_schedule_payload_issues(data, events))

    return RuntimeReplayVerification(
        event_types=event_types,
        expected_event_types=expected_event_types,
        issues=issues,
    )


def _runtime_data(result: Any) -> Any:
    return result.to_dict() if hasattr(result, "to_dict") else result


def _input_issue(data: Any) -> str:
    return "Runtime replay input must be a dictionary or expose to_dict()." if not isinstance(data, dict) else ""


def _events_issue(events: Any) -> str:
    return "Runtime replay events must be a list." if not isinstance(events, list) else ""


def _event_types(events: list[Any]) -> list[str]:
    return [str(event.get("event_type", "")) for event in events if isinstance(event, dict)]


def _event_order_issues(
    label: str,
    event_types: list[str],
    expected_event_types: list[str],
    raw_events: list[Any],
) -> list[str]:
    issues: list[str] = []
    if event_types != expected_event_types:
        issues.append(f"{label} event order mismatch: expected {expected_event_types}, received {event_types}.")
    if len(event_types) != len(raw_events):
        issues.append("Runtime replay events must all be dictionaries with event_type values.")
    return issues


def _partial_schedule_payload_issues(data: dict[str, Any], events: list[Any]) -> list[str]:
    issues: list[str] = []
    runtime_result = data.get("runtime_result", {})
    if isinstance(runtime_result, dict) and runtime_result.get("status") != "partial":
        issues.append("Partial schedule runtime replay requires runtime_result status to be partial.")

    if data.get("execution") is not None:
        issues.append("Partial schedule runtime replay requires execution to be omitted.")

    failed_payload = _final_failed_event_payload(events)
    if failed_payload is None:
        issues.append("Partial schedule runtime replay requires a runtime_failed event payload.")
        return issues

    unscheduled_nodes = failed_payload.get("unscheduled_nodes")
    unscheduled_count = failed_payload.get("unscheduled_count")
    if not isinstance(unscheduled_nodes, list):
        issues.append("Partial schedule runtime_failed payload requires unscheduled_nodes list.")
    if not isinstance(unscheduled_count, int):
        issues.append("Partial schedule runtime_failed payload requires unscheduled_count integer.")
    if isinstance(unscheduled_nodes, list) and isinstance(unscheduled_count, int) and unscheduled_count != len(unscheduled_nodes):
        issues.append("Partial schedule runtime_failed unscheduled_count must match unscheduled_nodes length.")

    schedule = data.get("schedule", {})
    schedule_nodes = schedule.get("unscheduled_nodes") if isinstance(schedule, dict) else None
    if isinstance(schedule_nodes, list) and isinstance(unscheduled_nodes, list) and schedule_nodes != unscheduled_nodes:
        issues.append("Partial schedule runtime_failed unscheduled_nodes must match schedule unscheduled_nodes.")

    return issues


def _final_failed_event_payload(events: list[Any]) -> dict[str, Any] | None:
    failed_events = [event for event in events if isinstance(event, dict) and event.get("event_type") == "runtime_failed"]
    if not failed_events:
        return None
    payload = failed_events[-1].get("payload")
    return payload if isinstance(payload, dict) else None
