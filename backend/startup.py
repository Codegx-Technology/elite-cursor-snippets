import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

# Adjust import paths if necessary
from config_loader import get_config
from backend.ai_models.model_store import ModelStore
from backend.ai_health.healthcheck import aggregate
from backend.ai_health.rollback import should_rollback, perform_rollback
from backend.notifications.admin_notify import send_admin_notification
from feature_flags import feature_flag_manager

logger = logging.getLogger(__name__)

# Initialize ModelStore and config
model_store = ModelStore()
config = get_config()

def run_safety_rollback_on_boot():
    """
    Guards startup: if last activation < 15 min ago AND current health is red,
    auto-rollback on boot. Ensures idempotent and logged.
    """
    if not feature_flag_manager.is_enabled("AUTO_ROLLBACK_ON_BOOT"):
        logger.info("AUTO_ROLLBACK_ON_BOOT feature flag is disabled. Skipping safety rollback check.")
        return

    logger.info("Running safety rollback check on boot...")

    # Iterate through configured models
    for model_type, model_config in config.models.items():
        provider = "unknown"
        model_name = model_type
        
        if hasattr(model_config, 'hf_api_id') and model_config.hf_api_id:
            model_name = model_config.hf_api_id.split('/')[-1]
            provider = "huggingface"
        elif hasattr(model_config, 'local_fallback_path') and model_config.local_fallback_path:
            model_name = Path(model_config.local_fallback_path).name
            provider = "local"

        current_active = model_store.current(provider, model_name)
        if not current_active:
            logger.info(f"No active version found for {provider}/{model_name}. Skipping rollback check.")
            continue

        last_activated_at_str = current_active.get("activated_at")
        if not last_activated_at_str:
            logger.warning(f"No 'activated_at' timestamp found for {provider}/{model_name}. Skipping rollback check.")
            continue

        try:
            last_activated_at = datetime.fromisoformat(last_activated_at_str)
        except ValueError:
            logger.error(f"Invalid 'activated_at' format for {provider}/{model_name}: {last_activated_at_str}. Skipping rollback check.")
            continue

        # Check if last activation was within the last 15 minutes
        if datetime.now() - last_activated_at < timedelta(minutes=15):
            logger.info(f"Model {provider}/{model_name} activated recently ({last_activated_at}). Checking health...")
            
            # Query aggregates for the current active model
            agg_metrics = aggregate(provider, model_name, current_active["version_tag"])
            
            # Get rollback thresholds (assuming they are defined in config.yaml under models.<type>)
            thresholds = config.models.get(model_type, {}).get("rollback_thresholds", {
                "error_rate_threshold": 0.1,
                "min_success_rate": 0.9,
                "max_avg_response_time": 15.0
            })

            if should_rollback(agg_metrics, thresholds):
                logger.warning(f"Degraded health detected for {provider}/{model_name} on boot. Aggregated metrics: {agg_metrics}. Initiating auto-rollback.")
                
                rolled_back_to_tag = perform_rollback(provider, model_name, dry_run=False)
                
                if rolled_back_to_tag:
                    subject = f"🚨 Auto-Rollback on Boot: {model_name} Degraded"
                    body = (
                        f"Model {provider}/{model_name} was found to be degraded on boot "
                        f"(activated at {last_activated_at_str}) and has been automatically rolled back.\n"
                        f"Metrics: {agg_metrics}\n"
                        f"Rolled back to version: {rolled_back_to_tag}"
                    )
                    send_admin_notification(subject, body)
                    logger.info(f"Auto-rollback successful for {provider}/{model_name} to {rolled_back_to_tag}.")
                else:
                    logger.info(f"Auto-rollback failed for {provider}/{model_name} on boot. Admin notification sent.")
                    send_admin_notification(
                        subject=f"❌ Auto-Rollback Failed on Boot: {model_name} Degraded",
                        message=f"Model {provider}/{model_name} was degraded on boot but auto-rollback failed. Metrics: {agg_metrics}"
                    )
            else:
                logger.info(f"Model {provider}/{model_name} is healthy on boot. No rollback needed.")
        else:
            logger.info(f"Model {provider}/{model_name} was not activated recently. Skipping rollback check.")

if __name__ == "__main__":
    # This block is for testing the script directly
    run_safety_rollback_on_boot()
