from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from constraintos.repair_loop import dry_run_repair_loop


@dataclass
class VolumePlate:
    id: str
    title: str
    specification_path: str
    sequence: int

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


def create_volume_plan(volume_id: str, title: str, plates: list[dict[str, Any]], max_iterations: int = 3) -> dict[str, Any]:
    ordered = sorted(plates, key=lambda item: item.get("sequence", 0))
    return {
        "volume_plan": {
            "id": volume_id,
            "title": title,
            "created": date.today().isoformat(),
            "status": "draft",
            "max_iterations_per_plate": max_iterations,
        },
        "plates": ordered,
        "build_policy": {
            "stop_on_blocked_plate": True,
            "require_review_gate_pass": True,
            "renderer_mode": "dry-run",
        },
    }


def run_volume_dry_build(volume_plan: dict[str, Any], specs_by_artifact_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    blocked = False
    for plate in volume_plan.get("plates", []) or []:
        artifact_id = str(plate.get("id"))
        spec = specs_by_artifact_id.get(artifact_id)
        if spec is None:
            results.append({"artifact_id": artifact_id, "status": "blocked", "reason": "missing specification", "iterations": []})
            blocked = True
            if volume_plan.get("build_policy", {}).get("stop_on_blocked_plate", True):
                break
            continue
        loop_result = dry_run_repair_loop(spec, max_iterations=volume_plan.get("volume_plan", {}).get("max_iterations_per_plate", 3))
        results.append({"artifact_id": artifact_id, "status": loop_result.get("status"), "reason": "dry-run completed", "iterations": loop_result.get("iterations", [])})
        if loop_result.get("status") == "blocked":
            blocked = True
            if volume_plan.get("build_policy", {}).get("stop_on_blocked_plate", True):
                break
    return {
        "volume_build": {
            "id": f"BUILD-{volume_plan.get('volume_plan', {}).get('id', 'VOLUME')}",
            "volume_id": volume_plan.get("volume_plan", {}).get("id"),
            "created": date.today().isoformat(),
            "status": "blocked" if blocked else "complete",
        },
        "results": results,
        "summary": {
            "total": len(volume_plan.get("plates", []) or []),
            "processed": len(results),
            "blocked": sum(1 for item in results if item.get("status") == "blocked"),
            "complete": sum(1 for item in results if item.get("status") in {"pass", "needs_iteration"}),
        },
    }


def create_volume_completion_report(volume_build: dict[str, Any]) -> dict[str, Any]:
    summary = volume_build.get("summary", {})
    return {
        "volume_completion_report": {
            "id": f"REPORT-{volume_build.get('volume_build', {}).get('id', 'UNKNOWN')}",
            "volume_id": volume_build.get("volume_build", {}).get("volume_id"),
            "created": date.today().isoformat(),
            "status": volume_build.get("volume_build", {}).get("status"),
        },
        "summary": summary,
        "recommendation": "proceed" if summary.get("blocked", 0) == 0 else "resolve_blockers",
    }
