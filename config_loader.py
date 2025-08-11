import yaml
import os
from dotmap import DotMap # For easy access to nested dicts
import boto3 # Elite Cursor Snippet: boto3_import
from botocore.exceptions import ClientError # Elite Cursor Snippet: botocore_exception_import
from logging_setup import get_logger # Elite Cursor Snippet: logger_import

logger = get_logger(__name__)

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

    def _get_secret_from_aws_secrets_manager(self, secret_name: str, region_name: str) -> str:
        # // [TASK]: Fetch secret from AWS Secrets Manager
        # // [GOAL]: Centralize secure secret retrieval
        # // [ELITE_CURSOR_SNIPPET]: securitycheck
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            logger.error(f"Failed to retrieve secret '{secret_name}' from AWS Secrets Manager: {e}")
            raise e
        else:
            if 'SecretString' in get_secret_value_response:
                return get_secret_value_response['SecretString']
            else:
                return get_secret_value_response['SecretBinary'].decode('utf-8')

    def _process_config(self, config_map, prefix="SHUJAA_"):
        for key, value in config_map.items():
            env_var_name = f"{prefix}{key.upper()}"
            if isinstance(value, DotMap):
                self._process_config(value, f"{env_var_name}_")
            elif isinstance(value, str) and value.startswith("aws_secret:"):
                # Handle AWS Secrets Manager values like aws_secret:my/secret/name
                try:
                    secret_path = value.split("aws_secret:")[1]
                    # Assuming region is configured in AWS credentials or environment
                    # For explicit region, you might add it to config.yaml
                    region_name = os.environ.get("AWS_REGION", "us-east-1") # Default region
                    config_map[key] = self._get_secret_from_aws_secrets_manager(secret_path, region_name)
                    logger.info(f"Successfully loaded secret for {key} from AWS Secrets Manager.")
                except Exception as e:
                    logger.warning(f"Failed to load secret for {key} from AWS Secrets Manager: {e}. Falling back to environment variable.")
                    config_map[key] = os.environ.get(env_var_name, "") # Fallback to env var
            elif isinstance(value, str) and value.startswith("${{") and value.endswith("}"):
                # Handle sensitive values like ${HF_API_KEY}
                env_key = value[2:-1] # Extract HF_API_KEY from ${HF_API_KEY}
                if env_key in os.environ:
                    config_map[key] = os.environ[env_key]
                else:
                    logger.warning(f"Environment variable {env_key} not found for {key}. Setting to empty string.")
                    config_map[key] = "" # Set to empty string if not found
            elif env_var_name in os.environ:
                # Override with environment variable
                config_map[key] = os.environ[env_var_name]

    def get_config(self):
        return self._config

def get_config():
    return ConfigLoader().get_config()
