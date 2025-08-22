# backend/superadmin/auth.py

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from auth.jwt_utils import create_access_token, verify_jwt
from auth.user_models import User
from auth.rbac import Role
from auth.auth_service import authenticate_user, create_user
from database import get_db
from logging_setup import get_logger
from config_loader import get_config

logger = get_logger(__name__)
config = get_config()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/superadmin/token")

async def create_superadmin_users(db: Session):
    """
    Ensures the default superadmin users exist by reading from the config.
    """
    # [SNIPPET]: thinkwithai + kenyafirst + enterprise-secure
    # [CONTEXT]: Seeding superadmin users from a secure configuration source instead of hardcoded values.
    # [GOAL]: Eliminate hardcoded credentials and improve security posture.
    # [TASK]: Replace hardcoded list with a loop over config.auth.super_admins.
    if not config.auth.super_admins:
        logger.warning("No super admins defined in the configuration. Skipping super admin seeding.")
        return

    for admin_data in config.auth.super_admins:
        existing_user = db.query(User).filter_by(username=admin_data["username"]).first()
        if not existing_user:
            logger.info(f"Seeding super admin user: {admin_data['username']}")
            create_user(
                db,
                username=admin_data["username"],
                email=admin_data["email"],
                password=admin_data["password"],
                tenant_name="default", # Super admins belong to the default tenant
                role=admin_data["role"]
            )
        else:
            logger.info(f"Super admin user {admin_data['username']} already exists.")

async def superadmin_login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user or user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password or not an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.auth.access_token_expire_minutes)
    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username, "tenant_id": user.tenant_id, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_superadmin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_jwt(token)
        user_id: str = payload.get("user_id")
        user_role: str = payload.get("role")
        if user_id is None or user_role != Role.ADMIN:
            raise credentials_exception
    except Exception as e:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or user.role != Role.ADMIN:
        raise credentials_exception
    return user
