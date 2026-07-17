param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$ScenarioId,

    [string]$OutputRoot,

    [switch]$Force
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$RegistryPath = Join-Path $RepoRoot "config\technical-reference-source-registry.json"
if (-not (Test-Path $RegistryPath)) {
    throw "Missing technical reference source registry: $RegistryPath"
}

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $RepoRoot "reference-sources"
}

$Registry = Get-Content -Raw -Encoding UTF8 $RegistryPath | ConvertFrom-Json
$Scenario = $Registry.scenarios | Where-Object { $_.scenario_id -eq $ScenarioId } | Select-Object -First 1
if ($null -eq $Scenario) {
    $AvailableScenarios = ($Registry.scenarios | ForEach-Object { $_.scenario_id }) -join ", "
    throw "Scenario is not registered: $ScenarioId. Available scenarios: $AvailableScenarios"
}

$ScenarioRoot = Join-Path $OutputRoot $ScenarioId
$FilesRoot = Join-Path $ScenarioRoot "files"
New-Item -ItemType Directory -Force -Path $FilesRoot | Out-Null

$MaterializedSources = @()
$Failures = @()

foreach ($Source in $Scenario.sources) {
    if (-not $Source.ingestion_required) {
        continue
    }
    if ([string]::IsNullOrWhiteSpace([string]$Source.download_url)) {
        $Failures += "Source $($Source.source_id) has no download_url."
        continue
    }
    if ([string]::IsNullOrWhiteSpace([string]$Source.target_filename)) {
        $Failures += "Source $($Source.source_id) has no target_filename."
        continue
    }

    $TargetPath = Join-Path $FilesRoot ([string]$Source.target_filename)
    try {
        if ($Force -or -not (Test-Path $TargetPath)) {
            Write-Host "Downloading $($Source.source_id)..."
            $RequestParameters = @{
                Uri = [string]$Source.download_url
                OutFile = $TargetPath
                UseBasicParsing = $true
                Headers = @{ "User-Agent" = "ConstraintOS-Reference-Package/1.0" }
            }
            Invoke-WebRequest @RequestParameters
        }

        $File = Get-Item $TargetPath
        $Digest = (Get-FileHash -Algorithm SHA256 -Path $TargetPath).Hash.ToLowerInvariant()
        $MaterializedSources += [ordered]@{
            source_id = [string]$Source.source_id
            authority = [string]$Source.authority
            source_class = [string]$Source.source_class
            source_page_url = [string]$Source.url
            download_url = [string]$Source.download_url
            local_file = "files/$($Source.target_filename)"
            size_bytes = [long]$File.Length
            sha256 = $Digest
            usage_terms_status = [string]$Source.usage_terms_status
            status = "materialized"
        }
    }
    catch {
        $Failures += "Source $($Source.source_id) failed: $($_.Exception.Message)"
    }
}

$Manifest = [ordered]@{
    manifest_id = "constraintos-reference-source-package/v1"
    manifest_version = "1.1.0"
    scenario_id = [string]$Scenario.scenario_id
    subject = [string]$Scenario.subject
    preferred_production_mode = [string]$Scenario.preferred_production_mode
    generated_at_utc = (Get-Date).ToUniversalTime().ToString("o")
    source_registry = "config/technical-reference-source-registry.json"
    source_registry_version = [string]$Registry.registry_version
    materialized_sources = $MaterializedSources
    failure_count = $Failures.Count
    failures = $Failures
    preflight_status = if ($Failures.Count -eq 0 -and $MaterializedSources.Count -gt 0) { "source_files_materialized" } else { "blocked" }
    production_ready = $false
    production_blockers = @(
        "usage_terms_review_required",
        "component_inventory_not_registered",
        "view_or_source_plate_contract_not_registered",
        "render_preset_not_registered"
    )
}

$ManifestPath = Join-Path $ScenarioRoot "source-package-manifest.json"
$Manifest | ConvertTo-Json -Depth 12 | Set-Content -Encoding UTF8 $ManifestPath

Write-Host "Reference source package: $ScenarioRoot"
Write-Host "Manifest: $ManifestPath"
Write-Host "Preflight status: $($Manifest.preflight_status)"

if ($Failures.Count -gt 0) {
    throw ($Failures -join [Environment]::NewLine)
}
