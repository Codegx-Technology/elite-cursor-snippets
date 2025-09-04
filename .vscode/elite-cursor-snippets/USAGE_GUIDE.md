# Elite Cursor Snippets Automation - Usage Guide

🚀 **Complete guide to using the Elite Auto-Fix automation system**

## 🎯 Quick Start

### 1. Basic Analysis
```bash
# Analyze a single file
node elite-auto-fix.js src/components/Header.jsx

# Or use the CLI
node elite-cli.js analyze src/components/Header.jsx
```

### 2. Get Smart Suggestions
```bash
# Get contextual suggestions
node elite-cli.js suggest "React component with performance issues"
node elite-cli.js suggest "Bug in async function"
node elite-cli.js suggest "Need to refactor messy code"
```

### 3. Apply Fixes
```bash
# Apply suggested fix
node elite-cli.js fix src/components/Header.jsx autocomp

# Auto-detect best fix
node elite-cli.js fix src/components/Header.jsx
```

## 🔍 Understanding the Output

### Analysis Results Format
```
🧠 Elite Auto-Fix Analysis for: Header.jsx
============================================================

🔍 Found 5 issue(s):
  1. 🚨 innerHTML usage detected. Potential XSS vulnerability
  2. ⚠️ Class component found. Consider converting to functional component
  3. ⚡ Missing key prop in mapped components
  4. 🇰🇪 USD currency format found. Use Kenya Shilling (KSh) format
  5. ℹ️ console.log() found. Remove before production

🎯 Recommended Actions:
  1. Use snippet: securitycheck
     Address security vulnerabilities
     Priority: 200

🚀 Quick Fix:
VSCode/Cursor: Type "securitycheck" and press Tab
CLI: elite fix "Header.jsx" securitycheck
```

### Severity Levels
- 🚨 **Critical**: Security vulnerabilities, blocking issues
- ⚠️ **High**: Important bugs, error handling issues
- ⚡ **Medium**: Performance, accessibility, code quality
- ℹ️ **Low**: Style issues, console logs, minor improvements

## 🎮 Command Reference

### Analysis Commands
```bash
# Analyze single file
elite analyze <file-path>

# Analyze all files in project
elite analyze --all

# Analyze with specific severity filter
elite analyze <file-path> --severity=high

# Generate JSON report
elite analyze <file-path> --format=json
```

### Fix Commands
```bash
# Apply specific snippet
elite fix <file-path> <snippet-name>

# Auto-detect and apply best fix
elite fix <file-path>

# Preview fixes without applying
elite fix <file-path> --preview

# Apply multiple fixes
elite fix <file-path> --all
```

### Suggestion Commands
```bash
# Get contextual suggestions
elite suggest "<description>"

# Get suggestions for specific file type
elite suggest "React component issues" --type=jsx

# Get suggestions with confidence scores
elite suggest "<description>" --verbose
```

### Configuration Commands
```bash
# Show current configuration
elite config show

# Edit configuration file
elite config edit

# Reset to default configuration
elite config reset

# Show specific config section
elite config show --section=kenyaSpecific
```

### Installation Commands
```bash
# Install git hooks
elite install hooks

# Install VSCode integration
elite install vscode

# Install everything
elite install all

# Uninstall git hooks
elite install hooks --uninstall
```

## 🧠 Smart Snippet Selection

The system automatically selects the best snippet based on:

### Context Analysis
- **File type**: `.jsx` → React-specific snippets
- **Content patterns**: `async function` → error handling
- **Issue severity**: Critical security → `securitycheck`
- **Keywords**: "performance" → `perfcheck` or `autocomp`

### Selection Examples
```bash
# Context: "React component with performance issues"
# → Suggests: autocomp, perfcheck

# Context: "Bug in JavaScript function"
# → Suggests: surgicalfix, errorcheck

# Context: "Need to refactor messy code"
# → Suggests: refactorintent, refactorclean

# Context: "Missing unit tests"
# → Suggests: writetest

# Context: "Security vulnerability found"
# → Suggests: securitycheck
```

## 🛡️ Guardrails Reference

### Code Quality Guardrails
- **srpcheck**: Single Responsibility Principle
  - Detects: Long functions (>300 chars), deep nesting (>3 levels)
  - Suggests: Break into smaller functions

- **noconlog**: Console cleanup
  - Detects: `console.log()`, `console.warn()`, `debugger`
  - Suggests: Remove debug statements

### React Guardrails
- **hookcheck**: React hooks best practices
  - Detects: Class components, lifecycle methods
  - Suggests: Convert to functional components with hooks

- **autocomp**: React optimization
  - Detects: Performance issues, missing keys
  - Suggests: Optimize components

