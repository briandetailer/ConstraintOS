from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "watch-candidate-byte-loader.ps1"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loader_Demo_Watch_Script_v1.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_candidate_byte_loader_demo_watch_script_exists_and_has_defaults() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert 'param(' in content
    assert '[string]$Record = "perseverance"' in content
    assert '[int]$WatchDelayMs = 500' in content
    assert 'runs\\candidate-byte-loader\\$Record\\$Timestamp' in content
    assert 'ConstraintOS candidate byte-loader demo watch' in content
    assert 'Demo principle: structured specifications, validation, and traceability are the source of truth.' in content


def test_candidate_byte_loader_demo_watch_script_runs_visible_pipeline_stages() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        'Load deterministic fixture bytes for selected record',
        'Build selected record byte-loading review packet',
        'Review deterministic fixture registry descriptors',
        'Review fixture registry failure matrix',
        'Capture JSON evidence files',
        'Final demo decision',
        '@("minimal", $Record)',
        '@("review-packet", $Record)',
        '@("registry-review-packet")',
        '@("failure-review-packet")',
    ]
    for item in expected:
        assert item in content


def test_candidate_byte_loader_demo_watch_script_captures_evidence_outputs() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        'terminal-transcript.txt',
        'watch-output.txt',
        'minimal-byte-loading.json',
        'minimal-review-packet.json',
        'fixture-registry-review-packet.json',
        'fixture-registry-failure-review-packet.json',
        'run-metadata.json',
        'Tee-Object -FilePath $WatchOutputPath',
        'ConvertTo-Json -Depth 4',
    ]
    for item in expected:
        assert item in content


def test_candidate_byte_loader_demo_watch_script_preserves_safety_boundaries() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        'no local file opening, download, network fetch, image decoding, scoring, mutation, or approval',
        'local_image_file_opening = "not_run"',
        'artifact_download = "not_run"',
        'network_fetch = "not_run"',
        'image_decoding = "not_run"',
        'candidate_scoring = "not_run"',
        'source_report_mutation = "not_run"',
        'approval_automation = "not_run"',
        'approval_allowed = $false',
        'approval_allowed: false',
    ]
    for item in expected:
        assert item in content


def test_candidate_byte_loader_demo_watch_milestone_records_business_demo_scope() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert 'milestone: Candidate Image Byte Loader Demo Watch Script v1' in content
    assert 'status: active' in content
    assert 'Business Demo Visibility Track' in content
    assert 'business-demo-friendly watch script' in content
    assert 'Structured specifications, validation, and traceability' in content
    assert 'demo_source: scripts/watch-candidate-byte-loader.ps1' in content
    assert 'pytest tests/test_candidate_image_byte_loader_demo_watch_script.py' in content
    assert 'No local image file opening.' in content
    assert 'No network fetch.' in content
    assert 'No image decoding.' in content
    assert 'No candidate scoring.' in content


def test_command_reference_includes_candidate_byte_loader_demo_watch_script() -> None:
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert 'Candidate image byte loader demo watch script' in command_reference
    assert '.\\scripts\\watch-candidate-byte-loader.ps1' in command_reference
    assert 'pytest tests/test_candidate_image_byte_loader_demo_watch_script.py' in command_reference
