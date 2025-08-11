import os
import asyncio
import aiohttp
import hashlib
from pathlib import Path
from logging_setup import get_logger
from config_loader import get_config

logger = get_logger(__name__)
config = get_config()

class AssetManager:
    """
    // [TASK]: Manage high-performance asset loading with caching and integrity checks
    // [GOAL]: Centralize asset management for models, images, and weights
    """
    def __init__(self):
        self.cache_dir = Path("asset_cache")
        self.cache_dir.mkdir(exist_ok=True)
        logger.info(f"AssetManager initialized. Cache directory: {self.cache_dir}")

    async def _download_asset(self, url: str, destination_path: Path) -> bool:
        """
        // [TASK]: Download an asset asynchronously
        // [GOAL]: Support CDN fallback and signed URLs (conceptual)
        // [TODO]: Implement actual CDN fallback logic and signed URL handling.
        """
        logger.info(f"Attempting to download asset from: {url} to {destination_path}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status() # Raise an exception for bad status codes
                    with open(destination_path, 'wb') as f:
                        while True:
                            chunk = await response.content.read(8192)
                            if not chunk:
                                break
                            f.write(chunk)
            logger.info(f"✅ Successfully downloaded asset: {destination_path}")
            return True
        except aiohttp.ClientError as e:
            logger.error(f"❌ Failed to download asset from {url}: {e}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during download from {url}: {e}")
            return False

    def _calculate_checksum(self, file_path: Path, algorithm='sha256') -> str:
        """
        // [TASK]: Calculate checksum of a file
        // [GOAL]: Ensure model integrity
        """
        hasher = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()

    async def get_asset(self, asset_id: str, url: str, expected_checksum: str = None, version: str = "latest") -> Path:
        """
        // [TASK]: Get an asset, prioritizing cache and handling downloads
        // [GOAL]: Provide cached or newly downloaded assets with integrity checks
        // [TODO]: Implement sophisticated async lazy-loading for models not immediately required.
        """
        asset_filename = f"{asset_id}_{version}_{os.path.basename(url)}"
        local_path = self.cache_dir / asset_filename

        if local_path.exists():
            logger.info(f"Asset {asset_id} found in cache: {local_path}")
            if expected_checksum:
                calculated_checksum = self._calculate_checksum(local_path)
                if calculated_checksum == expected_checksum:
                    logger.info(f"✅ Checksum verified for cached asset: {asset_id}")
                    return local_path
                else:
                    logger.warning(f"❌ Checksum mismatch for cached asset {asset_id}. Recalculating...")
                    os.remove(local_path) # Invalidate cache
            else:
                logger.info(f"Checksum not provided for {asset_id}. Using cached version.")
                return local_path

        # Download if not in cache or checksum mismatch
        logger.info(f"Asset {asset_id} not in cache or checksum mismatch. Downloading...")
        start_time = asyncio.get_event_loop().time()
        download_success = await self._download_asset(url, local_path)
        end_time = asyncio.get_event_loop().time()
        load_time = end_time - start_time
        logger.info(f"Asset {asset_id} downloaded in {load_time:.2f} seconds.")

        if download_success:
            if expected_checksum:
                calculated_checksum = self._calculate_checksum(local_path)
                if calculated_checksum != expected_checksum:
                    logger.error(f"❌ Checksum mismatch after download for {asset_id}. Deleting corrupted file.")
                    os.remove(local_path)
                    log_and_raise(ValueError(f"Checksum mismatch for {asset_id} after download."), "Asset integrity compromised")
            logger.info(f"✅ Asset {asset_id} ready at: {local_path}")
            return local_path
        else:
            log_and_raise(IOError(f"Failed to download asset {asset_id} from {url}"), "Asset download failed")

# Example usage (conceptual)
async def main():
    asset_manager = AssetManager()
    
    # Example: Download a dummy file
    dummy_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    dummy_checksum = "c291b1a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0" # Placeholder checksum
    
    try:
        # This will download and cache the image
        asset_path = await asset_manager.get_asset("google_logo", dummy_url, dummy_checksum, version="1.0")
        logger.info(f"Google logo asset path: {asset_path}")

        # This will retrieve from cache
        asset_path = await asset_manager.get_asset("google_logo", dummy_url, dummy_checksum, version="1.0")
        logger.info(f"Google logo asset path (from cache): {asset_path}")

    except Exception as e:
        logger.error(f"Error in asset manager example: {e}")

if __name__ == "__main__":
    asyncio.run(main())
