import asyncio
import unittest
import os
import sys
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

# Add the project root to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from backend.ai_routing.providers.colab_provider import ColabProvider
from backend.ai_routing.providers.kaggle_provider import KaggleProvider
from backend.ai_routing.providers.huggingface_provider import HuggingFaceProvider
from backend.ai_routing.providers.runpod_provider import RunPodProvider
from backend.ai_routing.providers.gemini_provider import GeminiProvider

class TestProviderIntegrations(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # [SNIPPET]: thinkwithai + kenyafirst + enterprise-secure
        # [CONTEXT]: Loading mock API key from environment variables for tests.
        # [GOAL]: Eliminate hardcoded credentials in test files.
        # [TASK]: Replace hardcoded mock_key with an environment variable lookup.
        mock_api_key = os.getenv("MOCK_API_KEY", "mock_key_if_not_set")
        self.mock_config = {"api_endpoint": "http://mock.api/v1", "api_key": mock_api_key, "model_id": "mock_model", "endpoint_id": "mock_endpoint"}
        self.test_payload = {"prompt": "Generate a test response"}

    async def test_colab_provider(self):
        provider = ColabProvider("test_colab", self.mock_config)
        self.assertTrue(await provider.check_health())
        result = await provider.process_request("text_generation", self.test_payload)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["provider"], "test_colab")

    async def test_kaggle_provider(self):
        provider = KaggleProvider("test_kaggle", self.mock_config)
        self.assertTrue(await provider.check_health())
        result = await provider.process_request("image_generation", self.test_payload)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["provider"], "test_kaggle")

    async def test_huggingface_provider(self):
        provider = HuggingFaceProvider("test_huggingface", self.mock_config)
        self.assertTrue(await provider.check_health())
        result = await provider.process_request("text_generation", self.test_payload)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["provider"], "test_huggingface")

    async def test_runpod_provider(self):
        provider = RunPodProvider("test_runpod", self.mock_config)
        self.assertTrue(await provider.check_health())
        result = await provider.process_request("video_generation", self.test_payload)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["provider"], "test_runpod")

    async def test_gemini_provider(self):
        provider = GeminiProvider("test_gemini", self.mock_config)
        self.assertTrue(await provider.check_health())
        result = await provider.process_request("text_generation", self.test_payload)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["provider"], "test_gemini")

if __name__ == "__main__":
    unittest.main()