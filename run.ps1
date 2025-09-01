# Shujaa Studio Professional Launcher
# Elite PowerShell script for surgical, token-efficient development workflow
# Compatible with AugmentCode methodology and GEMINI.md contract

param(
    [switch]$BackendOnly,
    [switch]$FrontendOnly,
    [switch]$Check,
    [switch]$Help
)

Write-Host "SHUJAA STUDIO PROFESSIONAL LAUNCHER" -ForegroundColor Green
Write-Host "Elite • Surgical • Token-Efficient" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ProjectRoot "shujaa_venv\Scripts\python.exe"
$FrontendPath = Join-Path $ProjectRoot "frontend"

Write-Host "Project Root: $ProjectRoot" -ForegroundColor Cyan

if ($Help) {
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1                 # Launch both servers" -ForegroundColor Cyan
    Write-Host "  .\run.ps1 -Check          # Health check" -ForegroundColor Cyan
    Write-Host "  .\run.ps1 -Help           # Show help" -ForegroundColor Cyan
    Write-Host "  .\run.ps1 -BackendOnly    # Backend only" -ForegroundColor Cyan
    Write-Host "  .\run.ps1 -FrontendOnly   # Frontend only" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Harambee! Elite development workflow ready!" -ForegroundColor Yellow
    return
}

Write-Host "Checking environment..." -ForegroundColor Yellow

if (-not (Test-Path $PythonExe)) {
    Write-Host "ERROR: shujaa_venv not found at: $PythonExe" -ForegroundColor Red
    Write-Host "Please run: python -m venv shujaa_venv" -ForegroundColor Yellow
    return
}
Write-Host "SUCCESS: Python environment found" -ForegroundColor Green

$NodeFound = $false
try {
    Get-Command node -ErrorAction Stop | Out-Null
    Get-Command npm -ErrorAction Stop | Out-Null
    $NodeFound = $true
    Write-Host "SUCCESS: Node.js and npm found" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Node.js not found" -ForegroundColor Red
    if (-not $BackendOnly) {
        Write-Host "Install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    }
}

if ($Check) {
    Write-Host ""
    Write-Host "Health check complete!" -ForegroundColor Green
    Write-Host "Python: $PythonExe" -ForegroundColor Cyan
    if ($NodeFound) {
        Write-Host "Node.js: Available" -ForegroundColor Cyan
    }
    Write-Host "Shujaa Studio is ready for development!" -ForegroundColor Yellow
    return
}

if (-not $FrontendOnly) {
    Write-Host "Starting Backend Server..." -ForegroundColor Green
    $BackendCmd = "cd '$ProjectRoot'; Write-Host 'SHUJAA STUDIO BACKEND' -ForegroundColor Green; & '$PythonExe' universal_server.py --backend-only"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $BackendCmd
    Start-Sleep 2
}

if (-not $BackendOnly -and $NodeFound) {
    Write-Host "Starting Frontend Server..." -ForegroundColor Green
    $FrontendCmd = "cd '$FrontendPath'; Write-Host 'SHUJAA STUDIO FRONTEND' -ForegroundColor Green; npm run dev"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $FrontendCmd
    Start-Sleep 2
}

Write-Host ""
Write-Host "Shujaa Studio launched successfully!" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend UI: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Harambee! Elite development environment active!" -ForegroundColor Yellow