# backend/core/plan_guard.py

from fastapi import Request, Response, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from database import get_db # Import get_db
from sqlalchemy.orm import Session # Import Session

# Define a custom error code for PlanGuard blocks
PLAN_GUARD_BLOCK = "PLAN_GUARD_BLOCK"

class PlanGuardMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Get the plan_guard instance from the app state
        plan_guard = request.app.state.plan_guard

        # Define paths to intercept for widget-related actions
        widget_install_path = "/api/widgets/install"
        widget_update_path = "/api/widgets/update"
        module_execute_path = "/api/execute-module"

        # Check if the request path is one of the intercepted paths
        if request.url.path == widget_install_path or \
           request.url.path == widget_update_path or \
           request.url.path == module_execute_path:
            
            user_id = request.state.get("user_id") # Assuming user_id is set by auth middleware
            if not user_id:
                raise HTTPException(status_code=401, detail="Unauthorized: User ID not found.")

            # Get a database session for this request
            db: Session = next(get_db()) # Use next() to get the session from the generator

            try:
                # Read the request body to get widget/module details
                body = await request.json()
                dependencies = []
                action_type = ""

                if request.url.path == widget_install_path:
                    widget_name = body.get("widget_name")
                    dependencies = body.get("dependencies", [])
                    action_type = "widget_install"
                    # Validate against plan and dependencies, passing the db session
                    await validate_plan_and_dependencies(plan_guard, user_id, dependencies, action_type, widget_name, db)
                elif request.url.path == widget_update_path:
                    widget_name = body.get("widget_name")
                    dependencies = body.get("new_dependencies", [])
                    action_type = "widget_update"
                    # Validate against plan and dependencies, passing the db session
                    await validate_plan_and_dependencies(plan_guard, user_id, dependencies, action_type, widget_name, db)
                elif request.url.path == module_execute_path:
                    module_name = body.get("module_name")
                    action_type = "module_execute"
                    # For module execution, we might check module-specific permissions or dependencies
                    # For now, we'll use a placeholder check, passing the db session
                    await plan_guard.check_action_permission(user_id, f"execute_{module_name}", db)

            except HTTPException as e:
                raise e # Re-raise HTTPExceptions from validation
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail={"code": "INVALID_REQUEST_BODY", "message": f"Invalid request body for PlanGuard check: {e}"}
                )
            finally:
                db.close() # Ensure the session is closed

        response = await call_next(request)
        return response

# Helper function for PlanGuard validation (to be expanded)
async def validate_plan_and_dependencies(plan_guard_instance, user_id: str, dependencies: list[str], action_type: str, item_name: str = "", db: Session = None) -> dict:
    # This function will now use the passed plan_guard_instance
    print(f"Validating {action_type} for user {user_id}, item: {item_name}, dependencies: {dependencies}")
    
    try:
        # Check general action permission first
        await plan_guard_instance.check_action_permission(user_id, action_type, db)

        # Then check each dependency against the user's plan
        for dep in dependencies:
            # Assuming plan_guard_instance has a method to check dependency access
            # This might be a more granular check than check_action_permission
            await plan_guard_instance.check_dependency_access(user_id, dep, db)
        
        return {"allowed": True, "message": "Validation successful."}
    except PlanGuardException as e:
        raise HTTPException(
            status_code=403,
            detail={
                "code": PLAN_GUARD_BLOCK,
                "message": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "PLAN_GUARD_ERROR",
                "message": f"An unexpected error occurred during PlanGuard validation: {e}"
            }
        )
