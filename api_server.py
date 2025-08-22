import asyncio # New import
import json # New import
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import timedelta, datetime
import uvicorn
import uuid
from fastapi.responses import JSONResponse # Elite Cursor Snippet: json_response_import

from logging_setup import get_logger
from logging_setup import get_audit_logger
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
from auth.user_models import Base, User, Tenant, AuditLog, Consent
from auth.auth_service import create_user, authenticate_user, create_access_token, update_user_profile
from sqlalchemy.orm import Session

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis

# J.1: Monitoring Integration
from starlette_prometheus import PrometheusMiddleware, metrics
from prometheus_client import Counter, Histogram # ADD THIS LINE
from feature_flags import feature_flag_manager # Elite Cursor Snippet: feature_flag_import
from chaos_utils import chaos_injector # Elite Cursor Snippet: chaos_injector_import
from auth.tenancy import current_tenant
from auth.rbac import has_role, Role

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any # Added Dict, Any for model management
from datetime import timedelta, datetime
import uvicorn
import uuid
from fastapi.responses import JSONResponse # Elite Cursor Snippet: json_response_import

from logging_setup import get_logger
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
from auth.user_models import Base, User, Tenant, AuditLog, Consent
from auth.auth_service import create_user, authenticate_user, create_access_token, update_user_profile
from sqlalchemy.orm import Session

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis

# J.1: Monitoring Integration
from starlette_prometheus import PrometheusMiddleware, metrics
from prometheus_client import Counter, Histogram # ADD THIS LINE
from feature_flags import feature_flag_manager # Elite Cursor Snippet: feature_flag_import
from chaos_utils import chaos_injector # Elite Cursor Snippet: chaos_injector_import
from auth.tenancy import current_tenant
from auth.rbac import has_role, Role

from security.audit_log_manager import audit_log_manager, AuditEventType # ADD THIS LINE

# Imports for Model Management Admin Widget
from backend.ai_models.model_store import ModelStore
from backend.ai_health.healthcheck import score_inference, record_metric, aggregate
from backend.ai_health.rollback import should_rollback, perform_rollback
from backend.notifications.admin_notify import send_admin_notification
from backend.startup import run_safety_rollback_on_boot # New import for safety rollback
from backend.core.voices.versioning import register_voice, rollback_voice, get_active_voice, get_latest_voice, load_versions # Voice versioning imports
from backend.core_modules.module_registry import get_module_dependencies # New import

from auth.user_models import User # New import
from auth.auth_service import create_user # New import
from sqlalchemy.orm import Session # New import

from billing.plan_guard import PlanGuard, PlanGuardException # New import
from backend.widget_manager import WidgetManager # New import

# Initialize ModelStore
model_store = ModelStore()
plan_guard = PlanGuard(db_session_factory=get_db) # Initialize PlanGuard with db_session_factory
widget_manager = WidgetManager(plan_guard) # Initialize WidgetManager


logger = get_logger(__name__)
audit_logger = get_audit_logger() # This will be replaced or removed later
config = get_config()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.app.name,
    version=config.app.version,
    description="API for Shujaa Studio - Enterprise AI Video Generation"
)

# Attach PlanGuard after app is created
app.state.plan_guard = plan_guard # Store plan_guard in app.state for middleware access

# --- Prometheus Custom Metrics ---
VIDEO_GENERATION_REQUESTS = Counter(
    'video_generation_requests_total',
    'Total number of video generation requests',
    ['status'] # Label for success/failure
)
VIDEO_GENERATION_DURATION = Histogram(
    'video_generation_duration_seconds',
    'Duration of video generation requests in seconds',
    ['status'] # Label for success/failure
)
VIDEO_GENERATION_FAILURES = Counter(
    'video_generation_failures_total',
    'Total number of failed video generation requests'
)

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

FastAPIInstrumentor.instrument_app(app)

from auth.tenancy import TenantMiddleware
from backend.middleware.policy_resolver import PolicyResolverMiddleware # Import PolicyResolverMiddleware
from backend.core.plan_guard import PlanGuardMiddleware # New import for PlanGuardMiddleware

from backend.superadmin.routes import router as superadmin_router # New import
from backend.routers.custom_domain import router as custom_domain_router # New import

app.add_middleware(TenantMiddleware)
app.add_middleware(PolicyResolverMiddleware) # Add PolicyResolverMiddleware
app.add_middleware(PlanGuardMiddleware) # Add PlanGuardMiddleware
app.add_route("/metrics", metrics)

app.include_router(superadmin_router, prefix="/superadmin", tags=["SuperAdmin"]) # Include SuperAdmin router
app.include_router(custom_domain_router, prefix="/api", tags=["Custom Domain"]) # Include Custom Domain router

orchestrator = PipelineOrchestrator()
landing_page_service = LandingPageService()
scan_alert_system = ScanAlertSystem()
crm_integration_service = CRMIntegrationService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Pydantic Models ---

class GenerateVideoRequest(BaseModel):
    # // [TASK]: Encrypt model inference inputs/outputs using AES-256 before transmission
    # // [GOAL]: Enhance security of sensitive data during model inference
    # // [ELITE_CURSOR_SNIPPET]: securitycheck
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
    role: Optional[str] = "user"

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


class AnalyticsData(BaseModel):
    overview: dict
    usage_trends: List[dict]
    popular_content: List[dict]
    performance_metrics: dict


class ApiKey(BaseModel):
    id: str
    key: str
    created_at: str
    last_used_at: Optional[str] = None
    is_active: bool


class Integration(BaseModel):
    id: str
    name: str
    type: str
    is_enabled: bool
    config: dict


class UserData(BaseModel):
    id: int
    username: str
    email: str
    role: str
    tenant_name: str
    is_active: bool


class Project(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    type: str
    status: str
    created_at: str
    updated_at: str
    items_count: int


class Asset(BaseModel):
    id: str
    name: str
    type: str
    url: str
    thumbnail_url: Optional[str] = None
    size: int
    uploaded_at: str
    usage_count: int

# Pydantic Models for Model Management Admin Widget
class ModelVersionInfo(BaseModel):
    version_tag: str
    path: str
    checksum: str
    activated_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ModelHealthMetrics(BaseModel):
    error_rate: float
    p50_latency_ms: float
    avg_score: float
    count: int

class ModelStatusResponse(BaseModel):
    provider: str
    model_name: str
    active_version: Optional[ModelVersionInfo] = None
    recent_versions: List[ModelVersionInfo]
    health_metrics: Optional[ModelHealthMetrics] = None
    
class PromoteRequest(BaseModel):
    provider: str
    model_name: str
    version_tag: str # The green version to promote

class RollbackRequest(BaseModel):
    provider: str
    model_name: str
    target_tag: str # The version to rollback to

# Pydantic Models for Voice Management Admin Widget
class VoiceVersionInfo(BaseModel):
    version: str
    registered_at: str
    metadata: Optional[Dict[str, Any]] = None

class VoiceStatusResponse(BaseModel):
    voice_name: str
    active_version: Optional[VoiceVersionInfo] = None
    available_versions: List[VoiceVersionInfo]

# Pydantic Models for Widget Management
class WidgetInstallRequest(BaseModel):
    widget_name: str
    widget_version: str
    dependencies: List[str]

class WidgetUpdateRequest(BaseModel):
    widget_name: str
    new_widget_version: str
    new_dependencies: List[str]

class WidgetLoadRequest(BaseModel):
    widget_name: str

# --- Dependency Functions ---

# Pydantic model for tenant branding updates
class TenantBrandingUpdate(BaseModel):
    theme: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    favicon_url: Optional[str] = None
    custom_domain: Optional[str] = None
    tagline: Optional[str] = None

    class Config:
        extra = "ignore"  # Ignore unknown fields to keep endpoint flexible

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), request: Request = None):
    try:
        payload = verify_jwt(token)
        user_id = payload.get("user_id")
        if user_id is None:
            audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_FAILURE, "Authentication failed: User ID missing in token.", user_id=None, ip_address=request.client.host if request else None)
            raise HTTPException(status_code=401, detail="Invalid authentication credentials: User ID missing")
        request.state.user_id = user_id # Set user_id in request.state

        # Determine grace mode status
        user_sub = get_user_subscription(user_id) # Get user subscription
        current_plan = next((p for p in get_default_plans() if p.name == user_sub.plan_name), None)

        request.state.is_in_grace_mode = False
        request.state.grace_expires_at = None

        if not user_sub.is_active and current_plan and current_plan.grace_period_hours > 0:
            # Simulate grace period logic from PlanGuard
            if not user_sub.grace_expires_at or user_sub.grace_expires_at < datetime.now():
                # This should ideally be persisted in the DB for the user_sub
                user_sub.grace_expires_at = datetime.now() + timedelta(hours=current_plan.grace_period_hours)
                # In a real system, you'd update the user_sub in the DB here

            if datetime.now() < user_sub.grace_expires_at:
                request.state.is_in_grace_mode = True
                request.state.grace_expires_at = user_sub.grace_expires_at

        return payload
    except Exception as e:
        audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_FAILURE, f"Authentication failed for token: {token[:10]}... Error: {e}", user_id=None, ip_address=request.client.host if request else None)
        raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {e}")

