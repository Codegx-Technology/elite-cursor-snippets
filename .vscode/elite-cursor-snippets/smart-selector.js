/**
 * Smart Snippet Selector
 * 
 * Intelligently selects the most appropriate snippet based on code context,
 * file type, detected issues, and user patterns.
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 1.0.0
 */

class SmartSnippetSelector {
    constructor(config = {}) {
        this.config = config;
        this.snippetDatabase = this.initializeSnippetDatabase();
        this.contextAnalyzer = new ContextAnalyzer();
        this.learningEngine = new LearningEngine();
    }

    /**
     * Initialize snippet database with metadata
     */
    initializeSnippetDatabase() {
        return {
            // Core AI Prompts
            'thinkwithai': {
                category: 'thinking',
                useCase: ['strategic-planning', 'complex-analysis', 'problem-solving'],
                triggers: ['complex', 'strategy', 'analyze', 'think', 'plan'],
                fileTypes: ['*'],
                priority: 70,
                description: 'Strategic reasoning and analysis'
            },
            'surgicalfix': {
                category: 'fixing',
                useCase: ['bug-fix', 'logic-error', 'quick-fix'],
                triggers: ['bug', 'error', 'fix', 'broken', 'issue'],
                fileTypes: ['js', 'jsx', 'ts', 'tsx', 'py', 'java'],
                priority: 90,
                description: 'Precision bug fixes and logic corrections'
            },
            'refactorintent': {
                category: 'refactoring',
                useCase: ['code-improvement', 'maintainability', 'clean-code'],
                triggers: ['refactor', 'improve', 'clean', 'optimize', 'restructure'],
                fileTypes: ['js', 'jsx', 'ts', 'tsx', 'py', 'java'],
                priority: 60,
                description: 'Intentional refactoring for better code quality'
            },
            'refactorclean': {
                category: 'refactoring',
                useCase: ['clean-code', 'best-practices', 'code-style'],
                triggers: ['clean', 'style', 'convention', 'standard'],
                fileTypes: ['js', 'jsx', 'ts', 'tsx'],
                priority: 55,
                description: 'Clean refactoring following best practices'
            },
            'autocomp': {
                category: 'react',
                useCase: ['react-optimization', 'component-improvement', 'performance'],
                triggers: ['component', 'react', 'performance', 'optimize'],
                fileTypes: ['jsx', 'tsx'],
                priority: 80,
                description: 'Auto-optimize React components'
            },
            'writetest': {
                category: 'testing',
                useCase: ['unit-testing', 'test-coverage', 'quality-assurance'],
                triggers: ['test', 'testing', 'coverage', 'spec'],
                fileTypes: ['js', 'jsx', 'ts', 'tsx', 'py'],
                priority: 50,
                description: 'Generate comprehensive unit tests'
            },
            'doccode': {
                category: 'documentation',
                useCase: ['documentation', 'comments', 'api-docs'],
                triggers: ['document', 'comment', 'doc', 'explain'],
                fileTypes: ['*'],
                priority: 30,
                description: 'Kenya-first documentation generation'
            },
            'unstuck': {
                category: 'problem-solving',
                useCase: ['debugging', 'problem-solving', 'guidance'],
                triggers: ['stuck', 'help', 'confused', 'lost'],
                fileTypes: ['*'],
                priority: 75,
                description: 'Get unstuck and find solutions'
            },
            'augmentsearch': {
                category: 'search',
                useCase: ['codebase-search', 'pattern-finding', 'exploration'],
                triggers: ['search', 'find', 'locate', 'explore'],
                fileTypes: ['*'],
                priority: 40,
                description: 'Semantic search across codebase'
            },
            'kenyafirst': {
                category: 'localization',
                useCase: ['localization', 'kenya-specific', 'cultural-adaptation'],
                triggers: ['kenya', 'localization', 'culture', 'local'],
                fileTypes: ['*'],
                priority: 35,
                description: 'Apply Kenya-first principles'
            },
            'mindreset': {
                category: 'meta',
                useCase: ['context-reset', 'refocusing', 'clarity'],
                triggers: ['reset', 'clear', 'refocus', 'start-over'],
                fileTypes: ['*'],
                priority: 45,
                description: 'Reset context and refocus'
            },
            'guardon': {
                category: 'quality',
                useCase: ['quality-assurance', 'standards', 'guardrails'],
                triggers: ['quality', 'standard', 'check', 'validate'],
                fileTypes: ['*'],
                priority: 65,
                description: 'Activate quality guardrails'
            },

            // Guardrail Snippets
            'srpcheck': {
                category: 'guardrail',
                useCase: ['single-responsibility', 'function-size', 'complexity'],
                triggers: ['long-function', 'complex-function', 'responsibility'],
                fileTypes: ['js', 'jsx', 'ts', 'tsx', 'py'],
                priority: 85,
                description: 'Single Responsibility Principle validation'
            },
            'noconlog': {
                category: 'guardrail',
                useCase: ['console-cleanup', 'production-ready', 'debugging'],
                triggers: ['console.log', 'debug', 'logging'],
                fileTypes: ['js', 'jsx', 'ts', 'tsx'],
                priority: 20,
                description: 'Remove console.log statements'
            },
            'hookcheck': {
                category: 'guardrail',
                useCase: ['react-hooks', 'functional-components', 'modern-react'],
                triggers: ['class-component', 'hooks', 'functional'],
                fileTypes: ['jsx', 'tsx'],
                priority: 70,
                description: 'React hooks best practices'
            },
            'kenyacheck': {
                category: 'guardrail',
                useCase: ['kenya-validation', 'localization-check', 'cultural-compliance'],
                triggers: ['currency', 'phone', 'timezone', 'format'],
                fileTypes: ['*'],
                priority: 40,
                description: 'Kenya-specific requirements validation'
            },
            'mobilecheck': {
                category: 'guardrail',
                useCase: ['mobile-optimization', 'responsive-design', 'mobile-first'],
                triggers: ['mobile', 'responsive', 'viewport', 'touch'],
                fileTypes: ['jsx', 'tsx', 'css', 'scss'],
                priority: 50,
                description: 'Mobile-first design validation'
            },
            'errorcheck': {
                category: 'guardrail',
                useCase: ['error-handling', 'exception-management', 'robustness'],
                triggers: ['error', 'exception', 'try-catch', 'async'],
                fileTypes: ['js', 'jsx', 'ts', 'tsx', 'py'],
                priority: 85,
                description: 'Error handling validation'
            },
            'securitycheck': {
                category: 'guardrail',
                useCase: ['security-validation', 'vulnerability-check', 'safety'],
                triggers: ['security', 'vulnerability', 'xss', 'injection'],
                fileTypes: ['*'],
                priority: 95,
                description: 'Security vulnerability detection'
            },
            'perfcheck': {
                category: 'guardrail',
                useCase: ['performance-optimization', 'efficiency', 'speed'],
                triggers: ['performance', 'slow', 'optimization', 'memory'],
                fileTypes: ['js', 'jsx', 'ts', 'tsx'],
                priority: 60,
                description: 'Performance optimization validation'
            },
            'a11ycheck': {
                category: 'guardrail',
                useCase: ['accessibility', 'inclusive-design', 'usability'],
                triggers: ['accessibility', 'a11y', 'screen-reader', 'aria'],
                fileTypes: ['jsx', 'tsx', 'html'],
                priority: 55,
                description: 'Accessibility standards validation'
            }
        };
    }

