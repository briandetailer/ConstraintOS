from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ExecutionNode:
    id: str
    plugin: str
    action: str
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "plugin": self.plugin,
            "action": self.action,
            "inputs": self.inputs,
            "outputs": self.outputs,
        }


@dataclass(frozen=True)
class ExecutionDependency:
    node_id: str
    depends_on: str

    def to_dict(self) -> dict[str, str]:
        return {
            "node_id": self.node_id,
            "depends_on": self.depends_on,
        }


@dataclass(frozen=True)
class ExecutionStage:
    id: str
    node_ids: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "node_ids": self.node_ids,
        }


@dataclass(frozen=True)
class ExecutionPlan:
    id: str
    source_id: str
    status: str
    nodes: list[ExecutionNode]
    dependencies: list[ExecutionDependency]
    stages: list[ExecutionStage]
    required_plugins: list[str]
    messages: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_plan": {
                "id": self.id,
                "source_id": self.source_id,
                "status": self.status,
                "created": date.today().isoformat(),
            },
            "required_plugins": self.required_plugins,
            "stages": [stage.to_dict() for stage in self.stages],
            "nodes": [node.to_dict() for node in self.nodes],
            "dependencies": [dependency.to_dict() for dependency in self.dependencies],
            "messages": self.messages,
        }
