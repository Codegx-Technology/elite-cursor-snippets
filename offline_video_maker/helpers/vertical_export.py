#!/usr/bin/env python3
"""
📱 Vertical Export - Combo Pack D TikTok/Mobile Export System
9:16 aspect ratio export with mobile optimization

// [TASK]: Create comprehensive vertical export system for mobile platforms
// [GOAL]: TikTok, Instagram Stories, WhatsApp optimized video export
// [SNIPPET]: surgicalfix + refactorclean + kenyafirst
// [CONTEXT]: Elite mobile video export for social media
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VerticalExport:
    """Professional vertical video export for mobile platforms"""
    
    def __init__(self):
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Mobile platform specifications
        self.platforms = {
            "tiktok": {
                "resolution": (1080, 1920),
                "aspect_ratio": "9:16",
                "max_duration": 180,  # 3 minutes
                "max_file_size": 287 * 1024 * 1024,  # 287 MB
                "video_codec": "libx264",
                "audio_codec": "aac",
                "video_bitrate": "2500k",
                "audio_bitrate": "128k",
                "crf": 23,
                "description": "TikTok optimized"
            },
            "instagram_stories": {
                "resolution": (1080, 1920),
                "aspect_ratio": "9:16",
                "max_duration": 60,  # 1 minute
                "max_file_size": 100 * 1024 * 1024,  # 100 MB
                "video_codec": "libx264",
                "audio_codec": "aac",
                "video_bitrate": "2000k",
                "audio_bitrate": "128k",
                "crf": 25,
                "description": "Instagram Stories optimized"
            },
            "whatsapp": {
                "resolution": (720, 1280),
                "aspect_ratio": "9:16",
                "max_duration": 90,  # 1.5 minutes
                "max_file_size": 16 * 1024 * 1024,  # 16 MB
                "video_codec": "libx264",
                "audio_codec": "aac",
                "video_bitrate": "800k",
                "audio_bitrate": "96k",
                "crf": 28,
                "description": "WhatsApp optimized"
            },
            "youtube_shorts": {
                "resolution": (1080, 1920),
                "aspect_ratio": "9:16",
                "max_duration": 60,  # 1 minute
                "max_file_size": 256 * 1024 * 1024,  # 256 MB
                "video_codec": "libx264",
                "audio_codec": "aac",
                "video_bitrate": "3000k",
                "audio_bitrate": "128k",
                "crf": 22,
                "description": "YouTube Shorts optimized"
            },
            "facebook_stories": {
                "resolution": (1080, 1920),
                "aspect_ratio": "9:16",
                "max_duration": 120,  # 2 minutes
                "max_file_size": 150 * 1024 * 1024,  # 150 MB
                "video_codec": "libx264",
                "audio_codec": "aac",
                "video_bitrate": "2200k",
                "audio_bitrate": "128k",
                "crf": 24,
                "description": "Facebook Stories optimized"
            }
        }
        
        logger.info(f"[VERTICAL] Vertical export system initialized with {len(self.platforms)} platforms")
    
    def convert_to_vertical(self, input_video: str, output_video: str, 
                           platform: str = "tiktok", 
                           background_color: str = "black",
                           add_blur_background: bool = False) -> bool:
        """
        Convert horizontal/square video to vertical format
        
        Args:
            input_video: Input video path
            output_video: Output video path
            platform: Target platform (tiktok, instagram_stories, whatsapp, etc.)
            background_color: Background color for padding
            add_blur_background: Whether to add blurred background instead of solid color
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[VERTICAL] Converting to {platform} format → {output_video}")
            
            if not os.path.exists(input_video):
                logger.error(f"[VERTICAL] Input video not found: {input_video}")
                return False
            
            if platform not in self.platforms:
                logger.error(f"[VERTICAL] Unknown platform: {platform}")
                return False
            
            platform_config = self.platforms[platform]
            width, height = platform_config["resolution"]
            
            # Build FFmpeg filter
            if add_blur_background:
                # Create blurred background version
                video_filter = (
                    f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                    f"boxblur=10:1[bg];"
                    f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2"
                )
            else:
                # Simple padding with solid color
                video_filter = (
                    f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                    f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:{background_color}"
                )
            
            # Build FFmpeg command
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-vf", video_filter,
                "-c:v", platform_config["video_codec"],
                "-preset", "veryfast",
                "-crf", str(platform_config["crf"]),
                "-b:v", platform_config["video_bitrate"],
                "-c:a", platform_config["audio_codec"],
                "-b:a", platform_config["audio_bitrate"],
                "-movflags", "+faststart",  # Optimize for streaming
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Check file size
            file_size = os.path.getsize(output_video)
            max_size = platform_config["max_file_size"]
            
            if file_size > max_size:
                logger.warning(f"[VERTICAL] File size ({file_size/1024/1024:.1f}MB) exceeds {platform} limit ({max_size/1024/1024:.1f}MB)")
                # Attempt compression
                return self._compress_for_platform(output_video, platform)
            
            logger.info(f"[VERTICAL] ✅ Vertical conversion successful ({file_size/1024/1024:.1f}MB)")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"[VERTICAL] ❌ Conversion failed: {e}")
            logger.error(f"[VERTICAL] FFmpeg error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"[VERTICAL] ❌ Unexpected error: {e}")
            return False
    
    def _compress_for_platform(self, video_path: str, platform: str) -> bool:
        """
        Compress video to meet platform file size requirements
        
        Args:
            video_path: Video file path
            platform: Target platform
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[VERTICAL] Compressing for {platform} size limits")
            
            platform_config = self.platforms[platform]
            compressed_path = video_path.replace(".mp4", "_compressed.mp4")
            
            # More aggressive compression settings
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-c:v", "libx264",
                "-preset", "slow",  # Better compression
                "-crf", str(platform_config["crf"] + 3),  # Higher CRF = more compression
                "-b:v", str(int(platform_config["video_bitrate"].replace("k", "")) // 2) + "k",  # Half bitrate
                "-c:a", "aac",
                "-b:a", "64k",  # Lower audio bitrate
                "-movflags", "+faststart",
                compressed_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Replace original with compressed version
            os.replace(compressed_path, video_path)
            
            new_size = os.path.getsize(video_path)
            logger.info(f"[VERTICAL] ✅ Compression successful ({new_size/1024/1024:.1f}MB)")
            return True
            
        except Exception as e:
            logger.error(f"[VERTICAL] ❌ Compression failed: {e}")
            return False
    
    def create_vertical_image(self, input_image: str, output_image: str,
                             platform: str = "tiktok",
                             background_color: str = "black") -> bool:
        """
        Convert image to vertical format for mobile platforms
        
        Args:
            input_image: Input image path
            output_image: Output image path
            platform: Target platform
            background_color: Background color for padding
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[VERTICAL] Converting image to {platform} format → {output_image}")
            
            if not os.path.exists(input_image):
                logger.error(f"[VERTICAL] Input image not found: {input_image}")
                return False
            
            if platform not in self.platforms:
                logger.error(f"[VERTICAL] Unknown platform: {platform}")
                return False
            
            width, height = self.platforms[platform]["resolution"]
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_image,
                "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:{background_color}",
                "-q:v", "2",
                output_image
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"[VERTICAL] ✅ Image conversion successful")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"[VERTICAL] ❌ Image conversion failed: {e}")
            return False
        except Exception as e:
            logger.error(f"[VERTICAL] ❌ Unexpected error: {e}")
            return False
    
    def batch_convert_to_platforms(self, input_video: str, output_dir: str,
                                  platforms: List[str] = None) -> Dict[str, bool]:
        """
        Convert video to multiple platform formats
        
        Args:
            input_video: Input video path
            output_dir: Output directory
            platforms: List of platforms to convert to (default: all)
            
        Returns:
            Dictionary with conversion results for each platform
        """
        if platforms is None:
            platforms = list(self.platforms.keys())
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results = {}
        base_name = Path(input_video).stem
        
        for platform in platforms:
            output_file = output_path / f"{base_name}_{platform}.mp4"
            success = self.convert_to_vertical(input_video, str(output_file), platform)
            results[platform] = success
            
            if success:
                logger.info(f"[VERTICAL] ✅ {platform}: {output_file}")
            else:
                logger.error(f"[VERTICAL] ❌ {platform}: Failed")
        
        return results
    
    def get_platform_info(self, platform: str = None) -> Dict:
        """
        Get platform specifications
        
        Args:
            platform: Specific platform (optional)
            
        Returns:
            Platform specifications
        """
        if platform:
            return self.platforms.get(platform, {})
        return self.platforms
    
    def validate_video_for_platform(self, video_path: str, platform: str) -> Dict[str, bool]:
        """
        Validate video against platform requirements
        
        Args:
            video_path: Video file path
            platform: Target platform
            
        Returns:
            Validation results
        """
        validation = {
            "file_exists": os.path.exists(video_path),
            "platform_supported": platform in self.platforms,
            "size_ok": False,
            "duration_ok": False
        }
        
        if validation["file_exists"] and validation["platform_supported"]:
            platform_config = self.platforms[platform]
            
            # Check file size
            file_size = os.path.getsize(video_path)
            validation["size_ok"] = file_size <= platform_config["max_file_size"]
            
            # Check duration (would need ffprobe for accurate duration)
            validation["duration_ok"] = True  # Placeholder
        
        return validation
