from __future__ import annotations

import html
import shutil
from pathlib import Path
from typing import Any

import app_v2 as CORE


BASE_HTML_PAGE = CORE.html_page


def previous_compatible_output_digest(
    app_root: Path,
    current_run_dir: Path,
    contract_id: str,
    render_preset_version: str,
    component_registry_id: str,
    component_registry_version: str,
) -> str | None:
    scenario_root = app_root / "runs" / "output-poc" / CORE.SCENARIO
    if not scenario_root.exists():
        return None
    candidates = sorted(
        [item for item in scenario_root.iterdir() if item.is_dir() and item != current_run_dir],
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    for candidate in candidates:
        manifest_path = candidate / "technical-render-manifest.json"
        if not manifest_path.exists():
            continue
        manifest = CORE.read_json(manifest_path)
        if manifest.get("contract_id") != contract_id:
            continue
        if manifest.get("render_preset_version") != render_preset_version:
            continue
        if manifest.get("component_registry_id") != component_registry_id:
            continue
        if manifest.get("component_registry_version") != component_registry_version:
            continue
        digest = manifest.get("output_sha256")
        if isinstance(digest, str) and digest:
            return digest
    return None


def validate_component_registry_layout(
    registry: dict[str, Any],
    width: int,
    height: int,
) -> list[str]:
    validated: list[str] = []
    for component in registry.get("components", []):
        component_id = str(component["component_id"])
        anchor = component["anchor"]
        anchor_x = float(anchor["x"])
        anchor_y = float(anchor["y"])
        if not (0.0 <= anchor_x <= 1.0 and 0.0 <= anchor_y <= 1.0):
            raise RuntimeError(f"Component {component_id} has an anchor outside the source raster.")

        label_position = component["label_position"]
        label_x = float(label_position["x"])
        label_y = float(label_position["y"])
        text_anchor = str(label_position["text_anchor"])
        if text_anchor not in {"start", "middle", "end"}:
            raise RuntimeError(f"Component {component_id} has an unsupported text anchor.")
        if not (50.0 <= label_x <= width - 50.0 and 80.0 <= label_y <= height - 80.0):
            raise RuntimeError(f"Component {component_id} label position is outside the output safe area.")

        route = component["route"]
        for route_key in ("elbow_x", "line_end_x"):
            route_x = float(route[route_key])
            if not (24.0 <= route_x <= width - 24.0):
                raise RuntimeError(f"Component {component_id} route is outside the output bounds.")
        validated.append(component_id)
    return validated


def component_callout_svg(
    component: dict[str, Any],
    placement: dict[str, Any],
) -> str:
    anchor = component["anchor"]
    label_position = component["label_position"]
    route = component["route"]
    anchor_x = float(placement["x"]) + float(anchor["x"]) * float(placement["width"])
    anchor_y = float(placement["y"]) + float(anchor["y"]) * float(placement["height"])
    label_x = float(label_position["x"])
    label_y = float(label_position["y"])
    elbow_x = float(route["elbow_x"])
    line_end_x = float(route["line_end_x"])
    text_anchor = html.escape(str(label_position["text_anchor"]))
    component_id = html.escape(str(component["component_id"]))
    label = html.escape(str(component["label"]))
    line_y = label_y - 10
    return f"""
  <g data-component-id="{component_id}">
    <polyline points="{anchor_x:.2f},{anchor_y:.2f} {elbow_x:.2f},{anchor_y:.2f} {elbow_x:.2f},{line_y:.2f} {line_end_x:.2f},{line_y:.2f}" fill="none" stroke="#1f4e79" stroke-width="3" stroke-linejoin="round"/>
    <circle cx="{anchor_x:.2f}" cy="{anchor_y:.2f}" r="8" fill="#ffffff" stroke="#1f4e79" stroke-width="4"/>
    <text x="{label_x:.2f}" y="{label_y - 24:.2f}" text-anchor="{text_anchor}" font-family="Consolas, monospace" font-size="17" fill="#49627a">{component_id}</text>
    <text x="{label_x:.2f}" y="{label_y:.2f}" text-anchor="{text_anchor}" font-family="Arial, Helvetica, sans-serif" font-size="25" font-weight="700" fill="#12233d">{label}</text>
  </g>"""


def render_registered_source_plate(
    app_root: Path,
    run_dir: Path,
) -> dict[str, Any]:
    status = CORE.technical_source_status(app_root)
    if not status.get("ready"):
        raise RuntimeError(f"Source-backed technical render is blocked: {status['message']}")

    contract = CORE.read_json(Path(status["contract_path"]))
    registry_path = app_root / str(contract["component_registry"])
    if not registry_path.exists():
        raise RuntimeError(f"Source-backed technical render is blocked: missing component registry {registry_path}")
    registry = CORE.read_json(registry_path)
    if registry.get("status") != "active":
        raise RuntimeError("Source-backed technical render is blocked: component registry is not active.")
    if registry.get("source_id") != contract["canonical_source"]["source_id"]:
        raise RuntimeError("Source-backed technical render is blocked: component registry source does not match the contract.")

    source_path = Path(status["source_file"])
    output_root = run_dir / "technical-render"
    output_root.mkdir(parents=True, exist_ok=True)
    source_copy = output_root / "toyota-2jz-gte-source-plate.jpg"
    shutil.copyfile(source_path, source_copy)

    width = int(contract["output"]["width"])
    height = int(contract["output"]["height"])
    placement = contract["source_placement"]
    annotations = contract["annotations"]
    components = registry["components"]
    validated_component_ids = validate_component_registry_layout(registry, width, height)
    callouts = "".join(component_callout_svg(component, placement) for component in components)
    notes = registry["system_notes"]
    escaped_title = html.escape(str(annotations["title"]))
    escaped_subtitle = html.escape(str(annotations["subtitle"]))
    escaped_footer = html.escape(str(annotations["footer"]))
    escaped_note_1 = html.escape(str(notes[0]["text"]))
    escaped_note_2 = html.escape(str(notes[1]["text"]))
    short_digest = str(status["source_sha256"])[:16]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  <rect x="24" y="24" width="{width - 48}" height="{height - 48}" fill="none" stroke="#172033" stroke-width="3"/>
  <text x="70" y="72" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="700" fill="#111827">{escaped_title}</text>
  <text x="70" y="112" font-family="Arial, Helvetica, sans-serif" font-size="21" fill="#374151">{escaped_subtitle}</text>
  <image href="toyota-2jz-gte-source-plate.jpg" x="{placement['x']}" y="{placement['y']}" width="{placement['width']}" height="{placement['height']}" preserveAspectRatio="xMidYMid meet"/>
  <rect x="{placement['x']}" y="{placement['y']}" width="{placement['width']}" height="{placement['height']}" fill="none" stroke="#8aa0b5" stroke-width="2"/>
{callouts}
  <line x1="70" y1="1080" x2="{width - 70}" y2="1080" stroke="#172033" stroke-width="2"/>
  <text x="70" y="1125" font-family="Arial, Helvetica, sans-serif" font-size="21" fill="#12233d">{escaped_note_1}</text>
  <text x="70" y="1162" font-family="Arial, Helvetica, sans-serif" font-size="19" fill="#6b2d2d">{escaped_note_2}</text>
  <text x="70" y="1210" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="700" fill="#111827">{escaped_footer}</text>
  <text x="70" y="1250" font-family="Consolas, monospace" font-size="15" fill="#4b5563">Source SHA-256: {short_digest}… · Contract: {html.escape(str(contract['contract_id']))}</text>
  <text x="{width - 70}" y="1250" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#991b1b">SOURCE-BACKED DRAFT · MANUAL REVIEW REQUIRED</text>
</svg>
"""
    svg_path = output_root / "toyota-2jz-gte-source-backed-plate.svg"
    svg_path.write_text(svg, encoding="utf-8")
    output_digest = CORE.sha256_file(svg_path)
    previous_digest = previous_compatible_output_digest(
        app_root,
        run_dir,
        str(contract["contract_id"]),
        str(contract["render_preset_version"]),
        str(registry["registry_id"]),
        str(registry["registry_version"]),
    )
    comparison_status = (
        "baseline_created"
        if previous_digest is None
        else ("passed" if previous_digest == output_digest else "failed")
    )

    manifest = {
        "manifest_id": "constraintos-technical-render-manifest/v1",
        "scenario_id": CORE.REFERENCE_SCENARIO,
        "production_mode": "source_plate_annotation",
        "status": "complete" if comparison_status != "failed" else "blocked",
        "source_package_manifest": status["manifest_path"],
        "source_file": status["source_file"],
        "source_sha256": status["source_sha256"],
        "contract_id": contract["contract_id"],
        "render_preset_version": contract["render_preset_version"],
        "component_registry_id": registry["registry_id"],
        "component_registry_version": registry["registry_version"],
        "registered_callout_count": len(components),
        "validated_component_ids": validated_component_ids,
        "callout_layout_bounds_passed": True,
        "output_file": "technical-render/toyota-2jz-gte-source-backed-plate.svg",
        "output_sha256": output_digest,
        "repeat_render_comparison": {
            "status": comparison_status,
            "previous_output_sha256": previous_digest,
            "current_output_sha256": output_digest,
            "comparison_scope": "matching_contract_render_preset_and_component_registry_version",
        },
        "generated_text_inside_source_raster": False,
        "annotation_source": "registered_component_registry",
        "annotation_strings_registry_backed": True,
        "callout_targets_registry_backed": True,
        "hidden_geometry_inferred": False,
        "approval_allowed": False,
        "review_decision": "needs_review",
    }
    CORE.write_json(run_dir / "technical-render-manifest.json", manifest)
    if comparison_status == "failed":
        raise RuntimeError(
            "Repeat-render comparison failed: the registry-backed deterministic SVG changed."
        )
    return manifest


def html_page() -> str:
    content = BASE_HTML_PAGE()
    content = content.replace(
        "deterministic registered metadata overlay",
        "deterministic registry-backed component callout overlay",
    )
    content = content.replace(
        '<iframe id="technicalFrame" class="technical-frame"></iframe>',
        '<img id="technicalFrame" class="technical-frame" alt="Source-backed Toyota technical plate"/>',
    )
    content = content.replace(
        ".technical-frame { min-height:760px; border:0; }",
        ".technical-frame { display:block; height:auto; border:0; }",
    )
    content = content.replace(
        '<p id="technicalLinks"></p>',
        '<div id="technicalSummary" class="status">Repeat-render and component-registry evidence will appear here after a source-backed run.</div><p id="technicalLinks"></p>',
    )
    content = content.replace(
        "status.textContent='Complete.\\nMode: '+data.run_mode+'\\nRun directory: '+data.run_dir+'\\nApproval allowed: false';",
        "const comparison=data.technical_render?.repeat_render_comparison?.status||'not_applicable';const currentHash=data.technical_render?.output_sha256||'not_applicable';const previousHash=data.technical_render?.repeat_render_comparison?.previous_output_sha256||'none';const calloutCount=data.technical_render?.registered_callout_count||0;status.textContent='Complete.\\nMode: '+data.run_mode+'\\nRun directory: '+data.run_dir+'\\nRepeat-render comparison: '+comparison+'\\nRegistered callouts: '+calloutCount+'\\nCurrent output SHA-256: '+currentHash+'\\nPrevious output SHA-256: '+previousHash+'\\nApproval allowed: false';",
    )
    content = content.replace(
        "document.getElementById('technicalLinks').innerHTML='<a href=\"'+data.technical_render_url+'\" target=\"_blank\">Open source-backed SVG</a> · <a href=\"'+data.technical_render_manifest_url+'\" target=\"_blank\">Open technical render manifest</a>';",
        "const repeat=data.technical_render.repeat_render_comparison;document.getElementById('technicalSummary').textContent='Repeat-render comparison: '+repeat.status+'\\nRegistered callouts: '+data.technical_render.registered_callout_count+'\\nComponent registry: '+data.technical_render.component_registry_id+' @ '+data.technical_render.component_registry_version+'\\nCallout layout bounds: '+data.technical_render.callout_layout_bounds_passed+'\\nCurrent output SHA-256: '+repeat.current_output_sha256+'\\nPrevious output SHA-256: '+(repeat.previous_output_sha256||'none')+'\\nSource SHA-256: '+data.technical_render.source_sha256;document.getElementById('technicalLinks').innerHTML='<a href=\"'+data.technical_render_url+'\" target=\"_blank\">Open source-backed plate</a> · <a href=\"'+data.technical_render_manifest_url+'\" target=\"_blank\">Open repeatability manifest</a>';",
    )
    return content


CORE.render_registered_source_plate = render_registered_source_plate
CORE.html_page = html_page


def main() -> int:
    return int(CORE.main())


if __name__ == "__main__":
    raise SystemExit(main())
