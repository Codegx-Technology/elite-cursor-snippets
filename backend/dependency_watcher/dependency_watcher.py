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

logger = logging.getLogger(__name__)

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

            installed_version = None
            status = "HEALTHY"
            message = ""

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
                "message": message
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
                    # Create a PatchCandidate from the dependency info
                    # This is a simplified conversion; real implementation might need more data
                    patch_candidates.append({
                        "id": str(uuid.uuid4()), # Generate a new ID for the candidate
                        "kind": "pip" if dep['message'].startswith("Package") else "model",
                        "env": dep['message'].split('venv: ')[1].split(')')[0] if 'venv' in dep['message'] else None,
                        "name": dep['name'],
                        "fromVersion": dep['installed_version'],
                        "toVersion": dep['required_range'].split('-')[0] if dep['required_range'] else dep['installed_version'], # Target version
                        "source": "pypi" if dep['message'].startswith("Package") else "huggingface", # Simplified source
                        "downloadSizeMB": None # To be determined by patcher
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