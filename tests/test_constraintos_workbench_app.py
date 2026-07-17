from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "constraintos_workbench" / "app.py"
PACKAGER = ROOT / "scripts" / "package-constraintos-workbench-app.ps1"


def test_constraintos_workbench_app_server_exists_and_targets_localhost() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "HOST = \"127.0.0.1\"",
        "PORT = int(os.environ.get(\"CONSTRAINTOS_WORKBENCH_PORT\", \"8787\"))",
        "ThreadingHTTPServer",
        "webbrowser.open(url)",
        "ConstraintOS Workbench app running.",
        "Close this window to stop the local app server.",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_serves_pretty_browser_front_door() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "ConstraintOS Workbench App",
        "Portable Workbench App",
        "Run ConstraintOS Demo",
        "Browser request input",
        "Run the app",
        "Safety state",
        "App status",
        "Generated Workbench",
        "manual review only",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_binds_button_with_valid_javascript() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "return r\"\"\"<!doctype html>",
        '<button id="runButton" type="button">Run ConstraintOS Demo</button>',
        "async function runDemo()",
        "document.addEventListener('DOMContentLoaded'",
        "button.addEventListener('click', runDemo)",
        "Browser request received.\\n\\n",
        "Ready to run ConstraintOS. Edit the browser request, optionally enable real images, then click Run ConstraintOS Demo.",
        "frame.removeAttribute('src')",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_accepts_browser_request_input() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "def normalize_demo_request(payload: dict[str, Any] | None)",
        "requestText",
        "requestedFocus",
        "outputCount",
        "function readDemoRequest()",
        "request_text: document.getElementById('requestText').value",
        "requested_focus: document.getElementById('requestedFocus').value",
        "output_count: Number(document.getElementById('outputCount').value)",
        "body: JSON.stringify({ demo_request: demoRequest })",
        "Open captured browser request",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_persists_browser_request_and_handles_bom_json() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "def read_json_file(path: Path) -> dict[str, Any]",
        "encoding=\"utf-8-sig\"",
        "def persist_browser_request(run_dir: Path, demo_request: dict[str, Any]) -> Path",
        "browser-request.json",
        "write_json_file(request_path, request_payload)",
        "exercise_state[\"browser_request\"] = demo_request",
        "browser_request_url",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_runs_pipeline_from_browser_api() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "def run_exercise_pipeline(repo_root: Path, demo_request: dict[str, Any])",
        'script = repo_root / "scripts" / "exercise-constraintos.ps1"',
        '"powershell.exe"',
        '"-ExecutionPolicy"',
        '"Bypass"',
        '"-NoOpenBrowser"',
        'if parsed.path != "/api/run"',
        "fetch('/api/run', {",
        "RUN_LOCK",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_supports_optional_openai_image_generation() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        'OPENAI_IMAGES_ENDPOINT = "https://api.openai.com/v1/images/generations"',
        "enableRealImages",
        "Generate real image candidates with OpenAI Images API",
        "OPENAI_API_KEY",
        '"gpt-image-1-mini"',
        '"gpt-image-1"',
        "def call_openai_image_generation(prompt: str, model: str, api_key: str) -> bytes",
        "urllib.request.Request",
        '"Authorization": f"Bearer {api_key}"',
        '"output_format": "png"',
        "base64.b64decode(b64_json)",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_writes_real_image_artifacts_for_manual_review() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "def generate_real_images(repo_root: Path, run_dir: Path, demo_request: dict[str, Any]) -> list[dict[str, Any]]",
        "generated-images",
        "real-image-generation-manifest.json",
        "openai_images_api",
        "review_decision",
        "needs_review",
        "approval_allowed",
        "False",
        "real_image_generation",
        "generated_images",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_renders_real_image_cards_and_serves_pngs() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "Generated Real Image Candidates",
        "renderGeneratedImages(data.generated_images || [])",
        "Open PNG artifact",
        "image_url",
        'elif artifact_path.suffix.lower() == ".png"',
        'content_type = "image/png"',
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_returns_generated_workbench_artifacts() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "exercise-workbench.html",
        "exercise-state.json",
        "workbench_url",
        "exercise_state_url",
        "generated workbench",
        "Open generated workbench",
        "Open exercise state JSON",
        "needs_review",
        "approval_allowed: false",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_serves_only_run_artifacts() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        'if parsed.path.startswith("/artifact/")',
        "def _serve_artifact",
        'runs_root = (self.repo_root / "runs").resolve()',
        "Artifact not found",
        'content_type = "text/html; charset=utf-8"',
        'content_type = "application/json; charset=utf-8"',
        'content_type = "image/svg+xml"',
        'content_type = "image/png"',
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_packager_builds_portable_app_folder() -> None:
    content = PACKAGER.read_text(encoding="utf-8")

    expected = [
        'apps\\constraintos_workbench\\app.py',
        'dist',
        'ConstraintOS Workbench',
        'ConstraintOS Workbench.exe',
        'python -m venv',
        'pip install --upgrade pip pyinstaller',
        '--onedir',
        '--name "ConstraintOS Workbench"',
        'Copy-Item -Recurse -Force (Join-Path $RepoRoot "scripts")',
        'README-FIRST.txt',
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_packaged_readme_is_recipient_facing() -> None:
    content = PACKAGER.read_text(encoding="utf-8")

    expected = [
        "Double-click: ConstraintOS Workbench.exe",
        "Your browser will open to the local Workbench app.",
        "Edit the browser request if desired.",
        "Click: Run ConstraintOS Demo",
        "It does not require the recipient to open the repository.",
        "It does not require typing PowerShell commands.",
        "Close the app window to stop the local server.",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_packaged_readme_documents_optional_real_images() -> None:
    content = PACKAGER.read_text(encoding="utf-8")

    expected = [
        "Optional real image generation:",
        "OPENAI_API_KEY",
        "Do not place the API key in this app folder or commit it to source control.",
        "OpenAI Images API",
        "PNG candidates",
        "needs_review",
        "approval_allowed: false",
    ]
    for item in expected:
        assert item in content
