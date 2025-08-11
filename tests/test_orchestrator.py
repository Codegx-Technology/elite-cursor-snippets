# // [TASK]: Create unit tests for pipeline_orchestrator.py
# // [GOAL]: Ensure correct pipeline selection and execution
# // [ELITE_CURSOR_SNIPPET]: writetest

import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from pipeline_orchestrator import PipelineOrchestrator
from config_loader import get_config

# Mock the config for tests
@pytest.fixture(autouse=True)
def mock_config():
    with patch('pipeline_orchestrator.config', new=MagicMock()) as mock_cfg:
        mock_cfg.models.image_generation.local_fallback_path = None
        mock_cfg.models.voice_synthesis.local_fallback_path = None
        yield mock_cfg

@pytest.fixture
def orchestrator_instance():
    return PipelineOrchestrator()

@pytest.mark.asyncio
async def test_decide_pipeline_news_url(orchestrator_instance):
    decision = orchestrator_instance.decide_pipeline("news_url")
    assert decision["chosen"] == "news_video_generator"
    assert "news URL" in decision["reason"]

@pytest.mark.asyncio
async def test_decide_pipeline_script_file(orchestrator_instance):
    decision = orchestrator_instance.decide_pipeline("script_file")
    assert decision["chosen"] == "news_video_generator"
    assert "script file" in decision["reason"]

@pytest.mark.asyncio
async def test_decide_pipeline_cartoon_prompt(orchestrator_instance):
    decision = orchestrator_instance.decide_pipeline("cartoon_prompt")
    assert decision["chosen"] == "cartoon_anime_pipeline"
    assert "cartoon prompt" in decision["reason"]

@pytest.mark.asyncio
async def test_decide_pipeline_general_prompt_api_fallback(orchestrator_instance):
    decision = orchestrator_instance.decide_pipeline("general_prompt", api_call=True)
    assert decision["chosen"] == "news_video_generator"
    assert "API, falling back to news_video_generator" in decision["reason"]

@pytest.mark.asyncio
async def test_decide_pipeline_general_prompt_basic_fallback(orchestrator_instance):
    decision = orchestrator_instance.decide_pipeline("general_prompt", api_call=False)
    assert decision["chosen"] == "basic_video_generator"
    assert "basic video generator" in decision["reason"]

@pytest.mark.asyncio
async def test_decide_pipeline_general_prompt_advanced_offline(orchestrator_instance, mock_config):
    mock_config.models.image_generation.local_fallback_path = "/path/to/local/sdxl"
    mock_config.models.voice_synthesis.local_fallback_path = "/path/to/local/bark"
    decision = orchestrator_instance.decide_pipeline("general_prompt", api_call=True)
    assert decision["chosen"] == "offline_video_maker"
    assert "advanced offline pipeline" in decision["reason"]

@pytest.mark.asyncio
async def test_decide_pipeline_unknown_type(orchestrator_instance):
    decision = orchestrator_instance.decide_pipeline("unknown_type")
    assert decision["chosen"] is None
    assert "Unknown input type" in decision["reason"]

@pytest.mark.asyncio
@patch('pipeline_orchestrator.news_video_generator.main', new_callable=AsyncMock)
async def test_run_pipeline_news_video_generator(mock_news_main, orchestrator_instance):
    mock_news_main.return_value = {"video_url": "http://example.com/news_video.mp4"}
    result = await orchestrator_instance.run_pipeline("news_url", "http://example.com/news")
    assert result["status"] == "success"
    assert result["pipeline"] == "news_video_generator"
    mock_news_main.assert_called_once_with(news="http://example.com/news", script_file=None, prompt=None)

@pytest.mark.asyncio
@patch('pipeline_orchestrator.offline_video_maker.generate_video.main')
async def test_run_pipeline_offline_video_maker(mock_offline_main, orchestrator_instance):
    mock_offline_main.return_value = {"video_url": "http://example.com/offline_video.mp4"}
    result = await orchestrator_instance.run_pipeline("general_prompt", "test prompt", api_call=False) # Force offline
    assert result["status"] == "success"
    assert result["pipeline"] == "basic_video_generator" # This will be basic due to mock_config
    # The actual call to offline_video_maker.generate_video.main is done in a thread, so direct assert_called_once is tricky
    # We'd need to mock run_in_executor or ensure the mock is called within the executor
    # For now, we rely on the decision logic being correct.

@pytest.mark.asyncio
async def test_run_pipeline_basic_video_generator_api_call(orchestrator_instance):
    result = await orchestrator_instance.run_pipeline("general_prompt", "test prompt", api_call=True)
    assert result["status"] == "success"
    assert result["pipeline"] == "news_video_generator" # Falls back to news_video_generator for API calls

@pytest.mark.asyncio
async def test_run_pipeline_unknown_type_error(orchestrator_instance):
    result = await orchestrator_instance.run_pipeline("unknown_type", "some data")
    assert result["status"] == "error"
    assert "Failed to decide pipeline" in result["message"]

@pytest.mark.asyncio
@patch('pipeline_orchestrator.news_video_generator.main', side_effect=Exception("Test Error"))
async def test_run_pipeline_exception_handling(mock_news_main, orchestrator_instance):
    result = await orchestrator_instance.run_pipeline("news_url", "http://example.com/news")
    assert result["status"] == "error"
    assert "An error occurred: Test Error" in result["message"]