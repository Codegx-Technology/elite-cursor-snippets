from typing import List
from backend.depwatcher.schemas import PatchCandidate, PatchPlan
from datetime import datetime
import uuid

# In-memory storage for patch plans (replace with database in production)
_patch_plans: List[PatchPlan] = []

def create_patch_plan(candidates: List[PatchCandidate], created_by: str, mode: str = "apply") -> PatchPlan:
    """Creates a new patch plan."""
    plan_id = str(uuid.uuid4())
    new_plan = PatchPlan(
        id=plan_id,
        items=candidates,
        mode=mode,
        createdBy=created_by,
        createdAt=datetime.now(),
        status="pending"
    )
    _patch_plans.append(new_plan)
    return new_plan

def list_pending_plans() -> List[PatchPlan]:
    """Lists all pending patch plans."""
    return [plan for plan in _patch_plans if plan.status == "pending"]

def mark_plan_status(plan_id: str, status: str) -> Optional[PatchPlan]:
    """Marks the status of a patch plan."""
    for plan in _patch_plans:
        if plan.id == plan_id:
            plan.status = status
            return plan
    return None
