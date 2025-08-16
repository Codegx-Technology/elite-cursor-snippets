import asyncio
import os
import logging
from backend.cloud_registry import ProviderRegistry
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Dialect to provider mapping (can add local fine-tuned model)
DIALECT_PROVIDER_MAP = {
    "yoruba": ["GeminiProvider", "HuggingFaceProvider", "ColabProvider"], # Using actual class names
    "swahili": ["HuggingFaceProvider", "GeminiProvider", "KaggleProvider"],
    "igbo": ["GeminiProvider", "ColabProvider", "HuggingFaceProvider"],
    "kikuyu": ["ColabProvider", "HuggingFaceProvider"]
}

class AfricanCinematicGenerator:
    def __init__(self):
        self.registry = ProviderRegistry()
    
    async def generate(self, prompt: str, dialect: Optional[str] = None, max_retries: int = 3) -> Dict[str, Any]:
        last_exception = None
        
        # Determine provider priority based on dialect
        providers_to_try: List[str] = []
        if dialect and dialect.lower() in DIALECT_PROVIDER_MAP:
            providers_to_try = DIALECT_PROVIDER_MAP[dialect.lower()]
            logger.info(f"Dialect '{dialect}' detected. Prioritizing providers: {providers_to_try}")
        else:
            # If no specific dialect or dialect not mapped, try all registered providers
            providers_to_try = [type(p).__name__ for p in self.registry.providers]
            logger.info(f"No specific dialect or dialect not mapped. Trying all available providers: {providers_to_try}")

        # Filter and sort available providers based on the determined order
        # This assumes self.registry.providers contains instances of the provider classes
        # and that their __name__ matches the string in DIALECT_PROVIDER_MAP
        available_providers_instances = {type(p).__name__: p for p in self.registry.providers}
        
        sorted_providers_for_task = []
        for provider_name in providers_to_try:
            if provider_name in available_providers_instances:
                sorted_providers_for_task.append(available_providers_instances[provider_name])
        
        # If no specific dialect providers are available, fall back to all healthy providers sorted by router's default
        if not sorted_providers_for_task and dialect:
            logger.warning(f"No specific dialect providers found for '{dialect}'. Falling back to general routing.")
            # This will let the router decide the best provider based on its internal logic (health, latency, etc.)
            # We'll just pass the request to the router without pre-sorting providers.
            pass # Handled by the main try-except block below

        # Attempt generation with fallback
        for attempt in range(max_retries):
            logger.info(f"Attempt {attempt + 1}/{max_retries} for prompt: '{prompt[:50]}...'")
            
            # If specific providers were sorted, try them first
            if sorted_providers_for_task:
                for provider_instance in sorted_providers_for_task:
                    try:
                        logger.info(f"Trying provider: {type(provider_instance).__name__} for task.")
                        # The task_type here is implicitly "text_generation" or "audio_generation"
                        # based on the cinematic generator's purpose.
                        # We need to map this to the router's expected task_type.
                        # For now, let's assume "cinematic_content_generation" as a generic task_type.
                        # The router's execute_with_fallback will then use its internal routing rules.
                        
                        # The prompt needs to be passed as part of the payload
                        payload = {"prompt": prompt, "dialect": dialect}
                        result = await self.registry.route_request(
                            task_type="cinematic_content_generation", # Generic task type for router
                            payload=payload
                        )
                        # If route_request returns successfully, it means one of its internal fallbacks worked
                        
                        # Render the cinematic output
                        rendered_output_path = await self._render_cinematic_output(result, prompt, dialect) # ADD THIS LINE
                        result["rendered_output_path"] = rendered_output_path # ADD THIS LINE
                        return result
                    except Exception as e:
                        self.registry.log_failure(type(provider_instance).__name__, e)
                        last_exception = e
                        logger.warning(f"Provider {type(provider_instance).__name__} failed: {e}")
                        continue # Try next provider in the sorted list
            
            # If sorted_providers_for_task was empty or all failed,
            # or if no dialect was specified, let the router handle the full fallback chain
            try:
                logger.info("Attempting general routing via ProviderRegistry.route_request.")
                payload = {"prompt": prompt, "dialect": dialect}
                result = await self.registry.route_request(
                    task_type="cinematic_content_generation", # Generic task type for router
                    payload=payload
                )
                # Render the cinematic output
                rendered_output_path = await self._render_cinematic_output(result, prompt, dialect) # ADD THIS LINE
                result["rendered_output_path"] = rendered_output_path # ADD THIS LINE
                return result
            except Exception as e:
                self.registry.log_failure("GeneralRouting", e)
                last_exception = e
                logger.warning(f"General routing failed: {e}")
                # If this is the last attempt, the outer loop will raise
                if attempt == max_retries - 1:
                    raise RuntimeError(f"All generation attempts failed after {max_retries} retries: {last_exception}")
                else:
                    logger.info(f"Retrying generation (attempt {attempt + 2})...")
                    await asyncio.sleep(1) # Small delay before next retry

        raise RuntimeError(f"All generation attempts failed after {max_retries} retries: {last_exception}")

