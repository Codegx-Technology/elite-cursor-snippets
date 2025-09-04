from typing import Dict, Any
import uuid
import logging
from backend.depwatcher.patcher import apply_patch_plan
from backend.depwatcher.approvals import _patch_plans # Access the in-memory storage
from celery_app import app, PRIORITY_QUEUE_MAP # Import Celery app and priority map
from backend.core.jobs_hooks import record_usage_cost # Import record_usage_cost
from database import SessionLocal # Import SessionLocal

logger = logging.getLogger(__name__)

# In-memory job storage (replace with database in production)
jobs_storage: Dict[str, Dict[str, Any]] = {}

@app.task(bind=True) # Make this a Celery task
def process_job_task(self, job_id: str, job_type: str, payload: Dict[str, Any], telemetry_tags: Dict[str, Any]):
    job = jobs_storage[job_id]
    db = SessionLocal() # Create a new session for the task
    try:
        job["status"] = "running"
        logger.info(f"Processing job {job_id} ({job_type}) with tags: {telemetry_tags}")
        job["progress"] = 0 # Reset progress for actual work

        if job_type == "APPLY_PATCH_PLAN":
            plan_id = payload.get("plan_id")
            if not plan_id:
                raise ValueError("Patch plan ID not provided in payload.")
            
            # Retrieve the PatchPlan object from in-memory storage
            patch_plan = next((p for p in _patch_plans if p.id == plan_id), None)
            if not patch_plan:
                raise ValueError(f"Patch plan with ID {plan_id} not found.")

            # apply_patch_plan is async, but Celery tasks are sync. Need to run it in an event loop.
            # For simplicity, we'll use asyncio.run here, but in a real Celery worker,
            # you'd typically use a library like `celery-gevent` or `eventlet` for async tasks.
            import asyncio
            asyncio.run(apply_patch_plan(patch_plan))
            job["result"] = {"message": "Patch applied successfully"}
        else:
            # Simulate work for other job types
            import time
            time.sleep(2) 
            job["progress"] = 100
            job["result"] = {"message": f"Processed {job_type} (simulated)"}

        job["status"] = "completed"
        job["progress"] = 100
        logger.info(f"Job {job_id} ({job_type}) completed.")

        # Record usage cost after successful completion
        # This is a placeholder. Actual cost metrics (amount, metric, provider, model_name, model_version)
        # would come from the job's payload or execution details.
        user_id = telemetry_tags.get("userId", "anonymous")
        tier_code = telemetry_tags.get("tier", "FREE")
        task_type = telemetry_tags.get("taskType", "unknown")
        
        # Example: Record 1 job unit cost
        asyncio.run(record_usage_cost(
            db=db,
            job_id=job_id,
            user_id=user_id,
            tier_code=tier_code,
            task_type=task_type,
            provider="internal", # Placeholder
            metric="jobs",
            amount=1.0,
            model_name="N/A",
            model_version="N/A"
        ))

    except Exception as e:
        job["status"] = "failed"
        job["error"] = str(e)
        logger.error(f"Job {job_id} ({job_type}) failed: {e}")
        
        # Record usage cost for failed job (if applicable, e.g., partial cost)
        # This is a placeholder. Actual cost metrics would come from the job's payload.
        user_id = telemetry_tags.get("userId", "anonymous")
        tier_code = telemetry_tags.get("tier", "FREE")
        task_type = telemetry_tags.get("taskType", "unknown")
        
        asyncio.run(record_usage_cost(
            db=db,
            job_id=job_id,
            user_id=user_id,
            tier_code=tier_code,
            task_type=task_type,
            provider="internal", # Placeholder
            metric="jobs_failed",
            amount=1.0,
            model_name="N/A",
            model_version="N/A",
            actual_cost_usd=0.0 # Or a partial cost if applicable
        ))

        # Celery retry logic
        raise self.retry(exc=e, countdown=5, max_retries=self.request.retries + 1) # Example retry
    finally:
        db.close() # Close the session

async def enqueue_job(job_type: str, payload: Dict[str, Any], user_tier_code: str = "FREE") -> str:
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

    # Determine queue and retries based on tier
    tier_config = PRIORITY_QUEUE_MAP.get(user_tier_code, PRIORITY_QUEUE_MAP["FREE"])
    queue_name = tier_config["queue"]
    max_retries = tier_config["retries"]

    # Prepare telemetry tags
    telemetry_tags = {
        "userId": payload.get("user_id", "anonymous"), # Assuming user_id is in payload
        "tier": user_tier_code,
        "taskType": job_type,
        # Add model@version, provider if available in payload
    }

    # Dispatch Celery task
    process_job_task.apply_async(
        args=[job_id, job_type, payload, telemetry_tags],
        queue=queue_name,
        max_retries=max_retries,
        # Add DLQ routing if configured in celery_app.py
    )
    return job_id

async def get_job_status(job_id: str) -> Dict[str, Any]:
    return jobs_storage.get(job_id, {"status": "not_found"})