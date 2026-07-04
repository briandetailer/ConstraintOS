from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SUPPORTED_CONSTRAINT_TYPES = {
    "semantic",
    "geometric",
    "topological",
    "visual",
    "stylistic",
    "publishing",
    "evidence",
    "negative",
    "workflow",
}


@dataclass
class CompileResult:
    renderer: str
    artifact_id: str
    instruction: str
    unsupported_constraints: list[dict[str, Any]]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "renderer": self.renderer,
            "artifact_id": self.artifact_id,
            "instruction": self.instruction,
            "unsupported_constraints": self.unsupported_constraints,
            "warnings": self.warnings,
        }


def compile_to_text(spec: dict[str, Any], renderer: str = "generic") -> CompileResult:
    artifact = spec.get("artifact", {})
    subject = spec.get("subject", {})
    view = spec.get("view", {})
    constraints = spec.get("constraints", []) or []
    renderer_config = spec.get("renderer", {})

    artifact_id = str(artifact.get("id", "UNKNOWN"))
    lines: list[str] = []
    warnings: list[str] = []
    unsupported: list[dict[str, Any]] = []

    lines.append(f"Renderer target: {renderer}")
    lines.append(f"Artifact: {artifact_id} - {artifact.get('title', '')}")
    lines.append(f"Artifact type: {artifact.get('type', '')}")
    lines.append("")

    if subject:
        lines.append("SUBJECT")
        for key, value in subject.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    if view:
        lines.append("VIEW")
        lines.append(str(view))
        lines.append("")

    if renderer_config:
        lines.append("RENDERER PROFILE")
        for key, value in renderer_config.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    lines.append("CONSTRAINTS")
    for constraint in constraints:
        constraint_type = constraint.get("type", "semantic")
        if constraint_type not in SUPPORTED_CONSTRAINT_TYPES:
            unsupported.append(constraint)
            continue
        lines.append(f"- {constraint.get('id')}: {constraint.get('statement')}")
        lines.append(f"  severity: {constraint.get('severity')}")
        lines.append(f"  acceptance: {constraint.get('acceptance')}")

    if not constraints:
        warnings.append("Specification has no constraints.")

    if unsupported:
        warnings.append("One or more constraints used unsupported constraint types.")

    lines.append("")
    lines.append("Do not invent unsupported details. If a detail is not specified, keep it neutral or omit it.")
    lines.append("Preserve all blocker constraints. Report ambiguity rather than guessing.")

    return CompileResult(
        renderer=renderer,
        artifact_id=artifact_id,
        instruction="\n".join(lines),
        unsupported_constraints=unsupported,
        warnings=warnings,
    )
