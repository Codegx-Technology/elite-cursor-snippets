import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional, Type

import yaml
from dotmap import DotMap

from backend.ai_routing.providers.base_provider import BaseProvider
from backend.ai_routing.providers.colab_provider import ColabProvider
from backend.ai_routing.providers.kaggle_provider import KaggleProvider
from backend.ai_routing.providers.huggingface_provider import HuggingFaceProvider
from backend.ai_routing.providers.runpod_provider import RunPodProvider
from backend.ai_routing.providers.gemini_provider import GeminiProvider

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Router:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()
        self.providers: Dict[str, BaseProvider] = {}
        self.health_check_interval = self.config.get('health_check_interval', 30) # seconds
        self.fallback_retries = self.config.get('fallback_retries', 2)

        # Dynamically initialize and register providers from config
        for provider_name, provider_config in self.config.providers.items():
            provider_type = provider_config.get("type")
            if provider_type in self.PROVIDER_CLASSES:
                provider_class = self.PROVIDER_CLASSES[provider_type]
                instance = provider_class(provider_name, provider_config)
                self.register_provider(instance)
            else:
                logger.warning(f"Unknown provider type '{provider_type}' for provider '{provider_name}'. Skipping.")

    PROVIDER_CLASSES = {
        "colab": ColabProvider,
        "kaggle": KaggleProvider,
        "huggingface": HuggingFaceProvider,
        "runpod": RunPodProvider,
        "gemini": GeminiProvider,
    }

    def load_config(self) -> DotMap:
        """Loads routing configuration from a YAML file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {self.config_path}")
        return DotMap(config_data)

    def register_provider(self, provider_instance: BaseProvider):
        """Registers a provider with the router."""
        self.providers[provider_instance.name] = provider_instance
        logger.info(f"Provider '{provider_instance.name}' registered.")

    async def _perform_health_check(self, provider: BaseProvider):
        """Performs a health check for a single provider."""
        start_time = time.time()
        try:
            is_healthy = await provider.check_health()
            if is_healthy:
                latency = (time.time() - start_time) * 1000 # ms
                provider.latency = latency
            else:
                provider.latency = float('inf') # Set to inf if unhealthy
            provider.is_healthy = is_healthy
            if is_healthy:
                logger.debug(f"Provider '{provider.name}' is healthy (latency: {latency:.2f}ms).")
            else:
                logger.warning(f"Provider '{provider.name}' is unhealthy.")
        except Exception as e:
            provider.is_healthy = False
            provider.latency = float('inf')
            logger.error(f"Health check for '{provider.name}' failed: {e}")

    async def start_health_monitoring(self):
        """Starts periodic health monitoring for all registered providers."""
        while True:
            logger.info("Starting periodic health checks...")
            tasks = [self._perform_health_check(p) for p in self.providers.values()]
            await asyncio.gather(*tasks)
            logger.info(f"Health checks completed. Next check in {self.health_check_interval} seconds.")
            await asyncio.sleep(self.health_check_interval)

    def route_task(self, task_type: str, payload: Dict[str, Any]) -> Optional[BaseProvider]:
        """
        Chooses the best provider for a given task type based on routing rules,
        health, and latency.
        """
        rules = self.config.routing_rules.get(task_type)
        if not rules:
            logger.warning(f"No routing rules found for task type '{task_type}'.")
            return None

        eligible_providers = []
        for provider_name in rules.priority:
            provider = self.providers.get(provider_name)
            if provider and provider.is_healthy:
                eligible_providers.append(provider)
            elif provider:
                logger.debug(f"Provider '{provider_name}' is not healthy, skipping for '{task_type}'.")
            else:
                logger.warning(f"Configured provider '{provider_name}' not registered.")

        if not eligible_providers:
            logger.error(f"No healthy providers available for task type '{task_type}'.")
            return None

        # Sort by latency (fastest first) if multiple eligible providers
        eligible_providers.sort(key=lambda p: p.latency)

        return eligible_providers[0]

    async def execute_with_fallback(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a task, attempting fallbacks if the preferred provider fails.
        """
        attempt = 0
        while attempt <= self.fallback_retries:
            provider = self.route_task(task_type, payload)
            if not provider:
                raise RuntimeError(f"No suitable provider found for task type '{task_type}' after {attempt} attempts.")

            logger.info(f"Attempting task '{task_type}' with provider '{provider.name}' (attempt {attempt + 1})...")
            try:
                result = await provider.process_request(task_type, payload)
                logger.info(f"Task '{task_type}' successful with provider '{provider.name}'.")
                return result
            except Exception as e:
                logger.error(f"Provider '{provider.name}' failed for task '{task_type}': {e}")
                attempt += 1
                if attempt <= self.fallback_retries:
                    logger.info(f"Attempting fallback for task '{task_type}'...")
                else:
                    logger.error(f"All fallback attempts failed for task '{task_type}'.")
                    # The final RuntimeError after the loop will handle this.

        raise RuntimeError(f"Failed to execute task '{task_type}' after {self.fallback_retries + 1} attempts.")
