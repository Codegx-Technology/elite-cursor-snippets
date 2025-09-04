# Elite Cursor Snippets Automation System

🧠 **Intelligent automation for Kenya-First engineering excellence**

An AI-powered automation system that analyzes your code, detects issues, and automatically suggests the right Elite Cursor Snippet to fix them. Built with Kenya-First principles and designed for elite engineering teams.

## 🚀 Features

### 🔍 Smart Issue Detection
- **Code Quality Analysis**: Detects long functions, complex logic, poor naming
- **React Optimization**: Identifies class components, missing hooks, performance issues
- **Security Scanning**: Finds XSS vulnerabilities, hardcoded secrets, unsafe practices
- **Kenya-First Validation**: Ensures KSh currency, +254 phone format, EAT timezone
- **Accessibility Checks**: Validates ARIA labels, alt text, keyboard navigation
- **Performance Monitoring**: Identifies bundle size issues, memory leaks, slow renders

### 🎯 Intelligent Snippet Selection
- **Context-Aware**: Analyzes file type, code content, and detected issues
- **Priority-Based**: Ranks suggestions by severity and impact
- **Learning Engine**: Adapts to your patterns and preferences over time
- **Confidence Scoring**: Provides confidence levels for each suggestion

### 🛡️ Automated Guardrails
- **srpcheck**: Single Responsibility Principle validation
- **noconlog**: Console.log cleanup for production
- **hookcheck**: React hooks best practices
- **kenyacheck**: Kenya-specific requirements validation
- **mobilecheck**: Mobile-first design principles
- **errorcheck**: Error handling validation
- **securitycheck**: Security vulnerability detection
- **perfcheck**: Performance optimization
- **a11ycheck**: Accessibility standards

### 🔧 Git Integration
- **Pre-commit**: Blocks commits with critical issues
- **Post-commit**: Suggests improvements after commits
- **Pre-push**: Full project analysis before push
- **Commit-msg**: Validates commit message format

## 📦 Installation

### Quick Setup
```bash
# Navigate to your elite-cursor-snippets directory
cd .vscode/elite-cursor-snippets

# Install dependencies
npm install

# Setup git hooks and integrations
npm run setup
```

### Manual Installation
```bash
# Install git hooks
node scripts/install-git-hooks.js

# Make CLI globally available
npm link
```

## 🎮 Usage

### Command Line Interface

```bash
# Analyze a specific file
elite analyze src/components/Header.jsx

# Fix issues in a file
elite fix src/utils/api.js

# Scan entire project
elite scan

# Get contextual suggestions
elite suggest "React component with performance issues"

# Show configuration
elite config show

# Install git hooks
elite install hooks
```

### Programmatic Usage

```javascript
const EliteAutoFix = require('./elite-auto-fix');

const autoFix = new EliteAutoFix();
const content = fs.readFileSync('MyComponent.jsx', 'utf8');
const issues = autoFix.analyzeCode(content, 'MyComponent.jsx');
const suggestions = autoFix.generateFixSuggestions(issues);

console.log('Recommended snippet:', suggestions[0].snippet);
```

### VSCode/Cursor Integration

The system automatically integrates with your editor:

1. **Auto-detection**: Analyzes files as you work
2. **Smart suggestions**: Shows relevant snippets in problems panel
3. **Quick fixes**: One-click application of suggested snippets
4. **Context awareness**: Adapts to your current file and project

## 🎯 Snippet Mapping

### Core AI Prompts
- **thinkwithai**: Strategic reasoning and complex analysis
- **surgicalfix**: Precision bug fixes and logic corrections
- **refactorintent**: Intentional refactoring for better code quality
- **refactorclean**: Clean refactoring following best practices
- **autocomp**: Auto-optimize React components
- **writetest**: Generate comprehensive unit tests
- **doccode**: Kenya-first documentation generation
- **unstuck**: Get unstuck when facing complex problems
- **augmentsearch**: Semantic search across codebase
- **kenyafirst**: Apply Kenya-first principles and localization
- **mindreset**: Reset context and refocus
- **guardon**: Activate quality guardrails and standards

### Guardrail Snippets
- **srpcheck**: Single Responsibility Principle validation
- **noconlog**: Remove console.log statements
- **hookcheck**: React hooks best practices
- **kenyacheck**: Kenya-specific requirements validation
- **mobilecheck**: Mobile-first design principles
- **errorcheck**: Error handling validation
- **securitycheck**: Security vulnerability detection
- **perfcheck**: Performance optimization
- **a11ycheck**: Accessibility standards validation

