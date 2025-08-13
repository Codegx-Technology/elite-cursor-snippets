from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import asyncio
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path to import from main codebase
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pipeline_orchestrator import PipelineOrchestrator
    from ai_model_manager import generate_text, generate_image, generate_speech
    from enhanced_model_router import enhanced_router, GenerationRequest, GenerationMethod
    PIPELINE_AVAILABLE = True
    ENHANCED_ROUTER_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False
    ENHANCED_ROUTER_AVAILABLE = False
    print("Warning: Pipeline modules not available. Using mock responses.")

app = FastAPI(
    title="Shujaa Studio API",
    description="Kenya-First AI Video Generation Platform",
    version="1.0.0"
)

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo (replace with database in production)
jobs_storage = {}
projects_storage = {}
gallery_storage = []
analytics_storage = {
    "overview": {
        "total_videos": 0,
        "total_images": 0,
        "total_audio": 0,
        "total_views": 0,
        "total_downloads": 0,
    },
    "usage_trends": [],
    "popular_content": [],
    "performance_metrics": {
        "avg_generation_time": 0,
        "success_rate": 95,
        "user_satisfaction": 88,
    }
}

# Initialize pipeline orchestrator if available
orchestrator = PipelineOrchestrator() if PIPELINE_AVAILABLE else None

# Pydantic models
class VideoGenerationRequest(BaseModel):
    prompt: str
    lang: Optional[str] = "en"
    scenes: Optional[int] = 3
    vertical: Optional[bool] = True
    style: Optional[str] = "realistic"
    duration: Optional[int] = 30
    voice_type: Optional[str] = "female"
    background_music: Optional[bool] = True
    cultural_preset: Optional[str] = None

class NewsVideoGenerationRequest(BaseModel):
    news_url: Optional[str] = None
    news_query: Optional[str] = None
    script_content: Optional[str] = None
    lang: Optional[str] = "en"
    scenes: Optional[int] = 3
    duration: Optional[int] = 60
    voice_type: Optional[str] = "male"
    upload_youtube: Optional[bool] = False

class ImageGenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = "realistic"
    size: Optional[str] = "1024x1024"
    cultural_preset: Optional[str] = None

class AudioGenerationRequest(BaseModel):
    text: str
    voice_type: Optional[str] = "female"
    language: Optional[str] = "en"
    speed: Optional[float] = 1.0

class ProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None
    type: str  # 'video', 'image', 'audio'

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

# Content Generation Endpoints
@app.post("/api/generate/video")
async def generate_video(request: VideoGenerationRequest, background_tasks: BackgroundTasks):
    """Generate video content using AI pipeline"""
    job_id = str(uuid.uuid4())

    # Create job entry
    job = {
        "id": job_id,
        "type": "video",
        "status": "pending",
        "progress": 0,
        "created_at": datetime.now().isoformat(),
        "metadata": request.dict(),
        "result_url": None,
        "error_message": None
    }
    jobs_storage[job_id] = job

    # Start background processing
    background_tasks.add_task(process_video_generation, job_id, request)

    return {
        "status": "success",
        "video_id": job_id,
        "message": "Video generation started",
        "progress": 0,
        "estimated_time": 120  # 2 minutes estimate
    }

@app.post("/api/generate/news-video")
async def generate_news_video(request: NewsVideoGenerationRequest, background_tasks: BackgroundTasks):
    """Generate news video content using AI pipeline"""
    job_id = str(uuid.uuid4())

    # Create job entry
    job = {
        "id": job_id,
        "type": "news_video",
        "status": "pending",
        "progress": 0,
        "created_at": datetime.now().isoformat(),
        "metadata": request.dict(),
        "result_url": None,
        "error_message": None
    }
    jobs_storage[job_id] = job

    # Start background processing
    background_tasks.add_task(process_news_video_generation, job_id, request)

    return {
        "status": "success",
        "video_id": job_id,
        "message": "News video generation started",
        "progress": 0,
        "estimated_time": 180  # 3 minutes estimate for news processing
    }

