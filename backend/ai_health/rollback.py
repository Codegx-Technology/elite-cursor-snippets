import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

from backend.ai_models.model_store import ModelStore # Assuming ModelStore is accessible this way
from billing.plan_guard import PlanGuard, PlanGuardException # New import

logger = logging.getLogger(__name__)
model_store = ModelStore()
plan_guard = PlanGuard() # Instantiate PlanGuard

# Determine project root (assuming rollback.py is in backend/ai_health/)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()

def _get_model_history_path(provider: str, model_name: str) -> Path:
    """Returns the path to the history.json file for a model."""
    # This path needs to match how ModelStore determines its history path
    return PROJECT_ROOT / "models" / provider / model_name / "history.json"

def _read_model_history(provider: str, model_name: str) -> List[Dict[str, Any]]:
    """Reads the activation history for a model."""
    history_path = _get_model_history_path(provider, model_name)
    if history_path.exists():
        with open(history_path, 'r') as f:
            return json.load(f)
    return []

def should_rollback(agg_metrics: Dict[str, Any], thresholds: Dict[str, Any]) -> bool:
    """
    Determines if a rollback is necessary based on aggregated metrics and predefined thresholds.
    agg_metrics example: {"error_rate": 0.15, "avg_response_time": 5.2, "success_rate": 0.85}
    thresholds example: {"error_rate_threshold": 0.1, "min_success_rate": 0.9, "max_avg_response_time": 5.0}
    """
    error_rate = agg_metrics.get("error_rate", 0.0)
    success_rate = agg_metrics.get("success_rate", 1.0)
    avg_response_time = agg_metrics.get("avg_response_time", 0.0)

    if error_rate > thresholds.get("error_rate_threshold", 0.05):
        logger.warning(f"Rollback triggered: Error rate {error_rate:.2f} exceeds threshold {thresholds.get('error_rate_threshold', 0.05):.2f}")
        return True
    
    if success_rate < thresholds.get("min_success_rate", 0.95):
        logger.warning(f"Rollback triggered: Success rate {success_rate:.2f} below threshold {thresholds.get('min_success_rate', 0.95):.2f}")
        return True

    if avg_response_time > thresholds.get("max_avg_response_time", 10.0):
        logger.warning(f"Rollback triggered: Average response time {avg_response_time:.2f}s exceeds threshold {thresholds.get('max_avg_response_time', 10.0):.2f}s")
        return True

    return False

async def perform_rollback(provider: str, model_name: str, dry_run: bool = False, user_id: Optional[str] = None) -> Optional[str]:
    """
    Performs a rollback to the last known good version of a model.
    Returns the tag of the version rolled back to, or None if no rollback occurred.
    """
    if user_id:
        try:
            await plan_guard.check_rollback_permission(user_id)
        except PlanGuardException as e:
            logger.error(f"PlanGuardException in perform_rollback for user {user_id}, model {model_name}: {e}")
            raise e

    history = _read_model_history(provider, model_name)
    
    # Find the last successfully activated version that is not the current one
    current_active = model_store.current(provider, model_name)
    current_tag = current_active["version_tag"] if current_active else None

    last_known_good_tag = None
    for entry in reversed(history):
        # Assuming "success" or "status" key in history entry indicates good state
        # For now, we'll consider any previously activated version as "good" for rollback purposes
        # A more sophisticated system would mark versions as "good" after post-deployment tests
        if entry["version_tag"] != current_tag:
            last_known_good_tag = entry["version_tag"]
            break
    
    if not last_known_good_tag:
        logger.info(f"No suitable previous version found for rollback for {provider}/{model_name}.")
        return None

    logger.info(f"Attempting to roll back {provider}/{model_name} from {current_tag} to {last_known_good_tag}")

    if dry_run:
        logger.info(f"Dry run: Would roll back {provider}/{model_name} to {last_known_good_tag}")
        return last_known_good_tag
    
    try:
        model_store.rollback(user_id, provider, model_name, last_known_good_tag) # Pass user_id
        logger.info(f"Successfully rolled back {provider}/{model_name} to {last_known_good_tag}")
        return last_known_good_tag
    except Exception as e:
        logger.error(f"Failed to perform rollback for {provider}/{model_name} to {last_known_good_tag}: {e}")
        return None