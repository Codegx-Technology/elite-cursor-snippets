# Project Overview: Shujaa Studio

## 1. Introduction

Shujaa Studio is an offline-first AI video generator designed to empower African content creators. It transforms text prompts into engaging videos, complete with voice narration, visuals, and subtitles. The project prioritizes cultural relevance, local language support, and accessibility for users with limited internet connectivity.

## 2. Core Features

*   **Text-to-Video Generation:** The primary function of Shujaa Studio is to generate videos from user-provided text prompts.
*   **Offline First:** All core functionalities are designed to work without an internet connection, making it suitable for use in areas with limited or unreliable internet access.
*   **African-Centric Content:** The project is tailored to create content that is culturally relevant to Africa, with a focus on local stories, languages, and contexts.
*   **Modular Architecture:** The video generation process is broken down into a series of modular components, allowing for flexibility and future expansion.
*   **Web and CLI Interfaces:** Shujaa Studio provides both a user-friendly web interface (powered by Gradio) and a command-line interface (CLI) for advanced users and automation.

## 3. Target Audience

*   **Youth Content Creators:** Creating engaging content such as Sheng cartoons, music videos, and short stories.
*   **Civic Organizations:** Developing educational materials on topics like anti-corruption, election processes, and civic rights.
*   **Cultural Heritage Keepers:** Preserving and sharing folktales, legends, and historical narratives from various African cultures.
*   **Educators:** Creating localized educational content and edutainment videos.

## 4. Technology Stack

*   **Backend:** Python
*   **Web UI:** Gradio
*   **Video Processing:** FFmpeg, MoviePy
*   **AI Models:**
    *   **Language (LLM):** Mistral, LLaMA
    *   **Text-to-Speech (TTS):** Bark, XTTS, Coqui TTS
    *   **Image Generation:** Stable Diffusion (SDXL, SD 1.5)
    *   **Subtitles:** Whisper