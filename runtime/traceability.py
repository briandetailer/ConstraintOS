from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from runtime.result import RuntimeResult


@dataclass(frozen=True)
class RuntimeTraceRecord:
    record_id: str
    record_type: str
    source_id: str
    runtime_id: str
    status: str
    parent_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.record_id,
            "type": self.record_type,
            "source_id": self.source_id,
            "runtime_id": self.runtime_id,
            "status": self.status,
            "parent_id": self.parent_id,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class RuntimeTrace:
    runtime_id: str
    status: str
    success: bool
    records: list[RuntimeTraceRecord]

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_traceability": {
                "runtime_id": self.runtime_id,
                "status": self.status,
                "success": self.success,
                "record_count": len(self.records),
            },
            "records": [record.to_dict() for record in self.records],
        }


def runtime_result_to_trace(result: RuntimeResult | dict[str, Any]) -> RuntimeTrace:
    data = result.to_dict() if isinstance(result, RuntimeResult) else result
    if not isinstance(data, dict):
        data = {}
    runtime_result = _dict_value(data, "runtime_result")
    runtime_id = str(runtime_result.get("id", "RUNTIME-UNKNOWN"))
    status = str(runtime_result.get("status", "unknown"))
    success = bool(runtime_result.get("success", False))

    records: list[RuntimeTraceRecord] = []
    records.extend(_plan_records(runtime_id, data))
    records.extend(_schedule_records(runtime_id, data))
    records.extend(_execution_records(runtime_id, data))
    records.extend(_artifact_records(runtime_id, data))
    records.extend(_event_records(runtime_id, data))

    return RuntimeTrace(runtime_id=runtime_id, status=status, success=success, records=records)


def _plan_records(runtime_id: str, data: dict[str, Any]) -> list[RuntimeTraceRecord]:
    records: list[RuntimeTraceRecord] = []
    plan = _dict_value(data, "plan")
    plan_id = _nested_value(plan, "execution_plan", "id", "PLAN-UNKNOWN")
    for node in _list_value(plan, "nodes"):
        node_id = str(node.get("id", "NODE-UNKNOWN")) if isinstance(node, dict) else "NODE-UNKNOWN"
        records.append(RuntimeTraceRecord(f"{runtime_id}:plan:{node_id}", "plan_node", node_id, runtime_id, "planned", plan_id))
    return records


def _schedule_records(runtime_id: str, data: dict[str, Any]) -> list[RuntimeTraceRecord]:
    records: list[RuntimeTraceRecord] = []
    schedule = _dict_value(data, "schedule")
    schedule_id = _nested_value(schedule, "schedule_result", "id", "SCHEDULE-UNKNOWN")
    for assignment in _list_value(schedule, "assignments"):
        if not isinstance(assignment, dict):
            continue
        node_id = str(assignment.get("node_id", "NODE-UNKNOWN"))
        records.append(RuntimeTraceRecord(f"{runtime_id}:schedule:{node_id}", "scheduled_assignment", node_id, runtime_id, "scheduled", schedule_id, {"worker_id": assignment.get("worker_id")}))
    for node_id in _list_value(schedule, "unscheduled_nodes"):
        records.append(RuntimeTraceRecord(f"{runtime_id}:unscheduled:{node_id}", "unscheduled_node", str(node_id), runtime_id, "unscheduled", schedule_id))
    return records


def _execution_records(runtime_id: str, data: dict[str, Any]) -> list[RuntimeTraceRecord]:
    records: list[RuntimeTraceRecord] = []
    execution = _dict_value(data, "execution")
    execution_id = _nested_value(execution, "execution_result", "id", "EXECUTION-UNKNOWN")
    for node_result in _list_value(execution, "node_results"):
        if not isinstance(node_result, dict):
            continue
        node_id = str(node_result.get("node_id", "NODE-UNKNOWN"))
        records.append(RuntimeTraceRecord(f"{runtime_id}:execution:{node_id}", "node_result", node_id, runtime_id, str(node_result.get("status", "unknown")), execution_id, {"plugin": node_result.get("plugin"), "worker_id": node_result.get("worker_id")}))
    return records


def _artifact_records(runtime_id: str, data: dict[str, Any]) -> list[RuntimeTraceRecord]:
    records: list[RuntimeTraceRecord] = []
    artifacts = _dict_value(data, "artifacts")
    for artifact in _list_value(artifacts, "artifacts"):
        if not isinstance(artifact, dict):
            continue
        artifact_id = str(artifact.get("id", "ARTIFACT-UNKNOWN"))
        records.append(RuntimeTraceRecord(f"{runtime_id}:artifact:{artifact_id}", "artifact", artifact_id, runtime_id, "recorded", str(artifact.get("producer", runtime_id)), {"uri": artifact.get("uri"), "kind": artifact.get("kind")}))
    return records


def _event_records(runtime_id: str, data: dict[str, Any]) -> list[RuntimeTraceRecord]:
    records: list[RuntimeTraceRecord] = []
    for index, event in enumerate(_list_value(data, "events"), start=1):
        if not isinstance(event, dict):
            continue
        event_type = str(event.get("event_type", "runtime_event"))
        records.append(RuntimeTraceRecord(f"{runtime_id}:event:{index:04d}", "runtime_event", event_type, runtime_id, event_type, runtime_id))
    return records


def _dict_value(value: dict[str, Any], key: str) -> dict[str, Any]:
    payload = value.get(key, {}) if isinstance(value, dict) else {}
    return payload if isinstance(payload, dict) else {}


def _list_value(value: dict[str, Any], key: str) -> list[Any]:
    payload = value.get(key, []) if isinstance(value, dict) else []
    return payload if isinstance(payload, list) else []


def _nested_value(value: dict[str, Any], key: str, nested_key: str, default: str) -> str:
    nested = _dict_value(value, key)
    return str(nested.get(nested_key, default))
