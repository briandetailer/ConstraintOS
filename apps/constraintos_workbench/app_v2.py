from __future__ import annotations

import base64
import hashlib
import html
import json
import os
import posixpath
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

HOST = "127.0.0.1"
PORT = int(os.environ.get("CONSTRAINTOS_WORKBENCH_PORT", "8787"))
SCENARIO = "supra_2jz_gte_twin_turbo"
REFERENCE_SCENARIO = "toyota_supra_a80_2jz_gte"
OPENAI_IMAGES_ENDPOINT = "https://api.openai.com/v1/images/generations"
RUN_LOCK = threading.Lock()

DEFAULT_REQUEST: dict[str, Any] = {
    "scenario_key": SCENARIO,
    "request_text": (
        "Create a source-backed technical plate for the Toyota Supra A80 "
        "2JZ-GTE twin-turbo engine while preserving manual review."
    ),
    "requested_focus": "technical_comparison",
    "output_count": 2,
    "image_model": "gpt-image-1-mini",
    "run_mode": "deterministic_demo",
}

EXPLORATORY_PROFILES = [
    {
        "id": "identity_reference",
        "title": "Identity reference",
        "prompt_focus": (
            "Explore broad visual identity for a Toyota Supra A80 2JZ-GTE "
            "inline-six twin-turbo engine."
        ),
    },
    {
        "id": "system_reference",
        "title": "System reference",
        "prompt_focus": (
            "Explore a simplified engine-system composition without labels, "
            "dimensions, legends, arrows, or technical approval marks."
        ),
    },
]


def resolve_app_root() -> Path:
    explicit_root = os.environ.get("CONSTRAINTOS_APP_ROOT")
    if explicit_root:
        return Path(explicit_root).resolve()
    if getattr(sys, "frozen", False):
        executable_root = Path(sys.executable).resolve().parent
        if (executable_root / "scripts" / "exercise-constraintos.ps1").exists():
            return executable_root
        bundled_root = Path(getattr(sys, "_MEIPASS", executable_root)).resolve()
        if (bundled_root / "scripts" / "exercise-constraintos.ps1").exists():
            return bundled_root
        return executable_root
    return Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def latest_run_dir(repo_root: Path) -> Path | None:
    scenario_root = repo_root / "runs" / "output-poc" / SCENARIO
    if not scenario_root.exists():
        return None
    candidates = [item for item in scenario_root.iterdir() if item.is_dir()]
    return max(candidates, key=lambda item: item.stat().st_mtime) if candidates else None


def reference_source_roots(app_root: Path) -> list[Path]:
    candidates: list[Path] = []
    explicit_root = os.environ.get("CONSTRAINTOS_REFERENCE_SOURCE_ROOT")
    if explicit_root:
        candidates.append(Path(explicit_root).resolve())
    candidates.extend(
        [
            (app_root / "reference-sources").resolve(),
            (app_root.parent.parent / "reference-sources").resolve(),
        ]
    )
    unique: list[Path] = []
    for candidate in candidates:
        if candidate not in unique:
            unique.append(candidate)
    return unique


def source_plate_contract_path(app_root: Path) -> Path:
    return (
        app_root
        / "config"
        / "technical-source-plate-contracts"
        / "toyota-supra-a80-2jz-gte-v1.json"
    )


