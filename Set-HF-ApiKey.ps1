param(
    [Parameter(Mandatory = $false)]
    [string]$ApiKey
)

# Set-HF-ApiKey.ps1
# Sets Hugging Face API key for current session and persists for the user.
# Usage:
#   Interactive:   .\Set-HF-ApiKey.ps1   (will prompt)
#   Non-interactive: .\Set-HF-ApiKey.ps1 -ApiKey "hf_xxx"

function Set-EnvVarBothScopes {
    param(
        [Parameter(Mandatory = $true)] [string]$Name,
        [Parameter(Mandatory = $true)] [string]$Value
    )
    # Current session
    $env:${Name} = $Value
    # Persist for the user
    [System.Environment]::SetEnvironmentVariable($Name, $Value, [System.EnvironmentVariableTarget]::User)
}

if (-not $ApiKey) {
    $ApiKey = Read-Host "Enter your Hugging Face API key (starts with hf_)"
}

if ([string]::IsNullOrWhiteSpace($ApiKey)) {
    Write-Host "ERROR: No API key provided. Aborting." -ForegroundColor Red
    exit 1
}

try {
    # Optional: ensure default HF cache directory
    if (-not $env:HF_HOME) {
        $homeCache = Join-Path $HOME ".cache\huggingface"
        Set-EnvVarBothScopes -Name "HF_HOME" -Value $homeCache
    }

    # Set both common env var names for compatibility
    Set-EnvVarBothScopes -Name "HF_API_KEY" -Value $ApiKey
    Set-EnvVarBothScopes -Name "HF_TOKEN" -Value $ApiKey

    Write-Host "OK: Hugging Face API key saved to session and user env." -ForegroundColor Green
    Write-Host "Note: New terminals need to be restarted to pick up persisted value." -ForegroundColor Yellow
}
catch {
    Write-Host ("ERROR: Failed to set HF API key. " + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
