from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request

from auth.user_models import User, Tenant
from auth.jwt_utils import create_jwt, hash_password, verify_password, verify_jwt # Import hash_password and verify_password
from logging_setup import get_logger # ADD THIS
from config_loader import get_config # ADD THIS
from security.audit_log_manager import audit_log_manager, AuditEventType # ADD THIS
from database import get_db

logger = get_logger(__name__) # ADD THIS
config = get_config() # ADD THIS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    """
    // [TASK]: Retrieve a user by username from the database
    // [GOAL]: Support user authentication
    """
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """
    // [TASK]: Retrieve a user by email from the database
    // [GOAL]: Support user registration and authentication
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str, tenant_name: str = "default", role: str = "user"):
    """
    // [TASK]: Create a new user in the database
    // [GOAL]: Handle user registration
    """
    # Check if username or email already exists
    if get_user_by_username(db, username):
        audit_log_manager.log_event(db, AuditEventType.USER_REGISTER, f"Registration failed: Username {username} already exists.", user_id=None) # Use audit_log_manager
        return None
    if get_user_by_email(db, email):
        audit_log_manager.log_event(db, AuditEventType.USER_REGISTER, f"Registration failed: Email {email} already exists.", user_id=None) # Use audit_log_manager
        return None

    hashed_password = hash_password(password)
    
    # Ensure tenant exists or create it
    tenant = db.query(Tenant).filter(Tenant.name == tenant_name).first()
    if not tenant:
        tenant = Tenant(name=tenant_name)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        audit_log_manager.log_event(db, AuditEventType.TENANT_CREATE, f"New tenant created: {tenant_name}", user_id=None, tenant_id=tenant.id) # Use audit_log_manager

    db_user = User(username=username, email=email, hashed_password=hashed_password, tenant_id=tenant.id, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    audit_log_manager.log_event(db, AuditEventType.USER_REGISTER, f"User {username} registered successfully for tenant {tenant_name}.", user_id=db_user.id, tenant_id=tenant.id) # Use audit_log_manager
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """
    // [TASK]: Authenticate a user
    // [GOAL]: Verify user credentials for login
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_FAILURE, f"Authentication failed: Invalid credentials for username {username}.", user_id=user.id if user else None) # Use audit_log_manager
        return False
    audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_SUCCESS, f"User {username} authenticated successfully.", user_id=user.id, tenant_id=user.tenant_id) # Use audit_log_manager
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    // [TASK]: Create an access token (JWT)
    // [GOAL]: Issue JWTs upon successful user login
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.auth.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    
    # Use jwt_utils.py to create the token
    token = create_jwt(to_encode)
    audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_SUCCESS, f"Access token created for user: {data.get('username')}", user_id=data.get('user_id'), tenant_id=data.get('tenant_id')) # Use audit_log_manager
    return token

def update_user_profile(db: Session, user_id: int, user_update_data: dict):
    """
    // [TASK]: Update a user's profile information
    // [GOAL]: Allow users to modify their profile
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        audit_log_manager.log_event(db, AuditEventType.USER_PROFILE_UPDATE, f"Profile update failed: User with ID {user_id} not found.", user_id=user_id) # Use audit_log_manager
        return None

    for key, value in user_update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    audit_log_manager.log_event(db, AuditEventType.USER_PROFILE_UPDATE, f"User profile updated for user ID: {user_id}", user_id=user_id, tenant_id=user.tenant_id, event_details=user_update_data) # Use audit_log_manager
    return user

def _extract_bearer_token(auth_header: Optional[str]) -> Optional[str]:
    if not auth_header:
        return None
    parts = auth_header.split(" ", 1)
    if len(parts) != 2:
        return None
    scheme, token = parts[0], parts[1]
    if scheme.lower() != "bearer":
        return None
    return token.strip()

def get_current_active_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    // [TASK]: Resolve the current active user from Authorization: Bearer <token>
    // [GOAL]: Provide a FastAPI dependency for RBAC and protected endpoints
    """
    auth_header = request.headers.get("Authorization")
    token = _extract_bearer_token(auth_header)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

    try:
        payload = verify_jwt(token)
    except Exception as e:
        audit_log_manager.log_event(db, AuditEventType.USER_LOGIN_FAILURE, f"JWT verification failed: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("user_id") or payload.get("sub")
    username = payload.get("username")

    user = None
    if user_id is not None:
        user = db.query(User).filter(User.id == user_id).first()
    if user is None and username:
        user = get_user_by_username(db, username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user