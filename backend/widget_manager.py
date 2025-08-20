from typing import List, Dict, Any
import logging

from billing.plan_guard import PlanGuard, PlanGuardException
from backend.core.dependencies_enforcer import DependencyEnforcer

logger = logging.getLogger(__name__)

class WidgetManager:
    def __init__(self, plan_guard: PlanGuard):
        self.dependency_enforcer = DependencyEnforcer(plan_guard)
        self.installed_widgets: Dict[str, Dict[str, Any]] = {} # Conceptual storage for installed widgets

    async def install_widget(self, user_id: str, widget_name: str, widget_version: str, dependencies: List[str]) -> Dict[str, Any]:
        """
        Simulates installing a widget, enforcing PlanGuard rules for dependencies.
        """
        logger.info(f"Attempting to install widget '{widget_name}' for user {user_id}...")
        try:
            await self.dependency_enforcer.enforce_runtime(user_id, widget_name, dependencies)
            
            # Simulate installation process
            self.installed_widgets[widget_name] = {"version": widget_version, "dependencies": dependencies}
            logger.info(f"Widget '{widget_name}' installed successfully for user {user_id}.")
            return {"status": "success", "message": f"Widget '{widget_name}' installed."}
        except PlanGuardException as e:
            logger.warn(f"Widget install blocked for user {user_id}: {e.message}")
            return {"status": "error", "message": e.message, "code": 403}
        except Exception as e:
            logger.error(f"Unexpected error during widget install for user {user_id}: {e}")
            return {"status": "error", "message": "Internal server error during install."}

    async def update_widget(self, user_id: str, widget_name: str, new_widget_version: str, new_dependencies: List[str]) -> Dict[str, Any]:
        """
        Simulates updating a widget, enforcing PlanGuard rules for new dependencies.
        """
        logger.info(f"Attempting to update widget '{widget_name}' for user {user_id}...")
        try:
            await self.dependency_enforcer.enforce_runtime(user_id, widget_name, new_dependencies)
            
            # Simulate update process
            self.installed_widgets[widget_name] = {"version": new_widget_version, "dependencies": new_dependencies}
            logger.info(f"Widget '{widget_name}' updated successfully for user {user_id}.")
            return {"status": "success", "message": f"Widget '{widget_name}' updated."}
        except PlanGuardException as e:
            logger.warn(f"Widget update blocked for user {user_id}: {e.message}")
            return {"status": "error", "message": e.message, "code": 403}
        except Exception as e:
            logger.error(f"Unexpected error during widget update for user {user_id}: {e}")
            return {"status": "error", "message": "Internal server error during update."}

    async def load_widget(self, user_id: str, widget_name: str) -> Dict[str, Any]:
        """
        Simulates loading a widget at runtime, enforcing PlanGuard rules for its dependencies.
        """
        logger.info(f"Attempting to load widget '{widget_name}' for user {user_id}...")
        if widget_name not in self.installed_widgets:
            return {"status": "error", "message": f"Widget '{widget_name}' not installed.", "code": 404}

        dependencies = self.installed_widgets[widget_name]["dependencies"]
        try:
            await self.dependency_enforcer.enforce_runtime(user_id, widget_name, dependencies)
            
            logger.info(f"Widget '{widget_name}' loaded successfully for user {user_id}.")
            return {"status": "success", "message": f"Widget '{widget_name}' loaded."}
        except PlanGuardException as e:
            logger.warn(f"Widget load blocked for user {user_id}: {e.message}")
            return {"status": "error", "message": e.message, "code": 403}
        except Exception as e:
            logger.error(f"Unexpected error during widget load for user {user_id}: {e}")
            return {"status": "error", "message": "Internal server error during load."}

# Example usage (for testing purposes)
async def main():
    from billing.plan_guard import PlanGuard
    plan_guard_instance = PlanGuard()
    widget_manager = WidgetManager(plan_guard_instance)

    user_id_pro = "test_pro_user"
    user_id_free = "test_free_user"

    print("\n--- Testing Widget Installation ---")
    # Pro user installs widget with allowed dependencies
    result = await widget_manager.install_widget(user_id_pro, "pro_widget", "1.0", ["gpt-4o", "analytics"])
    print(f"Pro user install: {result}")

    # Free user installs widget with premium dependencies
    result = await widget_manager.install_widget(user_id_free, "premium_widget", "1.0", ["gpt-5", "enterprise_features"])
    print(f"Free user install (premium deps): {result}")

    print("\n--- Testing Widget Loading ---")
    # Pro user loads installed widget
    result = await widget_manager.load_widget(user_id_pro, "pro_widget")
    print(f"Pro user load: {result}")

    # Free user tries to load premium widget (should be blocked at install, but testing runtime enforcement)
    widget_manager.installed_widgets["premium_widget"] = {"version": "1.0", "dependencies": ["gpt-5", "enterprise_features"]}
    result = await widget_manager.load_widget(user_id_free, "premium_widget")
    print(f"Free user load (premium deps): {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
