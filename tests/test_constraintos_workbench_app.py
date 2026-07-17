import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "apps" / "constraintos_workbench"
CORE_APP = APP_DIR / "app_v2.py"
UI_APP = APP_DIR / "app_v3.py"
LEGACY_APP = APP_DIR / "app.py"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
UI_SPEC = importlib.util.spec_from_file_location("constraintos_workbench_app_v3", UI_APP)
assert UI_SPEC is not None and UI_SPEC.loader is not None
ui = importlib.util.module_from_spec(UI_SPEC)
UI_SPEC.loader.exec_module(ui)
app = ui.CORE

PACKAGER = ROOT / "scripts" / "package-constraintos-workbench-app.ps1"
CONTRACT = (
    ROOT
    / "config"
    / "technical-source-plate-contracts"
    / "toyota-supra-a80-2jz-gte-v1.json"
)
COMPONENT_REGISTRY = (
    ROOT
    / "config"
    / "technical-component-registries"
    / "toyota-supra-a80-2jz-gte-source-plate-v1.json"
)


def install_test_source_package(app_root: Path) -> Path:
    contract_target = (
        app_root
        / "config"
        / "technical-source-plate-contracts"
        / "toyota-supra-a80-2jz-gte-v1.json"
    )
    contract_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CONTRACT, contract_target)

    registry_target = (
        app_root
        / "config"
        / "technical-component-registries"
        / "toyota-supra-a80-2jz-gte-source-plate-v1.json"
    )
    registry_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(COMPONENT_REGISTRY, registry_target)

    package_root = (
        app_root
        / "reference-sources"
        / "toyota_supra_a80_2jz_gte"
    )
    source_file = package_root / "files" / "toyota-2jz-gte-official-source-plate.jpg"
    source_file.parent.mkdir(parents=True, exist_ok=True)
    source_file.write_bytes(b"deterministic-toyota-source-plate")
    digest = hashlib.sha256(source_file.read_bytes()).hexdigest()
    manifest = {
        "manifest_id": "constraintos-reference-source-package/v1",
        "scenario_id": "toyota_supra_a80_2jz_gte",
        "preflight_status": "source_files_materialized",
        "materialized_sources": [
            {
                "source_id": "toyota-2jz-gte-official-image-1993",
                "local_file": "files/toyota-2jz-gte-official-source-plate.jpg",
                "sha256": digest,
                "status": "materialized",
            }
        ],
    }
    (package_root / "source-package-manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return source_file


def test_source_backed_workbench_is_the_packaged_entry_point() -> None:
    core_content = CORE_APP.read_text(encoding="utf-8")
    legacy_content = LEGACY_APP.read_text(encoding="utf-8")
    packager_content = PACKAGER.read_text(encoding="utf-8")

    assert 'HOST = "127.0.0.1"' in core_content
    assert "ThreadingHTTPServer" in core_content
    assert "webbrowser.open(url)" in core_content
    assert 'with_name("app_v3.py")' in legacy_content
    assert 'apps\\constraintos_workbench\\app_v3.py' in packager_content


def test_workbench_separates_exploration_from_technical_rendering() -> None:
    content = CORE_APP.read_text(encoding="utf-8")

    assert "Explore Generated Raster References" in content
    assert "Render Registered Toyota Source Plate" in content
    assert "Exploratory Generated Raster References" in content
    assert "These images may invent geometry" in content
    assert "Run with Real Images" not in content
    assert "exploratory_reference_only" in content
    assert "technical_output_allowed" in content


def test_repeatability_and_registry_evidence_is_visible_without_opening_json() -> None:
    content = UI_APP.read_text(encoding="utf-8")

    assert "Repeat-render comparison:" in content
    assert "Registered callouts:" in content
    assert "Component registry:" in content
    assert "Current output SHA-256:" in content
    assert "Previous output SHA-256:" in content
    assert "Source SHA-256:" in content
    assert "Open source-backed plate" in content
    assert "Open repeatability manifest" in content
    assert "technical_render?.repeat_render_comparison?.status" in content


def test_exploratory_prompt_prohibits_generated_technical_text() -> None:
    prompt = app.build_exploratory_prompt(
        app.DEFAULT_REQUEST,
        app.EXPLORATORY_PROFILES[0],
    )

    assert "Do not include any words, letters, numbers, labels" in prompt
    assert "Do not represent the output as a technical drawing" in prompt
    assert "engineering labels" not in prompt
    assert "dense technical callouts" not in prompt


def test_source_status_fails_closed_without_materialized_package(tmp_path: Path) -> None:
    contract_target = (
        tmp_path
        / "config"
        / "technical-source-plate-contracts"
        / "toyota-supra-a80-2jz-gte-v1.json"
    )
    contract_target.parent.mkdir(parents=True)
    shutil.copyfile(CONTRACT, contract_target)

    status = app.technical_source_status(tmp_path)

    assert status["ready"] is False
    assert status["status"] == "blocked"
    assert status["reason"] == "source_package_missing"


def test_source_status_requires_digest_match(tmp_path: Path) -> None:
    source_file = install_test_source_package(tmp_path)
    ready = app.technical_source_status(tmp_path)

    assert ready["ready"] is True
    assert ready["status"] == "ready"
    assert ready["production_mode"] == "source_plate_annotation"
    assert ready["production_ready"] is False
    assert ready["approval_allowed"] is False

    source_file.write_bytes(b"changed-source-plate")
    blocked = app.technical_source_status(tmp_path)

    assert blocked["ready"] is False
    assert blocked["reason"] == "source_digest_mismatch"


def test_source_plate_render_is_byte_repeatable_with_registered_callouts(tmp_path: Path) -> None:
    install_test_source_package(tmp_path)
    scenario_root = tmp_path / "runs" / "output-poc" / app.SCENARIO
    first_run = scenario_root / "run-001"
    second_run = scenario_root / "run-002"
    first_run.mkdir(parents=True)
    second_run.mkdir(parents=True)

    first = ui.render_registered_source_plate(tmp_path, first_run)
    second = ui.render_registered_source_plate(tmp_path, second_run)

    first_svg = first_run / first["output_file"]
    second_svg = second_run / second["output_file"]
    assert first_svg.read_bytes() == second_svg.read_bytes()
    assert first["repeat_render_comparison"]["status"] == "baseline_created"
    assert second["repeat_render_comparison"]["status"] == "passed"
    assert first["source_sha256"] == second["source_sha256"]
    assert second["registered_callout_count"] == 4
    assert second["generated_text_inside_source_raster"] is False
    assert second["annotation_source"] == "registered_component_registry"
    assert second["annotation_strings_registry_backed"] is True
    assert second["callout_targets_registry_backed"] is True
    assert second["hidden_geometry_inferred"] is False
    assert second["approval_allowed"] is False
    svg_content = second_svg.read_text(encoding="utf-8")
    assert "2JZ-COMP-001" in svg_content
    assert "2JZ-COMP-004" in svg_content
    assert "Turbocharger hardware is not fully exposed" in svg_content


def test_source_plate_contract_limits_capabilities() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert contract["contract_version"] == "2.0.0"
    assert contract["production_mode"] == "source_plate_annotation"
    assert contract["canonical_source"]["authority"] == "Toyota Motor Corporation"
    assert contract["annotations"]["provider_generated_text_allowed"] is False
    assert contract["annotations"]["component_callouts_in_this_contract"] is True
    assert contract["annotations"]["component_callout_source"] == "registered_component_registry"
    assert contract["capability_limits"]["component_callouts_allowed"] is True
    assert contract["capability_limits"]["component_callouts_limited_to_registered_visible_components"] is True
    assert contract["capability_limits"]["novel_camera_views_allowed"] is False
    assert contract["capability_limits"]["hidden_geometry_inference_allowed"] is False


def test_component_registry_uses_only_registered_visible_targets() -> None:
    registry = json.loads(COMPONENT_REGISTRY.read_text(encoding="utf-8"))

    assert registry["status"] == "active"
    assert registry["coordinate_system"] == "normalized_source_raster"
    assert len(registry["components"]) == 4
    assert all(item["confidence"] == "high" for item in registry["components"])
    assert all(item["visibility"].startswith("clearly_visible") for item in registry["components"])
    assert registry["guardrails"]["unregistered_callouts_allowed"] is False
    assert registry["guardrails"]["hidden_component_callouts_allowed"] is False
    assert registry["guardrails"]["provider_generated_text_allowed"] is False


def test_packager_copies_registered_config_and_materialized_toyota_package() -> None:
    content = PACKAGER.read_text(encoding="utf-8")

    assert 'Copy-Item -Recurse -Force (Join-Path $RepoRoot "config")' in content
    assert 'reference-sources\\toyota_supra_a80_2jz_gte' in content
    assert "Copying materialized Toyota reference package" in content
    assert "source-package-manifest.json" in content
    assert "Explore Generated Raster References" in content
    assert "Render Registered Toyota Source Plate" in content
    assert "repeat-render comparison status" in content
    assert "No screenshot is required" in content
    assert "Run with Real Images" not in content


def test_app_serves_source_status_and_required_artifact_types() -> None:
    content = CORE_APP.read_text(encoding="utf-8")

    assert 'parsed.path == "/api/source-status"' in content
    assert "technical_source_status(self.app_root)" in content
    assert 'content_type = "image/svg+xml"' in content
    assert 'content_type = "image/jpeg"' in content
    assert "technical-render-manifest.json" in content
    assert "exploratory-reference-manifest.json" in content
