import os
import json
from pathlib import Path
from datetime import datetime

VOICE_STORE_DIR = Path("model_store/voices")
VOICE_STORE_DIR.mkdir(parents=True, exist_ok=True)

VERSIONS_FILE = VOICE_STORE_DIR / "versions.json"

def load_versions():
    if VERSIONS_FILE.exists():
        return json.loads(VERSIONS_FILE.read_text())
    return {}

def save_versions(data):
    VERSIONS_FILE.write_text(json.dumps(data, indent=2))

def register_voice(voice_name, version, metadata=None):
    versions = load_versions()
    versions.setdefault(voice_name, {})
    versions[voice_name][version] = {
        "registered_at": datetime.utcnow().isoformat(),
        "metadata": metadata or {}
    }
    save_versions(versions)

def get_latest_voice(voice_name):
    versions = load_versions().get(voice_name, {})
    if not versions: return None
    return sorted(versions.keys())[-1]

def rollback_voice(voice_name, target_version):
    versions = load_versions()
    if voice_name not in versions or target_version not in versions[voice_name]:
        raise ValueError(f"Version {target_version} for {voice_name} not found")
    versions[voice_name]["active"] = target_version
    save_versions(versions)
    return target_version

def get_active_voice(voice_name):
    versions = load_versions().get(voice_name, {})
    return versions.get("active", get_latest_voice(voice_name))

# Example usage:
# register_voice("xtts", "v2", {"lang":"multi", "source":"HuggingFace"})
# rollback_voice("xtts", "v1")