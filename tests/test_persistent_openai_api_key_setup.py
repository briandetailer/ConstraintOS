from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP_SCRIPT = ROOT / "scripts" / "set-openai-api-key.ps1"
CREDENTIAL_HELPER = ROOT / "scripts" / "lib" / "openai-credential.ps1"
GENERATION_SCRIPT = ROOT / "scripts" / "generate-raspberry-pi-5-candidates.ps1"
RESEARCH_SCRIPT = ROOT / "scripts" / "exercise-research-to-render.ps1"


def test_credential_helper_uses_windows_dpapi_and_never_plaintext_storage() -> None:
    content = CREDENTIAL_HELPER.read_text(encoding="utf-8")

    assert 'openai-api-key.dpapi' in content
    assert 'Join-Path $env:LOCALAPPDATA "ConstraintOS\\credentials"' in content
    assert 'ConvertFrom-SecureString -SecureString $SecureValue' in content
    assert 'ConvertTo-SecureString -String $EncryptedValue' in content
    assert 'Read-Host "Paste the OpenAI API key" -AsSecureString' in content
    assert 'ZeroFreeBSTR' in content
    assert 'Test-ConstraintOSPlaceholderOpenAIKey' in content
    assert 'Ensure-ConstraintOSOpenAIKey' in content
    assert '[EnvironmentVariableTarget]::User' in content
    assert 'Save-ConstraintOSOpenAIKey -SecureValue $LegacySecure' in content
    assert 'Set-Content $PlainValue' not in content
    assert 'Write-Host $PlainValue' not in content
    assert 'Write-Output $PlainValue' not in content


def test_setup_script_supports_secure_setup_status_and_removal() -> None:
    content = SETUP_SCRIPT.read_text(encoding="utf-8")

    assert '[switch]$Status' in content
    assert '[switch]$Remove' in content
    assert r'lib\openai-credential.ps1' in content
    assert 'Save-ConstraintOSOpenAIKey -SecureValue $SecureValue' in content
    assert 'Get-ConstraintOSOpenAIKeyStatus' in content
    assert 'Remove-ConstraintOSOpenAIKey' in content
    assert 'Encrypted credential present:' in content
    assert 'Legacy user environment variable present:' in content
    assert 'Available to this PowerShell process:' in content
    assert 'Windows DPAPI will encrypt the key' in content
    assert 'source package, run directory, or command history' in content
    assert 'echo $env:OPENAI_API_KEY' not in content


def test_generation_script_prompts_once_when_credential_is_missing() -> None:
    content = GENERATION_SCRIPT.read_text(encoding="utf-8")

    assert r'lib\openai-credential.ps1' in content
    assert 'Ensure-ConstraintOSOpenAIKey | Out-Null' in content
    assert 'No persisted OpenAI API key was found' not in content
    assert 'set-openai-api-key.ps1 once' not in content


def test_live_research_uses_the_same_automatic_credential_flow() -> None:
    content = RESEARCH_SCRIPT.read_text(encoding="utf-8")

    assert r'lib\openai-credential.ps1' in content
    assert 'if ($LiveWebSearch)' in content
    assert 'Ensure-ConstraintOSOpenAIKey | Out-Null' in content
    assert 'No persisted OpenAI API key was found' not in content
