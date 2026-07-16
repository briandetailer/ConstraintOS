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
        "Demo input",
        "Run the app",
        "Safety state",
        "App status",
        "Generated Workbench",
        "manual review only",
    ]
    for item in expected:
        assert item in content


def test_constraintos_workbench_app_runs_pipeline_from_browser_api() -> None:
    content = APP.read_text(encoding="utf-8")

    expected = [
        "def run_exercise_pipeline(repo_root: Path)",
        'script = repo_root / "scripts" / "exercise-constraintos.ps1"',
        '"powershell.exe"',
        '"-ExecutionPolicy"',
        '"Bypass"',
        '"-NoOpenBrowser"',
        'if parsed.path != "/api/run"',
        "fetch('/api/run', { method: 'POST' })",
        "RUN_LOCK",
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
        "Click: Run ConstraintOS Demo",
        "It does not require the recipient to open the repository.",
        "It does not require typing PowerShell commands.",
        "Close the app window to stop the local server.",
    ]
    for item in expected:
        assert item in content
