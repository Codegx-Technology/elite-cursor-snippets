import asyncio
import unittest
import os
import sys
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

# Add the project root to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".")))

from backend.ai_routing.router import Router
from backend.ai_routing.providers.base_provider import BaseProvider
from backend.ai_routing.providers.openai_provider import OpenAIProvider
from backend.ai_routing.providers.anthropic_provider import AnthropicProvider

class MockProvider(BaseProvider):
    async def process_request(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"provider": self.name, "task_type": task_type, "response": "Mocked response"}
    async def check_health(self) -> bool:
        return True

# Mock config file path
MOCK_CONFIG_PATH = "backend/ai_routing/test_config.yaml"

# Helper to create a mock config file
def create_mock_config(content: str):
    with open(MOCK_CONFIG_PATH, "w") as f:
        f.write(content)

# Helper to clean up mock config file
def cleanup_mock_config():
    if os.path.exists(MOCK_CONFIG_PATH):
        os.remove(MOCK_CONFIG_PATH)

class TestRouter(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Ensure clean state before each test
        cleanup_mock_config()
        self.mock_config_content = """
health_check_interval: 1
fallback_retries: 1
providers:
  mock_openai:
    type: openai
    api_key: mock_key_openai
    fail_rate: 0.0
    unhealth_rate: 0.0
  mock_anthropic:
    type: anthropic
    api_key: mock_key_anthropic
    fail_rate: 0.0
    unhealth_rate: 0.0
  mock_unhealthy:
    type: mock
    api_key: mock_key_unhealthy
    fail_rate: 0.0
    unhealth_rate: 1.0 # Always unhealthy
routing_rules:
  test_task:
    priority: ["mock_openai", "mock_anthropic"]
  fallback_task:
    priority: ["mock_unhealthy", "mock_openai"]
  no_provider_task:
    priority: ["non_existent_provider"]
"""
        create_mock_config(self.mock_config_content)
        self.router = Router(MOCK_CONFIG_PATH)

        # Register mock providers
        # In a real scenario, these would be instantiated based on config.providers
        # For this example, we manually instantiate mock providers
        self.mock_openai_provider = OpenAIProvider("mock_openai", self.router.config.providers.mock_openai)
        self.mock_anthropic_provider = AnthropicProvider("mock_anthropic", self.router.config.providers.mock_anthropic)
        
        # Mock check_health and process_request for controlled testing
        self.mock_openai_provider.check_health = AsyncMock(return_value=True)
        self.mock_openai_provider.process_request = AsyncMock(return_value={"status": "success", "provider": "mock_openai"})
        
        self.mock_anthropic_provider.check_health = AsyncMock(return_value=True)
        self.mock_anthropic_provider.process_request = AsyncMock(return_value={"status": "success", "provider": "mock_anthropic"})

        self.router.register_provider(self.mock_openai_provider)
        self.router.register_provider(self.mock_anthropic_provider)
        self.mock_unhealthy_provider = MockProvider("mock_unhealthy", self.router.config.providers.mock_unhealthy)
        self.router.register_provider(self.mock_unhealthy_provider)

        # Start health monitoring in background for tests that need it
        self.health_monitor_task = asyncio.create_task(self.router.start_health_monitoring())
        await asyncio.sleep(self.router.health_check_interval + 0.1) # Give time for initial health check

    async def asyncTearDown(self):
        self.health_monitor_task.cancel()
        try:
            await self.health_monitor_task
        except asyncio.CancelledError:
            pass
        cleanup_mock_config()

    # --- Test load_config ---
    def test_load_config_success(self):
        self.assertIsNotNone(self.router.config)
        self.assertEqual(self.router.config.health_check_interval, 1)
        self.assertEqual(self.router.config.fallback_retries, 1)
        self.assertIn("mock_openai", self.router.config.providers)

    def test_load_config_file_not_found(self):
        cleanup_mock_config() # Remove the existing mock config
        with self.assertRaises(FileNotFoundError):
            Router("non_existent_config.yaml")

    # --- Test register_provider ---
    def test_register_provider(self):
        self.assertIn("mock_openai", self.router.providers)
        self.assertEqual(self.router.providers["mock_openai"].name, "mock_openai")

    # --- Test _perform_health_check ---
    async def test_perform_health_check_healthy(self):
        self.mock_openai_provider.check_health.return_value = True
        await self.router._perform_health_check(self.mock_openai_provider)
        self.assertTrue(self.mock_openai_provider.is_healthy)
        self.assertLess(self.mock_openai_provider.latency, float('inf'))

    async def test_perform_health_check_unhealthy(self):
        self.mock_openai_provider.check_health.return_value = False
        await self.router._perform_health_check(self.mock_openai_provider)
        self.assertFalse(self.mock_openai_provider.is_healthy)
        self.assertEqual(self.mock_openai_provider.latency, float('inf'))

    async def test_perform_health_check_exception(self):
        self.mock_openai_provider.check_health.side_effect = Exception("API error")
        await self.router._perform_health_check(self.mock_openai_provider)
        self.assertFalse(self.mock_openai_provider.is_healthy)
        self.assertEqual(self.mock_openai_provider.latency, float('inf'))

    # --- Test route_task ---
    async def test_route_task_normal(self):
        # All healthy, should pick mock_openai (first in priority)
        provider = self.router.route_task("test_task", {})
        self.assertEqual(provider.name, "mock_openai")

    async def test_route_task_fallback_due_to_unhealthy(self):
        # mock_openai is unhealthy, should pick mock_anthropic
        self.mock_openai_provider.is_healthy = False
        provider = self.router.route_task("test_task", {})
        self.assertEqual(provider.name, "mock_anthropic")
        self.mock_openai_provider.is_healthy = True # Reset

    async def test_route_task_no_rules(self):
        provider = self.router.route_task("non_existent_task", {})
        self.assertIsNone(provider)

    async def test_route_task_no_healthy_providers(self):
        self.mock_openai_provider.is_healthy = False
        self.mock_anthropic_provider.is_healthy = False
        provider = self.router.route_task("test_task", {})
        self.assertIsNone(provider)
        self.mock_openai_provider.is_healthy = True # Reset
        self.mock_anthropic_provider.is_healthy = True # Reset

    async def test_route_task_sort_by_latency(self):
        self.mock_openai_provider.latency = 100
        self.mock_anthropic_provider.latency = 50
        provider = self.router.route_task("test_task", {})
        self.assertEqual(provider.name, "mock_anthropic") # Anthropic is faster
        self.mock_openai_provider.latency = float('inf') # Reset
        self.mock_anthropic_provider.latency = float('inf') # Reset

    # --- Test execute_with_fallback ---
    async def test_execute_with_fallback_success_first_attempt(self):
        result = await self.router.execute_with_fallback("test_task", {"prompt": "initial request"})
        self.assertEqual(result["provider"], "mock_openai")
        self.mock_openai_provider.process_request.assert_called_once()

    async def test_execute_with_fallback_success_after_fallback(self):
        # For 'fallback_task', priority is mock_unhealthy, then mock_openai.
        # So, if mock_unhealthy is unhealthy, it will try mock_openai.
        # We need to ensure mock_unhealthy is unhealthy.
        mock_unhealthy_provider = self.router.providers["mock_unhealthy"]
        mock_unhealthy_provider.is_healthy = False # Manually set for this test

        # We want mock_openai to fail once, then succeed on retry.
        self.mock_openai_provider.process_request.side_effect = [
            Exception("Simulated OpenAI failure"),
            {"status": "success", "provider": "mock_openai_fallback"}
        ]
        
        result = await self.router.execute_with_fallback("fallback_task", {"prompt": "fallback request"})
        self.assertEqual(result["provider"], "mock_openai_fallback")
        self.assertEqual(self.mock_openai_provider.process_request.call_count, 2) # Called once, failed, called again, succeeded

    async def test_execute_with_fallback_all_attempts_fail(self):
        async def raise_connection_error(*args, **kwargs):
            raise ConnectionError("Simulated persistent connection error")

        # Set side_effect to a list of coroutines that raise exceptions
        self.mock_openai_provider.process_request.side_effect = [raise_connection_error for _ in range(self.router.fallback_retries + 1)]
        self.mock_anthropic_provider.process_request.side_effect = [raise_connection_error for _ in range(self.router.fallback_retries + 1)]

        with self.assertRaises(RuntimeError) as cm:
            await self.router.execute_with_fallback("test_task", {"prompt": "failing request"})
        self.assertIn("Failed to execute task 'test_task' after", str(cm.exception))
        # Assert that process_request was called the expected number of times for each provider
        self.assertEqual(self.mock_openai_provider.process_request.call_count, self.router.fallback_retries + 1)
        self.assertEqual(self.mock_anthropic_provider.process_request.call_count, self.router.fallback_retries + 1)

    async def test_execute_with_fallback_no_suitable_provider(self):
        # Ensure no healthy providers for this task type
        self.mock_openai_provider.is_healthy = False
        self.mock_anthropic_provider.is_healthy = False
        
        with self.assertRaises(RuntimeError) as cm:
            await self.router.execute_with_fallback("test_task", {"prompt": "no provider request"})
        self.assertIn("No suitable provider found for task type 'test_task'", str(cm.exception))
        self.assertEqual(self.mock_openai_provider.process_request.call_count, 0)
        self.assertEqual(self.mock_anthropic_provider.process_request.call_count, 0)

if __name__ == "__main__":
    unittest.main()