from __future__ import annotations

from typing import Any

from runtime.planner.models import ExecutionPlan
from runtime.scheduler.models import ScheduleResult, ScheduledAssignment, WorkerCapability


class SchedulingError(ValueError):
    """Raised when a schedule cannot be created."""


class RuntimeScheduler:
    def schedule(
        self,
        plan: ExecutionPlan | dict[str, Any],
        workers: list[WorkerCapability | dict[str, Any]],
        schedule_id: str = "SCHEDULE-0001",
    ) -> ScheduleResult:
        plan_data = plan.to_dict() if isinstance(plan, ExecutionPlan) else plan
        plan_id = plan_data.get("execution_plan", {}).get("id", "UNKNOWN-PLAN")
        nodes = {node["id"]: node for node in plan_data.get("nodes", [])}
        stages = plan_data.get("stages", [])
        worker_pool = [self._worker_from_input(worker) for worker in workers]
        assignments: list[ScheduledAssignment] = []
        unscheduled: list[str] = []
        for stage in stages:
            stage_id = stage.get("id", "UNKNOWN-STAGE")
            reserved_workers: set[str] = set()
            for node_id in stage.get("node_ids", []):
                node = nodes.get(node_id)
                if not node:
                    unscheduled.append(str(node_id))
                    continue
                worker = self._select_worker(str(node.get("plugin")), worker_pool, reserved_workers)
                if worker is None:
                    unscheduled.append(str(node_id))
                    continue
                reserved_workers.add(worker.worker_id)
                assignments.append(
                    ScheduledAssignment(
                        node_id=str(node_id),
                        stage_id=str(stage_id),
                        worker_id=worker.worker_id,
                        plugin=str(node.get("plugin")),
                        action=str(node.get("action")),
                    )
                )
        status = "scheduled" if not unscheduled else "partial"
        return ScheduleResult(
            id=schedule_id,
            plan_id=plan_id,
            status=status,
            assignments=assignments,
            unscheduled_nodes=unscheduled,
            messages=["Schedule built successfully." if status == "scheduled" else "Schedule contains unscheduled nodes."],
        )

    def _worker_from_input(self, worker: WorkerCapability | dict[str, Any]) -> WorkerCapability:
        if isinstance(worker, WorkerCapability):
            return worker
        return WorkerCapability(
            worker_id=str(worker.get("worker_id", "UNKNOWN-WORKER")),
            plugins=list(worker.get("plugins", [])),
            status=str(worker.get("status", "available")),
        )

    def _select_worker(self, plugin: str, workers: list[WorkerCapability], reserved_workers: set[str] | None = None) -> WorkerCapability | None:
        reserved = reserved_workers or set()
        candidates = [worker for worker in workers if worker.worker_id not in reserved and worker.supports(plugin)]
        if not candidates:
            return None
        return sorted(candidates, key=lambda worker: worker.worker_id)[0]