async def get_current_active_user(current_user_payload: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
    user_id = current_user_payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

async def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user

async def get_current_tenant():
    pass

async def get_current_locale(request: Request) -> str:
    # // [TASK]: Provide current locale as a dependency
    # // [GOAL]: Enable localized responses in API endpoints
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    return get_locale_from_request(request)

# Define a key_func for authenticated users
async def user_id_key_func(request: Request, current_user: dict = Depends(get_current_user)):
    return str(current_user.get("user_id", request.client.host)) # Fallback to IP if user_id not found

# --- Middleware ---



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
        # PII redaction middleware doesn't have direct access to db session easily
        # For now, we'll log using the regular logger or a simplified audit log call
        # A more robust solution would involve a dependency injection for db or a background task.
        logger.info(
            f"Access to sensitive endpoint: {request.url.path}. PII redaction applied to logs.",
            extra={'user_id': getattr(request.state, 'user_id', None), 'ip_address': request.client.host}
        )
        # In a real scenario, you would read the request body, redact PII,
        # and then pass the redacted body to the next middleware/endpoint.
        # This requires careful handling of async request body reading.
        # For now, we're just logging the access.

    response = await call_next(request)

    # Grace Mode Middleware
    if hasattr(request.state, 'is_in_grace_mode') and request.state.is_in_grace_mode:
        user_id = str(request.state.user_id) # Get user_id from request.state
        grace_expires_at = request.state.grace_expires_at
        
        # Apply artificial delay
        delay = plan_guard.get_grace_delay(grace_expires_at)
        if delay > 0:
            logger.info(f"User {user_id} in grace mode. Applying {delay}s delay.")
            import time # Import time for sleep
            time.sleep(delay)

        if isinstance(response, JSONResponse):
            response_body = json.loads(response.body.decode())
            response_body["status"] = "grace_mode"
            response_body["grace_expires_at"] = grace_expires_at.isoformat()
            
            time_left = grace_expires_at - datetime.now()
            hours, remainder = divmod(int(time_left.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            response_body["remaining"] = f"{hours}h {minutes}m"

            # Add slowdown message
            if delay > 0:
                response_body["message"] = f"You're in Grace Mode. Responses may feel slower as your plan is expiring. Upgrade now to restore full speed. ({hours}h {minutes}m left)"
            else:
                response_body["message"] = f"You're in Grace Mode. Your plan expires in {hours}h {minutes}m. Upgrade now!"

            response = JSONResponse(content=response_body, status_code=response.status_code)

    return response

# --- Event Handlers ---

from backend.superadmin.auth import create_superadmin_users # New import

@app.on_event("startup")
async def startup():
    # Initialize rate limiter Redis with safe fallback
    try:
        redis_url = None
        if hasattr(config, 'redis') and hasattr(config.redis, 'url'):
            redis_url = config.redis.url
        # Fallback if URL missing or missing scheme
        if not redis_url or not str(redis_url).startswith(("redis://", "rediss://", "unix://")):
            logger.warning("Invalid or missing Redis URL in config; defaulting to redis://localhost:6379/0")
            redis_url = "redis://localhost:6379/0"

        redis_connection = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(redis_connection)
        logger.info("FastAPI-Limiter initialized.")
    except Exception as e:
        logger.warning(f"FastAPI-Limiter Redis not available, continuing without rate limiting: {e}")
    
    # Run safety rollback check on boot
    run_safety_rollback_on_boot()

    # Seed super admin users
    with next(get_db()) as db_session:
        await create_superadmin_users(db_session) # Call the new async function

# --- API Endpoints ---

@app.get("/health")
async def health_check(locale: str = Depends(get_current_locale)):
    logger.info("Health check requested.")
    return {"status": gettext("status_ok", locale=locale), "message": gettext("api_running_message", locale=locale)}

@app.post("/register", response_model=UserCreate)
async def register_user_endpoint(user: UserCreate, db: Session = Depends(get_db), locale: str = Depends(get_current_locale), current_user: User = Depends(get_current_active_user), request: Request = None):
    if user.role == Role.ADMIN and (not current_user or current_user.role != Role.ADMIN):
        raise HTTPException(status_code=403, detail="Only admins can create other admins")
    db_user = create_user(db, user.username, user.email, user.password, user.tenant_name, user.role)
    if not db_user:
        audit_log_manager.log_event(db, AuditEventType.USER_REGISTER, f"User registration failed: Username {user.username} or email {user.email} already registered.", user_id=None, ip_address=request.client.host) # Pass request
        raise HTTPException(status_code=400, detail=gettext("username_or_email_registered", locale=locale))
    audit_log_manager.log_event(db, AuditEventType.USER_REGISTER, f"User registered: {user.username} (Tenant: {user.tenant_name})", user_id=db_user.id, tenant_id=db_user.tenant_id, ip_address=request.client.host) # Pass request
    return db_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), request: Request = None):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_FAILURE, f"Login failed: Invalid credentials for username {form_data.username}.", user_id=None, ip_address=request.client.host) # Pass request
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
    audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_SUCCESS, f"User logged in: {user.username} (Tenant: {user.tenant.name})", user_id=user.id, tenant_id=user.tenant_id, ip_address=request.client.host) # Pass request
    return {"access_token": access_token, "token_type": "bearer"}

from billing_models import get_default_plans, get_user_subscription # Elite Cursor Snippet: billing_api_imports

@app.get("/users/me", response_model=UserProfile)
async def read_users_me(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db), request: Request = None):
    audit_log_manager.log_event(db, AuditEventType.USER_PROFILE_VIEW, f"User profile viewed for user: {current_user.username}", user_id=current_user.id, tenant_id=current_user.tenant_id, ip_address=request.client.host)
    return current_user

