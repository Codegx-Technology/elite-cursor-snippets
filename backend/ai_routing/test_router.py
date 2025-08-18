import asyncio
import logging
from backend.ai_routing.router import Router
from backend.ai_routing.providers.openai_provider import OpenAIProvider
from backend.ai_routing.providers.anthropic_provider import AnthropicProvider

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    config_path = "backend/ai_routing/config.yaml"
    router = Router(config_path)

    # Register providers
    # In a real scenario, these would be instantiated based on config.providers
    # For this example, we manually instantiate mock providers
    openai_config = router.config.providers.openai
    router.register_provider(OpenAIProvider("openai", openai_config))

    anthropic_config = router.config.providers.anthropic
    router.register_provider(AnthropicProvider("anthropic", anthropic_config))

    # Start health monitoring in the background
    asyncio.create_task(router.start_health_monitoring())

    # Give some time for initial health checks to run
    logger.info("Waiting for initial health checks...")
    await asyncio.sleep(router.health_check_interval + 1) # Wait for one cycle + a bit

    # --- Test Scenarios ---

    # Scenario 1: Normal execution (text_completion)
    logger.info("\n--- Scenario 1: Normal execution (text_completion) ---")
    try:
        result = await router.execute_with_fallback("text_completion", {"prompt": "Hello world"})
        logger.info(f"Result: {result}")
    except Exception as e:
        logger.error(f"Scenario 1 failed: {e}")

    # Scenario 2: Simulate preferred provider failure and test fallback
    logger.info("\n--- Scenario 2: Simulate preferred provider failure (summarization) ---")
    # Temporarily mark Anthropic (preferred for summarization) as unhealthy
    if "anthropic" in router.providers:
        router.providers["anthropic"].is_healthy = False
        logger.warning("Simulating Anthropic provider as unhealthy.")
    try:
        result = await router.execute_with_fallback("summarization", {"text": "Long document to summarize"})
        logger.info(f"Result: {result}")
    except Exception as e:
        logger.error(f"Scenario 2 failed: {e}")
    finally:
        # Reset health for future tests
        if "anthropic" in router.providers:
            router.providers["anthropic"].is_healthy = True

    # Scenario 3: Task type with no healthy providers
    logger.info("\n--- Scenario 3: No healthy providers for task type (image_generation) ---")
    # Temporarily mark all image_generation providers as unhealthy
    if "huggingface" in router.providers:
        router.providers["huggingface"].is_healthy = False
    if "openai" in router.providers:
        router.providers["openai"].is_healthy = False
    try:
        result = await router.execute_with_fallback("image_generation", {"description": "A cat on the moon"})
        logger.info(f"Result: {result}")
    except Exception as e:
        logger.error(f"Scenario 3 failed as expected: {e}")
    finally:
        # Reset health
        if "huggingface" in router.providers:
            router.providers["huggingface"].is_healthy = True
        if "openai" in router.providers:
            router.providers["openai"].is_healthy = True

    logger.info("\n--- All scenarios completed ---")
    # Allow health monitoring to run for a bit more if needed for observation
    await asyncio.sleep(router.health_check_interval + 1)


if __name__ == "__main__":
    asyncio.run(main())
