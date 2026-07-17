from __future__ import annotations

import json
import os
import posixpath
import subprocess
import sys
import threading
import urllib.parse
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

HOST = "127.0.0.1"
PORT = int(os.environ.get("CONSTRAINTOS_WORKBENCH_PORT", "8787"))
SCENARIO = "supra_2jz_gte_twin_turbo"
RUN_LOCK = threading.Lock()
DEFAULT_DEMO_REQUEST: dict[str, Any] = {
    "scenario_key": SCENARIO,
    "request_text": "Create a technical graphic for a Toyota Supra A80 2JZ-GTE twin-turbo engine that demonstrates controlled output permutations and preserves manual review.",
    "requested_focus": "technical_comparison",
    "output_count": 4,
}
APP_STATE: dict[str, Any] = {
    "status": "idle",
    "scenario_key": SCENARIO,
    "message": "Ready to run ConstraintOS.",
}


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


def latest_run_dir(repo_root: Path) -> Path | None:
    scenario_root = repo_root / "runs" / "output-poc" / SCENARIO
    if not scenario_root.exists():
        return None
    run_dirs = [path for path in scenario_root.iterdir() if path.is_dir()]
    if not run_dirs:
        return None
    return max(run_dirs, key=lambda path: path.stat().st_mtime)


def normalize_demo_request(payload: dict[str, Any] | None) -> dict[str, Any]:
    raw_request = (payload or {}).get("demo_request", payload or {})
    if not isinstance(raw_request, dict):
        raw_request = {}

    request_text = str(raw_request.get("request_text") or DEFAULT_DEMO_REQUEST["request_text"]).strip()
    requested_focus = str(raw_request.get("requested_focus") or DEFAULT_DEMO_REQUEST["requested_focus"]).strip()
    output_count_raw = raw_request.get("output_count", DEFAULT_DEMO_REQUEST["output_count"])
    try:
        output_count = int(output_count_raw)
    except (TypeError, ValueError):
        output_count = int(DEFAULT_DEMO_REQUEST["output_count"])

    output_count = max(1, min(output_count, 4))
    if not request_text:
        request_text = DEFAULT_DEMO_REQUEST["request_text"]
    if requested_focus not in {"technical_comparison", "turbo_system", "inline_six_identity", "reviewer_safe"}:
        requested_focus = DEFAULT_DEMO_REQUEST["requested_focus"]

    return {
        "scenario_key": SCENARIO,
        "request_text": request_text,
        "requested_focus": requested_focus,
        "output_count": output_count,
        "source": "browser_form",
    }


def persist_browser_request(run_dir: Path, demo_request: dict[str, Any]) -> Path:
    request_path = run_dir / "browser-request.json"
    request_payload = {
        "browser_request": demo_request,
        "status": "captured",
        "note": "This request was submitted from the ConstraintOS Workbench browser UI and captured before manual-review output generation.",
    }
    request_path.write_text(json.dumps(request_payload, indent=2), encoding="utf-8")

    exercise_state_path = run_dir / "exercise-state.json"
    if exercise_state_path.exists():
        exercise_state = json.loads(exercise_state_path.read_text(encoding="utf-8-sig"))
        exercise_state["browser_request"] = demo_request
        artifacts = exercise_state.setdefault("generated_artifacts", [])
        if "browser-request.json" not in artifacts:
            artifacts.append("browser-request.json")
        exercise_state_path.write_text(json.dumps(exercise_state, indent=2), encoding="utf-8")
    return request_path


