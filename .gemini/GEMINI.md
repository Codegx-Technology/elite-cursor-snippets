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

These contributions have significantly moved Shujaa Studio towards becoming a more intelligent, reliable, and culturally authentic platform for AI-powered cinematic content creation.

## Build Execution

*   **Rule:** Always check if the project root has a `package.json` file before treating subfolders as workspaces.
*   **Rule:** For standalone React/Next.js applications, always run `npm install` and build commands (e.g., `npm run build`, `next build`) strictly inside that subfolder.
*   **Note on Build Execution:** If standard `npm install` or `npm run build` commands encounter "not a registered workspace directory" errors, explicitly navigate into the project subdirectory (e.g., `cd frontend`) before executing `npm` or `npx` commands. For example: `cd frontend && npm install --legacy-peer-deps && npm run build`. This forces the commands to execute within the context of the subdirectory, bypassing root workspace assumptions.