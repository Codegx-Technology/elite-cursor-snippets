#!/usr/bin/env node

/**
 * Git Hooks Installation Script
 * 
 * Installs pre-commit, post-commit, and pre-push hooks for Elite Auto-Fix
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class GitHooksInstaller {
    constructor() {
        this.projectRoot = this.findProjectRoot();
        this.hooksDir = path.join(this.projectRoot, '.git', 'hooks');
        this.eliteDir = path.join(this.projectRoot, '.vscode', 'elite-cursor-snippets');
    }

    /**
     * Find the project root directory
     */
    findProjectRoot() {
        let currentDir = __dirname;
        
        while (currentDir !== path.dirname(currentDir)) {
            if (fs.existsSync(path.join(currentDir, '.git'))) {
                return currentDir;
            }
            currentDir = path.dirname(currentDir);
        }
        
        throw new Error('Git repository not found. Please run this script from within a git repository.');
    }

    /**
     * Install all git hooks
     */
    install() {
        console.log('🚀 Installing Elite Auto-Fix Git Hooks...');
        console.log(`Project root: ${this.projectRoot}`);
        console.log(`Hooks directory: ${this.hooksDir}`);

        if (!fs.existsSync(this.hooksDir)) {
            console.error('❌ Git hooks directory not found. Is this a git repository?');
            process.exit(1);
        }

        try {
            this.installPreCommitHook();
            this.installPostCommitHook();
            this.installPrePushHook();
            this.installCommitMsgHook();
            
            console.log('\n✅ Elite Auto-Fix Git Hooks installed successfully!');
            console.log('\n🎯 What happens now:');
            console.log('  • Pre-commit: Analyzes staged files for issues');
            console.log('  • Post-commit: Generates improvement suggestions');
            console.log('  • Pre-push: Runs full project analysis');
            console.log('  • Commit-msg: Validates commit message format');
            
        } catch (error) {
            console.error('❌ Failed to install git hooks:', error.message);
            process.exit(1);
        }
    }

    /**
     * Install pre-commit hook
     */
    installPreCommitHook() {
        const hookPath = path.join(this.hooksDir, 'pre-commit');
        const hookContent = this.generatePreCommitHook();
        
        this.writeHook(hookPath, hookContent);
        console.log('✅ Pre-commit hook installed');
    }

    /**
     * Install post-commit hook
     */
    installPostCommitHook() {
        const hookPath = path.join(this.hooksDir, 'post-commit');
        const hookContent = this.generatePostCommitHook();
        
        this.writeHook(hookPath, hookContent);
        console.log('✅ Post-commit hook installed');
    }

    /**
     * Install pre-push hook
     */
    installPrePushHook() {
        const hookPath = path.join(this.hooksDir, 'pre-push');
        const hookContent = this.generatePrePushHook();
        
        this.writeHook(hookPath, hookContent);
        console.log('✅ Pre-push hook installed');
    }

    /**
     * Install commit-msg hook
     */
    installCommitMsgHook() {
        const hookPath = path.join(this.hooksDir, 'commit-msg');
        const hookContent = this.generateCommitMsgHook();
        
        this.writeHook(hookPath, hookContent);
        console.log('✅ Commit-msg hook installed');
    }

    /**
     * Write hook file with proper permissions
     */
    writeHook(hookPath, content) {
        // Backup existing hook if it exists
        if (fs.existsSync(hookPath)) {
            const backupPath = `${hookPath}.backup.${Date.now()}`;
            fs.copyFileSync(hookPath, backupPath);
            console.log(`📋 Backed up existing hook to: ${path.basename(backupPath)}`);
        }

        fs.writeFileSync(hookPath, content);
        
        // Make hook executable (Unix-like systems)
        if (process.platform !== 'win32') {
            fs.chmodSync(hookPath, '755');
        }
    }

    /**
     * Generate pre-commit hook content
     */
    generatePreCommitHook() {
        return `#!/bin/sh
#
# Elite Auto-Fix Pre-Commit Hook
# Analyzes staged files for issues before commit
#

echo "🔍 Elite Auto-Fix: Analyzing staged files..."

# Get the elite-cursor-snippets directory
ELITE_DIR="${this.getRelativeEliteDir()}"

# Check if elite-auto-fix exists
if [ ! -f "$ELITE_DIR/elite-auto-fix.js" ]; then
    echo "⚠️  Elite Auto-Fix not found. Skipping analysis."
    exit 0
fi

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E "\\.(js|jsx|ts|tsx|py|java|cs|php|rb|go|rs|swift|kt)$" || true)

if [ -z "$STAGED_FILES" ]; then
    echo "✅ No code files staged for commit."
    exit 0
fi

# Analyze each staged file
CRITICAL_ISSUES=0
HIGH_ISSUES=0
TOTAL_ISSUES=0

for FILE in $STAGED_FILES; do
    if [ -f "$FILE" ]; then
        echo "📁 Analyzing: $FILE"
        
        # Run elite-auto-fix analysis
        RESULT=$(node "$ELITE_DIR/elite-auto-fix.js" "$FILE" 2>/dev/null || echo "error")
        
        if [ "$RESULT" != "error" ]; then
            # Count issues (simplified - in real implementation, parse JSON output)
            ISSUES=$(echo "$RESULT" | grep -c "issue" || echo "0")
            TOTAL_ISSUES=$((TOTAL_ISSUES + ISSUES))
            
            # Check for critical issues
            CRITICAL=$(echo "$RESULT" | grep -c "critical" || echo "0")
            CRITICAL_ISSUES=$((CRITICAL_ISSUES + CRITICAL))
            
            # Check for high issues
            HIGH=$(echo "$RESULT" | grep -c "high" || echo "0")
            HIGH_ISSUES=$((HIGH_ISSUES + HIGH))
        fi
    fi
done

echo ""
echo "📊 Analysis Summary:"
echo "   Total issues: $TOTAL_ISSUES"
echo "   Critical: $CRITICAL_ISSUES"
echo "   High: $HIGH_ISSUES"

# Block commit if critical issues found
if [ $CRITICAL_ISSUES -gt 0 ]; then
    echo ""
    echo "🚨 COMMIT BLOCKED: Critical issues found!"
    echo "   Please fix critical issues before committing."
    echo "   Run: elite fix <file> to get suggestions"
    exit 1
fi

# Warn about high issues but allow commit
if [ $HIGH_ISSUES -gt 0 ]; then
    echo ""
    echo "⚠️  Warning: High priority issues found."
    echo "   Consider fixing before committing."
    echo "   Run: elite fix <file> to get suggestions"
fi

echo "✅ Pre-commit analysis complete."
exit 0
`;
    }

    /**
     * Generate post-commit hook content
     */
    generatePostCommitHook() {
        return `#!/bin/sh
#
# Elite Auto-Fix Post-Commit Hook
# Generates improvement suggestions after commit
#

echo "🎯 Elite Auto-Fix: Generating post-commit suggestions..."

# Get the elite-cursor-snippets directory
ELITE_DIR="${this.getRelativeEliteDir()}"

# Check if elite-cli exists
if [ ! -f "$ELITE_DIR/elite-cli.js" ]; then
    echo "⚠️  Elite CLI not found. Skipping post-commit analysis."
    exit 0
fi

# Get files from the last commit
COMMIT_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD | grep -E "\\.(js|jsx|ts|tsx|py|java|cs|php|rb|go|rs|swift|kt)$" || true)

if [ -z "$COMMIT_FILES" ]; then
    echo "✅ No code files in this commit."
    exit 0
fi

echo "📈 Analyzing committed files for improvement opportunities..."

# Generate suggestions for committed files
for FILE in $COMMIT_FILES; do
    if [ -f "$FILE" ]; then
        echo "💡 Suggestions for: $FILE"
        node "$ELITE_DIR/elite-cli.js" suggest "Improve code quality in $FILE" 2>/dev/null || true
    fi
done

echo ""
echo "🚀 Post-commit analysis complete!"
echo "   Use 'elite scan' to run full project analysis"
echo "   Use 'elite fix <file>' to apply suggested improvements"

exit 0
`;
    }

    /**
     * Generate pre-push hook content
     */
    generatePrePushHook() {
        return `#!/bin/sh
#
# Elite Auto-Fix Pre-Push Hook
# Runs full project analysis before push
#

echo "🔍 Elite Auto-Fix: Running pre-push analysis..."

# Get the elite-cursor-snippets directory
ELITE_DIR="${this.getRelativeEliteDir()}"

# Check if elite-cli exists
if [ ! -f "$ELITE_DIR/elite-cli.js" ]; then
    echo "⚠️  Elite CLI not found. Skipping pre-push analysis."
    exit 0
fi

# Run full project scan
echo "📊 Scanning entire project..."
SCAN_RESULT=$(node "$ELITE_DIR/elite-cli.js" scan --severity=high 2>/dev/null || echo "error")

if [ "$SCAN_RESULT" = "error" ]; then
    echo "⚠️  Scan failed. Proceeding with push."
    exit 0
fi

echo "$SCAN_RESULT"

# Extract critical issues count (simplified)
CRITICAL_COUNT=$(echo "$SCAN_RESULT" | grep -c "critical" || echo "0")

if [ $CRITICAL_COUNT -gt 0 ]; then
    echo ""
    echo "🚨 PUSH BLOCKED: Critical issues found in project!"
    echo "   Please fix critical issues before pushing."
    echo "   Run: elite scan --severity=critical for details"
    exit 1
fi

echo "✅ Pre-push analysis complete. Safe to push!"
exit 0
`;
    }

    /**
     * Generate commit-msg hook content
     */
    generateCommitMsgHook() {
        return `#!/bin/sh
#
# Elite Auto-Fix Commit Message Hook
# Validates commit message format
#

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat $COMMIT_MSG_FILE)

echo "📝 Elite Auto-Fix: Validating commit message..."

# Check for minimum length
if [ \${#COMMIT_MSG} -lt 10 ]; then
    echo "❌ Commit message too short (minimum 10 characters)"
    echo "   Current: \${#COMMIT_MSG} characters"
    exit 1
fi

# Check for Kenya-first principles in commit messages
if echo "$COMMIT_MSG" | grep -qi "fix\\|feat\\|docs\\|style\\|refactor\\|test\\|chore"; then
    echo "✅ Conventional commit format detected"
else
    echo "💡 Consider using conventional commit format:"
    echo "   feat: add new feature"
    echo "   fix: resolve bug"
    echo "   docs: update documentation"
    echo "   style: formatting changes"
    echo "   refactor: code restructuring"
    echo "   test: add tests"
    echo "   chore: maintenance tasks"
fi

# Check for Kenya-specific terms (optional enhancement)
if echo "$COMMIT_MSG" | grep -qi "kenya\\|ksh\\|mpesa\\|nairobi"; then
    echo "🇰🇪 Kenya-first commit detected!"
fi

echo "✅ Commit message validation complete"
exit 0
`;
    }

    /**
     * Get relative path to elite-cursor-snippets directory
     */
    getRelativeEliteDir() {
        const relativePath = path.relative(this.projectRoot, this.eliteDir);
        return relativePath.replace(/\\/g, '/'); // Use forward slashes for cross-platform compatibility
    }

    /**
     * Uninstall git hooks
     */
    uninstall() {
        console.log('🗑️  Uninstalling Elite Auto-Fix Git Hooks...');

        const hooks = ['pre-commit', 'post-commit', 'pre-push', 'commit-msg'];
        
        hooks.forEach(hookName => {
            const hookPath = path.join(this.hooksDir, hookName);
            
            if (fs.existsSync(hookPath)) {
                // Check if it's our hook
                const content = fs.readFileSync(hookPath, 'utf8');
                if (content.includes('Elite Auto-Fix')) {
                    fs.unlinkSync(hookPath);
                    console.log(`✅ Removed ${hookName} hook`);
                    
                    // Restore backup if exists
                    const backupFiles = fs.readdirSync(this.hooksDir)
                        .filter(file => file.startsWith(`${hookName}.backup.`))
                        .sort()
                        .reverse();
                    
                    if (backupFiles.length > 0) {
                        const latestBackup = path.join(this.hooksDir, backupFiles[0]);
                        fs.copyFileSync(latestBackup, hookPath);
                        console.log(`📋 Restored backup: ${backupFiles[0]}`);
                    }
                }
            }
        });

        console.log('✅ Elite Auto-Fix Git Hooks uninstalled');
    }
}

// CLI interface
if (require.main === module) {
    const installer = new GitHooksInstaller();
    const command = process.argv[2];

    try {
        if (command === 'uninstall') {
            installer.uninstall();
        } else {
            installer.install();
        }
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

module.exports = GitHooksInstaller;
