import os
import json
from pathlib import Path
from datetime import datetime
from logging_setup import get_logger

from billing.plan_guard import PlanGuard, PlanGuardException # New import

logger = get_logger(__name__)

VOICE_STORE_DIR = Path("model_store/voices")
VOICE_STORE_DIR.mkdir(parents=True, exist_ok=True)

VERSIONS_FILE = VOICE_STORE_DIR / "versions.json"

def load_versions():
    try:
        if VERSIONS_FILE.exists():
            return json.loads(VERSIONS_FILE.read_text())
        return {}
    except FileNotFoundError:
        logger.warning(f"Versions file not found at {VERSIONS_FILE}. Returning empty versions.")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {VERSIONS_FILE}: {e}. Returning empty versions.")
        return {}
    except IOError as e:
        logger.error(f"IOError reading {VERSIONS_FILE}: {e}. Returning empty versions.")
        return {}

def save_versions(data):
    try:
        VERSIONS_FILE.write_text(json.dumps(data, indent=2))
    except TypeError as e:
        logger.error(f"TypeError: Data is not JSON serializable: {e}. Data: {data}")
    except IOError as e:
        logger.error(f"IOError writing to {VERSIONS_FILE}: {e}")

async def register_voice(user_id: str, plan_guard: PlanGuard, voice_name, version, metadata=None):
    if not voice_name or not version:
        logger.warning(f"Attempted to register voice with empty name or version. Name: '{voice_name}', Version: '{version}'")
        raise ValueError("Voice name and version cannot be empty.")

    try:
        await plan_guard.check_tts_voice_access(user_id, voice_name)
    except PlanGuardException as e:
        logger.error(f"PlanGuardException in register_voice for user {user_id}, voice {voice_name}: {e}")
        raise e

    versions = load_versions()
    versions.setdefault(voice_name, {})
    versions[voice_name][version] = {
        "registered_at": datetime.utcnow().isoformat(),
        "metadata": metadata or {}
    }
    save_versions(versions)
    logger.info(f"Voice '{voice_name}' version '{version}' registered successfully.")

def get_latest_voice(voice_name):
    versions = load_versions().get(voice_name, {})
    if not versions: 
        logger.debug(f"No versions found for voice '{voice_name}'.")
        return None
    # Filter out 'active' key before sorting
    available_versions = {k: v for k, v in versions.items() if k != "active"}
    if not available_versions:
        logger.debug(f"No actual versions (excluding 'active') found for voice '{voice_name}'.")
        return None
    
    # Sort by registered_at timestamp if available, otherwise by version string
    try:
        return sorted(available_versions.keys(), key=lambda k: available_versions[k].get("registered_at", ""))[-1]
    except Exception as e:
        logger.warning(f"Could not sort versions by 'registered_at' for voice '{voice_name}': {e}. Falling back to string sort.")
        return sorted(available_versions.keys())[-1]

async def rollback_voice(user_id: str, plan_guard: PlanGuard, voice_name, target_version):
    if not voice_name or not target_version:
        logger.warning(f"Attempted to rollback voice with empty name or target version. Name: '{voice_name}', Target Version: '{target_version}'")
        raise ValueError("Voice name and target version cannot be empty.")

    try:
        await plan_guard.check_tts_voice_access(user_id, target_version)
    except PlanGuardException as e:
        logger.error(f"PlanGuardException in rollback_voice for user {user_id}, voice {voice_name}: {e}")
        raise e

    versions = load_versions()
    if voice_name not in versions:
        logger.warning(f"Attempted rollback for non-existent voice: '{voice_name}'.")
        raise ValueError(f"Voice '{voice_name}' not found.")
    
    if target_version not in versions[voice_name]:
        logger.warning(f"Attempted rollback for voice '{voice_name}' to non-existent version: '{target_version}'.")
        raise ValueError(f"Version {target_version} for voice '{voice_name}' not found.")
    
    versions[voice_name]["active"] = target_version
    save_versions(versions)
    logger.info(f"Voice '{voice_name}' successfully rolled back to version '{target_version}'.")
    return target_version

async def get_active_voice(user_id: str, plan_guard: PlanGuard, voice_name):
    versions = load_versions().get(voice_name, {})
    active_version = versions.get("active")
    if active_version:
        logger.debug(f"Active version for voice '{voice_name}' is '{active_version}'.")
        try:
            await plan_guard.check_tts_voice_access(user_id, active_version)
        except PlanGuardException as e:
            logger.error(f"PlanGuardException in get_active_voice for user {user_id}, voice {voice_name}: {e}")
            raise e
        return active_version
    
    latest_version = get_latest_voice(voice_name)
    if latest_version:
        logger.info(f"No explicit active version for voice '{voice_name}'. Defaulting to latest: '{latest_version}'.")
        try:
            await plan_guard.check_tts_voice_access(user_id, latest_version)
        except PlanGuardException as e:
            logger.error(f"PlanGuardException in get_active_voice for user {user_id}, voice {voice_name}: {e}")
            raise e
        return latest_version
    
    logger.debug(f"No active or latest version found for voice '{voice_name}'.")
    return None