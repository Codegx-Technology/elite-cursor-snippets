#!/usr/bin/env python3
"""
simple_api.py
Simple FastAPI endpoint for Shujaa Studio
Following elite-cursor-snippets patterns for Kenya-specific requirements

// [TASK]: Create simple FastAPI endpoint
// [GOAL]: Minimal API for video generation
// [SNIPPET]: surgicalfix + refactorclean + kenyafirst
// [CONTEXT]: Production-ready API for Astella integration
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pipeline_wrapper as pw
import uvicorn
import os
import uuid
import yaml
from typing import Optional, Dict, Any

# Load config
def load_config() -> Dict[str, Any]:
    """Load configuration"""
    try:
        with open("config.yaml", 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception:
        return {
            "api_host": "0.0.0.0",
            "api_port": 8000,
            "work_base": "./outputs"
        }

config = load_config()

# Create FastAPI app
app = FastAPI(
    title="Shujaa Studio API",
    description="Simple API for AI video generation",
    version="1.0.0"
)

# Request/Response models
class VideoRequest(BaseModel):
    prompt: str
    scenes: Optional[int] = None
    vertical: Optional[bool] = None
    lang: str = "sheng"
    user_id: Optional[str] = None

class VideoResponse(BaseModel):
    status: str
    video_path: str
    message: str

class BatchRequest(BaseModel):
    csv_path: str
    output_dir: Optional[str] = None

class BatchResponse(BaseModel):
    status: str
    output_dir: str
    message: str

# Health check
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Shujaa Studio API - AI Video Generation",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "shujaa-studio-api",
        "config_loaded": bool(config)
    }

# Video generation endpoint
@app.post("/generate", response_model=VideoResponse)
async def generate_video(req: VideoRequest):
    """
    Generate AI video from prompt
    
    Args:
        req: Video generation request
        
    Returns:
        VideoResponse: Generation result
    """
    try:
        # Generate video using pipeline wrapper
        video_path = pw.generate(
            prompt=req.prompt,
            scenes=req.scenes,
            vertical=req.vertical,
            lang=req.lang
        )
        
        # Convert to absolute path for API response
        abs_path = os.path.abspath(video_path)
        
        return VideoResponse(
            status="success",
            video_path=abs_path,
            message="Video generated successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Video generation failed: {str(e)}"
        )

# Batch generation endpoint
@app.post("/batch", response_model=BatchResponse)
async def batch_generate(req: BatchRequest):
    """
    Generate multiple videos from CSV
    
    Args:
        req: Batch generation request
        
    Returns:
        BatchResponse: Batch result
    """
    try:
        # Check if CSV file exists
        if not os.path.exists(req.csv_path):
            raise HTTPException(
                status_code=400,
                detail=f"CSV file not found: {req.csv_path}"
            )
        
        # Generate videos using pipeline wrapper
        result = pw.batch_generate(
            csv_path=req.csv_path,
            output_dir=req.output_dir
        )
        
        return BatchResponse(
            status="success",
            output_dir=result["output_dir"],
            message="Batch generation completed successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch generation failed: {str(e)}"
        )

# Configuration endpoint
@app.get("/config")
async def get_config():
    """Get current configuration"""
    return {
        "config": config,
        "pipeline_config": pw.get_config()
    }

# Video info endpoint
@app.get("/videos/{video_id}")
async def get_video_info(video_id: str):
    """Get information about a generated video"""
    try:
        # Look for video in outputs directory
        work_base = config.get("work_base", "./outputs")
        video_path = os.path.join(work_base, f"{video_id}.mp4")
        
        if not os.path.exists(video_path):
            raise HTTPException(
                status_code=404,
                detail="Video not found"
            )
        
        file_size = os.path.getsize(video_path)
        
        return {
            "video_id": video_id,
            "path": video_path,
            "size_bytes": file_size,
            "exists": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting video info: {str(e)}"
        )

# List videos endpoint
@app.get("/videos")
async def list_videos():
    """List all generated videos"""
    try:
        work_base = config.get("work_base", "./outputs")
        
        if not os.path.exists(work_base):
            return {"videos": []}
        
        videos = []
        for file in os.listdir(work_base):
            if file.endswith('.mp4'):
                file_path = os.path.join(work_base, file)
                video_id = file.replace('.mp4', '')
                
                videos.append({
                    "video_id": video_id,
                    "filename": file,
                    "size_bytes": os.path.getsize(file_path),
                    "created": os.path.getctime(file_path)
                })
        
        return {"videos": videos}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing videos: {str(e)}"
        )

# Test endpoint
@app.post("/test")
async def test_generation():
    """Test video generation with sample prompt"""
    try:
        test_prompt = "A young Kenyan entrepreneur builds an AI startup in Nairobi"
        
        video_path = pw.generate(
            prompt=test_prompt,
            scenes=2,
            vertical=True,
            lang="sheng"
        )
        
        return {
            "status": "success",
            "message": "Test video generated successfully",
            "video_path": os.path.abspath(video_path),
            "prompt": test_prompt
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Test generation failed: {str(e)}"
        )

if __name__ == "__main__":
    # Get config values
    host = config.get("api_host", "0.0.0.0")
    port = config.get("api_port", 8000)
    
    print(f"🚀 Starting Shujaa Studio API on {host}:{port}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    print(f"🔧 Health Check: http://{host}:{port}/health")
    
    # Start server
    uvicorn.run(
        "simple_api:app",
        host=host,
        port=port,
        reload=True
    )
