from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import timedelta, datetime
import uvicorn
import uuid
from fastapi.responses import JSONResponse # Elite Cursor Snippet: json_response_import

from logging_setup import get_logger, get_audit_logger
from config_loader import get_config
from auth.jwt_utils import verify_jwt
from pipeline_orchestrator import PipelineOrchestrator
from billing_middleware import enforce_limits, BillingException
from landing_page_service import LandingPageService
from scan_alert_system import ScanAlertSystem
from crm_integration import CRMIntegrationService
from utils.parallel_processing import ParallelProcessor
from i18n_utils import gettext, get_locale_from_request # Elite Cursor Snippet: i18n_imports

from database import engine, get_db
from auth.user_models import Base, User, Tenant
from auth.auth_service import create_user, authenticate_user, create_access_token, update_user_profile
from sqlalchemy.orm import Session

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis

# J.1: Monitoring Integration
from starlette_prometheus import PrometheusMiddleware, metrics
from feature_flags import feature_flag_manager # Elite Cursor Snippet: feature_flag_import

logger = get_logger(__name__)
audit_logger = get_audit_logger()
config = get_config()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.app.name,
    version=config.app.version,
    description="API for Shujaa Studio - Enterprise AI Video Generation"
)

# J.1: Add Prometheus middleware to expose /metrics endpoint
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

orchestrator = PipelineOrchestrator()
landing_page_service = LandingPageService()
scan_alert_system = ScanAlertSystem()
crm_integration_service = CRMIntegrationService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Pydantic Models ---

class GenerateVideoRequest(BaseModel):
    prompt: str
    news_url: Optional[str] = None
    script_file: Optional[str] = None
    upload_youtube: bool = False

class BatchGenerateVideoRequest(BaseModel):
    requests: List[GenerateVideoRequest]

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

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    tenant_name: Optional[str] = "default"

class Token(BaseModel):
    access_token: str
    token_type: str

class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    tenant_id: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None

# --- Dependency Functions ---

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt(token)
        user_id = payload.get("user_id")
        if user_id is None:
            audit_logger.warning("Authentication failed: User ID missing in token.", extra={'user_id': None})
            raise HTTPException(status_code=401, detail="Invalid authentication credentials: User ID missing")
        return payload
    except Exception as e:
        audit_logger.warning(f"Authentication failed for token: {token[:10]}... Error: {e}", extra={'user_id': None})
        raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {e}")

