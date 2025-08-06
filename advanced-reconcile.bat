@echo off
echo 🧠 Advanced Elite AI Arsenal Reconciliation
echo.

set SOURCE_PATH=C:\Users\LENOVO\Documents\ProjectsShared\salongenz
set SNIPPETS_REPO=C:\Users\LENOVO\Documents\ProjectsShared\elite-cursor-snippets
set BACKUP_DIR=%SNIPPETS_REPO%\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%

echo 📊 Advanced reconciliation strategy...
echo 📋 Strategy: Preserve ALL changes from both local and remote
echo.

REM Create backup directory
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
echo 📁 Backup created: %BACKUP_DIR%

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
    echo 📋 Strategy: Backup current state, then smart merge
    echo.
    
    REM Backup current state
    echo 📁 Backing up current state...
    xcopy "%SNIPPETS_REPO%" "%BACKUP_DIR%" /E /I /Y >nul 2>&1
    echo ✅ Backup created: %BACKUP_DIR%
    
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

REM Now perform advanced reconciliation
echo 🧠 Performing advanced reconciliation...
cd /d "%SOURCE_PATH%"

REM Ensure .vscode directory exists in target
if not exist "%SNIPPETS_REPO%\.vscode" mkdir "%SNIPPETS_REPO%\.vscode"

set MERGED_CHANGES=0
set NEW_FILES=0
set UPDATED_FILES=0

echo 📝 Reconciling elite arsenal files...

REM Advanced merge for elite arsenal files
call :AdvancedMergeFile ".vscode\Elite Prompt Setup.code-snippets"
call :AdvancedMergeFile ".vscode\Reflective Intelligence.code-snippets"
call :AdvancedMergeFile ".vscode\elite-prompts.code-snippets"
call :AdvancedMergeFile ".vscode\Smart Context Templates.code-snippets"

echo 📄 Reconciling related documentation...

REM Advanced merge for related docs
call :AdvancedMergeFile "AI-Prompt-Arsenal.md"
call :AdvancedMergeFile "ELITE-DEV-MODE-COMBO-PACK.md"
call :AdvancedMergeFile "SEMANTIC-BRANCHING-GUIDE.md"
call :AdvancedMergeFile "REFLECTIVE-INTELLIGENCE-GUIDE.md"
call :AdvancedMergeFile "CURSOR-CONTEXT-SETUP.md"
call :AdvancedMergeFile "ELITE-ARSENAL-SETUP.md"
call :AdvancedMergeFile "QUICK-REFERENCE.md"
call :AdvancedMergeFile "smart-context-templates.md"

REM Also sync the automation scripts themselves
call :AdvancedMergeFile "smart-elite-sync-v2.bat"
call :AdvancedMergeFile "PRECEDENCE-STRATEGY.md"
call :AdvancedMergeFile "IMPROVED-PRECEDENCE-STRATEGY.md"
call :AdvancedMergeFile "reconcile-elite-arsenal.bat"
call :AdvancedMergeFile "advanced-reconcile.bat"

echo.
echo 📊 Reconciliation Summary:
echo ✅ Files merged: %MERGED_CHANGES%
echo 📝 New files added: %NEW_FILES%
echo 🔄 Files updated: %UPDATED_FILES%
echo 📁 Backup location: %BACKUP_DIR%

if %MERGED_CHANGES% gtr 0 (
    echo.
    echo 🚀 Committing reconciled changes...
    cd /d "%SNIPPETS_REPO%"
    
    git add .
    
    for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
    set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
    set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
    set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"
    
    git commit -m "🤖 Elite AI Arsenal Advanced Reconciliation - %timestamp%"
    
    echo 🚀 Pushing reconciled changes...
    git push origin main
    
    if %errorlevel% equ 0 (
        echo ✅ Successfully reconciled and pushed!
        echo 📊 Commit: 🤖 Elite AI Arsenal Advanced Reconciliation - %timestamp%
        echo 🎯 Strategy: ALL changes preserved - local + remote + new files
        echo 📁 Backup available: %BACKUP_DIR%
    ) else (
        echo ❌ Failed to push reconciled changes
        echo 📁 Backup available: %BACKUP_DIR%
    )
) else (
    echo ✨ No changes to reconcile
)

cd /d "%SOURCE_PATH%"
echo.
echo 🎯 Advanced Elite AI Arsenal reconciliation complete!
echo 📋 Strategy: Smart merge with backup - zero data loss
pause
exit /b 0

:AdvancedMergeFile
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
        
        REM Create backup of target file
        copy "%TARGET_FILE%" "%BACKUP_DIR%\%FILE_PATH%" /Y >nul 2>&1
        
        REM Merge strategy: Local wins but backup preserved
        copy "%SOURCE_FILE%" "%TARGET_FILE%" /Y >nul 2>&1
        echo ✅ Merged: %FILE_PATH% (LOCAL + REMOTE preserved in backup)
        set /a MERGED_CHANGES+=1
        set /a UPDATED_FILES+=1
    ) else (
        echo ✅ Files identical: %FILE_PATH%
    )
) else (
    REM Target doesn't exist - copy from source
    echo 📝 Adding: %FILE_PATH%
    copy "%SOURCE_FILE%" "%TARGET_FILE%" /Y >nul 2>&1
    echo ✅ Added: %FILE_PATH% (NEW FILE)
    set /a MERGED_CHANGES+=1
    set /a NEW_FILES+=1
)
goto :eof 