from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from auth.user_models import User, Tenant
from auth.jwt_utils import create_jwt
from logging_setup import get_logger, get_audit_logger # Import get_audit_logger
from config_loader import get_config

logger = get_logger(__name__)
audit_logger = get_audit_logger() # Get audit logger
config = get_config()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """
    // [TASK]: Hash a plain-text password
    // [GOAL]: Securely store user passwords
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    // [TASK]: Verify a plain-text password against a hashed password
    // [GOAL]: Authenticate user login attempts
    """
    return pwd_context.verify(plain_password, hashed_password)

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

def create_user(db: Session, username: str, email: str, password: str, tenant_name: str = "default"):
    """
    // [TASK]: Create a new user in the database
    // [GOAL]: Handle user registration
    """
    # Check if username or email already exists
    if get_user_by_username(db, username):
        audit_logger.warning(f"Registration failed: Username {username} already exists.", extra={'user_id': None})
        return None
    if get_user_by_email(db, email):
        audit_logger.warning(f"Registration failed: Email {email} already exists.", extra={'user_id': None})
        return None

    hashed_password = get_password_hash(password)
    
    # Ensure tenant exists or create it
    tenant = db.query(Tenant).filter(Tenant.name == tenant_name).first()
    if not tenant:
        tenant = Tenant(name=tenant_name)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        audit_logger.info(f"New tenant created: {tenant_name}", extra={'user_id': None})

    db_user = User(username=username, email=email, hashed_password=hashed_password, tenant_id=tenant.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    audit_logger.info(f"User {username} registered successfully for tenant {tenant_name}.")
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """
    // [TASK]: Authenticate a user
    // [GOAL]: Verify user credentials for login
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        audit_logger.warning(f"Authentication failed: Invalid credentials for username {username}.", extra={'user_id': None})
        return False
    audit_logger.info(f"User {username} authenticated successfully.", extra={'user_id': user.id if user else None})
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
    audit_logger.info(f"Access token created for user: {data.get('username')}", extra={'user_id': data.get('user_id')})
    return token

def update_user_profile(db: Session, user_id: int, user_update_data: dict):
    """
    // [TASK]: Update a user's profile information
    // [GOAL]: Allow users to modify their profile
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        audit_logger.warning(f"Profile update failed: User with ID {user_id} not found.", extra={'user_id': user_id})
        return None

    for key, value in user_update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    audit_logger.info(f"User profile updated for user ID: {user_id}", extra={'user_id': user_id})
    return user