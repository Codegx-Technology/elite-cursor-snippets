import requests
from typing import Optional, List, Dict, Any
from dataclasses import asdict
from billing_models import get_default_plans, Plan, ModelPolicy, Quotas, MonthlyQuotas, RateLimit, PinnedModel, CostCaps, Visibility

class PlanGuardException(Exception):
    """Custom exception for PlanGuard related errors."""
    pass

class PlanGuard:
    def __init__(self, backend_api_url: str = "http://localhost:8000"):
        self.backend_api_url = backend_api_url
        self._cached_plans: Optional[List[Plan]] = None

    async def _fetch_plans_from_api(self) -> Optional[List[Plan]]:
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

    async def get_user_plan(self, user_id: str) -> Plan:
        # In a real system, this would fetch the user's specific plan from a database
        # For now, we'll simulate by assigning based on user_id or default to 'Free'
        # and use the plans fetched from API or default hardcoded ones.
        
        if not self._cached_plans:
            self._cached_plans = await self._fetch_plans_from_api()
            if not self._cached_plans:
                self._cached_plans = get_default_plans() # Fallback to hardcoded defaults

        # Simulate user plan assignment
        if user_id == "test_pro_user":
            plan_name = "Pro"
        elif user_id == "test_enterprise_user":
            plan_name = "Enterprise"
        else:
            plan_name = "Starter" # Default for all other users

        for plan in self._cached_plans:
            if plan.name == plan_name:
                return plan
        
        # Should not happen if default plans are correctly defined
        print(f"Warning: Plan '{plan_name}' not found. Returning Starter plan.")
        return next(p for p in self._cached_plans if p.name == "Starter")

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