## ⚙️ Configuration

### Basic Configuration (`elite-auto-fix.config.json`)

```json
{
  "autoApply": false,
  "verboseOutput": true,
  "enableGuardrails": true,
  "excludePatterns": ["node_modules", ".git", "dist"],
  "fileExtensions": [".js", ".jsx", ".ts", ".tsx"],
  "severityThresholds": {
    "critical": { "autoSuggest": true, "blockCommit": true },
    "high": { "autoSuggest": true, "blockCommit": false }
  }
}
```

### Kenya-First Settings

```json
{
  "kenyaSpecific": {
    "currency": { "preferred": "KSh", "avoid": ["$", "USD"] },
    "phoneFormat": { "preferred": "+254", "avoid": ["+1"] },
    "timezone": { "preferred": "EAT", "avoid": ["UTC", "GMT"] }
  }
}
```

### Custom Rules

```javascript
// custom-rules.js
module.exports = {
  'custom-rule-id': {
    name: 'Custom Rule',
    category: 'custom',
    severity: 'medium',
    patterns: [
      {
        regex: /your-pattern/g,
        message: 'Your custom message',
        suggestion: 'Your suggestion'
      }
    ],
    snippet: 'your-snippet'
  }
};
```

## 🔄 Workflow Integration

### Development Workflow
1. **Write code** in VSCode/Cursor
2. **Auto-analysis** runs in background
3. **Smart suggestions** appear in problems panel
4. **Apply snippets** with one click or keyboard shortcut
5. **Git hooks** validate before commit/push

### Team Workflow
1. **Shared configuration** across team members
2. **Consistent standards** enforced by guardrails
3. **Learning patterns** shared across projects
4. **Quality metrics** tracked over time

## 📊 Analytics & Reporting

### Issue Reports
```bash
# Generate detailed report
elite scan --format=json > analysis-report.json

# View summary
elite scan --summary
```

### Learning Insights
```bash
# View learning patterns
elite config show --learning

# Export usage statistics
elite export --stats
```

## 🇰🇪 Kenya-First Principles

This system is built with Kenya-First engineering principles:

- **Currency**: Enforces KSh format over USD
- **Phone Numbers**: Validates +254 format
- **Timezone**: Uses EAT (UTC+3) by default
- **Language**: Professional Kenyan English tone
- **Business Logic**: Supports local practices (M-Pesa, NHIF, KRA)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with `npm test`
5. Submit a pull request

### Adding New Rules
```javascript
// Add to guardrails-engine.js
const newRule = {
  name: 'Your Rule Name',
  category: 'your-category',
  severity: 'medium',
  patterns: [/* your patterns */],
  snippet: 'your-snippet'
};
```

### Adding New Snippets
1. Add snippet to appropriate `.code-snippets` file
2. Update `smart-selector.js` mapping
3. Add to documentation

## 📚 Examples

### Example 1: React Component Analysis
```bash
$ elite analyze src/components/UserProfile.jsx

🔍 Analysis Results for: UserProfile.jsx
========================================

Found 3 issue(s):
  1. ⚠️ Class component found. Consider converting to functional component
  2. ⚡ Missing key prop in mapped components
  3. 🇰🇪 USD currency format found. Use Kenya Shilling (KSh) format

🎯 Recommended Actions:
  1. Use snippet: autocomp
     Auto-optimize React components for performance
     Priority: 80

🚀 Quick Fix:
VSCode/Cursor: Type "autocomp" and press Tab
CLI: elite fix "src/components/UserProfile.jsx" autocomp
```

### Example 2: Security Issue Detection
```bash
$ elite analyze src/utils/api.js

🔍 Analysis Results for: api.js
===============================

Found 2 issue(s):
  1. 🚨 innerHTML usage detected. Potential XSS vulnerability
  2. ⚠️ Async function missing error handling

🎯 Recommended Actions:
  1. Use snippet: securitycheck
     Address security vulnerabilities
     Priority: 95

🚀 Quick Fix:
VSCode/Cursor: Type "securitycheck" and press Tab
```

## 🔗 Links

- [Elite Cursor Snippets Repository](https://github.com/your-org/elite-cursor-snippets)
- [Kenya-First Engineering Guide](./docs/kenya-first-guide.md)
- [Contributing Guidelines](./CONTRIBUTING.md)
- [Changelog](./CHANGELOG.md)

## 📄 License

MIT License - Built with 🇰🇪 Kenya-First principles

---

**🚀 Ship clean, ship fast, ship Kenya-first!**