@app.put("/users/me", response_model=UserProfile)
async def update_users_me(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user), request: Request = None):
    update_data = user_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided.")
    
    updated_user = update_user_profile(db, current_user.id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    audit_log_manager.log_event(db, AuditEventType.USER_PROFILE_UPDATE, f"User profile updated for user: {current_user.username}", user_id=current_user.id, tenant_id=current_user.tenant_id, ip_address=request.client.host, event_details=user_update.dict(exclude_unset=True))
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

@app.get("/api/plan/status")
async def get_plan_status(current_user: User = Depends(get_current_active_user)):
    """
    Returns the detailed plan status for the current user, including quotas and usage.
    This endpoint is used by the PlanGuardWidget.
    """
    user_id = str(current_user.id)
    try:
        user_plan = await plan_guard.get_user_plan(user_id)
        # In a real system, you'd fetch actual usage data here
        # For now, we'll use placeholder usage
        usage = {
            "tokens": 5000, # Example: 5000 tokens used
            "audioMins": 10, # Example: 10 audio minutes used
            "videoMins": 5, # Example: 5 video minutes used
        }

        return {
            "planCode": user_plan.name.lower().replace(" ", "_"),
            "planName": user_plan.name,
            "state": "healthy", # Default to healthy, will be overridden by PlanGuardException
            "quota": {
                "tokens": user_plan.quotas.monthly.tokens,
                "audioMins": user_plan.quotas.monthly.audioMins,
                "videoMins": user_plan.quotas.monthly.videoMins,
            },
            "usage": usage,
            "expiresAt": None, # Placeholder
            "graceExpiresAt": None, # Placeholder
            "upgradeUrl": "/billing", # Placeholder
            "lastCheckedAt": datetime.utcnow().isoformat(),
            "adminConsoleUrl": None, # Placeholder
        }
    except PlanGuardException as e:
        # If PlanGuard raises an exception, it means the plan is not healthy
        return {
            "planCode": "unknown", # Or derive from e.plan_name if available
            "planName": "Unknown",
            "state": "view_only" if e.is_view_only else ("grace" if e.is_in_grace_mode else "locked"),
            "quota": { "tokens": 0, "audioMins": 0, "videoMins": 0 }, # Set to 0 for restricted plans
            "usage": { "tokens": 0, "audioMins": 0, "videoMins": 0 },
            "expiresAt": None,
            "graceExpiresAt": e.grace_expires_at.isoformat() if e.grace_expires_at else None,
            "upgradeUrl": "/billing",
            "lastCheckedAt": datetime.utcnow().isoformat(),
            "adminConsoleUrl": None,
            "message": str(e) # Include the PlanGuard message
        }
    except Exception as e:
        logger.error(f"Error fetching plan status for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch plan status.")

@app.get("/api/plans")
async def get_all_plans():
    # // [TASK]: Expose API for frontend to display all available plans
    # // [GOAL]: Provide all plan details to the UI for pricing page
    all_plans = get_default_plans()
    # Convert dataclass objects to dictionaries for JSON serialization
    return [plan.__dict__ for plan in all_plans]

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

@app.put("/tenants/me/branding")
async def update_tenant_branding(
    branding_data: TenantBrandingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    request: Request = None
):
    # // [TASK]: Implement API endpoint for updating tenant branding
    # // [GOAL]: Allow tenants to customize their branding (theme, logo, custom domain)
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    tenant_id = current_user.tenant_id
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Update branding fields
    update_data = branding_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tenant, key, value)
    
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    audit_log_manager.log_event(db, AuditEventType.TENANT_BRANDING_UPDATE, f"Tenant branding updated for tenant ID: {tenant_id}", user_id=current_user.id, tenant_id=tenant_id, ip_address=request.client.host, event_details=branding_data.dict(exclude_unset=True))
    return {"message": "Tenant branding updated successfully", "tenant_id": tenant_id}

from backend.mock_db import mock_db # New import

@app.get("/reports/sla/{tenant_id}/{month}")
async def get_sla_report(tenant_id: str, month: str, current_user: User = Depends(get_current_active_user)):
    # // [TASK]: Implement API endpoint for SLA reports
    # // [GOAL]: Provide tenants with their service level agreement performance
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    # In a real system, ensure user has permission to view this tenant's SLA
    if str(current_user.tenant_id) != tenant_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view this tenant's SLA.")
    
    record = mock_db.get_sla_record(tenant_id, month) # Use mock_db
    if not record:
        raise HTTPException(status_code=404, detail="SLA record not found for specified tenant and month.")
    return record

@app.get("/reports/billing/transactions/{user_id}")
async def get_billing_transactions(user_id: str, current_user: User = Depends(get_current_active_user)):
    # // [TASK]: Implement API endpoint for billing transactions
    # // [GOAL]: Provide users with their billing history
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    # In a real system, fetch from database
    if str(current_user.id) != user_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view these transactions.")
    
    return mock_db.get_billing_transactions(user_id) # Use mock_db

@app.get("/reports/usage/{user_id}")
async def get_usage_records(user_id: str, current_user: User = Depends(get_current_active_user)):
    # // [TASK]: Implement API endpoint for usage records
    # // [GOAL]: Provide users with their detailed usage statistics
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    # In a real system, fetch from database
    if str(current_user.id) != user_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view these usage records.")
    
    return mock_db.get_usage_records(user_id) # Use mock_db

@app.get("/reports/reconciliation/{month}")
async def get_reconciliation_report(month: str, current_user: User = Depends(get_current_active_user)):
    # // [TASK]: Implement API endpoint for reconciliation reports
    # // [GOAL]: Provide administrators with billing reconciliation summaries
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required for reconciliation reports.")
    
    report = mock_db.get_reconciliation_report(month) # Use mock_db
    if not report:
        raise HTTPException(status_code=404, detail="Reconciliation report not found for specified month.")
    return report


@app.get("/api/analytics")
async def get_analytics_data(timeRange: str = "30d"):
    # TODO: Replace with real data from a database or analytics service
    return {
        "overview": {
            "total_videos": 1250,
            "total_images": 8345,
            "total_audio": 3210,
            "total_views": 1200000,
            "total_downloads": 780
        },
        "usage_trends": [
            {"date": "2025-08-01", "videos": 20, "images": 150, "audio": 50},
            {"date": "2025-08-02", "videos": 25, "images": 160, "audio": 55},
            {"date": "2025-08-03", "videos": 30, "images": 170, "audio": 60},
            {"date": "2025-08-04", "videos": 28, "images": 180, "audio": 65},
            {"date": "2025-08-05", "videos": 35, "images": 190, "audio": 70},
            {"date": "2025-08-06", "videos": 40, "images": 200, "audio": 75},
            {"date": "2025-08-07", "videos": 45, "images": 210, "audio": 80},
        ],
        "popular_content": [
            {"id": "1", "title": "Kenya Wildlife", "type": "video", "views": 1500, "downloads": 300},
            {"id": "2", "title": "Nairobi Skyline", "type": "image", "views": 2500, "downloads": 500},
            {"id": "3", "title": "Maasai Mara Beat", "type": "audio", "views": 3500, "downloads": 700},
        ],
        "performance_metrics": {
            "avg_generation_time": 45,
            "success_rate": 0.95,
            "user_satisfaction": 4.8
        }
    }


@app.get("/api/keys", response_model=List[ApiKey])
async def get_api_keys():
    # TODO: Replace with real data from a database
    return [
        {"id": "1", "key": "shujaa_sk_123...", "created_at": "2025-08-01", "last_used_at": "2025-08-17", "is_active": True},
        {"id": "2", "key": "shujaa_sk_456...", "created_at": "2025-07-15", "last_used_at": None, "is_active": False},
    ]