    /**
     * Select the best snippet based on context
     */
    selectBestSnippet(context) {
        const analysis = this.contextAnalyzer.analyze(context);
        const candidates = this.findCandidateSnippets(analysis);
        const scored = this.scoreSnippets(candidates, analysis);
        const best = this.rankSnippets(scored);

        return {
            primary: best[0],
            alternatives: best.slice(1, 4),
            reasoning: this.explainSelection(best[0], analysis),
            confidence: this.calculateConfidence(best[0], analysis)
        };
    }

    /**
     * Find candidate snippets based on analysis
     */
    findCandidateSnippets(analysis) {
        const candidates = [];

        for (const [snippetId, snippet] of Object.entries(this.snippetDatabase)) {
            let score = 0;

            // File type matching
            if (snippet.fileTypes.includes('*') || snippet.fileTypes.includes(analysis.fileType)) {
                score += 10;
            }

            // Trigger word matching
            for (const trigger of snippet.triggers) {
                if (analysis.keywords.includes(trigger)) {
                    score += 20;
                }
            }

            // Use case matching
            for (const useCase of snippet.useCase) {
                if (analysis.detectedUseCases.includes(useCase)) {
                    score += 15;
                }
            }

            // Issue type matching
            if (analysis.detectedIssues.some(issue => snippet.useCase.includes(issue.type))) {
                score += 25;
            }

            if (score > 0) {
                candidates.push({
                    id: snippetId,
                    snippet: snippet,
                    baseScore: score
                });
            }
        }

        return candidates;
    }

