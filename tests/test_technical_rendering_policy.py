import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "technical-rendering-policy.json"


def load_policy() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


def test_technical_rendering_policy_exists_and_is_active() -> None:
    policy = load_policy()

    assert policy["policy_id"] == "constraintos-technical-rendering/v1"
    assert policy["status"] == "active"


def test_text_to_image_is_exploratory_only() -> None:
    text_to_image = load_policy()["text_to_image"]

    assert text_to_image["role"] == "exploratory_reference_only"
    assert text_to_image["production_technical_output_allowed"] is False
    assert text_to_image["production_approval_allowed"] is False
    assert text_to_image["provider_generated_labels_allowed"] is False
    assert text_to_image["provider_generated_dimensions_allowed"] is False
    assert text_to_image["provider_generated_legends_allowed"] is False


def test_production_rendering_requires_deterministic_foundations() -> None:
    production = load_policy()["production_output"]

    assert production["renderer_class"] == "deterministic_geometry"
    assert production["canonical_asset_required"] is True
    assert production["locked_camera_required"] is True
    assert production["locked_render_preset_required"] is True
    assert production["component_registry_required"] is True
    assert production["deterministic_annotation_overlay_required"] is True
    assert production["fail_closed_when_requirements_missing"] is True


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
        "canonical_asset_present",
        "canonical_asset_digest_matches",
        "expected_component_inventory_present",
        "locked_view_definition_present",
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
