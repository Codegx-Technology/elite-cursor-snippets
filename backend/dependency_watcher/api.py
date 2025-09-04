from fastapi import APIRouter, Depends, HTTPException, status
from backend.dependency_watcher.dependency_watcher import run_dependency_check
from backend.api import verify_admin # Import the actual admin verification function

router = APIRouter(prefix="/api/dependencies", tags=["dependencies"])

@router.get("/status")
async def get_dependency_status(current_user: bool = Depends(verify_admin)):
    """
    Returns the current status of all monitored dependencies.
    Requires admin privileges.
    """
    # run_dependency_check() already logs and notifies admin on issues
    # It also returns the status report
    status_report = run_dependency_check()
    return {"dependencies": status_report}