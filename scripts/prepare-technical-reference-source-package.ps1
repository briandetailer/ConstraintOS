param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$ScenarioId,

    [string]$OutputRoot,

    [switch]$Force
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Get-OptionalSourceValue {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Source,

        [Parameter(Mandatory = $true)]
        [string]$PropertyName
    )

    $Property = $Source.PSObject.Properties[$PropertyName]
    if ($null -eq $Property -or $null -eq $Property.Value) {
        return ""
    }
    return [string]$Property.Value
}

function Get-MaterializationRequirement {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Source
    )

    $Configured = Get-OptionalSourceValue -Source $Source -PropertyName "materialization_requirement"
    if (-not [string]::IsNullOrWhiteSpace($Configured)) {
        if ($Configured -notin @("required", "optional", "reference_only")) {
            throw "Source $($Source.source_id) has unsupported materialization_requirement: $Configured"
        }
        return $Configured
    }

    if ([bool]$Source.ingestion_required) {
        return "required"
    }
    return "reference_only"
}

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
$ReferencedSources = @()
$Failures = @()
$Warnings = @()
$RequiredSourceCount = 0

foreach ($Source in $Scenario.sources) {
    $MaterializationRequirement = Get-MaterializationRequirement -Source $Source
    $DownloadUrl = Get-OptionalSourceValue -Source $Source -PropertyName "download_url"
    $TargetFilename = Get-OptionalSourceValue -Source $Source -PropertyName "target_filename"
    $SourceAccessNote = Get-OptionalSourceValue -Source $Source -PropertyName "source_access_note"

    if ($MaterializationRequirement -eq "reference_only") {
        $ReferencedSources += [ordered]@{
            source_id = [string]$Source.source_id
            authority = [string]$Source.authority
            source_class = [string]$Source.source_class
            source_page_url = [string]$Source.url
            download_url = $DownloadUrl
            usage_terms_status = [string]$Source.usage_terms_status
            materialization_requirement = $MaterializationRequirement
            source_access_note = $SourceAccessNote
            status = "reference_only_not_materialized"
        }
        Write-Host "Recording reference-only source $($Source.source_id) without downloading it."
        continue
    }

    if ($MaterializationRequirement -eq "required") {
        $RequiredSourceCount += 1
    }

    if ([string]::IsNullOrWhiteSpace($DownloadUrl)) {
        $Message = "Source $($Source.source_id) has no download_url."
        if ($MaterializationRequirement -eq "optional") {
            $Warnings += $Message
        }
        else {
            $Failures += $Message
        }
        continue
    }
    if ([string]::IsNullOrWhiteSpace($TargetFilename)) {
        $Message = "Source $($Source.source_id) has no target_filename."
        if ($MaterializationRequirement -eq "optional") {
            $Warnings += $Message
        }
        else {
            $Failures += $Message
        }
        continue
    }

    $TargetPath = Join-Path $FilesRoot $TargetFilename
    try {
        if ($Force -or -not (Test-Path $TargetPath)) {
            Write-Host "Downloading $($Source.source_id)..."
            $RequestParameters = @{
                Uri = $DownloadUrl
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
            download_url = $DownloadUrl
            local_file = "files/$TargetFilename"
            size_bytes = [long]$File.Length
            sha256 = $Digest
            usage_terms_status = [string]$Source.usage_terms_status
            materialization_requirement = $MaterializationRequirement
            status = "materialized"
        }
    }
    catch {
        $Message = "Source $($Source.source_id) failed: $($_.Exception.Message)"
        if ($MaterializationRequirement -eq "optional") {
            $Warnings += $Message
            $ReferencedSources += [ordered]@{
                source_id = [string]$Source.source_id
                authority = [string]$Source.authority
                source_class = [string]$Source.source_class
                source_page_url = [string]$Source.url
                download_url = $DownloadUrl
                usage_terms_status = [string]$Source.usage_terms_status
                materialization_requirement = $MaterializationRequirement
                source_access_note = $SourceAccessNote
                status = "optional_download_failed"
            }
        }
        else {
            $Failures += $Message
        }
    }
}

$RequiredMaterializedCount = @(
    $MaterializedSources | Where-Object { $_.materialization_requirement -eq "required" }
).Count
$PreflightReady = (
    $Failures.Count -eq 0 -and
    $RequiredSourceCount -gt 0 -and
    $RequiredMaterializedCount -eq $RequiredSourceCount
)

$Manifest = [ordered]@{
    manifest_id = "constraintos-reference-source-package/v1"
    manifest_version = "1.2.0"
    scenario_id = [string]$Scenario.scenario_id
    subject = [string]$Scenario.subject
    preferred_production_mode = [string]$Scenario.preferred_production_mode
    generated_at_utc = (Get-Date).ToUniversalTime().ToString("o")
    source_registry = "config/technical-reference-source-registry.json"
    source_registry_version = [string]$Registry.registry_version
    required_source_count = $RequiredSourceCount
    required_materialized_count = $RequiredMaterializedCount
    materialized_sources = $MaterializedSources
    referenced_sources = $ReferencedSources
    failure_count = $Failures.Count
    failures = $Failures
    warning_count = $Warnings.Count
    warnings = $Warnings
    preflight_status = if ($PreflightReady) { "source_files_materialized" } else { "blocked" }
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
Write-Host "Required sources materialized: $RequiredMaterializedCount / $RequiredSourceCount"
Write-Host "Reference-only sources recorded: $($ReferencedSources.Count)"
Write-Host "Preflight status: $($Manifest.preflight_status)"

foreach ($Warning in $Warnings) {
    Write-Warning $Warning
}

if ($Failures.Count -gt 0) {
    throw ($Failures -join [Environment]::NewLine)
}
