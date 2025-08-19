import yaml
from pathlib import Path
from typing import Dict, Any
from logging_setup import get_logger

logger = get_logger(__name__)

class ProviderCosts:
    def __init__(self, config_path: str = "provider_costs.yml"):
        self.config_path = Path(config_path)
        self._costs: Dict[str, Any] = {}
        self._load_costs()

    def _load_costs(self):
        if not self.config_path.exists():
            logger.error(f"Provider costs configuration file not found at {self.config_path}")
            return
        try:
            with open(self.config_path, 'r') as f:
                self._costs = yaml.safe_load(f)
            logger.info(f"Loaded provider costs from {self.config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing provider costs YAML from {self.config_path}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred loading provider costs from {self.config_path}: {e}")

    def get_cost(self, provider: str, metric: str) -> float:
        """
        Retrieves the cost for a given provider and metric.
        Returns 0.0 if not found.
        """
        return self._costs.get(provider, {}).get(metric, 0.0)

# Initialize the provider costs service
provider_costs_service = ProviderCosts()
