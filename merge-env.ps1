Continue = 'Stop'
 = Get-Date -Format 'yyyyMMdd-HHmmss'
if (Test-Path .env) { Copy-Item .env ('.env.bak-' + ) -Force }

# Load current .env into hashtable
 = @{}
if (Test-Path .env) {
  Get-Content .env | ForEach-Object {
    if ( -match '^\s*#' -or  -match '^\s*$') { return }
    if ( -match '^\s*([A-Za-z_][A-Za-z0-9_]*)=(.*)$') {
       = [1]
       = [2]
      [] = 
    }
  }
}

 = Get-Content .env.example -Raw
 =  -split  ?


 = New-Object 'System.Collections.Generic.HashSet[string]'
 = New-Object 'System.Collections.Generic.List[string]'

foreach ( in ) {
  if ( -match '^\s*#' -or  -match '^\s*$') {
    .Add() | Out-Null
    continue
  }
  if ( -match '^\s*([A-Za-z_][A-Za-z0-9_]*)=(.*)$') {
     = [1]
    [void].Add()
    if (.ContainsKey()) {
      .Add( + '=' + []) | Out-Null
    } else {
      .Add() | Out-Null
    }
  } else {
    .Add() | Out-Null
  }
}

foreach ( in .Keys) {
  if (-not .Contains()) {
    .Add( + '=' + []) | Out-Null
  }
}

 = ( -join 
).TrimEnd()
Set-Content -Path .env -Value  -Encoding UTF8 -NoNewline:False
Write-Host ('Merged .env updated safely. Backup: .env.bak-' + )
