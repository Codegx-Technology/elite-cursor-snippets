# backend/superadmin/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from database import get_db
from auth.user_models import User, Tenant
from auth.rbac import Role
from auth.auth_service import create_user, update_user_profile, authenticate_user # Assuming these exist
from backend.superadmin.auth import get_current_superadmin_user
from billing.plan_guard import PlanGuard, PlanGuardException
from backend.core.dependencies_enforcer import DependencyEnforcer
from logging_setup import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Initialize PlanGuard and DependencyEnforcer (these should ideally be passed via dependency injection)
# For simplicity in this scaffold, we'll re-initialize, but in a real app, use app.state or similar
plan_guard = PlanGuard(db_session_factory=get_db) # Re-initialize with db_session_factory
dependency_enforcer = DependencyEnforcer(plan_guard)

# --- User Management ---
@router.get("/users", response_model=List[Dict[str, Any]])
async def get_all_users(db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    users = db.query(User).all()
    return [{
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "tenant_id": str(user.tenant_id),
        "is_active": user.is_active
    } for user in users]

@router.post("/users", response_model=Dict[str, Any])
async def create_new_user(user_data: Dict[str, Any], db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    try:
        new_user = create_user(
            db, 
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            tenant_name=user_data.get("tenant_name", "default"),
            role=user_data.get("role", Role.USER)
        )
        return {"status": "success", "message": f"User {new_user.username} created.", "user_id": str(new_user.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create user: {e}")

@router.put("/users/{user_id}", response_model=Dict[str, Any])
async def update_existing_user(user_id: str, user_data: Dict[str, Any], db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    try:
        updated_user = update_user_profile(db, user_id, user_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success", "message": f"User {updated_user.username} updated.", "user_id": str(updated_user.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update user: {e}")


@router.get("/tenants/{tenant_id}/branding", response_model=Dict[str, Any])
async def get_tenant_branding(tenant_id: str, db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    # TODO: Fetch real tenant branding data from database
    # For now, return mock data
    return {
        "tenant_id": tenant_id,
        "logo_url": "https://example.com/default_logo.png",
        "primary_color": "#00A651",
        "secondary_color": "#FFD700",
        "custom_domain": f"tenant-{tenant_id}.shujaastudio.com",
        "tls_status": "active",
        "name": "Default Tenant"
    }

# --- Tenant Management ---
@router.get("/audit-logs", response_model=List[Dict[str, Any]])
async def get_all_audit_logs(db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
    return [{
        "id": str(log.id),
        "timestamp": log.timestamp.isoformat(),
        "event_type": log.event_type,
        "message": log.message,
        "user_id": str(log.user_id) if log.user_id else None,
    } for log in logs]


# --- Tenant Management ---
@router.get("/tenants", response_model=List[Dict[str, Any]])
async def get_all_tenants(db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    tenants = db.query(Tenant).all()
    return [{
        "id": str(tenant.id),
        "name": tenant.name,
        "is_active": tenant.is_active,
        # TODO: Add plan info, usage, etc. from PlanGuard
    } for tenant in tenants]

@router.post("/tenants", response_model=Dict[str, Any])
async def create_new_tenant(tenant_data: Dict[str, Any], db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    # TODO: Implement tenant creation logic
    raise HTTPException(status_code=501, detail="Tenant creation not implemented yet.")

# --- Widget Marketplace Approvals ---
@router.post("/widgets/approve/{widget_name}")
async def approve_widget(widget_name: str, db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    # TODO: Implement logic to approve a widget for marketplace
    # This might involve updating a status in a widget registry DB
    return {"status": "success", "message": f"Widget {widget_name} approved (conceptual)."}

# --- PlanGuard Override ---
@router.post("/planguard/override/{user_id}")
async def override_planguard(user_id: str, action: str, db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    # This is a conceptual override. In a real system, this would modify user's plan/state in DB
    logger.info(f"Superadmin {current_superadmin.username} overriding PlanGuard for user {user_id} for action: {action}")
    # Example: Temporarily set user's plan to Enterprise or healthy state
    # This would require direct DB manipulation or a method in PlanGuard to do so.
    return {"status": "success", "message": f"PlanGuard overridden for user {user_id} for action {action} (conceptual)."}

@router.post("/planguard/enforce/{user_id}")
async def enforce_planguard(user_id: str, action: str, db: Session = Depends(get_db), current_superadmin: User = Depends(get_current_superadmin_user)):
    # This is a conceptual enforcement. In a real system, this would revert overrides or force a state.
    logger.info(f"Superadmin {current_superadmin.username} enforcing PlanGuard for user {user_id} for action: {action}")
    return {"status": "success", "message": f"PlanGuard enforced for user {user_id} for action {action} (conceptual)."}

# --- System Health Dashboard (Conceptual) ---
@router.get("/health/metrics", response_model=Dict[str, Any])
async def get_system_metrics(current_superadmin: User = Depends(get_current_superadmin_user)):
    # TODO: Fetch real system metrics (CPU, RAM, network, API latencies)
    return {"cpu_usage": "25%", "memory_usage": "60%", "api_latency_ms": 120}

@router.get("/health/logs", response_model=List[Dict[str, Any]])
async def get_system_logs(current_superadmin: User = Depends(get_current_superadmin_user)):
    # TODO: Fetch real system logs (from a logging service)
    return [
        {"timestamp": "2025-08-20T10:00:00Z", "level": "INFO", "message": "Server started"},
        {"timestamp": "2025-08-20T10:05:00Z", "level": "ERROR", "message": "Database connection lost"},
    ]

# --- Global Dependency Monitor (Conceptual) ---
@router.get("/dependencies/status", response_model=Dict[str, Any])
async def get_global_dependency_status(current_superadmin: User = Depends(get_current_superadmin_user)):
    # TODO: Implement logic to check global dependency status using dependency_enforcer
    # This might involve iterating through all known widgets/modules and checking their deps
    return {"status": "ok", "unmet_dependencies": []}

# --- Integrate with main app ---
# You would include this router in your main FastAPI app (e.g., api_server.py)
# app.include_router(superadmin_router, prefix="/superadmin", tags=["SuperAdmin"])