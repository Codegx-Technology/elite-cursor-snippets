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