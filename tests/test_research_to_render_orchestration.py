import json
from pathlib import Path

from runtime.research_to_render import ResearchToRenderOrchestrator

ROOT = Path(__file__).resolve().parents[1]
REQUEST_PATH = (
    ROOT
    / "config"
    / "research-to-render-examples"
    / "raspberry-pi-5-io-plate-request.json"
)
SOURCES_PATH = (
    ROOT
    / "config"
    / "research-to-render-examples"
    / "raspberry-pi-5-discovered-sources.json"
)


def load_fixture() -> tuple[dict, list[dict]]:
    return (
        json.loads(REQUEST_PATH.read_text(encoding="utf-8")),
        json.loads(SOURCES_PATH.read_text(encoding="utf-8")),
    )


def test_request_constraints_drive_research_and_render_planning() -> None:
    request, sources = load_fixture()
    result = ResearchToRenderOrchestrator().orchestrate_payload(request, sources)

    assert result.status == "planned"
    assert result.request.subject == "Raspberry Pi 5"
    assert result.request.viewpoint == "locked_top_view"
    assert len(result.request.required_visible_features) == 10
    assert "invented connectors" in result.request.forbidden_features
    assert result.request.repeatability_required is True
    assert result.request.authoritative_sources_required is True
    assert result.request.allow_exploratory_generation is False


def test_research_plan_is_generated_from_request_not_a_scenario_key() -> None:
    request, sources = load_fixture()
    result = ResearchToRenderOrchestrator().orchestrate_payload(request, sources)

    assert result.research_plan.subject == "Raspberry Pi 5"
    assert any("Raspberry Pi 5" in query for query in result.research_plan.queries)
    assert any("STEP CAD 3D model" in query for query in result.research_plan.queries)
    assert "registry_backed_label_evidence" in result.research_plan.required_source_classes
    assert any(
        "every requested visible feature" in condition
        for condition in result.research_plan.stop_conditions
    )


def test_authoritative_sources_cover_every_required_feature() -> None:
    request, sources = load_fixture()
    result = ResearchToRenderOrchestrator().orchestrate_payload(request, sources)

    assert len(result.selected_sources) == 5
    assert all(source.authoritative for source in result.selected_sources)
    assert result.source_evaluation.unsupported_required_features == ()
    assert set(result.source_evaluation.supported_features) == set(
        result.request.required_visible_features
    )
    assert "official_web_2d_source_plate" in result.source_evaluation.available_source_classes
    assert "official_web_3d_geometry" in result.source_evaluation.available_source_classes
    assert "official_web_mechanical_drawing" in result.source_evaluation.available_source_classes
    assert "official_web_product_documentation" in result.source_evaluation.available_source_classes


def test_book_illustration_request_selects_reference_conditioned_generation() -> None:
    request, sources = load_fixture()
    result = ResearchToRenderOrchestrator().orchestrate_payload(request, sources)
    plan = result.render_plan

    assert plan.production_mode == "reference_conditioned_generation"
    assert plan.mode_selection_reason == (
        "authoritative_fixed_view_reference_supports_new_constrained_"
        "illustration_without_geometry_reconstruction"
    )
    assert plan.canonical_source_ids == (
        "rpi5-official-top-view-source-plate-2026",
    )
    assert set(plan.annotation_source_ids) == {
        "rpi5-official-product-brief-2026",
        "rpi5-official-hardware-documentation-2026",
    }
    assert "source_plate_normalizer" in plan.required_workers
    assert "generation_constraint_compiler" in plan.required_workers
    assert "reference_conditioned_image_generator" in plan.required_workers
    assert "visual_constraint_validator" in plan.required_workers
    assert "deterministic_annotation_renderer" in plan.required_workers
    assert "component_anchor_registry_builder" not in plan.required_workers
    assert "deterministic_svg_renderer" not in plan.required_workers
    assert "locked_camera_renderer" not in plan.required_workers
    assert plan.exploratory_generation_allowed is False


def test_explicit_source_annotation_request_uses_direct_annotation_path() -> None:
    request, sources = load_fixture()
    request["output_kind"] = "annotated_source_plate"

    result = ResearchToRenderOrchestrator().orchestrate_payload(request, sources)
    plan = result.render_plan

    assert plan.production_mode == "source_plate_annotation"
    assert plan.mode_selection_reason == (
        "request_explicitly_requires_annotation_of_an_authoritative_fixed_source_plate"
    )
    assert "component_anchor_registry_builder" in plan.required_workers
    assert "deterministic_svg_renderer" in plan.required_workers
    assert "reference_conditioned_image_generator" not in plan.required_workers
    assert "repeat_render_difference_within_tolerance" in plan.validation_gates


