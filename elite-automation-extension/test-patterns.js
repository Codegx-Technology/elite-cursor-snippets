/**
 * Test Elite Automation Patterns
 */

// Mock window object for Node.js testing
global.window = {};

// Load the core
require('./elite-automation-core.js');

const core = new window.EliteAutomationCore();

// Test patterns
const testPrompts = [
    'fix sticky page loading issue on sidenav',
    'fix slow ui loading',
    'optimize React component performance',
    'write tests for authentication function',
    'convert USD to Kenya Shilling format',
    'security vulnerability in login system'
];

console.log('🤖 Testing Elite Automation Patterns:\n');

testPrompts.forEach(prompt => {
    const enhancement = core.analyzePrompt(prompt);
    
    if (enhancement) {
        console.log(`✅ "${prompt}"`);
        console.log(`   → ${enhancement.snippet} (${(enhancement.confidence * 100).toFixed(0)}% confidence)`);
        console.log(`   → ${enhancement.description}\n`);
    } else {
        console.log(`❌ "${prompt}" → No enhancement found\n`);
    }
});

console.log('🎯 Pattern recognition test complete!');
