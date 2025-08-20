import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def detect_envs() -> List[Dict[str, str]]:
    """Detects Python virtual environments and their executables."""
    envs = []
    # Common venv locations relative to project root
    project_root = Path(__file__).parent.parent.parent.parent.resolve()
    potential_venvs = [
        project_root / ".venv",
        project_root / "venv",
        project_root / ".venv311",
        project_root / ".venv312-lama",
        # Add other common venv names if applicable
    ]

    for venv_path in potential_venvs:
        if venv_path.is_dir():
            python_exe = None
            pip_exe = None

            # Check for Windows executables
            if sys.platform == "win32":
                python_exe = venv_path / "Scripts" / "python.exe"
                pip_exe = venv_path / "Scripts" / "pip.exe"
            # Check for Unix-like executables
            else:
                python_exe = venv_path / "bin" / "python"
                pip_exe = venv_path / "bin" / "pip"
            
            if python_exe.is_file() and pip_exe.is_file():
                envs.append({
                    "name": venv_path.name, # e.g., ".venv312-lama"
                    "path": str(venv_path),
                    "python": str(python_exe),
                    "pip": str(pip_exe)
                })
                logger.info(f"Detected environment: {venv_path.name} at {venv_path}")
            else:
                logger.warning(f"Found venv directory {venv_path.name} but missing python/pip executables.")
    
    # Also include the current running environment
    current_python = Path(sys.executable)
    current_pip = current_python.parent / ("pip.exe" if sys.platform == "win32" else "pip")
    if current_python.is_file() and current_pip.is_file():
        envs.append({
            "name": "current",
            "path": str(current_python.parent.parent), # Assuming venv structure
            "python": str(current_python),
            "pip": str(current_pip)
        })
        logger.info(f"Detected current environment: {current_python}")

    return envs

def run_in_env(env: Dict[str, str], args: List[str], timeout: int = 1800) -> subprocess.CompletedProcess:
    """Runs a command within a specified Python environment."""
    cmd = [env["python"], *args]
    logger.info(f"Running in env '{env['name']}': {' '.join(cmd)}")
    try:
        # Use shell=False and full paths for Windows safety
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=timeout)
        logger.debug(f"Stdout: {result.stdout}")
        if result.stderr:
            logger.warning(f"Stderr: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed in env '{env['name']}': {e.cmd}\nStdout: {e.stdout}\nStderr: {e.stderr}")
        raise
    except subprocess.TimeoutExpired as e:
        logger.error(f"Command timed out in env '{env['name']}': {e.cmd}")
        raise
    except Exception as e:
        logger.error(f"Error running command in env '{env['name']}': {e}")
        raise
