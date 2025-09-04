#!/usr/bin/env node

/**
 * Cursor AI Automation Integration
 * 
 * Automatically detects prompts in Cursor AI and triggers the right Elite snippets
 * without user interaction. This is TRUE AUTOMATION.
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const EliteAutoFix = require('./elite-auto-fix');
const SmartSnippetSelector = require('./smart-selector');

class CursorAutomation {
    constructor() {
        this.autoFix = new EliteAutoFix();
        this.selector = new SmartSnippetSelector();
        this.isActive = true;
        this.promptPatterns = this.initializePromptPatterns();
        this.workspaceRoot = this.findWorkspaceRoot();
        this.logFile = path.join(this.workspaceRoot, '.vscode', 'elite-automation.log');
    }

    /**
     * Initialize prompt patterns that trigger automation
     */
    initializePromptPatterns() {
        return {
            // Bug fixing patterns
            'bug-fix': {
                patterns: [
                    /fix\s+.*?(bug|issue|error|problem)/i,
                    /resolve\s+.*?(bug|issue|error)/i,
                    /debug\s+.*?(issue|problem)/i,
                    /(bug|issue|error)\s+.*?fix/i,
                    /not\s+working/i,
                    /broken/i
                ],
                snippet: 'surgicalfix',
                priority: 90,
                description: 'Bug fixing and error resolution'
            },

            // Performance optimization
            'performance': {
                patterns: [
                    /slow|performance|optimize|speed/i,
                    /improve.*?performance/i,
                    /make.*?faster/i,
                    /optimization/i,
                    /lag|laggy|sluggish/i
                ],
                snippet: 'perfcheck',
                priority: 80,
                description: 'Performance optimization'
            },

            // React component issues
            'react-component': {
                patterns: [
                    /react\s+component/i,
                    /component.*?(issue|problem|fix)/i,
                    /hook.*?(issue|problem)/i,
                    /render.*?(issue|problem)/i,
                    /state.*?(issue|problem)/i
                ],
                snippet: 'autocomp',
                priority: 85,
                description: 'React component optimization'
            },

            // Refactoring requests
            'refactoring': {
                patterns: [
                    /refactor/i,
                    /clean\s+up/i,
                    /improve.*?code/i,
                    /restructure/i,
                    /organize.*?code/i,
                    /messy.*?code/i
                ],
                snippet: 'refactorintent',
                priority: 70,
                description: 'Code refactoring and cleanup'
            },

            // Testing requests
            'testing': {
                patterns: [
                    /test|testing|spec/i,
                    /write.*?test/i,
                    /add.*?test/i,
                    /unit.*?test/i,
                    /test.*?coverage/i
                ],
                snippet: 'writetest',
                priority: 75,
                description: 'Test generation and coverage'
            },

            // Documentation requests
            'documentation': {
                patterns: [
                    /document|documentation|comment/i,
                    /add.*?comment/i,
                    /explain.*?code/i,
                    /document.*?function/i
                ],
                snippet: 'doccode',
                priority: 60,
                description: 'Code documentation'
            },

            // Security issues
            'security': {
                patterns: [
                    /security|secure|vulnerability/i,
                    /xss|injection|attack/i,
                    /sanitize|validate.*?input/i,
                    /security.*?issue/i
                ],
                snippet: 'securitycheck',
                priority: 95,
                description: 'Security vulnerability fixes'
            },

            // Accessibility issues
            'accessibility': {
                patterns: [
                    /accessibility|a11y/i,
                    /screen.*?reader/i,
                    /aria.*?label/i,
                    /alt.*?text/i,
                    /keyboard.*?navigation/i
                ],
                snippet: 'a11ycheck',
                priority: 70,
                description: 'Accessibility improvements'
            },

            // Kenya-specific issues
            'kenya-localization': {
                patterns: [
                    /kenya|kenyan|nairobi/i,
                    /shilling|ksh/i,
                    /\+254|254/i,
                    /east.*?africa.*?time|eat/i,
                    /localization|localisation/i
                ],
                snippet: 'kenyacheck',
                priority: 65,
                description: 'Kenya-first localization'
            },

            // General problem solving
            'problem-solving': {
                patterns: [
                    /stuck|help|confused/i,
                    /don\'t\s+know|not\s+sure/i,
                    /how\s+to/i,
                    /can\'t\s+figure/i,
                    /need\s+help/i
                ],
                snippet: 'unstuck',
                priority: 80,
                description: 'Problem-solving assistance'
            },

            // Strategic thinking
            'strategic': {
                patterns: [
                    /strategy|approach|architecture/i,
                    /best\s+practice/i,
                    /design\s+pattern/i,
                    /think.*?through/i,
                    /analyze.*?problem/i
                ],
                snippet: 'thinkwithai',
                priority: 75,
                description: 'Strategic analysis and planning'
            }
        };
    }

    /**
     * Find workspace root directory
     */
    findWorkspaceRoot() {
        let currentDir = process.cwd();
        
        while (currentDir !== path.dirname(currentDir)) {
            if (fs.existsSync(path.join(currentDir, '.vscode'))) {
                return currentDir;
            }
            currentDir = path.dirname(currentDir);
        }
        
        return process.cwd();
    }

    /**
     * Analyze prompt and determine the best automation action
     */
    analyzePrompt(prompt, context = {}) {
        const matches = [];
        
        // Check each pattern category
        for (const [category, config] of Object.entries(this.promptPatterns)) {
            for (const pattern of config.patterns) {
                if (pattern.test(prompt)) {
                    matches.push({
                        category,
                        snippet: config.snippet,
                        priority: config.priority,
                        description: config.description,
                        confidence: this.calculateConfidence(prompt, pattern)
                    });
                    break; // Only count first match per category
                }
            }
        }

        // Sort by priority and confidence
        matches.sort((a, b) => {
            const priorityDiff = b.priority - a.priority;
            if (priorityDiff !== 0) return priorityDiff;
            return b.confidence - a.confidence;
        });

        return matches;
    }

    /**
     * Calculate confidence score for pattern match
     */
    calculateConfidence(prompt, pattern) {
        const match = prompt.match(pattern);
        if (!match) return 0;
        
        // Base confidence
        let confidence = 0.7;
        
        // Increase confidence for exact keyword matches
        const keywords = match[0].toLowerCase();
        if (keywords.length > 3) confidence += 0.1;
        if (keywords.length > 6) confidence += 0.1;
        
        // Increase confidence for multiple related words
        const relatedWords = prompt.toLowerCase().match(/\b(fix|bug|error|issue|problem|optimize|improve|refactor|test)\b/g);
        if (relatedWords && relatedWords.length > 1) {
            confidence += 0.1;
        }
        
        return Math.min(confidence, 1.0);
    }

    /**
     * Automatically trigger the appropriate snippet based on prompt
     */
    async autoTrigger(prompt, filePath = null, options = {}) {
        try {
            this.log(`🤖 AUTO-TRIGGER: Analyzing prompt: "${prompt}"`);
            
            // Analyze the prompt
            const matches = this.analyzePrompt(prompt);
            
            if (matches.length === 0) {
                this.log('❌ No automation patterns matched');
                return {
                    success: false,
                    message: 'No automation patterns matched this prompt',
                    suggestions: ['Try using keywords like: fix, optimize, refactor, test, debug']
                };
            }

            const bestMatch = matches[0];
            this.log(`🎯 Best match: ${bestMatch.snippet} (${bestMatch.description})`);

            // If file path provided, analyze the file first
            let fileAnalysis = null;
            if (filePath && fs.existsSync(filePath)) {
                const content = fs.readFileSync(filePath, 'utf8');
                const issues = this.autoFix.analyzeCode(content, filePath);
                fileAnalysis = {
                    issues,
                    suggestions: this.autoFix.generateFixSuggestions(issues)
                };
                this.log(`📁 File analysis: ${issues.length} issues found`);
            }

            // Generate the automation response
            const response = await this.generateAutomationResponse(bestMatch, prompt, fileAnalysis, options);
            
            this.log(`✅ Automation complete: ${response.snippet}`);
            return response;

        } catch (error) {
            this.log(`❌ Automation error: ${error.message}`);
            return {
                success: false,
                error: error.message,
                fallback: 'thinkwithai'
            };
        }
    }

    /**
     * Generate automation response with context
     */
    async generateAutomationResponse(match, prompt, fileAnalysis, options) {
        const response = {
            success: true,
            snippet: match.snippet,
            category: match.category,
            description: match.description,
            confidence: match.confidence,
            prompt: prompt,
            timestamp: new Date().toISOString(),
            context: this.buildContext(match, prompt, fileAnalysis),
            cursorCommand: this.generateCursorCommand(match, prompt, fileAnalysis),
            alternatives: this.getAlternativeSnippets(match)
        };

        // Add file-specific context if available
        if (fileAnalysis) {
            response.fileIssues = fileAnalysis.issues.length;
            response.fileSuggestions = fileAnalysis.suggestions.slice(0, 3);
        }

        return response;
    }

    /**
     * Build context for the automation
     */
    buildContext(match, prompt, fileAnalysis) {
        let context = `// 🤖 ELITE AUTO-TRIGGERED: ${match.snippet.toUpperCase()}\n`;
        context += `// Prompt: "${prompt}"\n`;
        context += `// Category: ${match.description}\n`;
        context += `// Confidence: ${(match.confidence * 100).toFixed(1)}%\n`;
        
        if (fileAnalysis && fileAnalysis.issues.length > 0) {
            context += `// File Issues Detected: ${fileAnalysis.issues.length}\n`;
            const criticalIssues = fileAnalysis.issues.filter(i => i.severity === 'critical');
            if (criticalIssues.length > 0) {
                context += `// 🚨 Critical Issues: ${criticalIssues.length}\n`;
            }
        }
        
        context += `// 🇰🇪 Kenya-First Engineering Automation\n`;
        context += `// Generated: ${new Date().toLocaleString()}\n\n`;
        
        return context;
    }

    /**
     * Generate Cursor AI command
     */
    generateCursorCommand(match, prompt, fileAnalysis) {
        return {
            snippet: match.snippet,
            trigger: `Type "${match.snippet}" and press Tab in Cursor AI`,
            autoContext: true,
            promptEnhancement: this.enhancePromptForCursor(match, prompt, fileAnalysis)
        };
    }

    /**
     * Enhance prompt for Cursor AI with context
     */
    enhancePromptForCursor(match, originalPrompt, fileAnalysis) {
        let enhanced = originalPrompt;
        
        // Add context based on snippet type
        switch (match.snippet) {
            case 'surgicalfix':
                enhanced += '\n\nApply precise surgical fixes without breaking existing functionality. Focus on the specific issue mentioned.';
                break;
            case 'perfcheck':
                enhanced += '\n\nOptimize for performance. Check for inefficient loops, unnecessary re-renders, and memory leaks.';
                break;
            case 'autocomp':
                enhanced += '\n\nOptimize React component. Convert to functional component with hooks if needed. Add performance optimizations.';
                break;
            case 'securitycheck':
                enhanced += '\n\nAddress security vulnerabilities. Sanitize inputs, avoid XSS, and follow security best practices.';
                break;
            case 'kenyacheck':
                enhanced += '\n\nApply Kenya-first principles. Use KSh currency, +254 phone format, EAT timezone, and professional Kenyan English.';
                break;
        }

        // Add file analysis context
        if (fileAnalysis && fileAnalysis.issues.length > 0) {
            const criticalIssues = fileAnalysis.issues.filter(i => i.severity === 'critical');
            if (criticalIssues.length > 0) {
                enhanced += `\n\n🚨 Critical issues detected: ${criticalIssues.map(i => i.message).join(', ')}`;
            }
        }

        return enhanced;
    }

    /**
     * Get alternative snippets
     */
    getAlternativeSnippets(match) {
        const alternatives = [];
        
        // Add related snippets based on category
        const relatedSnippets = {
            'bug-fix': ['errorcheck', 'thinkwithai', 'unstuck'],
            'performance': ['autocomp', 'refactorclean', 'surgicalfix'],
            'react-component': ['hookcheck', 'perfcheck', 'a11ycheck'],
            'refactoring': ['refactorclean', 'srpcheck', 'doccode'],
            'testing': ['surgicalfix', 'refactorintent'],
            'security': ['errorcheck', 'surgicalfix'],
            'accessibility': ['mobilecheck', 'autocomp'],
            'kenya-localization': ['kenyafirst', 'doccode']
        };

        const related = relatedSnippets[match.category] || [];
        related.forEach(snippet => {
            if (snippet !== match.snippet) {
                alternatives.push(snippet);
            }
        });

        return alternatives.slice(0, 3);
    }

    /**
     * Log automation activity
     */
    log(message) {
        const timestamp = new Date().toISOString();
        const logEntry = `[${timestamp}] ${message}\n`;
        
        try {
            fs.appendFileSync(this.logFile, logEntry);
        } catch (error) {
            console.error('Failed to write to log file:', error.message);
        }
        
        if (process.env.ELITE_DEBUG) {
            console.log(logEntry.trim());
        }
    }

    /**
     * Start monitoring for prompts (for future integration)
     */
    startMonitoring() {
        this.log('🚀 Elite Cursor Automation started monitoring');
        this.isActive = true;
        
        // This would integrate with Cursor AI's extension API
        // For now, it's a placeholder for future development
        console.log('🤖 Elite Automation is active and ready!');
        console.log('💡 Usage: node cursor-automation.js "fix the footer blinking button issue"');
    }

    /**
     * Stop monitoring
     */
    stopMonitoring() {
        this.log('⏹️ Elite Cursor Automation stopped');
        this.isActive = false;
    }
}

