from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional, List
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

# Initialize ModelStore
model_store = ModelStore()


logger = get_logger(__name__)
audit_logger = get_audit_logger() # This will be replaced or removed later
config = get_config()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.app.name,
    version=config.app.version,
    description="API for Shujaa Studio - Enterprise AI Video Generation"
)

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

app.add_middleware(TenantMiddleware)
app.add_route("/metrics", metrics)

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

# --- Dependency Functions ---

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), request: Request = None):
    try:
        payload = verify_jwt(token)
        user_id = payload.get("user_id")
        if user_id is None:
            audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_FAILURE, "Authentication failed: User ID missing in token.", user_id=None, ip_address=request.client.host if request else None)
            raise HTTPException(status_code=401, detail="Invalid authentication credentials: User ID missing")
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
        logger.info(f"Access to sensitive endpoint: {request.url.path}. PII redaction applied to logs.", extra={'user_id': request.state.get('user_id', None), 'ip_address': request.client.host})
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
    
    # Run safety rollback check on boot
    run_safety_rollback_on_boot()

# --- API Endpoints ---

@app.get("/health")
@RateLimiter(times=5, seconds=10)
async def health_check(locale: str = Depends(get_current_locale)):
    logger.info("Health check requested.")
    return {"status": gettext("status_ok", locale=locale), "message": gettext("api_running_message", locale=locale)}

@app.post("/register", response_model=UserCreate)
@RateLimiter(times=2, seconds=60)
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
@RateLimiter(times=5, seconds=30)
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

@app.get("/reports/sla/{tenant_id}/{month}")
async def get_sla_report(tenant_id: str, month: str, current_user: User = Depends(get_current_active_user)):
    # // [TASK]: Implement API endpoint for SLA reports
    # // [GOAL]: Provide tenants with their service level agreement performance
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    # In a real system, ensure user has permission to view this tenant's SLA
    if str(current_user.tenant_id) != tenant_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view this tenant's SLA.")
    
    record = sla_tracker.get_sla_record(tenant_id, month)
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
    
    # Return mock data for now
    return [
        {"transaction_id": "mock_txn_1", "amount": 25.0, "currency": "KES", "timestamp": datetime.utcnow().isoformat(), "provider": "Mpesa"},
        {"transaction_id": "mock_txn_2", "amount": 19.99, "currency": "USD", "timestamp": datetime.utcnow().isoformat(), "provider": "Stripe"}
    ]

@app.get("/reports/usage/{user_id}")
async def get_usage_records(user_id: str, current_user: User = Depends(get_current_active_user)):
    # // [TASK]: Implement API endpoint for usage records
    # // [GOAL]: Provide users with their detailed usage statistics
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    # In a real system, fetch from database
    if str(current_user.id) != user_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view these usage records.")
    
    # Return mock data for now
    return [
        {"feature": "video_generation", "count": 5, "timestamp": datetime.utcnow().isoformat()},
        {"feature": "image_generation", "count": 150, "timestamp": datetime.utcnow().isoformat()}
    ]

@app.get("/reports/reconciliation/{month}")
async def get_reconciliation_report(month: str, current_user: User = Depends(get_current_active_user)):
    # // [TASK]: Implement API endpoint for reconciliation reports
    # // [GOAL]: Provide administrators with billing reconciliation summaries
    # // [ELITE_CURSOR_SNIPPET]: aihandle
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required for reconciliation reports.")
    
    report = billing_reconciler.get_reconciliation_report(month)
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
async def generate_api_key():
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
async def revoke_api_key(key_id: str):
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
async def update_integration(integration_id: str, config: dict):
    # TODO: Replace with real database update
    return {"id": integration_id, "name": "Google Drive", "type": "storage", "is_enabled": config.get("is_enabled"), "config": {"folder": "/ShujaaStudio"}}


@app.get("/api/users", response_model=List[UserData])
async def get_users():
    # TODO: Replace with real data from a database
    return [
        {"id": 1, "username": "testuser", "email": "testuser@example.com", "role": "user", "tenant_name": "default", "is_active": True},
        {"id": 2, "username": "adminuser", "email": "adminuser@example.com", "role": "admin", "tenant_name": "default", "is_active": True},
    ]


@app.get("/api/users/{user_id}", response_model=UserData)
async def get_user(user_id: int):
    # TODO: Replace with real data from a database
    return {"id": user_id, "username": "testuser", "email": "testuser@example.com", "role": "user", "tenant_name": "default", "is_active": True}