def technical_source_status(app_root: Path) -> dict[str, Any]:
    contract_path = source_plate_contract_path(app_root)
    if not contract_path.exists():
        return {
            "status": "blocked",
            "ready": False,
            "reason": "missing_source_plate_contract",
            "message": f"Missing registered source-plate contract: {contract_path}",
        }

    contract = read_json(contract_path)
    checked_roots: list[str] = []
    for source_root in reference_source_roots(app_root):
        checked_roots.append(str(source_root))
        package_root = source_root / REFERENCE_SCENARIO
        manifest_path = package_root / "source-package-manifest.json"
        if not manifest_path.exists():
            continue

        manifest = read_json(manifest_path)
        if manifest.get("preflight_status") != "source_files_materialized":
            return {
                "status": "blocked",
                "ready": False,
                "reason": "source_package_not_materialized",
                "manifest_path": str(manifest_path),
                "message": "The Toyota source package exists but is not materialized successfully.",
            }

        source_id = contract["canonical_source"]["source_id"]
        source_record = next(
            (
                item
                for item in manifest.get("materialized_sources", [])
                if item.get("source_id") == source_id
            ),
            None,
        )
        if source_record is None:
            return {
                "status": "blocked",
                "ready": False,
                "reason": "registered_source_missing",
                "manifest_path": str(manifest_path),
                "message": f"Materialized source package does not contain {source_id}.",
            }

        source_file = package_root / str(source_record["local_file"])
        if not source_file.exists():
            return {
                "status": "blocked",
                "ready": False,
                "reason": "source_file_missing",
                "source_file": str(source_file),
                "message": "The registered Toyota source plate file is missing.",
            }

        observed_digest = sha256_file(source_file)
        expected_digest = str(source_record.get("sha256", "")).lower()
        if not expected_digest or observed_digest != expected_digest:
            return {
                "status": "blocked",
                "ready": False,
                "reason": "source_digest_mismatch",
                "source_file": str(source_file),
                "expected_sha256": expected_digest,
                "observed_sha256": observed_digest,
                "message": "The registered Toyota source plate digest does not match its source-package manifest.",
            }

        return {
            "status": "ready",
            "ready": True,
            "scenario_id": REFERENCE_SCENARIO,
            "production_mode": "source_plate_annotation",
            "manifest_path": str(manifest_path),
            "source_file": str(source_file),
            "source_sha256": observed_digest,
            "contract_path": str(contract_path),
            "contract_id": contract["contract_id"],
            "render_preset_version": contract["render_preset_version"],
            "production_ready": False,
            "approval_allowed": False,
            "message": (
                "Registered Toyota source plate is present and digest-verified. "
                "A repeatable local source-backed draft can be rendered; production approval remains blocked."
            ),
        }

    return {
        "status": "blocked",
        "ready": False,
        "reason": "source_package_missing",
        "checked_roots": checked_roots,
        "message": (
            "No materialized Toyota source package was found. Run "
            "prepare-technical-reference-source-package.ps1 for toyota_supra_a80_2jz_gte, "
            "then rebuild or point CONSTRAINTOS_REFERENCE_SOURCE_ROOT to the reference-sources folder."
        ),
    }


def openai_api_key_value() -> str:
    return os.environ.get("OPENAI_API_KEY", "").strip()


def openai_api_key_looks_placeholder(api_key: str) -> bool:
    lowered = api_key.lower().strip()
    markers = [
        "your_api_key_here",
        "paste_your_key_here",
        "your_api",
        "api_key_here",
        "key_here",
        "replace_me",
        "example",
        "placeholder",
    ]
    return bool(lowered) and any(marker in lowered for marker in markers)


def provider_status() -> dict[str, Any]:
    api_key = openai_api_key_value()
    placeholder = openai_api_key_looks_placeholder(api_key)
    ready = bool(api_key) and not placeholder
    return {
        "provider": "openai_images_api",
        "endpoint": OPENAI_IMAGES_ENDPOINT,
        "api_key_visible_to_app": bool(api_key),
        "api_key_looks_placeholder": placeholder,
        "status": "ready" if ready else ("placeholder_api_key" if placeholder else "missing_api_key"),
        "message": (
            "Exploratory raster generation is available. It is not a technical drawing path."
            if ready
            else "Set a real OPENAI_API_KEY before launching the app to enable exploratory raster references."
        ),
    }


def require_ready_openai_api_key() -> str:
    api_key = openai_api_key_value()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not visible to this app process.")
    if openai_api_key_looks_placeholder(api_key):
        raise RuntimeError("OPENAI_API_KEY looks like placeholder text.")
    return api_key


