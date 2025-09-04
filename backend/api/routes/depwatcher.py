from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from backend.depwatcher.schemas import PatchCandidate, PatchPlan
from backend.depwatcher.approvals import create_patch_plan, list_pending_plans, mark_plan_status
from backend.core.jobs import enqueue_job, get_job_status
from backend.core.authz import is_admin # Import the new is_admin function
from backend.api import verify_admin # Import the actual admin verification from main api
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/depwatcher", tags=["Dependency Watcher"])

@router.post("/plan", response_model=PatchPlan)
async def create_plan_endpoint(candidates: List[PatchCandidate], current_user: Dict[str, Any] = Depends(verify_admin)):
    """
    Creates a new patch plan from a list of patch candidates.
    Requires admin privileges.
    """
    # Placeholder for strict validation of PatchPlan items
    # Ensure no arbitrary shell commands, whitelisted indices/extra-index, sanitized model IDs
    for candidate in candidates:
        if candidate.kind == "pip":
            # Example: validate package name, version format
            if not all(c.isalnum() or c in '.-_' for c in candidate.name):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid package name: {candidate.name}")
        elif candidate.kind == "model":
            # Example: validate model ID format (e.g., no ../ or special chars)
            if not all(c.isalnum() or c in './-_' for c in candidate.name):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid model ID: {candidate.name}")
        # Add more validation as needed

    # Log audit trail: who approved, when, what changed
    logger.info(f"Audit: Admin user {current_user.get("username", "unknown")} created patch plan with candidates: {[c.dict() for c in candidates]}")

    plan = create_patch_plan(candidates, created_by=current_user.get("username", "unknown"), mode="apply")
    logger.info(f"Created new patch plan: {plan.id}")
    return plan

@router.post("/approve/{plan_id}", response_model=PatchPlan)
async def approve_plan_endpoint(plan_id: str, current_user: Dict[str, Any] = Depends(verify_admin)):
    """
    Approves a pending patch plan.
    Requires admin privileges.
    """
    if not is_admin(current_user): # Explicit admin role check
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can approve patch plans.")
    
    plan = mark_plan_status(plan_id, "approved")
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patch plan not found")
    
    logger.info(f"Audit: Admin user {current_user.get("username", "unknown")} approved patch plan: {plan.id}")
    logger.info(f"Approved patch plan: {plan.id}")
    return plan

@router.post("/dry-run/{plan_id}", response_model=Dict)
async def dry_run_plan_endpoint(plan_id: str, current_user: Dict[str, Any] = Depends(verify_admin)):
    """
    Performs a dry run of a patch plan.
    Requires admin privileges.
    """
    # In a real implementation, this would call patcher.apply_patch_plan with mode="dry-run"
    # and return detailed logs/diffs.
    logger.info(f"Audit: Admin user {current_user.get("username", "unknown")} initiated dry run for patch plan: {plan_id}")
    logger.info(f"Performing dry run for patch plan: {plan_id}")
    return {"status": "dry_run_simulated", "plan_id": plan_id, "message": "Dry run simulated. Actual dry run logic to be implemented."}

@router.post("/apply/{plan_id}", response_model=Dict)
async def apply_plan_endpoint(plan_id: str, current_user: Dict[str, Any] = Depends(verify_admin)):
    """
    Applies a patch plan by enqueuing a background job.
    Requires admin privileges.
    """
    if not is_admin(current_user): # Explicit admin role check
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can apply patch plans.")

    plan = mark_plan_status(plan_id, "applying") # Mark as applying
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patch plan not found")
    
    job_id = await enqueue_job("APPLY_PATCH_PLAN", {"plan_id": plan_id})
    logger.info(f"Audit: Admin user {current_user.get("username", "unknown")} enqueued apply job for patch plan {plan_id}. Job ID: {job_id}")
    logger.info(f"Enqueued apply job for patch plan {plan_id}. Job ID: {job_id}")
    return {"status": "job_enqueued", "job_id": job_id, "plan_id": plan_id}

@router.get("/jobs/{job_id}/status", response_model=Dict)
async def get_job_status_endpoint(job_id: str, current_user: Dict[str, Any] = Depends(verify_admin)):
    """
    Gets the status of a background job.
    Requires admin privileges.
    """
    # No explicit is_admin check here, as verify_admin already ensures authentication
    # and job status might be viewable by any authenticated user, or only admin. (Assuming for now that verify_admin is sufficient.)
    status = await get_job_status(job_id)
    return status

@router.get("/pending_plans", response_model=List[PatchPlan])
async def get_pending_plans_endpoint(current_user: Dict[str, Any] = Depends(verify_admin)):
    """
    Gets a list of all pending patch plans.
    Requires admin privileges.
    """
    # Assuming verify_admin is sufficient for viewing pending plans
    return list_pending_plans()