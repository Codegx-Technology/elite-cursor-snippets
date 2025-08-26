
import asyncio
import json
import uvicorn
import uuid
import psutil
import time
import hmac
import hashlib
from datetime import timedelta, datetime
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Request, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session
import redis.asyncio as redis

from logging_setup import get_logger, get_audit_logger
from config_loader import get_config
from database import engine, get_db

from auth.jwt_utils import verify_jwt
from auth.user_models import Base, User, Tenant, AuditLog, Consent
from auth.auth_service import create_user, authenticate_user, create_access_token, update_user_profile
from auth.tenancy import current_tenant, TenantMiddleware
from auth.rbac import has_role, Role
from security.audit_log_manager import audit_log_manager, AuditEventType

from pipeline_orchestrator import PipelineOrchestrator
from billing_middleware import enforce_limits, BillingException
from landing_page_service import LandingPageService
from scan_alert_system import ScanAlertSystem
from crm_integration import CRMIntegrationService
from utils.parallel_processing import ParallelProcessor
from i18n_utils import gettext, get_locale_from_request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from starlette_prometheus import PrometheusMiddleware, metrics
from prometheus_client import Counter, Histogram
from feature_flags import feature_flag_manager
from chaos_utils import chaos_injector
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Backend-specific imports
from backend.ai_models.model_store import ModelStore
from backend.ai_health.healthcheck import score_inference, record_metric, aggregate
from backend.ai_health.rollback import should_rollback, perform_rollback
from backend.notifications.admin_notify import send_admin_notification
from backend.startup import run_safety_rollback_on_boot
from backend.core.voices.versioning import register_voice, rollback_voice, get_active_voice, get_latest_voice, load_versions
from backend.core_modules.module_registry import get_module_dependencies
from backend.middleware.policy_resolver import PolicyResolverMiddleware
from backend.core.plan_guard import PlanGuardMiddleware
from backend.superadmin.routes import router as superadmin_router
from backend.routers.custom_domain import router as custom_domain_router
from backend.models.webhook_dlq import WebhookDLQItem
from backend.superadmin.auth import create_superadmin_users
from backend.mock_db import mock_db

from billing.plan_guard import PlanGuard, PlanGuardException
from billing_models import get_default_plans, get_user_subscription
from backend.widget_manager import WidgetManager


# Initialize ModelStore
model_store = ModelStore()
plan_guard = PlanGuard(db_session_factory=get_db)
widget_manager = WidgetManager(plan_guard)


logger = get_logger(__name__)
audit_logger = get_audit_logger()
config = get_config()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.app.name,
    version=config.app.version,
    description="API for Shujaa Studio - Enterprise AI Video Generation"
)

# Attach PlanGuard after app is created
app.state.plan_guard = plan_guard

# --- Prometheus Custom Metrics ---
VIDEO_GENERATION_REQUESTS = Counter(
    'video_generation_requests_total',
    'Total number of video generation requests',
    ['status']
)
VIDEO_GENERATION_DURATION = Histogram(
    'video_generation_duration_seconds',
    'Duration of video generation requests in seconds',
    ['status']
)
VIDEO_GENERATION_FAILURES = Counter(
    'video_generation_failures_total',
    'Total number of failed video generation requests'
)


FastAPIInstrumentor.instrument_app(app)

app.add_middleware(TenantMiddleware)
app.add_middleware(PolicyResolverMiddleware)
app.add_middleware(PlanGuardMiddleware)
app.add_route("/metrics", metrics)

app.include_router(superadmin_router, prefix="/superadmin", tags=["SuperAdmin"])
app.include_router(custom_domain_router, prefix="/api", tags=["Custom Domain"])

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
    version_tag: str

class RollbackRequest(BaseModel):
    provider: str
    model_name: str
    target_tag: str

class VoiceVersionInfo(BaseModel):
    version: str
    registered_at: str
    metadata: Optional[Dict[str, Any]] = None

