import asyncio
import logging
from typing import Any, Dict
from backend.ai_routing.providers.base_provider import BaseProvider
# Assuming Hugging Face API client is available or can be imported
# from transformers import pipeline # Example for local inference
# from huggingface_hub import InferenceClient # Example for hosted inference

logger = logging.getLogger(__name__)

class HuggingFaceProvider(BaseProvider):
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.model_id = config.get("model_id")
        self.api_key = config.get("api_key") # For hosted inference API

        if not self.model_id:
            logger.warning(f"HuggingFaceProvider {self.name}: 'model_id' not configured.")
        # Initialize InferenceClient if using hosted models
        from huggingface_hub import InferenceClient
        self.client = InferenceClient(model=self.model_id, token=self.api_key)

    async def process_request(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"HuggingFaceProvider {self.name}: Processing {task_type} request for model {self.model_id}.")
        try:
            if not self.model_id:
                raise ValueError("Hugging Face model_id not configured.")
            
            if task_type == "text_generation":
                prompt = payload.get("prompt")
                if not prompt:
                    raise ValueError("Prompt is required for text generation.")
                response = await self.client.text_generation(prompt)
                result_content = response # InferenceClient.text_generation returns string
            elif task_type == "image_generation":
                prompt = payload.get("prompt")
                if not prompt:
                    raise ValueError("Prompt is required for image generation.")
                image_bytes = await self.client.image_generation(prompt)
                # Save image bytes to a temporary file and return path
                import tempfile
                import os
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_file.write(image_bytes)
                    result_content = tmp_file.name
                logger.info(f"HuggingFaceProvider {self.name}: Image saved to {result_content}")
            elif task_type == "audio_generation": # Assuming TTS
                text = payload.get("prompt") # Assuming prompt is the text for TTS
                if not text:
                    raise ValueError("Text is required for audio generation.")
                audio_bytes = await self.client.text_to_speech(text)
                # Save audio bytes to a temporary file and return path
                import tempfile
                import os
                with tempfile.NamedTemporaryFile(delete=False, suffix=".flac") as tmp_file: # HF often returns FLAC
                    tmp_file.write(audio_bytes)
                    result_content = tmp_file.name
                logger.info(f"HuggingFaceProvider {self.name}: Audio saved to {result_content}")
            else:
                raise ValueError(f"Unsupported task type for Hugging Face: {task_type}")

            response_data = {
                "status": "success",
                "provider": self.name,
                "task_type": task_type,
                "result": result_content # This will be the generated text or path to file
            }
            logger.info(f"HuggingFaceProvider {self.name}: Request processed successfully.")
            return response_data
        except Exception as e:
            logger.error(f"HuggingFaceProvider {self.name}: Failed to process request: {e}")
            raise

    async def check_health(self) -> bool:
        logger.info(f"HuggingFaceProvider {self.name}: Checking health for model {self.model_id}.")
        try:
            if not self.model_id:
                logger.warning(f"HuggingFaceProvider {self.name}: No model_id configured for health check.")
                return False
            
            # Attempt a very small, quick inference to check health
            # For text generation, a simple "hello" prompt
            # For other models, a specific health check endpoint or a small dummy request
            
            # This is a simplified health check. A robust one might check model status directly.
            # For now, we'll try a text generation if the model is a text model, or just assume healthy if model_id exists.
            
            # If the model is a text generation model, try a quick inference
            # This is a heuristic, as self.client.text_generation might not be available for all model types
            try:
                # Attempt a very small text generation to check if the model is responsive
                # This might fail if the model_id is not for text generation
                await self.client.text_generation("health check", max_new_tokens=1)
                logger.info(f"HuggingFaceProvider {self.name}: Health check successful via text generation.")
                return True
            except Exception as e:
                logger.warning(f"HuggingFaceProvider {self.name}: Text generation health check failed: {e}. Assuming unhealthy.")
                return False
            
        except Exception as e:
            logger.error(f"HuggingFaceProvider {self.name}: Health check failed: {e}")
            return False