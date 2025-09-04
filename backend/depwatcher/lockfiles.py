import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List
import logging
import os

logger = logging.getLogger(__name__)

def read_lock(env_name: str, snapshot_id: str) -> Dict[str, str]:
    """Reads a pip freeze lock file for a given environment and snapshot ID."""
    lock_file_path = Path(f".ops/snapshots/{snapshot_id}_{env_name}.txt")
    if not lock_file_path.exists():
        return {}
    
    deps = {}
    with open(lock_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '==' in line:
                    name, version = line.split('==', 1)
                    deps[name] = version
    return deps

def write_lock(env_name: str, snapshot_id: str, deps: Dict[str, str]):
    """Writes a pip freeze-like lock file for a given environment and snapshot ID."""
    ops_snapshots_dir = Path(".ops/snapshots")
    ops_snapshots_dir.mkdir(parents=True, exist_ok=True)
    lock_file_path = ops_snapshots_dir / f"{snapshot_id}_{env_name}.txt"
    
    with open(lock_file_path, 'w') as f:
        for name, version in deps.items():
            f.write(f"{name}=={version}\n")
    logger.info(f"Wrote lock file for {env_name} to {lock_file_path}")

def write_model_manifest(model_name: str, snapshot_id: str, files: List[Dict[str, Any]]):
    """Writes a manifest for a model, including file paths, sizes, and hashes."""
    ops_snapshots_dir = Path(".ops/snapshots")
    ops_snapshots_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = ops_snapshots_dir / f"{snapshot_id}_{model_name}_manifest.json"
    
    with open(manifest_path, 'w') as f:
        json.dump(files, f, indent=2)
    logger.info(f"Wrote model manifest for {model_name} to {manifest_path}")

def read_model_manifest(model_name: str, snapshot_id: str) -> List[Dict[str, Any]]:
    """Reads a model manifest file."""
    manifest_path = Path(f".ops/snapshots/{snapshot_id}_{model_name}_manifest.json")
    if not manifest_path.exists():
        return []
    with open(manifest_path, 'r') as f:
        return json.load(f)
