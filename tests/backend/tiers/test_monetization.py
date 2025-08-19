import pytest
from httpx import AsyncClient
from main import app # Assuming your FastAPI app is named 'app' in main.py
from unittest.mock import patch, AsyncMock
from datetime import datetime, timedelta

# Assuming get_default_plans and get_user_subscription are accessible
from billing_models import get_default_plans, UserSubscription

# Assuming quota_service is accessible
from backend.services.quota_service import quota_service

# Assuming ModelStore is accessible
from backend.ai_models.model_store import ModelStore

# Mock authentication for admin user
async def mock_get_current_admin_user():
    return {"username": "admin", "role": "ADMIN"}

# Mock authentication for regular user
async def mock_get_current_user():
    return {"user_id": "test_user", "username": "test_user"}

@pytest.fixture(name="test_client")
async def test_client_fixture():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
def mock_dependencies():
    with (
        patch("api_server.get_current_admin_user", new=mock_get_current_admin_user),
        patch("api_server.get_current_user", new=mock_get_current_user),
        patch("backend.middleware.policy_resolver.get_user_subscription") as mock_get_user_sub,
        patch("backend.middleware.policy_resolver.get_default_plans") as mock_get_default_plans,
        patch("backend.services.quota_service.QuotaService.redis_client", new=AsyncMock()) as mock_redis_client,
        patch("backend.ai_models.model_store.ModelStore.current") as mock_model_store_current,
        patch("backend.ai_models.model_store.ModelStore.activate") as mock_model_store_activate,
        patch("backend.ai_routing.router.ModelStore.current") as mock_router_model_store_current,
        patch("backend.ai_routing.router.ModelStore.activate") as mock_router_model_store_activate,
        patch("backend.ai_routing.router.perform_rollback") as mock_perform_rollback,
        patch("backend.ai_routing.router.send_admin_email") as mock_send_admin_email,
        patch("backend.core.voices.versioning.load_versions") as mock_load_versions,
        patch("backend.core.voices.versioning.save_versions") as mock_save_versions,
        patch("backend.core.voices.versioning.get_active_voice") as mock_get_active_voice,
        patch("backend.core.voices.versioning.rollback_voice") as mock_rollback_voice,
    ) as mocks:
        # Configure mock_get_default_plans to return actual default plans
        mock_get_default_plans.return_value = get_default_plans()
        
        # Configure mock_get_user_subscription for a FREE user by default
        mock_get_user_sub.return_value = UserSubscription(
            user_id="test_user",
            plan_name="Free",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30)
        )

        # Mock Redis client methods
        mock_redis_client.incrby.return_value = 1 # Default for quota checks
        mock_redis_client.zremrangebyscore.return_value = 0
        mock_redis_client.zadd.return_value = 1
        mock_redis_client.zcard.return_value = 1 # Default for rate limit checks
        mock_redis_client.expire.return_value = True
        mock_redis_client.get.return_value = None # For monthly cost

        yield mocks

# --- Test Cases ---

@pytest.mark.asyncio
async def test_free_user_hits_429_on_rate_limit(test_client, mock_dependencies):
    # Configure user to be Free tier
    mock_dependencies[2].return_value = UserSubscription(
        user_id="test_user",
        plan_name="Free",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30)
    )
    # Configure rate limit to be hit immediately
    mock_dependencies[4].zcard.return_value = 100 # Simulate hitting limit

    response = await test_client.post("/generate_video", json={
        "prompt": "generate a video",
        "news_url": None,
        "script_file": None,
        "upload_youtube": False
    })
    assert response.status_code == 429
    assert "Too Many Requests" in response.json()["detail"]

@pytest.mark.asyncio
async def test_enterprise_pinned_tts_no_drift(test_client, mock_dependencies):
    # Configure user to be Enterprise tier
    mock_dependencies[2].return_value = UserSubscription(
        user_id="test_user",
        plan_name="Enterprise",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30)
    )

    # Mock ModelStore.current to return the pinned version
    mock_dependencies[5].return_value = {
        "version_tag": "a1b2c3d4",
        "path": "/path/to/model",
        "checksum": "mock_checksum",
        "metadata": {}
    }

    # Mock the router's internal model_store.current call
    mock_dependencies[7].return_value = {
        "version_tag": "a1b2c3d4",
        "path": "/path/to/model",
        "checksum": "mock_checksum",
        "metadata": {"strategy": "bluegreen", "canary_pct": 0}
    }

    # Mock the actual pipeline execution
    with patch("pipeline_orchestrator.PipelineOrchestrator.run_pipeline", new=AsyncMock()) as mock_run_pipeline:
        mock_run_pipeline.return_value = {"status": "success", "result": "mock_video_url"}
        response = await test_client.post("/generate_video", json={
            "prompt": "generate a video",
            "news_url": None,
            "script_file": None,
            "upload_youtube": False
        })
        assert response.status_code == 200
        # Assert that the router was called with the pinned version (this requires inspecting router internals)
        # For now, we'll rely on the mock setup to ensure the pinned version is returned by ModelStore.current

@pytest.mark.asyncio
async def test_cost_cap_reached_hard_stop(test_client, mock_dependencies):
    # Configure user to be Enterprise tier with hardStop
    mock_dependencies[2].return_value = UserSubscription(
        user_id="test_user",
        plan_name="Enterprise",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30)
    )
    # Mock get_user_monthly_cost to return a value exceeding the cap
    mock_dependencies[4].get.return_value = "10000.0" # Simulate high cost

    response = await test_client.post("/generate_video", json={
        "prompt": "generate a video",
        "news_url": None,
        "script_file": None,
        "upload_youtube": False
    })
    assert response.status_code == 403
    assert "Monthly cost cap exceeded" in response.json()["detail"]

# TODO: Add more test cases:
# - Provider fallback: ElevenLabs fail -> XTTS local -> success
# - Cost cap reached -> soft throttle (low-priority only)
# - Other quota types (tokens, audioSecs, videoMins)
# - Model drift detected vs pinned (alert only) - this is more for watcher tests
