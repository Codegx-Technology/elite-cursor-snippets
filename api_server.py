from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import uvicorn

from logging_setup import get_logger
from config_loader import get_config
from auth.jwt_utils import verify_jwt # Import verify_jwt
from pipeline_orchestrator import PipelineOrchestrator # Import PipelineOrchestrator
from billing_middleware import enforce_limits, BillingException # Import billing middleware
from landing_page_service import LandingPageService # Import LandingPageService
from scan_alert_system import ScanAlertSystem # Import ScanAlertSystem
from crm_integration import CRMIntegrationService # Import CRMIntegrationService

from database import engine, get_db # Import database engine and session dependency
from auth.user_models import Base, User, Tenant # Import SQLAlchemy models
from auth.auth_service import create_user, authenticate_user, create_access_token # Import auth service functions
from sqlalchemy.orm import Session # Import Session for type hinting

logger = get_logger(__name__)
config = get_config()

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.app.name,
    version=config.app.version,
    description="API for Shujaa Studio - Enterprise AI Video Generation"
)

# Initialize PipelineOrchestrator
orchestrator = PipelineOrchestrator()

# Initialize LandingPageService
landing_page_service = LandingPageService()

# Initialize ScanAlertSystem
scan_alert_system = ScanAlertSystem()

# Initialize CRMIntegrationService
crm_integration_service = CRMIntegrationService()

# OAuth2PasswordBearer for JWT token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # tokenUrl is a placeholder

class GenerateVideoRequest(BaseModel):
    prompt: str
    news_url: Optional[str] = None
    script_file: Optional[str] = None
    upload_youtube: bool = False

class GenerateLandingPageRequest(BaseModel):
    qr_code_id: str
    brand_metadata: dict

class ScanAlertRequest(BaseModel):
    qr_code_id: str
    location_data: dict
    device_type: str
    user_settings: dict

class CRMPushContactRequest(BaseModel):
    crm_name: str
    contact_data: dict

