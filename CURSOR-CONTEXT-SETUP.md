# 🧠 Cursor Auto Context Setup Guide

## **Phase 7: Auto-Inject Local Context (Cursor Elite Mode)**

Enable Cursor to automatically load your project's unique context before responding — so it behaves like an embedded team member, not a generic assistant.

---

## ✅ **Step 1: Create prompt.context.yml**

**Location:** `C:\Users\LENOVO\Documents\ProjectsShared\salongenz\prompt.context.yml`

✅ **Already created!** The file contains your project's:
- Project goals and objectives
- Technology stack and conventions
- Coding rules and best practices
- Kenya-specific requirements
- UI/UX principles
- Payment flow requirements
- Development workflow

---

## ✅ **Step 2: Enable Auto Context in Cursor**

### **Method 1: Command Palette**
1. Open Cursor
2. Press `Ctrl + Shift + P` to open Command Palette
3. Type: `Toggle Inject Project Context`
4. Click to enable ✅

### **Method 2: Settings**
1. Open Cursor Settings (`Ctrl + ,`)
2. Search for "Inject Project Context"
3. Enable the experimental feature ✅

### **Method 3: Settings JSON**
Add to your Cursor settings:
```json
{
  "cursor.experimental.injectProjectContext": true
}
```

---

## 🎯 **Step 3: Verify Context Loading**

### **Test Context Loading**
Ask Cursor: "What project am I working on?"

**Expected Response:** Cursor should mention SalonGenz, Kenya, salon booking platform, etc.

### **Test Context Awareness**
Ask Cursor: "What coding conventions should I follow?"

**Expected Response:** Should mention snake_case for Python, camelCase for JS, async/await, etc.

---

## 🚀 **Phase 7 Usage Examples**

### **When Coding:**
```
Given the context, fix this form logic without breaking validation or payment flow.
```

### **When Debugging:**
```
Fix this error in booking flow. Reminder: we use async/await and don't break existing UX.
```

### **When Refactoring:**
```
Refactor this page to be cleaner, but don't break login or appointment state — context loaded.
```

### **When Adding Features:**
```
Add a new payment method following our Kenya-specific requirements and security standards.
```

---

## 🧠 **Context-Aware Prompts**

### **Payment Integration:**
```
Following our payment flow context, implement M-Pesa integration with proper error handling.
```

### **UI/UX Development:**
```
Create a mobile-first booking form following our UI/UX principles and Kenya-specific requirements.
```

### **Backend Development:**
```
Implement the booking API following our Python conventions and security considerations.
```

### **Frontend Development:**
```
Build a React component for service selection following our frontend conventions and responsive design.
```

---

## 🔧 **Advanced Context Features**

### **Context Variables Available:**
- `project_name`: SalonGenz
- `owner`: Paps
- `language_stack`: React, Django, Tailwind
- `conventions`: Coding standards
- `rules`: Development rules
- `kenya_specific`: Local requirements
- `ui_ux_principles`: Design guidelines
- `payment_flow`: Payment requirements
- `booking_system`: Booking features
- `development_workflow`: Git, testing, deployment
- `ai_integration`: AI usage guidelines
- `security_considerations`: Security requirements

### **Context-Aware Code Generation:**
```
// Cursor will automatically consider:
// - React functional components with hooks
// - camelCase for JavaScript
// - Mobile-first responsive design
// - Kenya-specific requirements
// - Payment flow integration
// - Security considerations
```

---

## 🎯 **Benefits of Auto Context**

### **Consistent Responses:**
- Cursor always knows your project context
- No need to repeat project details
- Consistent coding standards
- Aligned with project goals

### **Faster Development:**
- Reduced context switching
- Immediate project awareness
- Faster code generation
- Better debugging assistance

### **Quality Assurance:**
- Follows established conventions
- Respects security requirements
- Maintains UI/UX principles
- Considers local requirements

---

## 🔄 **Context Updates**

### **When to Update prompt.context.yml:**
- New technology stack additions
- Updated coding conventions
- New project requirements
- Security policy changes
- UI/UX guideline updates

### **How to Update:**
1. Edit `prompt.context.yml`
2. Save the file
3. Cursor automatically picks up changes
4. Test with a simple question

---

## ✅ **Verification Checklist**

- [ ] `prompt.context.yml` created in project root
- [ ] "Inject Project Context" enabled in Cursor
- [ ] Context loading verified with test questions
- [ ] Context-aware prompts working
- [ ] Project conventions being followed
- [ ] Kenya-specific requirements considered

---

## 🚀 **Ready for Phase 8**

Once you've completed Phase 7 setup and verification, you're ready for:

**Phase 8: Reflective Intelligence Layer (Daily Boost & Self-Coach Mode)**

This will add daily reflection prompts, self-coaching capabilities, and continuous improvement features to your Elite AI Prompt Arsenal.

---

**Your Cursor is now equipped with Auto Context and behaves like an embedded team member!** 🧠⚡ 