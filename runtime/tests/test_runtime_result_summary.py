from runtime import RuntimeEngine
from runtime.scheduler import WorkerCapability


def test_runtime_result_summary_counts_completed_run() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [
            {"id": "NODE-0001", "plugin": "generic", "action": "prepare"},
            {"id": "NODE-0002", "plugin": "generic", "action": "package", "depends_on": "NODE-0001"},
        ],
    }

    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])

    assert result.summary()["plan_nodes"] == 2
    assert result.summary()["plan_stages"] == 2
    assert result.summary()["scheduled_assignments"] == 2
    assert result.summary()["unscheduled_nodes"] == 0
    assert result.summary()["node_results"] == 2
    assert result.summary()["events"] == 5
    assert result.to_dict()["summary"] == result.summary()


def test_runtime_result_summary_counts_partial_schedule() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}],
    }

    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])

    assert result.summary()["plan_nodes"] == 1
    assert result.summary()["scheduled_assignments"] == 0
    assert result.summary()["unscheduled_nodes"] == 1
    assert result.summary()["node_results"] == 0
    assert result.to_dict()["summary"] == result.summary()
