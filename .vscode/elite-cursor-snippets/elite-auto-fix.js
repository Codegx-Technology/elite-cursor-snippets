#!/usr/bin/env node

/**
 * Elite Cursor Snippets Automation System
 * 
 * Intelligently analyzes code issues and suggests the appropriate snippet/fix
 * from the elite-cursor-snippets arsenal.
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class EliteAutoFix {
    constructor() {
        this.snippetMappings = this.loadSnippetMappings();
        this.guardrails = this.loadGuardrails();
        this.config = this.loadConfig();
    }

    /**
     * Load snippet mappings from configuration
     */
    loadSnippetMappings() {
        return {
            // Code Quality Issues
            'long-function': 'refactorintent',
            'complex-logic': 'thinkwithai',
            'duplicate-code': 'refactorclean',
            'poor-naming': 'refactorintent',
            'missing-error-handling': 'surgicalfix',
            
            // React-specific Issues
            'class-component': 'autocomp',
            'missing-hooks': 'hookcheck',
            'performance-issue': 'perfcheck',
            'accessibility-issue': 'a11ycheck',
            
            // Testing Issues
            'missing-tests': 'writetest',
            'test-coverage': 'writetest',
            
            // Documentation Issues
            'missing-docs': 'doccode',
            'poor-comments': 'doccode',
            
            // Kenya-specific Issues
            'currency-format': 'kenyacheck',
            'phone-format': 'kenyacheck',
            'timezone-issue': 'kenyacheck',
            'localization': 'kenyafirst',
            
            // Security Issues
            'security-vulnerability': 'securitycheck',
            'input-validation': 'securitycheck',
            
            // Performance Issues
            'bundle-size': 'perfcheck',
            'memory-leak': 'perfcheck',
            'slow-render': 'autocomp',
            
            // General Issues
            'console-log': 'noconlog',
            'single-responsibility': 'srpcheck',
            'mobile-optimization': 'mobilecheck',
            'stuck-problem': 'unstuck',
            'search-codebase': 'augmentsearch'
        };
    }

    /**
     * Load guardrails configuration
     */
    loadGuardrails() {
        return {
            'srpcheck': {
                patterns: [
                    /function\s+\w+\([^)]*\)\s*{[^}]{200,}}/g, // Long functions
                    /const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*{[^}]{200,}}/g // Long arrow functions
                ],
                message: 'Function is too long. Consider breaking it down (Single Responsibility Principle)'
            },
            'noconlog': {
                patterns: [
                    /console\.log\(/g,
                    /console\.warn\(/g,
                    /console\.error\(/g
                ],
                message: 'Remove console.log statements before production'
            },
            'hookcheck': {
                patterns: [
                    /class\s+\w+\s+extends\s+React\.Component/g,
                    /class\s+\w+\s+extends\s+Component/g
                ],
                message: 'Consider converting to functional component with hooks'
            },
            'kenyacheck': {
                patterns: [
                    /\$\d+/g, // Dollar signs
                    /USD/g,
                    /\+1\d{10}/g // US phone format
                ],
                message: 'Use Kenya-first formats (KSh, +254, EAT timezone)'
            },
            'mobilecheck': {
                patterns: [
                    /width:\s*\d+px/g,
                    /height:\s*\d+px/g
                ],
                message: 'Use responsive units (rem, %, vw, vh) for mobile-first design'
            },
            'errorcheck': {
                patterns: [
                    /fetch\(/g,
                    /axios\./g,
                    /async\s+function/g
                ],
                message: 'Add proper error handling with try/catch blocks'
            },
            'securitycheck': {
                patterns: [
                    /innerHTML\s*=/g,
                    /dangerouslySetInnerHTML/g,
                    /eval\(/g
                ],
                message: 'Potential security vulnerability detected'
            },
            'perfcheck': {
                patterns: [
                    /useEffect\(\(\)\s*=>\s*{[^}]*},\s*\[\]\)/g, // Empty dependency array
                    /map\([^)]*\)\s*\.map\(/g // Chained maps
                ],
                message: 'Performance optimization opportunity detected'
            },
            'a11ycheck': {
                patterns: [
                    /<img(?![^>]*alt=)/g,
                    /<button(?![^>]*aria-label)/g,
                    /<input(?![^>]*aria-label)(?![^>]*placeholder)/g
                ],
                message: 'Accessibility improvement needed (alt text, aria-labels)'
            }
        };
    }

    /**
     * Load configuration from file or use defaults
     */
    loadConfig() {
        const configPath = path.join(__dirname, 'elite-auto-fix.config.json');
        if (fs.existsSync(configPath)) {
            return JSON.parse(fs.readFileSync(configPath, 'utf8'));
        }
        
        return {
            autoApply: false,
            verboseOutput: true,
            enableGuardrails: true,
            excludePatterns: ['node_modules', '.git', 'dist', 'build'],
            fileExtensions: ['.js', '.jsx', '.ts', '.tsx', '.vue', '.py', '.java', '.cs']
        };
    }

    /**
     * Analyze code content and detect issues
     */
    analyzeCode(content, filePath = '') {
        const issues = [];
        const fileExt = path.extname(filePath);
        
        // Run guardrails checks
        if (this.config.enableGuardrails) {
            for (const [guardName, guard] of Object.entries(this.guardrails)) {
                for (const pattern of guard.patterns) {
                    const matches = content.match(pattern);
                    if (matches) {
                        issues.push({
                            type: 'guardrail',
                            guard: guardName,
                            message: guard.message,
                            matches: matches.length,
                            snippet: guardName,
                            severity: this.getIssueSeverity(guardName)
                        });
                    }
                }
            }
        }

        // Detect code quality issues
        issues.push(...this.detectCodeQualityIssues(content, fileExt));
        
        // Detect React-specific issues
        if (['.jsx', '.tsx'].includes(fileExt)) {
            issues.push(...this.detectReactIssues(content));
        }

        // Detect Kenya-specific issues
        issues.push(...this.detectKenyaIssues(content));

        return issues;
    }

    /**
     * Detect code quality issues
     */
    detectCodeQualityIssues(content, fileExt) {
        const issues = [];
        
        // Long functions
        const longFunctions = content.match(/function\s+\w+\([^)]*\)\s*{[^}]{300,}}/g);
        if (longFunctions) {
            issues.push({
                type: 'code-quality',
                issue: 'long-function',
                message: 'Function is too long and complex',
                snippet: 'refactorintent',
                severity: 'medium'
            });
        }

        // Missing error handling in async functions
        const asyncWithoutTryCatch = content.match(/async\s+function[^{]*{(?![^}]*try)[^}]*}/g);
        if (asyncWithoutTryCatch) {
            issues.push({
                type: 'code-quality',
                issue: 'missing-error-handling',
                message: 'Async function missing error handling',
                snippet: 'surgicalfix',
                severity: 'high'
            });
        }

        return issues;
    }

    /**
     * Detect React-specific issues
     */
    detectReactIssues(content) {
        const issues = [];
        
        // Class components
        if (content.includes('extends React.Component') || content.includes('extends Component')) {
            issues.push({
                type: 'react',
                issue: 'class-component',
                message: 'Consider converting to functional component',
                snippet: 'autocomp',
                severity: 'medium'
            });
        }

        // Missing key prop in lists
        if (content.match(/\.map\([^}]*<\w+(?![^>]*key=)/g)) {
            issues.push({
                type: 'react',
                issue: 'missing-key-prop',
                message: 'Missing key prop in mapped components',
                snippet: 'surgicalfix',
                severity: 'high'
            });
        }

        return issues;
    }

    /**
     * Detect Kenya-specific issues
     */
    detectKenyaIssues(content) {
        const issues = [];
        
        // Currency format
        if (content.match(/\$\d+|\bUSD\b/g)) {
            issues.push({
                type: 'kenya',
                issue: 'currency-format',
                message: 'Use Kenya Shilling (KSh) format instead of USD',
                snippet: 'kenyacheck',
                severity: 'medium'
            });
        }

        // Phone format
        if (content.match(/\+1\d{10}/g)) {
            issues.push({
                type: 'kenya',
                issue: 'phone-format',
                message: 'Use Kenya phone format (+254) instead of US format',
                snippet: 'kenyacheck',
                severity: 'medium'
            });
        }

        return issues;
    }

    /**
     * Get issue severity level
     */
    getIssueSeverity(guardName) {
        const severityMap = {
            'securitycheck': 'critical',
            'errorcheck': 'high',
            'hookcheck': 'medium',
            'srpcheck': 'medium',
            'perfcheck': 'medium',
            'a11ycheck': 'medium',
            'kenyacheck': 'low',
            'mobilecheck': 'low',
            'noconlog': 'low'
        };
        
        return severityMap[guardName] || 'low';
    }

    /**
     * Generate fix suggestions based on detected issues
     */
    generateFixSuggestions(issues) {
        const suggestions = [];
        
        // Group issues by snippet type
        const groupedIssues = {};
        issues.forEach(issue => {
            const snippet = issue.snippet;
            if (!groupedIssues[snippet]) {
                groupedIssues[snippet] = [];
            }
            groupedIssues[snippet].push(issue);
        });

        // Generate suggestions for each snippet type
        for (const [snippet, snippetIssues] of Object.entries(groupedIssues)) {
            suggestions.push({
                snippet,
                issues: snippetIssues,
                priority: this.calculatePriority(snippetIssues),
                description: this.getSnippetDescription(snippet),
                command: this.generateSnippetCommand(snippet, snippetIssues)
            });
        }

        // Sort by priority
        suggestions.sort((a, b) => b.priority - a.priority);
        
        return suggestions;
    }

    /**
     * Calculate priority based on issue severity
     */
    calculatePriority(issues) {
        const severityWeights = {
            'critical': 100,
            'high': 75,
            'medium': 50,
            'low': 25
        };
        
        return issues.reduce((total, issue) => {
            return total + (severityWeights[issue.severity] || 25);
        }, 0);
    }

    /**
     * Get snippet description
     */
    getSnippetDescription(snippet) {
        const descriptions = {
            'surgicalfix': 'Apply precise surgical fixes to resolve bugs and logic issues',
            'refactorintent': 'Refactor code with clear intent for better maintainability',
            'refactorclean': 'Clean refactoring following best practices',
            'autocomp': 'Auto-optimize React components for performance',
            'writetest': 'Generate comprehensive unit tests',
            'doccode': 'Create Kenya-first documentation',
            'thinkwithai': 'Strategic thinking and problem analysis',
            'unstuck': 'Get unstuck when facing complex problems',
            'augmentsearch': 'Semantic search across codebase',
            'kenyafirst': 'Apply Kenya-first principles and localization',
            'guardon': 'Activate quality guardrails and standards',
            'srpcheck': 'Ensure single responsibility principle',
            'noconlog': 'Remove console.log statements',
            'hookcheck': 'Apply React hooks best practices',
            'kenyacheck': 'Validate Kenya-specific requirements',
            'mobilecheck': 'Optimize for mobile-first design',
            'errorcheck': 'Add proper error handling',
            'securitycheck': 'Address security vulnerabilities',
            'perfcheck': 'Optimize performance',
            'a11ycheck': 'Improve accessibility'
        };
        
        return descriptions[snippet] || 'Apply appropriate fixes';
    }

    /**
     * Generate snippet command with context
     */
    generateSnippetCommand(snippet, issues) {
        const issueDescriptions = issues.map(issue => issue.message).join(', ');
        
        return {
            prefix: snippet,
            context: issueDescriptions,
            template: this.getSnippetTemplate(snippet, issues)
        };
    }

    /**
     * Get snippet template with context
     */
    getSnippetTemplate(snippet, issues) {
        const templates = {
            'surgicalfix': `// 🔧 SURGICAL FIX MODE
// Issues detected: ${issues.map(i => i.message).join(', ')}
// Apply precise fixes without breaking existing functionality`,
            
            'refactorintent': `// 🔄 REFACTOR WITH INTENT
// Code quality issues: ${issues.map(i => i.message).join(', ')}
// Refactor following clean code principles`,
            
            'autocomp': `// ⚡ AUTO-OPTIMIZE COMPONENT
// React optimization needed: ${issues.map(i => i.message).join(', ')}
// Convert to functional component with performance optimizations`,
            
            'writetest': `// 🧪 WRITE COMPREHENSIVE TESTS
// Testing gaps identified: ${issues.map(i => i.message).join(', ')}
// Generate unit tests with edge cases`,
            
            'kenyacheck': `// 🇰🇪 KENYA-FIRST VALIDATION
// Kenya-specific issues: ${issues.map(i => i.message).join(', ')}
// Apply Kenya-first principles (KSh, +254, EAT timezone)`
        };
        
        return templates[snippet] || `// ${snippet.toUpperCase()} - ${issues.map(i => i.message).join(', ')}`;
    }
}

