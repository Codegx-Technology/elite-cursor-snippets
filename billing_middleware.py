from datetime import datetime
from billing_models import get_user_subscription, get_default_plans
from redis_client import redis_client
from logging_setup import get_logger

logger = get_logger(__name__)

class BillingException(Exception):
    """Custom exception for billing-related errors."""
    pass

def enforce_limits(user_id: str, feature_name: str) -> bool:
    """
    // [TASK]: Enforce feature limits based on user's subscription plan
    // [GOAL]: Restrict access to features for users exceeding their plan limits
    """
    try:
        user_sub = get_user_subscription(user_id)
        all_plans = get_default_plans()
        current_plan = next((p for p in all_plans if p.name == user_sub.plan_name), None)

        if not current_plan:
            logger.error(f"User {user_id} has unknown plan: {user_sub.plan_name}")
            raise BillingException("Invalid subscription plan.")

        # Check feature gating
        if feature_name not in current_plan.features_enabled:
            logger.warning(f"Feature '{feature_name}' not enabled for plan '{current_plan.name}' (User: {user_id})")
            raise BillingException(f"Feature '{feature_name}' requires plan upgrade.")

        # Apply request-based limits using Redis counters
        if current_plan.max_requests_per_day > 0:
            current_day = datetime.now().strftime("%Y-%m-%d")
            counter_key = f"{feature_name}:{current_day}"
            
            current_count = redis_client.get_counter(user_id, counter_key)

            if current_count >= current_plan.max_requests_per_day:
                logger.warning(f"User {user_id} exceeded daily limit for {feature_name} ({current_count}/{current_plan.max_requests_per_day})")
                raise BillingException(f"Daily limit for '{feature_name}' exceeded. Upgrade required.")
            
            redis_client.increment_counter(user_id, counter_key)
            logger.info(f"User {user_id} used {feature_name}: {current_count + 1}/{current_plan.max_requests_per_day}")
        
        return True

    except BillingException as e:
        logger.warning(f"Billing enforcement failed for user {user_id}: {e}")
        # Return a 403-like response conceptually
        # In a web framework, this would be an actual HTTP 403 response
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred during billing enforcement for user {user_id}: {e}", exc_info=True)
        raise BillingException("Internal billing error.")

# Example of how it would be used in a pipeline (conceptual)
async def conceptual_pipeline_step(user_id: str, data: str):
    """
    // [TASK]: Conceptual pipeline step demonstrating billing enforcement
    // [GOAL]: Show where enforce_limits would be called
    """
    feature_used = "text_gen"
    try:
        enforce_limits(user_id, feature_used)
        logger.info(f"User {user_id} is allowed to use {feature_used}. Processing data: {data[:20]}...")
        # Actual processing logic here
        return {"status": "success", "message": "Request processed."}
    except BillingException as e:
        logger.error(f"Request denied for user {user_id}: {e}")
        return {"status": "error", "message": str(e), "code": 403}
    except Exception as e:
        logger.error(f"Unexpected error for user {user_id}: {e}")
        return {"status": "error", "message": "Internal server error.", "code": 500}
