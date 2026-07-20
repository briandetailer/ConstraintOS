param(
    [switch]$Status,
    [switch]$Remove
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($Status -and $Remove) {
    throw "Use either -Status or -Remove, not both."
}

$CredentialHelper = Join-Path $PSScriptRoot "lib\openai-credential.ps1"
if (-not (Test-Path $CredentialHelper)) {
    throw "Missing ConstraintOS credential helper: $CredentialHelper"
}
. $CredentialHelper

if ($Status) {
    $CredentialStatus = Get-ConstraintOSOpenAIKeyStatus
    Write-Host "ConstraintOS OpenAI credential status"
    Write-Host "Encrypted credential present: $($CredentialStatus.EncryptedCredentialPresent)"
    Write-Host "Legacy user environment variable present: $($CredentialStatus.LegacyUserVariablePresent)"
    Write-Host "Available to this PowerShell process: $($CredentialStatus.AvailableToCurrentProcess)"
    Write-Host "Credential file: $($CredentialStatus.CredentialPath)"
    exit 0
}

if ($Remove) {
    Remove-ConstraintOSOpenAIKey
    Write-Host "Removed the saved ConstraintOS OpenAI API key for this Windows user."
    exit 0
}

Write-Host "One-time ConstraintOS OpenAI API key setup"
Write-Host "Windows DPAPI will encrypt the key for the current Windows user."
Write-Host "It will not be written to the repository, source package, run directory, or command history."
$SecureValue = Read-Host "Paste the OpenAI API key" -AsSecureString
try {
    Save-ConstraintOSOpenAIKey -SecureValue $SecureValue
}
finally {
    $SecureValue.Dispose()
}

Write-Host "OpenAI API key encrypted and saved for future ConstraintOS runs." -ForegroundColor Green
Write-Host "Run .\scripts\set-openai-api-key.ps1 -Status to verify configuration without displaying the key."