@app.post("/api/generate/image")
async def generate_image_endpoint(request: ImageGenerationRequest, background_tasks: BackgroundTasks):
    """Generate image content using AI pipeline"""
    job_id = str(uuid.uuid4())

    job = {
        "id": job_id,
        "type": "image",
        "status": "pending",
        "progress": 0,
        "created_at": datetime.now().isoformat(),
        "metadata": request.dict(),
        "result_url": None,
        "error_message": None
    }
    jobs_storage[job_id] = job

    background_tasks.add_task(process_image_generation, job_id, request)

    return {
        "status": "success",
        "video_id": job_id,  # Keep same interface
        "message": "Image generation started",
        "progress": 0,
        "estimated_time": 30
    }

@app.post("/api/generate/audio")
async def generate_audio_endpoint(request: AudioGenerationRequest, background_tasks: BackgroundTasks):
    """Generate audio content using AI pipeline"""
    job_id = str(uuid.uuid4())

    job = {
        "id": job_id,
        "type": "audio",
        "status": "pending",
        "progress": 0,
        "created_at": datetime.now().isoformat(),
        "metadata": request.dict(),
        "result_url": None,
        "error_message": None
    }
    jobs_storage[job_id] = job

    background_tasks.add_task(process_audio_generation, job_id, request)

    return {
        "status": "success",
        "video_id": job_id,  # Keep same interface
        "message": "Audio generation started",
        "progress": 0,
        "estimated_time": 15
    }

@app.get("/api/status")
async def get_status():
    return {
        "status": "ok",
        "message": "Shujaa Studio Backend is running and ready for action! 🇰🇪",
        "pipeline_available": PIPELINE_AVAILABLE,
        "enhanced_router_available": ENHANCED_ROUTER_AVAILABLE,
        "features": {
            "video_generation": True,
            "image_generation": True,
            "audio_generation": True,
            "analytics": True,
            "projects": True,
            "gallery": True,
            "intelligent_fallbacks": ENHANCED_ROUTER_AVAILABLE,
            "kenya_first_experience": True
        }
    }

