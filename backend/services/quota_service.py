import redis.asyncio as redis
from datetime import datetime
from typing import Optional, Dict, Any
from logging_setup import get_logger
from config_loader import get_config
from sqlalchemy.orm import Session
import sqlalchemy
from backend.ai.models import UsageCost # Import UsageCost model

logger = get_logger(__name__)
config = get_config()

class _NoopPipeline:
    async def zadd(self, *args, **kwargs):
        return 0
    async def zcard(self, *args, **kwargs):
        return 0
    async def expire(self, *args, **kwargs):
        return True
    async def execute(self):
        # Return two zeros for zcard results at the end
        return [None, None, None, None, 0, 0]

class _NoopAsyncRedis:
    async def incrby(self, *args, **kwargs):
        return 0
    async def expire(self, *args, **kwargs):
        return True
    async def zremrangebyscore(self, *args, **kwargs):
        return 0
    def pipeline(self):
        return _NoopPipeline()
    async def set(self, *args, **kwargs):
        return True
    async def delete(self, *args, **kwargs):
        return 1
    async def decrby(self, *args, **kwargs):
        return 0

class QuotaService:
    def __init__(self):
        # Initialize Redis client safely; fall back to Noop to avoid crashing the server
        try:
            url = getattr(config, 'redis', None) and getattr(config.redis, 'url', None)
            if not url or not isinstance(url, str) or '://' not in url:
                raise ValueError("Invalid or missing Redis URL in config. Expected scheme like redis://localhost:6379/0")
            self.redis_client = redis.from_url(url, decode_responses=True)
        except Exception as e:
            logger.warning(f"Redis disabled: {e}. Falling back to Noop client; rate limits/quotas won't be enforced.")
            self.redis_client = _NoopAsyncRedis()

    async def _get_monthly_key(self, user_id: str, metric: str) -> str:
        now = datetime.utcnow()
        return f"usage:{user_id}:{now.year}-{now.month}:{metric}"

    async def _get_rate_limit_key(self, user_id: str, window_name: str) -> str:
        return f"rl:{user_id}:{window_name}"

    async def check_and_increment_quota(self, user_id: str, metric: str, amount: int, monthly_limit: int) -> bool:
        key = await self._get_monthly_key(user_id, metric)
        current_usage = await self.redis_client.incrby(key, amount)
        
        # Set expiration for the key to the end of the current month
        # This is a simplified approach; a more robust solution would calculate exact seconds to month end
        # For now, we'll set it to 31 days (approx. a month)
        await self.redis_client.expire(key, 31 * 24 * 3600) 

        if current_usage > monthly_limit:
            logger.warning(f"Quota exceeded for user {user_id}, metric {metric}. Limit: {monthly_limit}, Current: {current_usage}")
            return False
        return True

    async def check_rate_limit(self, user_id: str, rpm_limit: int, rps_limit: int, burst_limit: int) -> bool:
        # Simplified sliding window rate limiting
        now = datetime.utcnow().timestamp()
        minute_key = await self._get_rate_limit_key(user_id, "minute")
        second_key = await self._get_rate_limit_key(user_id, "second")

        # Clean up old entries and count current requests
        await self.redis_client.zremrangebyscore(minute_key, 0, now - 60) # Remove entries older than 60 seconds
        await self.redis_client.zremrangebyscore(second_key, 0, now - 1) # Remove entries older than 1 second

        pipe = self.redis_client.pipeline()
        pipe.zadd(minute_key, {now: now})
        pipe.zadd(second_key, {now: now})
        pipe.zcard(minute_key)
        pipe.zcard(second_key)
        pipe.expire(minute_key, 60) # Expire after 60 seconds
        pipe.expire(second_key, 1) # Expire after 1 second
        results = await pipe.execute()

        current_minute_requests = results[-2] # Result of zcard(minute_key)
        current_second_requests = results[-1] # Result of zcard(second_key)

        if current_minute_requests > rpm_limit or current_second_requests > rps_limit:
            logger.warning(f"Rate limit exceeded for user {user_id}. RPM: {current_minute_requests}/{rpm_limit}, RPS: {current_second_requests}/{rps_limit}")
            return False
        
        # Burst limit check (simplified: check if current requests are within burst capacity)
        # This is a very basic burst check. A token bucket or leaky bucket would be more robust.
        if current_minute_requests > burst_limit: # Using minute count for burst as a simple proxy
             logger.warning(f"Burst limit exceeded for user {user_id}. Current: {current_minute_requests}, Burst: {burst_limit}")
             return False

        return True

    async def record_provisional_usage(self, user_id: str, job_id: str, metric: str, amount: int):
        # Record usage that is pending job completion
        key = f"provisional:{user_id}:{job_id}:{metric}"
        await self.redis_client.set(key, amount, ex=3600) # Provisional usage expires in 1 hour
        logger.info(f"Provisional usage recorded for job {job_id}: {metric} {amount}")

    async def finalize_usage(self, user_id: str, job_id: str, metric: str, amount: int):
        # Finalize usage and remove provisional record
        provisional_key = f"provisional:{user_id}:{job_id}:{metric}"
        await self.redis_client.delete(provisional_key)
        logger.info(f"Finalized usage for job {job_id}: {metric} {amount}")

    async def rollback_usage(self, user_id: str, job_id: str, metric: str, amount: int):
        # Rollback usage if job failed
        provisional_key = f"provisional:{user_id}:{job_id}:{metric}"
        await self.redis_client.delete(provisional_key) # Remove provisional record
        
        # Decrement actual usage if it was already incremented (e.g., for monthly quotas)
        # This assumes check_and_increment_quota increments immediately. If it only records provisional,
        # then this decrement might not be needed.
        monthly_key = await self._get_monthly_key(user_id, metric)
        await self.redis_client.decrby(monthly_key, amount)
        logger.warning(f"Rolled back usage for job {job_id}: {metric} {amount}")

quota_service = QuotaService()

async def get_user_monthly_cost(user_id: str, db: Session) -> float:
    """
    Calculates the estimated total cost for the current month for a given user.
    """
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)

    total_cost = (
        db.query(sqlalchemy.func.sum(UsageCost.estimated_cost_usd))
          .filter(UsageCost.user_id == user_id)
          .filter(UsageCost.timestamp >= start_of_month)
          .scalar()
    )
    
    return total_cost if total_cost is not None else 0.0

