from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "watch-graphics-contract.ps1"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_graphics_contract_watch_capture_script_exists() -> None:
    assert SCRIPT.exists()


def test_graphics_contract_watch_capture_script_uses_contract_cli_and_local_runs() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert "param(" in content
    assert '[string]$Contract = "perseverance"' in content
    assert "Get-Command cos-graphics-contracts" in content
    assert "python -m constraintos.graphics_contracts_cli" in content
    assert 'runs\\graphics-contracts\\$Contract\\$Timestamp' in content


def test_graphics_contract_watch_capture_script_captures_expected_files() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert 'terminal-transcript.txt' in content
    assert 'watch-output.txt' in content
    assert 'graphics-contract-runtime-result.json' in content
    assert 'run-metadata.json' in content
    assert 'generated_by = "scripts/watch-graphics-contract.ps1"' in content


def test_graphics_contract_watch_capture_script_supports_plan_only_and_delay() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert "[switch]$PlanOnly" in content
    assert "--plan-only" in content
    assert "[int]$WatchDelayMs = 250" in content
    assert "--watch-delay-ms" in content
    assert "--watch" in content


def test_command_reference_includes_graphics_contract_capture_commands() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert ".\\scripts\\watch-graphics-contract.ps1" in content
    assert ".\\scripts\\watch-graphics-contract.ps1 -Contract supra_2jz_gte_twin_turbo" in content
    assert ".\\scripts\\watch-graphics-contract.ps1 -Contract perseverance -PlanOnly" in content
    assert "graphics-contract-runtime-result.json" in content