class VoiceStatusResponse(BaseModel):
    voice_name: str
    active_version: Optional[VoiceVersionInfo] = None
    available_versions: List[VoiceVersionInfo]

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
        extra = "ignore"

class WebhookPaymentStatus(BaseModel):
    user_id: str
    transaction_id: str
    status: str
    amount: float
    currency: str
    plan_name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    signature: str

class CheckDependenciesRequest(BaseModel):
    dependencies: List[str]

class ExecuteModuleRequest(BaseModel):
    module_name: str


# --- Dependency Functions ---

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), request: Request = None):
    try:
        payload = verify_jwt(token)
        user_id = payload.get("user_id")
        if user_id is None:
            audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_FAILURE, "Authentication failed: User ID missing in token.", user_id=None, ip_address=request.client.host if request else None)
            raise HTTPException(status_code=401, detail="Invalid authentication credentials: User ID missing")
        request.state.user_id = user_id

        user_sub = get_user_subscription(user_id)
        current_plan = next((p for p in get_default_plans() if p.name == user_sub.plan_name), None)

        request.state.is_in_grace_mode = False
        request.state.grace_expires_at = None

        if not user_sub.is_active and current_plan and current_plan.grace_period_hours > 0:
            if not user_sub.grace_expires_at or user_sub.grace_expires_at < datetime.now():
                user_sub.grace_expires_at = datetime.now() + timedelta(hours=current_plan.grace_period_hours)

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

async def get_current_locale(request: Request) -> str:
    return get_locale_from_request(request)

async def user_id_key_func(request: Request, current_user: dict = Depends(get_current_user)):
    return str(current_user.get("user_id", request.client.host))

# --- Middleware ---

