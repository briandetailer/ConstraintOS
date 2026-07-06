from runtime.planner import RuntimePlanner
from runtime.scheduler import RuntimeScheduler, WorkerCapability


def test_schedule_single_node() -> None:
    plan = RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}]})
    result = RuntimeScheduler().schedule(plan, [WorkerCapability("WORKER-0001", ["blender"])])
    data = result.to_dict()
    assert data["schedule_result"]["status"] == "scheduled"
    assert data["assignments"][0]["worker_id"] == "WORKER-0001"


def test_schedule_uses_deterministic_worker_order() -> None:
    plan = RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}]})
    result = RuntimeScheduler().schedule(
        plan,
        [
            WorkerCapability("WORKER-0002", ["blender"]),
            WorkerCapability("WORKER-0001", ["blender"]),
        ],
    )
    assert result.assignments[0].worker_id == "WORKER-0001"


def test_schedule_reports_missing_worker_capability() -> None:
    plan = RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "plugin": "freecad", "action": "model"}]})
    result = RuntimeScheduler().schedule(plan, [WorkerCapability("WORKER-0001", ["blender"])])
    data = result.to_dict()
    assert data["schedule_result"]["status"] == "partial"
    assert data["unscheduled_nodes"] == ["NODE-0001"]


def test_schedule_accepts_dict_workers() -> None:
    plan = RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "package"}]})
    result = RuntimeScheduler().schedule(plan, [{"worker_id": "WORKER-0001", "plugins": ["generic"], "status": "available"}])
    assert result.to_dict()["assignments"][0]["worker_id"] == "WORKER-0001"


def test_busy_worker_is_not_selected() -> None:
    plan = RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}]})
    result = RuntimeScheduler().schedule(plan, [WorkerCapability("WORKER-0001", ["blender"], status="busy")])
    assert result.to_dict()["schedule_result"]["status"] == "partial"


def test_scheduler_does_not_double_book_workers_within_same_stage() -> None:
    plan = RuntimePlanner().build(
        {
            "execution_steps": [
                {"id": "NODE-0001", "plugin": "blender", "action": "render"},
                {"id": "NODE-0002", "plugin": "blender", "action": "render"},
            ]
        }
    )
    result = RuntimeScheduler().schedule(
        plan,
        [
            WorkerCapability("WORKER-0001", ["blender"]),
            WorkerCapability("WORKER-0002", ["blender"]),
        ],
    )

    assert result.status == "scheduled"
    assert [assignment.worker_id for assignment in result.assignments] == ["WORKER-0001", "WORKER-0002"]


def test_scheduler_marks_concurrent_node_unscheduled_when_stage_capacity_is_exceeded() -> None:
    plan = RuntimePlanner().build(
        {
            "execution_steps": [
                {"id": "NODE-0001", "plugin": "blender", "action": "render"},
                {"id": "NODE-0002", "plugin": "blender", "action": "render"},
            ]
        }
    )
    result = RuntimeScheduler().schedule(plan, [WorkerCapability("WORKER-0001", ["blender"])])

    assert result.status == "partial"
    assert [assignment.node_id for assignment in result.assignments] == ["NODE-0001"]
    assert result.unscheduled_nodes == ["NODE-0002"]


def test_scheduler_allows_worker_reuse_across_sequential_stages() -> None:
    plan = RuntimePlanner().build(
        {
            "execution_steps": [
                {"id": "NODE-0001", "plugin": "blender", "action": "render"},
                {"id": "NODE-0002", "plugin": "blender", "action": "render", "depends_on": "NODE-0001"},
            ]
        }
    )
    result = RuntimeScheduler().schedule(plan, [WorkerCapability("WORKER-0001", ["blender"])])

    assert result.status == "scheduled"
    assert [assignment.worker_id for assignment in result.assignments] == ["WORKER-0001", "WORKER-0001"]
    assert [assignment.stage_id for assignment in result.assignments] == ["STAGE-0001", "STAGE-0002"]
