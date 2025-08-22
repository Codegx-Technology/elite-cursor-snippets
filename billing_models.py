from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

@dataclass
class RateLimit:
    rpm: int = 0
    rps: int = 0
    burst: int = 0

@dataclass
class MonthlyQuotas:
    tokens: int = 0
    audioSecs: int = 0
    videoMins: int = 0
    jobs: int = 0

@dataclass
class Quotas:
    monthly: MonthlyQuotas = field(default_factory=MonthlyQuotas)
    concurrency: int = 0
    rateLimit: RateLimit = field(default_factory=RateLimit)

@dataclass
class PinnedModel:
    model: str
    version: str

@dataclass
class ModelPolicy:
    defaultRouting: str = "latest" # 'latest' | 'pinned' | 'allow_minor'
    pinned: Dict[str, PinnedModel] = field(default_factory=dict) # e.g. "tts": {model:"xtts-v2","version":"a1b2c3d4"}
    providers: Dict[str, List[str]] = field(default_factory=dict) # ordered fallback e.g. "tts": ["elevenlabs","xtts","local"]
    allowed_models: List[str] = field(default_factory=list) # New field
    default_pinned_model: Optional[str] = None # New field
    tts_voices: List[str] = field(default_factory=list) # New field

@dataclass
class CostCaps:
    monthlyUsd: float = 0.0
    hardStop: bool = False

@dataclass
class Visibility:
    showBetaModels: bool = False
    allowUnverified: bool = False

@dataclass
class Plan:
    name: str
    price: float # Renamed from cost_per_month to align with snippet
    max_requests_per_day: int # Keep existing for now, will add max_requests_per_month
    features_enabled: List[str]
    currency: str = "KES" # Added currency with Kenya-first default
    tier_code: str = "FREE" # 'FREE' | 'PRO' | 'BUSINESS' | 'ENTERPRISE'
    model_policy: ModelPolicy = field(default_factory=ModelPolicy)
    quotas: Quotas = field(default_factory=Quotas)
    priority_level: int = 1 # Changed from str to int, with default
    cost_caps: CostCaps = field(default_factory=CostCaps)
    visibility: Visibility = field(default_factory=Visibility)
    max_requests_per_month: int = 0 # New field
    rollback_window_days: Optional[int] = None # New field
    grace_period_hours: int = 0 # New field


@dataclass
class UserSubscription:
    user_id: str
    plan_name: str
    start_date: datetime
    end_date: datetime
    is_active: bool = True
    grace_expires_at: Optional[datetime] = None # New field

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
            name="Starter",
            price=500,
            currency="KES",
            max_requests_per_day=166, # 5000 requests / 30 days (approx)
            features_enabled=["text_gen", "image_gen", "tts", "stt"],
            tier_code="FREE",
            model_policy=ModelPolicy(
                allowed_models=["gpt-4o-mini"],
                default_pinned_model="gpt-4o-mini",
                tts_voices=["xtts-v2"]
            ),
            quotas=Quotas(monthly=MonthlyQuotas(tokens=1000, audioSecs=60, videoMins=1, jobs=5), concurrency=1, rateLimit=RateLimit(rpm=5, rps=1, burst=2)),
            priority_level=1,
            cost_caps=CostCaps(monthlyUsd=0.0, hardStop=True),
            visibility=Visibility(showBetaModels=False, allowUnverified=False),
            max_requests_per_month=5000,
            rollback_window_days=3,
            grace_period_hours=0 # Free users get no grace
        ),
        Plan(
            name="Pro",
            price=2500,
            currency="KES",
            max_requests_per_day=1666, # 50000 requests / 30 days (approx)
            features_enabled=["text_gen", "image_gen", "tts", "stt", "youtube_upload"],
            tier_code="PRO",
            model_policy=ModelPolicy(
                allowed_models=["gpt-4o", "gpt-5"],
                default_pinned_model="gpt-5",
                tts_voices=["xtts-v2", "elevenlabs-pro"]
            ),
            quotas=Quotas(monthly=MonthlyQuotas(tokens=100000, audioSecs=600, videoMins=10, jobs=100), concurrency=5, rateLimit=RateLimit(rpm=100, rps=10, burst=20)),
            priority_level=2,
            cost_caps=CostCaps(monthlyUsd=50.0, hardStop=False),
            visibility=Visibility(showBetaModels=False, allowUnverified=False),
            max_requests_per_month=50000,
            rollback_window_days=7,
            grace_period_hours=24 # Pro users get 24 hours grace
        ),
        Plan(
            name="Enterprise",
            price=15000,
            currency="KES",
            max_requests_per_day=16666, # 500000 requests / 30 days (approx)
            features_enabled=["text_gen", "image_gen", "tts", "stt", "youtube_upload", "analytics", "crm_integration", "priority_support", "dedicated_instance"],
            tier_code="ENTERPRISE",
            model_policy=ModelPolicy(
                defaultRouting="pinned",
                pinned={"tts":PinnedModel(model="xtts-v2",version="a1b2c3d4")},
                providers={"tts":["local","elevenlabs","xtts"]},
                allowed_models=["gpt-5", "gpt-5.5", "custom-finetunes"],
                default_pinned_model="gpt-5.5",
                tts_voices=["xtts-v2", "elevenlabs-pro", "elevenlabs-multi"]
            ),
            quotas=Quotas(monthly=MonthlyQuotas(tokens=5000000, audioSecs=30000, videoMins=500, jobs=5000), concurrency=100, rateLimit=RateLimit(rpm=5000, rps=500, burst=1000)),
            priority_level=5,
            cost_caps=CostCaps(monthlyUsd=5000.0, hardStop=True),
            visibility=Visibility(showBetaModels=True, allowUnverified=True),
            max_requests_per_month=500000,
            rollback_window_days=30,
            grace_period_hours=72 # Enterprise users get 72 hours grace
        ),
    ]

def get_user_subscription(user_id: str) -> UserSubscription:
    """
    // [TASK]: Retrieve a user's subscription details
    // [GOAL]: Simulate fetching subscription from a database
    """
    # This is a placeholder. In a real system, this would query a database.
    # For demonstration, we'll simulate different states for specific user_ids
    if user_id == "test_free_user":
        return UserSubscription(
            user_id=user_id,
            plan_name="Starter",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2024, 1, 1),
            is_active=True
        )
    elif user_id == "test_pro_user":
        return UserSubscription(
            user_id=user_id,
            plan_name="Pro",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2024, 1, 1),
            is_active=True
        )
    elif user_id == "test_enterprise_user":
        return UserSubscription(
            user_id=user_id,
            plan_name="Enterprise",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2024, 1, 1),
            is_active=True
        )
    elif user_id == "test_expired_pro_user":
        # Simulate an expired Pro user who should enter grace mode
        return UserSubscription(
            user_id=user_id,
            plan_name="Pro",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2024, 1, 1) - timedelta(days=1), # Expired yesterday
            is_active=False # Explicitly set to inactive
        )
    else:
        # Default to Starter for unknown users
        default_end_date = datetime(2024, 1, 1) # This date is in the past (Aug 22, 2025)
        # Dynamically determine is_active based on end_date
        default_is_active = datetime.now() < default_end_date

        # If the plan is expired, set grace_expires_at to None initially,
        # PlanGuard will then handle grace period logic.
        default_grace_expires_at = None

        return UserSubscription(
            user_id=user_id,
            plan_name="Starter",
            start_date=datetime(2023, 1, 1),
            end_date=default_end_date,
            is_active=default_is_active, # Now correctly reflects expiration
            grace_expires_at=default_grace_expires_at
        )