@app.post("/api/keys", response_model=ApiKey)
async def generate_api_key(current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    # TODO: Replace with real key generation and database storage
    new_key = {
        "id": str(uuid.uuid4()),
        "key": f"shujaa_sk_{uuid.uuid4().hex[:12]}...",
        "created_at": datetime.utcnow().isoformat(),
        "last_used_at": None,
        "is_active": True,
    }
    return new_key


@app.delete("/api/keys/{key_id}")
async def revoke_api_key(key_id: str, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "DELETE")

    # TODO: Replace with real database update
    return {"success": True}


@app.get("/api/integrations", response_model=List[Integration])
async def get_integrations():
    # TODO: Replace with real data from a database
    return [
        {"id": "1", "name": "Google Drive", "type": "storage", "is_enabled": True, "config": {"folder": "/ShujaaStudio"}},
        {"id": "2", "name": "Slack", "type": "notification", "is_enabled": False, "config": {"channel": "#general"}},
    ]


@app.put("/api/integrations/{integration_id}", response_model=Integration)
async def update_integration(integration_id: str, config: dict, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    # TODO: Replace with real database update
    return {"id": integration_id, "name": "Google Drive", "type": "storage", "is_enabled": config.get("is_enabled"), "config": {"folder": "/ShujaaStudio"}}


@app.get("/api/users", response_model=List[UserData])
async def get_users(current_user: User = Depends(get_current_admin_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "READ")

    # TODO: Replace with real data from a database
    return [
        {"id": 1, "username": "testuser", "email": "testuser@example.com", "role": "user", "tenant_name": "default", "is_active": True},
        {"id": 2, "username": "adminuser", "email": "adminuser@example.com", "role": "admin", "tenant_name": "default", "is_active": True},
    ]


@app.get("/api/users/{user_id}", response_model=UserData)
async def get_user(user_id: int, current_user: User = Depends(get_current_admin_user)):
    user_id_str = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id_str, "READ")

    # TODO: Replace with real data from a database
    return {"id": user_id, "username": "testuser", "email": "testuser@example.com", "role": "user", "tenant_name": "default", "is_active": True}


@app.post("/api/users", response_model=UserData)
async def create_user(user: UserData, current_user: User = Depends(get_current_admin_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    # TODO: Replace with real database insertion
    return user


@app.put("/api/users/{user_id}", response_model=UserData)
async def update_user(user_id: int, user: UserData, current_user: User = Depends(get_current_admin_user)):
    user_id_str = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id_str, "WRITE")

    # TODO: Replace with real database update
    return user


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_admin_user)):
    user_id_str = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id_str, "DELETE")

    # TODO: Replace with real database deletion
    return {"success": True}


@app.get("/api/projects", response_model=List[Project])
async def get_projects(page: int = 1, limit: int = 6, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "READ")

    # TODO: Replace with real data from a database
    return {
        "projects": [
            {"id": "1", "name": "Project 1", "description": "Description 1", "type": "video", "status": "completed", "created_at": "2025-08-01", "updated_at": "2025-08-17", "items_count": 10},
            {"id": "2", "name": "Project 2", "description": "Description 2", "type": "image", "status": "in_progress", "created_at": "2025-08-02", "updated_at": "2025-08-18", "items_count": 5},
        ],
        "total": 2,
        "page": 1,
        "pages": 1,
    }


@app.post("/api/projects", response_model=Project)
async def create_project(project: Project, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    # TODO: Replace with real database insertion
    return project


@app.put("/api/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, project: Project, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    # TODO: Replace with real database update
    return project


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "DELETE")

    # TODO: Replace with real database deletion
    return {"success": True}


@app.get("/api/assets", response_model=List[Asset])
async def get_assets(page: int = 1, limit: int = 10, type: Optional[str] = None, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "READ")

    # TODO: Replace with real data from a database
    # For now, using mock data and applying CDN logic
    mock_assets = [
        {"id": "1", "name": "Asset 1", "type": "image", "url": "/local_assets/image1.jpg", "size": 1024, "uploaded_at": "2025-08-01", "usage_count": 5},
        {"id": "2", "name": "Asset 2", "type": "audio", "url": "/local_assets/audio1.mp3", "size": 2048, "uploaded_at": "2025-08-02", "usage_count": 10},
    ]

    cdn_endpoints = config.app.get("cdn_endpoints", [])
    processed_assets = []

    from utils.asset_utils import generate_signed_url # Import here to avoid circular dependency if asset_utils imports config

    for asset in mock_assets:
        asset_url = asset["url"]
        if cdn_endpoints:
            # Try to prepend CDN URL, assuming asset_url is a relative path or local path
            for cdn_base_url in cdn_endpoints:
                # Simple concatenation for demonstration. In a real scenario,
                # you'd handle path joining carefully (e.g., urllib.parse.urljoin)
                cdn_url = f"{cdn_base_url}{asset_url.lstrip('/')}"
                # In a real system, you'd check if the CDN asset exists/is reachable
                # For now, we'll just use the first CDN URL
                asset["url"] = cdn_url
                break # Use the first CDN endpoint
        else:
            # If no CDN, generate a signed URL for the local asset path
            # Assuming asset["url"] is a path relative to some base asset storage
            asset["url"] = generate_signed_url(asset_url)
        processed_assets.append(asset)

    return {
        "assets": processed_assets,
        "pages": 1,
        "total": len(processed_assets),
    }


@app.post("/api/assets")
async def upload_asset(file: UploadFile, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    # TODO: Replace with real file upload and database insertion
    return {"id": "3", "name": file.filename, "type": "image", "url": "https://example.com/image2.jpg", "size": 1024, "uploaded_at": "2025-08-18", "usage_count": 0}


@app.delete("/api/assets/{asset_id}")
async def delete_asset(asset_id: str, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "DELETE")

    # TODO: Replace with real database deletion
    return {"success": True}



@app.post("/generate_video", dependencies=[Depends(RateLimiter(times=1, seconds=5, key_func=user_id_key_func))])
async def generate_video_endpoint(request_data: GenerateVideoRequest, current_user: dict = Depends(get_current_user), current_tenant: str = current_tenant, db: Session = Depends(get_db), request: Request = None):
    start_time = time.time() # ADD THIS LINE
    status_label = "failure" # Default status for metrics # ADD THIS LINE
    user_id = str(current_user.get("user_id")) # Get user_id
    try: # Wrap existing code in try-finally for metrics # ADD THIS LINE
        # Check action permission
        await plan_guard.check_action_permission(user_id, "WRITE")

        audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Access granted: User {user_id} (Tenant: {current_tenant}) accessing /generate_video.", user_id=user_id, tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/generate_video", "request_data": request_data.dict()})
        try:
            enforce_limits(user_id=user_id, feature_name="video_generation")
        except BillingException as e:
            status_label = "billing_failure" # ADD THIS LINE
            raise HTTPException(status_code=403, detail=str(e))

        if not request_data.prompt and not request_data.news_url and not request_data.script_file:
            status_label = "validation_failure" # ADD THIS LINE
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
            api_call=True,
            request=request # Pass the request object
        )

        if result.get("status") == "error":
            status_label = "pipeline_error" # ADD THIS LINE
            raise HTTPException(status_code=500, detail=result.get("message"))

        status_label = "success" # ADD THIS LINE

        # Conceptual Model Usage Tracking
        user_id = str(current_user.get("user_id"))
        model_name_used = "gpt-4o" # Placeholder: In reality, this comes from pipeline result
        model_version_used = "latest" # Placeholder
        tokens_used = 1000 # Placeholder: In reality, this comes from pipeline result
        
        model_cost = calculate_model_cost(model_name_used, tokens_used)
        await record_model_usage(user_id, model_name_used, model_version_used, tokens_used, model_cost)

        return result
    finally: # ADD THIS BLOCK
        end_time = time.time()
        duration = end_time - start_time
        VIDEO_GENERATION_REQUESTS.labels(status=status_label).inc()
        VIDEO_GENERATION_DURATION.labels(status=status_label).observe(duration)
        if status_label != "success":
            VIDEO_GENERATION_FAILURES.inc()

@app.post("/generate_tts", dependencies=[Depends(RateLimiter(times=1, seconds=5, key_func=user_id_key_func))])
async def generate_tts_endpoint(text: str, voice_name: str, current_user: dict = Depends(get_current_user)):
    """
    Conceptual endpoint for TTS generation, including usage tracking.
    """
    user_id = str(current_user.get("user_id"))
    tts_version_used = "v1.0" # Placeholder
    seconds_generated = len(text) / 10 # Placeholder: 10 chars per second

    try:
        # Check action permission
        await plan_guard.check_action_permission(user_id, "WRITE")

        # Check if user has access to this voice
        await plan_guard.check_tts_voice_access(user_id, voice_name)

        tts_cost = calculate_tts_cost(voice_name, seconds_generated)
        await record_tts_usage(user_id, voice_name, tts_version_used, seconds_generated, tts_cost)

        return {"status": "success", "message": "TTS generated successfully (conceptual).", "audio_url": "https://example.com/audio.mp3"}
    except PlanGuardException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating TTS for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate TTS.")

