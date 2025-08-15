import abc
from typing import Any, Dict, List, Optional

class BaseProvider(abc.ABC):
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.is_healthy = True # Assume healthy until health check fails
        self.latency = float('inf') # Assume infinite latency until measured

    @abc.abstractmethod
    async def process_request(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Processes a request using the provider's API."""
        pass

    @abc.abstractmethod
    async def check_health(self) -> bool:
        """Checks the health and latency of the provider."""
        pass

    def __str__(self):
        return f"Provider(name={self.name}, healthy={self.is_healthy}, latency={self.latency:.2f}ms)"

    def __repr__(self):
        return self.__str__()