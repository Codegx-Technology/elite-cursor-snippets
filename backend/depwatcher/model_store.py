import os
import hashlib
from pathlib import Path
from typing import Optional, Tuple
import logging
from huggingface_hub import snapshot_download, HfApi, HfHub
from huggingface_hub.utils import HfHubDisabled, EntryNotFoundError
import sys

logger = logging.getLogger(__name__)

def hf_cache_root() -> Path:
    """Determines the Hugging Face cache root, handling Windows specifics."""
    # HF_HOME environment variable takes precedence
    hf_home = os.getenv("HF_HOME")
    if hf_home:
        return Path(hf_home).resolve()
    
    # Default cache location
    if sys.platform == "win32":
        return Path(os.path.expanduser("~")) / ".cache" / "huggingface"
    else:
        return Path(os.path.expanduser("~")) / ".cache" / "huggingface"

def calculate_file_hash(filepath: Path, hash_algo='sha256', chunk_size=8192):
    """Calculates the hash of a file."""
    hasher = hashlib.new(hash_algo)
    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

async def is_model_present(provider: str, model_id: str, revision: Optional[str] = None, local_path: Optional[Path] = None) -> bool:
    """
    Checks if a model is present locally.
    For Hugging Face, checks the cache. For local_path, checks existence.
    """
    if provider == "huggingface":
        try:
            # Use HfApi to check if the model exists in the cache without downloading
            # This is a more robust check than just looking at the directory
            repo_info = HfApi().repo_info(model_id, revision=revision, token=os.getenv("HF_TOKEN"))
            
            # Check if the model is actually downloaded in the cache
            # This is a heuristic, a more robust check would involve checking specific files
            cache_path = HfHub.cached_repo_path(repo_id=model_id, revision=revision)
            if Path(cache_path).exists() and any(Path(cache_path).iterdir()):
                logger.info(f"Hugging Face model {model_id} (revision: {revision or 'main'}) found in cache.")
                return True
            else:
                logger.info(f"Hugging Face model {model_id} (revision: {revision or 'main'}) not fully cached.")
                return False
        except (EntryNotFoundError, HfHubDisabled):
            logger.warning(f"Hugging Face model {model_id} not found on Hub or Hub disabled.")
            return False
        except Exception as e:
            logger.error(f"Error checking Hugging Face model {model_id}: {e}")
            return False
    elif provider == "local_path" and local_path:
        if local_path.exists():
            logger.info(f"Local model found at: {local_path}")
            return True
        else:
            logger.info(f"Local model not found at: {local_path}")
            return False
    else:
        logger.warning(f"Unsupported model provider: {provider}")
        return False

async def fetch_model(provider: str, model_id: str, revision: Optional[str] = None, local_dir: Optional[Path] = None) -> Tuple[bool, float]:
    """
    Fetches a model from the specified provider.
    Returns (downloaded: bool, sizeMB: float).
    """
    downloaded = False
    size_mb = 0.0

    if provider == "huggingface":
        try:
            logger.info(f"Attempting to download Hugging Face model: {model_id} (revision: {revision or 'main'})")
            # snapshot_download is idempotent and uses the cache
            local_path = snapshot_download(repo_id=model_id, revision=revision, cache_dir=str(hf_cache_root()))
            
            # Calculate size of the downloaded model
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(local_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp): # Avoid double counting symlinks
                        total_size += os.path.getsize(fp)
            size_mb = round(total_size / (1024 * 1024), 2)
            downloaded = True
            logger.info(f"Successfully downloaded/verified Hugging Face model {model_id}. Size: {size_mb} MB")
        except Exception as e:
            logger.error(f"Failed to download Hugging Face model {model_id}: {e}")
            downloaded = False
    elif provider == "local_path" and local_dir:
        # For local_path, we just ensure the directory exists
        local_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured local model directory exists: {local_dir}")
        downloaded = True # Considered "downloaded" if path is ensured
        # Size calculation for local_path is more complex, might need to iterate files
        # For now, return 0.0 or implement a more robust size calculation if needed.
    else:
        logger.warning(f"Unsupported model provider for fetching: {provider}")
        downloaded = False
    
    return downloaded, size_mb
