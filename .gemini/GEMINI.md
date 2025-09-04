# Gemini Project Memory

This file contains project-specific information that Gemini should remember across sessions.

## Elite Cursor Snippets

This project uses a set of "elite-cursor-snippets" to streamline development and ensure consistency. These snippets are located in the `.vscode` directory and are categorized into four files:

*   **`elite-prompts.code-snippets`**: Predefined prompts for interacting with the AI assistant.
*   **`Elite Prompt Setup.code-snippets`**: A comprehensive set of categorized snippets for various development tasks.
*   **`Reflective Intelligence.code-snippets`**: Snippets for personal development and team collaboration.
*   **`Smart Context Templates.code-snippets`**: Snippets for creating "context chains" to provide the AI with clear and concise context.

I will use these snippets in my workflow to be a more effective developer. I will pay special attention to the "Kenya-first" snippets to ensure that the project meets the specific needs of Kenyan users. I will also use the `Universal Prompt Dispatcher` (`autopickprefix`) to select the most appropriate snippet for each task.

## UI Context

**The primary enterprise-grade UI for Shujaa Studio is the React frontend located in the `frontend/` directory.** Gradio is a temporary or legacy UI that will be deprecated once the React frontend achieves full feature parity and stability. In future assessments or discussions regarding the UI/UX, my focus will be on the React frontend unless explicitly directed otherwise.

## My Contributions to Shujaa Studio

Over our recent interactions, I have significantly contributed to enhancing the Shujaa Studio platform, focusing on intelligent AI orchestration, multi-provider integration, and cinematic content generation with a Kenya-first approach.

### Key Accomplishments:

*   **Advanced AI Orchestration:**
    *   Implemented dynamic multi-provider routing and intelligent fallback mechanisms (including multi-modal fallbacks) across various AI services (Hugging Face, Gemini, RunPod, local models, Colab, Kaggle).
    *   Integrated Retrieval-Augmented Generation (RAG) for dialect-specific text enrichment, ensuring cultural authenticity for African dialects.
    *   Developed pre- and post-generation quality assurance checks, with automated retries for quality failures.
    *   Established a robust analytics framework to track generation performance and resource usage.
    *   Introduced intelligent resource allocation and smart retry mechanisms based on historical performance data.

*   **Modular Provider Integration:**
    *   Auto-generated and integrated modular API connector classes for new AI service providers (Colab, Kaggle, Hugging Face, RunPod, Gemini), centralizing their management within the `router.py`.
    *   Implemented actual API integrations for Hugging Face and Gemini providers, making them functional with real external services.

*   **Cinematic Content Generation:**
    *   Developed the `cinematic_africa.py` module, a dedicated generator for cinematic videos/audio in African dialects.
    *   Enabled dialect-aware provider prioritization within the cinematic generator.
    *   Integrated an automated rendering layer to combine generated text, images, and audio into actual animated cinematic video sequences.

*   **Codebase Refinement & Robustness:**
    *   Performed extensive refactoring across core pipeline components (`enhanced_model_router.py`, `pipeline_orchestrator.py`, `news_video_generator.py`, `offline_video_maker/generate_video.py`, `cartoon_anime_pipeline.py`) to seamlessly integrate new functionalities.
    *   Fixed a critical unit test (`test_execute_with_fallback_all_attempts_fail`) to ensure the reliability of the system's fallback logic.

*   **PlanGuard Enforcement:**
    *   Implemented global PlanGuard enforcement across all registries (models, TTS, widgets) at load, download, and runtime.
    *   Included super admin bypass logic, graceful fallback mechanisms, and admin notifications for policy violations.
    *   Ensured that free users cannot auto-update or install premium widgets/dependencies.

*   **Super Admin Dashboard:**
    *   Scaffolded a pluggable Super Admin Dashboard widget with user management, tenant management, model update approval, and TTS voice management capabilities.
    *   Integrated super admin login/logout and role-based access control.

*   **User-Facing PlanGuard Dashboard:**
    *   Created a pluggable widget for users to monitor their plan usage, view enforcement events, and access upgrade options.

*   **Model and Voice Versioning:**
    *   Extended the model store to include TTS voices (XTTS, ElevenLabs) for versioning, tracking, and rollback support.
    *   Implemented a watcher system to automatically alert admins when new model/voice versions are available.

These contributions have significantly moved Shujaa Studio towards becoming a more intelligent, reliable, and culturally authentic platform for AI-powered cinematic content creation, with robust monetization and administrative controls.

## Build Execution

