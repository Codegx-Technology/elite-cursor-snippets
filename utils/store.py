# utils/store.py

from typing import Dict, Any, Optional

class ModelStore:
    """
    Placeholder for a simplified ModelStore to satisfy model_watcher.py imports.
    In a real system, this would interact with a database or persistent storage.
    """
    def __init__(self):
        self._models: Dict[str, Dict[str, Any]] = {}

    def get_model(self, key: str) -> Optional[Dict[str, Any]]:
        return self._models.get(key)

    def stage_model_update(self, key: str, latest_meta: Dict[str, Any]):
        self._models[key] = latest_meta
        print(f"[ModelStore] Staged update for {key}: {latest_meta}")
