from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Plan:
    name: str
    max_requests_per_day: int
    features_enabled: List[str]
    cost_per_month: float

@dataclass
class UserSubscription:
    user_id: str
    plan_name: str
    start_date: datetime
    end_date: datetime
    is_active: bool = True

# // [TASK]: Implement SLA tracking and billing reconciliation models
# // [GOAL]: Provide enterprise SLAs, automated billing reconciliation, and analytics
# // [ELITE_CURSOR_SNIPPET]: aihandle

@dataclass
class SLARecord:
    tenant_id: str
    month: str # YYYY-MM
    uptime_percentage: float
    response_time_slo_met: bool
    credits_due: float = 0.0

@dataclass
class BillingTransaction:
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    timestamp: datetime
    provider: str # e.g., Stripe, Mpesa

@dataclass
class UsageRecord:
    user_id: str
    feature: str
    count: int
    timestamp: datetime

@dataclass
class ReconciliationReport:
    month: str # YYYY-MM
    total_billed: float
    total_usage_cost: float
    mismatches: List[str]
    tickets_created: List[str]

# --- Mock Data / Placeholder Functions ---

def get_default_plans() -> List[Plan]:
    """
    // [TASK]: Define default subscription plans
    // [GOAL]: Provide a set of predefined plans for the system
    """
    return [
        Plan(
            name="Free",
            max_requests_per_day=5,
            features_enabled=["text_gen", "image_gen", "tts", "stt"],
            cost_per_month=0.0
        ),
        Plan(
            name="Pro",
            max_requests_per_day=100,
            features_enabled=["text_gen", "image_gen", "tts", "stt", "youtube_upload"],
            cost_per_month=19.99
        ),
        Plan(
            name="Enterprise",
            max_requests_per_day=1000,
            features_enabled=["text_gen", "image_gen", "tts", "stt", "youtube_upload", "analytics", "crm_integration"],
            cost_per_month=99.99
        ),
    ]

def get_user_subscription(user_id: str) -> UserSubscription:
    """
    // [TASK]: Retrieve a user's subscription details
    // [GOAL]: Simulate fetching subscription from a database
    """
    # This is a placeholder. In a real system, this would query a database.
    if user_id == "test_free_user":
        return UserSubscription(
            user_id=user_id,
            plan_name="Free",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2024, 1, 1)
        )
    elif user_id == "test_pro_user":
        return UserSubscription(
            user_id=user_id,
            plan_name="Pro",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2024, 1, 1)
        )
    else:
        # Default to Free for unknown users
        return UserSubscription(
            user_id=user_id,
            plan_name="Free",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2024, 1, 1)
        )
