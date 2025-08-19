from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Callable, Awaitable
from logging_setup import get_logger
from config_loader import get_config
from billing_models import get_user_subscription, get_default_plans # Assuming these are accessible

logger = get_logger(__name__)
config = get_config()

class PolicyResolverMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[JSONResponse]]):
        # Skip policy resolution for health checks or static files
        if request.url.path.startswith("/health") or request.url.path.startswith("/static"):
            return await call_next(request)

        # Get user ID from request state (assuming it's set by an auth middleware)
        user_id = request.state.get("user_id") # Or however user_id is extracted

        if not user_id:
            # For unauthenticated requests, apply default FREE tier policy
            user_tier_code = "FREE"
            logger.debug("Unauthenticated request. Applying FREE tier policy.")
        else:
            # Fetch user's subscription and determine tier
            user_subscription = get_user_subscription(user_id)
            all_plans = get_default_plans()
            user_plan = next((p for p in all_plans if p.name == user_subscription.plan_name), None)

            if not user_plan:
                logger.error(f"User {user_id} has an unknown plan: {user_subscription.plan_name}. Defaulting to FREE tier.")
                user_tier_code = "FREE"
            else:
                user_tier_code = user_plan.tier_code
                request.state.user_plan = user_plan # Attach plan to request state for later use

        # Attach tier code to request state
        request.state.user_tier_code = user_tier_code

        # TODO: Implement full policy resolution logic here:
        # 1. Decide: pinned vs latest vs allow_minor (semver compare).
        # 2. Build ordered provider list (respect tier.providers[taskType]).
        # 3. Enforce quotas/rate limits/concurrency (pre-check).
        # 4. Attach to req.ctx: { taskType, model, version, providers[], priorityQueue, costBudget }.
        # 5. If policy forbids unverified models and chosen is unverified → downgrade to next provider.

        # For now, just pass through after setting tier code
        response = await call_next(request)
        return response
