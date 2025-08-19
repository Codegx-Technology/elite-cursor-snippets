from dataclasses import dataclass, field
from datetime import datetime
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
    max_requests_per_day: int
    features_enabled: List[str]
    cost_per_month: float
    tier_code: str = "FREE" # 'FREE' | 'PRO' | 'BUSINESS' | 'ENTERPRISE'
    model_policy: ModelPolicy = field(default_factory=ModelPolicy)
    quotas: Quotas = field(default_factory=Quotas)
    priority: str = "low" # 'low' | 'standard' | 'high' | 'critical'
    cost_caps: CostCaps = field(default_factory=CostCaps)
    visibility: Visibility = field(default_factory=Visibility)

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
            cost_per_month=0.0,
            tier_code="FREE",
            quotas=Quotas(monthly=MonthlyQuotas(tokens=1000, audioSecs=60, videoMins=1, jobs=5), concurrency=1, rateLimit=RateLimit(rpm=5, rps=1, burst=2)),
            priority="low",
            cost_caps=CostCaps(monthlyUsd=0.0, hardStop=True),
            visibility=Visibility(showBetaModels=False, allowUnverified=False)
        ),
        Plan(
            name="Pro",
            max_requests_per_day=100,
            features_enabled=["text_gen", "image_gen", "tts", "stt", "youtube_upload"],
            cost_per_month=19.99,
            tier_code="PRO",
            quotas=Quotas(monthly=MonthlyQuotas(tokens=100000, audioSecs=600, videoMins=10, jobs=100), concurrency=5, rateLimit=RateLimit(rpm=100, rps=10, burst=20)),
            priority="standard",
            cost_caps=CostCaps(monthlyUsd=50.0, hardStop=False),
            visibility=Visibility(showBetaModels=False, allowUnverified=False)
        ),
        Plan(
            name="Business",
            max_requests_per_day=500,
            features_enabled=["text_gen", "image_gen", "tts", "stt", "youtube_upload", "analytics", "crm_integration", "priority_support"],
            cost_per_month=99.99,
            tier_code="BUSINESS",
            model_policy=ModelPolicy(defaultRouting="allow_minor", providers={"tts":["elevenlabs","xtts","local"]}),
            quotas=Quotas(monthly=MonthlyQuotas(tokens=500000, audioSecs=3000, videoMins=50, jobs=500), concurrency=20, rateLimit=RateLimit(rpm=500, rps=50, burst=100)),
            priority="high",
            cost_caps=CostCaps(monthlyUsd=500.0, hardStop=False),
            visibility=Visibility(showBetaModels=True, allowUnverified=False)
        ),
        Plan(
            name="Enterprise",
            max_requests_per_day=1000,
            features_enabled=["text_gen", "image_gen", "tts", "stt", "youtube_upload", "analytics", "crm_integration", "priority_support", "dedicated_instance"],
            cost_per_month=999.99,
            tier_code="ENTERPRISE",
            model_policy=ModelPolicy(defaultRouting="pinned", pinned={"tts":PinnedModel(model="xtts-v2",version="a1b2c3d4")}, providers={"tts":["local","elevenlabs","xtts"]}),
            quotas=Quotas(monthly=MonthlyQuotas(tokens=5000000, audioSecs=30000, videoMins=500, jobs=5000), concurrency=100, rateLimit=RateLimit(rpm=5000, rps=500, burst=1000)),
            priority="critical",
            cost_caps=CostCaps(monthlyUsd=5000.0, hardStop=True),
            visibility=Visibility(showBetaModels=True, allowUnverified=True)
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
