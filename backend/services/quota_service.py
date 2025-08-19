import redis.asyncio as redis
from datetime import datetime
from typing import Optional, Dict, Any
from logging_setup import get_logger
from config_loader import get_config

logger = get_logger(__name__)
config = get_config()

class QuotaService:
    def __init__(self):
        self.redis_client = redis.from_url(config.redis.url, decode_responses=True)

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
