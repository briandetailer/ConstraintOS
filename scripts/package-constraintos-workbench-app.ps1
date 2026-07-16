param(
    [switch]$Clean
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$AppEntry = Join-Path $RepoRoot "apps\constraintos_workbench\app.py"
$BuildRoot = Join-Path $RepoRoot ".build\constraintos-workbench-app"
$VenvRoot = Join-Path $BuildRoot ".venv"
$DistRoot = Join-Path $RepoRoot "dist"
$AppDist = Join-Path $DistRoot "ConstraintOS Workbench"
$LauncherExe = Join-Path $AppDist "ConstraintOS Workbench.exe"

if (-not (Test-Path $AppEntry)) {
    throw "ConstraintOS Workbench app entry point missing: $AppEntry"
}

if ($Clean) {
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $BuildRoot
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $AppDist
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH. Install Python before packaging the ConstraintOS Workbench app."
}

New-Item -ItemType Directory -Force -Path $BuildRoot | Out-Null
New-Item -ItemType Directory -Force -Path $DistRoot | Out-Null

if (-not (Test-Path $VenvRoot)) {
    Write-Host "Creating temporary packaging environment..." -ForegroundColor Cyan
    python -m venv $VenvRoot
}

$PythonExe = Join-Path $VenvRoot "Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    throw "Packaging Python executable missing: $PythonExe"
}

Write-Host "Installing packaging dependencies..." -ForegroundColor Cyan
& $PythonExe -m pip install --upgrade pip pyinstaller

Write-Host "Building portable ConstraintOS Workbench app..." -ForegroundColor Cyan
& $PythonExe -m PyInstaller `
    --noconfirm `
    --clean `
    --onedir `
    --name "ConstraintOS Workbench" `
    --distpath $DistRoot `
    --workpath (Join-Path $BuildRoot "pyinstaller") `
    --specpath $BuildRoot `
    $AppEntry

if (-not (Test-Path $LauncherExe)) {
    throw "Packaged workbench executable was not created: $LauncherExe"
}

Write-Host "Copying bundled ConstraintOS runtime assets..." -ForegroundColor Cyan
Copy-Item -Recurse -Force (Join-Path $RepoRoot "scripts") (Join-Path $AppDist "scripts")

$ReadmePath = Join-Path $AppDist "README-FIRST.txt"
@"
ConstraintOS Workbench Demo App

How to run:
1. Double-click: ConstraintOS Workbench.exe
2. Your browser will open to the local Workbench app.
3. Edit the browser request if desired.
4. Choose the output focus and output count.
5. Click: Run ConstraintOS Demo
6. Review the generated workbench and candidate SVG outputs.
7. Open the captured browser request JSON from the artifact links if you want to inspect exactly what was submitted.

Notes:
- This is a local portable demo app.
- It does not require the recipient to open the repository.
- It does not require typing PowerShell commands.
- It runs on localhost and writes run artifacts inside this app folder.
- It captures browser input as browser-request.json for traceability.
- Close the app window to stop the local server.

Current guardrails:
- No real generated final graphics.
- No production artwork approval.
- No local image input.
- No image decoding.
- No pixel inspection.
- No CV/OCR integration.
- No automatic approval.
"@ | Set-Content -Path $ReadmePath -Encoding UTF8

Write-Host "ConstraintOS Workbench app package ready." -ForegroundColor Green
Write-Host "App folder: $AppDist"
Write-Host "Double-click: $LauncherExe"
