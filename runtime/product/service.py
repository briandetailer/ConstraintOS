from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Mapping

from runtime.research_to_render import (
    ConstraintRequest,
    OpenAIWebDiscoveryProvider,
    ResearchToRenderOrchestrator,
)

from .intake import IntakeError, OpenAIConstraintIntakeProvider, normalize_explicit_request
from .models import ImageJob
from .store import FileJobStore, JobStoreError


class ProductServiceError(RuntimeError):
    pass


DiscoveryFactory = Callable[[], OpenAIWebDiscoveryProvider]


class ConstraintOSProductService:
    def __init__(
        self,
        store: FileJobStore,
        *,
        intake_provider: OpenAIConstraintIntakeProvider | None = None,
        discovery_provider_factory: DiscoveryFactory | None = None,
        orchestrator: ResearchToRenderOrchestrator | None = None,
    ) -> None:
        self.store = store
        self.intake_provider = intake_provider
        self.discovery_provider_factory = discovery_provider_factory
        self.orchestrator = orchestrator or ResearchToRenderOrchestrator()

    def create_job(
        self,
        payload: Mapping[str, Any],
        *,
        run_research: bool = False,
    ) -> ImageJob:
        request_text = str(payload.get("request_text", "")).strip()
        title = str(payload.get("title", "")).strip() or None
        requested_job_id = str(payload.get("job_id", "")).strip() or None
        try:
            job = self.store.create(
                request_text=request_text,
                title=title,
                requested_job_id=requested_job_id,
            )
            self.store.write_artifact(
                job.job_id,
                "submitted-request.json",
                dict(payload),
                artifact_key="submitted_request",
            )
            job = self.compile_constraints(job.job_id, payload)
            if job.status == "needs_clarification":
                return job
            job = self.plan_research(job.job_id)
            if run_research:
                job = self.run_research(job.job_id)
            return job
        except (JobStoreError, IntakeError, ValueError, TypeError) as exc:
            if "job" in locals():
                self._fail_job(job.job_id, "request_intake", exc)
            raise ProductServiceError(str(exc)) from exc

    def compile_constraints(
        self,
        job_id: str,
        payload: Mapping[str, Any] | None = None,
    ) -> ImageJob:
        job = self.store.load(job_id)
        source_payload = dict(payload or {})
        if not source_payload:
            submitted_path = job.artifacts.get("submitted_request")
            if not submitted_path:
                raise ProductServiceError("The job has no submitted request artifact.")
            source_payload = json.loads(Path(submitted_path).read_text(encoding="utf-8-sig"))
        self.store.update(
            job_id,
            status="running",
            current_stage="constraint_compilation",
            error=None,
        )
        self.store.append_event(
            job_id,
            stage="constraint_compilation",
            event_type="stage_started",
            message="Compiling the request into executable image constraints.",
        )
        try:
            has_explicit_subject = bool(str(source_payload.get("subject", "")).strip())
            raw_constraints = source_payload.get("constraints", {})
            explicit_features = source_payload.get("required_visible_features")
            if isinstance(raw_constraints, Mapping) and not explicit_features:
                explicit_features = raw_constraints.get("required_visible_features")
            if has_explicit_subject and explicit_features:
                request_payload = normalize_explicit_request(
                    job_id,
                    job.request_text,
                    source_payload,
                )
            else:
                provider = self.intake_provider or OpenAIConstraintIntakeProvider()
                request_payload = provider.compile(job_id, job.request_text)

            request_path = self.store.write_artifact(
                job_id,
                "request.json",
                request_payload,
                artifact_key="normalized_request",
            )
            request = ConstraintRequest.from_payload(request_payload)
            intake = request_payload.get("intake", {})
            assumptions = [str(item) for item in intake.get("assumptions", [])]
            unresolved = [str(item) for item in intake.get("unresolved_questions", [])]
            allow_unresolved = bool(source_payload.get("allow_unresolved_questions", False))
            status = "needs_clarification" if unresolved and not allow_unresolved else "constraints_ready"
            current_stage = "clarification" if status == "needs_clarification" else "research_planning"
            blockers = tuple(f"clarification_required:{item}" for item in unresolved)
            warnings = tuple(f"assumption:{item}" for item in assumptions)
            updated = self.store.update(
                job_id,
                status=status,
                current_stage=current_stage,
                subject=request.subject,
                blockers=blockers,
                warnings=warnings,
                error=None,
            )
            self.store.append_event(
                job_id,
                stage="constraint_compilation",
                event_type="stage_completed",
                message="Executable image constraints compiled.",
                data={
                    "request_artifact": str(request_path),
                    "subject": request.subject,
                    "required_feature_count": len(request.required_visible_features),
                    "assumption_count": len(assumptions),
                    "unresolved_question_count": len(unresolved),
                },
            )
            return updated
        except Exception as exc:
            self._fail_job(job_id, "constraint_compilation", exc)
            raise

    def plan_research(self, job_id: str) -> ImageJob:
        job = self.store.load(job_id)
        if job.status == "needs_clarification":
            raise ProductServiceError("Resolve the job's clarification blockers before research planning.")
        request = self._load_request(job)
        self.store.update(
            job_id,
            status="running",
            current_stage="research_planning",
            error=None,
        )
        self.store.append_event(
            job_id,
            stage="research_planning",
            event_type="stage_started",
            message="Building request-derived research queries and stop conditions.",
        )
        try:
            plan = self.orchestrator.build_research_plan(request)
            path = self.store.write_artifact(
                job_id,
                "research-plan.json",
                plan.to_dict(),
                artifact_key="research_plan",
            )
            updated = self.store.update(
                job_id,
                status="research_ready",
                current_stage="source_discovery",
                blockers=(),
                error=None,
            )
            self.store.append_event(
                job_id,
                stage="research_planning",
                event_type="stage_completed",
                message="Research plan created.",
                data={"artifact": str(path), "query_count": len(plan.queries)},
            )
            return updated
        except Exception as exc:
            self._fail_job(job_id, "research_planning", exc)
            raise ProductServiceError(str(exc)) from exc

    def run_research(self, job_id: str) -> ImageJob:
        job = self.store.load(job_id)
        if job.status not in {"research_ready", "research_failed", "reference_preparation_required"}:
            raise ProductServiceError(
                f"Job {job_id} cannot run research from status {job.status}."
            )
        request = self._load_request(job)
        research_plan = self.orchestrator.build_research_plan(request)
        self.store.update(
            job_id,
            status="running",
            current_stage="source_discovery",
            error=None,
        )
        self.store.append_event(
            job_id,
            stage="source_discovery",
            event_type="stage_started",
            message="Searching for authoritative visual, geometry, and documentation sources.",
        )
        try:
            provider = (
                self.discovery_provider_factory()
                if self.discovery_provider_factory is not None
                else OpenAIWebDiscoveryProvider()
            )
            sources = provider.discover(request, research_plan)
            sources_payload = [source.to_dict() for source in sources]
            sources_path = self.store.write_artifact(
                job_id,
                "discovered-sources.json",
                sources_payload,
                artifact_key="discovered_sources",
            )
            result = self.orchestrator.orchestrate(request, sources)
            orchestration_payload = result.to_dict()
            orchestration_payload["discovery"] = dict(provider.last_manifest)
            orchestration_path = self.store.write_artifact(
                job_id,
                "orchestration.json",
                orchestration_payload,
                artifact_key="orchestration",
            )
            if result.status == "blocked":
                status = "blocked"
                current_stage = "source_evaluation"
                blockers = tuple(
                    [
                        *(
                            f"unsupported_feature:{item}"
                            for item in result.source_evaluation.unsupported_required_features
                        ),
                        *result.render_plan.preflight_blockers,
                    ]
                )
            else:
                status = "reference_preparation_required"
                current_stage = "reference_preparation"
                blockers = tuple(result.render_plan.preflight_blockers)
            updated = self.store.update(
                job_id,
                status=status,
                current_stage=current_stage,
                blockers=tuple(dict.fromkeys(blockers)),
                error=None,
            )
            self.store.append_event(
                job_id,
                stage="source_discovery",
                event_type="stage_completed",
                message="Source discovery and render-strategy selection completed.",
                data={
                    "source_count": len(sources),
                    "selected_source_count": len(result.selected_sources),
                    "production_mode": result.render_plan.production_mode,
                    "job_status": status,
                    "sources_artifact": str(sources_path),
                    "orchestration_artifact": str(orchestration_path),
                },
            )
            return updated
        except Exception as exc:
            self._fail_job(job_id, "source_discovery", exc, status="research_failed")
            raise ProductServiceError(str(exc)) from exc

    def resume_after_clarification(
        self,
        job_id: str,
        structured_request: Mapping[str, Any],
        *,
        run_research: bool = False,
    ) -> ImageJob:
        job = self.store.load(job_id)
        if job.status != "needs_clarification":
            raise ProductServiceError("Only needs_clarification jobs can be resumed this way.")
        submitted = dict(structured_request)
        submitted["request_text"] = job.request_text
        self.store.write_artifact(
            job_id,
            "submitted-request.json",
            submitted,
            artifact_key="submitted_request",
        )
        updated = self.compile_constraints(job_id, submitted)
        if updated.status == "needs_clarification":
            return updated
        updated = self.plan_research(job_id)
        if run_research:
            updated = self.run_research(job_id)
        return updated

    def get_job(self, job_id: str, *, include_events: bool = False) -> dict[str, Any]:
        job = self.store.load(job_id)
        payload = job.to_dict()
        if include_events:
            payload["events"] = [event.to_dict() for event in self.store.read_events(job_id)]
        return payload

    def list_jobs(self, *, limit: int = 100) -> list[dict[str, Any]]:
        return [job.to_dict() for job in self.store.list_jobs(limit=limit)]

    def _load_request(self, job: ImageJob) -> ConstraintRequest:
        request_path = job.artifacts.get("normalized_request")
        if not request_path:
            raise ProductServiceError("The job has no normalized request artifact.")
        payload = json.loads(Path(request_path).read_text(encoding="utf-8-sig"))
        return ConstraintRequest.from_payload(payload)

    def _fail_job(
        self,
        job_id: str,
        stage: str,
        exc: Exception,
        *,
        status: str = "failed",
    ) -> None:
        message = str(exc) or exc.__class__.__name__
        self.store.update(
            job_id,
            status=status,
            current_stage=stage,
            error=message,
            approval_allowed=False,
            production_ready=False,
        )
        self.store.append_event(
            job_id,
            stage=stage,
            event_type="stage_failed",
            message=message,
            data={"exception_type": exc.__class__.__name__},
        )
