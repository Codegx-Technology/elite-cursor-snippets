import redis
from logging_setup import get_logger
from config_loader import get_config

logger = get_logger(__name__)
config = get_config()

class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._client = cls._instance._connect()
        return cls._instance

    def _connect(self):
        try:
            # Assuming Redis is running on localhost:6379 by default
            # Can be configured via config.yaml later
            client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            client.ping()
            logger.info("✅ Connected to Redis.")
            return client
        except redis.exceptions.ConnectionError as e:
            logger.error(f"❌ Could not connect to Redis: {e}")
            return None

    def get_client(self):
        return self._client

    def increment_counter(self, user_id: str, feature_name: str, expiry_seconds: int = 86400): # 24 hours
        """
        // [TASK]: Increment a counter for a user and feature
        // [GOAL]: Track usage for billing limits
        """
        if not self._client:
            logger.warning("Redis client not available. Cannot increment counter.")
            return
        
        key = f"user:{user_id}:feature:{feature_name}"
        try:
            count = self._client.incr(key)
            if count == 1: # Set expiry only on first increment
                self._client.expire(key, expiry_seconds)
            logger.debug(f"Incremented {key} to {count}")
            return count
        except Exception as e:
            logger.error(f"Failed to increment Redis counter {key}: {e}")
            return None

    def get_counter(self, user_id: str, feature_name: str):
        """
        // [TASK]: Get the current value of a counter
        // [GOAL]: Retrieve usage for billing limits
        """
        if not self._client:
            logger.warning("Redis client not available. Cannot get counter.")
            return 0

        key = f"user:{user_id}:feature:{feature_name}"
        try:
            count = self._client.get(key)
            return int(count) if count else 0
        except Exception as e:
            logger.error(f"Failed to get Redis counter {key}: {e}")
            return 0

# Singleton instance
redis_client = RedisClient()
