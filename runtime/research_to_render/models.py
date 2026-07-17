from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


def _tuple_of_strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value.strip(),) if value.strip() else ()
    if isinstance(value, (list, tuple, set)):
        return tuple(str(item).strip() for item in value if str(item).strip())
    raise TypeError(f"Expected a string collection, received {type(value).__name__}")


@dataclass(frozen=True)
class ConstraintRequest:
    request_id: str
    request_text: str
    subject: str
    output_kind: str
    viewpoint: str
    required_visible_features: tuple[str, ...]
    forbidden_features: tuple[str, ...]
    repeatability_required: bool
    authoritative_sources_required: bool
    labels_required: bool
    novel_view_requested: bool
    allow_exploratory_generation: bool
    manual_review_required: bool

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ConstraintRequest":
        constraints = payload.get("constraints", {})
        if not isinstance(constraints, Mapping):
            raise TypeError("constraints must be an object")
        request_id = str(payload.get("request_id", "")).strip()
        request_text = str(payload.get("request_text", "")).strip()
        subject = str(payload.get("subject", "")).strip()
        output_kind = str(payload.get("output_kind", "technical_illustration")).strip()
        viewpoint = str(payload.get("viewpoint", "unspecified")).strip()
        if not request_id:
            raise ValueError("request_id is required")
        if not request_text:
            raise ValueError("request_text is required")
        if not subject:
            raise ValueError("subject is required")
        required_visible_features = _tuple_of_strings(
            constraints.get("required_visible_features")
        )
        if not required_visible_features:
            raise ValueError("At least one required_visible_feature is required")
        return cls(
            request_id=request_id,
            request_text=request_text,
            subject=subject,
            output_kind=output_kind,
            viewpoint=viewpoint,
            required_visible_features=required_visible_features,
            forbidden_features=_tuple_of_strings(constraints.get("forbidden_features")),
            repeatability_required=bool(constraints.get("repeatability_required", True)),
            authoritative_sources_required=bool(
                constraints.get("authoritative_sources_required", True)
            ),
            labels_required=bool(constraints.get("labels_required", True)),
            novel_view_requested=bool(constraints.get("novel_view_requested", False)),
            allow_exploratory_generation=bool(
                constraints.get("allow_exploratory_generation", False)
            ),
            manual_review_required=bool(constraints.get("manual_review_required", True)),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceCandidate:
    source_id: str
    title: str
    authority: str
    url: str
    download_url: str | None
    source_class: str
    formats: tuple[str, ...]
    authoritative: bool
    supports_features: tuple[str, ...]
    evidence_claims: tuple[str, ...]
    usage_terms_status: str

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "SourceCandidate":
        source_id = str(payload.get("source_id", "")).strip()
        title = str(payload.get("title", "")).strip()
        authority = str(payload.get("authority", "")).strip()
        url = str(payload.get("url", "")).strip()
        source_class = str(payload.get("source_class", "")).strip()
        if not all((source_id, title, authority, url, source_class)):
            raise ValueError("Source candidates require id, title, authority, url, and class")
        raw_download_url = payload.get("download_url")
        download_url = str(raw_download_url).strip() if raw_download_url else None
        return cls(
            source_id=source_id,
            title=title,
            authority=authority,
            url=url,
            download_url=download_url,
            source_class=source_class,
            formats=_tuple_of_strings(payload.get("formats")),
            authoritative=bool(payload.get("authoritative", False)),
            supports_features=_tuple_of_strings(payload.get("supports_features")),
            evidence_claims=_tuple_of_strings(payload.get("evidence_claims")),
            usage_terms_status=str(
                payload.get("usage_terms_status", "review_required_before_distribution")
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResearchPlan:
    subject: str
    queries: tuple[str, ...]
    preferred_authorities: tuple[str, ...]
    required_source_classes: tuple[str, ...]
    stop_conditions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceEvaluation:
    selected_source_ids: tuple[str, ...]
    rejected_sources: Mapping[str, str]
    supported_features: tuple[str, ...]
    unsupported_required_features: tuple[str, ...]
    available_source_classes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RenderPlan:
    production_mode: str
    mode_selection_reason: str
    canonical_source_ids: tuple[str, ...]
    annotation_source_ids: tuple[str, ...]
    required_workers: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    preflight_blockers: tuple[str, ...]
    validation_gates: tuple[str, ...]
    production_ready: bool
    exploratory_generation_allowed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OrchestrationResult:
    request: ConstraintRequest
    research_plan: ResearchPlan
    source_evaluation: SourceEvaluation
    selected_sources: tuple[SourceCandidate, ...]
    render_plan: RenderPlan
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "request": self.request.to_dict(),
            "research_plan": self.research_plan.to_dict(),
            "source_evaluation": self.source_evaluation.to_dict(),
            "selected_sources": [source.to_dict() for source in self.selected_sources],
            "render_plan": self.render_plan.to_dict(),
        }