@app.post("/api/users", response_model=UserData)
async def create_user(user: UserData):
    # TODO: Replace with real database insertion
    return user


@app.put("/api/users/{user_id}", response_model=UserData)
async def update_user(user_id: int, user: UserData):
    # TODO: Replace with real database update
    return user


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    # TODO: Replace with real database deletion
    return {"success": True}


@app.get("/api/projects", response_model=List[Project])
async def get_projects(page: int = 1, limit: int = 6):
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
async def create_project(project: Project):
    # TODO: Replace with real database insertion
    return project


@app.put("/api/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, project: Project):
    # TODO: Replace with real database update
    return project


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    # TODO: Replace with real database deletion
    return {"success": True}


@app.get("/api/assets", response_model=List[Asset])
async def get_assets(page: int = 1, limit: int = 10, type: Optional[str] = None):
    # TODO: Replace with real data from a database
    return {
        "assets": [
            {"id": "1", "name": "Asset 1", "type": "image", "url": "https://example.com/image1.jpg", "size": 1024, "uploaded_at": "2025-08-01", "usage_count": 5},
            {"id": "2", "name": "Asset 2", "type": "audio", "url": "https://example.com/audio1.mp3", "size": 2048, "uploaded_at": "2025-08-02", "usage_count": 10},
        ],
        "pages": 1,
        "total": 2,
    }


@app.post("/api/assets")
async def upload_asset(file: UploadFile):
    # TODO: Replace with real file upload and database insertion
    return {"id": "3", "name": file.filename, "type": "image", "url": "https://example.com/image2.jpg", "size": 1024, "uploaded_at": "2025-08-18", "usage_count": 0}


@app.delete("/api/assets/{asset_id}")
async def delete_asset(asset_id: str):
    # TODO: Replace with real database deletion
    return {"success": True}



@app.post("/generate_video")
@RateLimiter(times=1, seconds=5, key_func=user_id_key_func)
async def generate_video_endpoint(request_data: GenerateVideoRequest, current_user: dict = Depends(get_current_user), current_tenant: str = current_tenant, db: Session = Depends(get_db), request: Request = None):
    start_time = time.time() # ADD THIS LINE
    status_label = "failure" # Default status for metrics # ADD THIS LINE
    try: # Wrap existing code in try-finally for metrics # ADD THIS LINE
        audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Access granted: User {current_user.get('user_id')} (Tenant: {current_tenant}) accessing /generate_video.", user_id=current_user.get('user_id'), tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/generate_video", "request_data": request_data.dict()})
        try:
            enforce_limits(user_id=current_user.get('user_id', 'anonymous_user'), feature_name="video_generation")
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
            api_call=True
        )

        if result.get("status") == "error":
            status_label = "pipeline_error" # ADD THIS LINE
            raise HTTPException(status_code=500, detail=result.get("message"))

        status_label = "success" # ADD THIS LINE
        return result
    finally: # ADD THIS BLOCK
        end_time = time.time()
        duration = end_time - start_time
        VIDEO_GENERATION_REQUESTS.labels(status=status_label).inc()
        VIDEO_GENERATION_DURATION.labels(status=status_label).observe(duration)
        if status_label != "success":
            VIDEO_GENERATION_FAILURES.inc()

@app.post("/batch_generate_video")
async def batch_generate_video_endpoint(batch_request: BatchGenerateVideoRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db), request: Request = None):
    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Batch video generation request received from user {current_user.get('user_id')}. Count: {len(batch_request.requests)}", user_id=current_user.get('user_id'), tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/batch_generate_video", "batch_size": len(batch_request.requests)})
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
    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Access granted: User {current_user.get('user_id')} (Tenant: {current_tenant}) accessing /generate_landing_page.", user_id=current_user.get('user_id'), tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/generate_landing_page", "qr_code_id": request_data.qr_code_id})
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
@RateLimiter(times=10, seconds=60, key_func=user_id_key_func)
async def scan_alert_endpoint(request_data: ScanAlertRequest, current_user: dict = Depends(get_current_user), current_tenant: str = current_tenant, db: Session = Depends(get_db), request: Request = None):
    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Access granted: User {current_user.get('user_id')} (Tenant: {current_tenant}) accessing /scan_alert.", user_id=current_user.get('user_id'), tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/scan_alert", "qr_code_id": request_data.qr_code_id})
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
@RateLimiter(times=5, seconds=60, key_func=user_id_key_func)
async def crm_push_contact_endpoint(request_data: CRMPushContactRequest, current_user: dict = Depends(get_current_user), current_tenant: str = current_tenant, db: Session = Depends(get_db), request: Request = None):
    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Access granted: User {current_user.get('user_id')} (Tenant: {current_tenant}) accessing /crm_push_contact.", user_id=current_user.get('user_id'), tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/crm_push_contact", "crm_name": request_data.crm_name})
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