module.exports = EliteAutoFix;

// CLI interface
if (require.main === module) {
    const autoFix = new EliteAutoFix();
    
    // Get file path from command line arguments
    const filePath = process.argv[2];
    
    if (!filePath) {
        console.log('Usage: node elite-auto-fix.js <file-path>');
        console.log('       node elite-auto-fix.js --analyze-all');
        process.exit(1);
    }
    
    if (filePath === '--analyze-all') {
        console.log('🔍 Analyzing entire codebase...');
        // Implementation for analyzing all files
    } else {
        if (!fs.existsSync(filePath)) {
            console.error(`File not found: ${filePath}`);
            process.exit(1);
        }
        
        const content = fs.readFileSync(filePath, 'utf8');
        const issues = autoFix.analyzeCode(content, filePath);
        const suggestions = autoFix.generateFixSuggestions(issues);
        
        console.log(`\n🧠 Elite Auto-Fix Analysis for: ${filePath}`);
        console.log('=' .repeat(60));
        
        if (suggestions.length === 0) {
            console.log('✅ No issues detected. Code looks clean!');
        } else {
            suggestions.forEach((suggestion, index) => {
                console.log(`\n${index + 1}. ${suggestion.description}`);
                console.log(`   Priority: ${suggestion.priority}`);
                console.log(`   Snippet: ${suggestion.snippet}`);
                console.log(`   Issues: ${suggestion.issues.length}`);
                console.log(`   Template:\n${suggestion.command.template}`);
            });
            
            console.log('\n🚀 Recommended Action:');
            console.log(`Use snippet: ${suggestions[0].snippet}`);
            console.log(`VSCode: Type "${suggestions[0].snippet}" and press Tab`);
        }
    }
}
