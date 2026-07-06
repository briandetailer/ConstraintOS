import pytest

from runtime.execution import DryRunExecutor, ExecutionError, ExecutionRequest, PluginExecutor
from runtime.planner import RuntimePlanner
from runtime.plugins import PluginDispatchError, PluginResult
from runtime.scheduler import RuntimeScheduler, WorkerCapability


class _StaticDispatcher:
    def __init__(self, result: object) -> None:
        self.result = result

    def dispatch(self, assignment: dict[str, object], context: object | None = None) -> object:
        return self.result


class _RaisingDispatcher:
    def dispatch(self, assignment: dict[str, object], context: object | None = None) -> object:
        raise RuntimeError("plugin exploded")


class _DispatchErrorDispatcher:
    def dispatch(self, assignment: dict[str, object], context: object | None = None) -> object:
        raise PluginDispatchError("assignment must include a plugin")


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


def test_plugin_executor_maps_standard_plugin_result() -> None:
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id="SCHEDULE-0001",
        assignments=[
            {"node_id": "NODE-0001", "worker_id": "WORKER-0001", "plugin": "echo", "action": "package"}
        ],
    )
    executor = PluginExecutor(
        _StaticDispatcher(
            PluginResult(
                plugin="echo",
                node_id="NODE-0001",
                action="package",
                status="complete",
                outputs=["echo://NODE-0001"],
                logs=["ok"],
                metrics={"worker_id": "WORKER-0001"},
            )
        )
    )

    result = executor.execute(request)

    assert result.status == "complete"
    assert result.node_results[0].node_id == "NODE-0001"
    assert result.node_results[0].status == "complete"
    assert result.node_results[0].outputs == ["echo://NODE-0001"]
    assert result.node_results[0].message == "ok"


def test_plugin_executor_converts_malformed_plugin_result_to_failed_node_result() -> None:
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id="SCHEDULE-0001",
        assignments=[
            {"node_id": "NODE-0001", "worker_id": "WORKER-0001", "plugin": "broken", "action": "package"}
        ],
    )
    executor = PluginExecutor(_StaticDispatcher({"not": "a plugin result"}))

    result = executor.execute(request)

    assert result.status == "partial"
    assert result.messages == ["Plugin execution completed with failed or skipped assignments."]
    assert result.node_results[0].node_id == "NODE-0001"
    assert result.node_results[0].worker_id == "WORKER-0001"
    assert result.node_results[0].plugin == "broken"
    assert result.node_results[0].action == "package"
    assert result.node_results[0].status == "plugin_execution_failed"
    assert result.node_results[0].outputs == []
    assert result.node_results[0].message == "plugin dispatcher must return PluginResult"


def test_plugin_executor_converts_plugin_exception_to_failed_node_result() -> None:
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id="SCHEDULE-0001",
        assignments=[
            {"node_id": "NODE-0001", "worker_id": "WORKER-0001", "plugin": "broken", "action": "package"}
        ],
    )

    result = PluginExecutor(_RaisingDispatcher()).execute(request)

    assert result.status == "partial"
    assert result.node_results[0].status == "plugin_execution_failed"
    assert result.node_results[0].message == "plugin exploded"


def test_plugin_executor_preserves_dispatch_errors() -> None:
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id="SCHEDULE-0001",
        assignments=[{"node_id": "NODE-0001", "worker_id": "WORKER-0001", "action": "package"}],
    )

    with pytest.raises(PluginDispatchError, match="assignment must include a plugin"):
        PluginExecutor(_DispatchErrorDispatcher()).execute(request)


def test_plugin_executor_rejects_invalid_assignments_shape() -> None:
    with pytest.raises(ExecutionError, match="assignments must be a list"):
        PluginExecutor(_StaticDispatcher(None)).execute(
            {"execution_request": {"id": "EXEC-REQ-0001"}, "assignments": {}}
        )


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
