from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
import uvicorn

from logging_setup import get_logger
from config_loader import get_config
from auth.jwt_utils import verify_jwt # Import verify_jwt

logger = get_logger(__name__)
config = get_config()

app = FastAPI(
    title=config.app.name,
    version=config.app.version,
    description="API for Shujaa Studio - Enterprise AI Video Generation"
)

# OAuth2PasswordBearer for JWT token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # tokenUrl is a placeholder

class GenerateVideoRequest(BaseModel):
    prompt: str
    news_url: Optional[str] = None
    script_file: Optional[str] = None
    upload_youtube: bool = False

# --- Dependency Functions for Authentication and Authorization ---

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    // [TASK]: Extract and verify JWT token to get current user
    // [GOAL]: Implement JWT-based access control
    """
    try:
        payload = verify_jwt(token)
        # In a real app, you'd fetch user from DB based on payload.get('user_id')
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {e}")

async def get_current_tenant(user: dict = Depends(get_current_user)):
    """
    // [TASK]: Extract tenant ID from current user's payload
    // [GOAL]: Implement multi-tenancy
    """
    tenant_id = user.get("tenant_id")
    if not tenant_id:
        raise HTTPException(status_code=403, detail="Tenant ID not found in token.")
    return tenant_id

# --- Middleware for Tenancy (Conceptual) ---

@app.middleware("http")
async def add_tenant_context(request: Request, call_next):
    """
    // [TASK]: Add tenant context to request state
    // [GOAL]: Make tenant ID easily accessible throughout the request lifecycle
    """
    try:
        # Attempt to get tenant_id from JWT if present
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = verify_jwt(token)
            request.state.tenant_id = payload.get("tenant_id")
            logger.debug(f"Tenant ID from JWT: {request.state.tenant_id}")
        else:
            request.state.tenant_id = "default_tenant" # Fallback for unauthenticated requests
            logger.debug("No JWT, using default tenant.")

    except Exception as e:
        logger.warning(f"Error in tenant context middleware: {e}")
        request.state.tenant_id = "unauthenticated_tenant"

    response = await call_next(request)
    return response

# --- API Endpoints ---

@app.get("/health")
async def health_check():
    """
    // [TASK]: Health check endpoint
    // [GOAL]: Verify API server is running
    """
    logger.info("Health check requested.")
    return {"status": "ok", "message": "Shujaa Studio API is running!"}

@app.post("/generate_video")
async def generate_video_endpoint(request_data: GenerateVideoRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    """
    // [TASK]: Video generation endpoint
    // [GOAL]: Expose video generation pipeline via API with authentication and tenancy
    """
    logger.info(f"Video generation request received from user {current_user.get('user_id')} (Tenant: {current_tenant}): {request_data.dict()}")
    
    # This is a placeholder. In a real scenario, this would call
    # the pipeline_orchestrator or news_video_generator directly.
    # For now, just simulate success.
    
    if not request_data.prompt and not request_data.news_url and not request_data.script_file:
        raise HTTPException(status_code=400, detail="Either 'prompt', 'news_url', or 'script_file' must be provided.")

    # Simulate processing time
    await asyncio.sleep(2) 

    logger.info("Video generation simulated successfully.")
    return {"status": "success", "video_id": "simulated_video_123", "message": "Video generation request received and processing (simulated)."}

# Example of a protected endpoint
@app.get("/protected_data")
async def protected_data(current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    """
    // [TASK]: Example of a protected endpoint
    // [GOAL]: Demonstrate JWT and tenancy integration
    """
    return {"message": f"Welcome, {current_user.get('user_id')} from tenant {current_tenant}! This is protected data.", "user": current_user, "tenant": current_tenant}

if __name__ == "__main__":
    # To run this server, use: uvicorn api_server:app --reload --port 8000
    # Or programmatically:
    uvicorn.run(app, host="0.0.0.0", port=8000)