# README_DEPLOY.md

This document outlines the deployment strategy and operational guidance for Shujaa Studio, focusing on enterprise-grade practices.

## 1. Branch Strategy

We follow a Gitflow-like branching strategy:
*   `main`: Production-ready code. Only stable, tested releases are merged here.
*   `develop`: Integration branch for new features. All feature branches are merged into `develop`.
*   `feature/your-feature-name`: Branches for new features or significant changes. Branch off `develop`.
*   `bugfix/issue-id`: Branches for bug fixes. Branch off `main` for hotfixes, or `develop` for regular bug fixes.
*   `release/version-number`: Branches for preparing new releases. Branch off `develop`.

## 2. How to Run Tests

Ensure you have installed the development dependencies (e.g., `pytest`).

```bash
pip install -r requirements.txt
pip install pytest
pytest
```

## 3. How to Run Orchestrator in Dry-Run Mode

The `pipeline_orchestrator.py` can be run in a dry-run mode to test its decision-making logic without executing the full video generation pipelines.

```bash
python pipeline_orchestrator.py
```

This will print the orchestrator's decisions based on various simulated inputs.

## 4. How to Set Hugging Face API Key

Your Hugging Face API key is crucial for accessing various AI models. It should be set as an environment variable.

*   **Linux/macOS:**
    ```bash
    export HF_API_KEY="your_hugging_face_api_key"
    ```
*   **Windows (Command Prompt):**
    ```cmd
    set HF_API_KEY="your_hugging_face_api_key"
    ```
*   **Windows (PowerShell):**
    ```powershell
    $env:HF_API_KEY="your_hugging_face_api_key"
    ```

Alternatively, you can place it in a `.env` file in the project root:

```
HF_API_KEY=your_hugging_face_api_key
```

## 5. How to Add Local Models

For local fallbacks or offline operation, you can configure paths to local models in `config.yaml`.

1.  **Download Models:** Obtain the model files (e.g., LLaMA.cpp compatible LLM, Stable Diffusion checkpoints, Bark models, Whisper models).
2.  **Update `config.yaml`:** Modify the `local_fallback_path` for each model type:

    ```yaml
    models:
      text_generation:
        local_fallback_path: "/path/to/your/local/llm_model"
      image_generation:
        local_fallback_path: "/path/to/your/local/sd_model"
      voice_synthesis:
        local_fallback_path: "/path/to/your/local/bark_model"
      speech_to_text:
        local_fallback_path: "/path/to/your/local/whisper_model"
    ```

## 6. Docker Commands

To build and run the application using Docker (requires Docker installed):

*   **Build the Docker image:**
    ```bash
    docker build -t shujaa-studio .
    ```
*   **Run the application with Docker Compose (includes Redis and Celery):**
    ```bash
    docker-compose up --build
    ```

## 7. Typical Troubleshooting Steps

*   **HF 403 Forbidden Error:**
    *   Ensure your `HF_API_KEY` is correct and has 'read' access.
    *   Verify you have accepted the terms and conditions for specific models (e.g., LLaMA 3) on their Hugging Face model page.
    *   Run `python -c "from hf_utils import validate_hf_model_access; print(validate_hf_model_access('meta-llama/Meta-LLaMA-3-8B-Instruct', os.getenv('HF_API_KEY')))"` to diagnose model access.
*   **Missing Dependencies:** Run `pip install -r requirements.txt`.
*   **FFmpeg Not Found:** Ensure FFmpeg is installed and added to your system's PATH.
*   **Redis Connection Error:** Ensure your Redis server is running and accessible on `localhost:6379` (or as configured).

## 8. PR Guidance

(This section will be detailed in Step 15 of the execution plan.)
