import json
import os
import sys
from pathlib import Path

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from scripts.check_and_download_models import HF_MODELS, MODELS_DIR, is_cached
except Exception as e:
    print(json.dumps({"error": f"failed to import check_and_download_models: {e}"}))
    sys.exit(0)

try:
    from huggingface_hub import HfApi  # type: ignore
    api = HfApi()
except Exception:
    api = None

results = []
for repo_id, subdir in HF_MODELS:
    present = False
    try:
        present = is_cached(repo_id, subdir)
    except Exception:
        present = False

    p = MODELS_DIR / subdir
    local_size = 0
    if p.exists():
        for root, _, files in os.walk(p):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    local_size += os.path.getsize(fp)
                except Exception:
                    pass

    remote_size = None
    if api is not None:
        # Prefer repo_info with files metadata; fallback to model_info
        try:
            info = api.repo_info(repo_id, repo_type='model', files_metadata=True)
            siblings = getattr(info, 'siblings', None)
            if siblings:
                remote_size = sum((getattr(s, 'size', 0) or 0) for s in siblings)
        except Exception:
            try:
                info = api.model_info(repo_id)
                siblings = getattr(info, 'siblings', None)
                if siblings:
                    remote_size = sum((getattr(s, 'size', 0) or 0) for s in siblings)
            except Exception:
                remote_size = None

    remaining = None
    if isinstance(remote_size, int):
        remaining = max(remote_size - local_size, 0)

    results.append({
        "repo": repo_id,
        "subdir": subdir,
        "present": present,
        "local_bytes": local_size,
        "remote_bytes": remote_size,
        "remaining_bytes": remaining,
    })

summary = {
    "models_dir": str(MODELS_DIR),
    "models": results,
    "totals": {
        "local_bytes": sum(r["local_bytes"] for r in results),
        "remaining_bytes": sum((r["remaining_bytes"] or 0) for r in results),
    },
    "can_resume": True,  # snapshot_download uses HF cache and resumes
}

print(json.dumps(summary, indent=2))