# Background processing functions
async def process_video_generation(job_id: str, request: VideoGenerationRequest):
    """Background task for video generation with enhanced routing"""
    try:
        job = jobs_storage[job_id]
        job["status"] = "processing"
        job["progress"] = 10

        if ENHANCED_ROUTER_AVAILABLE:
            # Use enhanced router for intelligent fallbacks
            generation_request = GenerationRequest(
                prompt=request.prompt,
                type="video",
                user_id=None,  # TODO: Get from request context
                preferences={
                    "lang": request.lang,
                    "scenes": request.scenes,
                    "vertical": request.vertical,
                    "style": request.style,
                    "voice_type": request.voice_type,
                    "background_music": request.background_music
                },
                cultural_preset=request.cultural_preset,
                quality="standard"
            )

            # Update progress
            job["progress"] = 20

            # Route through enhanced system
            result = await enhanced_router.route_generation(generation_request)

            if result.success:
                job["status"] = "completed"
                job["progress"] = 100
                job["result_url"] = result.content_url
                job["completed_at"] = datetime.now().isoformat()
                job["method_used"] = result.method_used.value if result.method_used else "unknown"
                job["generation_time"] = result.generation_time
                job["cached"] = result.cached

                # Add to gallery
                gallery_item = {
                    "id": job_id,
                    "type": "video",
                    "title": f"Video: {request.prompt[:50]}...",
                    "thumbnail": "/api/placeholder/400/300",
                    "created_at": job["created_at"],
                    "duration": f"{request.duration}s",
                    "size": "45 MB",
                    "tags": ["AI Generated", "Kenya"],
                    "url": job["result_url"],
                    "method_used": job["method_used"],
                    "cached": job["cached"]
                }
                gallery_storage.append(gallery_item)

                # Update analytics
                analytics_storage["overview"]["total_videos"] += 1
            else:
                # Handle friendly fallback
                if result.method_used == GenerationMethod.FRIENDLY_FALLBACK:
                    job["status"] = "friendly_fallback"
                    job["progress"] = 0
                    job["friendly_message"] = result.metadata.get("friendly_message") if result.metadata else None
                    job["retry_options"] = result.metadata.get("retry_options") if result.metadata else []
                    job["spinner_type"] = result.metadata.get("spinner_type") if result.metadata else "kenya_flag"
                else:
                    job["status"] = "failed"
                    job["error_message"] = result.error_message or "Video generation failed"

        elif PIPELINE_AVAILABLE and orchestrator:
            # Fallback to original pipeline
            result = await orchestrator.run_pipeline(
                input_type="general_prompt",
                input_data=request.prompt,
                user_preferences={
                    "lang": request.lang,
                    "scenes": request.scenes,
                    "vertical": request.vertical,
                    "style": request.style,
                    "voice_type": request.voice_type,
                    "background_music": request.background_music
                }
            )

            if result.get("status") == "success":
                job["status"] = "completed"
                job["progress"] = 100
                job["result_url"] = result.get("video_path", "/api/placeholder/video.mp4")
                job["completed_at"] = datetime.now().isoformat()

                # Add to gallery
                gallery_item = {
                    "id": job_id,
                    "type": "video",
                    "title": f"Video: {request.prompt[:50]}...",
                    "thumbnail": "/api/placeholder/400/300",
                    "created_at": job["created_at"],
                    "duration": f"{request.duration}s",
                    "size": "45 MB",
                    "tags": ["AI Generated", "Kenya"],
                    "url": job["result_url"]
                }
                gallery_storage.append(gallery_item)

                # Update analytics
                analytics_storage["overview"]["total_videos"] += 1
            else:
                job["status"] = "failed"
                job["error_message"] = result.get("message", "Video generation failed")
        else:
            # Mock processing for demo
            await asyncio.sleep(5)  # Simulate processing time
            job["status"] = "completed"
            job["progress"] = 100
            job["result_url"] = "/api/placeholder/video.mp4"
            job["completed_at"] = datetime.now().isoformat()

            # Add mock gallery item
            gallery_item = {
                "id": job_id,
                "type": "video",
                "title": f"Video: {request.prompt[:50]}...",
                "thumbnail": "/api/placeholder/400/300",
                "created_at": job["created_at"],
                "duration": f"{request.duration}s",
                "size": "45 MB",
                "tags": ["AI Generated", "Kenya"],
                "url": job["result_url"]
            }
            gallery_storage.append(gallery_item)
            analytics_storage["overview"]["total_videos"] += 1

    except Exception as e:
        job["status"] = "failed"
        job["error_message"] = str(e)

async def process_news_video_generation(job_id: str, request: NewsVideoGenerationRequest):
    """Background task for news video generation"""
    try:
        job = jobs_storage[job_id]
        job["status"] = "processing"
        job["progress"] = 10

        # Mock news video generation for now
        await asyncio.sleep(3)  # Simulate news processing
        job["progress"] = 50

        await asyncio.sleep(2)  # Simulate video generation
        job["status"] = "completed"
        job["progress"] = 100
        job["result_url"] = f"/generated/news_video_{job_id}.mp4"
        job["completed_at"] = datetime.now().isoformat()

        # Add to gallery
        gallery_item = {
            "id": job_id,
            "type": "video",
            "title": f"News: {(request.news_query or request.script_content or 'News Video')[:50]}...",
            "thumbnail": "/api/placeholder/400/300",
            "created_at": job["created_at"],
            "duration": f"{request.duration}s",
            "size": "52 MB",
            "tags": ["News", "AI Generated", "Kenya"],
            "url": job["result_url"]
        }
        gallery_storage.append(gallery_item)

        # Update analytics
        analytics_storage["overview"]["total_videos"] += 1

    except Exception as e:
        job["status"] = "failed"
        job["error_message"] = str(e)