def test_novel_view_constraint_promotes_verified_geometry() -> None:
    request, sources = load_fixture()
    request["viewpoint"] = "locked_oblique_view"
    request["constraints"]["novel_view_requested"] = True

    result = ResearchToRenderOrchestrator().orchestrate_payload(request, sources)
    plan = result.render_plan

    assert plan.production_mode == "geometry_render"
    assert plan.mode_selection_reason == (
        "verified_geometry_required_for_requested_view_or_no_suitable_"
        "fixed_source_plate"
    )
    assert plan.canonical_source_ids == ("rpi5-official-step-2026",)
    assert "geometry_normalizer" in plan.required_workers
    assert "locked_camera_renderer" in plan.required_workers


def test_generation_plan_fails_closed_before_reference_generation_is_configured() -> None:
    request, sources = load_fixture()
    result = ResearchToRenderOrchestrator().orchestrate_payload(request, sources)
    plan = result.render_plan

    assert plan.production_ready is False
    assert "source_plate_not_materialized_or_digest_verified" in plan.preflight_blockers
    assert "generation_package_not_compiled" in plan.preflight_blockers
    assert "image_generation_provider_not_configured" in plan.preflight_blockers
    assert "visual_constraint_validator_not_configured" in plan.preflight_blockers
    assert "source_usage_terms_review_required" in plan.preflight_blockers
    assert "provider_generated_technical_text" in plan.blocked_capabilities
    assert "hidden_geometry_inference" in plan.blocked_capabilities
    assert "novel_camera_views" in plan.blocked_capabilities
    assert "generation_package_digest_recorded" in plan.validation_gates
    assert "reference_image_supplied_to_generator" in plan.validation_gates
    assert "generated_candidate_digest_recorded" in plan.validation_gates
    assert "candidate_visual_constraint_validation_complete" in plan.validation_gates
    assert "repeat_render_difference_within_tolerance" not in plan.validation_gates


def test_mechanical_drawing_alone_cannot_be_promoted_to_component_plate() -> None:
    request, sources = load_fixture()
    supporting_only = [
        source
        for source in sources
        if source["source_class"]
        not in {"official_web_3d_geometry", "official_web_2d_source_plate"}
    ]
    result = ResearchToRenderOrchestrator().orchestrate_payload(
        request,
        supporting_only,
    )

    assert result.status == "blocked"
    assert result.render_plan.production_mode == "reference_bundle_only"
    assert result.render_plan.mode_selection_reason == (
        "no_supported_visual_or_geometry_base_source"
    )
    assert result.render_plan.canonical_source_ids == ()
    assert "no_supported_production_base_source" in result.render_plan.preflight_blockers


def test_non_authoritative_sources_are_rejected_when_request_requires_authority() -> None:
    request, sources = load_fixture()
    sources.append(
        {
            "source_id": "unverified-blog-image",
            "title": "Unverified board image",
            "authority": "Unknown blog",
            "url": "https://example.invalid/board.jpg",
            "source_class": "official_web_2d_source_plate",
            "formats": ["jpg"],
            "authoritative": False,
            "supports_features": ["40-pin GPIO header"],
            "evidence_claims": [],
        }
    )
    result = ResearchToRenderOrchestrator().orchestrate_payload(request, sources)

    assert result.source_evaluation.rejected_sources["unverified-blog-image"] == (
        "not_authoritative"
    )
    assert "unverified-blog-image" not in result.source_evaluation.selected_source_ids


def test_orchestration_result_serializes_as_deterministic_json_data() -> None:
    request, sources = load_fixture()
    orchestrator = ResearchToRenderOrchestrator()
    first = orchestrator.orchestrate_payload(request, sources).to_dict()
    second = orchestrator.orchestrate_payload(request, sources).to_dict()

    assert first == second
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert first["render_plan"]["production_mode"] == (
        "reference_conditioned_generation"
    )
    assert first["render_plan"]["mode_selection_reason"].startswith(
        "authoritative_fixed_view_reference"
    )
