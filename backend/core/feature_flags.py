import os
from typing import Any

def get_feature_flag(flag_name: str, default_value: Any) -> Any:
    """
    Retrieves a feature flag value from environment variables.
    Environment variables take precedence over default values.
    """
    env_value = os.getenv(flag_name)
    if env_value is not None:
        if isinstance(default_value, bool):
            return env_value.lower() in ('true', '1', 't', 'y', 'yes')
        elif isinstance(default_value, int):
            try:
                return int(env_value)
            except ValueError:
                return default_value
        else:
            return env_value
    return default_value

# Define feature flags
ENABLE_DEPWATCHER = get_feature_flag("ENABLE_DEPWATCHER", True)
ALLOW_AUTOPATCH = get_feature_flag("ALLOW_AUTOPATCH", False)
PATCH_WINDOW_CRON = get_feature_flag("PATCH_WINDOW_CRON", "0 2 * * SUN") # Default: Sunday 02:00
