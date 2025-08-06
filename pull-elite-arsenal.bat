@echo off
echo 📥 Pull Elite AI Arsenal from Repository
echo.

set SNIPPETS_REPO=C:\Users\LENOVO\Documents\ProjectsShared\elite-cursor-snippets
set TARGET_PROJECT=%1

if "%TARGET_PROJECT%"=="" (
    echo ❌ Error: Please specify target project path
    echo Usage: pull-elite-arsenal.bat "C:\path\to\your\project"
    pause
    exit /b 1
)

echo 📁 Target Project: %TARGET_PROJECT%
echo 📁 Source Repository: %SNIPPETS_REPO%
echo.

REM Check if target project exists
if not exist "%TARGET_PROJECT%" (
    echo ❌ Error: Target project not found: %TARGET_PROJECT%
    pause
    exit /b 1
)

REM Check if snippets repo exists
if not exist "%SNIPPETS_REPO%" (
    echo ❌ Error: Snippets repository not found: %SNIPPETS_REPO%
    pause
    exit /b 1
)

echo 🔄 Pulling latest changes from repository...
cd /d "%SNIPPETS_REPO%"

REM Fetch and pull latest changes
git fetch origin >nul 2>&1
git pull origin main

if %errorlevel% neq 0 (
    echo ❌ Error: Failed to pull latest changes
    pause
    exit /b 1
)

echo ✅ Latest changes pulled successfully
echo.

echo 📝 Copying elite arsenal files to target project...

REM Ensure .vscode directory exists in target project
if not exist "%TARGET_PROJECT%\.vscode" mkdir "%TARGET_PROJECT%\.vscode"

set FILES_COPIED=0

REM Copy elite arsenal files
copy "%SNIPPETS_REPO%\.vscode\Elite Prompt Setup.code-snippets" "%TARGET_PROJECT%\.vscode\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: Elite Prompt Setup.code-snippets
    set /a FILES_COPIED+=1
) else (
    echo ⚠️  File not found: Elite Prompt Setup.code-snippets
)

copy "%SNIPPETS_REPO%\.vscode\Reflective Intelligence.code-snippets" "%TARGET_PROJECT%\.vscode\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: Reflective Intelligence.code-snippets
    set /a FILES_COPIED+=1
) else (
    echo ⚠️  File not found: Reflective Intelligence.code-snippets
)

copy "%SNIPPETS_REPO%\.vscode\elite-prompts.code-snippets" "%TARGET_PROJECT%\.vscode\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: elite-prompts.code-snippets
    set /a FILES_COPIED+=1
) else (
    echo ⚠️  File not found: elite-prompts.code-snippets
)

copy "%SNIPPETS_REPO%\.vscode\Smart Context Templates.code-snippets" "%TARGET_PROJECT%\.vscode\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: Smart Context Templates.code-snippets
    set /a FILES_COPIED+=1
) else (
    echo ⚠️  File not found: Smart Context Templates.code-snippets
)

echo.
echo 📄 Copying related documentation...

REM Copy related docs
copy "%SNIPPETS_REPO%\AI-Prompt-Arsenal.md" "%TARGET_PROJECT%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: AI-Prompt-Arsenal.md
    set /a FILES_COPIED+=1
)

copy "%SNIPPETS_REPO%\ELITE-DEV-MODE-COMBO-PACK.md" "%TARGET_PROJECT%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: ELITE-DEV-MODE-COMBO-PACK.md
    set /a FILES_COPIED+=1
)

copy "%SNIPPETS_REPO%\SEMANTIC-BRANCHING-GUIDE.md" "%TARGET_PROJECT%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: SEMANTIC-BRANCHING-GUIDE.md
    set /a FILES_COPIED+=1
)

copy "%SNIPPETS_REPO%\REFLECTIVE-INTELLIGENCE-GUIDE.md" "%TARGET_PROJECT%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: REFLECTIVE-INTELLIGENCE-GUIDE.md
    set /a FILES_COPIED+=1
)

copy "%SNIPPETS_REPO%\CURSOR-CONTEXT-SETUP.md" "%TARGET_PROJECT%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: CURSOR-CONTEXT-SETUP.md
    set /a FILES_COPIED+=1
)

copy "%SNIPPETS_REPO%\ELITE-ARSENAL-SETUP.md" "%TARGET_PROJECT%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: ELITE-ARSENAL-SETUP.md
    set /a FILES_COPIED+=1
)

copy "%SNIPPETS_REPO%\QUICK-REFERENCE.md" "%TARGET_PROJECT%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: QUICK-REFERENCE.md
    set /a FILES_COPIED+=1
)

copy "%SNIPPETS_REPO%\smart-context-templates.md" "%TARGET_PROJECT%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Copied: smart-context-templates.md
    set /a FILES_COPIED+=1
)

echo.
echo 📊 Summary:
echo ✅ Files copied: %FILES_COPIED%
echo 📁 Target project: %TARGET_PROJECT%
echo 📋 Strategy: Latest from repository → Target project
echo.

echo 🎯 Elite AI Arsenal successfully pulled to target project!
echo 📋 Note: This project now has the latest elite arsenal files
pause 