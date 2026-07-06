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

    def _execution_request_from_schedule(
        self,
        plan_data: dict[str, Any],
        schedule_data: dict[str, Any],
        request_id: str = "EXEC-REQ-0001",
    ) -> ExecutionRequest:
        enriched_schedule = dict(schedule_data)
        enriched_schedule["assignments"] = self._execution_assignments(plan_data, schedule_data)
        return ExecutionRequest.from_schedule(enriched_schedule, request_id=request_id)

    def _runtime_execution_request_id(self, runtime_id: str) -> str:
        return f"{runtime_id}-EXEC-REQ-0001"

    def _runtime_execution_result_id(self, runtime_id: str) -> str:
        return f"{runtime_id}-EXEC-RESULT-0001"

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

            request = self._execution_request_from_schedule(
                plan_data,
                schedule_data,
                request_id=self._runtime_execution_request_id(runtime_id),
            )
            events.append(
                RuntimeEvent(
                    RuntimeEventType.EXECUTION_STARTED,
                    {"schedule_id": schedule.id, "execution_request_id": request.id},
                )
            )
            execution = self.executor.execute(
                request,
                context=context,
                result_id=self._runtime_execution_result_id(runtime_id),
            )
            execution_data = execution.to_dict()
            self.artifact_collector.collect_from_execution(execution)
            artifact_data = self.artifact_store.to_dict()

            status = RuntimeState.COMPLETED if execution.status == "complete" else RuntimeState.PARTIAL
            success = status == RuntimeState.COMPLETED
            artifact_count = artifact_data.get("artifact_store", {}).get("count", 0) if isinstance(artifact_data, dict) else 0
            events.append(
                RuntimeEvent(
                    RuntimeEventType.COMPLETED,
                    {
                        "execution_result_id": execution.id,
                        "status": execution.status,
                        "node_results": len(execution.node_results),
                        "artifacts": artifact_count,
                    },
                )
            )
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
