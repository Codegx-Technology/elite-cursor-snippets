# Development Guide

This guide provides instructions for developers working on the Shujaa Studio project. It covers the project setup, development workflow, and coding conventions.

## 1. Project Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd ShujaaStudio
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Download AI models (optional):**

    Create the following directories:

    ```bash
    mkdir -p models/tts models/llm models/img models/music
    ```

    Download the required models and place them in the corresponding directories.

## 2. Development Workflow

1.  **Run the application:**

    *   **Web Interface:**

        ```bash
        python generate_video.py
        ```

    *   **Command-Line Interface:**

        ```bash
        python offline_video_maker/generate_video.py "Your prompt here"
        ```

2.  **Testing:**

    Run the test script to verify the video generation pipeline:

    ```bash
    python offline_video_maker/test_video_generation.py
    ```

## 3. Elite Cursor Snippets

The `offline_video_maker/generate_video.py` script follows a development methodology that uses special comments called "Elite Cursor Snippets." These snippets provide context about the code and its purpose.

**Snippet Format:**

```
// [KEY]: Value
```

**Common Keys:**

*   `[TASK]`: A description of the task that the code is supposed to accomplish.
*   `[GOAL]`: The objective of the code.
*   `[CONSTRAINTS]`: Any limitations or constraints on the code.
*   `[SNIPPET]`: The name of the snippet being used.
*   `[CONTEXT]`: The context in which the code is being used.
*   `[PROGRESS]`: The current status of the code.
*   `[NEXT]`: The next step in the development process.
*   `[LOCATION]`: The location of the code in the project.

These snippets help to improve code clarity, maintainability, and collaboration. When working on the project, you should follow this convention and use the snippets to document your code.

## 4. Coding Conventions

*   **Style:** Follow the PEP 8 style guide for Python code.
*   **Docstrings:** Use Google-style docstrings for all modules, classes, and functions.
*   **Comments:** Use comments to explain complex logic and to provide context for your code.
*   **Naming:** Use descriptive names for variables, functions, and classes.