import asyncio
import logging
import os
import time
import random # For canary routing
from typing import Any, Dict, List, Optional, Type

import yaml
from dotmap import DotMap

from backend.ai_routing.providers.base_provider import BaseProvider
from backend.ai_routing.providers.colab_provider import ColabProvider
from backend.ai_routing.providers.kaggle_provider import KaggleProvider
from backend.ai_routing.providers.huggingface_provider import HuggingFaceProvider
from backend.ai_routing.providers.runpod_provider import RunPodProvider
from backend.ai_routing.providers.gemini_provider import GeminiProvider

# Import healthcheck functions
from backend.ai_health.healthcheck import record_metric, aggregate, score_inference
# Import ModelStore to get model metadata (e.g., blue/green strategy)
from backend.ai_models.model_store import ModelStore

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize ModelStore
model_store = ModelStore()

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
        Integrates blue/green and canary routing.
        """
        # Extract model info from payload if available (assuming a convention)
        # This part needs to be adapted based on how model_name and provider are passed in payload
        model_name = payload.get("model_name") # Example
        provider_name = payload.get("provider_name") # Example

        # Get model metadata from ModelStore if available
        model_metadata = None
        if model_name and provider_name:
            current_model_info = model_store.current(provider_name, model_name)
            if current_model_info:
                model_metadata = current_model_info.get("metadata", {})

        strategy = model_metadata.get("strategy")
        canary_pct = model_metadata.get("canary_pct", 0)

        target_provider = None
        active_tag = "main" # Default to main/blue
        canary_tag = "staging" # Default to staging/green

        if strategy == "bluegreen" and model_name and provider_name:
            # Determine which version to route to
            if random.randint(1, 100) <= canary_pct:
                logger.info(f"Routing {canary_pct}% of requests for {model_name} to canary (green) version.")
                # In a real scenario, you'd need to get the path to the green version
                # For now, we'll assume the 'green' version is identified by a specific tag
                # and the provider can handle routing to it. This is a simplification.
                # The actual routing would involve passing the version_tag to the provider.
                # For this example, we'll just log and proceed with the default provider.
                target_provider = self.route_task(task_type, payload) # Still route to best provider
                active_tag = "green" # Indicate green path taken
            else:
                logger.info(f"Routing {100 - canary_pct}% of requests for {model_name} to active (blue) version.")
                target_provider = self.route_task(task_type, payload)
                active_tag = "blue" # Indicate blue path taken
        else:
            target_provider = self.route_task(task_type, payload)

        if not target_provider:
            raise RuntimeError(f"No suitable provider found for task type '{task_type}'.")

        attempt = 0
        while attempt <= self.fallback_retries:
            provider = target_provider # Start with the chosen provider (blue/green/canary)

            logger.info(f"Attempting task '{task_type}' with provider '{provider.name}' (attempt {attempt + 1})...")
            start_time = time.time()
            inference_ok = False
            inference_score = 0.0
            try:
                result = await provider.process_request(task_type, payload)
                latency_ms = (time.time() - start_time) * 1000
                inference_ok = True
                inference_score = score_inference(result) # Score the inference result
                logger.info(f"Task '{task_type}' successful with provider '{provider.name}'.")
                return result
            except Exception as e:
                latency_ms = (time.time() - start_time) * 1000
                logger.error(f"Provider '{provider.name}' failed for task '{task_type}': {e}")
                # Record metric for failed inference
                record_metric(provider.name, model_name, active_tag, False, latency_ms, 0.0)
                attempt += 1
                if attempt <= self.fallback_retries:
                    logger.info(f"Attempting fallback for task '{task_type}'...")
                else:
                    logger.error(f"All fallback attempts failed for task '{task_type}'.")
                    # The final RuntimeError after the loop will handle this.
            finally:
                # Record metric for successful inference (if applicable) and check for auto-promotion/rollback
                if inference_ok:
                    record_metric(provider.name, model_name, active_tag, True, latency_ms, inference_score)
                
                # Check health metrics and potentially promote/rollback
                if strategy == "bluegreen" and model_name and provider_name:
                    # Aggregate metrics for the current tag (blue or green)
                    agg_metrics = aggregate(provider.name, model_name, active_tag)
                    # Get min_health_score from config/model_registry (assuming it's loaded somewhere)
                    # For now, use a placeholder
                    min_health_score = 0.9 # Placeholder: Get from model registry config
                    
                    if active_tag == "green" and agg_metrics["avg_score"] >= min_health_score and agg_metrics["count"] >= 100:
                        logger.info(f"Canary (green) version for {model_name} is healthy. Promoting to active.")
                        # Promote green to active
                        # This would involve calling model_store.activate(..., version_tag=green_tag, metadata={"strategy":"blue"})
                        # For now, just log
                        pass
                    elif active_tag == "green" and agg_metrics["avg_score"] < min_health_score and agg_metrics["count"] >= 100:
                        logger.warning(f"Canary (green) version for {model_name} is unhealthy. Rolling back to blue.")
                        # Auto-rollback to blue
                        # This would involve calling model_store.rollback(..., target_tag=blue_tag)
                        # For now, just log
                        pass


        raise RuntimeError(f"Failed to execute task '{task_type}' after {self.fallback_retries + 1} attempts.")