### Kenya-First Guardrails
- **kenyacheck**: Kenya-specific validation
  - Detects: USD currency, US phone format, wrong timezone
  - Suggests: Use KSh, +254, EAT timezone

### Security Guardrails
- **securitycheck**: Security validation
  - Detects: XSS vulnerabilities, hardcoded secrets
  - Suggests: Sanitize inputs, use environment variables

- **errorcheck**: Error handling
  - Detects: Missing try-catch, unhandled promises
  - Suggests: Add proper error handling

### Performance Guardrails
- **perfcheck**: Performance optimization
  - Detects: Inefficient loops, memory leaks
  - Suggests: Optimize algorithms, use memoization

### Accessibility Guardrails
- **a11ycheck**: Accessibility validation
  - Detects: Missing alt text, aria labels
  - Suggests: Add accessibility attributes

### Mobile Guardrails
- **mobilecheck**: Mobile-first validation
  - Detects: Fixed pixel units, desktop-first media queries
  - Suggests: Use responsive units, mobile-first approach

## 🔧 Configuration Examples

### Basic Configuration
```json
{
  "autoApply": false,
  "verboseOutput": true,
  "enableGuardrails": true,
  "excludePatterns": ["node_modules", ".git", "dist"],
  "fileExtensions": [".js", ".jsx", ".ts", ".tsx"]
}
```

### Kenya-First Configuration
```json
{
  "kenyaSpecific": {
    "currency": {
      "preferred": "KSh",
      "alternatives": ["Ksh", "KES"],
      "avoid": ["$", "USD", "€"]
    },
    "phoneFormat": {
      "preferred": "+254",
      "alternatives": ["254", "0"],
      "avoid": ["+1", "+44"]
    },
    "timezone": {
      "preferred": "EAT",
      "alternatives": ["Africa/Nairobi", "UTC+3"],
      "avoid": ["UTC", "GMT", "PST"]
    }
  }
}
```

### Severity Thresholds
```json
{
  "severityThresholds": {
    "critical": {
      "autoSuggest": true,
      "requireConfirmation": true,
      "blockCommit": true
    },
    "high": {
      "autoSuggest": true,
      "requireConfirmation": true,
      "blockCommit": false
    },
    "medium": {
      "autoSuggest": true,
      "requireConfirmation": false,
      "blockCommit": false
    }
  }
}
```

## 🔄 Git Hooks Integration

### Pre-commit Hook
- **Triggers**: Before each commit
- **Action**: Analyzes staged files
- **Behavior**: Blocks commit if critical issues found

### Post-commit Hook
- **Triggers**: After successful commit
- **Action**: Generates improvement suggestions
- **Behavior**: Shows optimization opportunities

### Pre-push Hook
- **Triggers**: Before pushing to remote
- **Action**: Full project analysis
- **Behavior**: Blocks push if critical issues found

### Commit Message Hook
- **Triggers**: When writing commit message
- **Action**: Validates message format
- **Behavior**: Suggests conventional commit format

## 🎯 Best Practices

### Daily Workflow
1. **Start with analysis**: `elite analyze --all`
2. **Fix critical issues**: Focus on 🚨 and ⚠️ first
3. **Apply suggestions**: Use recommended snippets
4. **Commit with confidence**: Git hooks ensure quality
5. **Review suggestions**: Check post-commit recommendations

### Team Workflow
1. **Shared configuration**: Commit config files to repo
2. **Consistent standards**: Use same guardrails across team
3. **Regular reviews**: Weekly `elite scan` reports
4. **Learning patterns**: Share successful snippet usage

### Project Setup
1. **Install hooks**: `elite install hooks`
2. **Configure rules**: Customize for your project
3. **Train team**: Share this usage guide
4. **Monitor quality**: Track improvement over time

## 🚨 Troubleshooting

### Common Issues
```bash
# Hook not executing
chmod +x .git/hooks/pre-commit

# Node.js not found in hooks
which node  # Add path to hook scripts

# Configuration not loading
elite config show  # Verify config file exists

# False positives
elite config edit  # Adjust rule sensitivity
```

### Debug Mode
```bash
# Verbose output
elite analyze <file> --verbose

# Debug specific rule
elite analyze <file> --rule=securitycheck

# Test configuration
elite config validate
```

## 📊 Reporting

### Generate Reports
```bash
# JSON report
elite scan --format=json > report.json

# Markdown report
elite scan --format=markdown > QUALITY_REPORT.md

# Summary only
elite scan --summary
```

### Track Progress
```bash
# Before/after comparison
elite scan --baseline=baseline.json

# Trend analysis
elite scan --trend --days=30

# Team metrics
elite scan --team-report
```

---

🇰🇪 **Built with Kenya-First principles for elite engineering teams**
