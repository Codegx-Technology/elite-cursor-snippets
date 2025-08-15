# // [TASK]: Create unit tests for config_loader.py
# // [GOAL]: Ensure robust configuration loading and secret management
# // [ELITE_CURSOR_SNIPPET]: writetest

import os
import pytest
import yaml
from unittest.mock import patch, MagicMock
from config_loader import get_config, ConfigLoader

# Test get_config loads YAML
def test_get_config_loads_yaml(tmp_path, monkeypatch):
    config_content = """
    app:
      name: TestApp
      version: 1.0.0
    auth:
      access_token_expire_minutes: 30
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    monkeypatch.chdir(tmp_path) # Change current working directory for the test

    config = get_config()
    assert config.app.name == "TestApp"
    assert config.app.version == "1.0.0"
    assert config.auth.access_token_expire_minutes == 30

# Test environment variable override
def test_env_var_override(tmp_path, monkeypatch):
    config_content = """
    app:
      name: OriginalApp
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SHUJAA_APP_NAME", "OverriddenApp")

    config = get_config()
    assert config.app.name == "OverriddenApp"

# Test AWS Secrets Manager integration (mocked)
@patch('config_loader.boto3.session.Session')
def test_aws_secrets_manager_integration(mock_session, tmp_path, monkeypatch):
    config_content = """
    api_keys:
      some_key: aws_secret:my/test/secret
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    monkeypatch.chdir(tmp_path)

    # Mock AWS Secrets Manager client
    mock_client = MagicMock()
    mock_client.get_secret_value.return_value = {'SecretString': 'my_secret_value'}
    mock_session.return_value.client.return_value = mock_client

    config = get_config()
    assert config.api_keys.some_key == "my_secret_value"
    mock_client.get_secret_value.assert_called_once_with(SecretId='my/test/secret')

# Test sensitive value placeholder
def test_sensitive_value_placeholder(tmp_path, monkeypatch):
    config_content = """
    secrets:
      hf_token: ${HF_TOKEN}
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HF_TOKEN", "hf_12345")

    config = get_config()
    assert config.secrets.hf_token == "hf_12345"

# Test sensitive value placeholder not found
def test_sensitive_value_placeholder_not_found(tmp_path, monkeypatch, caplog):
    config_content = """
    secrets:
      hf_token: ${NON_EXISTENT_KEY}
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    monkeypatch.chdir(tmp_path)
    
    # Ensure the environment variable is not set
    if "NON_EXISTENT_KEY" in os.environ:
        monkeypatch.delenv("NON_EXISTENT_KEY")

    with caplog.at_level(os.environ.get("LOG_LEVEL", "INFO")):
        config = get_config()
        assert config.secrets.hf_token == ""
        assert "Environment variable NON_EXISTENT_KEY not found for hf_token" in caplog.text

# Test ConfigLoader is a singleton
def test_config_loader_is_singleton(tmp_path, monkeypatch):
    config_content = "app: {name: SingletonTest}"
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    monkeypatch.chdir(tmp_path)

    loader1 = ConfigLoader()
    loader2 = ConfigLoader()
    assert loader1 is loader2
    assert loader1.get_config().app.name == "SingletonTest"

    # Ensure subsequent calls don't reload config if already loaded
    config_file.write_text("app: {name: ChangedTest}") # Change file content
    loader3 = ConfigLoader()
    assert loader3.get_config().app.name == "SingletonTest" # Should still be original
