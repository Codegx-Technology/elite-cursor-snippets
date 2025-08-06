@echo off
echo 🧠 Smart Elite AI Arsenal Sync v2.0
echo.

set SOURCE_PATH=C:\Users\LENOVO\Documents\ProjectsShared\salongenz
set SNIPPETS_REPO=C:\Users\LENOVO\Documents\ProjectsShared\elite-cursor-snippets

echo 📊 Analyzing sync strategy...
echo.

REM Check if we're in a cloned repository scenario
if exist "%SNIPPETS_REPO%\.git" (
    echo 🔍 Detected: Cloned repository scenario
) else (
    echo ❌ Error: Snippets repository not found
    pause
    exit /b 1
)

REM Check for remote changes
echo 🔄 Checking for remote changes...
cd /d "%SNIPPETS_REPO%"
git fetch origin >nul 2>&1

REM Compare local vs remote
git log --oneline -1 > temp_local.txt
git log --oneline origin/main -1 > temp_remote.txt

set /p LOCAL_COMMIT=<temp_local.txt
set /p REMOTE_COMMIT=<temp_remote.txt

del temp_local.txt temp_remote.txt

echo 📊 Local commit:  %LOCAL_COMMIT%
echo 📊 Remote commit: %REMOTE_COMMIT%

REM Check if remote has newer changes
if not "%LOCAL_COMMIT%"=="%REMOTE_COMMIT%" (
    echo ⚠️  Remote has newer changes
    echo 📋 Strategy: Pull remote changes first, then sync local files
    echo.
    
    echo 🔄 Pulling remote changes...
    git pull origin main --rebase
    
    if %errorlevel% neq 0 (
        echo ❌ Conflict detected! Resolving...
        echo 📋 Strategy: Use local source files as truth
        git rebase --abort
        git reset --hard HEAD
    )
    
    echo ✅ Remote changes integrated
    echo.
) else (
    echo ✅ Local and remote are in sync
    echo.
)

REM Now sync local files (they always win for this project)
echo 🚀 Syncing local elite arsenal files...
cd /d "%SOURCE_PATH%"

REM Ensure .vscode directory exists in target
if not exist "%SNIPPETS_REPO%\.vscode" mkdir "%SNIPPETS_REPO%\.vscode"

set HAS_CHANGES=false

echo 📝 Syncing elite arsenal files...

REM Sync elite arsenal files with conflict resolution
copy "%SOURCE_PATH%\.vscode\Elite Prompt Setup.code-snippets" "%SNIPPETS_REPO%\.vscode\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: Elite Prompt Setup.code-snippets (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source file not found: Elite Prompt Setup.code-snippets
)

copy "%SOURCE_PATH%\.vscode\Reflective Intelligence.code-snippets" "%SNIPPETS_REPO%\.vscode\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: Reflective Intelligence.code-snippets (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source file not found: Reflective Intelligence.code-snippets
)

copy "%SOURCE_PATH%\.vscode\elite-prompts.code-snippets" "%SNIPPETS_REPO%\.vscode\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: elite-prompts.code-snippets (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source file not found: elite-prompts.code-snippets
)

copy "%SOURCE_PATH%\.vscode\Smart Context Templates.code-snippets" "%SNIPPETS_REPO%\.vscode\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: Smart Context Templates.code-snippets (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source file not found: Smart Context Templates.code-snippets
)

echo 📄 Syncing related docs...

REM Sync related docs
copy "%SOURCE_PATH%\AI-Prompt-Arsenal.md" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: AI-Prompt-Arsenal.md (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source doc not found: AI-Prompt-Arsenal.md
)

copy "%SOURCE_PATH%\ELITE-DEV-MODE-COMBO-PACK.md" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: ELITE-DEV-MODE-COMBO-PACK.md (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source doc not found: ELITE-DEV-MODE-COMBO-PACK.md
)

copy "%SOURCE_PATH%\SEMANTIC-BRANCHING-GUIDE.md" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: SEMANTIC-BRANCHING-GUIDE.md (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source doc not found: SEMANTIC-BRANCHING-GUIDE.md
)

copy "%SOURCE_PATH%\REFLECTIVE-INTELLIGENCE-GUIDE.md" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: REFLECTIVE-INTELLIGENCE-GUIDE.md (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source doc not found: REFLECTIVE-INTELLIGENCE-GUIDE.md
)

copy "%SOURCE_PATH%\CURSOR-CONTEXT-SETUP.md" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: CURSOR-CONTEXT-SETUP.md (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source doc not found: CURSOR-CONTEXT-SETUP.md
)

copy "%SOURCE_PATH%\ELITE-ARSENAL-SETUP.md" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: ELITE-ARSENAL-SETUP.md (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source doc not found: ELITE-ARSENAL-SETUP.md
)

copy "%SOURCE_PATH%\QUICK-REFERENCE.md" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: QUICK-REFERENCE.md (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source doc not found: QUICK-REFERENCE.md
)

copy "%SOURCE_PATH%\smart-context-templates.md" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: smart-context-templates.md (LOCAL WINS)
    set HAS_CHANGES=true
) else (
    echo ⚠️  Source doc not found: smart-context-templates.md
)

REM Also sync the automation scripts themselves
copy "%SOURCE_PATH%\smart-elite-sync-v2.bat" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: smart-elite-sync-v2.bat (LOCAL WINS)
    set HAS_CHANGES=true
)

copy "%SOURCE_PATH%\PRECEDENCE-STRATEGY.md" "%SNIPPETS_REPO%\" /Y >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Synced: PRECEDENCE-STRATEGY.md (LOCAL WINS)
    set HAS_CHANGES=true
)

if "%HAS_CHANGES%"=="true" (
    echo.
    echo 🚀 Committing changes with precedence strategy...
    cd /d "%SNIPPETS_REPO%"
    
    git add .
    
    for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
    set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
    set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
    set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"
    
    git commit -m "🤖 Elite AI Arsenal Update (LOCAL PRECEDENCE) - %timestamp%"
    
    echo 🚀 Pushing to remote...
    git push origin main
    
    if %errorlevel% equ 0 (
        echo ✅ Successfully synced with LOCAL PRECEDENCE!
        echo 📊 Commit: 🤖 Elite AI Arsenal Update (LOCAL PRECEDENCE) - %timestamp%
        echo 🎯 Strategy: Local working files always win
        echo 📋 Note: Remote changes were integrated before local sync
    ) else (
        echo ❌ Failed to push to remote repository
    )
) else (
    echo ✨ No changes to sync
)

cd /d "%SOURCE_PATH%"
echo.
echo 🎯 Smart Elite AI Arsenal sync complete!
echo 📋 Strategy: Remote changes integrated + Local files take precedence
pause 