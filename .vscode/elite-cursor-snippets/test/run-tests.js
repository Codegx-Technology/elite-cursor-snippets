#!/usr/bin/env node

/**
 * Test Runner for Elite Auto-Fix System
 * 
 * Tests the automation system with sample code to verify it works correctly
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');
const EliteAutoFix = require('../elite-auto-fix');
const SmartSnippetSelector = require('../smart-selector');
const GuardrailsEngine = require('../guardrails-engine');

class TestRunner {
    constructor() {
        this.autoFix = new EliteAutoFix();
        this.selector = new SmartSnippetSelector();
        this.guardrails = new GuardrailsEngine();
        this.testResults = [];
    }

    /**
     * Run all tests
     */
    async runAllTests() {
        console.log('🧪 Elite Auto-Fix Test Suite');
        console.log('=' .repeat(40));

        try {
            await this.testBasicAnalysis();
            await this.testGuardrailsEngine();
            await this.testSmartSelector();
            await this.testKenyaFirstValidation();
            await this.testReactOptimization();
            await this.testSecurityChecks();
            
            this.displayResults();
        } catch (error) {
            console.error('❌ Test suite failed:', error.message);
            process.exit(1);
        }
    }

    /**
     * Test basic code analysis
     */
    async testBasicAnalysis() {
        console.log('\n🔍 Testing Basic Code Analysis...');
        
        const sampleCodePath = path.join(__dirname, 'sample-code.js');
        const content = fs.readFileSync(sampleCodePath, 'utf8');
        
        const issues = this.autoFix.analyzeCode(content, sampleCodePath);
        const suggestions = this.autoFix.generateFixSuggestions(issues);

        this.assert(issues.length > 0, 'Should detect issues in sample code');
        this.assert(suggestions.length > 0, 'Should generate suggestions');
        
        console.log(`✅ Detected ${issues.length} issues`);
        console.log(`✅ Generated ${suggestions.length} suggestions`);
        
        // Test specific issue types
        const hasConsoleLog = issues.some(issue => issue.guard === 'noconlog');
        const hasLongFunction = issues.some(issue => issue.guard === 'srpcheck');
        const hasKenyaIssue = issues.some(issue => issue.guard === 'kenyacheck');
        
        this.assert(hasConsoleLog, 'Should detect console.log issues');
        this.assert(hasLongFunction, 'Should detect long function issues');
        this.assert(hasKenyaIssue, 'Should detect Kenya-specific issues');
        
        this.recordTest('Basic Analysis', true, `${issues.length} issues detected`);
    }

    /**
     * Test guardrails engine
     */
    async testGuardrailsEngine() {
        console.log('\n🛡️ Testing Guardrails Engine...');
        
        const testCode = `
            console.log('debug');
            function longFunction() {
                // This is a very long function that does many things
                // and violates the single responsibility principle
                // by having too much code in one place
                const data = fetchData();
                const processed = processData(data);
                const validated = validateData(processed);
                const formatted = formatData(validated);
                const saved = saveData(formatted);
                return saved;
            }
            const price = '$25.99';
        `;
        
        const violations = this.guardrails.runChecks(testCode, 'test.js');
        
        this.assert(violations.length > 0, 'Should detect guardrail violations');
        
        const hasNoConLog = violations.some(v => v.ruleId === 'noconlog');
        const hasKenyaCheck = violations.some(v => v.ruleId === 'kenyacheck');
        
        this.assert(hasNoConLog, 'Should detect console.log violations');
        this.assert(hasKenyaCheck, 'Should detect Kenya-specific violations');
        
        console.log(`✅ Detected ${violations.length} guardrail violations`);
        this.recordTest('Guardrails Engine', true, `${violations.length} violations detected`);
    }

    /**
     * Test smart snippet selector
     */
    async testSmartSelector() {
        console.log('\n🧠 Testing Smart Snippet Selector...');
        
        const contexts = [
            {
                description: 'React component with performance issues',
                filePath: 'Component.jsx',
                expectedSnippet: 'autocomp'
            },
            {
                description: 'Bug in JavaScript function',
                filePath: 'utils.js',
                expectedSnippet: 'surgicalfix'
            },
            {
                description: 'Need to refactor messy code',
                filePath: 'legacy.js',
                expectedSnippet: 'refactorintent'
            },
            {
                description: 'Missing unit tests',
                filePath: 'service.js',
                expectedSnippet: 'writetest'
            }
        ];

        let correctSelections = 0;
        
        for (const context of contexts) {
            const result = this.selector.selectBestSnippet(context);
            
            if (result.primary.id === context.expectedSnippet) {
                correctSelections++;
                console.log(`✅ Correctly selected ${result.primary.id} for: ${context.description}`);
            } else {
                console.log(`⚠️ Selected ${result.primary.id}, expected ${context.expectedSnippet} for: ${context.description}`);
            }
        }

        const accuracy = correctSelections / contexts.length;
        this.assert(accuracy >= 0.5, 'Should have at least 50% accuracy in snippet selection');
        
        console.log(`✅ Snippet selection accuracy: ${(accuracy * 100).toFixed(1)}%`);
        this.recordTest('Smart Selector', true, `${(accuracy * 100).toFixed(1)}% accuracy`);
    }

    /**
     * Test Kenya-first validation
     */
    async testKenyaFirstValidation() {
        console.log('\n🇰🇪 Testing Kenya-First Validation...');
        
        const kenyaTestCode = `
            const price = '$25.99';
            const phone = '+1234567890';
            const timezone = 'GMT';
            const color = 'blue';
        `;
        
        const violations = this.guardrails.runChecks(kenyaTestCode, 'kenya-test.js');
        const kenyaViolations = violations.filter(v => v.ruleId === 'kenyacheck');
        
        this.assert(kenyaViolations.length >= 3, 'Should detect multiple Kenya-specific issues');
        
        const hasCurrencyIssue = kenyaViolations.some(v => v.message.includes('currency'));
        const hasPhoneIssue = kenyaViolations.some(v => v.message.includes('phone'));
        const hasSpellingIssue = kenyaViolations.some(v => v.message.includes('spelling'));
        
        this.assert(hasCurrencyIssue, 'Should detect currency format issues');
        this.assert(hasPhoneIssue, 'Should detect phone format issues');
        
        console.log(`✅ Detected ${kenyaViolations.length} Kenya-specific issues`);
        this.recordTest('Kenya-First Validation', true, `${kenyaViolations.length} issues detected`);
    }

    /**
     * Test React optimization detection
     */
    async testReactOptimization() {
        console.log('\n⚛️ Testing React Optimization...');
        
        const reactTestCode = `
            class MyComponent extends React.Component {
                componentDidMount() {
                    this.fetchData();
                }
                render() {
                    return <div>Hello</div>;
                }
            }
            
            const ListComponent = ({ items }) => {
                return (
                    <ul>
                        {items.map(item => <li>{item.name}</li>)}
                    </ul>
                );
            };
        `;
        
        const violations = this.guardrails.runChecks(reactTestCode, 'Component.jsx');
        const reactViolations = violations.filter(v => v.ruleId === 'hookcheck');
        
        this.assert(reactViolations.length > 0, 'Should detect React optimization opportunities');
        
        const hasClassComponent = reactViolations.some(v => v.message.includes('Class component'));
        this.assert(hasClassComponent, 'Should detect class components');
        
        console.log(`✅ Detected ${reactViolations.length} React optimization opportunities`);
        this.recordTest('React Optimization', true, `${reactViolations.length} opportunities detected`);
    }

    /**
     * Test security checks
     */
    async testSecurityChecks() {
        console.log('\n🔒 Testing Security Checks...');
        
        const securityTestCode = `
            function displayMessage(msg) {
                document.getElementById('output').innerHTML = msg;
            }
            
            function executeCode(code) {
                return eval(code);
            }
            
            const config = {
                apiKey: 'sk-1234567890',
                password: 'secret123'
            };
        `;
        
        const violations = this.guardrails.runChecks(securityTestCode, 'security-test.js');
        const securityViolations = violations.filter(v => v.ruleId === 'securitycheck');
        
        this.assert(securityViolations.length >= 2, 'Should detect multiple security issues');
        
        const hasInnerHTML = securityViolations.some(v => v.message.includes('innerHTML'));
        const hasEval = securityViolations.some(v => v.message.includes('eval'));
        const hasCredentials = securityViolations.some(v => v.message.includes('credentials'));
        
        this.assert(hasInnerHTML, 'Should detect innerHTML security issues');
        this.assert(hasEval, 'Should detect eval security issues');
        this.assert(hasCredentials, 'Should detect hardcoded credentials');
        
        console.log(`✅ Detected ${securityViolations.length} security issues`);
        this.recordTest('Security Checks', true, `${securityViolations.length} issues detected`);
    }

    /**
     * Assert helper
     */
    assert(condition, message) {
        if (!condition) {
            throw new Error(`Assertion failed: ${message}`);
        }
    }

    /**
     * Record test result
     */
    recordTest(testName, passed, details) {
        this.testResults.push({
            name: testName,
            passed,
            details,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Display test results
     */
    displayResults() {
        console.log('\n📊 Test Results Summary');
        console.log('=' .repeat(40));
        
        const passedTests = this.testResults.filter(t => t.passed).length;
        const totalTests = this.testResults.length;
        
        this.testResults.forEach(test => {
            const status = test.passed ? '✅' : '❌';
            console.log(`${status} ${test.name}: ${test.details}`);
        });
        
        console.log('\n' + '=' .repeat(40));
        console.log(`🎯 Tests Passed: ${passedTests}/${totalTests}`);
        console.log(`📈 Success Rate: ${((passedTests / totalTests) * 100).toFixed(1)}%`);
        
        if (passedTests === totalTests) {
            console.log('\n🚀 All tests passed! Elite Auto-Fix is working correctly.');
        } else {
            console.log('\n⚠️ Some tests failed. Please check the implementation.');
            process.exit(1);
        }
    }
}

// Run tests if called directly
if (require.main === module) {
    const runner = new TestRunner();
    runner.runAllTests().catch(error => {
        console.error('❌ Test runner failed:', error);
        process.exit(1);
    });
}

module.exports = TestRunner;
