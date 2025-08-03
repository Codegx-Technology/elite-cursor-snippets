# 🧬 Smart Prompt Chaining Templates

## **Phase 4: Advanced Context Management**

Use these templates to create repeatable context chains in your code without external YML files.

---

## 🎯 **Context Chain Patterns**

### **1. Task Context Chain**
```javascript
// [TASK]: Implement user authentication flow
// [GOAL]: Secure login with JWT tokens
// [CONSTRAINTS]: Must work offline, no breaking changes
// [SNIPPET]: thinkwithai
// [CONTEXT]: Previous attempts failed due to token expiration

// Now, let's think through this step by step...
```

### **2. Memory Context Chain**
```javascript
// [AI-MEMORY]: ONBOARDING_LANG_SWITCH_LOGIC
// [SNIPPET]: thinkwithai
// [GOAL]: Implement multilingual bot using ARB + SharedPrefs
// [PROGRESS]: Completed language detection, stuck on persistence
// [NEXT]: Fix SharedPrefs write/read cycle

// Continuing from where we left off...
```

### **3. Debug Context Chain**
```javascript
// [DEBUG]: Authentication state loss after app restart
// [SNIPPET]: surgicalfix
// [LOCATION]: AuthService.java line 45
// [SYMPTOM]: Token persists but user state resets
// [SUSPECT]: SharedPrefs key mismatch

// Apply surgical fix here...
```

### **4. Refactor Context Chain**
```javascript
// [REFACTOR]: Extract reusable validation logic
// [SNIPPET]: refactorintent
// [TARGET]: Form validation methods
// [GOAL]: Single validation utility class
// [CONSTRAINTS]: Keep existing API, improve reusability

// Refactor with intent...
```

---

## 🔄 **Auto-Recall Patterns**

### **5. Search Context Chain**
```javascript
// [SEARCH]: Find all authentication-related files
// [SNIPPET]: augmentsearch
// [START]: AuthService.java
// [GOAL]: Understand complete auth flow
// [SCOPE]: All auth, login, token files

// Begin semantic search...
```

### **6. Recovery Context Chain**
```javascript
// [RECOVERY]: AI stuck in authentication loop
// [SNIPPET]: mindreset
// [ISSUE]: Cursor keeps suggesting OAuth when we need JWT
// [GOAL]: Simple JWT implementation
// [CLEAR]: Previous OAuth suggestions

// Reset and refocus...
```

---

## 🧠 **Context Variables**

Use these variables in your context chains:

| **Variable** | **Purpose** | **Example** |
|--------------|-------------|-------------|
| `[TASK]` | Current task description | `[TASK]: Fix login button styling` |
| `[GOAL]` | Desired outcome | `[GOAL]: Responsive design on all devices` |
| `[CONSTRAINTS]` | Limitations/requirements | `[CONSTRAINTS]: No external dependencies` |
| `[SNIPPET]` | Which prompt to use | `[SNIPPET]: surgicalfix` |
| `[CONTEXT]` | Background information | `[CONTEXT]: Previous attempts failed` |
| `[PROGRESS]` | Current status | `[PROGRESS]: 70% complete, stuck on validation` |
| `[NEXT]` | Next action | `[NEXT]: Implement error handling` |
| `[LOCATION]` | File/line reference | `[LOCATION]: LoginActivity.kt line 23` |

---

## 🚀 **Usage Instructions**

1. **Copy a template** from above
2. **Customize the variables** for your specific task
3. **Paste in your code** where you need AI assistance
4. **Use the specified snippet** (e.g., `thinkwithai`, `surgicalfix`)
5. **AI will pick up context** from the comment chain

---

## ✅ **Benefits**

- **No external files** - Everything in your code
- **Version controlled** - Context travels with your code
- **Team friendly** - Others can understand your AI context
- **Repeatable** - Same patterns work consistently
- **Token efficient** - Minimal overhead, maximum context

---

## 🎯 **Example Workflow**

```javascript
// [TASK]: Implement user profile editing
// [GOAL]: Allow users to update name, email, avatar
// [SNIPPET]: thinkwithai
// [CONSTRAINTS]: Must validate email format, image size < 5MB

// Let's think through this step by step...
```

**Result:** AI understands exactly what you're building and can provide targeted assistance.

---

**Your Smart Prompt Chaining system is now ready for advanced context management!** 🧬 