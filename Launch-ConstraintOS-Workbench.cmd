@echo off
setlocal
title ConstraintOS Workbench Launcher

set "REPO_ROOT=%~dp0"
set "WORKBENCH_SCRIPT=%REPO_ROOT%scripts\exercise-constraintos.ps1"

echo.
echo ============================================================
echo  ConstraintOS Workbench
echo ============================================================
echo.
echo Starting the local ConstraintOS Exercise Workbench...
echo.

if not exist "%WORKBENCH_SCRIPT%" (
    echo ERROR: Could not find scripts\exercise-constraintos.ps1
    echo.
    echo Expected location:
    echo   %WORKBENCH_SCRIPT%
    echo.
    echo Make sure this launcher is still in the ConstraintOS repository root.
    echo.
    pause
    exit /b 1
)

where powershell.exe >nul 2>nul
if errorlevel 1 (
    echo ERROR: powershell.exe was not found on this machine.
    echo ConstraintOS Workbench currently requires Windows PowerShell.
    echo.
    pause
    exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%WORKBENCH_SCRIPT%"
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo.
    echo ============================================================
    echo  ConstraintOS Workbench failed
    echo ============================================================
    echo Exit code: %EXIT_CODE%
    echo.
    echo Leave this window open and review the error above.
    echo.
    pause
    exit /b %EXIT_CODE%
)

echo.
echo ============================================================
echo  ConstraintOS Workbench launched successfully
echo ============================================================
echo.
echo The browser should now show the ConstraintOS Exercise Workbench.
echo.
echo Press any key to close this launcher window.
pause >nul
exit /b 0