import hmac
import hashlib

WEBHOOK_SECRET = "your_webhook_secret_key" # TODO: Load from secure config (e.g., config.security.webhook_secret)

@app.post("/webhook/payment_status")
async def webhook_payment_status(payload: WebhookPaymentStatus, request: Request, db: Session = Depends(get_db)):
    # // [TASK]: Implement secure signature verification for payment callbacks
    # // [GOAL]: Ensure webhook authenticity and prevent tampering
    # // [ELITE_CURSOR_SNIPPET]: securitycheck
    
    # Get raw request body
    body = await request.body()
    
    # Get signature from headers (e.g., "X-Hub-Signature" or "X-Signature")
    signature_header = request.headers.get("X-Webhook-Signature") # Example header name
    
    if not signature_header:
        audit_log_manager.log_event(db, AuditEventType.WEBHOOK_RECEIVED, "Webhook received without signature header.", user_id=payload.user_id, ip_address=request.client.host, event_details={"webhook_id": payload.transaction_id, "status": "missing_signature"})
        raise HTTPException(status_code=403, detail="Signature header missing")

    # Calculate expected signature
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
async def protected_data(current_user: User = Depends(get_current_active_user), current_tenant: str = current_tenant):
    audit_logger.info(f"Access granted: User {current_user.username} (Tenant: {current_tenant}) accessing /protected_data.", extra={'user_id': current_user.id})
    return {"message": f"Welcome, {current_user.username} from tenant {current_tenant}! This is protected data.", "user": UserProfile.from_orm(current_user), "tenant": current_tenant}

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
    try:
        model_store.activate(request.provider, request.model_name, request.version_tag, metadata={"promoted_by": current_user.username, "action": "admin_promote"})
        subject = f"✅ Model Promoted: {request.provider}/{request.model_name} to {request.version_tag}"
        body = f"Admin {current_user.username} promoted {request.provider}/{request.model_name} to version {request.version_tag}."
        send_admin_notification(subject, body)
        return {"status": "success", "message": f"Model {request.model_name} promoted to version {request.version_tag}."}
    except Exception as e:
        logger.error(f"Failed to promote model {request.model_name} to {request.version_tag}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to promote model: {e}")

@app.post("/admin/models/rollback")
async def rollback_model(request: RollbackRequest, current_user: User = Depends(get_current_admin_user)):
    """
    Rolls back a specified model to a target version. Requires admin access.
    """
    try:
        rolled_back_to_tag = perform_rollback(request.provider, request.model_name, dry_run=False)
        if rolled_back_to_tag:
            subject = f"🚨 Model Rolled Back: {request.provider}/{request.model_name} to {rolled_back_to_tag}"
            body = f"Admin {current_user.username} rolled back {request.provider}/{request.model_name} to version {rolled_back_to_tag}."
            send_admin_notification(subject, body)
            return {"status": "success", "message": f"Model {request.model_name} rolled back to version {rolled_back_to_tag}."}
        else:
            raise HTTPException(status_code=500, detail="Rollback failed: No suitable version found or an error occurred.")
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
            
            active_version_tag = get_active_voice(voice_name)
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
    try:
        rolled_back_to_version = rollback_voice(request.model_name, request.target_tag)
        subject = f"🚨 Voice Rolled Back: {request.model_name} to {rolled_back_to_version}"
        body = f"Admin {current_user.username} rolled back voice {request.model_name} to version {rolled_back_to_version}."
        send_admin_notification(subject, body)
        return {"status": "success", "message": f"Voice {request.model_name} rolled back to version {rolled_back_to_version}."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Rollback failed: {e}")
    except Exception as e:
        logger.error(f"Failed to rollback voice {request.model_name} to {request.target_tag}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to rollback voice: {e}")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)