# Pydantic models for User Authentication
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    tenant_name: Optional[str] = "default"

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Dependency Functions for Authentication and Authorization ---

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    // [TASK]: Extract and verify JWT token to get current user
    // [GOAL]: Implement JWT-based access control
    """
    try:
        payload = verify_jwt(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials: User ID missing")
        
        # In a real app, you'd fetch user from DB based on user_id to ensure it's active
        # For now, we just return the payload
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

@app.post("/register", response_model=UserCreate)
async def register_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """
    // [TASK]: User registration endpoint
    // [GOAL]: Allow new users to register
    """
    db_user = create_user(db, user.username, user.email, user.password, user.tenant_name)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered.")
    return db_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    // [TASK]: User login endpoint to get JWT token
    // [GOAL]: Authenticate users and issue access tokens
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.auth.access_token_expire_minutes)
    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username, "tenant_id": user.tenant_id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/generate_video")
async def generate_video_endpoint(request_data: GenerateVideoRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    """
    // [TASK]: Video generation endpoint
    // [GOAL]: Expose video generation pipeline via API
    """
    logger.info(f"Video generation request received from user {current_user.get('user_id')} (Tenant: {current_tenant}): {request_data.dict()}")
    
    # --- F.2: Integrate Billing Middleware ---
    # Use a placeholder user_id for now, as full user management is not yet implemented.
    # The feature name can be dynamic based on the request, but for now, assume 'video_generation'.
    try:
        enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="video_generation")
        logger.info(f"Billing limits checked for user {current_user.get('user_id')}. Proceeding.")
    except BillingException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during billing check: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during billing check.")
    # --- End F.2 ---

    if not request_data.prompt and not request_data.news_url and not request_data.script_file:
        raise HTTPException(status_code=400, detail="Either 'prompt', 'news_url', or 'script_file' must be provided.")

    # Determine input type for orchestrator
    input_type = "general_prompt"
    input_data = request_data.prompt
    if request_data.news_url:
        input_type = "news_url"
        input_data = request_data.news_url
    elif request_data.script_file:
        input_type = "script_file"
        input_data = request_data.script_file

    # Call the orchestrator to run the appropriate pipeline
    orchestrator_decision = orchestrator.decide_pipeline(input_type)
    chosen_pipeline = orchestrator_decision["chosen"]
    reason = orchestrator_decision["reason"]

    if not chosen_pipeline:
        raise HTTPException(status_code=500, detail=f"Could not determine pipeline: {reason}")

    logger.info(f"Orchestrator decided to use pipeline: {chosen_pipeline} (Reason: {reason})")

    # For now, orchestrator.run_pipeline is still dry-run. Actual execution will be integrated later.
    # Simulate processing time
    await asyncio.sleep(2) 

    logger.info("Video generation request received and processing (simulated).")
    return {"status": "success", "video_id": "simulated_video_123", "message": f"Video generation request routed to {chosen_pipeline} (simulated)."}

@app.post("/generate_landing_page")
async def generate_landing_page_endpoint(request_data: GenerateLandingPageRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    """
    // [TASK]: Landing page generation endpoint
    // [GOAL]: Expose landing page generation service via API
    """
    logger.info(f"Landing page generation request received from user {current_user.get('user_id')} (Tenant: {current_tenant}): {request_data.dict()}")

    # --- F.2: Integrate Billing Middleware (for landing page generation) ---
    try:
        enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="landing_page_generation")
        logger.info(f"Billing limits checked for user {current_user.get('user_id')}. Proceeding.")
    except BillingException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during billing check for landing page: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during billing check.")
    # --- End F.2 ---

    # Call the landing page service
    result = await landing_page_service.generate_landing_page(request_data.qr_code_id, request_data.brand_metadata)

    if result.get("status") == "success":
        logger.info(f"Landing page generated successfully: {result.get('s3_url')}")
        return {"status": "success", "s3_url": result.get('s3_url'), "message": "Landing page generation initiated."}
    else:
        raise HTTPException(status_code=500, detail=f"Landing page generation failed: {result.get('message', 'Unknown error')}")

@app.post("/scan_alert")
async def scan_alert_endpoint(request_data: ScanAlertRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    """
    // [TASK]: Scan alert endpoint
    // [GOAL]: Expose scan alert system via API
    """
    logger.info(f"Scan alert request received from user {current_user.get('user_id')} (Tenant: {current_tenant}): {request_data.dict()}")

    # --- F.2: Integrate Billing Middleware (for scan alerts) ---
    try:
        enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="scan_alert")
        logger.info(f"Billing limits checked for user {current_user.get('user_id')}. Proceeding.")
    except BillingException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during billing check for scan alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during billing check.")
    # --- End F.2 ---

    # Call the scan alert system
    result = await scan_alert_system.trigger_scan_alert(
        request_data.qr_code_id,
        request_data.location_data,
        request_data.device_type,
        request_data.user_settings
    )

    if result.get("status") == "alert_triggered":
        logger.info(f"Scan alert triggered successfully for QR code: {result.get('qr_code_id')}")
        return {"status": "success", "qr_code_id": result.get('qr_code_id'), "message": "Scan alert triggered."}
    else:
        raise HTTPException(status_code=500, detail=f"Scan alert failed: {result.get('message', 'Unknown error')}")

@app.post("/crm_push_contact")
async def crm_push_contact_endpoint(request_data: CRMPushContactRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    """
    // [TASK]: CRM push contact endpoint
    // [GOAL]: Expose CRM integration service via API
    """
    logger.info(f"CRM push contact request received from user {current_user.get('user_id')} (Tenant: {current_tenant}): {request_data.dict()}")

    # --- F.2: Integrate Billing Middleware (for CRM push) ---
    try:
        enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="crm_push_contact")
        logger.info(f"Billing limits checked for user {current_user.get('user_id')}. Proceeding.")
    except BillingException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during billing check for CRM push: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during billing check.")
    # --- End F.2 ---

    # Call the CRM integration service
    result = await crm_integration_service.push_contact_to_crm(request_data.crm_name, request_data.contact_data)

    if result.get("status") == "success":
        logger.info(f"Contact pushed to CRM successfully: {result.get('crm_response')}")
        return {"status": "success", "crm_response": result.get('crm_response'), "message": "Contact push to CRM initiated."}
    else:
        raise HTTPException(status_code=500, detail=f"Contact push to CRM failed: {result.get('message', 'Unknown error')}")

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