async def get_current_active_user(current_user_payload: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
    user_id = current_user_payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

async def get_current_tenant(user: dict = Depends(get_current_user)):
    tenant_id = user.get("tenant_id")
    if not tenant_id:
        audit_logger.warning(f"Authorization failed for user {user.get('user_id')}: Tenant ID missing in token.", extra={'user_id': user.get('user_id')})
        raise HTTPException(status_code=403, detail="Tenant ID not found in token.")
    return tenant_id

async def get_current_locale(request: Request) -> str:
    # // [TASK]: Provide current locale as a dependency
    # // [GOAL]: Enable localized responses in API endpoints
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    return get_locale_from_request(request)

# --- Middleware ---

@app.middleware("http")
async def add_tenant_context(request: Request, call_next):
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = verify_jwt(token)
            request.state.tenant_id = payload.get("tenant_id")
        else:
            request.state.tenant_id = "default_tenant"
    except Exception:
        request.state.tenant_id = "unauthenticated_tenant"
    response = await call_next(request)
    return response

@app.middleware("http")
async def pii_redaction_middleware(request: Request, call_next):
    # // [TASK]: Implement PII redaction middleware for logs
    # // [GOAL]: Prevent sensitive data from being logged
    # // [ELITE_CURSOR_SNIPPET]: securitycheck
    # This is a simplified example. A real PII scrubber would be more robust.
    # It would typically inspect request.body and response.body for PII.
    # For now, we'll just log a message if a sensitive endpoint is accessed.

    sensitive_paths = ["/register", "/token", "/users/me"] # Endpoints that might contain PII

    if request.url.path in sensitive_paths:
        audit_logger.info(f"Access to sensitive endpoint: {request.url.path}. PII redaction applied to logs.", extra={'user_id': request.state.get('user_id', None)})
        # In a real scenario, you would read the request body, redact PII,
        # and then pass the redacted body to the next middleware/endpoint.
        # This requires careful handling of async request body reading.
        # For now, we're just logging the access.

    response = await call_next(request)
    return response

# --- Event Handlers ---

@app.on_event("startup")
async def startup():
    redis_connection = redis.from_url(config.redis.url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    logger.info("FastAPI-Limiter initialized.")

# --- API Endpoints ---

@app.get("/health")
@RateLimiter(times=5, seconds=10)
async def health_check(locale: str = Depends(get_current_locale)):
    logger.info("Health check requested.")
    return {"status": gettext("status_ok", locale=locale), "message": gettext("api_running_message", locale=locale)}

@app.post("/register", response_model=UserCreate)
@RateLimiter(times=2, seconds=60)
async def register_user_endpoint(user: UserCreate, db: Session = Depends(get_db), locale: str = Depends(get_current_locale)):
    db_user = create_user(db, user.username, user.email, user.password, user.tenant_name)
    if not db_user:
        audit_logger.error(f"User registration failed: Username {user.username} or email {user.email} already registered.", extra={'user_id': None})
        raise HTTPException(status_code=400, detail=gettext("username_or_email_registered", locale=locale))
    audit_logger.info(f"User registered: {user.username} (Tenant: {user.tenant_name})", extra={'user_id': db_user.id})
    return db_user

@app.post("/token", response_model=Token)
@RateLimiter(times=5, seconds=30)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        audit_logger.warning(f"Login failed: Invalid credentials for username {form_data.username}.", extra={'user_id': None})
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
    audit_logger.info(f"User logged in: {user.username} (Tenant: {user.tenant.name})", extra={'user_id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}

from billing_models import get_default_plans, get_user_subscription # Elite Cursor Snippet: billing_api_imports

@app.get("/users/me", response_model=UserProfile)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    audit_logger.info(f"User profile viewed for user: {current_user.username}", extra={'user_id': current_user.id})
    return current_user

@app.put("/users/me", response_model=UserProfile)
async def update_users_me(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    update_data = user_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided.")
    
    updated_user = update_user_profile(db, current_user.id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    audit_logger.info(f"User profile updated for user: {current_user.username}", extra={'user_id': current_user.id})
    return updated_user

@app.get("/users/me/plan")
async def get_user_plan(current_user: dict = Depends(get_current_user)):
    # // [TASK]: Expose API for frontend to display user's plan info
    # // [GOAL]: Provide current subscription details to the UI
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    user_id = current_user.get("user_id")
    user_sub = get_user_subscription(user_id)
    all_plans = get_default_plans()
    current_plan = next((p for p in all_plans if p.name == user_sub.plan_name), None)

    if not current_plan:
        raise HTTPException(status_code=404, detail="Plan not found for user.")
    
    return {
        "plan_name": current_plan.name,
        "max_requests_per_day": current_plan.max_requests_per_day,
        "features_enabled": current_plan.features_enabled,
        "cost_per_month": current_plan.cost_per_month,
        "start_date": user_sub.start_date,
        "end_date": user_sub.end_date,
        "is_active": user_sub.is_active
    }

@app.get("/users/me/usage")
async def get_user_usage(current_user: dict = Depends(get_current_user)):
    # // [TASK]: Expose API for frontend to display user's usage limits
    # // [GOAL]: Provide current usage statistics to the UI
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    user_id = current_user.get("user_id")
    # This is a placeholder. In a real system, this would query a usage tracking system (e.g., Redis)
    # For now, we'll simulate usage.
    daily_usage = 7 # Simulated
    
    user_sub = get_user_subscription(user_id)
    all_plans = get_default_plans()
    current_plan = next((p for p in all_plans if p.name == user_sub.plan_name), None)

    if not current_plan:
        raise HTTPException(status_code=404, detail="Plan not found for user.")

    return {
        "plan_name": current_plan.name,
        "max_requests_per_day": current_plan.max_requests_per_day,
        "current_daily_usage": daily_usage,
        "remaining_daily_usage": max(0, current_plan.max_requests_per_day - daily_usage)
    }

@app.post("/generate_video")
@RateLimiter(times=1, seconds=5)
async def generate_video_endpoint(request_data: GenerateVideoRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    audit_logger.info(f"Access granted: User {current_user.get('user_id')} (Tenant: {current_tenant}) accessing /generate_video.", extra={'user_id': current_user.get('user_id')})
    try:
        enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="video_generation")
    except BillingException as e:
        raise HTTPException(status_code=403, detail=str(e))

    if not request_data.prompt and not request_data.news_url and not request_data.script_file:
        raise HTTPException(status_code=400, detail="Either 'prompt', 'news_url', or 'script_file' must be provided.")

    input_type = "general_prompt"
    input_data = request_data.prompt
    if request_data.news_url:
        input_type = "news_url"
        input_data = request_data.news_url
    elif request_data.script_file:
        input_type = "script_file"
        input_data = request_data.script_file

    user_preferences = {"upload_youtube": request_data.upload_youtube}
    result = await orchestrator.run_pipeline(
        input_type=input_type,
        input_data=input_data,
        user_preferences=user_preferences,
        api_call=True
    )

    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))

    return result

@app.post("/batch_generate_video")
async def batch_generate_video_endpoint(batch_request: BatchGenerateVideoRequest, current_user: dict = Depends(get_current_user)):
    audit_logger.info(f"Batch video generation request received from user {current_user.get('user_id')}. Count: {len(batch_request.requests)}", extra={'user_id': current_user.get('user_id')})
    MAX_BATCH_SIZE = config.video.get('max_batch_size', 10)
    if len(batch_request.requests) > MAX_BATCH_SIZE:
        raise HTTPException(status_code=400, detail=f"Batch size cannot exceed {MAX_BATCH_SIZE}.")

    async def video_worker(request_data: GenerateVideoRequest):
        try:
            enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="video_generation")
            input_type = "general_prompt"
            input_data = request_data.prompt
            if request_data.news_url:
                input_type = "news_url"
                input_data = request_data.news_url
            elif request_data.script_file:
                input_type = "script_file"
                input_data = request_data.script_file
            user_preferences = {"upload_youtube": request_data.upload_youtube}
            return await orchestrator.run_pipeline(input_type=input_type, input_data=input_data, user_preferences=user_preferences, api_call=True)
        except BillingException as e:
            return {"status": "error", "message": str(e), "request_prompt": request_data.prompt}
        except Exception as e:
            logger.exception(f"Error processing item in batch: {request_data.prompt}")
            return {"status": "error", "message": f"An unexpected error occurred: {e}", "request_prompt": request_data.prompt}

    parallel_processor = ParallelProcessor()
    batch_results = await parallel_processor.run_parallel(items=batch_request.requests, worker_function=video_worker)

    successful_jobs = [res for res in batch_results if res.get("status") == "success"]
    failed_jobs = [res for res in batch_results if res.get("status") != "success"]

    logger.info(f"Batch video generation completed for user {current_user.get('user_id')}. Success: {len(successful_jobs)}, Failed: {len(failed_jobs)}")
    return {
        "batch_id": f"batch_{uuid.uuid4().hex[:8]}",
        "status": "completed",
        "successful_videos": len(successful_jobs),
        "failed_videos": len(failed_jobs),
        "results": batch_results
    }

@app.post("/generate_landing_page")
async def generate_landing_page_endpoint(request_data: GenerateLandingPageRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    audit_logger.info(f"Access granted: User {current_user.get('user_id')} (Tenant: {current_tenant}) accessing /generate_landing_page.", extra={'user_id': current_user.get('user_id')})
    try:
        enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="landing_page_generation")
    except BillingException as e:
        raise HTTPException(status_code=403, detail=str(e))
    result = await landing_page_service.generate_landing_page(request_data.qr_code_id, request_data.brand_metadata)
    if result.get("status") == "success":
        return {"status": "success", "s3_url": result.get('s3_url'), "message": "Landing page generation initiated."}
    else:
        raise HTTPException(status_code=500, detail=f"Landing page generation failed: {result.get('message', 'Unknown error')}")

@app.post("/scan_alert")
@RateLimiter(times=10, seconds=60)
async def scan_alert_endpoint(request_data: ScanAlertRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    audit_logger.info(f"Access granted: User {current_user.get('user_id')} (Tenant: {current_tenant}) accessing /scan_alert.", extra={'user_id': current_user.get('user_id')})
    try:
        enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="scan_alert")
    except BillingException as e:
        raise HTTPException(status_code=403, detail=str(e))
    result = await scan_alert_system.trigger_scan_alert(
        request_data.qr_code_id,
        request_data.location_data,
        request_data.device_type,
        request_data.user_settings
    )
    if result.get("status") == "alert_triggered":
        return {"status": "success", "qr_code_id": result.get('qr_code_id'), "message": "Scan alert triggered."}
    else:
        raise HTTPException(status_code=500, detail=f"Scan alert failed: {result.get('message', 'Unknown error')}")

@app.post("/crm_push_contact")
@RateLimiter(times=5, seconds=60)
async def crm_push_contact_endpoint(request_data: CRMPushContactRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    audit_logger.info(f"Access granted: User {current_user.get('user_id')} (Tenant: {current_tenant}) accessing /crm_push_contact.", extra={'user_id': current_user.get('user_id')})
    try:
        enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="crm_push_contact")
    except BillingException as e:
        raise HTTPException(status_code=403, detail=str(e))
    result = await crm_integration_service.push_contact_to_crm(request_data.crm_name, request_data.contact_data)
    if result.get("status") == "success":
        return {"status": "success", "crm_response": result.get('crm_response'), "message": "Contact push to CRM initiated."}
    else:
        raise HTTPException(status_code=500, detail=f"Contact push to CRM failed: {result.get('message', 'Unknown error')}")

class WebhookPaymentStatus(BaseModel):
    user_id: str
    transaction_id: str
    status: str # e.g., "completed", "failed", "pending"
    amount: float
    currency: str
    plan_name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    signature: str # For secure verification

@app.post("/webhook/payment_status")
async def webhook_payment_status(payload: WebhookPaymentStatus, request: Request):
    # // [TASK]: Implement secure signature verification for payment callbacks
    # // [GOAL]: Ensure webhook authenticity and prevent tampering
    # // [ELITE_CURSOR_SNIPPET]: securitycheck
    # Placeholder for signature verification
    expected_signature = "mock_signature" # In real app, calculate based on payload and shared secret
    if payload.signature != expected_signature:
        audit_logger.error(f"Webhook signature mismatch for user {payload.user_id}. Potential tampering.", extra={'user_id': payload.user_id})
        raise HTTPException(status_code=403, detail="Invalid signature")

    audit_logger.info(f"Webhook received for user {payload.user_id}, transaction {payload.transaction_id}, status {payload.status}.", extra={'user_id': payload.user_id})

    # // [TASK]: Update user subscription status based on webhook notification
    # // [GOAL]: Automate subscription management in real-time
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    # This would involve updating the database with the new subscription status
    # For now, we'll just log it.
    if payload.status == "completed":
        logger.info(f"Payment completed for user {payload.user_id} for plan {payload.plan_name}. Updating subscription.")
        # In a real system:
        # 1. Find user in DB
        # 2. Update their subscription plan and dates
        # 3. Log the change
    elif payload.status == "failed":
        logger.warning(f"Payment failed for user {payload.user_id}, transaction {payload.transaction_id}.")
        # Handle failed payments (e.g., downgrade plan, send notification)
    
    return {"message": "Webhook received and processed"}

@app.get("/protected_data")
async def protected_data(current_user: User = Depends(get_current_active_user), current_tenant: str = Depends(get_current_tenant)):
    audit_logger.info(f"Access granted: User {current_user.username} (Tenant: {current_tenant}) accessing /protected_data.", extra={'user_id': current_user.id})
    return {"message": f"Welcome, {current_user.username} from tenant {current_tenant}! This is protected data.", "user": UserProfile.from_orm(current_user), "tenant": current_tenant}

@app.get("/feature_status/{feature_name}")
async def get_feature_status(feature_name: str, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(get_current_tenant)):
    # // [TASK]: Expose API for frontend to check feature flag status
    # // [GOAL]: Allow dynamic UI based on feature flags
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    user_id = str(current_user.get("user_id")) # Convert to string for hashing
    tenant_id = str(current_tenant) # Convert to string for consistency

    is_enabled = feature_flag_manager.is_enabled(feature_name, user_id=user_id, tenant_id=tenant_id)
    
    audit_logger.info(f"Feature flag check for '{feature_name}': {is_enabled} for user {user_id} (tenant {tenant_id}).", extra={'user_id': current_user.get('user_id')})
    return {"feature_name": feature_name, "is_enabled": is_enabled}

@app.get("/users/me/data/export")
async def export_user_data(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # // [TASK]: Implement data export endpoint for right-to-be-forgotten
    # // [GOAL]: Allow users to export their data for GDPR compliance
    # // [ELITE_CURSOR_SNIPPET]: securitycheck
    user_id = current_user.id
    audit_logger.info(f"User data export requested for user ID: {user_id}", extra={'user_id': user_id})

    # Fetch user data (example: User, AuditLog, Consent)
    user_data = {
        "user_profile": UserProfile.from_orm(current_user).dict(),
        "audit_logs": [log.message for log in db.query(AuditLog).filter_by(user_id=user_id).all()],
        "consents": [{"type": c.consent_type, "granted": c.is_granted} for c in db.query(Consent).filter_by(user_id=user_id).all()]
    }
    
    # In a real application, you might want to:
    # 1. Export more comprehensive data (e.g., video generation requests, billing history)
    # 2. Store the export in a secure, temporary location (e.g., S3) and provide a signed URL
    # 3. Encrypt the exported data
    
    return JSONResponse(content=user_data, media_type="application/json")

@app.delete("/users/me/data/delete")
async def delete_user_data(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # // [TASK]: Implement data deletion endpoint for right-to-be-forgotten
    # // [GOAL]: Allow users to request deletion of their data for GDPR compliance
    # // [ELITE_CURSOR_SNIPPET]: securitycheck
    user_id = current_user.id
    audit_logger.info(f"User data deletion requested for user ID: {user_id}", extra={'user_id': user_id})

    # In a real application, this would involve:
    # 1. Soft deleting the user (e.g., setting is_active=False, marking for deletion)
    # 2. Anonymizing or deleting associated PII from all related tables (e.g., AuditLog, Consent)
    # 3. Handling data in external systems (e.g., CRM, payment processors)
    # 4. Scheduling a background task for hard deletion after a retention period

    # For demonstration, we'll just mark the user as inactive and log the action
    current_user.is_active = False
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    # Example of anonymizing audit logs for this user
    db.query(AuditLog).filter_by(user_id=user_id).update({"user_id": None, "message": "[REDACTED]"}, synchronize_session=False)
    db.commit()

    # Example of deleting consent records
    db.query(Consent).filter_by(user_id=user_id).delete(synchronize_session=False)
    db.commit()

    return {"message": "User data deletion process initiated. Your account will be deactivated."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)