async def process_image_generation(job_id: str, request: ImageGenerationRequest):
    """Background task for image generation"""
    try:
        job = jobs_storage[job_id]
        job["status"] = "processing"
        job["progress"] = 20

        if PIPELINE_AVAILABLE:
            # Use real AI model
            image_bytes = await generate_image(request.prompt)
            if image_bytes:
                # Save image and get URL
                job["status"] = "completed"
                job["progress"] = 100
                job["result_url"] = "/api/placeholder/image.png"
                job["completed_at"] = datetime.now().isoformat()
            else:
                job["status"] = "failed"
                job["error_message"] = "Image generation failed"
        else:
            # Mock processing
            await asyncio.sleep(2)
            job["status"] = "completed"
            job["progress"] = 100
            job["result_url"] = "/api/placeholder/image.png"
            job["completed_at"] = datetime.now().isoformat()

        # Add to gallery
        gallery_item = {
            "id": job_id,
            "type": "image",
            "title": f"Image: {request.prompt[:50]}...",
            "thumbnail": "/api/placeholder/400/300",
            "created_at": job["created_at"],
            "size": "2.1 MB",
            "tags": ["AI Generated", "Kenya"],
            "url": job["result_url"]
        }
        gallery_storage.append(gallery_item)
        analytics_storage["overview"]["total_images"] += 1

    except Exception as e:
        job["status"] = "failed"
        job["error_message"] = str(e)

async def process_audio_generation(job_id: str, request: AudioGenerationRequest):
    """Background task for audio generation"""
    try:
        job = jobs_storage[job_id]
        job["status"] = "processing"
        job["progress"] = 30

        if PIPELINE_AVAILABLE:
            # Use real TTS
            audio_bytes = await generate_speech(request.text, voice_type=request.voice_type)
            if audio_bytes:
                job["status"] = "completed"
                job["progress"] = 100
                job["result_url"] = "/api/placeholder/audio.mp3"
                job["completed_at"] = datetime.now().isoformat()
            else:
                job["status"] = "failed"
                job["error_message"] = "Audio generation failed"
        else:
            # Mock processing
            await asyncio.sleep(1)
            job["status"] = "completed"
            job["progress"] = 100
            job["result_url"] = "/api/placeholder/audio.mp3"
            job["completed_at"] = datetime.now().isoformat()

        # Add to gallery
        gallery_item = {
            "id": job_id,
            "type": "audio",
            "title": f"Audio: {request.text[:50]}...",
            "thumbnail": "/api/placeholder/400/300",
            "created_at": job["created_at"],
            "duration": "1:45",
            "size": "8.5 MB",
            "tags": ["AI Generated", "Voice"],
            "url": job["result_url"]
        }
        gallery_storage.append(gallery_item)
        analytics_storage["overview"]["total_audio"] += 1

    except Exception as e:
        job["status"] = "failed"
        job["error_message"] = str(e)

# Job Management Endpoints
@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    """Get job status and details"""
    if job_id not in jobs_storage:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs_storage[job_id]

@app.get("/api/jobs")
async def get_jobs(limit: int = 10, offset: int = 0):
    """Get list of jobs with pagination"""
    all_jobs = list(jobs_storage.values())
    all_jobs.sort(key=lambda x: x["created_at"], reverse=True)

    total = len(all_jobs)
    jobs = all_jobs[offset:offset + limit]

    return {
        "jobs": jobs,
        "total": total,
        "limit": limit,
        "offset": offset
    }

