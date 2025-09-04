#!/usr/bin/env node

/**
 * Elite Cursor Snippets Setup Script
 * 
 * Complete setup and integration script for the automation system
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class EliteSetup {
    constructor() {
        this.projectRoot = this.findProjectRoot();
        this.eliteDir = __dirname;
    }

    /**
     * Find project root directory
     */
    findProjectRoot() {
        let currentDir = __dirname;
        
        while (currentDir !== path.dirname(currentDir)) {
            if (fs.existsSync(path.join(currentDir, '.git'))) {
                return currentDir;
            }
            currentDir = path.dirname(currentDir);
        }
        
        return __dirname;
    }

    /**
     * Run complete setup
     */
    async setup() {
        console.log('🚀 Elite Cursor Snippets Automation Setup');
        console.log('=' .repeat(50));
        console.log('🇰🇪 Kenya-First Engineering Excellence');
        console.log('');

        try {
            await this.checkPrerequisites();
            await this.installDependencies();
            await this.setupConfiguration();
            await this.installGitHooks();
            await this.setupVSCodeIntegration();
            await this.runTests();
            await this.displaySuccessMessage();
        } catch (error) {
            console.error('❌ Setup failed:', error.message);
            process.exit(1);
        }
    }

    /**
     * Check prerequisites
     */
    async checkPrerequisites() {
        console.log('🔍 Checking prerequisites...');

        // Check Node.js version
        try {
            const nodeVersion = execSync('node --version', { encoding: 'utf8' }).trim();
            console.log(`✅ Node.js: ${nodeVersion}`);
            
            const majorVersion = parseInt(nodeVersion.substring(1).split('.')[0]);
            if (majorVersion < 14) {
                throw new Error('Node.js 14 or higher is required');
            }
        } catch (error) {
            throw new Error('Node.js is not installed or not in PATH');
        }

        // Check if we're in a git repository
        try {
            execSync('git status', { stdio: 'ignore' });
            console.log('✅ Git repository detected');
        } catch (error) {
            console.log('⚠️ Not in a git repository. Git hooks will be skipped.');
        }

        // Check VSCode/Cursor
        const hasVSCode = fs.existsSync(path.join(this.projectRoot, '.vscode'));
        if (hasVSCode) {
            console.log('✅ VSCode configuration directory found');
        } else {
            console.log('ℹ️ VSCode configuration directory not found');
        }
    }

    /**
     * Install dependencies
     */
    async installDependencies() {
        console.log('\n📦 Installing dependencies...');

        const packageJsonPath = path.join(this.eliteDir, 'package.json');
        if (!fs.existsSync(packageJsonPath)) {
            console.log('⚠️ package.json not found. Skipping dependency installation.');
            return;
        }

        try {
            // Check if npm is available
            execSync('npm --version', { stdio: 'ignore' });
            
            console.log('📥 Installing npm packages...');
            execSync('npm install', { 
                cwd: this.eliteDir, 
                stdio: 'inherit' 
            });
            
            console.log('✅ Dependencies installed successfully');
        } catch (error) {
            console.log('⚠️ npm not available. Please install dependencies manually:');
            console.log('   cd .vscode/elite-cursor-snippets && npm install');
        }
    }

    /**
     * Setup configuration
     */
    async setupConfiguration() {
        console.log('\n⚙️ Setting up configuration...');

        const configPath = path.join(this.eliteDir, 'elite-auto-fix.config.json');
        
        if (fs.existsSync(configPath)) {
            console.log('✅ Configuration file already exists');
            return;
        }

        // Create default configuration
        const defaultConfig = {
            autoApply: false,
            verboseOutput: true,
            enableGuardrails: true,
            excludePatterns: ["node_modules", ".git", "dist", "build"],
            fileExtensions: [".js", ".jsx", ".ts", ".tsx", ".vue", ".py"],
            kenyaSpecific: {
                currency: { preferred: "KSh", avoid: ["$", "USD"] },
                phoneFormat: { preferred: "+254", avoid: ["+1"] },
                timezone: { preferred: "EAT", avoid: ["UTC", "GMT"] }
            },
            gitHooks: {
                preCommit: { enabled: true, blockOnCritical: true },
                postCommit: { enabled: true, generateReport: true },
                prePush: { enabled: true, fullAnalysis: true }
            }
        };

        fs.writeFileSync(configPath, JSON.stringify(defaultConfig, null, 2));
        console.log('✅ Default configuration created');
    }

    /**
     * Install git hooks
     */
    async installGitHooks() {
        console.log('\n🔗 Installing git hooks...');

        try {
            execSync('git status', { stdio: 'ignore' });
            
            const GitHooksInstaller = require('./scripts/install-git-hooks');
            const installer = new GitHooksInstaller();
            installer.install();
            
            console.log('✅ Git hooks installed successfully');
        } catch (error) {
            console.log('⚠️ Not in a git repository. Skipping git hooks installation.');
        }
    }

    /**
     * Setup VSCode integration
     */
    async setupVSCodeIntegration() {
        console.log('\n🔧 Setting up VSCode integration...');

        const vscodeDir = path.join(this.projectRoot, '.vscode');
        
        if (!fs.existsSync(vscodeDir)) {
            fs.mkdirSync(vscodeDir, { recursive: true });
            console.log('📁 Created .vscode directory');
        }

        // Create settings.json with Elite Auto-Fix integration
        const settingsPath = path.join(vscodeDir, 'settings.json');
        let settings = {};

        if (fs.existsSync(settingsPath)) {
            try {
                settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
            } catch (error) {
                console.log('⚠️ Could not parse existing settings.json');
            }
        }

        // Add Elite Auto-Fix settings
        settings['elite-auto-fix.enabled'] = true;
        settings['elite-auto-fix.autoSuggest'] = true;
        settings['elite-auto-fix.showInProblems'] = true;
        settings['elite-auto-fix.kenyaFirst'] = true;

        fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
        console.log('✅ VSCode settings updated');

        // Create tasks.json for Elite Auto-Fix commands
        const tasksPath = path.join(vscodeDir, 'tasks.json');
        const tasks = {
            version: "2.0.0",
            tasks: [
                {
                    label: "Elite: Analyze Current File",
                    type: "shell",
                    command: "node",
                    args: [".vscode/elite-cursor-snippets/elite-auto-fix.js", "${file}"],
                    group: "build",
                    presentation: {
                        echo: true,
                        reveal: "always",
                        focus: false,
                        panel: "shared"
                    }
                },
                {
                    label: "Elite: Scan Project",
                    type: "shell",
                    command: "node",
                    args: [".vscode/elite-cursor-snippets/elite-cli.js", "scan"],
                    group: "build"
                },
                {
                    label: "Elite: Fix Current File",
                    type: "shell",
                    command: "node",
                    args: [".vscode/elite-cursor-snippets/elite-cli.js", "fix", "${file}"],
                    group: "build"
                }
            ]
        };

        fs.writeFileSync(tasksPath, JSON.stringify(tasks, null, 2));
        console.log('✅ VSCode tasks created');
    }

    /**
     * Run tests to verify installation
     */
    async runTests() {
        console.log('\n🧪 Running verification tests...');

        try {
            const testPath = path.join(this.eliteDir, 'test', 'run-tests.js');
            
            if (fs.existsSync(testPath)) {
                console.log('🔍 Running Elite Auto-Fix tests...');
                execSync(`node "${testPath}"`, { 
                    cwd: this.eliteDir, 
                    stdio: 'inherit' 
                });
                console.log('✅ All tests passed');
            } else {
                console.log('⚠️ Test file not found. Skipping tests.');
            }
        } catch (error) {
            console.log('⚠️ Some tests failed, but setup can continue.');
            console.log('   Run tests manually: node test/run-tests.js');
        }
    }

    /**
     * Display success message and next steps
     */
    async displaySuccessMessage() {
        console.log('\n🎉 Elite Cursor Snippets Automation Setup Complete!');
        console.log('=' .repeat(60));
        console.log('');
        console.log('🚀 What\'s been installed:');
        console.log('  ✅ Elite Auto-Fix engine');
        console.log('  ✅ Smart snippet selector');
        console.log('  ✅ Guardrails system');
        console.log('  ✅ Git hooks integration');
        console.log('  ✅ VSCode/Cursor integration');
        console.log('  ✅ Kenya-First validation');
        console.log('');
        console.log('🎯 Quick start commands:');
        console.log('  📁 Analyze file:    node .vscode/elite-cursor-snippets/elite-cli.js analyze <file>');
        console.log('  🔍 Scan project:    node .vscode/elite-cursor-snippets/elite-cli.js scan');
        console.log('  🔧 Fix issues:      node .vscode/elite-cursor-snippets/elite-cli.js fix <file>');
        console.log('  💡 Get suggestions: node .vscode/elite-cursor-snippets/elite-cli.js suggest "<context>"');
        console.log('');
        console.log('📚 Documentation:');
        console.log('  📖 Usage Guide:     .vscode/elite-cursor-snippets/USAGE_GUIDE.md');
        console.log('  📋 README:          .vscode/elite-cursor-snippets/README.md');
        console.log('  ⚙️ Configuration:   .vscode/elite-cursor-snippets/elite-auto-fix.config.json');
        console.log('');
        console.log('🇰🇪 Kenya-First Features:');
        console.log('  💰 Currency validation (KSh format)');
        console.log('  📱 Phone format validation (+254)');
        console.log('  🕐 Timezone validation (EAT)');
        console.log('  🗣️ Professional Kenyan English tone');
        console.log('');
        console.log('🔄 Git Integration:');
        console.log('  🔒 Pre-commit: Blocks commits with critical issues');
        console.log('  📈 Post-commit: Suggests improvements');
        console.log('  🚀 Pre-push: Full project analysis');
        console.log('');
        console.log('🎮 VSCode Integration:');
        console.log('  ⌨️ Type snippet prefixes and press Tab');
        console.log('  🔍 View issues in Problems panel');
        console.log('  ⚡ Use Ctrl+Shift+P → "Tasks: Run Task" → Elite commands');
        console.log('');
        console.log('🚀 Happy coding with Elite Cursor Snippets!');
        console.log('   Ship clean, ship fast, ship Kenya-first! 🇰🇪');
    }

    /**
     * Uninstall the automation system
     */
    async uninstall() {
        console.log('🗑️ Uninstalling Elite Cursor Snippets Automation...');

        try {
            // Uninstall git hooks
            const GitHooksInstaller = require('./scripts/install-git-hooks');
            const installer = new GitHooksInstaller();
            installer.uninstall();

            console.log('✅ Elite Auto-Fix uninstalled successfully');
        } catch (error) {
            console.error('❌ Uninstall failed:', error.message);
        }
    }
}

// CLI interface
if (require.main === module) {
    const setup = new EliteSetup();
    const command = process.argv[2];

    if (command === 'uninstall') {
        setup.uninstall();
    } else {
        setup.setup();
    }
}

module.exports = EliteSetup;
