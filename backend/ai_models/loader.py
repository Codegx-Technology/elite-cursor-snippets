import logging
from backend.dependency_watcher.dependency_watcher import DependencyWatcher
from pathlib import Path
from typing import Optional, Dict, Any

from backend.ai_models.model_store import ModelStore

logger = logging.getLogger(__name__)

# Initialize DependencyWatcher (assuming a default config path)
# In a real application, this might be passed or configured differently
dependency_watcher = DependencyWatcher('backend/dependency_watcher/config/dependency_config.yaml')

class ModelNotReady(Exception):
    """Custom exception raised when a model is not ready for use."""
    pass

model_store = ModelStore()

def resolve_model_path(provider: str, model_name: str) -> Path:
    """
    Resolves the active model path using ModelStore, with fallback to legacy paths.
    Raises ModelNotReady if no active or legacy model path is found.
    """
    logger.info(f"Resolving model path for {provider}/{model_name}...")
    
    # 1. Try to get the current active model from ModelStore
    current_active_model = model_store.current(provider, model_name)
    if current_active_model and current_active_model.get("path"):
        model_path = Path(current_active_model["path"])
        if model_path.exists():
            logger.info(f"Found active model path via ModelStore: {model_path}")
            return model_path
        else:
            logger.warning(f"Active model path {model_path} from ModelStore does not exist. Falling back to legacy.")

    # 2. Fallback to legacy path for backward compatibility
    # Assuming legacy models are directly under models/<provider>/<model_name>/legacy
    # This path needs to be consistent with how legacy models might have been stored.
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
    MODELS_BASE_DIR = PROJECT_ROOT / "models"
    legacy_model_path = MODELS_BASE_DIR / provider / model_name / "legacy"
    
    if legacy_model_path.exists():
        logger.info(f"Found legacy model path: {legacy_model_path}")
        return legacy_model_path
    
    # 3. If no active or legacy version, raise ModelNotReady error
    error_message = f"Model {provider}/{model_name} is not ready: no active version found in ModelStore and no legacy path exists."
    logger.error(error_message)
    raise ModelNotReady(error_message)

def load_model(model_name: str):
    """
    Placeholder for actual model loading logic.
    This function might be updated to use resolve_model_path internally.
    """
    logger.info(f"Loading model: {model_name} (simulated)")
    # In a real scenario, this would load the actual model
    # e.g., from Hugging Face, local disk, etc.
    return f"Loaded_{model_name}_Instance"

def safe_model_load(model_name: str):
    """
    Safely loads a model after checking its dependencies.
    Raises RuntimeError if dependencies are not healthy.
    """
    logger.info(f"Attempting safe load for model: {model_name}")
    if not dependency_watcher.dependencies_ok(model_name):
        error_message = f"Dependencies for model '{model_name}' are not healthy. Aborting model load."
        logger.error(error_message)
        raise RuntimeError(error_message)

