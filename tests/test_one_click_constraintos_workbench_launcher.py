from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "Launch-ConstraintOS-Workbench.cmd"


def test_one_click_workbench_launcher_exists_at_repo_root() -> None:
    content = LAUNCHER.read_text(encoding="utf-8")

    expected = [
        "@echo off",
        "title ConstraintOS Workbench Launcher",
        "ConstraintOS Workbench",
        "Starting the local ConstraintOS Exercise Workbench...",
    ]
    for item in expected:
        assert item in content


def test_one_click_workbench_launcher_invokes_exercise_mode_without_user_command_typing() -> None:
    content = LAUNCHER.read_text(encoding="utf-8")

    expected = [
        'set "REPO_ROOT=%~dp0"',
        'set "WORKBENCH_SCRIPT=%REPO_ROOT%scripts\\exercise-constraintos.ps1"',
        'powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%WORKBENCH_SCRIPT%"',
    ]
    for item in expected:
        assert item in content


def test_one_click_workbench_launcher_has_clear_missing_dependency_errors() -> None:
    content = LAUNCHER.read_text(encoding="utf-8")

    expected = [
        'if not exist "%WORKBENCH_SCRIPT%"',
        "ERROR: Could not find scripts\\exercise-constraintos.ps1",
        "Make sure this launcher is still in the ConstraintOS repository root.",
        "where powershell.exe >nul 2>nul",
        "ERROR: powershell.exe was not found on this machine.",
    ]
    for item in expected:
        assert item in content


def test_one_click_workbench_launcher_preserves_error_window_and_reports_success() -> None:
    content = LAUNCHER.read_text(encoding="utf-8")

    expected = [
        'set "EXIT_CODE=%ERRORLEVEL%"',
        "ConstraintOS Workbench failed",
        "Leave this window open and review the error above.",
        "pause",
        "ConstraintOS Workbench launched successfully",
        "The browser should now show the ConstraintOS Exercise Workbench.",
        "Press any key to close this launcher window.",
    ]
    for item in expected:
        assert item in content