// CLI interface for testing
if (require.main === module) {
    const automation = new CursorAutomation();
    const prompt = process.argv[2];

    if (!prompt) {
        console.log('🤖 Elite Cursor Automation System');
        console.log('Usage: node cursor-automation.js "your prompt here"');
        console.log('');
        console.log('Examples:');
        console.log('  node cursor-automation.js "fix the footer blinking button issue"');
        console.log('  node cursor-automation.js "optimize React component performance"');
        console.log('  node cursor-automation.js "add unit tests for this function"');
        console.log('  node cursor-automation.js "refactor this messy code"');
        process.exit(1);
    }

    // Test the automation
    automation.autoTrigger(prompt).then(result => {
        console.log('\n🤖 ELITE AUTOMATION RESULT:');
        console.log('=' .repeat(50));
        
        if (result.success) {
            console.log(`✅ Triggered: ${result.snippet}`);
            console.log(`📝 Description: ${result.description}`);
            console.log(`🎯 Confidence: ${(result.confidence * 100).toFixed(1)}%`);
            console.log(`⚡ Action: ${result.cursorCommand.trigger}`);
            
            if (result.alternatives.length > 0) {
                console.log(`🔄 Alternatives: ${result.alternatives.join(', ')}`);
            }
            
            console.log('\n📋 Context for Cursor AI:');
            console.log(result.context);
            
            console.log('🚀 Enhanced Prompt:');
            console.log(result.cursorCommand.promptEnhancement);
        } else {
            console.log(`❌ Failed: ${result.message || result.error}`);
            if (result.suggestions) {
                console.log(`💡 Suggestions: ${result.suggestions.join(', ')}`);
            }
        }
    }).catch(error => {
        console.error('❌ Automation failed:', error.message);
    });
}

module.exports = CursorAutomation;
