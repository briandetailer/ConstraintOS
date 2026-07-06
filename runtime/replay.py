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


def verify_completed_runtime_traceability(result: Any) -> RuntimeReplayVerification:
    """Verify completed runtime identifiers and cross-payload event references."""

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
        label="Completed runtime",
        event_types=event_types,
        expected_event_types=expected_event_types,
        raw_events=events,
    )
    issues.extend(_completed_traceability_issues(data, events))

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
    runtime_result = _dict_value(data, "runtime_result")
    if runtime_result.get("status") != "partial":
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

    schedule = _dict_value(data, "schedule")
    schedule_nodes = schedule.get("unscheduled_nodes")
    if isinstance(schedule_nodes, list) and isinstance(unscheduled_nodes, list) and schedule_nodes != unscheduled_nodes:
        issues.append("Partial schedule runtime_failed unscheduled_nodes must match schedule unscheduled_nodes.")

    return issues


def _completed_traceability_issues(data: dict[str, Any], events: list[Any]) -> list[str]:
    issues: list[str] = []
    runtime_result = _dict_value(data, "runtime_result")
    plan_meta = _nested_dict_value(data, "plan", "execution_plan")
    schedule_meta = _nested_dict_value(data, "schedule", "schedule_result")
    execution_meta = _nested_dict_value(data, "execution", "execution_result")
    artifact_store = _nested_dict_value(data, "artifacts", "artifact_store")

    runtime_id = str(runtime_result.get("id", ""))
    plan_id = str(plan_meta.get("id", ""))
    schedule_id = str(schedule_meta.get("id", ""))
    schedule_status = str(schedule_meta.get("status", ""))
    execution_request_id = str(execution_meta.get("request_id", ""))
    execution_result_id = str(execution_meta.get("id", ""))
    execution_status = str(execution_meta.get("status", ""))
    node_result_count = _node_result_count(data)
    artifact_count = artifact_store.get("count")

    if runtime_result.get("status") != "completed":
        issues.append("Completed runtime traceability requires runtime_result status to be completed.")
    if not runtime_id:
        issues.append("Completed runtime traceability requires runtime_result id.")

    expected_request_id = f"{runtime_id}-EXEC-REQ-0001"
    expected_result_id = f"{runtime_id}-EXEC-RESULT-0001"
    if runtime_id and execution_request_id != expected_request_id:
        issues.append(f"Completed runtime execution request id must match {expected_request_id}.")
    if runtime_id and execution_result_id != expected_result_id:
        issues.append(f"Completed runtime execution result id must match {expected_result_id}.")

    started_payload = _event_payload(events, "runtime_started")
    planned_payload = _event_payload(events, "runtime_planned")
    scheduled_payload = _event_payload(events, "runtime_scheduled")
    execution_started_payload = _event_payload(events, "runtime_execution_started")
    completed_payload = _event_payload(events, "runtime_completed")

    if started_payload.get("runtime_id") != runtime_id:
        issues.append("runtime_started runtime_id must match runtime_result id.")
    if planned_payload.get("plan_id") != plan_id:
        issues.append("runtime_planned plan_id must match execution_plan id.")
    if scheduled_payload.get("schedule_id") != schedule_id:
        issues.append("runtime_scheduled schedule_id must match schedule_result id.")
    if scheduled_payload.get("status") != schedule_status:
        issues.append("runtime_scheduled status must match schedule_result status.")
    if execution_started_payload.get("schedule_id") != schedule_id:
        issues.append("runtime_execution_started schedule_id must match schedule_result id.")
    if execution_started_payload.get("execution_request_id") != execution_request_id:
        issues.append("runtime_execution_started execution_request_id must match execution result request_id.")
    if completed_payload.get("execution_result_id") != execution_result_id:
        issues.append("runtime_completed execution_result_id must match execution_result id.")
    if completed_payload.get("status") != execution_status:
        issues.append("runtime_completed status must match execution_result status.")
    if completed_payload.get("node_results") != node_result_count:
        issues.append("runtime_completed node_results must match serialized node result count.")
    if completed_payload.get("artifacts") != artifact_count:
        issues.append("runtime_completed artifacts must match artifact_store count.")

    return issues


def _dict_value(value: dict[str, Any], key: str) -> dict[str, Any]:
    payload = value.get(key, {}) if isinstance(value, dict) else {}
    return payload if isinstance(payload, dict) else {}


def _nested_dict_value(value: dict[str, Any], key: str, nested_key: str) -> dict[str, Any]:
    return _dict_value(_dict_value(value, key), nested_key)


def _node_result_count(data: dict[str, Any]) -> int:
    execution = _dict_value(data, "execution")
    node_results = execution.get("node_results", [])
    return len(node_results) if isinstance(node_results, list) else 0


def _event_payload(events: list[Any], event_type: str) -> dict[str, Any]:
    for event in events:
        if isinstance(event, dict) and event.get("event_type") == event_type:
            payload = event.get("payload", {})
            return payload if isinstance(payload, dict) else {}
    return {}


def _final_failed_event_payload(events: list[Any]) -> dict[str, Any] | None:
    failed_events = [event for event in events if isinstance(event, dict) and event.get("event_type") == "runtime_failed"]
    if not failed_events:
        return None
    payload = failed_events[-1].get("payload")
    return payload if isinstance(payload, dict) else None
