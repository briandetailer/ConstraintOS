from runtime import RuntimeContext, RuntimeEngine, RuntimeState
from runtime.execution import create_default_plugin_executor, create_default_plugin_registry
from runtime.scheduler import WorkerCapability


def test_default_plugin_registry_contains_builtin_plugins() -> None:
    registry = create_default_plugin_registry()

    assert registry.names() == ["dry_run", "echo"]


def test_runtime_engine_can_execute_registered_plugin_pipeline() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [
            {"id": "NODE-0001", "plugin": "echo", "action": "prepare"},
            {"id": "NODE-0002", "plugin": "echo", "action": "package", "depends_on": ["NODE-0001"]},
        ],
    }
    engine = RuntimeEngine(executor=create_default_plugin_executor())

    result = engine.run(
        specification,
        [WorkerCapability("WORKER-0001", ["echo"])],
        RuntimeContext(variables={"mode": "plugin-test"}),
    )

    execution = result.execution or {}
    node_results = execution.get("node_results", [])
    artifacts = result.artifacts or {}

    assert result.status == RuntimeState.COMPLETED
    assert result.success is True
    assert execution["execution_result"]["status"] == "complete"
    assert [node["plugin"] for node in node_results] == ["echo", "echo"]
    assert [node["status"] for node in node_results] == ["complete", "complete"]
    assert [node["outputs"] for node in node_results] == [["echo://NODE-0001"], ["echo://NODE-0002"]]
    assert artifacts["artifact_store"]["count"] == 2
    assert [artifact["uri"] for artifact in artifacts["artifacts"]] == ["echo://NODE-0001", "echo://NODE-0002"]
    assert [artifact["producer"] for artifact in artifacts["artifacts"]] == ["NODE-0001", "NODE-0002"]


def test_runtime_engine_reports_failure_for_unregistered_plugin_at_execution() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "missing", "action": "prepare"}],
    }
    engine = RuntimeEngine(executor=create_default_plugin_executor())

    result = engine.run(specification, [WorkerCapability("WORKER-0001", ["missing"])])

    assert result.status == RuntimeState.FAILED
    assert result.success is False
    assert result.messages == ["Plugin missing is not registered"]
