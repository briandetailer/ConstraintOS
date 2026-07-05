import pytest

from runtime.planner import DependencyResolutionError, DependencyResolver, RuntimePlanner


def test_dependency_resolver_accepts_valid_plan() -> None:
    plan = RuntimePlanner().build(
        {
            "execution_steps": [
                {"id": "NODE-0001", "plugin": "generic", "action": "prepare"},
                {"id": "NODE-0002", "plugin": "generic", "action": "package", "depends_on": ["NODE-0001"]},
            ]
        }
    )

    resolver = DependencyResolver()

    resolver.validate(plan)
    assert resolver.ordered_node_ids(plan) == ["NODE-0001", "NODE-0002"]


def test_dependency_resolver_rejects_duplicate_node_ids() -> None:
    plan = {
        "nodes": [{"id": "NODE-0001"}, {"id": "NODE-0001"}],
        "dependencies": [],
    }

    with pytest.raises(DependencyResolutionError, match="Duplicate node id NODE-0001"):
        DependencyResolver().validate(plan)


def test_dependency_resolver_rejects_unknown_dependency_node() -> None:
    plan = {
        "nodes": [{"id": "NODE-0001"}],
        "dependencies": [{"node_id": "NODE-9999", "depends_on": "NODE-0001"}],
    }

    with pytest.raises(DependencyResolutionError, match="Unknown dependency node NODE-9999"):
        DependencyResolver().validate(plan)


def test_dependency_resolver_rejects_unknown_dependency_target() -> None:
    plan = {
        "nodes": [{"id": "NODE-0001"}],
        "dependencies": [{"node_id": "NODE-0001", "depends_on": "NODE-9999"}],
    }

    with pytest.raises(DependencyResolutionError, match="Unknown dependency target NODE-9999"):
        DependencyResolver().validate(plan)


def test_dependency_resolver_rejects_self_dependency() -> None:
    plan = {
        "nodes": [{"id": "NODE-0001"}],
        "dependencies": [{"node_id": "NODE-0001", "depends_on": "NODE-0001"}],
    }

    with pytest.raises(DependencyResolutionError, match="Node NODE-0001 cannot depend on itself"):
        DependencyResolver().validate(plan)


def test_dependency_resolver_rejects_circular_dependencies() -> None:
    plan = {
        "nodes": [{"id": "NODE-0001"}, {"id": "NODE-0002"}],
        "dependencies": [
            {"node_id": "NODE-0001", "depends_on": "NODE-0002"},
            {"node_id": "NODE-0002", "depends_on": "NODE-0001"},
        ],
    }

    with pytest.raises(DependencyResolutionError, match="Circular dependency detected"):
        DependencyResolver().validate(plan)
