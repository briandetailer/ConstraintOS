import pytest

from runtime.execution import DryRunExecutor, ExecutionError, ExecutionRequest
from runtime.planner import RuntimePlanner
from runtime.scheduler import RuntimeScheduler, WorkerCapability


def test_execute_request_from_assignment() -> None:
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id="SCHEDULE-0001",
        assignments=[
            {"node_id": "NODE-0001", "worker_id": "WORKER-0001", "plugin": "blender", "action": "render"}
        ],
    )
    result = DryRunExecutor().execute(request)
    data = result.to_dict()
    assert data["execution_result"]["status"] == "complete"
    assert data["node_results"][0]["status"] == "dry_run_complete"
    assert data["node_results"][0]["outputs"] == ["dry-run://NODE-0001"]


def test_execute_rejects_non_dry_run() -> None:
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id="SCHEDULE-0001",
        assignments=[],
        dry_run=False,
    )
    with pytest.raises(ExecutionError, match="DryRunExecutor only accepts dry-run requests"):
        DryRunExecutor().execute(request)


def test_execute_rejects_invalid_assignments_shape() -> None:
    with pytest.raises(ExecutionError, match="assignments must be a list"):
        DryRunExecutor().execute({"execution_request": {"id": "EXEC-REQ-0001", "dry_run": True}, "assignments": {}})


def test_plan_schedule_execute_pipeline() -> None:
    plan = RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "package"}]})
    schedule = RuntimeScheduler().schedule(plan, [WorkerCapability("WORKER-0001", ["generic"])])
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id=schedule.id,
        assignments=schedule.to_dict()["assignments"],
    )
    result = DryRunExecutor().execute(request)
    assert result.status == "complete"
    assert result.node_results[0].node_id == "NODE-0001"
