# Elite AI Prompt Arsenal Deployment Script
# Automatically syncs your elite prompts to any project

param(
    [string]$ProjectPath = ".",
    [switch]$Global = $false
)

Write-Host "🚀 Deploying Elite AI Prompt Arsenal..." -ForegroundColor Green

# Source files
$SourceFile = Join-Path $PSScriptRoot ".vscode\Elite Prompt Setup.code-snippets"
$ContextFile = Join-Path $PSScriptRoot ".vscode\Smart Context Templates.code-snippets"

if ($Global) {
    # Deploy to global snippets
    $GlobalDir = "$env:APPDATA\Code\User\snippets"
    $GlobalFile = Join-Path $GlobalDir "elite-global-snippets.code-snippets"
    $GlobalContextFile = Join-Path $GlobalDir "elite-context-templates.code-snippets"
    
    if (!(Test-Path $GlobalDir)) {
        New-Item -ItemType Directory -Path $GlobalDir -Force | Out-Null
    }
    
    Copy-Item $SourceFile $GlobalFile -Force
    Copy-Item $ContextFile $GlobalContextFile -Force
    Write-Host "✅ Deployed to global snippets:" -ForegroundColor Green
    Write-Host "   - $GlobalFile" -ForegroundColor Cyan
    Write-Host "   - $GlobalContextFile" -ForegroundColor Cyan
} else {
    # Deploy to project .vscode folder
    $ProjectVSCodeDir = Join-Path $ProjectPath ".vscode"
    $TargetFile = Join-Path $ProjectVSCodeDir "Elite Prompt Setup.code-snippets"
    $TargetContextFile = Join-Path $ProjectVSCodeDir "Smart Context Templates.code-snippets"
    
    if (!(Test-Path $ProjectVSCodeDir)) {
        New-Item -ItemType Directory -Path $ProjectVSCodeDir -Force | Out-Null
    }
    
    Copy-Item $SourceFile $TargetFile -Force
    Copy-Item $ContextFile $TargetContextFile -Force
    Write-Host "✅ Deployed to project:" -ForegroundColor Green
    Write-Host "   - $TargetFile" -ForegroundColor Cyan
    Write-Host "   - $TargetContextFile" -ForegroundColor Cyan
}

Write-Host "🎯 Elite AI Prompt Arsenal ready to use!" -ForegroundColor Cyan
Write-Host "📝 Available prefixes:" -ForegroundColor Yellow
Write-Host "   Elite Prompts: thinkwithai, surgicalfix, refactorintent, writetest, doccode, unstuck, augmentsearch, kenyafirst, mindreset" -ForegroundColor Yellow
Write-Host "   Context Chains: taskchain, memorychain, debugchain, refactorchain, searchchain, recoverychain" -ForegroundColor Yellow 