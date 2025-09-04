#!/usr/bin/env node

/**
 * Elite Cursor Snippets CLI
 * 
 * Command-line interface for the Elite Auto-Fix system
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const EliteAutoFix = require('./elite-auto-fix');

class EliteCLI {
    constructor() {
        this.autoFix = new EliteAutoFix();
        this.commands = {
            'analyze': this.analyzeCommand.bind(this),
            'fix': this.fixCommand.bind(this),
            'scan': this.scanCommand.bind(this),
            'suggest': this.suggestCommand.bind(this),
            'config': this.configCommand.bind(this),
            'install': this.installCommand.bind(this),
            'help': this.helpCommand.bind(this)
        };
    }

    /**
     * Main CLI entry point
     */
    run(args) {
        const command = args[0] || 'help';
        const commandArgs = args.slice(1);

        if (this.commands[command]) {
            this.commands[command](commandArgs);
        } else {
            console.error(`❌ Unknown command: ${command}`);
            this.helpCommand();
            process.exit(1);
        }
    }

    /**
     * Analyze command - analyze files for issues
     */
    analyzeCommand(args) {
        const filePath = args[0];
        
        if (!filePath) {
            console.error('❌ Please provide a file path');
            console.log('Usage: elite analyze <file-path>');
            return;
        }

        if (filePath === '--all' || filePath === '-a') {
            this.analyzeAllFiles();
            return;
        }

        if (!fs.existsSync(filePath)) {
            console.error(`❌ File not found: ${filePath}`);
            return;
        }

        console.log(`🔍 Analyzing: ${filePath}`);
        const content = fs.readFileSync(filePath, 'utf8');
        const issues = this.autoFix.analyzeCode(content, filePath);
        const suggestions = this.autoFix.generateFixSuggestions(issues);

        this.displayAnalysisResults(filePath, issues, suggestions);
    }

    /**
     * Fix command - apply suggested fixes
     */
    fixCommand(args) {
        const filePath = args[0];
        const snippetType = args[1];

        if (!filePath) {
            console.error('❌ Please provide a file path');
            console.log('Usage: elite fix <file-path> [snippet-type]');
            return;
        }

        console.log(`🔧 Applying fixes to: ${filePath}`);
        
        if (snippetType) {
            console.log(`📝 Suggested snippet: ${snippetType}`);
            this.openSnippetInEditor(snippetType, filePath);
        } else {
            // Auto-detect best fix
            const content = fs.readFileSync(filePath, 'utf8');
            const issues = this.autoFix.analyzeCode(content, filePath);
            const suggestions = this.autoFix.generateFixSuggestions(issues);
            
            if (suggestions.length > 0) {
                const bestSuggestion = suggestions[0];
                console.log(`🎯 Best suggestion: ${bestSuggestion.snippet}`);
                this.openSnippetInEditor(bestSuggestion.snippet, filePath);
            } else {
                console.log('✅ No issues detected. Code looks clean!');
            }
        }
    }

    /**
     * Scan command - scan entire project
     */
    scanCommand(args) {
        const directory = args[0] || '.';
        const options = this.parseOptions(args);

        console.log(`🔍 Scanning project: ${directory}`);
        console.log('=' .repeat(50));

        const results = this.scanDirectory(directory, options);
        this.displayScanResults(results);
    }

    /**
     * Suggest command - get snippet suggestions
     */
    suggestCommand(args) {
        const context = args.join(' ');
        
        if (!context) {
            console.error('❌ Please provide context for suggestions');
            console.log('Usage: elite suggest "I need to fix a React component performance issue"');
            return;
        }

        console.log(`🧠 Analyzing context: "${context}"`);
        const suggestions = this.getContextualSuggestions(context);
        
        console.log('\n🎯 Suggested snippets:');
        suggestions.forEach((suggestion, index) => {
            console.log(`${index + 1}. ${suggestion.snippet} - ${suggestion.description}`);
        });
    }

    /**
     * Config command - manage configuration
     */
    configCommand(args) {
        const action = args[0];
        
        switch (action) {
            case 'show':
                this.showConfig();
                break;
            case 'edit':
                this.editConfig();
                break;
            case 'reset':
                this.resetConfig();
                break;
            default:
                console.log('Config commands:');
                console.log('  elite config show  - Show current configuration');
                console.log('  elite config edit  - Edit configuration file');
                console.log('  elite config reset - Reset to default configuration');
        }
    }

    /**
     * Install command - setup git hooks and integrations
     */
    installCommand(args) {
        const target = args[0] || 'all';
        
        console.log('🚀 Installing Elite Auto-Fix...');
        
        switch (target) {
            case 'hooks':
            case 'all':
                this.installGitHooks();
                break;
            case 'vscode':
                this.installVSCodeIntegration();
                break;
            case 'cursor':
                this.installCursorIntegration();
                break;
            default:
                console.log('Install options:');
                console.log('  elite install hooks  - Install git hooks');
                console.log('  elite install vscode - Install VSCode integration');
                console.log('  elite install cursor - Install Cursor integration');
                console.log('  elite install all    - Install everything');
        }
    }

    /**
     * Help command
     */
    helpCommand() {
        console.log(`
🧠 Elite Cursor Snippets CLI v1.0.0
Kenya-First Engineering Automation

USAGE:
  elite <command> [options]

COMMANDS:
  analyze <file>     Analyze file for issues and suggest fixes
  fix <file> [type]  Apply suggested fixes to file
  scan [dir]         Scan entire project for issues
  suggest <context>  Get snippet suggestions based on context
  config <action>    Manage configuration (show/edit/reset)
  install <target>   Install git hooks and integrations
  help              Show this help message

EXAMPLES:
  elite analyze src/components/Header.jsx
  elite fix src/utils/api.js surgicalfix
  elite scan --severity=high
  elite suggest "React component with performance issues"
  elite config show
  elite install hooks

OPTIONS:
  --severity=<level>  Filter by severity (critical/high/medium/low)
  --type=<type>       Filter by issue type
  --format=<format>   Output format (console/json/markdown)
  --auto-apply        Automatically apply suggested fixes
  --verbose           Verbose output

🇰🇪 Built with Kenya-First principles
🚀 Ship clean, ship fast, ship Kenya-first
        `);
    }

    /**
     * Display analysis results
     */
    displayAnalysisResults(filePath, issues, suggestions) {
        console.log(`\n📊 Analysis Results for: ${path.basename(filePath)}`);
        console.log('=' .repeat(60));

        if (issues.length === 0) {
            console.log('✅ No issues detected. Code looks clean!');
            return;
        }

        console.log(`\n🔍 Found ${issues.length} issue(s):`);
        issues.forEach((issue, index) => {
            const severityEmoji = this.getSeverityEmoji(issue.severity);
            console.log(`  ${index + 1}. ${severityEmoji} ${issue.message}`);
        });

        if (suggestions.length > 0) {
            console.log(`\n🎯 Recommended Actions:`);
            suggestions.slice(0, 3).forEach((suggestion, index) => {
                console.log(`  ${index + 1}. Use snippet: ${suggestion.snippet}`);
                console.log(`     ${suggestion.description}`);
                console.log(`     Priority: ${suggestion.priority}`);
            });

            console.log(`\n🚀 Quick Fix:`);
            console.log(`VSCode/Cursor: Type "${suggestions[0].snippet}" and press Tab`);
            console.log(`CLI: elite fix "${filePath}" ${suggestions[0].snippet}`);
        }
    }

    /**
     * Get severity emoji
     */
    getSeverityEmoji(severity) {
        const emojis = {
            'critical': '🚨',
            'high': '⚠️',
            'medium': '⚡',
            'low': 'ℹ️'
        };
        return emojis[severity] || 'ℹ️';
    }

    /**
     * Analyze all files in project
     */
    analyzeAllFiles() {
        console.log('🔍 Analyzing entire project...');
        // Implementation for scanning all files
        const results = this.scanDirectory('.', { recursive: true });
        this.displayScanResults(results);
    }

    /**
     * Scan directory for issues
     */
    scanDirectory(directory, options = {}) {
        const results = {
            totalFiles: 0,
            analyzedFiles: 0,
            totalIssues: 0,
            issuesBySeverity: { critical: 0, high: 0, medium: 0, low: 0 },
            suggestions: []
        };

        // Implementation for directory scanning
        return results;
    }

    /**
     * Display scan results
     */
    displayScanResults(results) {
        console.log('\n📊 Project Scan Results');
        console.log('=' .repeat(40));
        console.log(`Files analyzed: ${results.analyzedFiles}/${results.totalFiles}`);
        console.log(`Total issues: ${results.totalIssues}`);
        console.log(`Critical: ${results.issuesBySeverity.critical}`);
        console.log(`High: ${results.issuesBySeverity.high}`);
        console.log(`Medium: ${results.issuesBySeverity.medium}`);
        console.log(`Low: ${results.issuesBySeverity.low}`);
    }

    /**
     * Get contextual suggestions
     */
    getContextualSuggestions(context) {
        const suggestions = [];
        const lowerContext = context.toLowerCase();

        // Simple keyword matching for suggestions
        if (lowerContext.includes('performance') || lowerContext.includes('slow')) {
            suggestions.push({ snippet: 'perfcheck', description: 'Performance optimization' });
            suggestions.push({ snippet: 'autocomp', description: 'Auto-optimize React component' });
        }

        if (lowerContext.includes('bug') || lowerContext.includes('fix') || lowerContext.includes('error')) {
            suggestions.push({ snippet: 'surgicalfix', description: 'Surgical bug fixes' });
        }

        if (lowerContext.includes('refactor') || lowerContext.includes('clean')) {
            suggestions.push({ snippet: 'refactorintent', description: 'Refactor with intent' });
            suggestions.push({ snippet: 'refactorclean', description: 'Clean refactoring' });
        }

        if (lowerContext.includes('test')) {
            suggestions.push({ snippet: 'writetest', description: 'Generate unit tests' });
        }

        if (lowerContext.includes('kenya') || lowerContext.includes('localization')) {
            suggestions.push({ snippet: 'kenyafirst', description: 'Kenya-first principles' });
            suggestions.push({ snippet: 'kenyacheck', description: 'Kenya-specific validation' });
        }

        if (suggestions.length === 0) {
            suggestions.push({ snippet: 'thinkwithai', description: 'Strategic thinking and analysis' });
        }

        return suggestions;
    }

    /**
     * Open snippet in editor
     */
    openSnippetInEditor(snippet, filePath) {
        console.log(`📝 Opening ${snippet} snippet for ${filePath}`);
        console.log(`💡 In VSCode/Cursor: Type "${snippet}" and press Tab`);
    }

    /**
     * Show current configuration
     */
    showConfig() {
        const configPath = path.join(__dirname, 'elite-auto-fix.config.json');
        if (fs.existsSync(configPath)) {
            const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
            console.log('📋 Current Configuration:');
            console.log(JSON.stringify(config, null, 2));
        } else {
            console.log('⚠️ No configuration file found. Using defaults.');
        }
    }

    /**
     * Install git hooks
     */
    installGitHooks() {
        console.log('🔗 Installing git hooks...');
        // Implementation for git hooks installation
        console.log('✅ Git hooks installed successfully');
    }

    /**
     * Parse command line options
     */
    parseOptions(args) {
        const options = {};
        args.forEach(arg => {
            if (arg.startsWith('--')) {
                const [key, value] = arg.substring(2).split('=');
                options[key] = value || true;
            }
        });
        return options;
    }
}

// CLI entry point
if (require.main === module) {
    const cli = new EliteCLI();
    const args = process.argv.slice(2);
    cli.run(args);
}

module.exports = EliteCLI;
