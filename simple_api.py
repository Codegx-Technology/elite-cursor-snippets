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

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pipeline_wrapper as pw
import uvicorn
import os
import uuid
import yaml
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt

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

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "shujaa-studio-dev-secret-key-2025"  # In production, use environment variable
ALGORITHM = "HS256"

# Development users for super admin access
DEV_USERS = {
    "peter": {"password": "normal", "role": "admin", "email": "peter@shujaa.studio"},
    "apollo": {"password": "aluru742!!", "role": "user", "email": "apollo@shujaa.studio"}
}

# Development tenants for super admin access
DEV_TENANTS = {
    "tenant-1": {"name": "Shujaa Inc.", "plan": "Enterprise", "users": ["peter"]},
    "tenant-2": {"name": "Apollo Creations", "plan": "Pro", "users": ["apollo"]},
}

# Development projects
DEV_PROJECTS = [
    {"id": "proj-1", "name": "Sheng Dictionary Animation", "description": "An animated video explaining sheng words.", "type": "video", "status": "Completed", "created_at": "2025-08-20T10:00:00Z", "updated_at": "2025-08-21T12:00:00Z", "items_count": 10},
    {"id": "proj-2", "name": "Nairobi Tech Hub Promo", "description": "Promotional video for a tech hub in Nairobi.", "type": "video", "status": "In Progress", "created_at": "2025-08-22T14:00:00Z", "updated_at": "2025-08-22T14:00:00Z", "items_count": 5},
]

# Development models
DEV_MODELS = [
    {"id": "model-1", "name": "Shujaa-TTS-Sheng", "provider": "Hugging Face", "version": "1.2.0", "status": "available", "latest_version": "1.2.5", "update_status": "pending_approval"},
    {"id": "model-2", "name": "Gemini-Pro-Vision-Kenya", "provider": "Google", "version": "1.0.0", "status": "available", "latest_version": "1.0.0", "update_status": "up_to_date"},
    {"id": "model-3", "name": "RunPod-Stable-Diffusion-XL", "provider": "RunPod", "version": "1.0.0", "status": "not_downloaded", "latest_version": "1.1.0", "update_status": "available"},
]

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

# Authentication helper functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    user = DEV_USERS.get(username)
    if user and user["password"] == password:
        return {"username": username, **user}
    return None

# Authentication endpoints
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/superadmin/token")
async def superadmin_login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user or user["role"] != "admin":
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password or not an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_data = DEV_USERS.get(username)
        if user_data is None:
            raise HTTPException(status_code=401, detail="User not found")
        return {
            "username": username,
            "email": user_data["email"],
            "role": role,
            "id": username  # Simple ID for development
        }
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Admin-only endpoint to get all users
@app.get("/admin/users")
async def get_all_users(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Convert DEV_USERS to a list of user objects
        user_list = [
            {
                "id": username,
                "username": username,
                "email": userdata["email"],
                "role": userdata["role"]
            }
            for username, userdata in DEV_USERS.items()
        ]
        return {"users": user_list}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.delete("/admin/users/{user_id}")
async def delete_user(user_id: str, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        
        if user_id not in DEV_USERS:
            raise HTTPException(status_code=404, detail="User not found")
        
        # In a real app, you would delete from a database.
        # Here we just remove from the dictionary.
        del DEV_USERS[user_id]
        
        return {"status": "success", "message": "User deleted successfully"}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/admin/tenants")
async def get_all_tenants(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        
        tenant_list = [
            {
                "id": tenant_id,
                **tenant_data
            }
            for tenant_id, tenant_data in DEV_TENANTS.items()
        ]
        return {"tenants": tenant_list}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Project endpoints
@app.get("/api/projects")
async def get_projects(token: str = Depends(oauth2_scheme)):
    # In a real app, you'd have pagination and filtering.
    # For now, we'll just return all projects.
    return {"projects": DEV_PROJECTS, "total": len(DEV_PROJECTS), "page": 1, "pages": 1}

class ProjectUpdate(BaseModel):
    name: str
    description: Optional[str] = None

@app.put("/api/projects/{project_id}")
async def update_project(project_id: str, project_update: ProjectUpdate, token: str = Depends(oauth2_scheme)):
    for proj in DEV_PROJECTS:
        if proj["id"] == project_id:
            proj["name"] = project_update.name
            proj["description"] = project_update.description
            proj["updated_at"] = datetime.utcnow().isoformat() + "Z"
            return proj
    raise HTTPException(status_code=404, detail="Project not found")

# Model Management endpoints
@app.get("/admin/models")
async def get_models(token: str = Depends(oauth2_scheme)):
    return {"models": DEV_MODELS}

@app.post("/admin/models/{model_id}/download")
async def download_model(model_id: str, token: str = Depends(oauth2_scheme)):
    for model in DEV_MODELS:
        if model["id"] == model_id:
            model["status"] = "downloading"
            return {"status": "success", "message": f"Downloading model {model_id}"}
    raise HTTPException(status_code=404, detail="Model not found")

@app.post("/admin/models/{model_id}/approve")
async def approve_model_update(model_id: str, token: str = Depends(oauth2_scheme)):
    for model in DEV_MODELS:
        if model["id"] == model_id:
            model["update_status"] = "approved"
            model["version"] = model["latest_version"]
            return {"status": "success", "message": f"Model update for {model_id} approved"}
    raise HTTPException(status_code=404, detail="Model not found")


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
    # Fix Windows console encoding for emojis
    import sys
    if sys.platform == "win32":
        try:
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
        except Exception:
            pass

    # Get config values
    host = config.get("api_host", "0.0.0.0")
    port = config.get("api_port", 8000)

    try:
        print(f"🚀 Starting Shujaa Studio API on {host}:{port}")
        print(f"📖 API Documentation: http://{host}:{port}/docs")
        print(f"🔧 Health Check: http://{host}:{port}/health")
    except UnicodeEncodeError:
        # Fallback without emojis
        print(f"Starting Shujaa Studio API on {host}:{port}")
        print(f"API Documentation: http://{host}:{port}/docs")
        print(f"Health Check: http://{host}:{port}/health")

    # Start server
    uvicorn.run(
        "simple_api:app",
        host=host,
        port=port,
        reload=True
    )
