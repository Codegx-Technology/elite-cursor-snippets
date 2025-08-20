# backend/core/dependencies_enforcer.py

from typing import List, Dict, Any
from billing.plan_guard import PlanGuard, PlanGuardException
from auth.user_models import User # Assuming User model is accessible

class DependencyEnforcer:
    def __init__(self, plan_guard: PlanGuard):
        self.plan_guard = plan_guard

    async def check_widget_dependencies(self, user_id: str, widget_name: str, dependencies: List[str]) -> None:
        """
        Validates if a user's plan allows for the given widget and its dependencies.
        Raises PlanGuardException if not allowed.
        """
        try:
            # First, check if the user's plan state allows any operation
            # The plan_guard.check_action_permission already handles view_only/locked modes
            await self.plan_guard.check_action_permission(user_id, "widget_operation")

            # Then, check each specific dependency
            for dep in dependencies:
                await self.plan_guard.check_dependency_access(user_id, dep)
            
        except PlanGuardException:
            raise # Re-raise the exception
        except Exception as e:
            raise PlanGuardException(f"An unexpected error occurred during dependency check for widget {widget_name}: {e}")

    async def enforce_runtime_dependencies(self, user_id: str, module_name: str, dependencies: List[str]) -> None:
        """
        Enforces dependencies for a module at runtime. Raises PlanGuardException if not met.
        """
        try:
            # Check general module execution permission
            await self.plan_guard.check_action_permission(user_id, f"execute_{module_name}")

            # Check each specific dependency
            for dep in dependencies:
                await self.plan_guard.check_dependency_access(user_id, dep)
        except PlanGuardException:
            raise # Re-raise the exception
        except Exception as e:
            raise PlanGuardException(f"Runtime dependency enforcement failed for {module_name}: {e}")

    async def check_update_dependencies(self, user_id: str, update_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks dependencies before applying a widget/module update.
        """
        widget_name = update_manifest.get("widget_name")
        new_dependencies = update_manifest.get("dependencies", [])
        
        if not widget_name:
            return {"allowed": False, "message": "Update manifest missing widget_name."}

        return await self.check_widget_dependencies(user_id, widget_name, new_dependencies)

# Global instance (or can be passed via FastAPI dependency injection)
# from database import get_db # Assuming get_db is available
# dependencies_enforcer = DependencyEnforcer(PlanGuard(db_session_factory=get_db))