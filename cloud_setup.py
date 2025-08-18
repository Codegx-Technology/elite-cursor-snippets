import logging
from backend.ai_routing.router import Router
from backend.ai_routing.providers.base_provider import BaseProvider
from typing import List

logger = logging.getLogger(__name__)

def configure_providers() -> Tuple[Router, List[BaseProvider]]: # Return Router instance and providers
    """
    // [TASK]: Configure and return the Router instance and a list of initialized AI service providers.
    // [GOAL]: Centralize provider setup for auto-deploy and registration.
    // [ELITE_CURSOR_SNIPPET]: clouddeploy
    """
    logger.info("Configuring AI service providers...")
    # Assuming the main config file for the router is at backend/ai_routing/config.yaml
    router = Router(config_path="backend/ai_routing/config.yaml")
    
    # The router's __init__ method already dynamically loads and registers providers
    # based on the config. So, we just need to return the list of registered providers.
    
    configured_providers = list(router.providers.values())
    logger.info(f"Successfully configured {len(configured_providers)} providers.")
    return router, configured_providers # Return router and providers