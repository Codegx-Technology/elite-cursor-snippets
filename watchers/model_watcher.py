import requests
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal # Assuming SessionLocal is your session factory
from backend.notifications.admin_notifier import notify_admin
from backend.ai.models import ModelVersion, VoiceVersion
from logging_setup import get_logger # Import logger

from config_loader import get_config

config = get_config()
logger = get_logger(__name__) # Initialize logger

def check_model_updates(db: Session):
    """Check remote APIs for new LLM model versions"""
    new_releases = []

    # Load watched LLM models from config.yaml
    # Assuming config.models.llm_models or similar structure
    watched_llm_models_config = config.models.get("llm_models", {}) # Get from config, default to empty dict

    for model_type, model_info in watched_llm_models_config.items():
        model_name = model_info.get("name")
        provider = model_info.get("provider")
        api_id = model_info.get("api_id")

        if not all([model_name, provider, api_id]):
            logger.warning(f"Skipping incomplete LLM model configuration: {model_info}")
            continue

        if provider == "huggingface":
            try:
                resp = requests.get(f"https://huggingface.co/api/models/{api_id}")
                resp.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                data = resp.json()
                version_tag = data.get("sha", "")[:8]  # short commit ref

                if not version_tag:
                    logger.warning(f"HuggingFace API for {model_name} returned no SHA for version tag.")
                    continue

                # Check if version already exists in DB
                if not db.query(ModelVersion).filter_by(name=model_name, version=version_tag).first():
                    new_model_version = ModelVersion(
                        name=model_name,
                        version=version_tag,
                        checksum=data.get("sha"), # Use full SHA as checksum
                        released_at=datetime.utcnow()
                    )
                    db.add(new_model_version)
                    db.commit()
                    db.refresh(new_model_version)
                    new_releases.append(f"{model_name} {version_tag}")
            except requests.exceptions.RequestException as e:
                logger.error(f"HuggingFace API request failed for {model_name} ({api_id}): {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred during HuggingFace model check for {model_name}: {e}", exc_info=True)

    if new_releases:
        notify_admin(
            subject="[Watcher] New LLM Model Versions Released",
            message="; ".join(new_releases),
            system=True,
            email=True,
        )
        logger.info(f"New LLM model releases: {new_releases}")

def check_tts_updates(db: Session):
    """Check HuggingFace/other APIs for new TTS versions"""
    new_releases = []

    # Example: HuggingFace XTTS v3 check
    try:
        resp = requests.get("https://huggingface.co/api/models/coqui/XTTS-v3")
        resp.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        if resp.status_code == 200:
            data = resp.json()
            version_tag = data.get("sha", "")[:8]  # short commit ref
            
            if not version_tag:
                logger.warning(f"HuggingFace API for XTTS returned no SHA for version tag.")
                return

            # Check if version already exists in DB
            if not db.query(VoiceVersion).filter_by(name="XTTS", version=version_tag).first():
                new_voice_version = VoiceVersion(
                    name="XTTS",
                    version=version_tag,
                    released_at=datetime.utcnow()
                )
                db.add(new_voice_version)
                db.commit()
                db.refresh(new_voice_version)
                new_releases.append(f"XTTS {version_tag}")
    except requests.exceptions.RequestException as e:
        logger.error(f"HuggingFace API request failed for XTTS: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during XTTS check: {e}", exc_info=True)

    # Example: ElevenLabs (pseudo)
    # if elevenlabs_api_check():
    #   register version → VoiceVersion.objects.create(...)

    if new_releases:
        notify_admin(
            subject="[Watcher] New TTS Voices Released",
            message="; ".join(new_releases),
            system=True,
            email=True,
        )
        logger.info(f"New TTS releases: {new_releases}")

def run_model_watchers():
    """Main watcher entrypoint"""
    db = SessionLocal() # Create a new session
    try:
        # Existing LLM model check
        check_model_updates(db)

        # New: TTS voices check
        check_tts_updates(db)
    finally:
        db.close() # Close the session