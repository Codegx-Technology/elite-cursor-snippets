# 🧠 Elite AI Prompt Arsenal for Cursor & Augment

> **Lightning-fast AI patterns for elite engineering in Cursor**

A comprehensive collection of intelligent prompt snippets and context management tools that transform your Cursor experience into an elite AI-powered development environment.

---

## 🚀 Installation

Get up and running with the Elite AI Prompt Arsenal in a few simple steps.

### **Option 1: Global Installation (Recommended)**

Install the snippets globally to make them available in all your Cursor workspaces.

*   **On Windows (PowerShell):**
    ```powershell
    .\deploy-elite-arsenal.ps1 -Global
    ```
*   **On macOS/Linux (Bash):**
    ```bash
    ./sync-arsenal.sh -g
    ```

### **Option 2: Project-Specific Installation**

Install the snippets directly into your current project's `.vscode` directory.

*   **On Windows (PowerShell):**
    ```powershell
    .\deploy-elite-arsenal.ps1 -ProjectPath "C:\path\to\your\project"
    ```
*   **On macOS/Linux (Bash):**
    ```bash
    ./sync-arsenal.sh -p /path/to/your/project
    ```

---

## 🔧 How to Use

The arsenal is designed to be easy to learn and use. Instead of memorizing dozens of commands, you only need to remember **6 main category prefixes**.

**Step 1: Type a category prefix** in your code file to see the available options.

| Category     | Prefix     | What it does                      |
|--------------|------------|-----------------------------------|
| **Core AI**  | `ai`       | Show all AI prompt options        |
| **Refactor** | `refactor` | Show all refactoring options      |
| **Daily**    | `daily`    | Show all daily companion options  |
| **Guardrails**| `guard`    | Show all guardrails options       |
| **Context**  | `context`  | Show all context chain options    |
| **Quick**    | `quick`    | Show most commonly used options   |

**Step 2: Press `Tab`** to see the list of available snippets in that category.

**Step 3: Choose a snippet** from the list, type its prefix, and press `Tab` again to expand the full prompt.

---

## 🎯 The Prompts

This repository contains over 40 specialized prompts to accelerate your development workflow.

*   **For a gentle introduction** and to learn the system, check out the **[Getting Started Guide](./GETTING-STARTED-GUIDE.md)**.
*   **For a complete list** of all available prompts and their advanced features, see the **[Full Prompt Arsenal Reference](./AI-Prompt-Arsenal.md)**.

---

## 🔄 Synchronization and Collaboration

This repository uses a **two-way synchronization strategy** to ensure that all team members can contribute to and benefit from the latest updates to the prompt arsenal.

*   **The `elite-cursor-snippets` repository is the central source of truth.**
*   **Active Development:** When you are actively developing new snippets, use the `smart-elite-sync-v2.bat` script (in this repository) to push your changes to the central repository.
*   **Getting Updates:** To pull the latest snippets from the central repository into any of your projects, use the `pull-elite-arsenal.bat` script.

This system allows for seamless collaboration, ensuring that everyone has access to the most up-to-date set of tools.

---

## 🤝 Contributing

Want to add more elite prompts or improve the arsenal?

1.  Fork this repository.
2.  Add your enhancements.
3.  Submit a pull request.
4.  Help make Cursor even more powerful!

---

## 🌍 Global Snippets Location & Cross-Project Usage

The arsenal is typically installed globally so it works in every project for this Windows user account.

* __Global location (Windows)__
  * `C:\Users\LENOVO\AppData\Roaming\Code\User\snippets\elite-global-snippets.code-snippets`
  * `C:\Users\LENOVO\AppData\Roaming\Code\User\snippets\elite-context-templates.code-snippets`

* __What we changed (workspace cleanup)__
  * Removed duplicate configs from the root workspace `.vscode/` to avoid VS Code double-loading.
  * Kept this repo as the source of truth. Use the deploy scripts here to sync.

* **Use in other projects**
  * Global install: run `./deploy-elite-arsenal.ps1 -Global` (Windows) or `./sync-arsenal.sh -g` (macOS/Linux). Snippets will be available in all workspaces.
  * Project-scoped: run `./deploy-elite-arsenal.ps1 -ProjectPath "C:\path\to\project"` (or `./sync-arsenal.sh -p /path/to/project`) to copy into a project’s `.vscode/`.
  * In the editor: type a category prefix like `ai`, `refactor`, `daily`, `guard`, `context`, or `quick`, then press Tab. If Tab doesn’t expand, enable:
    - `editor.tabCompletion: on`
    - `editor.snippetSuggestions: top`
    - `editor.suggest.showSnippets: true`
  * Auto-deploy: a local `post-commit` hook runs the global deploy on each commit (developer machine only).

---

## 📄 License

MIT License - Use freely in your projects!

_Sync note: auto-deploy hook verification edit on 2025-08-18 15:30 EAT._