    /**
     * Score snippets based on context and priority
     */
    scoreSnippets(candidates, analysis) {
        return candidates.map(candidate => {
            let finalScore = candidate.baseScore;

            // Apply priority weighting
            finalScore += candidate.snippet.priority * 0.5;

            // Boost score for critical issues
            if (analysis.severity === 'critical' && candidate.snippet.category === 'guardrail') {
                finalScore += 30;
            }

            // Boost score for React-specific issues in React files
            if (analysis.fileType === 'jsx' || analysis.fileType === 'tsx') {
                if (candidate.snippet.category === 'react') {
                    finalScore += 20;
                }
            }

            // Apply learning engine adjustments
            const learningAdjustment = this.learningEngine.getAdjustment(candidate.id, analysis);
            finalScore += learningAdjustment;

            return {
                ...candidate,
                finalScore
            };
        });
    }

    /**
     * Rank snippets by final score
     */
    rankSnippets(scoredSnippets) {
        return scoredSnippets
            .sort((a, b) => b.finalScore - a.finalScore)
            .map(item => ({
                id: item.id,
                snippet: item.snippet,
                score: item.finalScore
            }));
    }

    /**
     * Explain why a snippet was selected
     */
    explainSelection(selectedSnippet, analysis) {
        const reasons = [];

        if (analysis.detectedIssues.length > 0) {
            reasons.push(`Detected ${analysis.detectedIssues.length} issue(s) matching this snippet's use case`);
        }

        if (selectedSnippet.snippet.fileTypes.includes(analysis.fileType)) {
            reasons.push(`Optimized for ${analysis.fileType} files`);
        }

        if (selectedSnippet.snippet.category === 'guardrail' && analysis.severity === 'critical') {
            reasons.push('Critical issue requires immediate guardrail intervention');
        }

        return reasons.join('; ');
    }

    /**
     * Calculate confidence in the selection
     */
    calculateConfidence(selectedSnippet, analysis) {
        let confidence = 0.5; // Base confidence

        // Increase confidence based on score
        if (selectedSnippet.score > 80) confidence += 0.3;
        else if (selectedSnippet.score > 60) confidence += 0.2;
        else if (selectedSnippet.score > 40) confidence += 0.1;

        // Increase confidence for exact matches
        if (analysis.keywords.some(keyword => 
            selectedSnippet.snippet.triggers.includes(keyword))) {
            confidence += 0.2;
        }

        return Math.min(confidence, 1.0);
    }

    /**
     * Get snippet suggestions for a given context
     */
    getSuggestions(context, limit = 5) {
        const result = this.selectBestSnippet(context);
        const suggestions = [result.primary, ...result.alternatives].slice(0, limit);

        return suggestions.map(suggestion => ({
            id: suggestion.id,
            description: suggestion.snippet.description,
            category: suggestion.snippet.category,
            score: suggestion.score,
            confidence: this.calculateConfidence(suggestion, this.contextAnalyzer.analyze(context))
        }));
    }

    /**
     * Learn from user selections to improve future recommendations
     */
    learnFromSelection(context, selectedSnippet, wasHelpful) {
        this.learningEngine.recordSelection(context, selectedSnippet, wasHelpful);
    }
}

/**
 * Context Analyzer - Analyzes code context to understand what's needed
 */
