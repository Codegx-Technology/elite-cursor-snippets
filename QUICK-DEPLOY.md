# 🚀 Quick Deploy Guide

## **Temporary Access (Until Dedicated Repo is Created)**

Since the Elite AI Prompt Arsenal is currently in the `salongenz` repository, here's how to access it:

### **Method 1: Clone from Existing Repository**
```bash
# Clone the salongenz repository
git clone https://github.com/Codegx-Technology/salonG
cd salonG

# Copy the arsenal files to your project
cp -r .vscode/Elite\ Prompt\ Setup.code-snippets /your/project/.vscode/
cp -r .vscode/Smart\ Context\ Templates.code-snippets /your/project/.vscode/
cp AI-Prompt-Arsenal.md /your/project/
```

### **Method 2: Download Individual Files**
```bash
# Create .vscode directory in your project
mkdir -p /your/project/.vscode

# Download the snippet files
curl -o /your/project/.vscode/Elite\ Prompt\ Setup.code-snippets \
  https://raw.githubusercontent.com/Codegx-Technology/salonG/main/.vscode/Elite%20Prompt%20Setup.code-snippets

curl -o /your/project/.vscode/Smart\ Context\ Templates.code-snippets \
  https://raw.githubusercontent.com/Codegx-Technology/salonG/main/.vscode/Smart%20Context%20Templates.code-snippets

curl -o /your/project/AI-Prompt-Arsenal.md \
  https://raw.githubusercontent.com/Codegx-Technology/salonG/main/AI-Prompt-Arsenal.md
```

### **Method 3: Manual Copy**
1. Go to https://github.com/Codegx-Technology/salonG
2. Navigate to `.vscode/` folder
3. Download `Elite Prompt Setup.code-snippets`
4. Download `Smart Context Templates.code-snippets`
5. Download `AI-Prompt-Arsenal.md`
6. Place them in your project's `.vscode/` folder

## **Available Arsenal**

### **Core AI Prompts (9 Patterns)**
- `thinkwithai` - Strategic reasoning partner
- `surgicalfix` - Precision bug fixes
- `refactorintent` - Clean refactoring
- `writetest` - Unit test generation
- `doccode` - Kenya-first documentation
- `unstuck` - Cursor rerouting
- `augmentsearch` - Semantic search
- `kenyafirst` - Kenyan tone/brand
- `mindreset` - State clearing

### **Smart Context Chains (6 Patterns)**
- `taskchain` - Task context
- `memorychain` - Memory context
- `debugchain` - Debug context
- `refactorchain` - Refactor context
- `searchchain` - Search context
- `recoverychain` - Recovery context

## **Usage**
1. Open any code file in Cursor
2. Type the prefix (e.g., `thinkwithai`)
3. Press Tab to expand
4. Fill in placeholders
5. Use in Cursor's AI chat

---

**Once the dedicated repository is created, you'll be able to use:**
```bash
git clone https://github.com/Codegx-Technology/elite-cursor-snippets
``` 