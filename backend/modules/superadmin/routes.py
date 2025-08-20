from fastapi import APIRouter, Depends, HTTPException
from backend.modules.superadmin.superadmin_service import get_metrics
from backend.utils.auth import get_current_user

router = APIRouter(prefix="/superadmin")

@router.get("/metrics")
def superadmin_metrics(current_user=Depends(get_current_user)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return get_metrics()
