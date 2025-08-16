import logging
from backend.ai_routing.router import Router
from backend.ai_routing.providers.base_provider import BaseProvider
from typing import List, Any

logger = logging.getLogger(__name__)

class ProviderRegistry:
    """
    Manages the registration and access to AI service providers.
    Acts as a bridge to the EnhancedModelRouter for dynamic routing.
    """
    def __init__(self):
        # Initialize the Router. This assumes router.py handles loading config and registering providers.
        # For this context, we'll assume a default config path or that the router is already initialized globally.
        # In a real application, the Router instance might be passed in or managed as a singleton.
        self.router = Router(config_path="backend/ai_routing/config.yaml") # Using test_config for now

    @property
    def providers(self) -> List[BaseProvider]:
        """Returns a list of all registered providers."""
        return list(self.router.providers.values())

    def log_failure(self, provider_name: str, exception: Exception):
        """Logs a failure for a specific provider."""
        logger.error(f"ProviderRegistry: Provider '{provider_name}' failed with exception: {exception}")
        # In a real system, this might update provider health status or analytics.

    async def route_request(self, task_type: str, payload: dict) -> dict:
        """Routes a request through the router's fallback mechanism."""
        return await self.router.execute_with_fallback(task_type, payload)