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
        "download_url",
        "target_filename",
        "Invoke-WebRequest @RequestParameters",
        "Get-FileHash -Algorithm SHA256",
        "source-package-manifest.json",
        'manifest_version = "1.1.0"',
        "production_ready = $false",
        "usage_terms_review_required",
    ]
    for item in expected:
        assert item in content
    assert "ValidateSet" not in content


def test_materialized_reference_sources_are_not_committed_by_default() -> None:
    content = GITIGNORE.read_text(encoding="utf-8")
    assert "reference-sources/" in content
