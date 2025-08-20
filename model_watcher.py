import time
from utils.store import ModelStore
from utils.notify import notify_admin

# Registry includes voices as well
WATCHED_MODELS = {
    "llm": {"provider": "huggingface", "name": "gpt-neo-2.7B"},
    "embedding": {"provider": "openai", "name": "text-embedding-3-small"},
    "tts_voice_xtts": {"provider": "huggingface", "name": "coqui/XTTS-v2"},
    "tts_voice_eleven": {"provider": "elevenlabs", "name": "english-female-v1"}
}

CHECK_INTERVAL = 3600  # 1 hour

def heartbeat():
    store = ModelStore()
    while True:
        for key, meta in WATCHED_MODELS.items():
            current_meta = store.get_model(key)
            latest_meta = check_remote(meta)

            if not current_meta or current_meta["checksum"] != latest_meta["checksum"]:
                notify_admin(
                    subject=f"🔔 New version available for {key}",
                    message=f"Model/Voice: {meta['name']} ({meta['provider']})\n"
                            f"Current: {current_meta['version'] if current_meta else 'none'}\n"
                            f"Latest: {latest_meta['version']}\n\n"
                            "Approve update in admin dashboard before rollout."
                )
                # Only save if admin approves via dashboard later
                store.stage_model_update(key, latest_meta)

        time.sleep(CHECK_INTERVAL)

def check_remote(meta: dict):
    """
    Stub for checking HuggingFace / ElevenLabs APIs.
    Returns dict with {version, checksum, last_updated}.
    """
    if meta["provider"] == "huggingface":
        # TODO: call HuggingFace API for model card metadata
        return {
            "version": "v3.0.0",
            "checksum": "abc123huggingface",
            "last_updated": "2025-08-19"
        }
    elif meta["provider"] == "elevenlabs":
        # TODO: call ElevenLabs API for voice version metadata
        return {
            "version": "v2.5",
            "checksum": "xyz789elevenlabs",
            "last_updated": "2025-08-19"
        }
    return {}

if __name__ == "__main__":
    heartbeat()
