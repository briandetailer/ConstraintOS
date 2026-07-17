param(
    [switch]$Status,
    [switch]$Remove
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($Status -and $Remove) {
    throw "Use either -Status or -Remove, not both."
}

$VariableName = "OPENAI_API_KEY"
$Target = [EnvironmentVariableTarget]::User

function Test-PlaceholderOpenAIKey {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $Lowered = $Value.Trim().ToLowerInvariant()
    $Markers = @(
        "your_api_key",
        "paste_your",
        "api_key_here",
        "key_here",
        "replace_me",
        "placeholder",
        "example"
    )
    foreach ($Marker in $Markers) {
        if ($Lowered.Contains($Marker)) {
            return $true
        }
    }
    return $false
}

function Get-PersistedOpenAIKey {
    return [Environment]::GetEnvironmentVariable($VariableName, $Target)
}

if ($Status) {
    $Persisted = Get-PersistedOpenAIKey
    $ProcessValue = [Environment]::GetEnvironmentVariable(
        $VariableName,
        [EnvironmentVariableTarget]::Process
    )
    Write-Host "ConstraintOS OpenAI credential status"
    Write-Host "Persisted for Windows user: $(-not [string]::IsNullOrWhiteSpace($Persisted))"
    Write-Host "Available to this PowerShell process: $(-not [string]::IsNullOrWhiteSpace($ProcessValue))"
    exit 0
}

if ($Remove) {
    [Environment]::SetEnvironmentVariable($VariableName, $null, $Target)
    Remove-Item "Env:$VariableName" -ErrorAction SilentlyContinue
    Write-Host "Removed the persisted ConstraintOS OpenAI API key for this Windows user."
    exit 0
}

Write-Host "One-time ConstraintOS OpenAI API key setup"
Write-Host "The key will be stored as the Windows user environment variable OPENAI_API_KEY."
Write-Host "It will not be written to the repository, source package, run directory, or command history."
$SecureValue = Read-Host "Paste the OpenAI API key" -AsSecureString
$Bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureValue)
try {
    $PlainValue = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($Bstr)
}
finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($Bstr)
}

if ([string]::IsNullOrWhiteSpace($PlainValue)) {
    throw "No API key was entered. Nothing was changed."
}
$PlainValue = $PlainValue.Trim()
if (Test-PlaceholderOpenAIKey -Value $PlainValue) {
    throw "The entered value looks like placeholder text. Nothing was changed."
}
if ($PlainValue.Length -lt 20) {
    throw "The entered value is too short to be a valid API key. Nothing was changed."
}

[Environment]::SetEnvironmentVariable($VariableName, $PlainValue, $Target)
$env:OPENAI_API_KEY = $PlainValue
$PlainValue = $null
$SecureValue.Dispose()

Write-Host "OpenAI API key saved for the current Windows user." -ForegroundColor Green
Write-Host "ConstraintOS generation scripts can now load it automatically in this and future sessions."
Write-Host "Run .\scripts\set-openai-api-key.ps1 -Status to verify configuration without displaying the key."
