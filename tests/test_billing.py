import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Adjust path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from billing_models import Plan, UserSubscription, get_default_plans, get_user_subscription
from billing_middleware import enforce_limits, BillingException

# --- Fixtures for Plans and Subscriptions ---

@pytest.fixture
def mock_default_plans():
    """Mocks get_default_plans to return a consistent set of plans."""
    return [
        Plan(name="Free", max_requests_per_day=5, features_enabled=["text_gen"], cost_per_month=0.0),
        Plan(name="Pro", max_requests_per_day=100, features_enabled=["text_gen", "image_gen"], cost_per_month=19.99),
        Plan(name="Enterprise", max_requests_per_day=1000, features_enabled=["text_gen", "image_gen", "tts", "stt"], cost_per_month=99.99),
    ]

@pytest.fixture
def mock_user_subscriptions():
    """Mocks get_user_subscription to return specific user subscriptions."""
    return {
        "user_free": UserSubscription(user_id="user_free", plan_name="Free", start_date=datetime.now(), end_date=datetime.now() + timedelta(days=30)),
        "user_pro": UserSubscription(user_id="user_pro", plan_name="Pro", start_date=datetime.now(), end_date=datetime.now() + timedelta(days=30)),
        "user_enterprise": UserSubscription(user_id="user_enterprise", plan_name="Enterprise", start_date=datetime.now(), end_date=datetime.now() + timedelta(days=30)),
        "user_unknown": UserSubscription(user_id="user_unknown", plan_name="Unknown", start_date=datetime.now(), end_date=datetime.now() + timedelta(days=30)),
    }

# --- Tests for billing_models.py ---

def test_get_default_plans(mock_default_plans):
    """Test that get_default_plans returns the expected plans."""
    plans = get_default_plans()
    assert len(plans) == 3
    assert any(p.name == "Free" for p in plans)
    assert any(p.name == "Pro" for p in plans)
    assert any(p.name == "Enterprise" for p in plans)

def test_get_user_subscription():
    """Test that get_user_subscription returns the correct mock subscriptions."""
    free_sub = get_user_subscription("test_free_user")
    assert free_sub.plan_name == "Free"

    pro_sub = get_user_subscription("test_pro_user")
    assert pro_sub.plan_name == "Pro"

    unknown_sub = get_user_subscription("some_other_user")
    assert unknown_sub.plan_name == "Free" # Default fallback

# --- Tests for billing_middleware.py ---

@patch('billing_middleware.get_user_subscription')
@patch('billing_middleware.get_default_plans')
@patch('billing_middleware.redis_client') # Assuming redis_client is used for usage tracking
def test_enforce_limits_feature_enabled(mock_redis_client, mock_get_default_plans, mock_get_user_subscription, mock_default_plans, mock_user_subscriptions):
    """Test that enforce_limits allows access when feature is enabled."""
    mock_get_default_plans.return_value = mock_default_plans
    mock_get_user_subscription.return_value = mock_user_subscriptions["user_pro"]
    mock_redis_client.get_counter.return_value = 0 # No usage yet

    # Pro user should be able to use image_gen
    enforce_limits(user_id="user_pro", feature_name="image_gen")
    # No exception means success

@patch('billing_middleware.get_user_subscription')
@patch('billing_middleware.get_default_plans')
@patch('billing_middleware.redis_client')
def test_enforce_limits_feature_not_enabled(mock_redis_client, mock_get_default_plans, mock_get_user_subscription, mock_default_plans, mock_user_subscriptions):
    """Test that enforce_limits raises exception when feature is not enabled."""
    mock_get_default_plans.return_value = mock_default_plans
    mock_get_user_subscription.return_value = mock_user_subscriptions["user_free"]
    mock_redis_client.get_counter.return_value = 0

    # Free user should NOT be able to use image_gen
    with pytest.raises(BillingException, match="Feature 'image_gen' requires plan upgrade."):
        enforce_limits(user_id="user_free", feature_name="image_gen")

@patch('billing_middleware.get_user_subscription')
@patch('billing_middleware.get_default_plans')
@patch('billing_middleware.redis_client')
def test_enforce_limits_daily_limit_exceeded(mock_redis_client, mock_get_default_plans, mock_get_user_subscription, mock_default_plans, mock_user_subscriptions):
    """Test that enforce_limits raises exception when daily limit is exceeded."""
    mock_get_default_plans.return_value = mock_default_plans
    mock_get_user_subscription.return_value = mock_user_subscriptions["user_pro"]
    mock_redis_client.get_counter.return_value = 100 # Pro limit is 100, so 100 is already used

    # Pro user should NOT be able to make another request
    with pytest.raises(BillingException, match="Daily usage limit exceeded."):
        enforce_limits(user_id="user_pro", feature_name="text_gen")

@patch('billing_middleware.get_user_subscription')
@patch('billing_middleware.get_default_plans')
@patch('billing_middleware.redis_client')
def test_enforce_limits_unknown_plan(mock_redis_client, mock_get_default_plans, mock_get_user_subscription, mock_default_plans, mock_user_subscriptions):
    """Test that enforce_limits handles unknown plans gracefully."""
    mock_get_default_plans.return_value = mock_default_plans
    mock_get_user_subscription.return_value = mock_user_subscriptions["user_unknown"]
    mock_redis_client.get_counter.return_value = 0

    with pytest.raises(BillingException, match="Invalid subscription plan."):
        enforce_limits(user_id="user_unknown", feature_name="text_gen")

@patch('billing_middleware.get_user_subscription')
@patch('billing_middleware.get_default_plans')
@patch('billing_middleware.redis_client')
def test_enforce_limits_no_max_requests(mock_redis_client, mock_get_default_plans, mock_get_user_subscription, mock_default_plans, mock_user_subscriptions):
    """Test that enforce_limits works for plans with no max_requests_per_day (e.g., Enterprise)."""
    mock_get_default_plans.return_value = mock_default_plans
    mock_get_user_subscription.return_value = mock_user_subscriptions["user_enterprise"]
    mock_redis_client.get_counter.return_value = 500 # Well within Enterprise limits

    # Enterprise user should be able to use text_gen even with high usage
    enforce_limits(user_id="user_enterprise", feature_name="text_gen")
    # No exception means success