import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import random
from collections import Counter
from pathlib import Path

# Adjust import paths if necessary
from backend.ai_routing.router import Router
from backend.ai_models.model_store import ModelStore
from backend.ai_health.healthcheck import record_metric, aggregate, score_inference

# Mock the config for the Router
@pytest.fixture
def mock_router_config():
    mock_config = MagicMock()
    mock_config.routing_rules = {
        "test_task": MagicMock(priority=["test_provider"])
    }
    mock_config.providers = {
        "test_provider": MagicMock(type="huggingface", name="test_provider")
    }
    mock_config.get.side_effect = lambda key, default: {
        'health_check_interval': 30,
        'fallback_retries': 2
    }.get(key, default)
    
    # Mock config.models for min_health_score access
    mock_config.models.image_generation.min_health_score = 0.9
    return mock_config

# Mock ModelStore and healthcheck functions
@pytest.fixture(autouse=True)
def mock_dependencies_for_canary(monkeypatch):
    mock_model_store = MagicMock(spec=ModelStore)
    mock_model_store.current.return_value = None # Default: no active model info
    monkeypatch.setattr("backend.ai_routing.router.model_store", mock_model_store)

    mock_record_metric = MagicMock()
    mock_aggregate = MagicMock()
    mock_score_inference = MagicMock(return_value=1.0) # Default to perfect score

    monkeypatch.setattr("backend.ai_health.healthcheck.record_metric", mock_record_metric)
    monkeypatch.setattr("backend.ai_health.healthcheck.aggregate", mock_aggregate)
    monkeypatch.setattr("backend.ai_health.healthcheck.score_inference", mock_score_inference)
    
    return mock_model_store, mock_record_metric, mock_aggregate, mock_score_inference

@pytest.fixture
def router_instance(mock_router_config):
    # Create a dummy config file for the Router to load
    config_content = """
routing_rules:
  test_task:
    priority: ["test_provider"]
providers:
  test_provider:
    type: "huggingface"
    name: "test_provider"
"""
    config_path = Path("test_router_config.yaml")
    config_path.write_text(config_content)
    
    router = Router(str(config_path))
    
    # Mock the provider instance within the router
    mock_provider = AsyncMock()
    mock_provider.name = "test_provider"
    mock_provider.is_healthy = True
    mock_provider.latency = 100
    mock_provider.process_request.return_value = {"status": "success", "content": "generated"}
    router.providers["test_provider"] = mock_provider
    
    yield router
    config_path.unlink() # Clean up dummy config file

@pytest.mark.asyncio
async def test_canary_routing_percentage(router_instance, mock_dependencies_for_canary):
    mock_model_store, mock_record_metric, mock_aggregate, _ = mock_dependencies_for_canary
    
    provider_name = "test_provider"
    model_name = "test_model"
    canary_pct = 10 # 10% of requests to green
    num_requests = 5000
    
    # Mock model_store.current to return metadata indicating blue/green with canary
    mock_model_store.current.return_value = {
        "version_tag": "blue_v1",
        "metadata": {
            "strategy": "bluegreen",
            "canary_pct": canary_pct,
            "green_version_tag": "green_v1" # Ensure green_version_tag is present
        }
    }
    
    # Mock aggregate to always return healthy metrics for green
    mock_aggregate.return_value = {
        "avg_score": 0.95,
        "count": 100,
        "error_rate": 0.01,
        "p50_latency_ms": 500
    }

    # Seed random for deterministic testing
    random.seed(42)
    
    routed_tags = []
    for _ in range(num_requests):
        # Mock random.randint to control routing
        # If random.randint(1, 100) <= canary_pct, it's green
        # Else, it's blue
        with patch('random.randint', return_value=random.randint(1, 100)):
            result = await router_instance.execute_with_fallback("test_task", {"model_name": model_name, "provider_name": provider_name})
            # The active_tag is set within execute_with_fallback
            # We need to inspect the mock_record_metric calls to see which tag was used
            # Or, we can modify the router to return the active_tag for testing purposes
            # For now, let's rely on inspecting the mock_record_metric calls
            
            # A simpler way for testing canary routing is to mock the internal random.randint
            # and then check the logic that uses it.
            # Since execute_with_fallback doesn't return the active_tag, we'll count
            # how many times the green path is taken by inspecting the mock_record_metric calls.
            pass # The actual routing happens inside execute_with_fallback

    # After all requests, inspect the calls to record_metric
    blue_count = 0
    green_count = 0
    for call_args in mock_record_metric.call_args_list:
        args, kwargs = call_args
        tag = args[2] # The third argument is the tag
        if tag == "green":
            green_count += 1
        elif tag == "blue":
            blue_count += 1
    
    total_routed = blue_count + green_count
    
    # Calculate observed percentages
    observed_canary_pct = (green_count / total_routed) * 100 if total_routed > 0 else 0
    observed_blue_pct = (blue_count / total_routed) * 100 if total_routed > 0 else 0

    # Check if observed percentages are within tolerance
    tolerance = 2 # ±2%
    assert canary_pct - tolerance <= observed_canary_pct <= canary_pct + tolerance
    assert (100 - canary_pct) - tolerance <= observed_blue_pct <= (100 - canary_pct) + tolerance
    
    print(f"Observed Canary %: {observed_canary_pct:.2f}% (Expected: {canary_pct}%) ")
    print(f"Observed Blue %: {observed_blue_pct:.2f}% (Expected: {100 - canary_pct}%) ")
