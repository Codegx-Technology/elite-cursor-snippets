import os
import json
import logging
from cloud_setup import configure_providers
from typing import List, Any, Tuple # Import Tuple
from backend.ai_routing.router import Router # Import Router for type hinting

logger = logging.getLogger(__name__)

class ProviderRegistry:
    def __init__(self):
        self.router, self.providers = configure_providers() # Get router and providers
        self.log_file = os.getenv("PROVIDER_LOG_FILE", "provider_fallback.log")
    
    def list_providers(self) -> List[str]:
        return [type(p).__name__ for p in self.providers]
    
    def log_failure(self, provider_name: str, error: Exception):
        with open(self.log_file, "a") as f:
            f.write(f"[{provider_name}] Failure: {str(error)}\n")
    
    async def execute(self, prompt: str, max_retries: int = 3) -> Any:
        # Leverage the router's execute_with_fallback for DRY principle
        logger.info(f"ProviderRegistry.execute: Routing request for prompt: '{prompt[:50]}...'")
        try:
            # The task_type here is implicitly "general_generation" or similar
            # The payload will contain the prompt.
            # The router's execute_with_fallback will handle all retries and fallbacks.
            result = await self.router.execute_with_fallback(
                task_type="general_generation", # Default task type for this interface
                payload={"prompt": prompt}
            )
            return result
        except Exception as e:
            self.log_failure("ProviderRegistry.execute", e)
            raise RuntimeError(f"ProviderRegistry.execute failed: {e}")

# Singleton instance for notebook access
registry = ProviderRegistry()
