import os
import shutil
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
import logging
import sys
# Note: Avoid importing deprecated/removed symbols from huggingface_hub.utils

import os
import shutil
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple, Callable
import logging
import sys
from sqlalchemy.orm import Session # Import Session

from billing.plan_guard import PlanGuard, PlanGuardException # New import
from backend.core.dependencies_enforcer import DependencyEnforcer # New import
from database import get_db # New import

logger = logging.getLogger(__name__)

# Determine project root (assuming model_store.py is in backend/ai_models/)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
MODELS_BASE_DIR = PROJECT_ROOT / "models" # This is the top-level models directory

class ModelStore:
    """
    Manages versioned model storage with atomic activation and rollback points.
    """
    _emergency_freeze_active: bool = False # Class-level flag for emergency freeze

    def __init__(self, db_session_factory: Callable[[], Session] = get_db):
        MODELS_BASE_DIR.mkdir(parents=True, exist_ok=True)
        self.plan_guard = PlanGuard(db_session_factory=db_session_factory) # Instantiate PlanGuard with db_session_factory
        self.dependency_enforcer = DependencyEnforcer(self.plan_guard) # Instantiate DependencyEnforcer

    @classmethod
    def set_emergency_freeze(cls, active: bool):
        cls._emergency_freeze_active = active
        logger.warning(f"Global emergency freeze set to: {active}")

    @classmethod
    def is_emergency_frozen(cls) -> bool:
        return cls._emergency_freeze_active

    def _check_freeze(self):
        if self._emergency_freeze_active:
            raise RuntimeError("Operation blocked: Global emergency freeze is active.")

    def _get_model_path(self, provider: str, model_name: str) -> Path:
        """Returns the base path for a specific model."""
        return MODELS_BASE_DIR / provider / model_name

    def _get_versions_path(self, provider: str, model_name: str) -> Path:
        """Returns the path to the versions directory for a model."""
        return self._get_model_path(provider, model_name) / "versions"

    def _get_active_pointer_path(self, provider: str, model_name: str) -> Path:
        """Returns the path to the 'active' symlink or active.json file."""
        return self._get_model_path(provider, model_name) / "active"

    def _get_history_path(self, provider: str, model_name: str) -> Path:
        """Returns the path to the history.json file."""
        return self._get_model_path(provider, model_name) / "history.json"

    def _read_history(self, provider: str, model_name: str) -> List[Dict[str, Any]]:
        """Reads the activation history for a model."""
        history_path = self._get_history_path(provider, model_name)
        if history_path.exists():
            with open(history_path, 'r') as f:
                return json.load(f)
        return []

    def _write_history(self, provider: str, model_name: str, history: List[Dict[str, Any]]):
        """Writes the activation history for a model."""
        history_path = self._get_history_path(provider, model_name)
        history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(history_path, 'w') as f:
            json.dump(history, f, indent=2)

    def _calculate_dir_checksum(self, directory_path: Path, hash_algo='sha256') -> str:
        """Calculates a checksum for a directory's contents."""
        hasher = hashlib.new(hash_algo)
        for root, _, files in os.walk(directory_path):
            for fname in sorted(files): # Ensure consistent order
                fpath = Path(root) / fname
                if fpath.is_file():
                    with open(fpath, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b''):
                            hasher.update(chunk)
        return hasher.hexdigest()

    async def prepare_staging(self, user_id: str, provider: str, model_name: str, version_tag: str, src_path: Path) -> Path:
        """
        Copies or hard-links downloaded artifacts into versions/<tag>; never touches active.
        """
        self._check_freeze() # Check freeze before preparing staging
        # PlanGuard check for model access
        try:
            await self.plan_guard.check_model_access(user_id, model_name)
        except PlanGuardException as e:
            logger.error(f"PlanGuardException in prepare_staging for user {user_id}, model {model_name}: {e}")
            raise e
        versions_path = self._get_versions_path(provider, model_name)
        versions_path.mkdir(parents=True, exist_ok=True)
        staging_path = versions_path / version_tag
        
        if staging_path.exists():
            logger.info(f"Staging path {staging_path} already exists. Removing old content.")
            shutil.rmtree(staging_path)

        logger.info(f"Preparing staging for {model_name} version {version_tag} from {src_path} to {staging_path}")
        
        # Use copytree for directories, copy for files
        if src_path.is_dir():
            shutil.copytree(src_path, staging_path)
        elif src_path.is_file():
            staging_path.mkdir(parents=True, exist_ok=True) # Create dir for single file
            shutil.copy(src_path, staging_path / src_path.name)
        else:
            raise ValueError(f"Source path {src_path} is neither a file nor a directory.")
        
        logger.info(f"Staging prepared at: {staging_path}")
        return staging_path

    async def activate(self, user_id: str, provider: str, model_name: str, version_tag: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Atomically activates a new model version by updating the 'active' pointer.
        Appends activation to history.json.
        """
        self._check_freeze() # Check freeze before activating
        
        # Prepare update manifest for dependency check
        update_manifest = {
            "widget_name": model_name, # Using model_name as widget_name for consistency
            "dependencies": [f"model:{model_name}@{version_tag}"], # Example dependency
            "version_tag": version_tag,
            "provider": provider,
        }
        
        # Run dependencies_enforcer check before applying update
        try:
            await self.dependency_enforcer.check_update_dependencies(user_id, update_manifest)
        except PlanGuardException as e:
            logger.error(f"PlanGuardException blocking model activation for user {user_id}, model {model_name}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during dependency check for model activation for user {user_id}, model {model_name}: {e}")
            raise PlanGuardException(f"Dependency check failed for model activation: {e}")

        model_base_path = self._get_model_path(provider, model_name)
        versions_path = self._get_versions_path(provider, model_name)
        target_version_path = versions_path / version_tag
        active_pointer_path = self._get_active_pointer_path(provider, model_name)
        
        if not target_version_path.exists():
            raise FileNotFoundError(f"Version {version_tag} not found in staging for {model_name}.")

        # Calculate checksum of the version being activated
        version_checksum = self._calculate_dir_checksum(target_version_path)
        model_base_path = self._get_model_path(provider, model_name)
        versions_path = self._get_versions_path(provider, model_name)
        target_version_path = versions_path / version_tag
        active_pointer_path = self._get_active_pointer_path(provider, model_name)
        
        if not target_version_path.exists():
            raise FileNotFoundError(f"Version {version_tag} not found in staging for {model_name}.")

        # Calculate checksum of the version being activated
        version_checksum = self._calculate_dir_checksum(target_version_path)

        # Atomic swap:
        # On Unix-like systems, os.symlink and os.rename are atomic.
        # On Windows, symlinks require admin. Fallback to active.json.
        temp_active_path = model_base_path / f"active_temp_{os.getpid()}"

        if sys.platform == "win32" and not os.getenv("PYTHON_SYMLINK_ADMIN"): # Check if symlink creation is allowed
            # Windows fallback: use active.json to store the active version tag
            active_json_path = active_pointer_path.with_suffix(".json")
            active_data = {
                "active_version_tag": version_tag,
                "active_path": str(target_version_path),
                "checksum": version_checksum,
                "activated_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            with open(active_json_path, 'w') as f:
                json.dump(active_data, f, indent=2)
            logger.info(f"Windows: Activated {model_name} version {version_tag} via {active_json_path}")
        else:
            # Unix-like or Windows with symlink admin
            if active_pointer_path.exists():
                active_pointer_path.unlink() # Remove old symlink/file
            
            os.symlink(target_version_path, active_pointer_path)
            logger.info(f"Activated {model_name} version {version_tag} via symlink: {active_pointer_path} -> {target_version_path}")

        # Append to history.json
        history = self._read_history(provider, model_name)
        history.append({
            "version_tag": version_tag,
            "checksum": version_checksum,
            "activated_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        self._write_history(provider, model_name, history)
        logger.info(f"Activation history updated for {model_name}.")

    def current(self, provider: str, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Returns active model info (path, tag, checksum).
        """
        active_pointer_path = self._get_active_pointer_path(provider, model_name)
        
        if sys.platform == "win32" and not os.getenv("PYTHON_SYMLINK_ADMIN"): # Check if symlink creation is allowed
            active_json_path = active_pointer_path.with_suffix(".json")
            if active_json_path.exists():
                with open(active_json_path, 'r') as f:
                    active_data = json.load(f)
                    active_data["path"] = active_data["active_path"] # Ensure consistent key
                    return active_data
            return None
        else:
            if active_pointer_path.is_symlink():
                target_path = Path(os.readlink(active_pointer_path))
                version_tag = target_path.name
                checksum = self._calculate_dir_checksum(target_path) # Recalculate for current
                return {
                    "version_tag": version_tag,
                    "path": str(target_path),
                    "checksum": checksum,
                    "activated_at": None # Not available from symlink
                }
            return None

    def list_versions(self, provider: str, model_name: str) -> List[Dict[str, Any]]:
        """
        Lists all available versions for a model."""
        versions_path = self._get_versions_path(provider, model_name)
        if not versions_path.exists():
            return []
        
        versions = []
        for version_dir in versions_path.iterdir():
            if version_dir.is_dir():
                try:
                    checksum = self._calculate_dir_checksum(version_dir)
                    versions.append({
                        "version_tag": version_dir.name,
                        "path": str(version_dir),
                        "checksum": checksum
                    })
                except Exception as e:
                    logger.warning(f"Could not calculate checksum for {version_dir.name}: {e}")
        return versions

    async def rollback(self, user_id: str, provider: str, model_name: str, target_tag: str) -> None:
        """
        Atomically switches back to a target version.
        Validates presence + checksum before swap.
        """
        self._check_freeze() # Check freeze before rolling back

        # Prepare update manifest for dependency check (for rollback)
        rollback_manifest = {
            "widget_name": model_name,
            "dependencies": [f"model:{model_name}@{target_tag}"], # Dependency on the target version
            "version_tag": target_tag,
            "provider": provider,
        }

        # Run dependencies_enforcer check before applying rollback
        try:
            await self.dependency_enforcer.check_update_dependencies(user_id, rollback_manifest)
        except PlanGuardException as e:
            logger.error(f"PlanGuardException blocking model rollback for user {user_id}, model {model_name}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during dependency check for model rollback for user {user_id}, model {model_name}: {e}")
            raise PlanGuardException(f"Dependency check failed for model rollback: {e}")

        model_base_path = self._get_model_path(provider, model_name)
        versions_path = self._get_versions_path(provider, model_name)
        target_version_path = versions_path / target_tag
        active_pointer_path = self._get_active_pointer_path(provider, model_name)

        if not target_version_path.exists():
            raise FileNotFoundError(f"Rollback target version {target_tag} not found for {model_name}.")

        # Validate checksum of the target version before rollback
        target_checksum = self._calculate_dir_checksum(target_version_path)
        history = self._read_history(provider, model_name)
        history_entry = next((entry for entry in history if entry["version_tag"] == target_tag), None)

        if history_entry and history_entry["checksum"] != target_checksum:
            logger.warning(f"Checksum mismatch for rollback target {target_tag}. Expected {history_entry['checksum']}, got {target_checksum}.")
            # Decide whether to proceed or raise error. For safety, raise error.
            raise ValueError(f"Checksum mismatch for rollback target {target_tag}. Aborting rollback.")

        # Perform atomic swap (same logic as activate)
        if sys.platform == "win32" and not os.getenv("PYTHON_SYMLINK_ADMIN"): # Check if symlink creation is allowed
            active_json_path = active_pointer_path.with_suffix(".json")
            active_data = {
                "active_version_tag": target_tag,
                "active_path": str(target_version_path),
                "checksum": target_checksum,
                "activated_at": datetime.now().isoformat(),
                "metadata": {"rolled_back_from": self.current(provider, model_name)["version_tag"] if self.current(provider, model_name) else "unknown"}
            }
            with open(active_json_path, 'w') as f:
                json.dump(active_data, f, indent=2)
            logger.info(f"Windows: Rolled back {model_name} to version {target_tag} via {active_json_path}")
        else:
            if active_pointer_path.exists():
                active_pointer_path.unlink()
            os.symlink(target_version_path, active_pointer_path)
            logger.info(f"Rolled back {model_name} to version {target_tag} via symlink: {active_pointer_path} -> {target_version_path}")

        # Append rollback to history.json
        history.append({
            "version_tag": target_tag,
            "checksum": target_checksum,
            "activated_at": datetime.now().isoformat(),
            "metadata": {"action": "rollback", "rolled_back_from": self.current(provider, model_name)["version_tag"] if self.current(provider, model_name) else "unknown"}
        })
        self._write_history(provider, model_name, history)
        logger.info(f"Rollback history updated for {model_name}.")

    def prune(self, provider: str, model_name: str, keep: int = 3) -> None:
        """
        Keeps the most-recent N versions and prunes older ones.
        Does not prune the currently active version.
        """
        history = self._read_history(provider, model_name)
        if not history:
            logger.info(f"No history found for {model_name}. Nothing to prune.")
            return

        # Sort history by activation date (most recent first)
        history.sort(key=lambda x: datetime.fromisoformat(x["activated_at"]), reverse=True)

        active_version_tag = self.current(provider, model_name)["version_tag"] if self.current(provider, model_name) else None
        
        versions_to_keep_tags = set()
        versions_to_keep_paths = set()

        # Always keep the active version
        if active_version_tag:
            versions_to_keep_tags.add(active_version_tag)
            active_path_info = self.current(provider, model_name)
            if active_path_info and active_path_info["path"]:
                versions_to_keep_paths.add(Path(active_path_info["path"]))

        # Keep the most recent 'keep' versions from history
        for entry in history:
            if len(versions_to_keep_tags) < keep + (1 if active_version_tag else 0): # +1 if active is not in history yet
                versions_to_keep_tags.add(entry["version_tag"])
                versions_to_keep_paths.add(self._get_versions_path(provider, model_name) / entry["version_tag"])
            else:
                break # Stop if we have enough versions

        versions_path = self._get_versions_path(provider, model_name)
        if not versions_path.exists():
            return

        for version_dir in versions_path.iterdir():
            if version_dir.is_dir() and version_dir not in versions_to_keep_paths:
                logger.info(f"Pruning old version: {version_dir.name}")
                try:
                    shutil.rmtree(version_dir)
                except Exception as e:
                    logger.error(f"Failed to prune {version_dir.name}: {e}")
            else:
                logger.debug(f"Keeping version: {version_dir.name}")

        logger.info(f"Pruning completed for {model_name}. Kept {len(versions_to_keep_tags)} versions.")