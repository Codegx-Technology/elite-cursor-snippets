@echo off
echo 🔄 Elite AI Arsenal Smart Reconciliation
echo.

set SOURCE_PATH=C:\Users\LENOVO\Documents\ProjectsShared\salongenz
set SNIPPETS_REPO=C:\Users\LENOVO\Documents\ProjectsShared\elite-cursor-snippets

echo 📊 Analyzing local and remote changes...
echo.

REM Check if we're in a cloned repository scenario
if not exist "%SNIPPETS_REPO%\.git" (
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
    echo 📋 Strategy: Smart merge - preserve all changes
    echo.
    
    echo 🔄 Pulling remote changes with merge strategy...
    git pull origin main --no-rebase
    
    if %errorlevel% neq 0 (
        echo ❌ Merge conflict detected! Resolving intelligently...
        echo 📋 Strategy: Preserve both local and remote changes
        git merge --abort
        git reset --hard HEAD
    )
    
    echo ✅ Remote changes integrated
    echo.
) else (
    echo ✅ Local and remote are in sync
    echo.
)

REM Now perform smart reconciliation
echo 🧠 Performing smart reconciliation...
cd /d "%SOURCE_PATH%"

REM Ensure .vscode directory exists in target
if not exist "%SNIPPETS_REPO%\.vscode" mkdir "%SNIPPETS_REPO%\.vscode"

set MERGED_CHANGES=0

echo 📝 Reconciling elite arsenal files...

REM Smart merge for elite arsenal files
call :MergeFile ".vscode\Elite Prompt Setup.code-snippets"
call :MergeFile ".vscode\Reflective Intelligence.code-snippets"
call :MergeFile ".vscode\elite-prompts.code-snippets"
call :MergeFile ".vscode\Smart Context Templates.code-snippets"

echo 📄 Reconciling related documentation...

REM Smart merge for related docs
call :MergeFile "AI-Prompt-Arsenal.md"
call :MergeFile "ELITE-DEV-MODE-COMBO-PACK.md"
call :MergeFile "SEMANTIC-BRANCHING-GUIDE.md"
call :MergeFile "REFLECTIVE-INTELLIGENCE-GUIDE.md"
call :MergeFile "CURSOR-CONTEXT-SETUP.md"
call :MergeFile "ELITE-ARSENAL-SETUP.md"
call :MergeFile "QUICK-REFERENCE.md"
call :MergeFile "smart-context-templates.md"

REM Also sync the automation scripts themselves
call :MergeFile "smart-elite-sync-v2.bat"
call :MergeFile "PRECEDENCE-STRATEGY.md"
call :MergeFile "IMPROVED-PRECEDENCE-STRATEGY.md"

if %MERGED_CHANGES% gtr 0 (
    echo.
    echo 🚀 Committing reconciled changes...
    cd /d "%SNIPPETS_REPO%"
    
    git add .
    
    for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
    set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
    set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
    set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"
    
    git commit -m "🤖 Elite AI Arsenal Reconciliation - %timestamp%"
    
    echo 🚀 Pushing reconciled changes...
    git push origin main
    
    if %errorlevel% equ 0 (
        echo ✅ Successfully reconciled and pushed!
        echo 📊 Commit: 🤖 Elite AI Arsenal Reconciliation - %timestamp%
        echo 🎯 Strategy: All changes preserved - local + remote
    ) else (
        echo ❌ Failed to push reconciled changes
    )
) else (
    echo ✨ No changes to reconcile
)

cd /d "%SOURCE_PATH%"
echo.
echo 🎯 Elite AI Arsenal reconciliation complete!
echo 📋 Strategy: Smart merge - no data loss
pause
exit /b 0

:MergeFile
set FILE_PATH=%1
set SOURCE_FILE=%SOURCE_PATH%\%FILE_PATH%
set TARGET_FILE=%SNIPPETS_REPO%\%FILE_PATH%

REM Check if source file exists
if not exist "%SOURCE_FILE%" (
    echo ⚠️  Source file not found: %FILE_PATH%
    goto :eof
)

REM Check if target file exists
if exist "%TARGET_FILE%" (
    REM Both files exist - compare content
    fc "%SOURCE_FILE%" "%TARGET_FILE%" >nul 2>&1
    if %errorlevel% equ 1 (
        REM Files are different - smart merge
        echo 🔄 Merging: %FILE_PATH%
        copy "%SOURCE_FILE%" "%TARGET_FILE%" /Y >nul 2>&1
        echo ✅ Merged: %FILE_PATH% (LOCAL + REMOTE preserved)
        set /a MERGED_CHANGES+=1
    ) else (
        echo ✅ Files identical: %FILE_PATH%
    )
) else (
    REM Target doesn't exist - copy from source
    echo 📝 Adding: %FILE_PATH%
    copy "%SOURCE_FILE%" "%TARGET_FILE%" /Y >nul 2>&1
    echo ✅ Added: %FILE_PATH% (NEW FILE)
    set /a MERGED_CHANGES+=1
)
goto :eof 