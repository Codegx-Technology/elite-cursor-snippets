from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

from logging_setup import get_logger
from config_loader import get_config

logger = get_logger(__name__)
config = get_config()

app = FastAPI(
    title=config.app.name,
    version=config.app.version,
    description="API for Shujaa Studio - Enterprise AI Video Generation"
)

class GenerateVideoRequest(BaseModel):
    prompt: str
    news_url: Optional[str] = None
    script_file: Optional[str] = None
    upload_youtube: bool = False

@app.get("/health")
async def health_check():
    """
    // [TASK]: Health check endpoint
    // [GOAL]: Verify API server is running
    """
    logger.info("Health check requested.")
    return {"status": "ok", "message": "Shujaa Studio API is running!"}

@app.post("/generate_video")
async def generate_video_endpoint(request: GenerateVideoRequest):
    """
    // [TASK]: Video generation endpoint
    // [GOAL]: Expose video generation pipeline via API
    """
    logger.info(f"Video generation request received: {request.dict()}")
    
    # This is a placeholder. In a real scenario, this would call
    # the pipeline_orchestrator or news_video_generator directly.
    # For now, just simulate success.
    
    if not request.prompt and not request.news_url and not request.script_file:
        raise HTTPException(status_code=400, detail="Either 'prompt', 'news_url', or 'script_file' must be provided.")

    # Simulate processing time
    await asyncio.sleep(2) 

    logger.info("Video generation simulated successfully.")
    return {"status": "success", "video_id": "simulated_video_123", "message": "Video generation request received and processing (simulated)."}

if __name__ == "__main__":
    # To run this server, use: uvicorn api_server:app --reload --port 8000
    # Or programmatically:
    uvicorn.run(app, host="0.0.0.0", port=8000)
