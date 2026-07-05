from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

from runtime.planner.models import ExecutionDependency, ExecutionNode, ExecutionPlan, ExecutionStage


class PlanningError(ValueError):
    """Raised when a runtime plan cannot be constructed."""


class RuntimePlanner:
    def build(self, specification: dict[str, Any], plan_id: str = "PLAN-0001") -> ExecutionPlan:
        source_id = self._source_id(specification)
        raw_steps = self._extract_steps(specification)
        nodes = [self._node_from_step(index, step) for index, step in enumerate(raw_steps, start=1)]
        dependencies = self._dependencies_from_steps(nodes, raw_steps)
        self._validate_dependencies(nodes, dependencies)
        stages = self._build_stages(nodes, dependencies)
        required_plugins = sorted({node.plugin for node in nodes})
        return ExecutionPlan(
            id=plan_id,
            source_id=source_id,
            status="planned",
            nodes=nodes,
            dependencies=dependencies,
            stages=stages,
            required_plugins=required_plugins,
            messages=["Execution plan built successfully."],
        )

    def _source_id(self, specification: dict[str, Any]) -> str:
        for key in ("artifact", "specification", "runtime_job", "execution_request"):
            value = specification.get(key)
            if isinstance(value, dict) and value.get("id"):
                return str(value["id"])
        return "UNKNOWN-SOURCE"

    def _extract_steps(self, specification: dict[str, Any]) -> list[dict[str, Any]]:
        for key in ("execution_steps", "steps", "runtime_steps"):
            steps = specification.get(key)
            if isinstance(steps, list):
                return [step for step in steps if isinstance(step, dict)]
        render_job = specification.get("render_job")
        if isinstance(render_job, dict):
            plugin = render_job.get("renderer", render_job.get("plugin", "generic"))
            action = render_job.get("action", "render")
            return [{"id": "NODE-0001", "plugin": plugin, "action": action, "inputs": specification.get("payload", {})}]
        artifact = specification.get("artifact")
        if isinstance(artifact, dict):
            return [{"id": "NODE-0001", "plugin": "generic", "action": "process_artifact", "inputs": specification}]
        return []

    def _node_from_step(self, index: int, step: dict[str, Any]) -> ExecutionNode:
        plugin = step.get("plugin") or step.get("renderer")
        action = step.get("action")
        if not plugin:
            raise PlanningError(f"Missing plugin for step {index}")
        if not action:
            raise PlanningError(f"Missing action for step {index}")
        return ExecutionNode(
            id=str(step.get("id", f"NODE-{index:04d}")),
            plugin=str(plugin),
            action=str(action),
            inputs=step.get("inputs", {}) if isinstance(step.get("inputs", {}), dict) else {},
            outputs=step.get("outputs", []) if isinstance(step.get("outputs", []), list) else [],
        )

    def _dependencies_from_steps(self, nodes: list[ExecutionNode], steps: list[dict[str, Any]]) -> list[ExecutionDependency]:
        dependencies: list[ExecutionDependency] = []
        node_ids = {node.id for node in nodes}
        for node, step in zip(nodes, steps):
            raw_depends_on = step.get("depends_on", [])
            if isinstance(raw_depends_on, str):
                raw_depends_on = [raw_depends_on]
            if not isinstance(raw_depends_on, list):
                raise PlanningError(f"Invalid depends_on for node {node.id}")
            for dependency in raw_depends_on:
                dependency_id = str(dependency)
                if dependency_id not in node_ids:
                    raise PlanningError(f"Unknown dependency {dependency_id} for node {node.id}")
                dependencies.append(ExecutionDependency(node_id=node.id, depends_on=dependency_id))
        return dependencies

    def _validate_dependencies(self, nodes: list[ExecutionNode], dependencies: list[ExecutionDependency]) -> None:
        node_ids = {node.id for node in nodes}
        graph: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
        for dependency in dependencies:
            graph[dependency.depends_on].append(dependency.node_id)
        visited: set[str] = set()
        visiting: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in visiting:
                raise PlanningError("Circular dependency detected")
            if node_id in visited:
                return
            visiting.add(node_id)
            for child in graph[node_id]:
                visit(child)
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in sorted(node_ids):
            visit(node_id)

    def _build_stages(self, nodes: list[ExecutionNode], dependencies: list[ExecutionDependency]) -> list[ExecutionStage]:
        if not nodes:
            return []
        node_ids = [node.id for node in nodes]
        incoming_count = {node_id: 0 for node_id in node_ids}
        children: dict[str, list[str]] = defaultdict(list)
        for dependency in dependencies:
            incoming_count[dependency.node_id] += 1
            children[dependency.depends_on].append(dependency.node_id)
        ready = deque(sorted(node_id for node_id, count in incoming_count.items() if count == 0))
        stages: list[ExecutionStage] = []
        stage_number = 1
        processed: set[str] = set()
        while ready:
            current_stage = sorted(ready)
            ready.clear()
            stages.append(ExecutionStage(id=f"STAGE-{stage_number:04d}", node_ids=current_stage))
            stage_number += 1
            for node_id in current_stage:
                processed.add(node_id)
                for child in sorted(children[node_id]):
                    incoming_count[child] -= 1
                    if incoming_count[child] == 0:
                        ready.append(child)
        if len(processed) != len(nodes):
            raise PlanningError("Unable to build complete execution stages")
        return stages