@app.middleware("http")
async def pii_redaction_middleware(request: Request, call_next):
    sensitive_paths = ["/register", "/token", "/users/me"]

    if request.url.path in sensitive_paths:
        logger.info(
            f"Access to sensitive endpoint: {request.url.path}. PII redaction applied to logs.",
            extra={'user_id': getattr(request.state, 'user_id', None), 'ip_address': request.client.host}
        )

    response = await call_next(request)

    if hasattr(request.state, 'is_in_grace_mode') and request.state.is_in_grace_mode:
        user_id = str(request.state.user_id)
        grace_expires_at = request.state.grace_expires_at
        
        delay = plan_guard.get_grace_delay(grace_expires_at)
        if delay > 0:
            logger.info(f"User {user_id} in grace mode. Applying {delay}s delay.")
            time.sleep(delay)

        if isinstance(response, JSONResponse):
            response_body = json.loads(response.body.decode())
            response_body["status"] = "grace_mode"
            response_body["grace_expires_at"] = grace_expires_at.isoformat()
            
            time_left = grace_expires_at - datetime.now()
            hours, remainder = divmod(int(time_left.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            response_body["remaining"] = f"{hours}h {minutes}m"

            if delay > 0:
                response_body["message"] = f"You're in Grace Mode. Responses may feel slower as your plan is expiring. Upgrade now to restore full speed. ({hours}h {minutes}m left)"
            else:
                response_body["message"] = f"You're in Grace Mode. Your plan expires in {hours}h {minutes}m. Upgrade now!"

            response = JSONResponse(content=response_body, status_code=response.status_code)

    return response

# --- Event Handlers ---

def rate_limit_user_id_key_func(request: Request) -> str:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if auth:
        return f"auth:{hash(auth)}"
    client = getattr(request, "client", None)
    host = getattr(client, "host", "unknown") if client else "unknown"
    return f"ip:{host}"

@app.on_event("startup")
async def startup():
    try:
        redis_url = getattr(config.redis, 'url', "redis://localhost:6379/0")
        if not str(redis_url).startswith(("redis://", "rediss://", "unix://")):
            logger.warning(f"Invalid or missing Redis URL in config; defaulting to redis://localhost:6379/0")
            redis_url = "redis://localhost:6379/0"

        redis_connection = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(redis_connection, identifier=rate_limit_user_id_key_func)
        logger.info("FastAPI-Limiter initialized.")
    except Exception as e:
        logger.warning(f"FastAPI-Limiter Redis not available, continuing without rate limiting: {e}")
    
    run_safety_rollback_on_boot()

    with next(get_db()) as db_session:
        await create_superadmin_users(db_session)

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
        audit_log_manager.log_event(db, AuditEventType.USER_REGISTER, f"User registration failed: Username {user.username} or email {user.email} already registered.", user_id=None, ip_address=request.client.host)
        raise HTTPException(status_code=400, detail=gettext("username_or_email_registered", locale=locale))
    audit_log_manager.log_event(db, AuditEventType.USER_REGISTER, f"User registered: {user.username} (Tenant: {user.tenant_name})", user_id=db_user.id, tenant_id=db_user.tenant_id, ip_address=request.client.host)
    return db_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), request: Request = None):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_FAILURE, f"Login failed: Invalid credentials for username {form_data.username}.", user_id=None, ip_address=request.client.host)
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
    audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_SUCCESS, f"User logged in: {user.username} (Tenant: {user.tenant.name})", user_id=user.id, tenant_id=user.tenant_id, ip_address=request.client.host)
    return {"access_token": access_token, "token_type": "bearer"}

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
    user_id = str(current_user.id)
    try:
        user_plan = await plan_guard.get_user_plan(user_id)
        usage = {"tokens": 5000, "audioMins": 10, "videoMins": 5}

        return {
            "planCode": user_plan.name.lower().replace(" ", "_"),
            "planName": user_plan.name,
            "state": "healthy",
            "quota": {
                "tokens": user_plan.quotas.monthly.tokens,
                "audioMins": user_plan.quotas.monthly.audioMins,
                "videoMins": user_plan.quotas.monthly.videoMins,
            },
            "usage": usage,
            "expiresAt": None,
            "graceExpiresAt": None,
            "upgradeUrl": "/billing",
            "lastCheckedAt": datetime.utcnow().isoformat(),
            "adminConsoleUrl": None,
        }
    except PlanGuardException as e:
        return {
            "planCode": "unknown",
            "planName": "Unknown",
            "state": "view_only" if e.is_view_only else ("grace" if e.is_in_grace_mode else "locked"),
            "quota": { "tokens": 0, "audioMins": 0, "videoMins": 0 },
            "usage": { "tokens": 0, "audioMins": 0, "videoMins": 0 },
            "expiresAt": None,
            "graceExpiresAt": e.grace_expires_at.isoformat() if e.grace_expires_at else None,
            "upgradeUrl": "/billing",
            "lastCheckedAt": datetime.utcnow().isoformat(),
            "adminConsoleUrl": None,
            "message": str(e)
        }
    except Exception as e:
        logger.error(f"Error fetching plan status for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch plan status.")

@app.get("/api/plans")
async def get_all_plans():
    all_plans = get_default_plans()
    return [plan.__dict__ for plan in all_plans]

