from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "prepare-technical-reference-source-package.ps1"
GITIGNORE = ROOT / ".gitignore"


def test_reference_source_package_script_exists_and_reads_registry() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "ValidateNotNullOrEmpty",
        'config\\technical-reference-source-registry.json',
        "Available scenarios:",
        "reference-sources",
        "materialization_requirement",
        '"required", "optional", "reference_only"',
        "reference_only_not_materialized",
        "referenced_sources",
        "required_source_count",
        "required_materialized_count",
        "warning_count",
        "download_url",
        "target_filename",
        "Invoke-WebRequest @RequestParameters",
        "Get-FileHash -Algorithm SHA256",
        "source-package-manifest.json",
        'manifest_version = "1.2.0"',
        "production_ready = $false",
        "usage_terms_review_required",
    ]
    for item in expected:
        assert item in content
    assert "ValidateSet" not in content


def test_reference_only_sources_do_not_enter_blocking_failure_path() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    reference_branch = content.index('if ($MaterializationRequirement -eq "reference_only")')
    continue_statement = content.index("continue", reference_branch)
    download_statement = content.index("Invoke-WebRequest @RequestParameters")

    assert reference_branch < continue_statement < download_statement
    assert 'status = "reference_only_not_materialized"' in content
    assert 'if ($Failures.Count -gt 0)' in content


def test_materialized_reference_sources_are_not_committed_by_default() -> None:
    content = GITIGNORE.read_text(encoding="utf-8")
    assert "reference-sources/" in content