class ContextAnalyzer {
    analyze(context) {
        return {
            fileType: this.extractFileType(context.filePath || ''),
            keywords: this.extractKeywords(context.content || context.description || ''),
            detectedIssues: context.issues || [],
            detectedUseCases: this.detectUseCases(context),
            severity: this.determineSeverity(context.issues || []),
            codeComplexity: this.analyzeComplexity(context.content || ''),
            projectContext: this.analyzeProjectContext(context.filePath || '')
        };
    }

    extractFileType(filePath) {
        const ext = filePath.split('.').pop();
        return ext || 'unknown';
    }

    extractKeywords(text) {
        const keywords = [];
        const lowerText = text.toLowerCase();
        
        // Common programming keywords
        const patterns = [
            'bug', 'error', 'fix', 'refactor', 'optimize', 'performance',
            'test', 'component', 'react', 'hook', 'function', 'class',
            'security', 'accessibility', 'mobile', 'responsive', 'kenya',
            'documentation', 'comment', 'clean', 'improve', 'search'
        ];

        patterns.forEach(pattern => {
            if (lowerText.includes(pattern)) {
                keywords.push(pattern);
            }
        });

        return keywords;
    }

    detectUseCases(context) {
        const useCases = [];
        const content = (context.content || context.description || '').toLowerCase();

        if (content.includes('test') || content.includes('spec')) {
            useCases.push('unit-testing');
        }
        if (content.includes('component') && content.includes('react')) {
            useCases.push('react-optimization');
        }
        if (content.includes('bug') || content.includes('error')) {
            useCases.push('bug-fix');
        }
        if (content.includes('refactor') || content.includes('clean')) {
            useCases.push('code-improvement');
        }
        if (content.includes('performance') || content.includes('slow')) {
            useCases.push('performance-optimization');
        }

        return useCases;
    }

    determineSeverity(issues) {
        if (issues.some(issue => issue.severity === 'critical')) return 'critical';
        if (issues.some(issue => issue.severity === 'high')) return 'high';
        if (issues.some(issue => issue.severity === 'medium')) return 'medium';
        return 'low';
    }

    analyzeComplexity(content) {
        // Simple complexity analysis
        const lines = content.split('\n').length;
        const functions = (content.match(/function|=>/g) || []).length;
        const conditions = (content.match(/if|switch|for|while/g) || []).length;

        if (lines > 100 || functions > 10 || conditions > 15) return 'high';
        if (lines > 50 || functions > 5 || conditions > 8) return 'medium';
        return 'low';
    }

    analyzeProjectContext(filePath) {
        if (filePath.includes('component') || filePath.includes('src')) return 'frontend';
        if (filePath.includes('api') || filePath.includes('server')) return 'backend';
        if (filePath.includes('test') || filePath.includes('spec')) return 'testing';
        return 'general';
    }
}

/**
 * Learning Engine - Learns from user patterns to improve suggestions
 */
class LearningEngine {
    constructor() {
        this.selectionHistory = [];
        this.patterns = {};
    }

    recordSelection(context, selectedSnippet, wasHelpful) {
        this.selectionHistory.push({
            context,
            selectedSnippet,
            wasHelpful,
            timestamp: Date.now()
        });

        this.updatePatterns();
    }

    updatePatterns() {
        // Analyze selection history to identify patterns
        // This is a simplified implementation
        this.patterns = {};
        
        this.selectionHistory.forEach(record => {
            const key = `${record.context.fileType}_${record.selectedSnippet}`;
            if (!this.patterns[key]) {
                this.patterns[key] = { count: 0, helpful: 0 };
            }
            this.patterns[key].count++;
            if (record.wasHelpful) {
                this.patterns[key].helpful++;
            }
        });
    }

    getAdjustment(snippetId, analysis) {
        const key = `${analysis.fileType}_${snippetId}`;
        const pattern = this.patterns[key];
        
        if (!pattern) return 0;
        
        const successRate = pattern.helpful / pattern.count;
        if (successRate > 0.8) return 10;
        if (successRate > 0.6) return 5;
        if (successRate < 0.3) return -5;
        
        return 0;
    }
}

module.exports = SmartSnippetSelector;