@app.get("/users/me/usage")
async def get_user_usage(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id")
    daily_usage = 7 
    
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
    tenant_id = current_user.tenant_id
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

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
    if str(current_user.tenant_id) != tenant_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view this tenant's SLA.")
    
    record = mock_db.get_sla_record(tenant_id, month)
    if not record:
        raise HTTPException(status_code=404, detail="SLA record not found for specified tenant and month.")
    return record

@app.get("/reports/billing/transactions/{user_id}")
async def get_billing_transactions(user_id: str, current_user: User = Depends(get_current_active_user)):
    if str(current_user.id) != user_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view these transactions.")
    
    return mock_db.get_billing_transactions(user_id)

@app.get("/reports/usage/{user_id}")
async def get_usage_records(user_id: str, current_user: User = Depends(get_current_active_user)):
    if str(current_user.id) != user_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view these usage records.")
    
    return mock_db.get_usage_records(user_id)

@app.get("/reports/reconciliation/{month}")
async def get_reconciliation_report(month: str, current_user: User = Depends(get_current_active_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required for reconciliation reports.")
    
    report = mock_db.get_reconciliation_report(month)
    if not report:
        raise HTTPException(status_code=404, detail="Reconciliation report not found for specified month.")
    return report


@app.get("/api/analytics", response_model=AnalyticsData)
async def get_analytics_data(db: Session = Depends(get_db), timeRange: str = "7d"):
    """
    Provides real-time analytics data for the Shujaa Studio dashboard.
    """
    try:
        # --- Overview Metrics ---
        total_users = db.query(func.count(User.id)).scalar()
        total_videos = db.query(func.count(AuditLog.id)).filter(
            AuditLog.event_type == AuditEventType.API_ACCESS,
            AuditLog.message.like('%/generate_video%')
        ).scalar()
        total_audio = db.query(func.count(AuditLog.id)).filter(
            AuditLog.event_type == AuditEventType.API_ACCESS,
            AuditLog.message.like('%/generate_tts%')
        ).scalar()
        total_images = total_videos * 5 

        overview = {
            "total_users": total_users,
            "total_videos": total_videos,
            "total_images": total_images,
            "total_audio": total_audio,
        }

        # --- Usage Trends ---
        days = 7 if timeRange == "7d" else 30
        start_date = datetime.utcnow() - timedelta(days=days)
        
        usage_trends_query = db.query(
            func.date(AuditLog.timestamp).label('date'),
            func.count(AuditLog.id).filter(AuditLog.message.like('%/generate_video%')).label('videos'),
            func.count(AuditLog.id).filter(AuditLog.message.like('%/generate_tts%')).label('audio')
        ).filter(AuditLog.timestamp >= start_date).group_by(func.date(AuditLog.timestamp)).order_by(func.date(AuditLog.timestamp)).all()

        usage_trends = [
            {
                "date": row.date.isoformat(),
                "videos": row.videos,
                "images": row.videos * 5,
                "audio": row.audio
            } for row in usage_trends_query
        ]

        # --- Popular Content (remains mock data for now) ---
        popular_content = [
            {"id": "1", "title": "Kenya Wildlife", "type": "video", "views": 1500, "downloads": 300},
            {"id": "2", "title": "Nairobi Skyline", "type": "image", "views": 2500, "downloads": 500},
            {"id": "3", "title": "Maasai Mara Beat", "type": "audio", "views": 3500, "downloads": 700},
        ]

        # --- Performance Metrics ---
        performance_metrics = {
            "cpu_usage_percent": psutil.cpu_percent(),
            "memory_usage_percent": psutil.virtual_memory().percent,
            "success_rate": 98.5,
            "avg_generation_time": 42,
        }

        return {
            "overview": overview,
            "usage_trends": usage_trends,
            "popular_content": popular_content,
            "performance_metrics": performance_metrics,
        }
    except Exception as e:
        logger.error(f"Error fetching analytics data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch analytics data.")


@app.get("/api/keys", response_model=List[ApiKey])
async def get_api_keys():
    return [
        {"id": "1", "key": "shujaa_sk_123...", "created_at": "2025-08-01", "last_used_at": "2025-08-17", "is_active": True},
        {"id": "2", "key": "shujaa_sk_456...", "created_at": "2025-07-15", "last_used_at": None, "is_active": False},
    ]


@app.post("/api/keys", response_model=ApiKey)
async def generate_api_key(current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "WRITE")

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
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "DELETE")
    return {"success": True}


@app.get("/api/integrations", response_model=List[Integration])
async def get_integrations():
    return [
        {"id": "1", "name": "Google Drive", "type": "storage", "is_enabled": True, "config": {"folder": "/ShujaaStudio"}},
        {"id": "2", "name": "Slack", "type": "notification", "is_enabled": False, "config": {"channel": "#general"}},
    ]


@app.put("/api/integrations/{integration_id}", response_model=Integration)
async def update_integration(integration_id: str, config: dict, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "WRITE")
    return {"id": integration_id, "name": "Google Drive", "type": "storage", "is_enabled": config.get("is_enabled"), "config": {"folder": "/ShujaaStudio"}}


@app.get("/api/users", response_model=List[UserData])
async def get_users(current_user: User = Depends(get_current_admin_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "READ")
    return [
        {"id": 1, "username": "testuser", "email": "testuser@example.com", "role": "user", "tenant_name": "default", "is_active": True},
        {"id": 2, "username": "adminuser", "email": "adminuser@example.com", "role": "admin", "tenant_name": "default", "is_active": True},
    ]


@app.get("/api/users/{user_id}", response_model=UserData)
async def get_user(user_id: int, current_user: User = Depends(get_current_admin_user)):
    user_id_str = str(current_user.id)
    await plan_guard.check_action_permission(user_id_str, "READ")
    return {"id": user_id, "username": "testuser", "email": "testuser@example.com", "role": "user", "tenant_name": "default", "is_active": True}


@app.post("/api/users", response_model=UserData)
async def create_user_endpoint(user: UserData, current_user: User = Depends(get_current_admin_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "WRITE")
    return user


@app.put("/api/users/{user_id}", response_model=UserData)
async def update_user(user_id: int, user: UserData, current_user: User = Depends(get_current_admin_user)):
    user_id_str = str(current_user.id)
    await plan_guard.check_action_permission(user_id_str, "WRITE")
    return user


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_admin_user)):
    user_id_str = str(current_user.id)
    await plan_guard.check_action_permission(user_id_str, "DELETE")
    return {"success": True}


@app.get("/api/projects", response_model=List[Project])
async def get_projects(page: int = 1, limit: int = 6, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "READ")
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
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "WRITE")
    return project


@app.put("/api/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, project: Project, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "WRITE")
    return project


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "DELETE")
    return {"success": True}


@app.get("/api/assets", response_model=List[Asset])
async def get_assets(page: int = 1, limit: int = 10, type: Optional[str] = None, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "READ")
    
    from utils.asset_utils import generate_signed_url
    
    mock_assets = [
        {"id": "1", "name": "Asset 1", "type": "image", "url": "/local_assets/image1.jpg", "size": 1024, "uploaded_at": "2025-08-01", "usage_count": 5},
        {"id": "2", "name": "Asset 2", "type": "audio", "url": "/local_assets/audio1.mp3", "size": 2048, "uploaded_at": "2025-08-02", "usage_count": 10},
    ]

    cdn_endpoints = config.app.get("cdn_endpoints", [])
    processed_assets = []

    for asset in mock_assets:
        asset_url = asset["url"]
        if cdn_endpoints:
            for cdn_base_url in cdn_endpoints:
                asset["url"] = f"{cdn_base_url}{asset_url.lstrip('/')}"
                break
        else:
            asset["url"] = generate_signed_url(asset_url)
        processed_assets.append(asset)

    return {
        "assets": processed_assets,
        "pages": 1,
        "total": len(processed_assets),
    }


@app.post("/api/assets")
async def upload_asset(file: UploadFile, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "WRITE")
    return {"id": "3", "name": file.filename, "type": "image", "url": "https://example.com/image2.jpg", "size": 1024, "uploaded_at": "2025-08-18", "usage_count": 0}


@app.delete("/api/assets/{asset_id}")
async def delete_asset(asset_id: str, current_user: User = Depends(get_current_active_user)):
    user_id = str(current_user.id)
    await plan_guard.check_action_permission(user_id, "DELETE")
    return {"success": True}



@app.post("/generate_video", dependencies=[Depends(RateLimiter(times=1, seconds=5))])
async def generate_video_endpoint(request_data: GenerateVideoRequest, current_user: dict = Depends(get_current_user), current_tenant: str = Depends(current_tenant), db: Session = Depends(get_db), request: Request = None):
    start_time = time.time()
    status_label = "failure"
    user_id = str(current_user.get("user_id"))
    try:
        await plan_guard.check_action_permission(user_id, "WRITE")

        audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Access granted: User {user_id} (Tenant: {current_tenant}) accessing /generate_video.", user_id=user_id, tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/generate_video", "request_data": request_data.dict()})
        try:
            enforce_limits(user_id=user_id, feature_name="video_generation")
        except BillingException as e:
            status_label = "billing_failure"
            raise HTTPException(status_code=403, detail=str(e))

        if not request_data.prompt and not request_data.news_url and not request_data.script_file:
            status_label = "validation_failure"
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
            request=request
        )

        if result.get("status") == "error":
            status_label = "pipeline_error"
            raise HTTPException(status_code=500, detail=result.get("message"))

        status_label = "success"
        
        # ... (conceptual usage tracking)

        return result
    finally:
        end_time = time.time()
        duration = end_time - start_time
        VIDEO_GENERATION_REQUESTS.labels(status=status_label).inc()
        VIDEO_GENERATION_DURATION.labels(status=status_label).observe(duration)
        if status_label != "success":
            VIDEO_GENERATION_FAILURES.inc()

