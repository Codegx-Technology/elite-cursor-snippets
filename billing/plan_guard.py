import requests
from typing import Optional, List, Dict, Any, Callable
from dataclasses import asdict
from datetime import datetime, timedelta # Import datetime and timedelta
from sqlalchemy.orm import Session # Import Session
from auth.user_models import User, Role # Import User and Role
from billing_models import get_default_plans, Plan, ModelPolicy, Quotas, MonthlyQuotas, RateLimit, PinnedModel, CostCaps, Visibility

class PlanGuardException(Exception):
    """Custom exception for PlanGuard related errors."""
    def __init__(self, message: str, is_in_grace_mode: bool = False, grace_expires_at: Optional[datetime] = None, is_view_only: bool = False):
        super().__init__(message)
        self.is_in_grace_mode = is_in_grace_mode
        self.grace_expires_at = grace_expires_at
        self.is_view_only = is_view_only

class PlanGuard:
    def __init__(self, backend_api_url: str = "http://localhost:8000", db_session_factory: Optional[Callable[[], Session]] = None):
        self.backend_api_url = backend_api_url
        self._cached_plans: Optional[List[Plan]] = None
        self.db_session_factory = db_session_factory # Store the session factory

    async def _fetch_plans_from_api(self) -> Optional[List[Plan]>:
        try:
            response = requests.get(f"{self.backend_api_url}/api/plans")
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            
            # Deserialize JSON data back into Plan dataclass objects
            plans = []
            for p_data in data:
                # Handle nested dataclasses
                model_policy = ModelPolicy(**p_data.pop('model_policy', {}))
                quotas_data = p_data.pop('quotas', {})
                monthly_quotas = MonthlyQuotas(**quotas_data.pop('monthly', {}))
                rate_limit = RateLimit(**quotas_data.pop('rateLimit', {}))
                quotas = Quotas(monthly=monthly_quotas, rateLimit=rate_limit, **quotas_data)
                cost_caps = CostCaps(**p_data.pop('cost_caps', {}))
                visibility = Visibility(**p_data.pop('visibility', {}))

                plan = Plan(
                    model_policy=model_policy,
                    quotas=quotas,
                    cost_caps=cost_caps,
                    visibility=visibility,
                    **p_data
                )
                plans.append(plan)
            self._cached_plans = plans
            return plans
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not connect to backend API at {self.backend_api_url}. Falling back to default plans. Error: {e}")
            return None
        except Exception as e:
            print(f"Error fetching plans from API: {e}")
            return None

    async def _is_super_admin(self, user_id: str) -> bool:
        if not self.db_session_factory:
            print("Warning: db_session_factory not provided to PlanGuard. Cannot check super admin status.")
            return False
        
        with self.db_session_factory() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user and user.role == Role.ADMIN: # Assuming 'admin' is the role for super admins
                return True
            return False

    async def get_user_plan(self, user_id: str) -> Plan:
        # In a real system, this would fetch the user's specific plan from a database
        # For now, we'll simulate by assigning based on user_id or default to 'Starter'
        # and use the plans fetched from API or default hardcoded ones.
        
        if not self._cached_plans:
            self._cached_plans = await self._fetch_plans_from_api()
            if not self._cached_plans:
                self._cached_plans = get_default_plans() # Fallback to hardcoded defaults

        # Simulate user plan assignment and grace period
        user_sub = get_user_subscription(user_id) # This function needs to be updated to return grace_expires_at
        
        # Find the plan based on user_sub.plan_name
        current_plan = next((p for p in self._cached_plans if p.name == user_sub.plan_name), None)
        if not current_plan:
            print(f"Warning: Plan '{user_sub.plan_name}' not found. Returning Starter plan.")
            current_plan = next(p for p in self._cached_plans if p.name == "Starter")

        # Simulate grace period logic
        if not user_sub.is_active and current_plan.grace_period_hours > 0:
            # If user's subscription is inactive, but they have a grace period
            # and grace_expires_at is not set or has passed, set it.
            if not user_sub.grace_expires_at or user_sub.grace_expires_at < datetime.now():
                user_sub.grace_expires_at = datetime.now() + timedelta(hours=current_plan.grace_period_hours)
                print(f"User {user_id} entered grace mode. Expires at: {user_sub.grace_expires_at}")
            
            if datetime.now() < user_sub.grace_expires_at:
                # User is in grace mode
                raise PlanGuardException(
                    f"Plan expired. You are in grace mode. Expires: {user_sub.grace_expires_at}",
                    is_in_grace_mode=True,
                    grace_expires_at=user_sub.grace_expires_at
                )
            else:
                # Grace period expired, enter view-only mode
                user_sub.grace_expires_at = None # Reset grace period
                user_sub.is_active = False # Ensure it's marked inactive
                raise PlanGuardException("Plan expired. Grace period exhausted. Entering view-only mode.", is_view_only=True)
        elif not user_sub.is_active and current_plan.grace_period_hours == 0:
            # Immediate hard-lock for plans with no grace period
            raise PlanGuardException("Plan expired. Please upgrade.")

        return current_plan

    async def check_model_access(self, user_id: str, requested_model: str) -> None:
        user_plan = await self.get_user_plan(user_id)
        if requested_model not in user_plan.model_policy.allowed_models:
            raise PlanGuardException(f"Model '{requested_model}' is not allowed for your '{user_plan.name}' plan.")

    async def check_tts_voice_access(self, user_id: str, requested_voice: str) -> None:
        user_plan = await self.get_user_plan(user_id)
        if requested_voice not in user_plan.model_policy.tts_voices:
            raise PlanGuardException(f"TTS voice '{requested_voice}' is not allowed for your '{user_plan.name}' plan.")

    async def check_download_permission(self, user_id: str) -> None:
        user_plan = await self.get_user_plan(user_id)
        # For simplicity, assume only Enterprise plan allows direct downloads
        if user_plan.name != "Enterprise":
            raise PlanGuardException(f"Direct downloads are not allowed for your '{user_plan.name}' plan. Please upgrade to Enterprise.")

    async def check_runtime_usage(self, user_id: str, feature: str, usage_amount: int = 1) -> None:
        user_plan = await self.get_user_plan(user_id)
        # This is a simplified check. Real implementation would track actual usage.
        if feature == "video_generation" and user_plan.quotas.monthly.videoMins == 0:
            raise PlanGuardException(f"Video generation is not allowed for your '{user_plan.name}' plan.")
        # Add more detailed quota checks here based on feature and usage_amount
        print(f"User {user_id} on plan {user_plan.name} is allowed to use {feature}.")

    async def check_rollback_permission(self, user_id: str) -> None:
        user_plan = await self.get_user_plan(user_id)
        if user_plan.rollback_window_days == 0:
            raise PlanGuardException(f"Rollback is not allowed for your '{user_plan.name}' plan. Please upgrade.")
        print(f"User {user_id} on plan {user_plan.name} has rollback permission.")

    async def check_action_permission(self, user_id: str, action_type: str) -> None:
        """
        Checks if the user has permission to perform a specific action type.
        Allows READ/EXPORT in view-only mode, blocks others.
        Super admins can bypass all checks.
        """
        if await self._is_super_admin(user_id):
            print(f"Super admin {user_id} bypassing PlanGuard for action '{action_type}'.")
            return # Super admins bypass all checks

        try:
            user_plan = await self.get_user_plan(user_id)
            # If get_user_plan raises PlanGuardException with is_view_only=True,
            # it means the user is in view-only mode.
        except PlanGuardException as e:
            if e.is_view_only:
                if action_type.upper() in ["READ", "EXPORT"]:
                    print(f"User {user_id} is in view-only mode, but action '{action_type}' is allowed.")
                    return # Allowed
                else:
                    raise PlanGuardException(f"Action '{action_type}' is blocked in view-only mode. Upgrade required for full access.", is_view_only=True)
            else:
                # Re-raise other PlanGuardExceptions
                raise e
        
        # If no exception was raised by get_user_plan, the user is active or in grace mode
        # and can perform any action (assuming other checks like check_model_access pass).
        print(f"User {user_id} on plan {user_plan.name} is allowed to perform action '{action_type}'.")

    async def check_dependency_access(self, user_id: str, dependency: str) -> None:
        """
        Checks if the user has access to a specific dependency.
        Super admins can bypass all checks.
        """
        if await self._is_super_admin(user_id):
            print(f"Super admin {user_id} bypassing PlanGuard for dependency '{dependency}'.")
            return # Super admins bypass all checks

        user_plan = await self.get_user_plan(user_id)
        # Assuming dependencies are mapped to allowed_models or features_enabled in the plan
        if dependency not in user_plan.model_policy.allowed_models and \
           dependency not in user_plan.features_enabled: # Assuming features_enabled is a list of strings
            raise PlanGuardException(f"Dependency '{dependency}' is not allowed for your '{user_plan.name}' plan. Upgrade required.")
        print(f"User {user_id} on plan {user_plan.name} is allowed to use dependency '{dependency}'.")

    def get_grace_delay(self, grace_expires_at: datetime) -> float:
        """
        Calculates the artificial delay to inject during grace mode based on remaining time.
        """
        time_left = grace_expires_at - datetime.now()
        remaining_hours = time_left.total_seconds() / 3600

        if remaining_hours > 12:
            return 0.0 # No slowdown for the first 12 hours
        elif remaining_hours > 6:
            return 1.0 # +1s delay for 12-6 hours left
        elif remaining_hours > 1:
            return 3.0 # +3s delay for 6-1 hours left
        else:
            return 5.0 # +5s delay for less than 1 hour left

# Example usage (for testing purposes)
async def main():
    plan_guard = PlanGuard()
    
    # Test fetching plans
    print("Fetching plans from API or using defaults...")
    plans = await plan_guard._fetch_plans_from_api()
    if plans:
        print("Plans fetched successfully:")
        for plan in plans:
            print(f"- {plan.name}: Price={plan.price} {plan.currency}, Allowed Models={plan.model_policy.allowed_models}, Max Requests={plan.max_requests_per_month}")
    else:
        print("Using default hardcoded plans.")

    # Test user plan access and checks
    test_users = ["test_free_user", "test_pro_user", "test_enterprise_user", "unknown_user"]
    for user_id in test_users:
        print(f"\n--- Testing for user: {user_id} ---")
        try:
            plan = await plan_guard.get_user_plan(user_id)
            print(f"User {user_id} is on plan: {plan.name}")

            # Test model access
            try:
                await plan_guard.check_model_access(user_id, "gpt-4o-mini")
                print("gpt-4o-mini access: OK")
            except PlanGuardException as e:
                print(f"gpt-4o-mini access: {e}")

            try:
                await plan_guard.check_model_access(user_id, "gpt-5")
                print("gpt-5 access: OK")
            except PlanGuardException as e:
                print(f"gpt-5 access: {e}")

            # Test TTS voice access
            try:
                await plan_guard.check_tts_voice_access(user_id, "xtts-v2")
                print("xtts-v2 voice access: OK")
            except PlanGuardException as e:
                print(f"xtts-v2 voice access: {e}")

            try:
                await plan_guard.check_tts_voice_access(user_id, "elevenlabs-pro")
                print("elevenlabs-pro voice access: OK")
            except PlanGuardException as e:
                print(f"elevenlabs-pro voice access: {e}")

            # Test download permission
            try:
                await plan_guard.check_download_permission(user_id)
                print("Download permission: OK")
            except PlanGuardException as e:
                print(f"Download permission: {e}")

            # Test runtime usage
            try:
                await plan_guard.check_runtime_usage(user_id, "video_generation")
                print("Video generation usage: OK")
            except PlanGuardException as e:
                print(f"Video generation usage: {e}")

        except Exception as e:
            print(f"An unexpected error occurred for user {user_id}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