def normalize_request(payload: dict[str, Any] | None) -> dict[str, Any]:
    raw = (payload or {}).get("demo_request", payload or {})
    if not isinstance(raw, dict):
        raw = {}
    request_text = str(raw.get("request_text") or DEFAULT_REQUEST["request_text"]).strip()
    focus = str(raw.get("requested_focus") or DEFAULT_REQUEST["requested_focus"]).strip()
    model = str(raw.get("image_model") or DEFAULT_REQUEST["image_model"]).strip()
    run_mode = str(raw.get("run_mode") or DEFAULT_REQUEST["run_mode"]).strip()
    try:
        output_count = int(raw.get("output_count", DEFAULT_REQUEST["output_count"]))
    except (TypeError, ValueError):
        output_count = int(DEFAULT_REQUEST["output_count"])
    output_count = max(1, min(output_count, len(EXPLORATORY_PROFILES)))
    if model not in {"gpt-image-1-mini", "gpt-image-1"}:
        model = DEFAULT_REQUEST["image_model"]
    if run_mode not in {"deterministic_demo", "exploratory_reference", "source_plate_render"}:
        run_mode = DEFAULT_REQUEST["run_mode"]
    return {
        "scenario_key": SCENARIO,
        "request_text": request_text,
        "requested_focus": focus,
        "output_count": output_count,
        "image_model": model,
        "run_mode": run_mode,
        "source": "browser_form",
    }


def persist_browser_request(run_dir: Path, request_payload: dict[str, Any]) -> Path:
    path = run_dir / "browser-request.json"
    write_json(
        path,
        {
            "browser_request": request_payload,
            "status": "captured",
            "note": "Captured before deterministic, exploratory, or source-backed rendering.",
        },
    )
    state_path = run_dir / "exercise-state.json"
    if state_path.exists():
        state = read_json(state_path)
        state["browser_request"] = request_payload
        artifacts = state.setdefault("generated_artifacts", [])
        if "browser-request.json" not in artifacts:
            artifacts.append("browser-request.json")
        write_json(state_path, state)
    return path


def build_exploratory_prompt(request_payload: dict[str, Any], profile: dict[str, str]) -> str:
    return (
        f"{request_payload['request_text']}\n\n"
        f"Exploratory reference: {profile['title']}.\n"
        f"Visual focus: {profile['prompt_focus']}\n"
        "This is a non-authoritative exploratory raster reference only. "
        "Do not include any words, letters, numbers, labels, legends, measurements, arrows, "
        "callout lines, diagrams, approval marks, or title blocks. "
        "Do not represent the output as a technical drawing, engineering diagram, or verified geometry."
    )


def provider_http_error_message(exc: urllib.error.HTTPError) -> str:
    _ = exc.read()
    if exc.code == 401:
        return "OpenAI rejected the API key with HTTP 401."
    if exc.code == 429:
        return "OpenAI returned HTTP 429 for rate limit, quota, or billing."
    return f"OpenAI exploratory image generation failed with HTTP {exc.code}."


