import os
import sys
from pathlib import Path
from typing import List, Tuple

from huggingface_hub import snapshot_download

MODELS_DIR = Path(os.environ.get("MODELS_DIR", "./models")).resolve()
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Core models used by the project
HF_MODELS: List[Tuple[str, str]] = [
    ("stabilityai/sdxl-turbo", "sdxl-turbo"),
    ("runwayml/stable-diffusion-inpainting", "sd_inpaint"),
    ("facebook/sam-vit-base", "sam"),
    ("saic-mdal/lama", "lama"),
]


def is_cached(repo_id: str, subdir: str) -> bool:
    """Return True if the repo appears cached locally in our models dir."""
    target = MODELS_DIR / subdir
    # Try an HF local-only probe first
    try:
        snapshot_download(repo_id=repo_id, cache_dir=str(target), local_files_only=True)
        return True
    except Exception:
        # Not present locally
        return target.exists() and any(target.iterdir())


def ensure_model(repo_id: str, subdir: str) -> bool:
    """Download model if missing. Returns True if available after this call."""
    target = MODELS_DIR / subdir
    target.mkdir(parents=True, exist_ok=True)

    if is_cached(repo_id, subdir):
        print(f"✅ Cached: {repo_id} -> {target}")
        return True

    print(f"⬇️  Downloading: {repo_id} -> {target}")
    try:
        snapshot_download(repo_id=repo_id, cache_dir=str(target), local_files_only=False)
        print(f"✅ Downloaded: {repo_id}")
        return True
    except Exception as e:
        # Be broad to support multiple huggingface_hub versions without specific exception class
        print(f"❌ Failed: {repo_id} — {e}")
    return False


def check_whisper() -> None:
    """Best-effort Whisper check/download for base model if whisper is installed."""
    try:
        import whisper  # type: ignore
    except Exception:
        print("ℹ️  Whisper not installed; skipping Whisper model.")
        return

    try:
        # Use default cache root inside our MODELS_DIR
        whisper_dir = MODELS_DIR / "whisper"
        whisper_dir.mkdir(parents=True, exist_ok=True)
        print("🔍 Checking Whisper 'base' model...")
        # This call will download if missing
        _ = whisper.load_model("base", download_root=str(whisper_dir))
        print(f"✅ Whisper 'base' available at {whisper_dir}")
    except Exception as e:
        print(f"❌ Whisper check/download failed: {e}")


def main():
    print(f"Models directory: {MODELS_DIR}")
    all_ok = True

    for repo_id, subdir in HF_MODELS:
        ok = ensure_model(repo_id, subdir)
        all_ok = all_ok and ok

    check_whisper()

    print("\nSummary:")
    for repo_id, subdir in HF_MODELS:
        status = "present" if is_cached(repo_id, subdir) else "missing"
        print(f" - {subdir:12s}: {status}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
