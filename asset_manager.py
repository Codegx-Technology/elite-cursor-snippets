import os
import asyncio
import aiohttp
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
import logging
import boto3
from botocore.exceptions import ClientError
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
        self.storage_provider = config.storage.provider
        self.s3_client = self._get_s3_client() if self.storage_provider == "s3" else None
        self.cdn_endpoints = config.app.cdn_endpoints or []
        self.last_used_cdn_index = 0
        logger.info(f"AssetManager initialized. Cache directory: {self.cache_dir}")

    def _get_s3_client(self):
        # [SNIPPET]: thinkwithai + kenyafirst + enterprise-secure
        # [CONTEXT]: Creating an S3 client for asset management.
        # [GOAL]: Securely connect to S3 for asset operations.
        # [TASK]: Initialize and return a boto3 S3 client.
        try:
            return boto3.client(
                's3',
                region_name=config.storage.s3.region_name,
                aws_access_key_id=config.storage.s3.access_key_id,
                aws_secret_access_key=config.storage.s3.secret_access_key
            )
        except Exception as e:
            logger.error(f"Failed to create S3 client: {e}")
            return None

    def generate_signed_url(self, asset_key: str) -> Optional[str]:
        # [SNIPPET]: thinkwithai + kenyafirst + enterprise-secure
        # [CONTEXT]: Generating a signed URL for an S3 asset.
        # [GOAL]: Provide secure, time-limited access to assets.
        # [TASK]: Generate and return a presigned URL for a given asset key.
        if self.storage_provider != "s3" or not self.s3_client:
            return None

        try:
            return self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': config.storage.s3.bucket_name, 'Key': asset_key},
                ExpiresIn=config.storage.s3.signed_url_expiry
            )
        except ClientError as e:
            logger.error(f"Failed to generate signed URL for {asset_key}: {e}")
            return None

    async def _download_asset(self, url: str, destination_path: Path, signed_url: Optional[str] = None) -> bool:
        """
        // [TASK]: Download an asset asynchronously with CDN fallback and signed URLs
        // [GOAL]: Support round-robin CDN fallback and signed URLs
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        urls_to_try = []
        if signed_url:
            urls_to_try.append(signed_url)

        # Add CDN endpoints for fallback in a round-robin fashion
        if self.cdn_endpoints:
            for i in range(len(self.cdn_endpoints)):
                cdn_index = (self.last_used_cdn_index + i) % len(self.cdn_endpoints)
                cdn_base_url = self.cdn_endpoints[cdn_index]
                asset_name = os.path.basename(url)
                cdn_url = f"{cdn_base_url.rstrip('/')}/{asset_name}"
                urls_to_try.append(cdn_url)

        urls_to_try.append(url) # Always try the original URL as a last resort

        for i, current_url in enumerate(urls_to_try):
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
                # Update the last used CDN index if a CDN was successful
                if i > 0 and i < len(self.cdn_endpoints) + 1:
                    self.last_used_cdn_index = (self.last_used_cdn_index + i) % len(self.cdn_endpoints)
                return True
            except aiohttp.ClientError as e:
                logger.error(f"❌ Failed to download asset from {current_url}: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred during download from {current_url}: {e}")
        
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

    async def get_asset(self, asset_id: str, url: str, expected_checksum: str = None, version: str = "latest", lazy_load: bool = False) -> Path | LazyAsset:
        """
        // [TASK]: Get an asset, prioritizing cache and handling downloads
        // [GOAL]: Provide cached or newly downloaded assets with integrity checks and signed URLs
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        signed_url = None
        if self.storage_provider == "s3":
            # Assuming the 'url' is the asset key in the S3 bucket
            asset_key = url
            signed_url = self.generate_signed_url(asset_key)

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
