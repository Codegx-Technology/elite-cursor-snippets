from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Callable, Awaitable
from logging_setup import get_logger
from config_loader import get_config
from billing_models import get_user_subscription, get_default_plans # Assuming these are accessible
from backend.services.quota_service import quota_service # Import quota_service

logger = get_logger(__name__)
config = get_config()

class PolicyResolverMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[JSONResponse]]):
        # Skip policy resolution for health checks or static files
        if request.url.path.startswith("/health") or request.url.path.startswith("/static"):
            return await call_next(request)

        # Get user ID from request state (assuming it's set by an auth middleware)
        user_id = request.state.get("user_id") # Or however user_id is extracted

        user_plan = None
        if not user_id:
            # For unauthenticated requests, apply default FREE tier policy
            all_plans = get_default_plans()
            user_plan = next((p for p in all_plans if p.tier_code == "FREE"), None)
            if not user_plan:
                logger.critical("FREE tier plan not found in default plans. System misconfiguration.")
                raise HTTPException(status_code=500, detail="System misconfiguration: FREE plan not found.")
            logger.debug("Unauthenticated request. Applying FREE tier policy.")
        else:
            # Fetch user's subscription and determine tier
            user_subscription = get_user_subscription(user_id)
            all_plans = get_default_plans()
            user_plan = next((p for p in all_plans if p.name == user_subscription.plan_name), None)

            if not user_plan:
                logger.error(f"User {user_id} has an unknown plan: {user_subscription.plan_name}. Defaulting to FREE tier.")
                user_plan = next((p for p in all_plans if p.tier_code == "FREE"), None)
                if not user_plan:
                    logger.critical("FREE tier plan not found in default plans. System misconfiguration.")
                    raise HTTPException(status_code=500, detail="System misconfiguration: FREE plan not found.")

        # Attach user_plan to request state for downstream access
        request.state.user_plan = user_plan

        # --- Enforce Quotas and Rate Limits (Pre-check) ---
        # Apply these checks only to resource-consuming endpoints
        if request.url.path == "/generate_video": # Example: apply to video generation
            # Rate Limit Check
            if not await quota_service.check_rate_limit(
                user_id=user_id if user_id else "anonymous",
                rpm_limit=user_plan.quotas.rateLimit.rpm,
                rps_limit=user_plan.quotas.rateLimit.rps,
                burst_limit=user_plan.quotas.rateLimit.burst
            ):
                raise HTTPException(status_code=429, detail="Too Many Requests. Please try again later or upgrade your plan.")
            
            # Quota Check (for jobs metric, assuming 1 job per video generation request)
            # This is a provisional check. Finalization happens after job completion.
            if not await quota_service.check_and_increment_quota(
                user_id=user_id if user_id else "anonymous",
                metric="jobs",
                amount=1,
                monthly_limit=user_plan.quotas.monthly.jobs
            ):
                raise HTTPException(status_code=429, detail="Monthly job quota exceeded. Please upgrade your plan.")
            
            # TODO: Record provisional usage here for the specific job
            # This would require the job_id to be known at this stage, or passed later.
            # For now, check_and_increment_quota acts as a provisional increment.

        # TODO: Implement full policy resolution logic here:
        # 1. Decide: pinned vs latest vs allow_minor (semver compare).
        # 2. Build ordered provider list (respect tier.providers[taskType]).
        # 3. Attach to req.ctx: { taskType, model, version, providers[], priorityQueue, costBudget }.
        # 4. If policy forbids unverified models and chosen is unverified → downgrade to next provider.

        response = await call_next(request)
        return response
