import logging
import json
from pathlib import Path
from typing import Dict, Any
from backend.depwatcher.schemas import PatchPlan, PatchCandidate
from backend.depwatcher.envs import detect_envs, run_in_env
from backend.depwatcher.model_store import fetch_model
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
                env = available_envs.get(item.env)
                if not env:
                    raise ValueError(f"Environment '{item.env}' not found for pip package '{item.name}'")
                
                # Construct pip install command
                pip_cmd = [env["pip"], "install", "--upgrade", "--no-warn-script-location"]
                if item.source == "pypi": # Assuming pypi for now
                    pip_cmd.append(f"{item.name}=={item.toVersion}") # Pin exact version
                else:
                    pip_cmd.append(f"{item.name}=={item.toVersion}") # Fallback for other sources

                # Add --only-binary=:all: if applicable and desired
                # pip_cmd.append("--only-binary=:all:") 

                # TODO: Respect constraints.txt/requirements.lock if pinned lock exists
                # This would involve parsing the lock file and adding -c <lock_file>

                result = await asyncio.to_thread(run_in_env, env, pip_cmd) # Run sync function in thread
                if result.returncode != 0:
                    raise Exception(f"Pip install failed: {result.stderr}")
                step_info.update({"status": "completed", "message": f"Successfully installed/upgraded {item.name}", "stdout": result.stdout, "stderr": result.stderr})

            elif item.kind == "model":
                # Assuming model_id is item.name, and provider is inferred or passed
                # For now, assume huggingface provider
                downloaded, size_mb = await fetch_model(provider="huggingface", model_id=item.name, revision=item.toVersion)
                if not downloaded:
                    raise Exception(f"Failed to fetch model: {item.name}")
                step_info.update({"status": "completed", "message": f"Successfully fetched model {item.name}", "downloadSizeMB": size_mb})

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
                        shutil.copy(source_asset_path, destination_asset_path)
                        logger.info(f"Copied asset from {source_asset_path} to {destination_asset_path}")
                        step_info.update({"status": "completed", "message": f"Successfully fetched asset {item.name} to {destination_asset_path}"})
                    except Exception as e:
                        raise Exception(f"Failed to copy asset {item.name}: {e}")
                else:
                    raise FileNotFoundError(f"Source asset not found: {source_asset_path}")

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