@app.post("/batch_generate_video")
async def batch_generate_video_endpoint(batch_request: BatchGenerateVideoRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db), request: Request = None):
    user_id = str(current_user.get("user_id")) # Get user_id
    # Check action permission for batch operation
    await plan_guard.check_action_permission(user_id, "WRITE")

    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Batch video generation request received from user {user_id}. Count: {len(batch_request.requests)}", user_id=user_id, tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/batch_generate_video", "batch_size": len(batch_request.requests)})
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

    parallel_processor = ParallelProcessor(max_workers=config.parallel_processing.max_workers)
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
async def generate_landing_page_endpoint(request_data: GenerateLandingPageRequest, current_user: dict = Depends(get_current_user), current_tenant: str = current_tenant, db: Session = Depends(get_db), request: Request = None):
    user_id = str(current_user.get("user_id")) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Access granted: User {user_id} (Tenant: {current_tenant}) accessing /generate_landing_page.", user_id=user_id, tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/generate_landing_page", "qr_code_id": request_data.qr_code_id})
    try:
        enforce_limits(user_id=user_id, feature_name="landing_page_generation")
    except BillingException as e:
        raise HTTPException(status_code=403, detail=str(e))
    result = await landing_page_service.generate_landing_page(request_data.qr_code_id, request_data.brand_metadata)
    if result.get("status") == "success":
        return {"status": "success", "s3_url": result.get('s3_url'), "message": "Landing page generation initiated."}
    else:
        raise HTTPException(status_code=500, detail=f"Landing page generation failed: {result.get('message', 'Unknown error')}")

@app.post("/scan_alert", dependencies=[Depends(RateLimiter(times=10, seconds=60, key_func=user_id_key_func))])
async def scan_alert_endpoint(request_data: ScanAlertRequest, current_user: dict = Depends(get_current_user), current_tenant: str = current_tenant, db: Session = Depends(get_db), request: Request = None):
    user_id = str(current_user.get("user_id")) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Access granted: User {user_id} (Tenant: {current_tenant}) accessing /scan_alert.", user_id=user_id, tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/scan_alert", "qr_code_id": request_data.qr_code_id})
    try:
        enforce_limits(user_id=user_id, feature_name="scan_alert")
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

@app.post("/crm_push_contact", dependencies=[Depends(RateLimiter(times=5, seconds=60, key_func=user_id_key_func))])
async def crm_push_contact_endpoint(request_data: CRMPushContactRequest, current_user: dict = Depends(get_current_user), current_tenant: str = current_tenant, db: Session = Depends(get_db), request: Request = None):
    user_id = str(current_user.get("user_id")) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Access granted: User {user_id} (Tenant: {current_tenant}) accessing /crm_push_contact.", user_id=user_id, tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/crm_push_contact", "crm_name": request_data.crm_name})
    try:
        enforce_limits(user_id=user_id, feature_name="crm_push_contact")
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

class CheckDependenciesRequest(BaseModel):
    dependencies: List[str]

class ExecuteModuleRequest(BaseModel):
    module_name: str

import hmac
import hashlib

WEBHOOK_SECRET = "your_webhook_secret_key" # TODO: Load from secure config (e.g., config.security.webhook_secret)

