import logging
import yaml
from pathlib import Path
import subprocess
import importlib.metadata
from packaging.version import parse as parse_version
from backend.notifications.admin_notifier import notify_admin
from typing import Optional, List, Dict, Any
from backend.core.dependency_ws import manager # Import the WebSocket manager
import asyncio
from backend.core.feature_flags import ALLOW_AUTOPATCH # Import feature flag
from backend.depwatcher.patcher import apply_patch_plan # Import apply_patch_plan
from datetime import datetime
import uuid

# New imports for model integrity and health checks
from backend.ai_models.model_store import ModelStore
from backend.ai_health.healthcheck import aggregate
from backend.ai_health.rollback import should_rollback, perform_rollback
from config_loader import get_config # To get model configuration

logger = logging.getLogger(__name__)

# Initialize ModelStore and config
model_store = ModelStore()
config = get_config()

_last_dependency_status: List[Dict[str, Any]] = [] # Global to store last known status

def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def resolve_installed_version(package_name: str, venv_path: Optional[Path] = None) -> Optional[str]:
    """
    Resolves the installed version of a package.
    If venv_path is provided, it checks within that virtual environment.
    """
    try:
        if venv_path:
            # For packages in a specific venv, we need to run pip show in that venv
            venv_python = venv_path / "Scripts" / "python.exe" # Windows
            if not venv_python.exists(): # Try Linux/macOS path
                venv_python = venv_path / "bin" / "python"
            
            if not venv_python.exists():
                logger.warning(f"Python executable not found for venv: {venv_path}")
                return None

            cmd = [str(venv_python), '-m', 'pip', 'show', package_name]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    return line.split(":", 1)[1].strip()
            return None # Version line not found
        else:
            # Check in the current environment
            return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking package {package_name} in venv {venv_path}: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error resolving version for {package_name}: {e}")
        return None

