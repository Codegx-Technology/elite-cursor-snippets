$ErrorActionPreference = 'Stop'

# Backup existing .env
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
if (Test-Path ..\.env) { Copy-Item ..\.env ("..\.env.bak-" + $timestamp) -Force }

# Load current .env into hashtable
$envMap = @{}
if (Test-Path ..\.env) {
  Get-Content ..\.env | ForEach-Object {
    if ($_ -like '#*' -or [string]::IsNullOrWhiteSpace($_)) { return }
    $parts = $_.Split('=',2)
    if ($parts.Length -ge 2) {
      $key = $parts[0]
      $val = $parts[1]
      $envMap[$key] = $val
    }
  }
}

# Read example file
$exampleRaw = Get-Content ..\.env.example -Raw
$linesRaw = $exampleRaw -replace "\r\n","\n" -split "\n"

$seen = New-Object 'System.Collections.Generic.HashSet[string]'
$merged = New-Object 'System.Collections.Generic.List[string]'

foreach ($line in $linesRaw) {
  if ($line -like '#*' -or [string]::IsNullOrWhiteSpace($line)) {
    $merged.Add($line) | Out-Null
    continue
  }
  $parts = $line.Split('=',2)
  if ($parts.Length -ge 2) {
    $key = $parts[0]
    [void]$seen.Add($key)
    if ($envMap.ContainsKey($key)) {
      $merged.Add($key + '=' + $envMap[$key]) | Out-Null
    } else {
      $merged.Add($line) | Out-Null
    }
  } else {
    $merged.Add($line) | Out-Null
  }
}

# Append any keys that exist only in .env
foreach ($k in $envMap.Keys) {
  if (-not $seen.Contains($k)) {
    $merged.Add($k + '=' + $envMap[$k]) | Out-Null
  }
}

$mergedText = ($merged -join "`r`n").TrimEnd()
Set-Content -Path ..\.env -Value $mergedText -Encoding UTF8
Write-Host ("Merged .env updated safely. Backup: .env.bak-" + $timestamp)
