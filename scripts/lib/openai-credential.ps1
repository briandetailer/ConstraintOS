Set-StrictMode -Version Latest

$script:ConstraintOSOpenAIVariableName = "OPENAI_API_KEY"
$script:ConstraintOSCredentialRoot = Join-Path $env:LOCALAPPDATA "ConstraintOS\credentials"
$script:ConstraintOSCredentialPath = Join-Path $script:ConstraintOSCredentialRoot "openai-api-key.dpapi"

function Test-ConstraintOSPlaceholderOpenAIKey {
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

function ConvertFrom-ConstraintOSSecureString {
    param(
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$SecureValue
    )

    $Bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureValue)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($Bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($Bstr)
    }
}

function Save-ConstraintOSOpenAIKey {
    param(
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$SecureValue
    )

    $PlainValue = ConvertFrom-ConstraintOSSecureString -SecureValue $SecureValue
    try {
        if ([string]::IsNullOrWhiteSpace($PlainValue)) {
            throw "No API key was entered. Nothing was changed."
        }
        $PlainValue = $PlainValue.Trim()
        if (Test-ConstraintOSPlaceholderOpenAIKey -Value $PlainValue) {
            throw "The entered value looks like placeholder text. Nothing was changed."
        }
        if ($PlainValue.Length -lt 20) {
            throw "The entered value is too short to be a valid API key. Nothing was changed."
        }

        New-Item -ItemType Directory -Force -Path $script:ConstraintOSCredentialRoot | Out-Null
        $EncryptedValue = ConvertFrom-SecureString -SecureString $SecureValue
        [IO.File]::WriteAllText(
            $script:ConstraintOSCredentialPath,
            $EncryptedValue,
            [Text.UTF8Encoding]::new($false)
        )
        $env:OPENAI_API_KEY = $PlainValue

        # Remove the earlier plaintext user-environment-variable storage after migration.
        [Environment]::SetEnvironmentVariable(
            $script:ConstraintOSOpenAIVariableName,
            $null,
            [EnvironmentVariableTarget]::User
        )
    }
    finally {
        $PlainValue = $null
    }
}

function Read-ConstraintOSOpenAIKey {
    if (-not (Test-Path $script:ConstraintOSCredentialPath)) {
        return $null
    }

    try {
        $EncryptedValue = [IO.File]::ReadAllText($script:ConstraintOSCredentialPath).Trim()
        if ([string]::IsNullOrWhiteSpace($EncryptedValue)) {
            return $null
        }
        $SecureValue = ConvertTo-SecureString -String $EncryptedValue
        try {
            return ConvertFrom-ConstraintOSSecureString -SecureValue $SecureValue
        }
        finally {
            $SecureValue.Dispose()
        }
    }
    catch {
        throw "ConstraintOS could not decrypt the saved OpenAI API key for this Windows user. Remove and re-enter it with .\scripts\set-openai-api-key.ps1 -Remove."
    }
}

function Import-ConstraintOSOpenAIKey {
    $ProcessValue = [Environment]::GetEnvironmentVariable(
        $script:ConstraintOSOpenAIVariableName,
        [EnvironmentVariableTarget]::Process
    )
    if (-not [string]::IsNullOrWhiteSpace($ProcessValue)) {
        return $true
    }

    $SavedValue = Read-ConstraintOSOpenAIKey
    if (-not [string]::IsNullOrWhiteSpace($SavedValue)) {
        $env:OPENAI_API_KEY = $SavedValue
        $SavedValue = $null
        return $true
    }

    # Backward-compatible migration from the former plaintext user environment variable.
    $LegacyValue = [Environment]::GetEnvironmentVariable(
        $script:ConstraintOSOpenAIVariableName,
        [EnvironmentVariableTarget]::User
    )
    if (-not [string]::IsNullOrWhiteSpace($LegacyValue)) {
        $LegacySecure = ConvertTo-SecureString $LegacyValue -AsPlainText -Force
        try {
            Save-ConstraintOSOpenAIKey -SecureValue $LegacySecure
        }
        finally {
            $LegacySecure.Dispose()
            $LegacyValue = $null
        }
        return $true
    }

    return $false
}

function Ensure-ConstraintOSOpenAIKey {
    if (Import-ConstraintOSOpenAIKey) {
        return $true
    }

    Write-Host "ConstraintOS needs an OpenAI API key for generation or live research."
    Write-Host "Enter it once. Windows DPAPI will encrypt it for this Windows user."
    $SecureValue = Read-Host "Paste the OpenAI API key" -AsSecureString
    try {
        Save-ConstraintOSOpenAIKey -SecureValue $SecureValue
    }
    finally {
        $SecureValue.Dispose()
    }
    Write-Host "OpenAI API key encrypted and saved for future ConstraintOS runs." -ForegroundColor Green
    return $true
}

function Get-ConstraintOSOpenAIKeyStatus {
    $ProcessValue = [Environment]::GetEnvironmentVariable(
        $script:ConstraintOSOpenAIVariableName,
        [EnvironmentVariableTarget]::Process
    )
    $LegacyValue = [Environment]::GetEnvironmentVariable(
        $script:ConstraintOSOpenAIVariableName,
        [EnvironmentVariableTarget]::User
    )
    return [PSCustomObject]@{
        EncryptedCredentialPresent = Test-Path $script:ConstraintOSCredentialPath
        LegacyUserVariablePresent = -not [string]::IsNullOrWhiteSpace($LegacyValue)
        AvailableToCurrentProcess = -not [string]::IsNullOrWhiteSpace($ProcessValue)
        CredentialPath = $script:ConstraintOSCredentialPath
    }
}

function Remove-ConstraintOSOpenAIKey {
    Remove-Item $script:ConstraintOSCredentialPath -Force -ErrorAction SilentlyContinue
    [Environment]::SetEnvironmentVariable(
        $script:ConstraintOSOpenAIVariableName,
        $null,
        [EnvironmentVariableTarget]::User
    )
    Remove-Item "Env:$($script:ConstraintOSOpenAIVariableName)" -ErrorAction SilentlyContinue
}
