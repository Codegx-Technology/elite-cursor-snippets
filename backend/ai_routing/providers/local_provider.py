from typing import Dict, Any
import httpx # Using httpx for async HTTP requests
import logging

from backend.ai_routing.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)

class LocalProvider(BaseProvider):
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.endpoint_url = config.get("endpoint_url")
        if not self.endpoint_url:
            raise ValueError(f"LocalProvider '{name}' requires 'endpoint_url' in its configuration.")
        self.client = httpx.AsyncClient() # Initialize async HTTP client
        logger.info(f"LocalProvider '{name}' initialized with endpoint: {self.endpoint_url}")

    async def process_request(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a request to the local model serving endpoint.
        """
        try:
            # Assuming the local endpoint expects a JSON payload
            response = await self.client.post(f"{self.endpoint_url}/{task_type}", json=payload)
            response.raise_for_status() # Raise an exception for 4xx or 5xx responses
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"LocalProvider '{self.name}' RequestError for {task_type}: {e}")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"LocalProvider '{self.name}' HTTPStatusError for {task_type}: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"LocalProvider '{self.name}' unexpected error for {task_type}: {e}")
            raise

    async def check_health(self) -> bool:
        """
        Checks the health of the local model serving endpoint.
        """
        try:
            response = await self.client.get(f"{self.endpoint_url}/health")
            response.raise_for_status()
            return response.status_code == 200 and response.json().get("status") == "ok"
        except httpx.RequestError as e:
            logger.warning(f"LocalProvider '{self.name}' health check failed: {e}")
            return False
        except Exception as e:
            logger.error(f"LocalProvider '{self.name}' unexpected error during health check: {e}")
            return False
