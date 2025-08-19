import requests
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal # Assuming SessionLocal is your session factory
from backend.notifications.admin_notifier import notify_admin
from backend.ai.models import ModelVersion, VoiceVersion

def check_tts_updates(db: Session):
    """Check HuggingFace/other APIs for new TTS versions"""
    new_releases = []

    # Example: HuggingFace XTTS v3 check
    try:
        resp = requests.get("https://huggingface.co/api/models/coqui/XTTS-v3")
        if resp.status_code == 200:
            data = resp.json()
            version_tag = data.get("sha", "")[:8]  # short commit ref
            
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
    except Exception as e:
        print(f"[WARN] XTTS check failed: {e}")

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
        print(f"[Watcher] New TTS releases: {new_releases}")

def run_model_watchers():
    """Main watcher entrypoint"""
    db = SessionLocal() # Create a new session
    try:
        # Existing LLM model check
        # check_model_updates(db) # Assuming this function exists elsewhere or will be added

        # New: TTS voices check
        check_tts_updates(db)
    finally:
        db.close() # Close the session