class DependencyWatcher:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)

    def _check_dependencies_internal(self) -> List[Dict[str, Any]]:
        dependencies_status = []
        for dep in self.config.get('dependencies', []):
            name = dep['name']
            min_version_str = dep.get('min_version')
            max_version_str = dep.get('max_version')
            dep_path = dep.get('path') # For models
            venv_name = dep.get('venv')
            kind = dep.get('kind')

            installed_version = None
            status = "HEALTHY"
            message = ""

            if kind == 'node':
                # Node project dependency check (package.json based)
                workdir = Path(dep.get('workdir') or dep_path or '.')
                pkg_json = workdir / 'package.json'
                node_modules = workdir / 'node_modules'
                lock_candidates = [
                    workdir / 'pnpm-lock.yaml',
                    workdir / 'yarn.lock',
                    workdir / 'package-lock.json',
                ]

                if not pkg_json.exists():
                    status = 'MISSING'
                    message = f"Node project '{name}' missing package.json at {pkg_json}"
                elif not any(p.exists() for p in lock_candidates):
                    status = 'MISSING'
                    message = f"Node project '{name}' missing lockfile in {workdir}"
                elif not node_modules.exists():
                    status = 'MISSING'
                    message = f"Node project '{name}' missing node_modules in {workdir}"
                else:
                    status = 'HEALTHY'
                    message = f"Node project '{name}' dependencies present in {workdir}"

                dependencies_status.append({
                    "name": name,
                    "installed_version": 'N/A',
                    "required_range": '',
                    "status": status,
                    "message": message,
                    "path": str(workdir),
                    "venv": '',
                    "workdir": str(workdir),
                    "kind": 'node'
                })
                if status != 'HEALTHY':
                    logger.error(message)
                    notify_admin(message, f"Dependency Alert: {name} is {status}")
                else:
                    logger.info(message)
                continue
            
            if dep_path: # It's a model (file/directory)
                model_path = Path(dep_path)
                if not model_path.exists():
                    status = "MISSING"
                    message = f"Model '{name}' not found at path: {dep_path}"
                else:
                    message = f"Model '{name}' found at path: {dep_path}"
            else: # It's a package
                venv_path = Path(f"./{venv_name}").resolve() if venv_name else None
                installed_version_str = resolve_installed_version(name, venv_path)
                
                if installed_version_str:
                    installed_version = parse_version(installed_version_str)
                    message = f"Package '{name}' installed version: {installed_version_str}"

                    if min_version_str:
                        min_version = parse_version(min_version_str)
                        if installed_version < min_version:
                            status = "OUTDATED"
                            message = f"Package '{name}' is version {installed_version_str}, but requires minimum {min_version_str}."
                    
                    if max_version_str:
                        max_version = parse_version(max_version_str)
                        if installed_version > max_version:
                            status = "UNSUPPORTED"
                            message = f"Package '{name}' is version {installed_version_str}, which is greater than maximum supported {max_version_str}. If this is intentional, please update max_version in config."
                else:
                    status = "MISSING"
                    message = f"Package '{name}' not found."
                    if venv_name:
                        message += f" (checked in venv: {venv_name})"

            dependencies_status.append({
                "name": name,
                "installed_version": str(installed_version) if installed_version else "N/A",
                "required_range": f"{min_version_str or ''}-{max_version_str or ''}",
                "status": status,
                "message": message,
                "path": dep_path or "",
                "venv": venv_name or "",
                "kind": kind or ("model" if dep_path else "pip")
            })

            if status != "HEALTHY":
                subject = f"Dependency Alert: {name} is {status}"
                logger.error(message)
                notify_admin(message, subject)
            else:
                logger.info(message)
        
        return dependencies_status

    def run_checks(self, auto_approve: bool = False) -> List[Dict[str, Any]]:
        """
        Runs dependency checks. If auto_approve is True and ALLOW_AUTOPATCH is True,
        it will attempt to apply patches for OUTDATED/MISSING dependencies.
        """
        global _last_dependency_status
        
        logger.info("Starting dependency checks...")
        current_status_report = self._check_dependencies_internal()

        # Compare with last status and broadcast if changed
        if current_status_report != _last_dependency_status:
            logger.info("Dependency status changed. Broadcasting update via WebSocket.")
            asyncio.run(manager.broadcast({
                "event": "dependency_status",
                "data": current_status_report
            }))
            _last_dependency_status = current_status_report # Update last status
        else:
            logger.info("Dependency status unchanged.")

        # Auto-patching logic
        if auto_approve and ALLOW_AUTOPATCH:
            logger.info("Auto-approve mode enabled. Checking for patchable dependencies.")
            patch_candidates = []
            for dep in current_status_report:
                if dep['status'] == 'OUTDATED' or dep['status'] == 'MISSING':
                    # Create a PatchCandidate from the dependency info using explicit fields
                    dep_kind = dep.get('kind') or ('model' if dep.get('path') else 'pip')
                    is_model = dep_kind == 'model'
                    kind = dep_kind
                    source = 'local_path' if is_model else ('pypi' if dep_kind == 'pip' else 'node')
                    env = dep.get('venv') or None
                    # Prefer min_version as target; if empty, fall back to installed or latest (empty means unpinned)
                    req_range = dep.get('required_range') or ''
                    min_req = req_range.split('-')[0].strip() if '-' in req_range else req_range.strip()
                    to_version = min_req if min_req else (None if kind == 'pip' else 'latest')

                    patch_candidates.append({
                        "id": str(uuid.uuid4()),
                        "kind": kind,
                        "env": env,
                        "name": dep['name'],
                        "fromVersion": dep.get('installed_version'),
                        "toVersion": to_version or "",
                        "source": source,
                        "downloadSizeMB": None,
                        "workdir": dep.get('workdir') if dep_kind == 'node' else None
                    })
            
            if patch_candidates:
                logger.info(f"Found {len(patch_candidates)} patch candidates. Creating and applying patch plan.")
                # Create a dummy PatchPlan object for apply_patch_plan
                # In a real scenario, this would come from the approvals system
                dummy_plan = {
                    "id": str(uuid.uuid4()),
                    "items": patch_candidates,
                    "mode": "apply",
                    "createdBy": "auto-watcher",
                    "createdAt": datetime.now(),
                    "status": "pending"
                }
                # Convert dict to PatchPlan object
                from backend.depwatcher.schemas import PatchPlan as ActualPatchPlan
                patch_plan_obj = ActualPatchPlan(**dummy_plan)

                try:
                    asyncio.run(apply_patch_plan(patch_plan_obj))
                    logger.info("Auto-patch plan applied successfully.")
                except Exception as e:
                    logger.error(f"Auto-patch plan failed: {e}")
                    notify_admin(
                        subject="Auto-Patch Failed",
                        message=f"An attempt to auto-patch dependencies failed: {e}"
                    )
            else:
                logger.info("No patchable dependencies found.")
        elif auto_approve and not ALLOW_AUTOPATCH:
            logger.warning("Auto-approve requested, but ALLOW_AUTOPATCH feature flag is disabled. Skipping auto-patch.")
            notify_admin(
                subject="Auto-Patch Disabled",
                message="Auto-approve was requested for dependency watcher, but ALLOW_AUTOPATCH feature flag is disabled."
            )
        
        return current_status_report

    def dependencies_ok(self, model_name: str = None) -> bool:
        """
        Checks if dependencies are healthy.
        If model_name is provided, checks only dependencies related to that model.
        """
        status_report = self._check_dependencies_internal() # Get current status

        if model_name:
            # Check only the specific model/package
            for dep in status_report:
                if dep['name'] == model_name:
                    return dep['status'] == 'HEALTHY'
            logger.warning(f"Dependency '{model_name}' not found in config.")
            return False # If model_name not in config, assume not ok or needs attention
        else:
            # Check all dependencies
            for dep in status_report:
                if dep['status'] != 'HEALTHY':
                    return False
            return True

    def check_model_store_integrity(self) -> List[Dict[str, Any]]:
        """
        Verifies the integrity of models in the ModelStore.
        Checks if active pointers are valid and target directories exist.
        """
        integrity_report = []
        
        # Helper function to process a single model configuration
        def process_model_config(model_config_item, model_type_key):
            provider = "unknown"
            model_name = model_type_key
            
            if hasattr(model_config_item, 'hf_api_id') and model_config_item.hf_api_id:
                model_name = model_config_item.hf_api_id.split('/')[-1]
                provider = "huggingface"
            elif hasattr(model_config_item, 'local_fallback_path') and model_config_item.local_fallback_path:
                model_name = Path(model_config_item.local_fallback_path).name
                provider = "local"
            elif hasattr(model_config_item, 'provider') and model_config_item.provider: # For TTS models
                provider = model_config_item.provider
                model_name = model_config_item.model_name

            status = "HEALTHY"
            message = "Active model pointer is valid and target exists."
            
            try:
                current_active = model_store.current(provider, model_name)
                if not current_active:
                    status = "MISSING_ACTIVE"
                    message = f"No active version found for {provider}/{model_name}."
                else:
                    active_path = Path(current_active.get("path", ""))
                    if not active_path.exists():
                        status = "BROKEN_POINTER"
                        message = f"Active model path {active_path} for {provider}/{model_name} does not exist."
                    elif not active_path.is_dir() and not active_path.is_file():
                        status = "INVALID_TARGET"
                        message = f"Active model path {active_path} for {provider}/{model_name} is not a valid file or directory."
            except Exception as e:
                status = "ERROR"
                message = f"Error checking integrity for {provider}/{model_name}: {e}"
                logger.error(message)

            integrity_report.append({
                "provider": provider,
                "model_name": model_name,
                "status": status,
                "message": message
            })
            
            if status != "HEALTHY":
                notify_admin(subject=f"Model Integrity Alert: {model_name} is {status}", message=message)
        
        # Iterate through top-level configured models
        for model_type, model_config_item in config.models.items():
            # Check if it's a nested group like 'tts_models'
            if isinstance(model_config_item, dict) and 'provider' not in model_config_item:
                for sub_model_type, sub_model_config_item in model_config_item.items():
                    process_model_config(sub_model_config_item, sub_model_type)
            else:
                process_model_config(model_config_item, model_type)
                
        return integrity_report

    def report_canary_health(self, auto_rollback_bad: bool = False) -> List[Dict[str, Any]]:
        """
        Reports the health of canary deployments and optionally triggers rollback.
        """
        canary_health_report = []
        
        # Helper function to process a single model configuration for canary health
        def process_canary_config(model_config_item, model_type_key):
            provider = "unknown"
            model_name = model_type_key
            
            if hasattr(model_config_item, 'hf_api_id') and model_config_item.hf_api_id:
                model_name = model_config_item.hf_api_id.split('/')[-1]
                provider = "huggingface"
            elif hasattr(model_config_item, 'local_fallback_path') and model_config_item.local_fallback_path:
                model_name = Path(model_config_item.local_fallback_path).name
                provider = "local"
            elif hasattr(model_config_item, 'provider') and model_config_item.provider: # For TTS models
                provider = model_config_item.provider
                model_name = model_config_item.model_name

            current_model_info = model_store.current(provider, model_name)
            if not current_model_info:
                return # Skip if no active model info

            model_metadata = current_model_info.get("metadata", {})
            strategy = model_metadata.get("strategy")
            
            if strategy == "bluegreen":
                active_tag = current_model_info.get("version_tag") # This is the blue tag
                green_tag = model_metadata.get("green_version_tag") # This is the green tag
                
                if not green_tag:
                    logger.warning(f"Blue/Green strategy enabled for {provider}/{model_name} but no green_version_tag found in metadata.")
                    return

                # Aggregate metrics for the green (canary) tag
                # Assuming aggregate can handle non-active tags for historical data
                agg_metrics = aggregate(provider, model_name, green_tag)
                
                # Get thresholds from config (assuming they are defined in config.yaml under models.<type>)
                # Or use default thresholds if not found
                thresholds = config.models.get(model_type_key, {}).get("rollback_thresholds", {
                    "error_rate_threshold": 0.1,
                    "min_success_rate": 0.9,
                    "max_avg_response_time": 15.0
                })
                
                health_status = "HEALTHY"
                health_message = "Canary is healthy."
                
                if should_rollback(agg_metrics, thresholds):
                    health_status = "DEGRADED"
                    health_message = f"Canary health degraded. Metrics: {agg_metrics}. Thresholds: {thresholds}"
                    logger.warning(health_message)
                    
                    if auto_rollback_bad:
                        logger.info(f"Attempting auto-rollback for {provider}/{model_name} due to degraded canary health.")
                        rolled_back_to_tag = perform_rollback(provider, model_name, dry_run=False)
                        if rolled_back_to_tag:
                            notify_admin(
                                subject=f"🚨 Auto-Rollback: {model_name} Canary Degraded",
                                message=f"Canary for {provider}/{model_name} was degraded and automatically rolled back to {rolled_back_to_tag}. Metrics: {agg_metrics}"
                            )
                            health_message += f" Auto-rolled back to {rolled_back_to_tag}."
                        else:
                            health_message += " Auto-rollback failed." # Changed from error to warning
                            notify_admin(
                                subject=f"❌ Auto-Rollback Failed: {model_name} Canary Degraded",
                                message=f"Canary for {provider}/{model_name} was degraded but auto-rollback failed. Metrics: {agg_metrics}"
                            )
                
                canary_health_report.append({
                    "provider": provider,
                    "model_name": model_name,
                    "canary_tag": green_tag,
                    "active_tag": active_tag,
                    "health_status": health_status,
                    "health_message": health_message,
                    "metrics": agg_metrics
                })
                
                if health_status == "DEGRADED":
                    notify_admin(subject=f"Canary Health Alert: {model_name} is {health_status}", message=health_message)
        
        # Iterate through top-level configured models
        for model_type, model_config_item in config.models.items():
            # Check if it's a nested group like 'tts_models'
            if isinstance(model_config_item, dict) and 'provider' not in model_config_item:
                for sub_model_type, sub_model_config_item in model_config_item.items():
                    process_canary_config(sub_model_config_item, sub_model_type)
            else:
                process_canary_config(model_config_item, model_type)
                
        return canary_health_report


def run_dependency_check():
    """
    Entrypoint to run the dependency watcher.
    """
    watcher = DependencyWatcher('backend/dependency_watcher/config/dependency_config.yaml')
    status_report = watcher.run_checks() # Call run_checks
    logger.info("\n--- Dependency Check Report ---")
    for dep in status_report:
        logger.info(f"  {dep['name']:<15} | Installed: {dep['installed_version']:<10} | Required: {dep['required_range']:<10} | Status: {dep['status']:<10} | Message: {dep['message']}")
    logger.info("-----------------------------")


if __name__ == '__main__':
    run_dependency_check()