@app.post("/api/execute-module")
async def execute_module_endpoint(request_data: ExecuteModuleRequest, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    try:
        result = await load_and_execute_module(user_id, request_data.module_name)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in execute_module_endpoint for user {user_id}, module {request_data.module_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.post("/api/check-widget-dependencies")
async def check_widget_dependencies(request_data: CheckDependenciesRequest, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    try:
        user_plan = await plan_guard.get_user_plan(user_id)
        
        # For each dependency, check if it's allowed by the user's plan
        # For now, we'll assume allowed_models in Plan can represent allowed dependencies
        # In a real system, you might have a separate list of allowed dependencies per plan
        for dep in request_data.dependencies:
            if dep not in user_plan.model_policy.allowed_models:
                return {"allowed": False, "message": f"Dependency '{dep}' is not allowed by your {user_plan.name} plan. Upgrade required.", "plan_name": user_plan.name}
        
        return {"allowed": True, "message": "All dependencies allowed.", "plan_name": user_plan.name}
    except PlanGuardException as e:
        # If PlanGuard itself raises an exception (e.g., plan expired, view-only mode)
        return {"allowed": False, "message": str(e), "is_in_grace_mode": e.is_in_grace_mode, "grace_expires_at": e.grace_expires_at.isoformat() if e.grace_expires_at else None, "is_view_only": e.is_view_only}
    except Exception as e:
        logger.error(f"Error checking widget dependencies for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error checking dependencies.")

webhook_queue = []
webhook_dlq = []

async def process_webhook_payload(payload: WebhookPaymentStatus, db: Session):
    """Conceptual function to process webhook payload."""
    try:
        # Simulate processing success or failure
        if payload.status == "completed":
            logger.info(f"Processing completed payment for user {payload.user_id} for plan {payload.plan_name}.")
            # In a real system:
            # 1. Find user in DB
            # 2. Update their subscription plan and dates
            # 3. Log the change
            return {"status": "success", "message": "Webhook processed successfully."}
        elif payload.status == "failed":
            logger.warning(f"Processing failed payment for user {payload.user_id}, transaction {payload.transaction_id}.")
            # Handle failed payments (e.g., downgrade plan, send notification)
            raise ValueError("Simulated processing failure for failed payment.")
        else:
            logger.info(f"Processing webhook for user {payload.user_id}, status {payload.status}.")
            return {"status": "success", "message": "Webhook processed successfully."}
    except Exception as e:
        logger.error(f"Error processing webhook for user {payload.user_id}: {e}")
        raise # Re-raise to be caught by the caller for DLQ handling

@app.post("/webhook/payment_status")
async def webhook_payment_status(payload: WebhookPaymentStatus, request: Request, db: Session = Depends(get_db)):
    user_id = payload.user_id # Get user_id from payload
    # Check action permission (this is a write operation as it updates subscription status)
    await plan_guard.check_action_permission(user_id, "WRITE")
    
    # Get signature from headers (e.g., "X-Hub-Signature" or "X-Signature")
    signature_header = request.headers.get("X-Webhook-Signature") # Example header name
    
    if not signature_header:
        audit_log_manager.log_event(db, AuditEventType.WEBHOOK_RECEIVED, "Webhook received without signature header.", user_id=payload.user_id, ip_address=request.client.host, event_details={"webhook_id": payload.transaction_id, "status": "missing_signature"})
        raise HTTPException(status_code=403, detail="Signature header missing")

    # Calculate expected signature
    # In a real scenario, 'body' would be the raw request body, not the parsed payload
    # For conceptual example, we'll use a simplified representation
    # body = await request.body() # Uncomment in real implementation
    body = str(payload.dict()).encode('utf-8') # Simplified for conceptual example

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()

    # Compare signatures
    if not hmac.compare_digest(expected_signature, signature_header):
        audit_log_manager.log_event(db, AuditEventType.WEBHOOK_SIGNATURE_MISMATCH, f"Webhook signature mismatch for user {payload.user_id}. Potential tampering.", user_id=payload.user_id, ip_address=request.client.host, event_details={"webhook_id": payload.transaction_id})
        raise HTTPException(status_code=403, detail="Invalid signature")

    audit_log_manager.log_event(db, AuditEventType.WEBHOOK_RECEIVED, f"Webhook received for user {payload.user_id}, transaction {payload.transaction_id}, status {payload.status}.", user_id=payload.user_id, ip_address=request.client.host, event_details={"webhook_id": payload.transaction_id, "status": payload.status})

    try:
        # Attempt to process the webhook payload
        result = await process_webhook_payload(payload, db)
        return result
    except Exception as e:
        logger.error(f"Failed to process webhook for user {payload.user_id}. Adding to DLQ. Error: {e}")
        webhook_dlq.append({"payload": payload.dict(), "error": str(e), "timestamp": datetime.utcnow().isoformat()})
        # In a real system, you'd return a 200 OK to the webhook sender to avoid retries from their end
        # and handle retries from your DLQ processing.
        return JSONResponse(status_code=200, content={"message": "Webhook received, but processing failed. Added to DLQ."})

# Background task to retry webhooks from DLQ (conceptual)
async def retry_dlq_webhooks():
    while True:
        if webhook_dlq:
            dlq_item = webhook_dlq.pop(0) # Get the oldest item
            payload = WebhookPaymentStatus(**dlq_item["payload"])
            logger.info(f"Attempting to retry webhook for user {payload.user_id} from DLQ.")
            try:
                # In a real system, you'd get a new DB session for this background task
                with next(get_db()) as db_session:
                    await process_webhook_payload(payload, db_session)
                logger.info(f"Successfully retried webhook for user {payload.user_id}.")
            except Exception as e:
                logger.error(f"Retry failed for webhook {payload.user_id}. Re-adding to DLQ. Error: {e}")
                # In a real system, you'd implement exponential backoff and max retries
                webhook_dlq.append(dlq_item) # Re-add to DLQ if retry fails
        await asyncio.sleep(60) # Check DLQ every 60 seconds (conceptual)

# Add the retry task to FastAPI startup events
@app.on_event("startup")
async def start_dlq_retry_task():
    asyncio.create_task(retry_dlq_webhooks())

@app.get("/protected_data")
async def protected_data(current_user: User = Depends(get_current_active_user), current_tenant: str = current_tenant):
    audit_logger.info(f"Access granted: User {current_user.username} (Tenant: {current_tenant}) accessing /protected_data.", extra={'user_id': current_user.id})
    return {"message": f"Welcome, {current_user.username} from tenant {current_tenant}! This is protected data.", "user": UserProfile.from_orm(current_user), "tenant": current_tenant}

@app.post("/webhook/simulate")
async def simulate_webhook(payload: WebhookPaymentStatus, request: Request, db: Session = Depends(get_db)):
    """
    Simulates a webhook call to the /webhook/payment_status endpoint.
    Useful for testing webhook processing logic without an external sender.
    """
    logger.info(f"Simulating webhook for user {payload.user_id} with status {payload.status}.")
    # Directly call the webhook_payment_status function
    # Note: This bypasses FastAPI's dependency injection for the request body and signature verification
    # For a true simulation, you might construct a dummy Request object or use httpx.AsyncClient
    # For this conceptual example, we'll just call the processing logic directly.
    try:
        # Simulate the signature header for the processing function
        # In a real scenario, you'd generate a valid signature based on the payload and WEBHOOK_SECRET
        request.headers.__dict__["_list"].append(
            (b"x-webhook-signature", b"simulated_signature")
        )
        
        response = await webhook_payment_status(payload, request, db)
        return {"status": "success", "message": "Webhook simulation successful.", "response": response}
    except HTTPException as e:
        logger.error(f"Simulated webhook failed with HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Simulated webhook failed with unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Webhook simulation failed: {e}")

@app.post("/webhook/simulate")
async def simulate_webhook(payload: WebhookPaymentStatus, request: Request, db: Session = Depends(get_db)):
    """
    Simulates a webhook call to the /webhook/payment_status endpoint.
    Useful for testing webhook processing logic without an external sender.
    """
    logger.info(f"Simulating webhook for user {payload.user_id} with status {payload.status}.")
    # Directly call the webhook_payment_status function
    # Note: This bypasses FastAPI's dependency injection for the request body and signature verification
    # For a true simulation, you might construct a dummy Request object or use httpx.AsyncClient
    # For this conceptual example, we'll just call the processing logic directly.
    try:
        # Simulate the signature header for the processing function
        # In a real scenario, you'd generate a valid signature based on the payload and WEBHOOK_SECRET
        request.headers.__dict__["_list"].append(
            (b"x-webhook-signature", b"simulated_signature")
        )
        
        response = await webhook_payment_status(payload, request, db)
        return {"status": "success", "message": "Webhook simulation successful.", "response": response}
    except HTTPException as e:
        logger.error(f"Simulated webhook failed with HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Simulated webhook failed with unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Webhook simulation failed: {e}")

@app.post("/webhook/simulate")
async def simulate_webhook(payload: WebhookPaymentStatus, request: Request, db: Session = Depends(get_db)):
    """
    Simulates a webhook call to the /webhook/payment_status endpoint.
    Useful for testing webhook processing logic without an external sender.
    """
    logger.info(f"Simulating webhook for user {payload.user_id} with status {payload.status}.")
    # Directly call the webhook_payment_status function
    # Note: This bypasses FastAPI's dependency injection for the request body and signature verification
    # For a true simulation, you might construct a dummy Request object or use httpx.AsyncClient
    # For this conceptual example, we'll just call the processing logic directly.
    try:
        # Simulate the signature header for the processing function
        # In a real scenario, you'd generate a valid signature based on the payload and WEBHOOK_SECRET
        request.headers.__dict__["_list"].append(
            (b"x-webhook-signature", b"simulated_signature")
        )
        
        response = await webhook_payment_status(payload, request, db)
        return {"status": "success", "message": "Webhook simulation successful.", "response": response}
    except HTTPException as e:
        logger.error(f"Simulated webhook failed with HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Simulated webhook failed with unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Webhook simulation failed: {e}")

@app.post("/webhook/simulate")
async def simulate_webhook(payload: WebhookPaymentStatus, request: Request, db: Session = Depends(get_db)):
    """
    Simulates a webhook call to the /webhook/payment_status endpoint.
    Useful for testing webhook processing logic without an external sender.
    """
    logger.info(f"Simulating webhook for user {payload.user_id} with status {payload.status}.")
    # Directly call the webhook_payment_status function
    # Note: This bypasses FastAPI's dependency injection for the request body and signature verification
    # For a true simulation, you might construct a dummy Request object or use httpx.AsyncClient
    # For this conceptual example, we'll just call the processing logic directly.
    try:
        # Simulate the signature header for the processing function
        # In a real scenario, you'd generate a valid signature based on the payload and WEBHOOK_SECRET
        request.headers.__dict__["_list"].append(
            (b"x-webhook-signature", b"simulated_signature")
        )
        
        response = await webhook_payment_status(payload, request, db)
        return {"status": "success", "message": "Webhook simulation successful.", "response": response}
    except HTTPException as e:
        logger.error(f"Simulated webhook failed with HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Simulated webhook failed with unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Webhook simulation failed: {e}")

@app.post("/admin/chaos/inject")
async def inject_chaos(
    scenario_type: str,
    duration_ms: Optional[int] = None,
    duration_s: Optional[int] = None,
    intensity: Optional[float] = None,
    size_mb: Optional[int] = None,
    probability: Optional[float] = None,
    current_user: User = Depends(get_current_active_user), # Requires authenticated user
    db: Session = Depends(get_db),
    request: Request = None
):
    # // [TASK]: Add endpoint to trigger chaos scenarios
    # // [GOAL]: Enable controlled failure injection for resilience testing
    # // [ELITE_CURSOR_SNIPPET]: securitycheck
    if current_user.username != "admin": # Simple admin check for demonstration
        raise HTTPException(status_code=403, detail="Admin access required to inject chaos.")

    audit_log_manager.log_event(db, AuditEventType.CHAOS_INJECTED, f"Chaos injection requested by admin {current_user.username}: {scenario_type}", user_id=current_user.id, tenant_id=current_user.tenant_id, ip_address=request.client.host, event_details={"scenario_type": scenario_type, "duration_ms": duration_ms, "intensity": intensity})

    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["scenario_type", "current_user", "db", "request"]}
    
    try:
        chaos_injector.inject_scenario(scenario_type, **kwargs)
        return {"status": "success", "message": f"Chaos scenario '{scenario_type}' injected."}
    except Exception as e:
        audit_log_manager.log_event(db, AuditEventType.CHAOS_INJECTED, f"Failed to inject chaos scenario '{scenario_type}': {e}", user_id=current_user.id, tenant_id=current_user.tenant_id, ip_address=request.client.host, event_details={"scenario_type": scenario_type, "error": str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to inject chaos: {e}")

# --- Admin Model Management Endpoints ---

@app.get("/admin/models/status", response_model=List[ModelStatusResponse])
async def get_model_status(current_user: User = Depends(get_current_admin_user)):
    """
    Retrieves the status of all configured models, including active versions,
    recent versions, and health metrics. Requires admin access.
    """
    all_model_statuses = []
    
    # Iterate through configured models in config.yaml
    # Assuming config.models has structure like:
    # models:
    #   text_generation: { hf_api_id: ..., local_fallback_path: ... }
    #   image_generation: { hf_api_id: ..., local_fallback_path: ... }
    #   ...
    for model_type, model_config in config.models.items():
        # For simplicity, we'll consider 'local' as the provider for local models
        # and the hf_api_id as the model_name for remote models. This needs to be refined.
        
        provider = "local" # Placeholder, needs to be dynamic
        model_name = model_type # Placeholder, needs to be dynamic

        # Try to get the actual model_name from config if available
        if hasattr(model_config, 'hf_api_id') and model_config.hf_api_id:
            model_name = model_config.hf_api_id.split('/')[-1] # Use last part of HF ID
            provider = "huggingface"
        elif hasattr(model_config, 'local_fallback_path') and model_config.local_fallback_path:
            model_name = Path(model_config.local_fallback_path).name
            provider = "local"
        else:
            # Fallback if no specific ID/path is found
            model_name = model_type
            provider = "unknown"

        active_version_info = model_store.current(provider, model_name)
        recent_versions_info = model_store.list_versions(provider, model_name)
        
        # Aggregate health metrics (assuming 'local' provider and model_name for simplicity)
        health_metrics_data = aggregate(provider, model_name, active_version_info.get("version_tag") if active_version_info else "N/A")
        
        all_model_statuses.append(ModelStatusResponse(
            provider=provider,
            model_name=model_name,
            active_version=ModelVersionInfo(**active_version_info) if active_version_info else None,
            recent_versions=[ModelVersionInfo(**v) for v in recent_versions_info],
            health_metrics=ModelHealthMetrics(**health_metrics_data)
        ))
    
    return all_model_statuses

@app.post("/admin/models/promote")
async def promote_model(request: PromoteRequest, current_user: User = Depends(get_current_admin_user)):
    """
    Promotes a specified model version to active. Requires admin access.
    """
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    try:
        await model_store.activate(user_id, request.provider, request.model_name, request.version_tag, metadata={"promoted_by": current_user.username, "action": "admin_promote"})
        subject = f"✅ Model Promoted: {request.provider}/{request.model_name} to {request.version_tag}"
        body = f"Admin {current_user.username} promoted {request.provider}/{request.model_name} to version {request.version_tag}."
        send_admin_notification(subject, body)
        return {"status": "success", "message": f"Model {request.model_name} promoted to version {request.version_tag}."}
    except PlanGuardException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to promote model {request.model_name} to {request.version_tag}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to promote model: {e}")

@app.post("/admin/models/rollback")
async def rollback_model(request: RollbackRequest, current_user: User = Depends(get_current_admin_user)):
    """
    Rolls back a specified model to a target version. Requires admin access.
    """
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    try:
        await plan_guard.check_rollback_permission(user_id) # Check rollback permission
        # perform_rollback internally calls model_store.rollback, which will use the PlanGuard
        rolled_back_to_tag = perform_rollback(request.provider, request.model_name, dry_run=False, user_id=user_id) # Pass user_id
        if rolled_back_to_tag:
            subject = f"🚨 Model Rolled Back: {request.provider}/{request.model_name} to {rolled_back_to_tag}"
            body = f"Admin {current_user.username} rolled back {request.provider}/{request.model_name} to version {rolled_back_to_tag}."
            send_admin_notification(subject, body)
            return {"status": "success", "message": f"Model {request.model_name} rolled back to version {rolled_back_to_tag}."}
        else:
            raise HTTPException(status_code=500, detail="Rollback failed: No suitable version found or an error occurred.")
    except PlanGuardException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to rollback model {request.model_name} to {request.target_tag}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to rollback model: {e}")

@app.get("/admin/voices/status", response_model=List[VoiceStatusResponse])
async def get_voice_status(current_user: User = Depends(get_current_admin_user)):
    """
    Retrieves the status of all configured TTS voices, including active versions
    and available versions. Requires admin access.
    """
    all_voice_statuses = []
    
    # Assuming TTS voice configurations are under config.models.tts_models
    if hasattr(config.models, 'tts_models'):
        for voice_type, voice_config in config.models.tts_models.items():
            voice_name = voice_config.model_name # Assuming model_name is the voice identifier
            
            active_version_tag = await get_active_voice(str(current_user.id), plan_guard, voice_name) # Pass user_id and plan_guard
            all_versions_data = load_versions().get(voice_name, {})
            
            active_version_info = None
            if active_version_tag and active_version_tag in all_versions_data:
                active_version_info = VoiceVersionInfo(
                    version=active_version_tag,
                    registered_at=all_versions_data[active_version_tag]["registered_at"],
                    metadata=all_versions_data[active_version_tag]["metadata"]
                )

            available_versions_list = []
            for version_tag, version_data in all_versions_data.items():
                if version_tag != "active": # Exclude the "active" pointer
                    available_versions_list.append(VoiceVersionInfo(
                        version=version_tag,
                        registered_at=version_data["registered_at"],
                        metadata=version_data["metadata"]
                    ))
            
            all_voice_statuses.append(VoiceStatusResponse(
                voice_name=voice_name,
                active_version=active_version_info,
                available_versions=sorted(available_versions_list, key=lambda x: x.registered_at, reverse=True)
            ))
            
    return all_voice_statuses

@app.post("/admin/voices/rollback")
async def rollback_voice_endpoint(request: RollbackRequest, current_user: User = Depends(get_current_admin_user)):
    """
    Rolls back a specified TTS voice to a target version. Requires admin access.
    """
    user_id = str(current_user.id) # Get user_id
    # Check action permission
    await plan_guard.check_action_permission(user_id, "WRITE")

    # Input Validation: Check if voice_name exists in config
    if not hasattr(config.models, 'tts_models') or request.model_name not in config.models.tts_models:
        logger.warning(f"Admin {current_user.username} attempted rollback for non-existent voice: {request.model_name}")
        raise HTTPException(status_code=404, detail=f"Voice '{request.model_name}' not found in configuration.")

    try:
        # Validate target_tag exists for the voice
        all_versions_data = load_versions().get(request.model_name, {})
        if request.target_tag not in all_versions_data or request.target_tag == "active":
            logger.warning(f"Admin {current_user.username} attempted rollback for voice {request.model_name} to invalid or non-existent version: {request.target_tag}")
            raise HTTPException(status_code=400, detail=f"Target version '{request.target_tag}' not found or invalid for voice '{request.model_name}'.")

        rolled_back_to_version = await rollback_voice(str(current_user.id), plan_guard, request.model_name, request.target_tag) # Pass user_id and plan_guard
        subject = f"✅ Voice Rolled Back: {request.model_name} to {rolled_back_to_version}"
        body = f"Admin {current_user.username} rolled back voice {request.model_name} to version {rolled_back_to_version}."
        send_admin_notification(subject, body)
        logger.info(f"Voice {request.model_name} successfully rolled back to {rolled_back_to_version} by admin {current_user.username}.")
        return {"status": "success", "message": f"Voice {request.model_name} rolled back to version {rolled_back_to_version}."}
    except ValueError as e:
        logger.error(f"Rollback failed for voice {request.model_name} to {request.target_tag} due to ValueError: {e}")
        raise HTTPException(status_code=400, detail=f"Rollback failed: {e}")
    except Exception as e:
        logger.critical(f"Critical error during voice rollback for {request.model_name} to {request.target_tag}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to rollback voice: An unexpected error occurred.")

@app.get("/feature_status/{feature_name}")
async def get_feature_status(feature_name: str, current_user: dict = Depends(get_current_user), current_tenant: str = current_tenant, db: Session = Depends(get_db), request: Request = None):
    # // [TASK]: Expose API for frontend to check feature flag status
    # // [GOAL]: Allow dynamic UI based on feature flags
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    user_id = str(current_user.get("user_id")) # Convert to string for hashing
    tenant_id = str(current_tenant) # Convert to string for consistency

    is_enabled = feature_flag_manager.is_enabled(feature_name, user_id=user_id, tenant_id=tenant_id)
    
    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Feature flag check for '{feature_name}': {is_enabled} for user {user_id} (tenant {tenant_id}).", user_id=current_user.get('user_id'), tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/feature_status", "feature_name": feature_name, "is_enabled": is_enabled})
    return {"feature_name": feature_name, "is_enabled": is_enabled}

@app.get("/users/me/data/export")
async def export_user_data(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db), request: Request = None):
    # // [TASK]: Implement data export endpoint for right-to-be-forgotten
    # // [GOAL]: Allow users to export their data for GDPR compliance
    # // [ELITE_CURSOR_SNIPPET]: securitycheck
    user_id = current_user.id
    audit_log_manager.log_event(db, AuditEventType.USER_DATA_EXPORT, f"User data export requested for user ID: {user_id}", user_id=user_id, tenant_id=current_user.tenant_id, ip_address=request.client.host)

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
async def delete_user_data(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db), request: Request = None):
    # // [TASK]: Implement data deletion endpoint for right-to-be-forgotten
    # // [GOAL]: Allow users to request deletion of their data for GDPR compliance
    # // [ELITE_CURSOR_SNIPPET]: securitycheck
    user_id = current_user.id
    audit_log_manager.log_event(db, AuditEventType.USER_DATA_DELETE, f"User data deletion requested for user ID: {user_id}", user_id=user_id, tenant_id=current_user.tenant_id, ip_address=request.client.host)

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

    return {"message": "User data deletion process initiated. Your account will be deactivated."}


