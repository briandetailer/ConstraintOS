from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

from runtime.planner.models import ExecutionPlan


class DependencyResolutionError(ValueError):
    """Raised when plan dependencies cannot be resolved safely."""


class DependencyResolver:
    """Validates execution-plan dependency integrity before scheduling."""

    def validate(self, plan: ExecutionPlan | dict[str, Any]) -> None:
        plan_data = plan.to_dict() if isinstance(plan, ExecutionPlan) else plan
        nodes = plan_data.get("nodes", [])
        dependencies = plan_data.get("dependencies", [])

        if not isinstance(nodes, list):
            raise DependencyResolutionError("nodes must be a list")
        if not isinstance(dependencies, list):
            raise DependencyResolutionError("dependencies must be a list")

        node_ids = self._node_ids(nodes)
        self._validate_dependency_references(node_ids, dependencies)
        self._validate_acyclic(node_ids, dependencies)

    def ordered_node_ids(self, plan: ExecutionPlan | dict[str, Any]) -> list[str]:
        plan_data = plan.to_dict() if isinstance(plan, ExecutionPlan) else plan
        nodes = plan_data.get("nodes", [])
        dependencies = plan_data.get("dependencies", [])
        if not isinstance(nodes, list):
            raise DependencyResolutionError("nodes must be a list")
        if not isinstance(dependencies, list):
            raise DependencyResolutionError("dependencies must be a list")

        node_ids = self._node_ids(nodes)
        self._validate_dependency_references(node_ids, dependencies)

        incoming_count = {node_id: 0 for node_id in node_ids}
        children: dict[str, list[str]] = defaultdict(list)
        for dependency in dependencies:
            node_id = str(dependency.get("node_id"))
            depends_on = str(dependency.get("depends_on"))
            incoming_count[node_id] += 1
            children[depends_on].append(node_id)

        ready = deque(sorted(node_id for node_id, count in incoming_count.items() if count == 0))
        ordered: list[str] = []
        while ready:
            node_id = ready.popleft()
            ordered.append(node_id)
            for child in sorted(children[node_id]):
                incoming_count[child] -= 1
                if incoming_count[child] == 0:
                    ready.append(child)

        if len(ordered) != len(node_ids):
            raise DependencyResolutionError("Circular dependency detected")
        return ordered

    def _node_ids(self, nodes: list[dict[str, Any]]) -> set[str]:
        node_ids: set[str] = set()
        for index, node in enumerate(nodes, start=1):
            if not isinstance(node, dict):
                raise DependencyResolutionError(f"Invalid node shape at index {index}")
            node_id = node.get("id")
            if not node_id:
                raise DependencyResolutionError(f"Missing node id at index {index}")
            node_id = str(node_id)
            if node_id in node_ids:
                raise DependencyResolutionError(f"Duplicate node id {node_id}")
            node_ids.add(node_id)
        return node_ids

    def _validate_dependency_references(self, node_ids: set[str], dependencies: list[dict[str, Any]]) -> None:
        for index, dependency in enumerate(dependencies, start=1):
            if not isinstance(dependency, dict):
                raise DependencyResolutionError(f"Invalid dependency shape at index {index}")
            node_id = str(dependency.get("node_id"))
            depends_on = str(dependency.get("depends_on"))
            if node_id not in node_ids:
                raise DependencyResolutionError(f"Unknown dependency node {node_id}")
            if depends_on not in node_ids:
                raise DependencyResolutionError(f"Unknown dependency target {depends_on}")
            if node_id == depends_on:
                raise DependencyResolutionError(f"Node {node_id} cannot depend on itself")

    def _validate_acyclic(self, node_ids: set[str], dependencies: list[dict[str, Any]]) -> None:
        self.ordered_node_ids({"nodes": [{"id": node_id} for node_id in sorted(node_ids)], "dependencies": dependencies})
