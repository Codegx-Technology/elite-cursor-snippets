import yaml
import os
from dotmap import DotMap # For easy access to nested dicts
import boto3 # Elite Cursor Snippet: boto3_import
from botocore.exceptions import ClientError # Elite Cursor Snippet: botocore_exception_import
import logging

# Use standard logging here to avoid circular import with logging_setup
logger = logging.getLogger(__name__)

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

    def _get_secret_from_secrets_manager(self, secret_type: str, secret_path: str, **kwargs) -> str:
        """
        // [TASK]: Dispatch secret retrieval to appropriate secrets manager
        // [GOAL]: Provide a unified interface for fetching secrets from various sources
        // [ELITE_CURSOR_SNIPPET]: securitycheck
        """
        if secret_type == "aws_secrets_manager":
            region_name = kwargs.get("region_name", os.environ.get("AWS_REGION", "us-east-1"))
            return self._get_secret_from_aws_secrets_manager(secret_path, region_name)
        elif secret_type == "hashicorp_vault":
            logger.warning("HashiCorp Vault integration is conceptual. Implement actual Vault client here.")
            # Example: return vault_client.read(secret_path)['data']['value']
            raise NotImplementedError(f"HashiCorp Vault integration not implemented for {secret_path}")
        elif secret_type == "kubernetes_secret":
            logger.warning("Kubernetes Secret integration is conceptual. Implement actual K8s client here.")
            # Example: return k8s_client.read_secret(secret_path)
            raise NotImplementedError(f"Kubernetes Secret integration not implemented for {secret_path}")
        else:
            raise ValueError(f"Unsupported secret type: {secret_type}")

    def _process_config(self, config_map, prefix="SHUJAA_"):
        for key, value in config_map.items():
            env_var_name = f"{prefix}{key.upper()}"
            if isinstance(value, DotMap):
                self._process_config(value, f"{env_var_name}_")
            elif isinstance(value, str) and value.startswith("secret:"):
                # Handle generic secret values like secret:aws_secrets_manager:my/secret/name
                try:
                    parts = value.split(":")
                    if len(parts) < 3:
                        raise ValueError("Invalid secret format. Expected 'secret:<type>:<path>'")
                    secret_type = parts[1]
                    secret_path = ":".join(parts[2:]) # Rejoin path in case it contains colons
                    config_map[key] = self._get_secret_from_secrets_manager(secret_type, secret_path)
                    logger.info(f"Successfully loaded secret for {key} from {secret_type}.")
                except Exception as e:
                    logger.warning(f"Failed to load secret for {key} from secrets manager: {e}. Falling back to environment variable.")
                    config_map[key] = os.environ.get(env_var_name, "") # Fallback to env var
            elif isinstance(value, str) and value.startswith("${{") and value.endswith("}"):
                # Handle sensitive values like ${HF_TOKEN}
                env_key = value[2:-1] # Extract HF_TOKEN from ${HF_TOKEN}
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
