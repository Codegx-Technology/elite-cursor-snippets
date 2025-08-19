from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from backend.ai.models import UsageCost
from backend.costs.provider_costs import provider_costs_service
from logging_setup import get_logger

logger = get_logger(__name__)

async def record_usage_cost(
    db: Session,
    job_id: str,
    user_id: str,
    tier_code: str,
    task_type: str,
    provider: str,
    metric: str,
    amount: float,
    model_name: str = None,
    model_version: str = None,
    actual_cost_usd: float = None
):
    estimated_cost_usd = provider_costs_service.get_cost(provider, metric) * amount

    usage_cost = UsageCost(
        job_id=job_id,
        user_id=user_id,
        tier_code=tier_code,
        task_type=task_type,
        model_name=model_name,
        model_version=model_version,
        provider=provider,
        metric=metric,
        amount=amount,
        estimated_cost_usd=estimated_cost_usd,
        actual_cost_usd=actual_cost_usd, # Can be updated later if reconciliation happens
        timestamp=datetime.utcnow()
    )
    db.add(usage_cost)
    db.commit()
    db.refresh(usage_cost)
    logger.info(f"Recorded usage cost for job {job_id}: {estimated_cost_usd:.4f} USD for {amount} {metric} of {task_type}")

# TODO: Implement pre-job budget check in PolicyResolverMiddleware
# This would involve checking user_plan.cost_caps.monthlyUsd against current month's usage
# and raising an HTTPException if exceeded.