# Singleton instance for notebooks
cinema_gen = AfricanCinematicGenerator()

    async def _render_cinematic_output(self, generation_result: Dict[str, Any], original_prompt: str, dialect: Optional[str]) -> str:
        """
        Renders the generated content into a cinematic video/audio output.
        This is a placeholder for actual video rendering logic using moviepy or similar.
        """
        logger.info(f"Rendering cinematic output for task type: {generation_result.get('task_type')}")
        
        output_dir = "cinematic_output"
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, f"cinematic_video_{int(time.time())}.mp4")

        content_type = generation_result.get("task_type")
        content_url = generation_result.get("result") # Assuming 'result' holds the content_url or actual content

        if content_type == "text_generation":
            # Create a simple video from text
            text_content = content_url # Assuming result is the text directly
            logger.info(f"Rendering text content: {text_content[:100]}...")
            # Placeholder: Create a simple video with text overlay on a black background
            # Requires moviepy
            try:
                from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip
                from moviepy.audio.AudioClip import AudioArrayClip
                import numpy as np
                import time # Import time for int(time.time())

                # Create a black background clip
                duration = 5 # seconds
                clip = ColorClip(size=(1280, 720), color=(0,0,0), duration=duration)

                # Create a text clip
                txt_clip = TextClip(text_content, fontsize=40, color='white', bg_color='transparent', size=(1200, 600))
                txt_clip = txt_clip.set_pos('center').set_duration(duration)

                # Composite the text onto the background
                final_clip = CompositeVideoClip([clip, txt_clip])

                # Add a silent audio track if no audio is generated
                # This is a simplified approach; a real scenario might generate TTS for the text
                audio_array = np.zeros((int(44100 * duration), 2)) # Stereo silent audio
                audio_clip = AudioArrayClip(audio_array, fps=44100)
                final_clip = final_clip.set_audio(audio_clip)

                final_clip.write_videofile(output_file_path, fps=24, codec="libx264")
                logger.info(f"Text-based video rendered to: {output_file_path}")
                return output_file_path
            except ImportError:
                logger.warning("MoviePy not installed. Cannot render text to video. Returning text content.")
                return text_content # Return raw text if rendering fails
            except Exception as e:
                logger.error(f"Error rendering text to video: {e}")
                return text_content # Return raw text on error

        elif content_type == "image_generation":
            # Create a video from an image
            image_path = content_url # Assuming result is the path to the image file
            logger.info(f"Rendering image from: {image_path}")
            try:
                from moviepy.editor import ImageClip, ColorClip, CompositeVideoClip, AudioFileClip
                from moviepy.audio.AudioClip import AudioArrayClip
                import numpy as np
                import time # Import time for int(time.time())

                duration = 5 # seconds
                # Create an image clip
                img_clip = ImageClip(image_path).set_duration(duration)
                
                # Ensure image clip has audio (silent if none provided)
                audio_array = np.zeros((int(44100 * duration), 2)) # Stereo silent audio
                audio_clip = AudioArrayClip(audio_array, fps=44100)
                img_clip = img_clip.set_audio(audio_clip)

                img_clip.write_videofile(output_file_path, fps=24, codec="libx264")
                logger.info(f"Image-based video rendered to: {output_file_path}")
                return output_file_path
            except ImportError:
                logger.warning("MoviePy not installed. Cannot render image to video. Returning image path.")
                return image_path
            except Exception as e:
                logger.error(f"Error rendering image to video: {e}")
                return image_path

        elif content_type == "audio_generation":
            # Create a video from audio with a static background (e.g., black screen or a placeholder image)
            audio_path = content_url # Assuming result is the path to the audio file
            logger.info(f"Rendering audio from: {audio_path}")
            try:
                from moviepy.editor import ColorClip, AudioFileClip
                import time # Import time for int(time.time())
                
                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration

                # Create a black background clip
                video_clip = ColorClip(size=(1280, 720), color=(0,0,0), duration=duration)
                video_clip = video_clip.set_audio(audio_clip)

                video_clip.write_videofile(output_file_path, fps=24, codec="libx264")
                logger.info(f"Audio-based video rendered to: {output_file_path}")
                return output_file_path
            except ImportError:
                logger.warning("MoviePy not installed. Cannot render audio to video. Returning audio path.")
                return audio_path
            except Exception as e:
                logger.error(f"Error rendering audio to video: {e}")
                return audio_path

        else:
            logger.warning(f"Unsupported content type for rendering: {content_type}. Returning raw content URL.")
            return content_url