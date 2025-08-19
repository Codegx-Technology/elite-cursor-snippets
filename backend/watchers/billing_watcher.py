from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.notifications.admin_notifier import notify_admin
from backend.services.quota_service import quota_service, get_user_monthly_cost
from billing_models import get_default_plans, get_user_subscription
from logging_setup import get_logger
from database import SessionLocal

logger = get_logger(__name__)

async def check_billing_thresholds():
    """
    Checks user quotas and cost caps and sends notifications if thresholds are met.
    This function should be run periodically (e.g., as a Celery beat task).
    """
    logger.info("Running billing threshold checks...")
    db = SessionLocal()
    try:
        all_plans = get_default_plans()
        # In a real system, you would iterate through all active users
        # For demonstration, we'll check a few example users or all users with recent activity
        
        # Example: Iterate through users who have consumed resources this month
        # This would require a query to UsageCost or a Redis key scan
        # For now, let's simulate checking a few users
        example_user_ids = ["test_free_user", "test_pro_user", "user_with_high_usage"]

        for user_id in example_user_ids:
            user_subscription = get_user_subscription(user_id)
            user_plan = next((p for p in all_plans if p.name == user_subscription.plan_name), None)

            if not user_plan:
                logger.warning(f"Skipping billing check for user {user_id}: unknown plan {user_subscription.plan_name}")
                continue

            # --- Quota Thresholds ---
            # This would require fetching current monthly usage for each metric (tokens, audioSecs, videoMins, jobs)
            # from Redis (similar to how check_and_increment_quota works, but just getting the value)
            # For now, let's assume we can get current usage for 'jobs'
            current_jobs_usage = await quota_service.redis_client.get(await quota_service._get_monthly_key(user_id, "jobs"))
            current_jobs_usage = int(current_jobs_usage) if current_jobs_usage else 0
            monthly_jobs_limit = user_plan.quotas.monthly.jobs

            if monthly_jobs_limit > 0:
                if current_jobs_usage >= monthly_jobs_limit * 0.8 and current_jobs_usage < monthly_jobs_limit * 0.95:
                    notify_admin(
                        subject=f"[Billing Alert] {user_id}: 80% Job Quota Used",
                        message=f"User {user_id} has used 80% of their monthly job quota ({current_jobs_usage}/{monthly_jobs_limit})."
                    )
                elif current_jobs_usage >= monthly_jobs_limit * 0.95 and current_jobs_usage < monthly_jobs_limit:
                    notify_admin(
                        subject=f"[Billing Alert] {user_id}: 95% Job Quota Used",
                        message=f"User {user_id} has used 95% of their monthly job quota ({current_jobs_usage}/{monthly_jobs_limit})."
                    )
                elif current_jobs_usage >= monthly_jobs_limit:
                    notify_admin(
                        subject=f"[Billing Alert] {user_id}: 100% Job Quota Used",
                        message=f"User {user_id} has used 100% of their monthly job quota ({current_jobs_usage}/{monthly_jobs_limit})."
                    )

            # --- Cost Cap Thresholds ---
            if user_plan.cost_caps.monthlyUsd > 0:
                current_monthly_cost = await get_user_monthly_cost(user_id, db)
                monthly_cost_limit = user_plan.cost_caps.monthlyUsd

                if current_monthly_cost >= monthly_cost_limit * 0.8 and current_monthly_cost < monthly_cost_limit * 0.95:
                    notify_admin(
                        subject=f"[Billing Alert] {user_id}: 80% Cost Cap Used",
                        message=f"User {user_id} has used 80% of their monthly cost cap ({current_monthly_cost:.2f}/{monthly_cost_limit:.2f} USD)."
                    )
                elif current_monthly_cost >= monthly_cost_limit * 0.95 and current_monthly_cost < monthly_cost_limit:
                    notify_admin(
                        subject=f"[Billing Alert] {user_id}: 95% Cost Cap Used",
                        message=f"User {user_id} has used 95% of their monthly cost cap ({current_monthly_cost:.2f}/{monthly_cost_limit:.2f} USD)."
                    )
                elif current_monthly_cost >= monthly_cost_limit:
                    notify_admin(
                        subject=f"[Billing Alert] {user_id}: 100% Cost Cap Used",
                        message=f"User {user_id} has used 100% of their monthly cost cap ({current_monthly_cost:.2f}/{monthly_cost_limit:.2f} USD)."
                    )
                    if user_plan.cost_caps.hardStop:
                        notify_admin(
                            subject=f"[Billing Alert] {user_id}: Hard Stop Activated",
                            message=f"User {user_id} has reached their monthly cost cap and hard stop is activated. Further high-cost tasks will be blocked."
                        )

    except Exception as e:
        logger.error(f"Error during billing threshold checks: {e}", exc_info=True)
    finally:
        db.close()

# This function would be scheduled by Celery Beat or similar scheduler
# @app.task
# def scheduled_billing_check():
#     asyncio.run(check_billing_thresholds())