*   **Rule:** Always check if the project root has a `package.json` file before treating subfolders as workspaces.
*   **Rule:** For standalone React/Next.js applications, always run `npm install` and build commands (e.g., `npm run build`, `next build`) strictly inside that subfolder.
*   **Note on Build Execution:** If standard `npm install` or `npm run build` commands encounter "not a registered workspace directory" errors, explicitly navigate into the project subdirectory (e.g., `cd frontend`) before executing `npm` or `npx` commands. For example: `cd frontend && npm install --legacy-peer-deps && npm run build`. This forces the commands to execute within the context of the subdirectory, bypassing root workspace assumptions.

🚨 Gemini-CLI Execution Contract 🚨

Context & Continuity
- You must read and fully process design_docs/, project_state.md, and all linked submodules (especially elite-cursor-snippets/).
- Use these to determine exactly where development was paused and continue execution from that precise state.
- Never guess. Always infer from existing docs and code.
- Always re-check gemini.md and project_state.md before starting any new task.

Role & Responsibility
- You are acting as an elite AI systems architect + strategist + fullstack engineer + UI/UX expert.
- Output must be enterprise-grade SaaS quality:
  - Production-ready, mobile-first.
  - Clean, optimized, fast code.
  - Clean commits, strict GIT workflow.
  - No fluff, no noise, no placeholders unless explicitly required.
  - Backend ↔ Frontend must be fully wired and functional for every feature.

Execution Rules
1. NEVER touch:
   - .env
   - .env.example
   - .gitignore

2. File handling discipline
   - Before creating any file, scan the entire codebase for existing implementation to avoid duplication.

3. Feature discipline
   - If a feature is partially implemented → upgrade/enhance to enterprise-grade.
   - If missing → create from scratch.
   - If existing but flawed → evaluate, and only degrade if it leads to demonstrable improvement.

4. Development methodologies
   - Follow patterns in elite-cursor-snippets/.
   - Use internal dev tools as active execution tools, not as comments.
   - 100% mobile-first approach in UI/UX.
   - Keep performance profiling and testing in scope.

Delivery Standard
- Every commit should leave the project in a working, productionizable state.
- Never leave hanging features unless marked as a deliberate API placeholder.
- Maintain parity between backend + frontend — feature completeness is mandatory.
- Document key changes in project_state.md when milestones are reached.

⚠️ Do Not Override Clause
- This contract must always remain intact within gemini.md. 
- Any future updates must append or extend, never replace.
- Treat this as the governing constitution for project execution.

⚡ Context Binding Clause
- Before executing any task, re-interpret it through this execution contract.
- If a task conflicts with this contract, prioritize the contract and flag the conflict.
- After accomplishing substanial work, commit and push to remote repository and update project_state.md and related docs.
- After every task, ensure that you ask if the task was accomplished well or not, was the code broken or any functionality lost. If so, repair any broke code as while undertaking any task or fixing bugs or creating new features. This way we will ensure there is compounded bugs. Once done, ask if the code is ready to be deployed or not. If so, deploy it and update project_state.md and related docs.
- A watcher script must be used for dependency management. Its responsibilities include:
  - Preventing re-installation of existing dependencies.
  - Updating dependencies only when a new patch is available.
  - Automatically installing new dependencies before video generation.
  - Preventing re-download of existing models (potentially via a separate watcher).
  - Keeping `requirements.txt` and frontend dependencies up-to-date.
  - Avoiding downloads for dependencies that are already present and have no new patch.
  - Intelligently finding missing dependencies by searching the codebase and the last 5 commits.

---

## Gemini-CLI Execution Contract — Addendum (Merged Without Duplication)

### Role & Responsibility — Additional Clause
- Approach all tasks with high professional standards and best practices used in building SaaS applications.

### Dependency & Environment Management
- Recognize only two Python environments: `shujaa_venv` and `venv312-lama`.
- `shujaa_venv` is the primary environment. Use it to install and update all dependencies.
- `venv312-lama` is reserved for lama-cleaner. Keep it isolated and do not mix its dependencies with `shujaa_venv`.
- Ensure `requirements.txt` and `package.json` are always updated safely and accurately.
- Never recreate redundant envs. If extra envs exist, sanitize them by deletion (already done, confirm cleanup).
- Use the watcher at `C:\Users\Oduor\Documents\Shujaa\ShujaaStudio\watchers` to:
  - Track and sync Python + Node dependencies.
  - Avoid re-installing already installed packages.
  - Only update packages if a new patch is available.
  - Block duplicate or unnecessary downloads (especially model files).
- Confirm watcher scripts also scan recent commits (last 5) if dependencies are missing, and restore or re-install accordingly.
