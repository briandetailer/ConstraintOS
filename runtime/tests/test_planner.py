import pytest

from runtime.planner import PlanningError, RuntimePlanner


def test_empty_specification_builds_empty_plan() -> None:
    plan = RuntimePlanner().build({})
    data = plan.to_dict()
    assert data["execution_plan"]["status"] == "planned"
    assert data["nodes"] == []
    assert data["stages"] == []


def test_single_stage_plan_from_artifact() -> None:
    plan = RuntimePlanner().build({"artifact": {"id": "SPEC-0001", "title": "Example"}})
    data = plan.to_dict()
    assert data["execution_plan"]["source_id"] == "SPEC-0001"
    assert data["required_plugins"] == ["generic"]
    assert data["stages"][0]["node_ids"] == ["NODE-0001"]


def test_multi_stage_dependency_graph() -> None:
    plan = RuntimePlanner().build(
        {
            "artifact": {"id": "SPEC-0002"},
            "execution_steps": [
                {"id": "NODE-0001", "plugin": "blender", "action": "render"},
                {"id": "NODE-0002", "plugin": "illustrator", "action": "vectorize", "depends_on": ["NODE-0001"]},
                {"id": "NODE-0003", "plugin": "generic", "action": "package", "depends_on": ["NODE-0002"]},
            ],
        }
    )
    data = plan.to_dict()
    assert [stage["node_ids"] for stage in data["stages"]] == [["NODE-0001"], ["NODE-0002"], ["NODE-0003"]]
    assert data["required_plugins"] == ["blender", "generic", "illustrator"]


def test_parallel_stage_grouping() -> None:
    plan = RuntimePlanner().build(
        {
            "artifact": {"id": "SPEC-0003"},
            "execution_steps": [
                {"id": "NODE-0001", "plugin": "blender", "action": "render_front"},
                {"id": "NODE-0002", "plugin": "blender", "action": "render_side"},
                {"id": "NODE-0003", "plugin": "generic", "action": "package", "depends_on": ["NODE-0001", "NODE-0002"]},
            ],
        }
    )
    data = plan.to_dict()
    assert data["stages"][0]["node_ids"] == ["NODE-0001", "NODE-0002"]
    assert data["stages"][1]["node_ids"] == ["NODE-0003"]


def test_missing_plugin_detection() -> None:
    with pytest.raises(PlanningError, match="Missing plugin"):
        RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "action": "render"}]})


def test_unknown_dependency_detection() -> None:
    with pytest.raises(PlanningError, match="Unknown dependency"):
        RuntimePlanner().build({"execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render", "depends_on": ["NODE-9999"]}]})


def test_circular_dependency_detection() -> None:
    with pytest.raises(PlanningError, match="Circular dependency"):
        RuntimePlanner().build(
            {
                "execution_steps": [
                    {"id": "NODE-0001", "plugin": "a", "action": "one", "depends_on": ["NODE-0002"]},
                    {"id": "NODE-0002", "plugin": "b", "action": "two", "depends_on": ["NODE-0001"]},
                ]
            }
        )