# Projects Endpoints
@app.get("/api/projects")
async def get_projects(page: int = 1, limit: int = 6):
    """Get projects with pagination"""
    all_projects = list(projects_storage.values())
    all_projects.sort(key=lambda x: x["created_at"], reverse=True)

    total = len(all_projects)
    start = (page - 1) * limit
    projects = all_projects[start:start + limit]
    pages = (total + limit - 1) // limit

    return {
        "projects": projects,
        "total": total,
        "page": page,
        "pages": pages
    }

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get specific project"""
    if project_id not in projects_storage:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects_storage[project_id]

@app.post("/api/projects")
async def create_project(request: ProjectRequest):
    """Create new project"""
    project_id = str(uuid.uuid4())
    project = {
        "id": project_id,
        "name": request.name,
        "description": request.description,
        "type": request.type,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "items_count": 0
    }
    projects_storage[project_id] = project
    return project

@app.put("/api/projects/{project_id}")
async def update_project(project_id: str, request: ProjectUpdate):
    """Update project"""
    if project_id not in projects_storage:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects_storage[project_id]
    if request.name is not None:
        project["name"] = request.name
    if request.description is not None:
        project["description"] = request.description
    if request.status is not None:
        project["status"] = request.status

    project["updated_at"] = datetime.now().isoformat()
    return project

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete project"""
    if project_id not in projects_storage:
        raise HTTPException(status_code=404, detail="Project not found")

    del projects_storage[project_id]
    return {"success": True}

# Gallery Endpoints
@app.get("/api/gallery")
async def get_gallery(
    page: int = 1,
    limit: int = 6,
    type: Optional[str] = None,
    search: Optional[str] = None
):
    """Get gallery items with pagination and filtering"""
    filtered_items = gallery_storage.copy()

    # Filter by type
    if type:
        filtered_items = [item for item in filtered_items if item["type"] == type]

    # Filter by search
    if search:
        search_lower = search.lower()
        filtered_items = [
            item for item in filtered_items
            if search_lower in item["title"].lower() or
               any(search_lower in tag.lower() for tag in item["tags"])
        ]

    # Sort by creation date
    filtered_items.sort(key=lambda x: x["created_at"], reverse=True)

    total = len(filtered_items)
    start = (page - 1) * limit
    items = filtered_items[start:start + limit]
    pages = (total + limit - 1) // limit if total > 0 else 1

    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": pages
    }

# Analytics Endpoints
@app.get("/api/analytics")
async def get_analytics(range: str = "30d"):
    """Get analytics data"""
    # Generate mock trends data based on range
    days = {"7d": 7, "30d": 30, "90d": 90}.get(range, 30)

    trends = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        trends.append({
            "date": date,
            "videos": max(0, analytics_storage["overview"]["total_videos"] // days + (i % 3)),
            "images": max(0, analytics_storage["overview"]["total_images"] // days + (i % 2)),
            "audio": max(0, analytics_storage["overview"]["total_audio"] // days + (i % 4))
        })

    # Generate popular content from gallery
    popular_content = []
    for item in gallery_storage[-5:]:  # Last 5 items
        popular_content.append({
            "id": item["id"],
            "title": item["title"],
            "type": item["type"],
            "views": 150 + len(item["id"]) % 500,  # Mock views
            "downloads": 50 + len(item["id"]) % 200  # Mock downloads
        })

    return {
        "overview": analytics_storage["overview"],
        "usage_trends": trends,
        "popular_content": popular_content,
        "performance_metrics": analytics_storage["performance_metrics"]
    }

@app.get("/api/analytics/overview")
async def get_analytics_overview():
    """Get analytics overview"""
    return analytics_storage["overview"]

# Dashboard Endpoints
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    return {
        "videosGenerated": analytics_storage["overview"]["total_videos"],
        "imagesCreated": analytics_storage["overview"]["total_images"],
        "audioTracks": analytics_storage["overview"]["total_audio"],
        "activeUsers": 1,  # Mock active users
        "systemStatus": "online",
        "lastGeneration": "2 minutes ago" if gallery_storage else "No data available"
    }

@app.get("/api/dashboard/activity")
async def get_recent_activity():
    """Get recent activity"""
    activities = []
    for item in gallery_storage[-4:]:  # Last 4 items
        activities.append({
            "id": item["id"],
            "type": item["type"],
            "title": item["title"],
            "timestamp": "2 minutes ago",  # Mock timestamp
            "status": "completed"
        })

    return activities

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
