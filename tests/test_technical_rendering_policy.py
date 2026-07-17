import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "technical-rendering-policy.json"


def load_policy() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


def test_technical_rendering_policy_exists_and_is_active() -> None:
    policy = load_policy()

    assert policy["policy_id"] == "constraintos-technical-rendering/v1"
    assert policy["policy_version"] == "1.1.0"
    assert policy["status"] == "active"


def test_examples_are_source_backed_by_web_available_material() -> None:
    strategy = load_policy()["source_strategy"]

    assert strategy["selection_principle"] == "examples_are_selected_for_web_available_reference_material"
    assert strategy["canonical_source_package_required"] is True
    assert strategy["authoritative_web_sources_allowed"] is True
    assert strategy["proprietary_3d_purchase_required"] is False
    assert strategy["capability_must_not_exceed_available_source_evidence"] is True
    assert {
        "official_web_3d_geometry",
        "official_web_2d_source_plate",
        "official_web_technical_documentation",
    }.issubset(strategy["accepted_source_classes"])


def test_text_to_image_is_exploratory_only() -> None:
    text_to_image = load_policy()["text_to_image"]

    assert text_to_image["role"] == "exploratory_reference_only"
    assert text_to_image["production_technical_output_allowed"] is False
    assert text_to_image["production_approval_allowed"] is False
    assert text_to_image["provider_generated_labels_allowed"] is False
    assert text_to_image["provider_generated_dimensions_allowed"] is False
    assert text_to_image["provider_generated_legends_allowed"] is False


def test_production_rendering_requires_deterministic_source_backing() -> None:
    production = load_policy()["production_output"]

    assert production["renderer_class"] == "deterministic_source_backed"
    assert production["canonical_asset_required"] is True
    assert production["canonical_asset_may_be_2d_or_3d"] is True
    assert production["locked_camera_required_for_geometry_rendering"] is True
    assert production["locked_source_crop_required_for_source_plate_rendering"] is True
    assert production["locked_render_preset_required"] is True
    assert production["component_registry_required"] is True
    assert production["deterministic_annotation_overlay_required"] is True
    assert production["fail_closed_when_requirements_missing"] is True


def test_production_modes_are_bounded_by_source_class() -> None:
    modes = load_policy()["production_modes"]

    assert modes["geometry_render"]["novel_views_allowed"] is True
    assert "official_web_3d_geometry" in modes["geometry_render"]["allowed_source_classes"]
    assert modes["source_plate_annotation"]["novel_views_allowed"] is False
    assert "official_web_2d_source_plate" in modes["source_plate_annotation"]["allowed_source_classes"]
    assert modes["reference_bundle_only"]["production_base_plate_allowed"] is False


def test_annotations_are_separate_registry_backed_overlays() -> None:
    annotation = load_policy()["annotation"]

    assert annotation["rendered_inside_raster_base_plate"] is False
    assert annotation["approved_source"] == "component_label_registry"
    assert annotation["output_format"] == "svg_overlay"
    assert annotation["component_anchor_required"] is True
    assert annotation["leader_line_target_required"] is True


def test_required_repeatability_gates_are_declared() -> None:
    policy = load_policy()

    assert {
        "canonical_source_package_present",
        "source_provenance_recorded",
        "source_usage_terms_recorded",
        "canonical_asset_present",
        "canonical_asset_digest_matches",
        "requested_capability_supported_by_source_class",
        "expected_component_inventory_present",
        "locked_view_or_source_plate_definition_present",
        "render_preset_version_matches",
    }.issubset(policy["required_preflight_gates"])

    assert {
        "forbidden_raster_text_absent",
        "annotation_strings_registry_backed",
        "callout_targets_registry_backed",
        "orientation_matches_view_contract",
        "repeat_render_difference_within_tolerance",
    }.issubset(policy["required_output_gates"])


def test_manual_review_cannot_replace_missing_preflight() -> None:
    review = load_policy()["review"]

    assert review["manual_review_required"] is True
    assert review["manual_review_substitutes_for_missing_preflight"] is False
    assert review["default_decision"] == "needs_review"
