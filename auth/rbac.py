# // [TASK]: Implement Role-Based Access Control (RBAC)
# // [GOAL]: Secure endpoints based on user roles
# // [ELITE_CURSOR_SNIPPET]: securitycheck

from fastapi import Depends, HTTPException
from auth.user_models import User
from auth.auth_service import get_current_active_user
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

def has_role(required_role: Role):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        # In a real application, you would fetch the user's roles from the database.
        # For this example, we'll assume the role is stored in the user model.
        if not hasattr(current_user, "role") or getattr(current_user, "role") != required_role:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return current_user
    return role_checker