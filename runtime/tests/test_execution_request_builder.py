import pytest

from runtime.execution import ExecutionRequest, ExecutionRequestBuildError
from runtime.planner import RuntimePlanner
from runtime.scheduler import RuntimeScheduler, WorkerCapability


def test_execution_request_from_scheduled_result() -> None:
    plan = RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "package"}]})
    schedule = RuntimeScheduler().schedule(plan, [WorkerCapability("WORKER-0001", ["generic"])])

    request = ExecutionRequest.from_schedule(schedule.to_dict(), request_id="EXEC-REQ-0007")

    assert request.id == "EXEC-REQ-0007"
    assert request.schedule_id == "SCHEDULE-0001"
    assert request.assignments == schedule.to_dict()["assignments"]


def test_execution_request_rejects_partial_schedule() -> None:
    plan = RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "plugin": "freecad", "action": "model"}]})
    schedule = RuntimeScheduler().schedule(plan, [WorkerCapability("WORKER-0001", ["generic"])])

    with pytest.raises(ExecutionRequestBuildError):
        ExecutionRequest.from_schedule(schedule.to_dict())
