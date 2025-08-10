from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from auth.user_models import User, Tenant
from auth.jwt_utils import create_jwt
from logging_setup import get_logger
from config_loader import get_config

logger = get_logger(__name__)
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
    hashed_password = get_password_hash(password)
    
    # Ensure tenant exists or create it
    tenant = db.query(Tenant).filter(Tenant.name == tenant_name).first()
    if not tenant:
        tenant = Tenant(name=tenant_name)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        logger.info(f"Created new tenant: {tenant_name}")

    db_user = User(username=username, email=email, hashed_password=hashed_password, tenant_id=tenant.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User {username} created successfully for tenant {tenant_name}.")
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """
    // [TASK]: Authenticate a user
    // [GOAL]: Verify user credentials for login
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
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
    return create_jwt(to_encode)