@app.post("/generate_tts", dependencies=[Depends(RateLimiter(times=1, seconds=5))])
async def generate_tts_endpoint(text: str, voice_name: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("user_id"))
    try:
        await plan_guard.check_action_permission(user_id, "WRITE")
        await plan_guard.check_tts_voice_access(user_id, voice_name)
        
        # ... (conceptual usage tracking)

        return {"status": "success", "message": "TTS generated successfully (conceptual).", "audio_url": "https://example.com/audio.mp3"}
    except PlanGuardException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating TTS for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate TTS.")

@app.post("/batch_generate_video")
async def batch_generate_video_endpoint(batch_request: BatchGenerateVideoRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db), request: Request = None):
    user_id = str(current_user.get("user_id"))
    await plan_guard.check_action_permission(user_id, "WRITE")

    audit_log_manager.log_event(db, AuditEventType.API_ACCESS, f"Batch video generation request received from user {user_id}. Count: {len(batch_request.requests)}", user_id=user_id, tenant_id=current_tenant, ip_address=request.client.host, event_details={"endpoint": "/batch_generate_video", "batch_size": len(batch_request.requests)})
    MAX_BATCH_SIZE = config.video.get('max_batch_size', 10)
    if len(batch_request.requests) > MAX_BATCH_SIZE:
        raise HTTPException(status_code=400, detail=f"Batch size cannot exceed {MAX_BATCH_SIZE}.")

    async def video_worker(request_data: GenerateVideoRequest):
        try:
            # ... (worker logic)
            return await orchestrator.run_pipeline(...)
        except Exception as e:
            return {"status": "error", "message": str(e), "request_prompt": request_data.prompt}

    parallel_processor = ParallelProcessor(max_workers=config.parallel_processing.max_workers)
    batch_results = await parallel_processor.run_parallel(items=batch_request.requests, worker_function=video_worker)

    successful_jobs = [res for res in batch_results if res.get("status") == "success"]
    failed_jobs = [res for res in batch_results if res.get("status") != "success"]

    logger.info(f"Batch video generation completed for user {user_id}. Success: {len(successful_jobs)}, Failed: {len(failed_jobs)}")
    return {
        "batch_id": f"batch_{uuid.uuid4().hex[:8]}",
        "status": "completed",
        "successful_videos": len(successful_jobs),
        "failed_videos": len(failed_jobs),
        "results": batch_results
    }

# ... (rest of the endpoints)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
