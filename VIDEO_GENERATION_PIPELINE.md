# Video Generation Pipeline

The video generation process in Shujaa Studio is a multi-step pipeline that transforms a text prompt into a complete video. This document outlines each stage of the pipeline.

## 1. Prompt Input

The process begins with a user providing a text prompt. This prompt can be a simple sentence, a short story, or a concept for a video. The prompt is the primary input that guides the entire video generation process.

## 2. Script Generation

*   **Input:** Text prompt
*   **Process:** The prompt is fed into a Large Language Model (LLM) like Mistral or LLaMA to generate a detailed script. The script includes a title, scene breakdowns, narration for each scene, and descriptions for the visuals.
*   **Output:** A structured script in JSON format.

## 3. Voice Synthesis

*   **Input:** Narration text from the script.
*   **Process:** For each scene, the narration text is converted into an audio file using a Text-to-Speech (TTS) engine like Bark or XTTS. The system can also use system-level TTS as a fallback.
*   **Output:** A series of audio files (e.g., in WAV format), one for each scene.

## 4. Image Generation

*   **Input:** Scene descriptions from the script.
*   **Process:** Based on the visual descriptions in the script, an image generation model like Stable Diffusion creates a unique image for each scene. If the model is not available, the system generates placeholder images.
*   **Output:** A series of image files (e.g., in PNG format), one for each scene.

## 5. Subtitle Generation

*   **Input:** The generated audio files.
*   **Process:** The audio for each scene is transcribed using the Whisper model to generate subtitles. This makes the videos more accessible and easier to understand.
*   **Output:** Subtitle files (e.g., in SRT format).

## 6. Video Assembly

*   **Input:** Audio files, image files, and subtitle files.
*   **Process:** The audio and image for each scene are combined to create a video clip. The subtitles are then overlaid on the video. Finally, all the scene clips are concatenated in the correct order to create the final video.
*   **Output:** A single video file (e.g., in MP4 format).

## 7. Fallback Mechanisms

The pipeline is designed to be resilient and work offline. If any of the AI models are not available, the system has fallback mechanisms:

*   **Voice:** If a TTS model is not available, the system can use a system-level TTS engine or generate a silent audio track.
*   **Image:** If an image generation model is not available, the system will create artistic placeholder images with the scene description as text.
*   **Video:** If `moviepy` is not available, the system will create an audio-only output of the generated narration.