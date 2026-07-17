import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "technical-reference-source-registry.json"


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def scenario(scenario_id: str) -> dict:
    for item in load_registry()["scenarios"]:
        if item["scenario_id"] == scenario_id:
            return item
    raise AssertionError(f"Missing scenario: {scenario_id}")


def source(scenario_id: str, source_id: str) -> dict:
    for item in scenario(scenario_id)["sources"]:
        if item["source_id"] == source_id:
            return item
    raise AssertionError(f"Missing source: {source_id}")


def test_reference_source_registry_is_active() -> None:
    registry = load_registry()

    assert registry["registry_id"] == "constraintos-technical-reference-sources/v1"
    assert registry["registry_version"] == "1.4.0"
    assert registry["status"] == "active"
    assert "web-available reference information" in registry["selection_principle"]


def test_perseverance_uses_official_web_geometry() -> None:
    perseverance = scenario("nasa_perseverance_rover")
    source_classes = {item["source_class"] for item in perseverance["sources"]}
    formats = {item for source_item in perseverance["sources"] for item in source_item.get("available_formats", [])}
    required_sources = [source_item for source_item in perseverance["sources"] if source_item["ingestion_required"]]

    assert perseverance["preferred_production_mode"] == "geometry_render"
    assert perseverance["capabilities"]["deterministic_geometry_render"] is True
    assert perseverance["capabilities"]["novel_locked_views"] is True
    assert "official_web_3d_geometry" in source_classes
    assert {"blend", "glb"}.issubset(formats)
    assert all(source_item["authority"] == "NASA/JPL-Caltech" for source_item in perseverance["sources"])
    assert all(source_item.get("download_url") for source_item in required_sources)
    assert all(source_item.get("target_filename") for source_item in required_sources)


def test_toyota_uses_official_source_plate_and_release() -> None:
    toyota = scenario("toyota_supra_a80_2jz_gte")
    source_classes = {item["source_class"] for item in toyota["sources"]}
    required_sources = [source_item for source_item in toyota["sources"] if source_item["ingestion_required"]]

    assert toyota["preferred_production_mode"] == "source_plate_annotation"
    assert toyota["capabilities"]["deterministic_source_plate_annotation"] is True
    assert toyota["capabilities"]["novel_locked_views"] is False
    assert "official_web_2d_source_plate" in source_classes
    assert "official_web_technical_documentation" in source_classes
    assert all(source_item["authority"] == "Toyota Motor Corporation" for source_item in toyota["sources"])
    assert all(source_item.get("download_url") for source_item in required_sources)
    assert all(source_item.get("target_filename") for source_item in required_sources)
    assert "Novel camera angles" in toyota["production_limit"]


def test_raspberry_pi_5_prefers_fixed_source_plate_and_retains_geometry_fallback() -> None:
    raspberry_pi = scenario("raspberry_pi_5_io_plate")
    source_classes = {item["source_class"] for item in raspberry_pi["sources"]}
    required_sources = [source_item for source_item in raspberry_pi["sources"] if source_item["ingestion_required"]]
    formats = {item for source_item in raspberry_pi["sources"] for item in source_item.get("available_formats", [])}

    assert raspberry_pi["preferred_production_mode"] == "source_plate_annotation"
    assert raspberry_pi["capabilities"]["deterministic_source_plate_annotation"] is True
    assert raspberry_pi["capabilities"]["deterministic_geometry_render"] is True
    assert raspberry_pi["capabilities"]["mechanical_dimension_validation"] is True
    assert raspberry_pi["capabilities"]["text_to_image_required"] is False
    assert {
        "official_web_2d_source_plate",
        "official_web_3d_geometry",
        "official_web_mechanical_drawing",
        "official_web_product_documentation",
        "official_web_component_documentation",
    }.issubset(source_classes)
    assert {"embedded_raster", "step", "pdf", "html"}.issubset(formats)
    assert all(source_item["authority"] == "Raspberry Pi Ltd" for source_item in raspberry_pi["sources"])
    assert all(source_item.get("download_url") for source_item in required_sources)
    assert all(source_item.get("target_filename") for source_item in required_sources)
    assert "source plate is preferred" in raspberry_pi["production_limit"]
    assert "STEP package remains a fallback" in raspberry_pi["production_limit"]


def test_raspberry_pi_html_documentation_is_reference_only() -> None:
    hardware_docs = source(
        "raspberry_pi_5_io_plate",
        "rpi5-official-hardware-documentation-2026",
    )

    assert hardware_docs["source_class"] == "official_web_component_documentation"
    assert hardware_docs["ingestion_required"] is False
    assert hardware_docs["materialization_requirement"] == "reference_only"
    assert "reject automated downloads" in hardware_docs["source_access_note"]
    assert "fan_connector_evidence" in hardware_docs["purpose"]
    assert "approved_component_terminology" in hardware_docs["purpose"]


def test_all_materialized_sources_require_usage_review() -> None:
    for item in load_registry()["scenarios"]:
        for source_item in item["sources"]:
            if source_item["ingestion_required"]:
                assert source_item["usage_terms_status"] == "review_required_before_distribution"


def test_scenario_capability_cannot_exceed_ingested_sources() -> None:
    onboarding = load_registry()["scenario_onboarding_rule"]

    assert onboarding["web_source_inventory_required"] is True
    assert onboarding["capability_classification_required"] is True
    assert onboarding["source_digest_required_after_ingestion"] is True
    assert onboarding["usage_terms_record_required"] is True
    assert onboarding["production_capability_may_not_exceed_source_package"] is True
