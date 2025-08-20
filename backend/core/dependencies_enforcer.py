# New module to handle core + widget dependencies globally
# - Validate dependencies on widget install/update
# - Enforce PlanGuard rules at runtime
# - Return structured error messages if dependency missing
# - Provide global grace (24h) + degrade modes (slowdown, view-only)
# Hook into widget_manager + plan_guard

from typing import List, Dict, Any, Optional
from billing.plan_guard import PlanGuard, PlanGuardException
import logging

logger = logging.getLogger(__name__)

class DependencyEnforcer:
    def __init__(self, plan_guard: PlanGuard):
        self.plan_guard = plan_guard

    async def check_dependencies(self, user_id: str, dependencies: List[str]) -> Dict[str, Any]:
        """
        Checks if a user's plan allows all specified dependencies.
        Returns a structured response indicating allowance and any issues.
        """
        try:
            user_plan = await self.plan_guard.get_user_plan(user_id)
            
            disallowed_deps = []
            for dep in dependencies:
                # For simplicity, we'll assume dependencies map to allowed_models or features_enabled
                # A more robust system would have a dedicated mapping for each dependency type
                if dep not in user_plan.model_policy.allowed_models and dep not in user_plan.features_enabled:
                    disallowed_deps.append(dep)
            
            if disallowed_deps:
                message = f"Your plan ({user_plan.name}) does not allow the following dependencies: {', '.join(disallowed_deps)}. Upgrade required."
                return {"allowed": False, "message": message, "plan_name": user_plan.name, "state": "locked"}
            
            # Check for grace mode or view-only mode
            # This logic is already handled by plan_guard.get_user_plan and PlanGuardException
            # If get_user_plan raises an exception, it will be caught by the caller

            return {"allowed": True, "message": "All dependencies allowed.", "plan_name": user_plan.name, "state": "healthy"}
        except PlanGuardException as e:
            # Propagate PlanGuardException details
            return {"allowed": False, "message": e.message, "state": "grace" if e.is_in_grace_mode else ("view_only" if e.is_view_only else "locked"), "grace_expires_at": e.grace_expires_at.isoformat() if e.grace_expires_at else None}
        except Exception as e:
            logger.error(f"Unexpected error in DependencyEnforcer.check_dependencies for user {user_id}: {e}")
            return {"allowed": False, "message": "Internal server error during dependency check.", "state": "error"}

    async def enforce_runtime(self, user_id: str, module_name: str, dependencies: List[str]) -> None:
        """
        Enforces PlanGuard rules at runtime for a given module and its dependencies.
        Raises PlanGuardException if enforcement fails (Hard Lock).
        """
        check_result = await self.check_dependencies(user_id, dependencies)
        if not check_result["allowed"]:
            raise PlanGuardException(check_result["message"], 
                                     is_in_grace_mode=check_result.get("state") == "grace", 
                                     grace_expires_at=check_result.get("grace_expires_at"),
                                     is_view_only=check_result.get("state") == "view_only")

# Example usage (for testing purposes)
async def main():
    from billing.plan_guard import PlanGuard
    plan_guard_instance = PlanGuard()
    dependency_enforcer = DependencyEnforcer(plan_guard_instance)

    print("\n--- Testing Dependency Enforcement ---")

    # Test user with allowed dependencies
    user_id_healthy = "test_pro_user"
    deps_healthy = ["gpt-4o", "analytics"]
    result_healthy = await dependency_enforcer.check_dependencies(user_id_healthy, deps_healthy)
    print(f"User {user_id_healthy} with deps {deps_healthy}: {result_healthy}")
    try:
        await dependency_enforcer.enforce_runtime(user_id_healthy, "test_module", deps_healthy)
        print(f"Runtime enforcement for {user_id_healthy} with {deps_healthy}: OK")
    except PlanGuardException as e:
        print(f"Runtime enforcement for {user_id_healthy} with {deps_healthy}: BLOCKED - {e.message}")

    # Test user with disallowed dependencies
    user_id_blocked = "test_free_user"
    deps_blocked = ["gpt-5", "enterprise_features"]
    result_blocked = await dependency_enforcer.check_dependencies(user_id_blocked, deps_blocked)
    print(f"User {user_id_blocked} with deps {deps_blocked}: {result_blocked}")
    try:
        await dependency_enforcer.enforce_runtime(user_id_blocked, "test_module", deps_blocked)
        print(f"Runtime enforcement for {user_id_blocked} with {deps_blocked}: OK")
    except PlanGuardException as e:
        print(f"Runtime enforcement for {user_id_blocked} with {deps_blocked}: BLOCKED - {e.message}")

    # Test user in grace mode
    user_id_grace = "test_expired_pro_user"
    deps_grace = ["gpt-4o"]
    result_grace = await dependency_enforcer.check_dependencies(user_id_grace, deps_grace)
    print(f"User {user_id_grace} with deps {deps_grace}: {result_grace}")
    try:
        await dependency_enforcer.enforce_runtime(user_id_grace, "test_module", deps_grace)
        print(f"Runtime enforcement for {user_id_grace} with {deps_grace}: OK")
    except PlanGuardException as e:
        print(f"Runtime enforcement for {user_id_grace} with {deps_grace}: BLOCKED - {e.message}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
