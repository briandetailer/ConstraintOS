from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP_SCRIPT = ROOT / "scripts" / "set-openai-api-key.ps1"
GENERATION_SCRIPT = ROOT / "scripts" / "generate-raspberry-pi-5-candidates.ps1"


def test_setup_script_securely_prompts_and_persists_user_environment_variable() -> None:
    content = SETUP_SCRIPT.read_text(encoding="utf-8")

    assert 'Read-Host "Paste the OpenAI API key" -AsSecureString' in content
    assert '[EnvironmentVariableTarget]::User' in content
    assert '[Environment]::SetEnvironmentVariable($VariableName, $PlainValue, $Target)' in content
    assert '$env:OPENAI_API_KEY = $PlainValue' in content
    assert 'ZeroFreeBSTR' in content
    assert 'Test-PlaceholderOpenAIKey' in content
    assert 'source package, run directory, or command history' in content


def test_setup_script_supports_safe_status_and_removal_without_displaying_key() -> None:
    content = SETUP_SCRIPT.read_text(encoding="utf-8")

    assert '[switch]$Status' in content
    assert '[switch]$Remove' in content
    assert 'Persisted for Windows user:' in content
    assert 'Available to this PowerShell process:' in content
    assert '[Environment]::SetEnvironmentVariable($VariableName, $null, $Target)' in content
    assert 'Write-Host $Persisted' not in content
    assert 'Write-Output $Persisted' not in content
    assert 'echo $env:OPENAI_API_KEY' not in content


def test_generation_script_automatically_imports_persisted_user_key() -> None:
    content = GENERATION_SCRIPT.read_text(encoding="utf-8")

    assert 'function Import-PersistedOpenAIKey' in content
    assert '[EnvironmentVariableTarget]::Process' in content
    assert '[EnvironmentVariableTarget]::User' in content
    assert '$env:OPENAI_API_KEY = $PersistedValue' in content
    assert 'Run .\\scripts\\set-openai-api-key.ps1 once' in content
    assert 'if (($Generate -or $Validate) -and -not (Import-PersistedOpenAIKey))' in content
