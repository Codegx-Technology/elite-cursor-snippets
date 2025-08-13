# // [TASK]: Implement multi-tenancy middleware and dependency
# // [GOAL]: Securely isolate tenants and provide tenant context to the application
# // [ELITE_CURSOR_SNIPPET]: aihandle

from fastapi import Request, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from auth.jwt_utils import verify_jwt
from database import get_db
from auth.user_models import Tenant
from sqlalchemy.orm import Session

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = verify_jwt(token)
                tenant_id = payload.get("tenant_id")
            except Exception:
                # Invalid token, but we don't want to block public endpoints
                pass
        
        request.state.tenant_id = tenant_id
        response = await call_next(request)
        return response

def get_tenant(request: Request, db: Session = Depends(get_db)) -> Tenant:
    tenant_id = getattr(request.state, "tenant_id", None)
    if tenant_id is None:
        raise HTTPException(status_code=403, detail="Could not validate tenant credentials")

    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    # Note: The returned Tenant object now includes branding fields (theme_name, primary_color, logo_url, custom_domain)
    return tenant

# Alias for dependency
current_tenant = Depends(get_tenant)