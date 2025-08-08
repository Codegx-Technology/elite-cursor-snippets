#!/usr/bin/env python3
"""
🎬 Media Utils - Combo Pack D Helper Functions
Audio mixing, subtitle burning, vertical padding, and scene video creation

// [TASK]: Create comprehensive media utilities for Combo Pack D
// [GOAL]: FFmpeg-based audio/video processing with TikTok/WhatsApp support
// [SNIPPET]: surgicalfix + refactorclean + kenyafirst
// [CONTEXT]: Elite video generation pipeline utilities
"""

import subprocess
import os
import logging
from pathlib import Path
from typing import Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MediaUtils:
    """Professional media processing utilities for Combo Pack D"""
    
    def __init__(self):
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        logger.info("[MEDIA] Media utilities initialized")
    
    def mix_audio(self, narration_path: str, music_path: str, out_path: str, 
                  music_vol: float = 0.3, narration_vol: float = 1.0) -> bool:
        """
        Mix narration and background music with volume control
        
        Args:
            narration_path: Path to narration audio file
            music_path: Path to background music file  
            out_path: Output path for mixed audio
            music_vol: Background music volume (0-1)
            narration_vol: Narration volume (0-1)
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[AUDIO] Mixing narration + music → {out_path}")
            
            # Ensure input files exist
            if not os.path.exists(narration_path):
                logger.error(f"[AUDIO] Narration file not found: {narration_path}")
                return False
                
            if not os.path.exists(music_path):
                logger.error(f"[AUDIO] Music file not found: {music_path}")
                return False
            
            # FFmpeg command for audio mixing
            cmd = [
                "ffmpeg", "-y",
                "-i", narration_path,
                "-i", music_path,
                "-filter_complex",
                f"[0:a]volume={narration_vol}[n];[1:a]volume={music_vol}[m];[n][m]amix=inputs=2:duration=shortest:dropout_transition=2[a]",
                "-map", "[a]",
                "-c:a", "aac",
                "-b:a", "192k",
                out_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"[AUDIO] ✅ Audio mixing successful")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"[AUDIO] ❌ Audio mixing failed: {e}")
            logger.error(f"[AUDIO] FFmpeg error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"[AUDIO] ❌ Unexpected error: {e}")
            return False

    def burn_subtitles(self, video_in: str, srt_path: str, video_out: str,
                      font_size: int = 36, font_name: str = "Arial") -> bool:
        """
        Burn subtitles into video using FFmpeg
        
        Args:
            video_in: Input video path
            srt_path: SRT subtitle file path
            video_out: Output video path
            font_size: Subtitle font size
            font_name: Subtitle font name
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[SUBTITLES] Burning subtitles → {video_out}")
            
            # Ensure input files exist
            if not os.path.exists(video_in):
                logger.error(f"[SUBTITLES] Video file not found: {video_in}")
                return False
                
            if not os.path.exists(srt_path):
                logger.error(f"[SUBTITLES] SRT file not found: {srt_path}")
                return False
            
            # Escape the SRT path for FFmpeg
            srt_escaped = srt_path.replace("\\", "/").replace(":", "\\:")
            
            # FFmpeg command for subtitle burning
            cmd = [
                "ffmpeg", "-y",
                "-i", video_in,
                "-vf", f"subtitles={srt_escaped}:force_style='FontName={font_name},FontSize={font_size},PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2'",
                "-c:a", "copy",
                video_out
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"[SUBTITLES] ✅ Subtitle burning successful")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"[SUBTITLES] ❌ Subtitle burning failed: {e}")
            logger.error(f"[SUBTITLES] FFmpeg error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"[SUBTITLES] ❌ Unexpected error: {e}")
            return False

    def vertical_pad_image_for_tiktok(self, img_in: str, img_out: str, 
                                     target_size: Tuple[int, int] = (1080, 1920)) -> bool:
        """
        Create vertical TikTok-ready image with proper padding
        
        Args:
            img_in: Input image path
            img_out: Output image path
            target_size: Target dimensions (width, height)
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[TIKTOK] Creating vertical image → {img_out}")
            
            if not os.path.exists(img_in):
                logger.error(f"[TIKTOK] Image file not found: {img_in}")
                return False
            
            width, height = target_size
            
            # FFmpeg command for vertical padding
            cmd = [
                "ffmpeg", "-y",
                "-i", img_in,
                "-vf", f"scale='min({width},iw)':'min({height},ih)':force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black",
                "-q:v", "2",
                img_out
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"[TIKTOK] ✅ Vertical image creation successful")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"[TIKTOK] ❌ Vertical image creation failed: {e}")
            logger.error(f"[TIKTOK] FFmpeg error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"[TIKTOK] ❌ Unexpected error: {e}")
            return False

    def make_scene_video(self, img_path: str, audio_path: str, out_mp4: str, 
                        duration: Optional[float] = None) -> bool:
        """
        Create MP4 video from image + audio
        
        Args:
            img_path: Input image path
            audio_path: Input audio path
            out_mp4: Output video path
            duration: Optional duration override
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[SCENE] Creating scene video → {out_mp4}")
            
            # Ensure input files exist
            if not os.path.exists(img_path):
                logger.error(f"[SCENE] Image file not found: {img_path}")
                return False
                
            if not os.path.exists(audio_path):
                logger.error(f"[SCENE] Audio file not found: {audio_path}")
                return False
            
            # Build FFmpeg command
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", img_path,
                "-i", audio_path,
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest"
            ]
            
            # Add duration if specified
            if duration:
                cmd.extend(["-t", str(duration)])
            
            cmd.append(out_mp4)
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"[SCENE] ✅ Scene video creation successful")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"[SCENE] ❌ Scene video creation failed: {e}")
            logger.error(f"[SCENE] FFmpeg error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"[SCENE] ❌ Unexpected error: {e}")
            return False

    def create_whatsapp_preset(self, input_video: str, output_video: str) -> bool:
        """
        Create WhatsApp-optimized video (720x1280, <16MB)
        
        Args:
            input_video: Input video path
            output_video: Output video path
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[WHATSAPP] Creating WhatsApp preset → {output_video}")
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-vf", "scale=720:1280",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "28",
                "-b:v", "800k",
                "-c:a", "aac",
                "-b:a", "96k",
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"[WHATSAPP] ✅ WhatsApp preset creation successful")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"[WHATSAPP] ❌ WhatsApp preset creation failed: {e}")
            return False

    def create_tiktok_preset(self, input_video: str, output_video: str) -> bool:
        """
        Create TikTok-optimized video (1080x1920, <287MB)
        
        Args:
            input_video: Input video path
            output_video: Output video path
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[TIKTOK] Creating TikTok preset → {output_video}")
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-vf", "scale=1080:1920",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                "-b:v", "2500k",
                "-c:a", "aac",
                "-b:a", "128k",
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"[TIKTOK] ✅ TikTok preset creation successful")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"[TIKTOK] ❌ TikTok preset creation failed: {e}")
            return False
