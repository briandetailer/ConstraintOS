from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from constraintos.compiler import compile_to_text
from constraintos.patching import create_patch_package
from constraintos.review import review_gate_status


@dataclass
class IterationRecord:
    iteration: int
    stage: str
    status: str
    artifact_id: str
    messages: list[str]
    outputs: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


def create_build_plan(plan_id: str, artifact_id: str, max_iterations: int = 3) -> dict[str, Any]:
    return {
        "build_plan": {
            "id": plan_id,
            "artifact_id": artifact_id,
            "created": date.today().isoformat(),
            "status": "draft",
            "max_iterations": max_iterations,
        },
        "stages": ["compile", "render", "validate", "review", "patch"],
        "stop_conditions": {
            "pass_review_gate": True,
            "max_iterations": max_iterations,
            "block_on_unsupported_constraints": True,
        },
    }


def create_iteration_record(iteration: int, stage: str, status: str, artifact_id: str, messages: list[str] | None = None, outputs: dict[str, Any] | None = None) -> dict[str, Any]:
    return IterationRecord(
        iteration=iteration,
        stage=stage,
        status=status,
        artifact_id=artifact_id,
        messages=messages or [],
        outputs=outputs or {},
    ).to_dict()


def dry_run_repair_loop(spec: dict[str, Any], compliance_report: dict[str, Any] | None = None, review_checklist: dict[str, Any] | None = None, max_iterations: int = 3) -> dict[str, Any]:
    artifact_id = str(spec.get("artifact", {}).get("id", "UNKNOWN"))
    plan = create_build_plan("BUILD-0001", artifact_id, max_iterations=max_iterations)
    iterations: list[dict[str, Any]] = []

    compile_result = compile_to_text(spec)
    iterations.append(
        create_iteration_record(
            1,
            "compile",
            "complete" if not compile_result.unsupported_constraints else "blocked",
            artifact_id,
            compile_result.warnings,
            {"unsupported_constraints": compile_result.unsupported_constraints},
        )
    )

    if compile_result.unsupported_constraints:
        return {"plan": plan, "status": "blocked", "iterations": iterations, "final_gate": None}

    iterations.append(create_iteration_record(1, "render", "dry_run", artifact_id, ["No live renderer called."], {"renderer": "dry-run"}))

    if compliance_report:
        failed_results = [item for item in compliance_report.get("constraint_results", []) or [] if item.get("result") in {"fail", "uncertain", "blocked_by_missing_evidence"}]
        status = "complete" if not failed_results else "needs_patch"
        iterations.append(create_iteration_record(1, "validate", status, artifact_id, [], {"failed_results": len(failed_results)}))
        if failed_results:
            patch = create_patch_package(compliance_report, "PATCH-0001")
            iterations.append(create_iteration_record(1, "patch", "created", artifact_id, [], {"patch_id": patch.patch_id, "failed_constraints": len(patch.failed_constraints)}))

    final_gate = None
    if review_checklist:
        final_gate = review_gate_status(review_checklist)
        iterations.append(create_iteration_record(1, "review", final_gate["gate"], artifact_id, [final_gate["reason"]], {"blocked_items": final_gate.get("blocked_items", [])}))

    final_status = "pass" if final_gate and final_gate.get("gate") == "pass" else "needs_iteration"
    return {"plan": plan, "status": final_status, "iterations": iterations, "final_gate": final_gate}
