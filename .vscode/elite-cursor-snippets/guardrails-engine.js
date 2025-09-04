/**
 * Guardrails Engine
 * 
 * Implements defensive patterns and quality checks for the Elite Cursor Snippets system.
 * Automatically detects code quality issues and suggests appropriate guardrail snippets.
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 1.0.0
 */

class GuardrailsEngine {
    constructor(config = {}) {
        this.config = config;
        this.rules = this.initializeRules();
        this.enabled = config.enableGuardrails !== false;
    }

    /**
     * Initialize guardrail rules
     */
    initializeRules() {
        return {
            // Single Responsibility Principle
            srpcheck: {
                name: 'Single Responsibility Principle',
                category: 'code-quality',
                severity: 'medium',
                patterns: [
                    {
                        regex: /function\s+\w+\([^)]*\)\s*{[^}]{300,}}/g,
                        message: 'Function is too long (>300 chars). Consider breaking it down.',
                        suggestion: 'Break this function into smaller, single-purpose functions'
                    },
                    {
                        regex: /const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*{[^}]{300,}}/g,
                        message: 'Arrow function is too long. Consider refactoring.',
                        suggestion: 'Extract logic into separate functions'
                    },
                    {
                        regex: /(if|else if|switch)[^{]*{[^}]*{[^}]*{[^}]*{/g,
                        message: 'Deeply nested code detected (>3 levels).',
                        suggestion: 'Extract nested logic into separate functions'
                    }
                ],
                autoFix: false,
                snippet: 'srpcheck'
            },

            // Console Log Cleanup
            noconlog: {
                name: 'Console Log Cleanup',
                category: 'production-ready',
                severity: 'low',
                patterns: [
                    {
                        regex: /console\.log\(/g,
                        message: 'console.log() found. Remove before production.',
                        suggestion: 'Use proper logging service or remove debug statements'
                    },
                    {
                        regex: /console\.warn\(/g,
                        message: 'console.warn() found. Consider proper error handling.',
                        suggestion: 'Replace with proper warning system'
                    },
                    {
                        regex: /console\.error\(/g,
                        message: 'console.error() found. Use proper error handling.',
                        suggestion: 'Implement proper error logging and handling'
                    },
                    {
                        regex: /debugger;/g,
                        message: 'debugger statement found. Remove before production.',
                        suggestion: 'Remove debugger statements'
                    }
                ],
                autoFix: true,
                snippet: 'noconlog'
            },

            // React Hooks Best Practices
            hookcheck: {
                name: 'React Hooks Best Practices',
                category: 'react',
                severity: 'medium',
                patterns: [
                    {
                        regex: /class\s+\w+\s+extends\s+(React\.)?Component/g,
                        message: 'Class component found. Consider converting to functional component with hooks.',
                        suggestion: 'Convert to functional component using useState and useEffect'
                    },
                    {
                        regex: /componentDidMount|componentDidUpdate|componentWillUnmount/g,
                        message: 'Lifecycle methods found. Use useEffect hook instead.',
                        suggestion: 'Replace lifecycle methods with useEffect'
                    },
                    {
                        regex: /useEffect\([^,]+,\s*\[\]\)/g,
                        message: 'useEffect with empty dependency array. Ensure this is intentional.',
                        suggestion: 'Verify that empty dependency array is correct'
                    },
                    {
                        regex: /useState\([^)]*\)[^;]*;\s*useState/g,
                        message: 'Multiple useState calls. Consider useReducer for complex state.',
                        suggestion: 'Consider using useReducer for related state variables'
                    }
                ],
                autoFix: false,
                snippet: 'hookcheck'
            },

            // Kenya-First Requirements
            kenyacheck: {
                name: 'Kenya-First Requirements',
                category: 'localization',
                severity: 'medium',
                patterns: [
                    {
                        regex: /\$\d+(\.\d{2})?/g,
                        message: 'USD currency format found. Use Kenya Shilling (KSh) format.',
                        suggestion: 'Replace with KSh format: KSh 1,000.00'
                    },
                    {
                        regex: /\bUSD\b|\bDollar\b/gi,
                        message: 'USD currency reference found. Use KSh or Kenya Shilling.',
                        suggestion: 'Use Kenya Shilling (KSh) instead of USD'
                    },
                    {
                        regex: /\+1\d{10}/g,
                        message: 'US phone format found. Use Kenya format (+254).',
                        suggestion: 'Use Kenya phone format: +254 XXX XXX XXX'
                    },
                    {
                        regex: /(GMT|UTC)(?!\+3)/g,
                        message: 'Non-Kenya timezone found. Use EAT (UTC+3).',
                        suggestion: 'Use East Africa Time (EAT) or UTC+3'
                    },
                    {
                        regex: /\b(color|center|meter|liter)\b/g,
                        message: 'American spelling found. Use British/Kenyan spelling.',
                        suggestion: 'Use British spelling: colour, centre, metre, litre'
                    }
                ],
                autoFix: false,
                snippet: 'kenyacheck'
            },

            // Mobile-First Design
            mobilecheck: {
                name: 'Mobile-First Design',
                category: 'responsive',
                severity: 'medium',
                patterns: [
                    {
                        regex: /width:\s*\d+px/g,
                        message: 'Fixed pixel width found. Use responsive units.',
                        suggestion: 'Use rem, %, vw, or other responsive units'
                    },
                    {
                        regex: /height:\s*\d+px/g,
                        message: 'Fixed pixel height found. Use responsive units.',
                        suggestion: 'Use rem, vh, or other responsive units'
                    },
                    {
                        regex: /font-size:\s*\d+px/g,
                        message: 'Fixed pixel font size. Use rem for scalability.',
                        suggestion: 'Use rem units for font sizes'
                    },
                    {
                        regex: /@media\s*\([^)]*min-width/g,
                        message: 'Desktop-first media query. Consider mobile-first approach.',
                        suggestion: 'Use max-width for mobile-first design'
                    }
                ],
                autoFix: false,
                snippet: 'mobilecheck'
            },

            // Error Handling
            errorcheck: {
                name: 'Error Handling',
                category: 'robustness',
                severity: 'high',
                patterns: [
                    {
                        regex: /async\s+function[^{]*{(?![^}]*try)[^}]*}/g,
                        message: 'Async function without try-catch block.',
                        suggestion: 'Add try-catch block for error handling'
                    },
                    {
                        regex: /fetch\([^)]*\)(?![^;]*catch)/g,
                        message: 'fetch() call without error handling.',
                        suggestion: 'Add .catch() or wrap in try-catch'
                    },
                    {
                        regex: /JSON\.parse\([^)]*\)(?![^;]*catch)/g,
                        message: 'JSON.parse() without error handling.',
                        suggestion: 'Wrap JSON.parse in try-catch block'
                    },
                    {
                        regex: /throw\s+new\s+Error\([^)]*\)/g,
                        message: 'Generic Error thrown. Use specific error types.',
                        suggestion: 'Create specific error classes or use descriptive error messages'
                    }
                ],
                autoFix: false,
                snippet: 'errorcheck'
            },

            // Security Checks
            securitycheck: {
                name: 'Security Checks',
                category: 'security',
                severity: 'critical',
                patterns: [
                    {
                        regex: /innerHTML\s*=/g,
                        message: 'innerHTML usage detected. Potential XSS vulnerability.',
                        suggestion: 'Use textContent or sanitize HTML content'
                    },
                    {
                        regex: /dangerouslySetInnerHTML/g,
                        message: 'dangerouslySetInnerHTML used. Ensure content is sanitized.',
                        suggestion: 'Sanitize HTML content before rendering'
                    },
                    {
                        regex: /eval\(/g,
                        message: 'eval() usage detected. Security risk.',
                        suggestion: 'Avoid eval(). Use JSON.parse() or other safe alternatives'
                    },
                    {
                        regex: /document\.write\(/g,
                        message: 'document.write() usage. Potential security risk.',
                        suggestion: 'Use DOM manipulation methods instead'
                    },
                    {
                        regex: /(password|secret|key|token)\s*[:=]\s*["'][^"']*["']/gi,
                        message: 'Hardcoded credentials detected.',
                        suggestion: 'Move credentials to environment variables'
                    }
                ],
                autoFix: false,
                snippet: 'securitycheck'
            },

            // Performance Checks
            perfcheck: {
                name: 'Performance Checks',
                category: 'performance',
                severity: 'medium',
                patterns: [
                    {
                        regex: /useEffect\(\(\)\s*=>\s*{[^}]*},\s*\[\]\)/g,
                        message: 'useEffect with empty deps. Consider if this should run on every render.',
                        suggestion: 'Verify useEffect dependencies are correct'
                    },
                    {
                        regex: /map\([^)]*\)\s*\.map\(/g,
                        message: 'Chained map operations. Consider combining for performance.',
                        suggestion: 'Combine multiple map operations into one'
                    },
                    {
                        regex: /for\s*\([^)]*\)\s*{[^}]*for\s*\([^)]*\)/g,
                        message: 'Nested loops detected. Consider optimization.',
                        suggestion: 'Optimize nested loops or use more efficient algorithms'
                    },
                    {
                        regex: /new\s+Date\(\)/g,
                        message: 'new Date() in render. Consider memoization.',
                        suggestion: 'Use useMemo or move Date creation outside render'
                    }
                ],
                autoFix: false,
                snippet: 'perfcheck'
            },

            // Accessibility Checks
            a11ycheck: {
                name: 'Accessibility Checks',
                category: 'accessibility',
                severity: 'medium',
                patterns: [
                    {
                        regex: /<img(?![^>]*alt=)/g,
                        message: 'Image without alt attribute.',
                        suggestion: 'Add alt attribute for screen readers'
                    },
                    {
                        regex: /<button(?![^>]*aria-label)(?![^>]*aria-labelledby)/g,
                        message: 'Button without accessible label.',
                        suggestion: 'Add aria-label or aria-labelledby attribute'
                    },
                    {
                        regex: /<input(?![^>]*aria-label)(?![^>]*placeholder)(?![^>]*aria-labelledby)/g,
                        message: 'Input without accessible label.',
                        suggestion: 'Add aria-label, placeholder, or aria-labelledby'
                    },
                    {
                        regex: /<div[^>]*onClick/g,
                        message: 'div with onClick. Use button or add keyboard support.',
                        suggestion: 'Use button element or add onKeyDown handler'
                    },
                    {
                        regex: /color:\s*#[0-9a-f]{3,6}/gi,
                        message: 'Color usage detected. Ensure sufficient contrast.',
                        suggestion: 'Verify color contrast meets WCAG guidelines'
                    }
                ],
                autoFix: false,
                snippet: 'a11ycheck'
            }
        };
    }

    /**
     * Run all guardrail checks on code content
     */
    runChecks(content, filePath = '', options = {}) {
        if (!this.enabled) return [];

        const violations = [];
        const fileExt = this.getFileExtension(filePath);

        for (const [ruleId, rule] of Object.entries(this.rules)) {
            // Skip rule if not applicable to file type
            if (!this.isRuleApplicable(rule, fileExt, content)) {
                continue;
            }

            // Skip rule if severity is below threshold
            if (options.minSeverity && !this.meetsSeverityThreshold(rule.severity, options.minSeverity)) {
                continue;
            }

            const ruleViolations = this.checkRule(rule, content, ruleId);
            violations.push(...ruleViolations);
        }

        return this.prioritizeViolations(violations);
    }

    /**
     * Check a specific rule against content
     */
    checkRule(rule, content, ruleId) {
        const violations = [];

        for (const pattern of rule.patterns) {
            const matches = content.match(pattern.regex);
            if (matches) {
                violations.push({
                    ruleId,
                    ruleName: rule.name,
                    category: rule.category,
                    severity: rule.severity,
                    message: pattern.message,
                    suggestion: pattern.suggestion,
                    snippet: rule.snippet,
                    matches: matches.length,
                    autoFixable: rule.autoFix,
                    pattern: pattern.regex.source
                });
            }
        }

        return violations;
    }

    /**
     * Check if rule is applicable to file type
     */
    isRuleApplicable(rule, fileExt, content) {
        // React-specific rules
        if (rule.category === 'react') {
            return ['jsx', 'tsx'].includes(fileExt) || content.includes('React');
        }

        // CSS-specific rules
        if (rule.category === 'responsive') {
            return ['css', 'scss', 'sass', 'less'].includes(fileExt) || content.includes('style');
        }

        // JavaScript-specific rules
        if (rule.category === 'production-ready' || rule.category === 'performance') {
            return ['js', 'jsx', 'ts', 'tsx'].includes(fileExt);
        }

        // Universal rules
        return true;
    }

    /**
     * Check if severity meets threshold
     */
    meetsSeverityThreshold(severity, threshold) {
        const severityLevels = { low: 1, medium: 2, high: 3, critical: 4 };
        return severityLevels[severity] >= severityLevels[threshold];
    }

    /**
     * Prioritize violations by severity and impact
     */
    prioritizeViolations(violations) {
        const severityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
        
        return violations.sort((a, b) => {
            // Sort by severity first
            const severityDiff = severityOrder[b.severity] - severityOrder[a.severity];
            if (severityDiff !== 0) return severityDiff;
            
            // Then by number of matches (more matches = higher priority)
            return b.matches - a.matches;
        });
    }

    /**
     * Get file extension
     */
    getFileExtension(filePath) {
        return filePath.split('.').pop()?.toLowerCase() || '';
    }

    /**
     * Generate guardrail report
     */
    generateReport(violations, filePath) {
        const report = {
            filePath,
            timestamp: new Date().toISOString(),
            summary: {
                totalViolations: violations.length,
                critical: violations.filter(v => v.severity === 'critical').length,
                high: violations.filter(v => v.severity === 'high').length,
                medium: violations.filter(v => v.severity === 'medium').length,
                low: violations.filter(v => v.severity === 'low').length
            },
            violations: violations.map(v => ({
                ...v,
                id: this.generateViolationId(v)
            })),
            recommendations: this.generateRecommendations(violations)
        };

        return report;
    }

    /**
     * Generate recommendations based on violations
     */
    generateRecommendations(violations) {
        const recommendations = [];
        const snippetCounts = {};

        // Count snippet suggestions
        violations.forEach(v => {
            snippetCounts[v.snippet] = (snippetCounts[v.snippet] || 0) + 1;
        });

        // Generate recommendations based on most common issues
        for (const [snippet, count] of Object.entries(snippetCounts)) {
            if (count >= 3) {
                recommendations.push({
                    priority: 'high',
                    snippet,
                    message: `Multiple ${snippet} issues detected (${count}). Consider running comprehensive ${snippet} review.`,
                    action: `Use snippet: ${snippet}`
                });
            }
        }

        return recommendations;
    }

    /**
     * Generate unique violation ID
     */
    generateViolationId(violation) {
        const hash = require('crypto')
            .createHash('md5')
            .update(`${violation.ruleId}-${violation.pattern}-${violation.message}`)
            .digest('hex')
            .substring(0, 8);
        return `${violation.ruleId}-${hash}`;
    }

    /**
     * Auto-fix violations where possible
     */
    autoFix(content, violations) {
        let fixedContent = content;
        const appliedFixes = [];

        for (const violation of violations) {
            if (violation.autoFixable) {
                const rule = this.rules[violation.ruleId];
                const pattern = rule.patterns.find(p => p.regex.source === violation.pattern);
                
                if (pattern && pattern.autoFix) {
                    fixedContent = pattern.autoFix(fixedContent);
                    appliedFixes.push(violation);
                }
            }
        }

        return {
            content: fixedContent,
            appliedFixes
        };
    }

    /**
     * Enable/disable specific rules
     */
    configureRules(ruleConfig) {
        for (const [ruleId, config] of Object.entries(ruleConfig)) {
            if (this.rules[ruleId]) {
                this.rules[ruleId] = { ...this.rules[ruleId], ...config };
            }
        }
    }

    /**
     * Add custom rule
     */
    addCustomRule(ruleId, rule) {
        this.rules[ruleId] = rule;
    }
}

module.exports = GuardrailsEngine;
