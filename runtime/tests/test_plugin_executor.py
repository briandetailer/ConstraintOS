import pytest

from runtime.context import RuntimeContext
from runtime.execution import ExecutionRequest, PluginExecutor
from runtime.plugins import DryRunPlugin, EchoPlugin, PluginDispatcher, PluginNotFoundError, PluginRegistry


def _executor_with_plugins() -> PluginExecutor:
    registry = PluginRegistry()
    registry.register(EchoPlugin())
    registry.register(DryRunPlugin())
    return PluginExecutor(PluginDispatcher(registry))


def test_plugin_executor_dispatches_echo_assignment() -> None:
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id="SCHEDULE-0001",
        assignments=[{"node_id": "NODE-0001", "worker_id": "WORKER-0001", "plugin": "echo", "action": "package"}],
    )

    result = _executor_with_plugins().execute(request, context=RuntimeContext(variables={"mode": "test"}))

    assert result.status == "complete"
    assert result.node_results[0].node_id == "NODE-0001"
    assert result.node_results[0].worker_id == "WORKER-0001"
    assert result.node_results[0].plugin == "echo"
    assert result.node_results[0].status == "complete"
    assert result.node_results[0].outputs == ["echo://NODE-0001"]
    assert result.node_results[0].message == "Executed package for NODE-0001."


def test_plugin_executor_dispatches_dry_run_assignment() -> None:
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id="SCHEDULE-0001",
        assignments=[{"node_id": "NODE-0002", "worker_id": "WORKER-0002", "plugin": "dry_run", "action": "render"}],
    )

    result = _executor_with_plugins().execute(request)

    assert result.status == "complete"
    assert result.node_results[0].worker_id == "WORKER-0002"
    assert result.node_results[0].plugin == "dry_run"
    assert result.node_results[0].status == "dry_run_complete"
    assert result.node_results[0].outputs == ["dry-run://NODE-0002"]


def test_plugin_executor_rejects_invalid_assignment_collection() -> None:
    with pytest.raises(ValueError, match="assignments must be a list"):
        _executor_with_plugins().execute({"execution_request": {"id": "EXEC-REQ-0001"}, "assignments": {}})


def test_plugin_executor_surfaces_unknown_plugin() -> None:
    request = ExecutionRequest(
        id="EXEC-REQ-0001",
        schedule_id="SCHEDULE-0001",
        assignments=[{"node_id": "NODE-0003", "worker_id": "WORKER-0001", "plugin": "missing", "action": "package"}],
    )

    with pytest.raises(PluginNotFoundError, match="Plugin missing is not registered"):
        _executor_with_plugins().execute(request)
