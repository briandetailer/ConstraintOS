from runtime import RuntimeEngine
from runtime.scheduler import WorkerCapability


def test_runtime_engine_builds_execution_request_with_node_inputs() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [
            {
                "id": "NODE-0001",
                "plugin": "generic",
                "action": "package",
                "inputs": {"source": "demo"},
                "outputs": ["bundle.zip"],
            }
        ],
    }

    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])

    assert result.execution is not None
    assert result.execution["node_results"][0]["node_id"] == "NODE-0001"
    assert result.success is True
