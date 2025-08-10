import os
import requests
from huggingface_hub import HfApi
from logging_setup import get_logger

logger = get_logger(__name__)

def validate_hf_model_access(model_id: str, token: str) -> bool:
    """
    // [TASK]: Validate access to a specific Hugging Face model
    // [GOAL]: Ensure the provided token has access to the model
    """
    if not token:
        logger.warning(f"No HF token provided for model access validation of {model_id}.")
        return False

    api = HfApi(token=token)
    try:
        # This checks if the model exists and if the token has access
        api.model_info(model_id, token=token)
        logger.info(f"✅ Successfully validated access to Hugging Face model: {model_id}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to validate access to Hugging Face model {model_id}: {e}")
        return False

def get_hf_model_info(model_id: str, token: str) -> dict:
    """
    // [TASK]: Get detailed information about a Hugging Face model
    // [GOAL]: Retrieve model details like license, tags, etc.
    """
    if not token:
        logger.warning(f"No HF token provided for model info of {model_id}.")
        return {}

    api = HfApi(token=token)
    try:
        info = api.model_info(model_id, token=token)
        logger.info(f"✅ Successfully retrieved info for Hugging Face model: {model_id}")
        return info.cardData # Or other relevant attributes
    except Exception as e:
        logger.error(f"❌ Failed to retrieve info for Hugging Face model {model_id}: {e}")
        return {}
