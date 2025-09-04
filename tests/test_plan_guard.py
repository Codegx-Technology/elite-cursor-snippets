import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from backend.core.plan_guard import PlanGuardMiddleware, PLAN_GUARD_BLOCK
from billing.plan_guard import PlanGuard, PlanGuardException # Assuming this is the real PlanGuard

# Mock PlanGuard for testing
class MockPlanGuard(PlanGuard):
    def __init__(self):
        # Initialize with default allowed state
        self._allowed_actions = {}
        self._allowed_dependencies = {}
        self._user_plan_state = "healthy"

    async def check_action_permission(self, user_id: str, action: str):
        if not self._allowed_actions.get(action, True):
            raise PlanGuardException(f"Action '{action}' not allowed by plan.")
        if self._user_plan_state == "view_only" or self._user_plan_state == "locked":
            raise PlanGuardException(f"Plan is in {self._user_plan_state} mode.")

    async def check_dependency_access(self, user_id: str, dependency: str):
        if not self._allowed_dependencies.get(dependency, True):
            raise PlanGuardException(f"Dependency '{dependency}' not allowed by plan.")
        if self._user_plan_state == "view_only" or self._user_plan_state == "locked":
            raise PlanGuardException(f"Plan is in {self._user_plan_state} mode.")

    def set_action_permission(self, action: str, allowed: bool):
        self._allowed_actions[action] = allowed

    def set_dependency_access(self, dependency: str, allowed: bool):
        self._allowed_dependencies[dependency] = allowed

    def set_user_plan_state(self, state: str):
        self._user_plan_state = state


@pytest.fixture
def mock_plan_guard():
    return MockPlanGuard()

@pytest.fixture
def app_with_plan_guard_middleware(mock_plan_guard):
    app = FastAPI()
    app.state.plan_guard = mock_plan_guard # Store mock PlanGuard in app state

    app.add_middleware(PlanGuardMiddleware)

    @app.post("/api/widgets/install")
    async def install_widget(widget_name: str, dependencies: list[str]):
        return {"message": f"Widget {widget_name} installed."}

    @app.post("/api/widgets/update")
    async def update_widget(widget_name: str, new_dependencies: list[str]):
        return {"message": f"Widget {widget_name} updated."}

    @app.post("/api/execute-module")
    async def execute_module(module_name: str):
        return {"message": f"Module {module_name} executed."}

    @app.get("/test-endpoint")
    async def test_endpoint():
        return {"message": "Test endpoint accessed."}

    return app

@pytest.fixture
def client(app_with_plan_guard_middleware):
    return TestClient(app_with_plan_guard_middleware)


def test_widget_install_allowed(client, mock_plan_guard):
    mock_plan_guard.set_user_plan_state("healthy")
    mock_plan_guard.set_action_permission("widget_install", True)
    mock_plan_guard.set_dependency_access("core_ai", True)

    response = client.post(
        "/api/widgets/install",
        headers={
            "Content-Type": "application/json",
            "X-User-Id": "test_user_1" # Simulate user_id from auth middleware
        },
        json={
            "widget_name": "TestWidget",
            "dependencies": ["core_ai"]
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Widget TestWidget installed."}


def test_widget_install_blocked_by_plan_state(client, mock_plan_guard):
    mock_plan_guard.set_user_plan_state("view_only")
    mock_plan_guard.set_action_permission("widget_install", True)
    mock_plan_guard.set_dependency_access("core_ai", True)

    response = client.post(
        "/api/widgets/install",
        headers={
            "Content-Type": "application/json",
            "X-User-Id": "test_user_1"
        },
        json={
            "widget_name": "TestWidget",
            "dependencies": ["core_ai"]
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == PLAN_GUARD_BLOCK
    assert "view_only" in response.json()["detail"]["message"]


def test_widget_install_blocked_by_dependency(client, mock_plan_guard):
    mock_plan_guard.set_user_plan_state("healthy")
    mock_plan_guard.set_action_permission("widget_install", True)
    mock_plan_guard.set_dependency_access("premium_feature", False) # Block this dependency

    response = client.post(
        "/api/widgets/install",
        headers={
            "Content-Type": "application/json",
            "X-User-Id": "test_user_1"
        },
        json={
            "widget_name": "PremiumWidget",
            "dependencies": ["premium_feature"]
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == PLAN_GUARD_BLOCK
    assert "premium_feature" in response.json()["detail"]["message"]


def test_module_execute_allowed(client, mock_plan_guard):
    mock_plan_guard.set_user_plan_state("healthy")
    mock_plan_guard.set_action_permission("execute_some_module", True)

    response = client.post(
        "/api/execute-module",
        headers={
            "Content-Type": "application/json",
            "X-User-Id": "test_user_1"
        },
        json={
            "module_name": "some_module"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Module some_module executed."}


def test_module_execute_blocked_by_action_permission(client, mock_plan_guard):
    mock_plan_guard.set_user_plan_state("healthy")
    mock_plan_guard.set_action_permission("execute_some_module", False) # Block this action

    response = client.post(
        "/api/execute-module",
        headers={
            "Content-Type": "application/json",
            "X-User-Id": "test_user_1"
        },
        json={
            "module_name": "some_module"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == PLAN_GUARD_BLOCK
    assert "execute_some_module" in response.json()["detail"]["message"]


def test_non_intercepted_endpoint_allowed(client, mock_plan_guard):
    mock_plan_guard.set_user_plan_state("view_only") # Should not affect this endpoint
    response = client.get("/test-endpoint")
    assert response.status_code == 200
    assert response.json() == {"message": "Test endpoint accessed."}