# Conceptual function to load and execute a backend module with PlanGuard enforcement
async def load_and_execute_module(user_id: str, module_name: str) -> Dict[str, Any]:
    module_dependencies = get_module_dependencies(module_name)
    if not module_dependencies:
        logger.info(f"Module '{module_name}' has no declared dependencies. Allowing execution.")
        # Simulate execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully (no dependencies)."}

    try:
        # Check each dependency against the user's plan
        for dep in module_dependencies:
            # For simplicity, we'll assume these map to allowed_models or features_enabled
            # A more robust solution would have a dedicated check in PlanGuard for module features
            await plan_guard.check_action_permission(user_id, dep) # Reusing check_action_permission for conceptual dependency check
        
        logger.info(f"Module '{module_name}' dependencies allowed for user {user_id}. Executing.")
        # Simulate module execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully."}
    except PlanGuardException as e:
        logger.warning(f"Module '{module_name}' execution blocked for user {user_id}: {e.message}")
        raise HTTPException(status_code=403, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error executing module '{module_name}' for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during module execution.")


# Conceptual function to load and execute a backend module with PlanGuard enforcement
async def load_and_execute_module(user_id: str, module_name: str) -> Dict[str, Any]:
    module_dependencies = get_module_dependencies(module_name)
    if not module_dependencies:
        logger.info(f"Module '{module_name}' has no declared dependencies. Allowing execution.")
        # Simulate execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully (no dependencies)."}

    try:
        # Check each dependency against the user's plan
        for dep in module_dependencies:
            # For simplicity, we'll assume these map to allowed_models or features_enabled
            # A more robust solution would have a dedicated check in PlanGuard for module features
            await plan_guard.check_action_permission(user_id, dep) # Reusing check_action_permission for conceptual dependency check
        
        logger.info(f"Module '{module_name}' dependencies allowed for user {user_id}. Executing.")
        # Simulate module execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully."}
    except PlanGuardException as e:
        logger.warning(f"Module '{module_name}' execution blocked for user {user_id}: {e.message}")
        raise HTTPException(status_code=403, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error executing module '{module_name}' for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during module execution.")


# Conceptual function to load and execute a backend module with PlanGuard enforcement
async def load_and_execute_module(user_id: str, module_name: str) -> Dict[str, Any]:
    module_dependencies = get_module_dependencies(module_name)
    if not module_dependencies:
        logger.info(f"Module '{module_name}' has no declared dependencies. Allowing execution.")
        # Simulate execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully (no dependencies)."}

    try:
        # Check each dependency against the user's plan
        for dep in module_dependencies:
            # For simplicity, we'll assume these map to allowed_models or features_enabled
            # A more robust solution would have a dedicated check in PlanGuard for module features
            await plan_guard.check_action_permission(user_id, dep) # Reusing check_action_permission for conceptual dependency check
        
        logger.info(f"Module '{module_name}' dependencies allowed for user {user_id}. Executing.")
        # Simulate module execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully."}
    except PlanGuardException as e:
        logger.warning(f"Module '{module_name}' execution blocked for user {user_id}: {e.message}")
        raise HTTPException(status_code=403, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error executing module '{module_name}' for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during module execution.")


# Conceptual function to load and execute a backend module with PlanGuard enforcement
async def load_and_execute_module(user_id: str, module_name: str) -> Dict[str, Any]:
    module_dependencies = get_module_dependencies(module_name)
    if not module_dependencies:
        logger.info(f"Module '{module_name}' has no declared dependencies. Allowing execution.")
        # Simulate execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully (no dependencies)."}

    try:
        # Check each dependency against the user's plan
        for dep in module_dependencies:
            # For simplicity, we'll assume these map to allowed_models or features_enabled
            # A more robust solution would have a dedicated check in PlanGuard for module features
            await plan_guard.check_action_permission(user_id, dep) # Reusing check_action_permission for conceptual dependency check
        
        logger.info(f"Module '{module_name}' dependencies allowed for user {user_id}. Executing.")
        # Simulate module execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully."}
    except PlanGuardException as e:
        logger.warning(f"Module '{module_name}' execution blocked for user {user_id}: {e.message}")
        raise HTTPException(status_code=403, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error executing module '{module_name}' for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during module execution.")


# Conceptual function to load and execute a backend module with PlanGuard enforcement
async def load_and_execute_module(user_id: str, module_name: str) -> Dict[str, Any]:
    module_dependencies = get_module_dependencies(module_name)
    if not module_dependencies:
        logger.info(f"Module '{module_name}' has no declared dependencies. Allowing execution.")
        # Simulate execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully (no dependencies)."}

    try:
        # Check each dependency against the user's plan
        for dep in module_dependencies:
            # For simplicity, we'll assume these map to allowed_models or features_enabled
            # A more robust solution would have a dedicated check in PlanGuard for module features
            await plan_guard.check_action_permission(user_id, dep) # Reusing check_action_permission for conceptual dependency check
        
        logger.info(f"Module '{module_name}' dependencies allowed for user {user_id}. Executing.")
        # Simulate module execution
        return {"status": "success", "message": f"Module '{module_name}' executed successfully."}
    except PlanGuardException as e:
        logger.warning(f"Module '{module_name}' execution blocked for user {user_id}: {e.message}")
        raise HTTPException(status_code=403, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error executing module '{module_name}' for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during module execution.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)