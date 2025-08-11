from config_loader import get_config
from logging_setup import get_logger
from functools import lru_cache

logger = get_logger(__name__)
config = get_config()

class FeatureFlagManager:
    def __init__(self):
        self._flags = config.get("feature_flags", {})
        logger.info(f"FeatureFlagManager initialized with flags: {self._flags}")

    @lru_cache(maxsize=128)
    def is_enabled(self, flag_name: str, user_id: str = None, tenant_id: str = None) -> bool:
        """
        Checks if a feature flag is enabled.
        // [TASK]: Check if a feature flag is enabled
        // [GOAL]: Control feature rollout based on configuration
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        flag_config = self._flags.get(flag_name)
        if flag_config is None:
            logger.warning(f"Feature flag '{flag_name}' not found. Defaulting to disabled.")
            return False

        enabled = flag_config.get("enabled", False)
        
        # Check for rollout percentage
        rollout_percentage = flag_config.get("rollout_percentage")
        if rollout_percentage is not None:
            if user_id:
                # Simple hash-based rollout for user_id
                import hashlib
                hash_value = int(hashlib.sha256(user_id.encode()).hexdigest(), 16) % 100
                if hash_value >= rollout_percentage:
                    enabled = False # User is not in the rollout group
            else:
                logger.warning(f"Feature flag '{flag_name}' has rollout_percentage but no user_id provided. Rollout not applied.")

        # Check for specific users/tenants
        if user_id and flag_config.get("users"):
            if user_id not in flag_config["users"]:
                enabled = False
        if tenant_id and flag_config.get("tenants"):
            if tenant_id not in flag_config["tenants"]:
                enabled = False

        logger.debug(f"Feature flag '{flag_name}' is_enabled: {enabled} for user {user_id}, tenant {tenant_id}")
        return enabled

# Initialize the manager
feature_flag_manager = FeatureFlagManager()

# Example usage (for testing)
if __name__ == "__main__":
    # Mock config for testing
    class MockFeatureFlagsConfig:
        feature_flags = {
            "new_ui": {"enabled": True, "rollout_percentage": 50},
            "beta_feature": {"enabled": False, "users": ["user123"]},
            "enterprise_dashboard": {"enabled": True, "tenants": ["enterprise_corp"]},
            "disabled_feature": {"enabled": False}
        }
    class MockConfig:
        def get(self, key, default=None):
            if key == "feature_flags":
                return MockFeatureFlagsConfig.feature_flags
            return default
    
    # Temporarily override global config for testing
    original_config = config
    config = MockConfig()

    print(f"New UI enabled for user_a (rollout 50%): {feature_flag_manager.is_enabled('new_ui', user_id='user_a')}")
    print(f"New UI enabled for user_b (rollout 50%): {feature_flag_manager.is_enabled('new_ui', user_id='user_b')}")
    print(f"Beta feature enabled for user123: {feature_flag_manager.is_enabled('beta_feature', user_id='user123')}")
    print(f"Beta feature enabled for user456: {feature_flag_manager.is_enabled('beta_feature', user_id='user456')}")
    print(f"Enterprise dashboard for enterprise_corp: {feature_flag_manager.is_enabled('enterprise_dashboard', tenant_id='enterprise_corp')}")
    print(f"Enterprise dashboard for small_biz: {feature_flag_manager.is_enabled('enterprise_dashboard', tenant_id='small_biz')}")
    print(f"Disabled feature: {feature_flag_manager.is_enabled('disabled_feature')}")

    # Restore original config
    config = original_config