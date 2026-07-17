from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .models import (
    ConstraintRequest,
    OrchestrationResult,
    RenderPlan,
    ResearchPlan,
    SourceCandidate,
    SourceEvaluation,
)


GEOMETRY_SOURCE_CLASSES = {
    "official_web_3d_geometry",
    "verified_local_geometry",
}
SOURCE_PLATE_CLASSES = {
    "official_web_2d_source_plate",
}
SUPPORTING_SOURCE_CLASSES = {
    "official_web_mechanical_drawing",
}
DOCUMENTATION_SOURCE_CLASSES = {
    "official_web_technical_documentation",
    "official_web_product_documentation",
    "official_web_component_documentation",
}


def _normalized(value: str) -> str:
    return " ".join(value.casefold().split())


class ResearchToRenderOrchestrator:
    """Create a fail-closed research and rendering plan from request constraints."""

    def build_research_plan(self, request: ConstraintRequest) -> ResearchPlan:
        feature_phrase = " ".join(request.required_visible_features[:4])
        queries = (
            f"{request.subject} official product documentation {feature_phrase}".strip(),
            f"{request.subject} official mechanical drawing dimensions",
            f"{request.subject} official STEP CAD 3D model",
            f"{request.subject} official connector component documentation",
        )
        required_source_classes = [
            "authoritative_visual_or_geometry_source",
            "official_web_technical_documentation",
        ]
        if request.labels_required:
            required_source_classes.append("registry_backed_label_evidence")
        stop_conditions = [
            "subject identity is established by an authoritative source",
            "every requested visible feature has evidence or is reported unsupported",
            "the available source class determines a supported rendering mode",
            "source provenance and usage-review status are recordable",
        ]
        return ResearchPlan(
            subject=request.subject,
            queries=queries,
            preferred_authorities=(
                "manufacturer_or_owner",
                "official_product_documentation",
                "official_design_files",
            ),
            required_source_classes=tuple(required_source_classes),
            stop_conditions=tuple(stop_conditions),
        )

    def evaluate_sources(
        self,
        request: ConstraintRequest,
        candidates: Iterable[SourceCandidate],
    ) -> tuple[SourceEvaluation, tuple[SourceCandidate, ...]]:
        selected: list[SourceCandidate] = []
        rejected: dict[str, str] = {}
        required_normalized = {
            _normalized(feature): feature for feature in request.required_visible_features
        }

        supported_classes = (
            GEOMETRY_SOURCE_CLASSES
            | SOURCE_PLATE_CLASSES
            | SUPPORTING_SOURCE_CLASSES
            | DOCUMENTATION_SOURCE_CLASSES
        )
        for candidate in candidates:
            if request.authoritative_sources_required and not candidate.authoritative:
                rejected[candidate.source_id] = "not_authoritative"
                continue
            candidate_features = {
                _normalized(feature) for feature in candidate.supports_features
            }
            has_feature_evidence = bool(candidate_features & required_normalized.keys())
            has_structural_value = candidate.source_class in supported_classes
            if not has_feature_evidence and not has_structural_value:
                rejected[candidate.source_id] = "not_relevant_to_requested_output"
                continue
            selected.append(candidate)

        supported_normalized: set[str] = set()
        for candidate in selected:
            supported_normalized.update(
                _normalized(feature) for feature in candidate.supports_features
            )
        supported_features = tuple(
            feature
            for normalized, feature in required_normalized.items()
            if normalized in supported_normalized
        )
        unsupported = tuple(
            feature
            for normalized, feature in required_normalized.items()
            if normalized not in supported_normalized
        )
        source_classes = tuple(sorted({item.source_class for item in selected}))
        evaluation = SourceEvaluation(
            selected_source_ids=tuple(item.source_id for item in selected),
            rejected_sources=rejected,
            supported_features=supported_features,
            unsupported_required_features=unsupported,
            available_source_classes=source_classes,
        )
        return evaluation, tuple(selected)

    def build_render_plan(
        self,
        request: ConstraintRequest,
        evaluation: SourceEvaluation,
        selected_sources: tuple[SourceCandidate, ...],
    ) -> RenderPlan:
        geometry_sources = tuple(
            source.source_id
            for source in selected_sources
            if source.source_class in GEOMETRY_SOURCE_CLASSES
        )
        source_plates = tuple(
            source.source_id
            for source in selected_sources
            if source.source_class in SOURCE_PLATE_CLASSES
        )
        documentation = tuple(
            source.source_id
            for source in selected_sources
            if source.source_class in DOCUMENTATION_SOURCE_CLASSES
        )

        if geometry_sources:
            production_mode = "geometry_render"
            canonical_sources = geometry_sources
            mode_workers = (
                "geometry_normalizer",
                "component_inventory_builder",
                "locked_camera_renderer",
            )
            mode_blockers = (
                "geometry_not_materialized_or_digest_verified",
                "geometry_not_normalized",
                "component_registry_not_built",
                "locked_camera_not_registered",
                "render_preset_not_registered",
            )
        elif source_plates and not request.novel_view_requested:
            production_mode = "source_plate_annotation"
            canonical_sources = source_plates
            mode_workers = (
                "source_plate_normalizer",
                "component_anchor_registry_builder",
                "deterministic_svg_renderer",
            )
            mode_blockers = (
                "source_plate_not_materialized_or_digest_verified",
                "fixed_view_contract_not_registered",
                "component_anchor_registry_not_built",
                "render_preset_not_registered",
            )
        else:
            production_mode = "reference_bundle_only"
            canonical_sources = ()
            mode_workers = ("evidence_report_builder",)
            mode_blockers = ("no_supported_production_base_source",)

        blockers = list(mode_blockers)
        if evaluation.unsupported_required_features:
            blockers.append("required_feature_evidence_incomplete")
        if not documentation and request.labels_required:
            blockers.append("label_evidence_documentation_missing")
        blockers.append("source_usage_terms_review_required")

        blocked_capabilities = [
            "provider_generated_technical_text",
            "unregistered_callouts",
            "hidden_geometry_inference",
            "automatic_production_approval",
        ]
        if production_mode != "geometry_render":
            blocked_capabilities.append("novel_camera_views")

        workers = (
            "constraint_parser",
            "research_planner",
            "source_discovery_worker",
            "source_evaluator",
            "evidence_extractor",
            "capability_classifier",
            "reference_package_builder",
            *mode_workers,
            "deterministic_annotation_renderer",
            "constraint_validator",
            "provenance_report_builder",
        )
        validation_gates = [
            "request_constraints_normalized",
            "authoritative_source_requirement_satisfied",
            "source_provenance_recorded",
            "source_usage_terms_recorded",
            "canonical_source_materialized",
            "canonical_source_digest_matches",
            "requested_features_evidence_backed",
            "render_mode_supported_by_source_class",
            "annotation_strings_registry_backed",
            "callout_targets_registry_backed",
            "forbidden_features_absent",
            "repeat_render_difference_within_tolerance",
            "manual_review_required",
        ]
        return RenderPlan(
            production_mode=production_mode,
            canonical_source_ids=canonical_sources,
            annotation_source_ids=documentation,
            required_workers=workers,
            blocked_capabilities=tuple(blocked_capabilities),
            preflight_blockers=tuple(dict.fromkeys(blockers)),
            validation_gates=tuple(validation_gates),
            production_ready=False,
            exploratory_generation_allowed=request.allow_exploratory_generation,
        )

    def orchestrate(
        self,
        request: ConstraintRequest,
        candidates: Iterable[SourceCandidate],
    ) -> OrchestrationResult:
        research_plan = self.build_research_plan(request)
        evaluation, selected = self.evaluate_sources(request, candidates)
        render_plan = self.build_render_plan(request, evaluation, selected)
        status = "planned"
        if (
            render_plan.production_mode == "reference_bundle_only"
            or evaluation.unsupported_required_features
        ):
            status = "blocked"
        return OrchestrationResult(
            request=request,
            research_plan=research_plan,
            source_evaluation=evaluation,
            selected_sources=selected,
            render_plan=render_plan,
            status=status,
        )

    def orchestrate_payload(
        self,
        request_payload: Mapping[str, Any],
        source_payloads: Iterable[Mapping[str, Any]],
    ) -> OrchestrationResult:
        request = ConstraintRequest.from_payload(request_payload)
        candidates = tuple(SourceCandidate.from_payload(item) for item in source_payloads)
        return self.orchestrate(request, candidates)
