import logging
import json
import subprocess
from pathlib import Path
from typing import Dict, Any
from backend.depwatcher.schemas import PatchPlan, PatchCandidate
from backend.depwatcher.envs import detect_envs, run_in_env
from backend.depwatcher.model_store import (
    fetch_model,
    is_model_present,
    find_existing_model_dirs,
    ensure_preferred_model_dir,
)
from backend.core.dependency_ws import manager as ws_manager # WebSocket manager
from backend.depwatcher.rollback import pre_patch_snapshot, rollback # Import rollback functions
import asyncio
import shutil # For copying assets

logger = logging.getLogger(__name__)

async def apply_patch_plan(plan: PatchPlan):
    """
    Applies a patch plan, handling pip installations, model downloads, and asset fetching.
    Emits WebSocket progress events.
    Includes pre-patch snapshot and rollback on failure.
    """
    logger.info(f"Applying patch plan: {plan.id} in {plan.mode} mode.")
    
    # Ensure .ops/patches directory exists for transaction logs
    ops_dir = Path(".ops/patches")
    ops_dir.mkdir(parents=True, exist_ok=True)
    transaction_log_path = ops_dir / f"{plan.id}.json"

    # Detect environments once
    available_envs = {env['name']: env for env in detect_envs()}

    progress_events = [] # To store events for the transaction log

    try:
        # 1. Take pre-patch snapshot
        await pre_patch_snapshot(plan)
        
        for i, item in enumerate(plan.items):
            step_info = {
                "step": i + 1,
                "total_steps": len(plan.items),
                "item_name": item.name,
                "item_kind": item.kind,
                "status": "in_progress",
                "message": f"Processing {item.kind}: {item.name}"
            }
            progress_events.append(step_info)
            await ws_manager.broadcast({"event": "patch_progress", "data": step_info})
            logger.info(f"Processing {item.kind}: {item.name} from {item.fromVersion} to {item.toVersion}")

            if item.kind == "pip":
                # Resolve environment; fallback to first detected env if none provided
                env = available_envs.get(item.env) if item.env else None
                if not env:
                    if available_envs:
                        env = next(iter(available_envs.values()))
                        logger.warning(
                            f"No environment specified for {item.name}; defaulting to detected env '{env.get('name','unknown')}'."
                        )
                    else:
                        raise ValueError(
                            f"No Python environments detected for pip package '{item.name}'. Configure an env or install manually."
                        )
                
                # Construct pip install command
                pip_cmd = [env["pip"], "install", "--upgrade", "--no-warn-script-location"]
                pkg_spec = item.name
                if item.toVersion:
                    pkg_spec = f"{item.name}=={item.toVersion}"
                pip_cmd.append(pkg_spec)

                # Add --only-binary=:all: if applicable and desired
                # pip_cmd.append("--only-binary=:all:") 

                # TODO: Respect constraints.txt/requirements.lock if pinned lock exists
                # This would involve parsing the lock file and adding -c <lock_file>

                result = await asyncio.to_thread(run_in_env, env, pip_cmd) # Run sync function in thread
                if result.returncode != 0:
                    raise Exception(f"Pip install failed: {result.stderr}")
                step_info.update({"status": "completed", "message": f"Successfully installed/upgraded {item.name}", "stdout": result.stdout, "stderr": result.stderr})

            elif item.kind == "model":
                # Determine provider from item.source
                provider = (item.source or "huggingface").lower()
                model_id = item.name
                revision = item.toVersion if item.toVersion and item.toVersion != "latest" else None

                # 0) Prefer placing under models/<last-segment>
                preferred_dir = ensure_preferred_model_dir(model_id)

                # 1) Check existing project models directory for a matching folder
                existing_dirs = find_existing_model_dirs(model_id)
                if existing_dirs:
                    logger.info(f"Model '{model_id}' already present at: {existing_dirs[0]}; skipping download.")
                    step_info.update({
                        "status": "completed",
                        "message": f"Model present at {existing_dirs[0]}, no download.",
                        "downloadSizeMB": 0.0,
                    })
                else:
                    # 2) Provider-specific presence check and fetch
                    if provider == "huggingface":
                        present = await is_model_present("huggingface", model_id, revision=revision)
                        if present:
                            logger.info(f"HF model '{model_id}' already cached; no download needed.")
                            step_info.update({
                                "status": "completed",
                                "message": f"HF cache already has {model_id}",
                                "downloadSizeMB": 0.0,
                            })
                        else:
                            downloaded, size_mb = await fetch_model(provider="huggingface", model_id=model_id, revision=revision)
                            if not downloaded:
                                raise Exception(f"Failed to fetch model: {model_id}")
                            step_info.update({
                                "status": "completed",
                                "message": f"Fetched model {model_id}",
                                "downloadSizeMB": size_mb,
                            })
                    elif provider == "local_path":
                        # Ensure the preferred directory exists; do not attempt remote download
                        preferred_dir.mkdir(parents=True, exist_ok=True)
                        logger.info(f"Ensured local model directory at {preferred_dir}")
                        step_info.update({
                            "status": "completed",
                            "message": f"Ensured local model dir {preferred_dir}",
                            "downloadSizeMB": 0.0,
                        })
                    else:
                        raise ValueError(f"Unsupported model provider: {provider}")

            elif item.kind == "asset":
                # For assets, assume item.name is the source path (relative to project root)
                # and item.toVersion is the destination path (relative to assets directory)
                # This is a simplified implementation. A real asset management system would be more complex.
                project_root = Path(__file__).parent.parent.parent.parent # Get to ShujaaStudio root
                source_asset_path = project_root / item.name
                destination_asset_dir = project_root / "assets" / item.toVersion # Assuming toVersion is a subdirectory in assets

                destination_asset_dir.mkdir(parents=True, exist_ok=True)
                destination_asset_path = destination_asset_dir / source_asset_path.name

                if source_asset_path.exists():
                    try:
                        shutil.copy2(source_asset_path, destination_asset_path)
                        logger.info(f"Copied asset from {source_asset_path} to {destination_asset_path}")
                        step_info.update({"status": "completed", "message": f"Successfully fetched asset {item.name} to {destination_asset_path}"})
                    except Exception as e:
                        raise Exception(f"Failed to copy asset {item.name}: {e}")
                else:
                    raise FileNotFoundError(f"Source asset not found: {source_asset_path}")

            elif item.kind == "node":
                workdir = Path(item.workdir or ".").resolve()
                if not workdir.exists():
                    raise FileNotFoundError(f"Node workdir not found: {workdir}")
                pkg_json = workdir / "package.json"
                if not pkg_json.exists():
                    raise FileNotFoundError(f"package.json not found in {workdir}")

                # Choose package manager based on lockfiles
                pnpm_lock = workdir / "pnpm-lock.yaml"
                yarn_lock = workdir / "yarn.lock"
                npm_lock = workdir / "package-lock.json"

                if pnpm_lock.exists():
                    cmd = ["pnpm", "install", "--frozen-lockfile"]
                elif yarn_lock.exists():
                    cmd = ["yarn", "install", "--frozen-lockfile"]
                elif npm_lock.exists():
                    cmd = ["npm", "ci"]
                else:
                    cmd = ["npm", "install"]

                # Idempotent behavior: if node_modules exists and lockfile exists, skip
                node_modules = workdir / "node_modules"
                if node_modules.exists() and (pnpm_lock.exists() or yarn_lock.exists() or npm_lock.exists()):
                    logger.info(f"Node dependencies already present in {workdir}; skipping install.")
                    step_info.update({"status": "completed", "message": f"Node deps present in {workdir}", "downloadSizeMB": 0.0})
                else:
                    logger.info(f"Installing Node dependencies in {workdir} with: {' '.join(cmd)}")
                    try:
                        result = subprocess.run(cmd, cwd=str(workdir), capture_output=True, text=True, check=True)
                        step_info.update({
                            "status": "completed",
                            "message": f"Installed Node deps in {workdir}",
                            "stdout": result.stdout,
                            "stderr": result.stderr,
                        })
                    except subprocess.CalledProcessError as e:
                        raise Exception(f"Node install failed in {workdir}: {e.stderr}")

            else:
                raise ValueError(f"Unknown patch item kind: {item.kind}")

            
            progress_events[-1] = step_info # Update the last event with final status

        # Write transaction log on success
        with open(transaction_log_path, 'w') as f:
            json.dump({"plan_id": plan.id, "status": "applied", "events": progress_events}, f, indent=2)
        
        logger.info(f"Patch plan {plan.id} applied successfully.")
        await ws_manager.broadcast({"event": "patch_completed", "data": {"plan_id": plan.id, "status": "success"}})

    except Exception as e:
        logger.error(f"Error applying patch plan {plan.id}: {e}")
        # 2. Rollback on failure
        await rollback(plan.id) # Call rollback function
        # Write transaction log on failure
        with open(transaction_log_path, 'w') as f:
            json.dump({"plan_id": plan.id, "status": "failed", "error": str(e), "events": progress_events}, f, indent=2)
        await ws_manager.broadcast({"event": "patch_completed", "data": {"plan_id": plan.id, "status": "failed", "error": str(e)}})
        raise # Re-raise to be caught by job orchestrator if any