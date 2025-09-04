from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from backend.modules.superadmin.superadmin_service import get_metrics
from backend.utils.auth import get_current_user
from backend.superadmin.auth import get_current_superadmin_user # New import

router = APIRouter(prefix="/superadmin")

@router.get("/metrics")
def superadmin_metrics(current_user=Depends(get_current_user)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return get_metrics()

@router.get("/model-updates", response_model=List[Dict[str, Any]])
async def get_pending_model_updates(current_superadmin: Any = Depends(get_current_superadmin_user)):
    # TODO: Fetch real pending model updates from a database or a staging area
    # For now, return mock data
    return [
        {
            "key": "llm:gpt-neo-2.7B:v3.0.0",
            "name": "gpt-neo-2.7B",
            "provider": "huggingface",
            "current_version": "v2.0.0",
            "latest_version": "v3.0.0",
            "message": "New major version available with improved performance."
        },
        {
            "key": "tts:coqui/XTTS-v2:v2.5",
            "name": "XTTS-v2",
            "provider": "huggingface",
            "current_version": "v2.0",
            "latest_version": "v2.5",
            "message": "New minor version with bug fixes and new voices."
        }
    ]

@router.post("/model-updates/approve/{update_key}")
async def approve_model_update(update_key: str, current_superadmin: Any = Depends(get_current_superadmin_user)):
    # TODO: Implement logic to approve the update (e.g., move from staging to active)
    print(f"Superadmin {current_superadmin.username} approved update: {update_key}")
    return {"status": "success", "message": f"Update {update_key} approved."}

@router.post("/model-updates/reject/{update_key}")
async def reject_model_update(update_key: str, current_superadmin: Any = Depends(get_current_superadmin_user)):
    # TODO: Implement logic to reject the update (e.g., remove from staging)
    print(f"Superadmin {current_superadmin.username} rejected update: {update_key}")
    return {"status": "success", "message": f"Update {update_key} rejected."}

@router.get("/voices", response_model=List[Dict[str, Any]])
async def get_tts_voice_status(current_superadmin: Any = Depends(get_current_superadmin_user)):
    # TODO: Fetch real TTS voice status from backend.core.voices.versioning
    # For now, return mock data
    return [
        {
            "voice_name": "XTTS-v2",
            "active_version": {"version": "v2.0", "registered_at": "2025-08-01T10:00:00Z"},
            "available_versions": [
                {"version": "v1.0", "registered_at": "2024-01-01T00:00:00Z"},
                {"version": "v2.0", "registered_at": "2025-08-01T10:00:00Z"},
                {"version": "v2.5", "registered_at": "2025-08-15T12:00:00Z"}
            ]
        },
        {
            "voice_name": "ElevenLabs-Pro",
            "active_version": {"version": "1.3.0", "registered_at": "2025-07-01T00:00:00Z"},
            "available_versions": [
                {"version": "1.2.0", "registered_at": "2025-06-01T00:00:00Z"},
                {"version": "1.3.0", "registered_at": "2025-07-01T00:00:00Z"}
            ]
        }
    ]

@router.post("/voices/activate/{voice_name}/{version}")
async def activate_tts_voice(voice_name: str, version: str, current_superadmin: Any = Depends(get_current_superadmin_user)):
    # TODO: Implement logic to activate a specific TTS voice version
    print(f"Superadmin {current_superadmin.username} activated voice {voice_name} version {version}")
    return {"status": "success", "message": f"Voice {voice_name} version {version} activated."}
