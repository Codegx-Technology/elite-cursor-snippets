/**
 * Elite Automation Core Engine
 * 
 * Automatically enhances AI chat prompts with intelligent context
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 2.0.0
 */

class EliteAutomationCore {
    constructor() {
        this.patterns = this.initializePromptPatterns();
        this.isEnabled = true;
        this.debugMode = false;
    }

    /**
     * Initialize prompt patterns for automatic detection
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
                template: `🔧 SURGICAL FIX MODE
Issue: {original_prompt}
Expected: [What should happen?]
Actual: [What's happening instead?]

Please provide a precise, surgical fix:`,
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
                    /lag|laggy|sluggish/i,
                    /loading.*?(slow|long)/i,
                    /page.*?load/i
                ],
                template: `⚡ PERFORMANCE OPTIMIZATION
Issue: {original_prompt}
Goal: Optimize for performance
Focus: Check for inefficient loops, unnecessary re-renders, memory leaks

Please analyze and optimize:`,
                priority: 80,
                description: 'Performance optimization'
            },

            // React component issues
            'react-component': {
                patterns: [
                    /react\s+component/i,
                    /component.*?(issue|problem|fix|slow)/i,
                    /hook.*?(issue|problem)/i,
                    /render.*?(issue|problem)/i,
                    /state.*?(issue|problem)/i
                ],
                template: `⚛️ REACT OPTIMIZATION
Component: {original_prompt}
Goal: Optimize React component with hooks and best practices
Focus: Reduce re-renders, improve performance, fix hooks issues

Please optimize this React component:`,
                priority: 85,
                description: 'React component optimization'
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
                template: `🧪 TEST GENERATION
Target: {original_prompt}
Framework: Jest/Mocha (auto-detect)
Coverage: Unit tests, edge cases, integration

Please generate comprehensive tests:`,
                priority: 75,
                description: 'Unit test generation'
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
                template: `🔄 CODE REFACTORING
Target: {original_prompt}
Goal: Clean, maintainable, readable code
Constraints: Keep existing API, avoid breaking changes

Please refactor with clear intent:`,
                priority: 70,
                description: 'Code refactoring and cleanup'
            },

            // Kenya-specific requests
            'kenya-first': {
                patterns: [
                    /kenya|kenyan|ksh|shilling/i,
                    /\+254|254/i,
                    /nairobi|mombasa|kisumu/i,
                    /m-?pesa|mpesa/i,
                    /currency.*?format/i,
                    /phone.*?format/i
                ],
                template: `🇰🇪 KENYA-FIRST OPTIMIZATION
Feature: {original_prompt}
Requirements: Kenya-specific formatting (KSh, +254, EAT timezone)
Context: Professional Kenyan English, local best practices

Please adapt for Kenya-first principles:`,
                priority: 85,
                description: 'Kenya-first localization'
            },

            // Security checks
            'security': {
                patterns: [
                    /security|secure|vulnerability/i,
                    /xss|injection|csrf/i,
                    /auth|authentication|authorization/i,
                    /hack|exploit|attack/i
                ],
                template: `🛡️ SECURITY ANALYSIS
Target: {original_prompt}
Focus: XSS, SQL injection, CSRF, authentication issues
Standards: OWASP best practices

Please analyze and secure:`,
                priority: 95,
                description: 'Security vulnerability analysis'
            },

            // Accessibility
            'accessibility': {
                patterns: [
                    /accessibility|a11y|accessible/i,
                    /screen.*?reader/i,
                    /keyboard.*?navigation/i,
                    /aria|wcag/i
                ],
                template: `♿ ACCESSIBILITY OPTIMIZATION
Target: {original_prompt}
Standards: WCAG 2.1 AA compliance
Focus: Screen readers, keyboard navigation, ARIA labels

Please make accessible:`,
                priority: 80,
                description: 'Accessibility compliance'
            }
        };
    }

    /**
     * Analyze prompt and return enhancement
     */
    analyzePrompt(prompt) {
        if (!prompt || prompt.trim().length < 3) {
            return null;
        }

        const matches = [];
        
        // Check each pattern category
        for (const [category, config] of Object.entries(this.patterns)) {
            for (const pattern of config.patterns) {
                if (pattern.test(prompt)) {
                    matches.push({
                        category,
                        config,
                        confidence: this.calculateConfidence(prompt, pattern)
                    });
                    break; // Only one match per category
                }
            }
        }

        if (matches.length === 0) {
            return null;
        }

        // Sort by priority and confidence
        matches.sort((a, b) => {
            const priorityDiff = b.config.priority - a.config.priority;
            if (priorityDiff !== 0) return priorityDiff;
            return b.confidence - a.confidence;
        });

        const bestMatch = matches[0];
        
        return {
            category: bestMatch.category,
            confidence: bestMatch.confidence,
            enhancedPrompt: bestMatch.config.template.replace('{original_prompt}', prompt),
            description: bestMatch.config.description,
            alternatives: matches.slice(1, 3).map(m => m.category)
        };
    }

    /**
     * Calculate confidence score for pattern match
     */
    calculateConfidence(prompt, pattern) {
        const match = prompt.match(pattern);
        if (!match) return 0;
        
        // Base confidence
        let confidence = 70;
        
        // Boost for exact keyword matches
        const keywords = ['fix', 'optimize', 'debug', 'test', 'refactor', 'performance'];
        for (const keyword of keywords) {
            if (prompt.toLowerCase().includes(keyword)) {
                confidence += 10;
            }
        }
        
        // Boost for specificity
        if (prompt.length > 20) confidence += 5;
        if (prompt.includes('component')) confidence += 5;
        if (prompt.includes('React')) confidence += 10;
        
        return Math.min(confidence, 100);
    }

    /**
     * Check if prompt should be enhanced
     */
    shouldEnhance(prompt) {
        // Skip if already enhanced
        if (prompt.includes('🔧') || prompt.includes('⚡') || prompt.includes('🇰🇪')) {
            return false;
        }
        
        // Skip very short prompts
        if (prompt.trim().length < 5) {
            return false;
        }
        
        return true;
    }

    /**
     * Main enhancement function
     */
    enhancePrompt(originalPrompt) {
        if (!this.isEnabled || !this.shouldEnhance(originalPrompt)) {
            return originalPrompt;
        }

        const analysis = this.analyzePrompt(originalPrompt);
        
        if (!analysis) {
            return originalPrompt;
        }

        if (this.debugMode) {
            console.log('🤖 Elite Automation Enhanced:', analysis);
        }

        return analysis.enhancedPrompt;
    }
}

// Export for use in content script
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EliteAutomationCore;
} else {
    window.EliteAutomationCore = EliteAutomationCore;
}
