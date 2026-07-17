param(
    [switch]$Clean
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$AppEntry = Join-Path $RepoRoot "apps\constraintos_workbench\app_v2.py"
$BuildRoot = Join-Path $RepoRoot ".build\constraintos-workbench-app"
$VenvRoot = Join-Path $BuildRoot ".venv"
$DistRoot = Join-Path $RepoRoot "dist"
$AppDist = Join-Path $DistRoot "ConstraintOS Workbench"
$LauncherExe = Join-Path $AppDist "ConstraintOS Workbench.exe"
$ToyotaSourcePackage = Join-Path $RepoRoot "reference-sources\toyota_supra_a80_2jz_gte"

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

Write-Host "Building source-backed ConstraintOS Workbench app..." -ForegroundColor Cyan
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
Copy-Item -Recurse -Force (Join-Path $RepoRoot "config") (Join-Path $AppDist "config")

$PackagedReferenceRoot = Join-Path $AppDist "reference-sources"
New-Item -ItemType Directory -Force -Path $PackagedReferenceRoot | Out-Null
if (Test-Path $ToyotaSourcePackage) {
    Write-Host "Copying materialized Toyota reference package..." -ForegroundColor Cyan
    Copy-Item -Recurse -Force $ToyotaSourcePackage $PackagedReferenceRoot
}
else {
    Write-Warning "Toyota reference source package was not found. The packaged source-backed render action will remain blocked."
}

$ReadmePath = Join-Path $AppDist "README-FIRST.txt"
@"
ConstraintOS Workbench Demo App

How to run:
1. Double-click: ConstraintOS Workbench.exe
2. Your browser will open to the local Workbench app.
3. Review both status cards:
   - OpenAI exploratory provider
   - Registered Toyota source package
4. Choose one action:
   - Run Deterministic Demo
   - Explore Generated Raster References
   - Render Registered Toyota Source Plate
5. Review the generated workbench and manifests.

Source-backed Toyota rendering:
- The Toyota source package must be materialized before packaging.
- The package script copies reference-sources\toyota_supra_a80_2jz_gte into the portable app when it exists.
- The browser source status must show ready before source-backed rendering is enabled.
- The app verifies the source file SHA-256 against source-package-manifest.json.
- The output is a deterministic SVG composition using the registered official Toyota source plate.
- It is a local source-backed draft and remains needs_review with approval_allowed: false.
- Novel camera angles, exploded views, hidden geometry, and component callouts remain blocked by the current source-plate contract.

Exploratory raster references:
- OPENAI_API_KEY is optional and is only used for Explore Generated Raster References.
- Do not use literal placeholder text such as your_api_key_here, paste_your_key_here, or api_key_here.
- Generated raster references may invent geometry.
- They are explicitly exploratory_reference_only.
- They are not technical drawings and cannot enter a production approval path.
- Do not place the API key in this app folder or commit it to source control.

Notes:
- This is a local portable demo app.
- It does not require the recipient to open the repository.
- It runs on localhost and writes run artifacts inside this app folder.
- It captures browser input as browser-request.json for traceability.
- Close the app window to stop the local server.

Current guardrails:
- No production artwork approval.
- No provider-generated labels, dimensions, legends, or callouts.
- No technical claims beyond the registered source package.
- No automatic approval.
"@ | Set-Content -Path $ReadmePath -Encoding UTF8

Write-Host "ConstraintOS Workbench app package ready." -ForegroundColor Green
Write-Host "App folder: $AppDist"
Write-Host "Double-click: $LauncherExe"
