import yaml
import os
from dotmap import DotMap # For easy access to nested dicts

class ConfigLoader:
    _instance = None

    def __new__(cls, config_path="config.yaml"):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._config = cls._instance._load_config(config_path)
        return cls._instance

    def _load_config(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Convert to DotMap for easy access
        config = DotMap(config)

        # Override with environment variables and handle sensitive values
        self._process_config(config)
        
        return config

    def _process_config(self, config_map, prefix="SHUJAA_"):
        for key, value in config_map.items():
            env_var_name = f"{prefix}{key.upper()}"
            if isinstance(value, DotMap):
                self._process_config(value, f"{env_var_name}_")
            elif isinstance(value, str) and value.startswith("${{") and value.endswith("}"):
                # Handle sensitive values like ${HF_API_KEY}
                env_key = value[2:-1] # Extract HF_API_KEY from ${HF_API_KEY}
                if env_key in os.environ:
                    config_map[key] = os.environ[env_key]
                else:
                    print(f"[WARNING] Environment variable {env_key} not found for {key}")
                    config_map[key] = "" # Set to empty string if not found
            elif env_var_name in os.environ:
                # Override with environment variable
                config_map[key] = os.environ[env_var_name]

    def get_config(self):
        return self._config

def get_config():
    return ConfigLoader().get_config()
