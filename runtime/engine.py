from __future__ import annotations

from typing import Any

from runtime.artifacts import ArtifactCollector, ArtifactStore
from runtime.context import RuntimeContext
from runtime.events import RuntimeEvent, RuntimeEventType
from runtime.execution import DryRunExecutor, ExecutionRequest, RuntimeExecutor
from runtime.planner import DependencyResolver, RuntimePlanner
from runtime.result import RuntimeResult
from runtime.scheduler import RuntimeScheduler, WorkerCapability
from runtime.state import RuntimeState


class RuntimeEngine:
    """Coordinates planning, scheduling, execution, and artifact collection for a runtime job."""

    def __init__(
        self,
        planner: RuntimePlanner | None = None,
        scheduler: RuntimeScheduler | None = None,
        executor: RuntimeExecutor | None = None,
        resolver: DependencyResolver | None = None,
        artifact_store: ArtifactStore | None = None,
        artifact_collector: ArtifactCollector | None = None,
    ) -> None:
        self.planner = planner or RuntimePlanner()
        self.scheduler = scheduler or RuntimeScheduler()
        self.executor = executor or DryRunExecutor()
        self.resolver = resolver or DependencyResolver()
        self.artifact_store = artifact_store or ArtifactStore()
        self.artifact_collector = artifact_collector or ArtifactCollector(self.artifact_store)

    def _execution_assignments(self, plan_data: dict[str, Any], schedule_data: dict[str, Any]) -> list[dict[str, Any]]:
        nodes = {node.get("id"): node for node in plan_data.get("nodes", []) if isinstance(node, dict)}
        assignments: list[dict[str, Any]] = []
        for assignment in schedule_data.get("assignments", []):
            if not isinstance(assignment, dict):
                continue
            node = nodes.get(assignment.get("node_id"), {})
            enriched = dict(assignment)
            if isinstance(node, dict):
                enriched["inputs"] = node.get("inputs", {})
                enriched["outputs"] = node.get("outputs", [])
            assignments.append(enriched)
        return assignments

    def run(
        self,
        specification: dict[str, Any],
        workers: list[WorkerCapability | dict[str, Any]],
        context: RuntimeContext | None = None,
        runtime_id: str = "RUNTIME-0001",
    ) -> RuntimeResult:
        context = context or RuntimeContext()
        events: list[RuntimeEvent] = [
            RuntimeEvent(
                RuntimeEventType.STARTED,
                {"runtime_id": runtime_id, "context": context.to_dict()},
            )
        ]
        plan_data: dict[str, Any] | None = None
        schedule_data: dict[str, Any] | None = None
        execution_data: dict[str, Any] | None = None
        artifact_data: dict[str, Any] | None = None

        try:
            plan = self.planner.build(specification)
            self.resolver.validate(plan)
            plan_data = plan.to_dict()
            events.append(RuntimeEvent(RuntimeEventType.PLANNED, {"plan_id": plan.id}))

            schedule = self.scheduler.schedule(plan, workers)
            schedule_data = schedule.to_dict()
            events.append(RuntimeEvent(RuntimeEventType.SCHEDULED, {"schedule_id": schedule.id, "status": schedule.status}))

            if schedule.unscheduled_nodes:
                events.append(
                    RuntimeEvent(
                        RuntimeEventType.FAILED,
                        {"unscheduled_nodes": schedule.unscheduled_nodes},
                    )
                )
                return RuntimeResult(
                    id=runtime_id,
                    status=RuntimeState.PARTIAL,
                    success=False,
                    plan=plan_data,
                    schedule=schedule_data,
                    execution=None,
                    artifacts=artifact_data,
                    events=events,
                    messages=["Runtime schedule contains unscheduled nodes; execution was not started."],
                )

            events.append(RuntimeEvent(RuntimeEventType.EXECUTION_STARTED, {"schedule_id": schedule.id}))
            request = ExecutionRequest(
                id="EXEC-REQ-0001",
                schedule_id=schedule.id,
                assignments=self._execution_assignments(plan_data, schedule_data),
                dry_run=True,
            )
            execution = self.executor.execute(request, context=context)
            execution_data = execution.to_dict()
            self.artifact_collector.collect_from_execution(execution)
            artifact_data = self.artifact_store.to_dict()

            status = RuntimeState.COMPLETED if execution.status == "complete" else RuntimeState.PARTIAL
            success = status == RuntimeState.COMPLETED
            events.append(RuntimeEvent(RuntimeEventType.COMPLETED, {"execution_result_id": execution.id, "status": execution.status}))
            return RuntimeResult(
                id=runtime_id,
                status=status,
                success=success,
                plan=plan_data,
                schedule=schedule_data,
                execution=execution_data,
                artifacts=artifact_data,
                events=events,
                messages=["Runtime completed successfully." if success else "Runtime completed with partial execution."],
            )
        except Exception as error:  # pragma: no cover - defensive orchestration boundary
            events.append(RuntimeEvent(RuntimeEventType.FAILED, {"error": str(error)}))
            return RuntimeResult(
                id=runtime_id,
                status=RuntimeState.FAILED,
                success=False,
                plan=plan_data,
                schedule=schedule_data,
                execution=execution_data,
                artifacts=artifact_data,
                events=events,
                messages=[str(error)],
            )
