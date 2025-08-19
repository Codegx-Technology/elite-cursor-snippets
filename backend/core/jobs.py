from typing import Dict, Any
import uuid
import asyncio
import logging
from backend.depwatcher.patcher import apply_patch_plan
from backend.depwatcher.approvals import _patch_plans # Access the in-memory storage

logger = logging.getLogger(__name__)

# In-memory job storage (replace with database in production)
jobs_storage: Dict[str, Dict[str, Any]] = {}

async def enqueue_job(job_type: str, payload: Dict[str, Any]) -> str:
    job_id = str(uuid.uuid4())
    job = {
        "id": job_id,
        "type": job_type,
        "status": "pending",
        "progress": 0,
        "payload": payload,
        "result": None,
        "error": None
    }
    jobs_storage[job_id] = job
    logger.info(f"Job enqueued: {job_type} with ID {job_id}")
    # In a real system, this would dispatch to a background worker (e.g., Celery)
    asyncio.create_task(_process_job(job_id, job_type, payload)) # For demo, run in current event loop
    return job_id

async def _process_job(job_id: str, job_type: str, payload: Dict[str, Any]):
    job = jobs_storage[job_id]
    try:
        job["status"] = "running"
        logger.info(f"Processing job {job_id} ({job_type})")
        job["progress"] = 0 # Reset progress for actual work

        if job_type == "APPLY_PATCH_PLAN":
            plan_id = payload.get("plan_id")
            if not plan_id:
                raise ValueError("Patch plan ID not provided in payload.")
            
            # Retrieve the PatchPlan object from in-memory storage
            patch_plan = next((p for p in _patch_plans if p.id == plan_id), None)
            if not patch_plan:
                raise ValueError(f"Patch plan with ID {plan_id} not found.")

            await apply_patch_plan(patch_plan) # Call the actual patch application
            job["result"] = {"message": "Patch applied successfully"}
        else:
            # Simulate work for other job types
            await asyncio.sleep(2) 
            job["progress"] = 100
            job["result"] = {"message": f"Processed {job_type} (simulated)"}

        job["status"] = "completed"
        job["progress"] = 100
        logger.info(f"Job {job_id} ({job_type}) completed.")

    except Exception as e:
        job["status"] = "failed"
        job["error"] = str(e)
        logger.error(f"Job {job_id} ({job_type}) failed: {e}")

async def get_job_status(job_id: str) -> Dict[str, Any]:
    return jobs_storage.get(job_id, {"status": "not_found"})