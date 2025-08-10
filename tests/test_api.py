import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

# It's important to import the app object from the main script
# As the tests directory is a sibling of api_server.py, we need to adjust the path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api_server import app, get_current_user 

# A mock user payload for dependency injection
MOCK_USER_PAYLOAD = {"user_id": 1, "username": "testuser", "tenant_id": 1}

# Override the dependency for getting the current user
async def override_get_current_user():
    return MOCK_USER_PAYLOAD

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def mock_orchestrator():
    """Mocks the pipeline orchestrator to avoid running real pipelines."""
    with patch("api_server.orchestrator.run_pipeline", new_callable=AsyncMock) as mock_run:
        # Configure the mock to return a successful response
        mock_run.return_value = {
            "status": "success",
            "pipeline": "mock_pipeline",
            "result": {"video_path": "/fake/video.mp4"}
        }
        yield mock_run

def test_health_check():
    """Tests the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Shujaa Studio API is running!"}

def test_generate_single_video(mock_orchestrator):
    """Tests the /generate_video endpoint with a mocked orchestrator."""
    response = client.post("/generate_video", json={"prompt": "test prompt"})
    assert response.status_code == 200
    mock_orchestrator.assert_called_once()
    assert response.json()["status"] == "success"

def test_batch_generate_video(mock_orchestrator):
    """Tests the /batch_generate_video endpoint."""
    payload = {
        "requests": [
            {"prompt": "first prompt"},
            {"prompt": "second prompt"}
        ]
    }
    response = client.post("/batch_generate_video", json=payload)
    
    assert response.status_code == 200
    # The orchestrator should have been called twice, once for each item in the batch
    assert mock_orchestrator.call_count == 2
    
    response_data = response.json()
    assert response_data["status"] == "completed"
    assert response_data["successful_videos"] == 2
    assert response_data["failed_videos"] == 0
    assert len(response_data["results"]) == 2
    assert response_data["results"][0]["status"] == "success"

def test_batch_generate_video_exceeds_limit(mock_orchestrator):
    """Tests that the batch endpoint rejects requests that are too large."""
    # Create a payload with more requests than the default limit (10)
    payload = {
        "requests": [{"prompt": f"prompt {i}"} for i in range(15)]
    }
    response = client.post("/batch_generate_video", json=payload)
    
    assert response.status_code == 400
    assert "Batch size cannot exceed" in response.json()["detail"]
    # The orchestrator should not have been called at all
    mock_orchestrator.assert_not_called()