def call_openai_image_generation(prompt: str, model: str, api_key: str) -> bytes:
    payload = {
        "model": model,
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "low",
        "output_format": "png",
    }
    request = urllib.request.Request(
        OPENAI_IMAGES_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:  # noqa: S310
            response_payload = json.loads(response.read().decode("utf-8-sig"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(provider_http_error_message(exc)) from exc

    image_payload = response_payload.get("data", [{}])[0]
    if image_payload.get("b64_json"):
        return base64.b64decode(image_payload["b64_json"])
    image_url = image_payload.get("url")
    if image_url:
        with urllib.request.urlopen(image_url, timeout=180) as image_response:  # noqa: S310
            return image_response.read()
    raise RuntimeError("OpenAI response did not include image bytes or an image URL.")


def generate_exploratory_references(
    run_dir: Path, request_payload: dict[str, Any]
) -> list[dict[str, Any]]:
    api_key = require_ready_openai_api_key()
    output_root = run_dir / "exploratory-generated-references"
    output_root.mkdir(parents=True, exist_ok=True)
    generated: list[dict[str, Any]] = []
    for index, profile in enumerate(
        EXPLORATORY_PROFILES[: int(request_payload["output_count"])], start=1
    ):
        prompt = build_exploratory_prompt(request_payload, profile)
        filename = f"{index:02d}-{profile['id']}.png"
        output_path = output_root / filename
        output_path.write_bytes(
            call_openai_image_generation(prompt, str(request_payload["image_model"]), api_key)
        )
        generated.append(
            {
                "id": profile["id"],
                "title": profile["title"],
                "provider": "openai_images_api",
                "model": request_payload["image_model"],
                "prompt": prompt,
                "output_file": f"exploratory-generated-references/{filename}",
                "artifact_role": "exploratory_reference_only",
                "technical_output_allowed": False,
                "approval_allowed": False,
            }
        )
        time.sleep(0.2)

    manifest = {
        "manifest_id": "constraintos-exploratory-reference-manifest/v1",
        "status": "complete",
        "artifact_role": "exploratory_reference_only",
        "technical_output_allowed": False,
        "production_approval_allowed": False,
        "generated_references": generated,
    }
    write_json(run_dir / "exploratory-reference-manifest.json", manifest)
    return generated


def previous_source_plate_digest(repo_root: Path, current_run_dir: Path) -> str | None:
    scenario_root = repo_root / "runs" / "output-poc" / SCENARIO
    if not scenario_root.exists():
        return None
    candidates = sorted(
        [item for item in scenario_root.iterdir() if item.is_dir() and item != current_run_dir],
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    for candidate in candidates:
        manifest_path = candidate / "technical-render-manifest.json"
        if manifest_path.exists():
            manifest = read_json(manifest_path)
            digest = manifest.get("output_sha256")
            if isinstance(digest, str) and digest:
                return digest
    return None


def render_registered_source_plate(
    app_root: Path, run_dir: Path
) -> dict[str, Any]:
    status = technical_source_status(app_root)
    if not status.get("ready"):
        raise RuntimeError(f"Source-backed technical render is blocked: {status['message']}")

    contract = read_json(Path(status["contract_path"]))
    source_path = Path(status["source_file"])
    output_root = run_dir / "technical-render"
    output_root.mkdir(parents=True, exist_ok=True)
    source_copy = output_root / "toyota-2jz-gte-source-plate.jpg"
    shutil.copyfile(source_path, source_copy)

    width = int(contract["output"]["width"])
    height = int(contract["output"]["height"])
    placement = contract["source_placement"]
    annotations = contract["annotations"]
    escaped_title = html.escape(annotations["title"])
    escaped_subtitle = html.escape(annotations["subtitle"])
    escaped_footer = html.escape(annotations["footer"])
    short_digest = str(status["source_sha256"])[:16]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  <rect x="24" y="24" width="{width - 48}" height="{height - 48}" fill="none" stroke="#172033" stroke-width="3"/>
  <text x="70" y="74" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="700" fill="#111827">{escaped_title}</text>
  <text x="70" y="112" font-family="Arial, Helvetica, sans-serif" font-size="21" fill="#374151">{escaped_subtitle}</text>
  <image href="toyota-2jz-gte-source-plate.jpg" x="{placement['x']}" y="{placement['y']}" width="{placement['width']}" height="{placement['height']}" preserveAspectRatio="xMidYMid meet"/>
  <line x1="70" y1="{height - 150}" x2="{width - 70}" y2="{height - 150}" stroke="#172033" stroke-width="2"/>
  <text x="70" y="{height - 105}" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#111827">{escaped_footer}</text>
  <text x="70" y="{height - 68}" font-family="Consolas, monospace" font-size="15" fill="#4b5563">Source SHA-256: {short_digest}… · Contract: {html.escape(contract['contract_id'])}</text>
  <text x="{width - 70}" y="{height - 68}" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#991b1b">SOURCE-BACKED DRAFT · MANUAL REVIEW REQUIRED</text>
</svg>
"""
    svg_path = output_root / "toyota-2jz-gte-source-backed-plate.svg"
    svg_path.write_text(svg, encoding="utf-8")
    output_digest = sha256_file(svg_path)
    previous_digest = previous_source_plate_digest(app_root, run_dir)
    comparison_status = (
        "baseline_created"
        if previous_digest is None
        else ("passed" if previous_digest == output_digest else "failed")
    )

    manifest = {
        "manifest_id": "constraintos-technical-render-manifest/v1",
        "scenario_id": REFERENCE_SCENARIO,
        "production_mode": "source_plate_annotation",
        "status": "complete" if comparison_status != "failed" else "blocked",
        "source_package_manifest": status["manifest_path"],
        "source_file": status["source_file"],
        "source_sha256": status["source_sha256"],
        "contract_id": contract["contract_id"],
        "render_preset_version": contract["render_preset_version"],
        "output_file": "technical-render/toyota-2jz-gte-source-backed-plate.svg",
        "output_sha256": output_digest,
        "repeat_render_comparison": {
            "status": comparison_status,
            "previous_output_sha256": previous_digest,
            "current_output_sha256": output_digest,
        },
        "generated_text_inside_source_raster": False,
        "annotation_source": "registered_source_plate_contract",
        "approval_allowed": False,
        "review_decision": "needs_review",
    }
    write_json(run_dir / "technical-render-manifest.json", manifest)
    if comparison_status == "failed":
        raise RuntimeError(
            "Repeat-render comparison failed: the deterministic source-backed SVG changed."
        )
    return manifest


def run_exercise_pipeline(app_root: Path, request_payload: dict[str, Any]) -> dict[str, Any]:
    script = app_root / "scripts" / "exercise-constraintos.ps1"
    if not script.exists():
        raise FileNotFoundError(f"Missing workbench exercise script: {script}")
    completed = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
            "-NoOpenBrowser",
        ],
        cwd=str(app_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "ConstraintOS exercise pipeline failed.\n"
            f"Exit code: {completed.returncode}\n\n"
            f"STDOUT:\n{completed.stdout}\n\nSTDERR:\n{completed.stderr}"
        )

    run_dir = latest_run_dir(app_root)
    if run_dir is None:
        raise RuntimeError("Pipeline completed but no run directory was found.")
    workbench = run_dir / "exercise-workbench.html"
    exercise_state = run_dir / "exercise-state.json"
    if not workbench.exists() or not exercise_state.exists():
        raise RuntimeError("Pipeline did not create the expected workbench artifacts.")

    browser_request = persist_browser_request(run_dir, request_payload)
    exploratory: list[dict[str, Any]] = []
    technical_render: dict[str, Any] | None = None
    if request_payload["run_mode"] == "exploratory_reference":
        exploratory = generate_exploratory_references(run_dir, request_payload)
    elif request_payload["run_mode"] == "source_plate_render":
        technical_render = render_registered_source_plate(app_root, run_dir)

    response_exploratory: list[dict[str, Any]] = []
    for item in exploratory:
        image_path = run_dir / item["output_file"]
        response_exploratory.append(
            {
                **item,
                "image_url": f"/artifact/{image_path.relative_to(app_root).as_posix()}",
            }
        )

    technical_render_url = None
    technical_manifest_url = None
    if technical_render:
        render_path = run_dir / technical_render["output_file"]
        technical_render_url = f"/artifact/{render_path.relative_to(app_root).as_posix()}"
        manifest_path = run_dir / "technical-render-manifest.json"
        technical_manifest_url = (
            f"/artifact/{manifest_path.relative_to(app_root).as_posix()}"
        )

    return {
        "status": "complete",
        "scenario_key": SCENARIO,
        "run_mode": request_payload["run_mode"],
        "run_dir": str(run_dir),
        "request_text": request_payload["request_text"],
        "exploratory_references": response_exploratory,
        "technical_render": technical_render,
        "technical_render_url": technical_render_url,
        "technical_render_manifest_url": technical_manifest_url,
        "workbench_url": f"/artifact/{workbench.relative_to(app_root).as_posix()}",
        "exercise_state_url": f"/artifact/{exercise_state.relative_to(app_root).as_posix()}",
        "browser_request_url": f"/artifact/{browser_request.relative_to(app_root).as_posix()}",
        "stdout": completed.stdout,
    }


def html_page() -> str:
    return r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>ConstraintOS Workbench</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, Segoe UI, Arial, sans-serif; background:#060913; color:#edf3ff; }
    body { margin:0; min-height:100vh; background:radial-gradient(circle at top left,#243b72 0,#111b36 35%,#060913 100%); }
    header { padding:34px 42px 22px; border-bottom:1px solid rgba(255,255,255,.12); }
    main { padding:26px 42px 44px; display:grid; gap:20px; }
    h1 { margin:0 0 8px; font-size:clamp(34px,5vw,58px); letter-spacing:-.05em; }
    p { color:#bdc9df; line-height:1.5; }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; }
    .card { background:rgba(10,17,34,.84); border:1px solid rgba(255,255,255,.14); border-radius:20px; padding:21px; box-shadow:0 18px 40px rgba(0,0,0,.28); }
    .input-card { grid-column:span 2; }
    label { display:block; font-weight:700; margin:13px 0 6px; }
    textarea,select { width:100%; box-sizing:border-box; border-radius:12px; border:1px solid rgba(255,255,255,.16); background:rgba(255,255,255,.07); color:#edf3ff; padding:11px; font:inherit; }
    textarea { min-height:105px; }
    option { color:#07111f; }
    button { border:0; border-radius:14px; padding:14px 18px; font-size:16px; font-weight:700; color:#07111f; cursor:pointer; margin:0 7px 8px 0; }
    button:disabled { opacity:.42; cursor:not-allowed; }
    .demo { background:#9bd4ff; }
    .explore { background:#ffd166; }
    .render { background:#83f2bf; }
    .status { white-space:pre-wrap; background:rgba(255,255,255,.06); border-radius:12px; padding:13px; color:#dce8ff; }
    .pill { display:inline-block; margin:4px 6px 4px 0; padding:7px 10px; border-radius:999px; border:1px solid rgba(132,190,255,.3); color:#dcebff; font-size:13px; }
    .warn { color:#fff2c5; border-color:rgba(255,206,86,.35); }
    .blocked { color:#ffd9e3; border-color:rgba(255,99,132,.35); }
    .image-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:15px; }
    .image-card img,.technical-frame { width:100%; border-radius:12px; background:white; }
    .technical-frame { min-height:760px; border:0; }
    iframe.workbench { width:100%; min-height:760px; border:1px solid rgba(255,255,255,.16); border-radius:18px; background:white; }
    a { color:#9bd4ff; }
    .muted { color:#9fafc9; font-size:13px; }
    @media(max-width:900px){.input-card{grid-column:span 1}}
  </style>
</head>
<body>
<header>
  <span class="pill">Portable Workbench App</span>
  <span class="pill warn">source-backed rendering</span>
  <span class="pill blocked">manual review only</span>
  <h1>ConstraintOS Workbench</h1>
  <p>Deterministic demos, explicitly exploratory generated references, and a source-backed Toyota technical plate using the materialized official web reference package.</p>
</header>
<main>
  <section class="grid">
    <div class="card input-card">
      <h2>Browser request</h2>
      <label for="requestText">Request</label>
      <textarea id="requestText">Create a source-backed technical plate for the Toyota Supra A80 2JZ-GTE twin-turbo engine while preserving manual review.</textarea>
      <label for="outputCount">Exploratory reference count</label>
      <select id="outputCount"><option value="2" selected>2</option><option value="1">1</option></select>
      <label for="imageModel">Exploratory image model</label>
      <select id="imageModel"><option value="gpt-image-1-mini" selected>gpt-image-1-mini</option><option value="gpt-image-1">gpt-image-1</option></select>
    </div>
    <div class="card"><h2>OpenAI exploratory provider</h2><div id="providerStatus" class="status">Checking...</div></div>
    <div class="card"><h2>Registered Toyota source package</h2><div id="sourceStatus" class="status">Checking...</div></div>
    <div class="card">
      <h2>Run</h2>
      <p>The image model is exploratory only. The green action uses the registered source plate and deterministic SVG composition.</p>
      <button id="demoButton" class="demo">Run Deterministic Demo</button>
      <button id="exploreButton" class="explore">Explore Generated Raster References</button>
      <button id="renderButton" class="render">Render Registered Toyota Source Plate</button>
    </div>
    <div class="card"><h2>Safety</h2><span class="pill warn">needs_review</span><span class="pill blocked">approval_allowed: false</span><p>Generated raster references cannot enter the technical approval path.</p></div>
  </section>
  <section class="card"><h2>App status</h2><div id="status" class="status">Ready.</div><p id="artifactLinks"></p></section>
  <section class="card" id="technicalCard" style="display:none"><h2>Source-Backed Toyota Technical Plate</h2><p>Built from the digest-verified official Toyota source plate and deterministic registered metadata overlay.</p><iframe id="technicalFrame" class="technical-frame"></iframe><p id="technicalLinks"></p></section>
  <section class="card" id="exploratoryCard" style="display:none"><h2>Exploratory Generated Raster References</h2><p>These images may invent geometry. They are not technical drawings and have no production approval path.</p><div id="exploratoryImages" class="image-grid"></div></section>
  <section class="card" id="workbenchCard" style="display:none"><h2>Generated ConstraintOS Workbench</h2><iframe id="workbenchFrame" class="workbench"></iframe></section>
</main>
<script>
let providerReady=false;
let sourceReady=false;
function requestPayload(runMode){return{scenario_key:'supra_2jz_gte_twin_turbo',request_text:document.getElementById('requestText').value,requested_focus:'technical_comparison',output_count:Number(document.getElementById('outputCount').value),image_model:document.getElementById('imageModel').value,run_mode:runMode};}
async function refreshStatuses(){
  const provider=await fetch('/api/provider-status').then(r=>r.json());
  providerReady=provider.status==='ready';
  document.getElementById('providerStatus').textContent='Status: '+provider.status+'\nAPI key visible: '+provider.api_key_visible_to_app+'\nPlaceholder detected: '+provider.api_key_looks_placeholder+'\n'+provider.message;
  document.getElementById('exploreButton').disabled=!providerReady;
  const source=await fetch('/api/source-status').then(r=>r.json());
  sourceReady=source.ready===true;
  document.getElementById('sourceStatus').textContent='Status: '+source.status+'\nReady for local source-backed draft: '+sourceReady+'\nProduction ready: '+(source.production_ready===true)+'\n'+source.message;
  document.getElementById('renderButton').disabled=!sourceReady;
}
function renderExploratory(items){
  const card=document.getElementById('exploratoryCard');
  const box=document.getElementById('exploratoryImages');
  box.innerHTML='';
  if(!items||items.length===0){card.style.display='none';return;}
  items.forEach(item=>{const node=document.createElement('div');node.className='card image-card';node.innerHTML='<h3>'+item.title+'</h3><img src="'+item.image_url+'" alt="'+item.title+'"/><p class="muted">Exploratory only · Technical output allowed: false · Approval allowed: false</p>';box.appendChild(node);});
  card.style.display='block';
}
async function run(runMode){
  if(runMode==='exploratory_reference'&&!providerReady){return;}
  if(runMode==='source_plate_render'&&!sourceReady){return;}
  const buttons=['demoButton','exploreButton','renderButton'].map(id=>document.getElementById(id));
  buttons.forEach(button=>button.disabled=true);
  document.getElementById('technicalCard').style.display='none';
  document.getElementById('exploratoryCard').style.display='none';
  document.getElementById('workbenchCard').style.display='none';
  const status=document.getElementById('status');
  status.textContent='Running '+runMode+'...';
  try{
    const response=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({demo_request:requestPayload(runMode)})});
    const data=await response.json();
    if(!response.ok){throw new Error(data.error||'Unknown failure');}
    status.textContent='Complete.\nMode: '+data.run_mode+'\nRun directory: '+data.run_dir+'\nApproval allowed: false';
    document.getElementById('artifactLinks').innerHTML='<a href="'+data.workbench_url+'" target="_blank">Open generated workbench</a> · <a href="'+data.exercise_state_url+'" target="_blank">Open exercise state</a> · <a href="'+data.browser_request_url+'" target="_blank">Open captured browser request</a>';
    renderExploratory(data.exploratory_references||[]);
    if(data.technical_render_url){
      document.getElementById('technicalFrame').src=data.technical_render_url;
      document.getElementById('technicalLinks').innerHTML='<a href="'+data.technical_render_url+'" target="_blank">Open source-backed SVG</a> · <a href="'+data.technical_render_manifest_url+'" target="_blank">Open technical render manifest</a>';
      document.getElementById('technicalCard').style.display='block';
    }
    document.getElementById('workbenchFrame').src=data.workbench_url;
    document.getElementById('workbenchCard').style.display='block';
  }catch(error){status.textContent='ConstraintOS run failed.\n\n'+error;}
  finally{document.getElementById('demoButton').disabled=false;document.getElementById('exploreButton').disabled=!providerReady;document.getElementById('renderButton').disabled=!sourceReady;}
}
document.addEventListener('DOMContentLoaded',()=>{document.getElementById('demoButton').onclick=()=>run('deterministic_demo');document.getElementById('exploreButton').onclick=()=>run('exploratory_reference');document.getElementById('renderButton').onclick=()=>run('source_plate_render');refreshStatuses();});
</script>
</body>
</html>"""


class WorkbenchHandler(BaseHTTPRequestHandler):
    app_root = resolve_app_root()

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        return

    def _send_text(
        self,
        status: HTTPStatus,
        text: str,
        content_type: str = "text/plain; charset=utf-8",
    ) -> None:
        encoded = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        self._send_text(status, json.dumps(payload, indent=2), "application/json; charset=utf-8")

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8-sig"))

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            self._send_text(HTTPStatus.OK, html_page(), "text/html; charset=utf-8")
            return
        if parsed.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok", "scenario_key": SCENARIO})
            return
        if parsed.path == "/api/provider-status":
            self._send_json(HTTPStatus.OK, provider_status())
            return
        if parsed.path == "/api/source-status":
            self._send_json(HTTPStatus.OK, technical_source_status(self.app_root))
            return
        if parsed.path.startswith("/artifact/"):
            self._serve_artifact(parsed.path.removeprefix("/artifact/"))
            return
        self._send_text(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/api/run":
            self._send_text(HTTPStatus.NOT_FOUND, "Not found")
            return
        try:
            request_payload = normalize_request(self._read_json_body())
        except Exception as exc:  # noqa: BLE001
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"status": "failed", "error": f"Invalid browser request JSON: {exc}"},
            )
            return
        with RUN_LOCK:
            try:
                result = run_exercise_pipeline(self.app_root, request_payload)
                self._send_json(HTTPStatus.OK, result)
            except Exception as exc:  # noqa: BLE001
                self._send_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"status": "failed", "error": str(exc)},
                )

    def _serve_artifact(self, relative_path: str) -> None:
        safe_path = posixpath.normpath(urllib.parse.unquote(relative_path)).lstrip("/")
        artifact_path = (self.app_root / safe_path).resolve()
        runs_root = (self.app_root / "runs").resolve()
        if (
            not str(artifact_path).startswith(str(runs_root))
            or not artifact_path.exists()
            or not artifact_path.is_file()
        ):
            self._send_text(HTTPStatus.NOT_FOUND, "Artifact not found")
            return
        content_type = "text/plain; charset=utf-8"
        suffix = artifact_path.suffix.lower()
        if suffix in {".html", ".htm"}:
            content_type = "text/html; charset=utf-8"
        elif suffix == ".json":
            content_type = "application/json; charset=utf-8"
        elif suffix == ".svg":
            content_type = "image/svg+xml"
        elif suffix == ".png":
            content_type = "image/png"
        elif suffix in {".jpg", ".jpeg"}:
            content_type = "image/jpeg"
        payload = artifact_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> int:
    server = ThreadingHTTPServer((HOST, PORT), WorkbenchHandler)
    url = f"http://{HOST}:{PORT}/"
    print("ConstraintOS Workbench app running.")
    print(f"Open: {url}")
    print("Close this window to stop the local app server.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
