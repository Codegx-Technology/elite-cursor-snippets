from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import subprocess
import uuid
import os
import asyncio
from pathlib import Path
from typing import Optional
import json

app = FastAPI(title="Shujaa Studio API", version="1.0.0")

class PromptRequest(BaseModel):
    prompt: str
    lang: str = "sheng"
    scenes: int = 3
    vertical: bool = True
    output_format: str = "mp4"

class VideoResponse(BaseModel):
    status: str
    video_id: str
    video_path: str
    message: str

# Ensure output directories exist
os.makedirs("videos", exist_ok=True)
os.makedirs("temp", exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Shujaa Studio API - AI Video Generation Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "shujaa-studio"}

@app.post("/generate-video", response_model=VideoResponse)
async def generate_video(req: PromptRequest):
    """
    Generate AI video from prompt using Shujaa Studio pipeline
    """
    try:
        video_id = str(uuid.uuid4())[:8]
        output_path = f"videos/{video_id}.{req.output_format}"
        
        # Sanitize prompt for command line
        sanitized_prompt = req.prompt.replace('"', '\\"')
        
        # Build pipeline command
        cmd = [
            "python", "pipeline.py",
            "--prompt", sanitized_prompt,
            "--lang", req.lang,
            "--scenes", str(req.scenes),
            "--out", output_path
        ]
        
        if req.vertical:
            cmd.append("--vertical")
        
        # Execute pipeline
        print(f"[API] Executing: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=500, 
                detail=f"Pipeline failed: {result.stderr}"
            )
        
        # Check if output file exists
        if not os.path.exists(output_path):
            raise HTTPException(
                status_code=500,
                detail="Video file not generated"
            )
        
        return VideoResponse(
            status="success",
            video_id=video_id,
            video_path=output_path,
            message="Video generated successfully"
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail="Video generation timed out"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )

@app.get("/videos/{video_id}")
async def get_video_info(video_id: str):
    """Get information about a generated video"""
    video_path = f"videos/{video_id}.mp4"
    
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

@app.get("/list-videos")
async def list_videos():
    """List all generated videos"""
    videos_dir = Path("videos")
    if not videos_dir.exists():
        return {"videos": []}
    
    videos = []
    for video_file in videos_dir.glob("*.mp4"):
        videos.append({
            "video_id": video_file.stem,
            "filename": video_file.name,
            "size_bytes": video_file.stat().st_size,
            "created": video_file.stat().st_ctime
        })
    
    return {"videos": videos}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