def run_exercise_pipeline(repo_root: Path, demo_request: dict[str, Any]) -> dict[str, Any]:
    script = repo_root / "scripts" / "exercise-constraintos.ps1"
    if not script.exists():
        raise FileNotFoundError(f"Missing workbench exercise script: {script}")

    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        "-NoOpenBrowser",
    ]
    completed = subprocess.run(
        command,
        cwd=str(repo_root),
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

    run_dir = latest_run_dir(repo_root)
    if run_dir is None:
        raise RuntimeError("ConstraintOS exercise pipeline completed but no run directory was found.")

    workbench = run_dir / "exercise-workbench.html"
    exercise_state = run_dir / "exercise-state.json"
    if not workbench.exists():
        raise RuntimeError(f"Exercise workbench was not created: {workbench}")
    if not exercise_state.exists():
        raise RuntimeError(f"Exercise state was not created: {exercise_state}")

    browser_request = persist_browser_request(run_dir, demo_request)
    relative_workbench = workbench.relative_to(repo_root).as_posix()
    relative_state = exercise_state.relative_to(repo_root).as_posix()
    relative_request = browser_request.relative_to(repo_root).as_posix()

    return {
        "status": "complete",
        "scenario_key": SCENARIO,
        "run_dir": str(run_dir),
        "request_text": demo_request["request_text"],
        "requested_focus": demo_request["requested_focus"],
        "output_count": demo_request["output_count"],
        "workbench_url": f"/artifact/{relative_workbench}",
        "exercise_state_url": f"/artifact/{relative_state}",
        "browser_request_url": f"/artifact/{relative_request}",
        "message": "ConstraintOS workbench run complete.",
        "stdout": completed.stdout,
    }


def html_page() -> str:
    return r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ConstraintOS Workbench App</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, Segoe UI, Arial, sans-serif; background: #060913; color: #edf3ff; }
    body { margin: 0; min-height: 100vh; background: radial-gradient(circle at top left, #243b72 0, #111b36 35%, #060913 100%); }
    header { padding: 38px 44px 24px; border-bottom: 1px solid rgba(255,255,255,.12); }
    main { padding: 28px 44px 44px; display: grid; gap: 22px; }
    h1 { margin: 0 0 10px; font-size: clamp(34px, 5vw, 58px); letter-spacing: -.05em; }
    p { color: #bdc9df; line-height: 1.55; }
    label { display: block; color: #e8f1ff; font-weight: 700; margin: 14px 0 6px; }
    textarea, select { width: 100%; box-sizing: border-box; border-radius: 14px; border: 1px solid rgba(255,255,255,.16); background: rgba(255,255,255,.07); color: #edf3ff; padding: 12px; font: inherit; }
    textarea { min-height: 118px; resize: vertical; }
    option { color: #07111f; }
    button { appearance: none; border: 0; border-radius: 16px; padding: 16px 22px; font-size: 17px; font-weight: 700; color: #07111f; background: #83f2bf; cursor: pointer; box-shadow: 0 18px 36px rgba(0,0,0,.28); }
    button:disabled { opacity: .55; cursor: not-allowed; }
    .subhead { max-width: 960px; font-size: 18px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
    .card { background: rgba(10, 17, 34, .82); border: 1px solid rgba(255,255,255,.14); border-radius: 20px; padding: 22px; box-shadow: 0 18px 40px rgba(0,0,0,.28); }
    .input-card { grid-column: span 2; }
    .pill { display: inline-block; margin: 4px 6px 4px 0; padding: 8px 11px; border-radius: 999px; background: rgba(132, 190, 255, .14); border: 1px solid rgba(132,190,255,.3); color: #dcebff; font-size: 13px; }
    .ok { background: rgba(95, 214, 157, .12); border-color: rgba(95, 214, 157, .35); color: #d9ffe9; }
    .warn { background: rgba(255, 206, 86, .13); border-color: rgba(255,206,86,.35); color: #fff2c5; }
    .blocked { background: rgba(255, 99, 132, .12); border-color: rgba(255,99,132,.35); color: #ffd9e3; }
    .status { white-space: pre-wrap; color: #dce8ff; background: rgba(255,255,255,.06); border-radius: 14px; padding: 14px; }
    iframe { width: 100%; min-height: 760px; border: 1px solid rgba(255,255,255,.16); border-radius: 20px; background: white; }
    a { color: #9bd4ff; }
    @media (max-width: 900px) { .input-card { grid-column: span 1; } }
  </style>
</head>
<body>
  <header>
    <span class="pill ok">Portable Workbench App</span>
    <span class="pill">localhost</span>
    <span class="pill blocked">manual review only</span>
    <h1>ConstraintOS Workbench</h1>
    <p class="subhead">A one-click local demo app. Describe what you want, click Run Demo, and the browser sends that request through the ConstraintOS pipeline.</p>
  </header>
  <main>
    <section class="grid">
      <div class="card input-card">
        <h2>Browser request input</h2>
        <p>This is the request that will be captured as <code>browser-request.json</code> and attached to the generated exercise state.</p>
        <label for="requestText">Graphic request</label>
        <textarea id="requestText">Create a technical graphic for a Toyota Supra A80 2JZ-GTE twin-turbo engine that demonstrates controlled output permutations and preserves manual review.</textarea>
        <label for="requestedFocus">Output focus</label>
        <select id="requestedFocus">
          <option value="technical_comparison">Technical comparison</option>
          <option value="turbo_system">Turbo system focus</option>
          <option value="inline_six_identity">Inline-six identity focus</option>
          <option value="reviewer_safe">Reviewer-safe minimal focus</option>
        </select>
        <label for="outputCount">Output count</label>
        <select id="outputCount">
          <option value="4" selected>4 candidate outputs</option>
          <option value="3">3 candidate outputs</option>
          <option value="2">2 candidate outputs</option>
          <option value="1">1 candidate output</option>
        </select>
      </div>
      <div class="card">
        <h2>Run the app</h2>
        <p>No terminal command required for the recipient. The app runs the local pipeline behind this browser UI.</p>
        <button id="runButton" type="button">Run ConstraintOS Demo</button>
      </div>
      <div class="card">
        <h2>Safety state</h2>
        <p>Generated results remain reviewer candidates. Approval is blocked until a human reviewer decides what to do next.</p>
        <span class="pill warn">needs_review</span>
        <span class="pill blocked">approval_allowed: false</span>
      </div>
    </section>

    <section class="card">
      <h2>App status</h2>
      <div id="status" class="status">Ready to run ConstraintOS.</div>
      <p id="artifactLinks"></p>
    </section>

    <section class="card" id="workbenchCard" style="display:none">
      <h2>Generated Workbench</h2>
      <iframe id="workbenchFrame" title="ConstraintOS generated workbench"></iframe>
    </section>
  </main>

  <script>
    function readDemoRequest() {
      return {
        scenario_key: 'supra_2jz_gte_twin_turbo',
        request_text: document.getElementById('requestText').value,
        requested_focus: document.getElementById('requestedFocus').value,
        output_count: Number(document.getElementById('outputCount').value)
      };
    }

    async function runDemo() {
      const button = document.getElementById('runButton');
      const status = document.getElementById('status');
      const links = document.getElementById('artifactLinks');
      const card = document.getElementById('workbenchCard');
      const frame = document.getElementById('workbenchFrame');
      const demoRequest = readDemoRequest();
      button.disabled = true;
      links.innerHTML = '';
      card.style.display = 'none';
      frame.removeAttribute('src');
      status.textContent = 'Browser request received.\n\n' + demoRequest.request_text + '\n\nRunning ConstraintOS pipeline...';
      try {
        const response = await fetch('/api/run', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ demo_request: demoRequest })
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || 'Unknown ConstraintOS failure');
        }
        status.textContent = 'Complete.\n\nRequest: ' + data.request_text + '\nFocus: ' + data.requested_focus + '\nOutputs requested: ' + data.output_count + '\nRun directory: ' + data.run_dir + '\nDecision: needs_review\nApproval allowed: false';
        links.innerHTML = '<a href="' + data.workbench_url + '" target="_blank">Open generated workbench</a> · <a href="' + data.exercise_state_url + '" target="_blank">Open exercise state JSON</a> · <a href="' + data.browser_request_url + '" target="_blank">Open captured browser request</a>';
        frame.src = data.workbench_url;
        card.style.display = 'block';
      } catch (error) {
        status.textContent = 'ConstraintOS run failed.\n\n' + error;
      } finally {
        button.disabled = false;
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      const button = document.getElementById('runButton');
      const status = document.getElementById('status');
      button.addEventListener('click', runDemo);
      status.textContent = 'Ready to run ConstraintOS. Edit the browser request, then click Run ConstraintOS Demo.';
    });
  </script>
</body>
</html>"""


class WorkbenchHandler(BaseHTTPRequestHandler):
    repo_root = resolve_app_root()

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        return

    def _send_text(self, status: HTTPStatus, text: str, content_type: str = "text/plain; charset=utf-8") -> None:
        encoded = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        self._send_text(status, json.dumps(payload, indent=2), "application/json; charset=utf-8")

    def _read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        if content_length == 0:
            return {}
        raw_body = self.rfile.read(content_length).decode("utf-8-sig")
        return json.loads(raw_body)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            self._send_text(HTTPStatus.OK, html_page(), "text/html; charset=utf-8")
            return
        if parsed.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok", "scenario_key": SCENARIO})
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
            payload = self._read_json_body()
            demo_request = normalize_demo_request(payload)
        except Exception as exc:  # noqa: BLE001
            self._send_json(HTTPStatus.BAD_REQUEST, {"status": "failed", "error": f"Invalid browser request JSON: {exc}"})
            return
        with RUN_LOCK:
            APP_STATE.update({"status": "running", "message": "ConstraintOS pipeline is running.", "browser_request": demo_request})
            try:
                result = run_exercise_pipeline(self.repo_root, demo_request)
                APP_STATE.update(result)
                self._send_json(HTTPStatus.OK, result)
            except Exception as exc:  # noqa: BLE001
                error = {"status": "failed", "error": str(exc)}
                APP_STATE.update(error)
                self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, error)

    def _serve_artifact(self, relative_path: str) -> None:
        safe_path = posixpath.normpath(urllib.parse.unquote(relative_path)).lstrip("/")
        artifact_path = (self.repo_root / safe_path).resolve()
        runs_root = (self.repo_root / "runs").resolve()
        if not str(artifact_path).startswith(str(runs_root)) or not artifact_path.exists() or not artifact_path.is_file():
            self._send_text(HTTPStatus.NOT_FOUND, "Artifact not found")
            return
        content_type = "text/plain; charset=utf-8"
        if artifact_path.suffix.lower() in {".html", ".htm"}:
            content_type = "text/html; charset=utf-8"
        elif artifact_path.suffix.lower() == ".json":
            content_type = "application/json; charset=utf-8"
        elif artifact_path.suffix.lower() == ".svg":
            content_type = "image/svg+xml"
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
