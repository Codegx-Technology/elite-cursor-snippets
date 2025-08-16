import os
import asyncio
import aiohttp
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
import logging
from config_loader import get_config

# Use standard logging to avoid circular import with logging_setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
config = get_config()

class LazyAsset:
    """
    Represents an asset that is loaded lazily (on demand).
    When awaited, it triggers the actual download and returns the asset's local path.
    """
    def __init__(self, asset_manager: 'AssetManager', asset_id: str, url: str, expected_checksum: Optional[str] = None, version: str = "latest", signed_url: Optional[str] = None):
        self._asset_manager = asset_manager
        self._asset_id = asset_id
        self._url = url
        self._expected_checksum = expected_checksum
        self._version = version
        self._signed_url = signed_url
        self._local_path: Optional[Path] = None
        self._load_task: Optional[asyncio.Task] = None

    async def load(self) -> Path:
        """Triggers the actual download and returns the local path."""
        if self._local_path:
            logger.info(f"Lazy asset {self._asset_id} already loaded from {self._local_path}.")
            return self._local_path
        
        if self._load_task is None:
            logger.info(f"Initiating lazy load for asset {self._asset_id} from {self._url}.")
            self._load_task = asyncio.create_task(
                self._asset_manager._perform_get_asset(
                    self._asset_id, self._url, self._expected_checksum, self._version, self._signed_url, is_lazy_load=True
                )
            )
        
        self._local_path = await self._load_task
        return self._local_path

    def __await__(self):
        return self.load().__await__()

    def __str__(self):
        return f"LazyAsset(id={self._asset_id}, url={self._url}, loaded={self._local_path is not None})"

    def __repr__(self):
        return self.__str__()

# Use standard logging to avoid circular import with logging_setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
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

    async def _download_asset(self, url: str, destination_path: Path, signed_url: Optional[str] = None) -> bool:
        """
        // [TASK]: Download an asset asynchronously with CDN fallback and signed URLs
        // [GOAL]: Support CDN fallback and signed URLs (conceptual)
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        urls_to_try = []
        if signed_url:
            urls_to_try.append(signed_url)
        urls_to_try.append(url) # Always try the original URL first

        # Add CDN endpoints for fallback
        cdn_endpoints = config.get('app', {}).get('cdn_endpoints', [])
        for cdn_base_url in cdn_endpoints:
            # Construct the full CDN URL. Assuming 'url' is a relative path or filename.
            # If 'url' is an absolute URL, we'll extract its basename.
            asset_name = os.path.basename(url)
            cdn_url = f"{cdn_base_url.rstrip('/')}/{asset_name}"
            urls_to_try.append(cdn_url)
        
        for current_url in urls_to_try:
            if not current_url:
                continue
            logger.info(f"Attempting to download asset from: {current_url} to {destination_path}")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(current_url) as response:
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
                logger.error(f"❌ Failed to download asset from {current_url}: {e}")
                # Try next URL in list if it's a CDN fallback scenario
            except Exception as e:
                logger.error(f"An unexpected error occurred during download from {current_url}: {e}")
                # Try next URL in list if it's a CDN fallback scenario
        
        return False # All download attempts failed

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

    async def _perform_get_asset(self, asset_id: str, url: str, expected_checksum: str = None, version: str = "latest", signed_url: Optional[str] = None, is_lazy_load: bool = False) -> Path:
        """
        Internal method to perform the actual asset retrieval (from cache or download).
        Used by get_asset and LazyAsset.
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
        download_success = await self._download_asset(url, local_path, signed_url) # Pass signed_url
        end_time = asyncio.get_event_loop().time()
        load_time = end_time - start_time
        logger.info(f"Asset {asset_id} downloaded in {load_time:.2f} seconds.")

        if download_success:
            if expected_checksum:
                calculated_checksum = self._calculate_checksum(local_path)
                if calculated_checksum != expected_checksum:
                    logger.error(f"❌ Checksum mismatch after download for {asset_id}. Deleting corrupted file.")
                    os.remove(local_path)
                    raise ValueError(f"Checksum mismatch for {asset_id} after download.") # Fallback if log_and_raise not defined
            logger.info(f"✅ Asset {asset_id} ready at: {local_path}")
            return local_path
        else:
            raise IOError(f"Failed to download asset {asset_id} from {url}")

    async def get_asset(self, asset_id: str, url: str, expected_checksum: str = None, version: str = "latest", signed_url: Optional[str] = None, lazy_load: bool = False) -> Path | LazyAsset:
        """
        // [TASK]: Get an asset, prioritizing cache and handling downloads
        // [GOAL]: Provide cached or newly downloaded assets with integrity checks
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        if lazy_load:
            logger.info(f"Asset {asset_id} marked for lazy loading. Returning LazyAsset object.")
            return LazyAsset(self, asset_id, url, expected_checksum, version, signed_url)
        
        return await self._perform_get_asset(asset_id, url, expected_checksum, version, signed_url)

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
