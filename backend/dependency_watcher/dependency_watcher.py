import logging
import yaml
from pathlib import Path
import subprocess
import importlib.metadata
from packaging.version import parse as parse_version
from backend.notifications.admin_notifier import notify_admin
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

    def check_dependencies(self):
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
                    # For models, version check might be more complex, or not applicable
                    # For now, just check existence. If min_version is provided, assume it's a version check for the model itself.
                    # This part needs clarification from user if models have explicit versions to check.
                    # For now, if path exists, it's healthy.
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
                            message = f"Package '{name}' is version {installed_version_str}, which is greater than maximum supported {max_version_str}."
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


def run_dependency_check():
    """
    Entrypoint to run the dependency watcher.
    """
    watcher = DependencyWatcher('backend/dependency_watcher/config/dependency_config.yaml')
    status_report = watcher.check_dependencies()
    logger.info("\n--- Dependency Check Report ---")
    for dep in status_report:
        logger.info(f"  {dep['name']:<15} | Installed: {dep['installed_version']:<10} | Required: {dep['required_range']:<10} | Status: {dep['status']:<10} | Message: {dep['message']}")
    logger.info("-----------------------------")


if __name__ == '__main__':
    run_dependency_check()