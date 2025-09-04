import logging
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from backend.depwatcher.schemas import PatchPlan, PatchCandidate
from backend.depwatcher.lockfiles import write_lock, read_lock, write_model_manifest, read_model_manifest
from backend.depwatcher.envs import detect_envs, run_in_env
from backend.depwatcher.model_store import hf_cache_root, calculate_file_hash
from backend.notifications.admin_notifier import notify_admin
import asyncio

logger = logging.getLogger(__name__)

async def pre_patch_snapshot(plan: PatchPlan):
    """
    Takes a snapshot of the current environment before patching.
    For pip: freezes installed packages.
    For models: lists existing files with hashes.
    """
    logger.info(f"Taking pre-patch snapshot for plan: {plan.id}")
    snapshot_id = plan.id # Use plan ID as snapshot ID

    # Snapshot pip environments
    available_envs = {env['name']: env for env in detect_envs()}
    for env_name, env_info in available_envs.items():
        try:
            result = await asyncio.to_thread(run_in_env, env_info, [env_info["pip"], "freeze"])
            deps = {}
            for line in result.stdout.splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    if '==' in line:
                        name, version = line.split('==', 1)
                        deps[name] = version
            write_lock(env_name, snapshot_id, deps)
            logger.info(f"Snapshot for pip env '{env_name}' taken.")
        except Exception as e:
            logger.warning(f"Could not take pip snapshot for env '{env_name}': {e}")

    # Snapshot models
    for item in plan.items:
        if item.kind == "model":
            if item.source == "huggingface":
                # For HF models, we assume they are in the HF cache
                # We need to list the files and their hashes using the local HF cache heuristic
                hub_cache = hf_cache_root() / "hub"
                repo_slug = f"models--{item.name.replace('/', '--')}"
                model_dirs = []
                if hub_cache.exists() and hub_cache.is_dir():
                    for d in hub_cache.iterdir():
                        if d.is_dir() and d.name.startswith(repo_slug):
                            model_dirs.append(d)
                if model_dirs:
                    files_manifest = []
                    for model_dir in model_dirs:
                        for root, _, filenames in os.walk(model_dir):
                            for fname in filenames:
                                fpath = Path(root) / fname
                                if fpath.is_file():
                                    try:
                                        rel_base = model_dir
                                        files_manifest.append({
                                            "path": str(fpath.relative_to(rel_base)),
                                            "size": fpath.stat().st_size,
                                            "hash": calculate_file_hash(fpath)
                                        })
                                    except Exception as e:
                                        logger.warning(f"Could not hash file {fpath}: {e}")
                    write_model_manifest(item.name, snapshot_id, files_manifest)
                    logger.info(f"Snapshot for HF model '{item.name}' taken.")
                else:
                    logger.info(f"HF model '{item.name}' not found in cache for snapshot.")
            elif item.kind == "asset" and item.local_path: # Assuming assets might have local_path
                asset_path = Path(item.local_path)
                if asset_path.is_dir():
                    files_manifest = []
                    for root, _, filenames in os.walk(asset_path):
                        for fname in filenames:
                            fpath = Path(root) / fname
                            if fpath.is_file():
                                try:
                                    files_manifest.append({
                                        "path": str(fpath.relative_to(asset_path)),
                                        "size": fpath.stat().st_size,
                                        "hash": calculate_file_hash(fpath)
                                    })
                                except Exception as e:
                                    logger.warning(f"Could not hash file {fpath}: {e}")
                    write_model_manifest(item.name, snapshot_id, files_manifest)
                    logger.info(f"Snapshot for asset '{item.name}' taken.")
                elif asset_path.is_file():
                    try:
                        files_manifest = [{
                            "path": asset_path.name,
                            "size": asset_path.stat().st_size,
                            "hash": calculate_file_hash(asset_path)
                        }]
                        write_model_manifest(item.name, snapshot_id, files_manifest)
                        logger.info(f"Snapshot for asset file '{item.name}' taken.")
                    except Exception as e:
                        logger.warning(f"Could not hash asset file {asset_path}: {e}")
                else:
                    logger.info(f"Asset '{item.name}' not found for snapshot.")

    logger.info("Pre-patch snapshot process completed.")


async def rollback(plan_id: str):
    """
    Rolls back a failed patch plan using the pre-patch snapshot.
    """
    logger.warning(f"Initiating rollback for plan: {plan_id}")
    snapshot_id = plan_id # Use plan ID as snapshot ID

    # Rollback pip environments
    available_envs = {env['name']: env for env in detect_envs()}
    for env_name, env_info in available_envs.items():
        try:
            # Read the snapshot lock file
            deps_to_reinstall = read_lock(env_name, snapshot_id)
            if deps_to_reinstall:
                # Uninstall current versions and reinstall snapshot versions
                # This is a simplified approach. A more robust one would compare diffs.
                pip_cmd = [env_info["pip"], "install", "--no-warn-script-location", "--force-reinstall"]
                for name, version in deps_to_reinstall.items():
                    pip_cmd.append(f"{name}=={version}")
                
                logger.info(f"Reinstalling snapshot dependencies for env '{env_name}'.")
                result = await asyncio.to_thread(run_in_env, env_info, pip_cmd)
                if result.returncode != 0:
                    raise Exception(f"Pip reinstall failed during rollback: {result.stderr}")
                logger.info(f"Rollback for pip env '{env_name}' completed.")
            else:
                logger.info(f"No pip snapshot found for env '{env_name}'. Skipping pip rollback.")
        except Exception as e:
            logger.error(f"Error during pip rollback for env '{env_name}': {e}")
            notify_admin(
                subject=f"CRITICAL: Rollback Failed for {env_name}",
                message=f"Failed to rollback pip packages for environment {env_name} for plan {plan_id}. Error: {e}"
            )

    # Rollback models/assets (placeholder)
    # NOTE: Detailed model/asset rollback is not implemented in this function signature.
    # It previously referenced an undefined 'plan'. Implement as needed in future.
    logger.info("Model/asset rollback is not implemented in this minimal rollback flow.")

    logger.info(f"Rollback for plan {plan_id} completed (placeholder for models/assets).")
    notify_admin(
        subject=f"Rollback Completed for Plan {plan_id}",
        message=f"Rollback process for patch plan {plan_id} has completed. Please verify system state."
    )