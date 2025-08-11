#!/usr/bin/env python3
"""
🎨 Cartoon/Anime Pipeline - African Animation Studio
Lightweight, CPU-friendly pipeline for cartoon/anime videos with African identity

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + surgicalfix
// [CONTEXT]: Separate cartoon/anime pipeline with African cultural elements
// [GOAL]: CPU-friendly animation with Sheng/Kiswahili TTS and mobile exports
"""

import cv2
import numpy as np
from pathlib import Path
import time
import json
import subprocess
from typing import List, Dict, Optional
import io
from PIL import Image

from config_loader import get_config
from ai_model_manager import generate_image, text_to_speech
from error_utils import log_and_raise, retry_on_exception

config = get_config()

class AfricanCartoonPipeline:
    """
    🎨 African Cartoon/Anime Video Generator
    
    Features:
    - CPU-friendly cartoon generation
    - African cultural elements
    - Sheng/Kiswahili TTS support
    - Mobile export presets
    - Batch processing from CSV
    """
    
    def __init__(self):
        self.output_folder = Path("cartoon_studio")
        self.output_folder.mkdir(exist_ok=True)
        
        # Animation settings
        self.fps = 24  # Standard animation FPS
        self.width = 1280
        self.height = 720
        
        # Cartoon style presets
        self.cartoon_styles = {
            "african_cartoon": {
                "base_prompt": "African cartoon style, vibrant colors, traditional attire, beautiful landscapes",
                "negative": "realistic, photographic, dark, gloomy"
            },
            "anime": {
                "base_prompt": "anime style, manga art, colorful, expressive characters",
                "negative": "realistic, western cartoon, 3D"
            },
            "kenyan_animation": {
                "base_prompt": "Kenyan animation style, Maasai patterns, savanna background, cultural clothing",
                "negative": "western style, modern city, foreign elements"
            }
        }
        
        # TTS language options
        self.tts_languages = {
            "sheng_male": {"lang": "sw", "voice": "male", "speed": 1.0},
            "sheng_female": {"lang": "sw", "voice": "female", "speed": 1.0},
            "kiswahili": {"lang": "sw", "voice": "neutral", "speed": 0.9},
            "english_news": {"lang": "en", "voice": "news", "speed": 1.1}
        }
        
        # Mobile export presets
        self.export_presets = {
            "tiktok": {"width": 720, "height": 1280, "fps": 30, "duration": 60},
            "whatsapp": {"width": 720, "height": 720, "fps": 24, "duration": 30},
            "youtube_shorts": {"width": 720, "height": 1280, "fps": 30, "duration": 60},
            "instagram_reel": {"width": 720, "height": 1280, "fps": 30, "duration": 30}
        }
        
        logger.info("🎨 AFRICAN CARTOON PIPELINE INITIALIZED")
        logger.info(f"📁 Studio folder: {self.output_folder.absolute()}")
        logger.info(f"🎬 Styles: {list(self.cartoon_styles.keys())}")
        logger.info(f"🎤 Languages: {list(self.tts_languages.keys())}")
        logger.info(f"📱 Export presets: {list(self.export_presets.keys())}")
    
    @retry_on_exception()
    def load_cartoon_model(self, style: str = "african_cartoon"):
        """
        // [TASK]: Load appropriate model for cartoon generation using ai_model_manager
        // [GOAL]: Centralize model loading and leverage fallback mechanisms
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        try:
            logger.info(f"🤖 Loading cartoon model for {style}...")
            # This pipeline will use ai_model_manager for image generation, so no direct pipeline loading here.
            # We just need to ensure the model path is configured.
            model_path = config.models.image_generation.local_fallback_path
            if not model_path:
                log_and_raise(ValueError("Local image generation model path not configured in config.yaml"), "Cartoon model loading failed")
            logger.info(f"✅ Cartoon model configured to use: {model_path}")
            return True # Indicate that the model is configured
            
        except Exception as e:
            log_and_raise(e, f"Cartoon model loading failed")
    
    @retry_on_exception()
    def break_script_into_scenes(self, script: str) -> List[Dict]:
        """Break script into cartoon scenes with dialogue"""
        
        logger.info("📝 Breaking script into cartoon scenes...")
        
        # Simple scene breakdown (in production, use GPT)
        sentences = script.split('. ')
        scenes = []
        
        for i, sentence in enumerate(sentences[:5]):  # Limit to 5 scenes
            if sentence.strip():
                scene = {
                    "id": i + 1,
                    "dialogue": sentence.strip() + ".",
                    "visual_description": f"African cartoon scene {i+1}: {sentence[:50]}...",
                    "duration": 3.0,  # 3 seconds per scene
                    "character_emotion": "happy" if i % 2 == 0 else "thoughtful"
                }
                scenes.append(scene)
        
        logger.info(f"✅ Created {len(scenes)} cartoon scenes")
        return scenes
    
    @retry_on_exception()
    def generate_cartoon_scene(self, scene: Dict, style: str) -> Optional[np.ndarray]:
        """
        // [TASK]: Generate single cartoon scene image using ai_model_manager
        // [GOAL]: Centralize image generation and leverage fallback mechanisms
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        logger.info(f"🎨 Generating cartoon scene {scene['id']}: {scene['visual_description'][:40]}...")
        
        try:
            # Build cartoon prompt
            style_config = self.cartoon_styles[style]
            
            prompt = f"""
            {style_config['base_prompt']}, 
            {scene['visual_description']}, 
            {scene['character_emotion']} expression,
            bright colors, clean lines, cartoon style,
            African setting, cultural elements
            """.strip().replace('\n', ' ')
            
            negative_prompt = style_config['negative']
            
            logger.info(f"📝 Prompt: {prompt[:60]}...")
            
            # Generate cartoon image using ai_model_manager
            image_bytes = asyncio.run(generate_image(
                prompt=prompt,
                model_id=config.models.image_generation.hf_api_id,
                use_local_fallback=True,
                negative_prompt=negative_prompt,
                num_inference_steps=2,
                guidance_scale=0.0,
                height=self.height,
                width=self.width
            ))
            
            if image_bytes:
                # Convert bytes to PIL Image, then to OpenCV format
                from PIL import Image
                image = Image.open(io.BytesIO(image_bytes))
                
                # Save scene image
                scene_path = self.output_folder / f"scene_{scene['id']:02d}_cartoon.png"
                image.save(scene_path)
                
                file_size = scene_path.stat().st_size / 1024
                logger.info(f"✅ Scene {scene['id']} generated: {file_size:.1f} KB")
                
                # Convert to OpenCV format
                cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                return cv_image
            else:
                log_and_raise(Exception("ai_model_manager.generate_image returned no bytes"), "Image generation failed")
            
        except Exception as e:
            log_and_raise(e, f"Scene {scene['id']} generation failed")
    
    def create_scene_animation(self, scene_image: np.ndarray, duration: float) -> List[np.ndarray]:
        """
        // [TASK]: Create simple animation from static scene
        """
        logger.info(f"🎬 Creating {duration}s animation...")
        
        frames = []
        total_frames = int(self.fps * duration)
        
        for frame_num in range(total_frames):
            frame = scene_image.copy()
            progress = frame_num / total_frames
            
            # Simple animation effects
            # 1. Subtle zoom
            zoom_factor = 1.0 + (np.sin(progress * np.pi * 2) * 0.02)
            
            # 2. Slight pan
            pan_x = int(np.sin(progress * np.pi) * 10)
            pan_y = int(np.cos(progress * np.pi) * 5)
            
            # Apply transformations
            h, w = frame.shape[:2]
            
            # Zoom
            crop_w = int(w / zoom_factor)
            crop_h = int(h / zoom_factor)
            x1 = max(0, (w - crop_w) // 2 + pan_x)
            y1 = max(0, (h - crop_h) // 2 + pan_y)
            x2 = min(w, x1 + crop_w)
            y2 = min(h, y1 + crop_h)
            
            cropped = frame[y1:y2, x1:x2]
            animated_frame = cv2.resize(cropped, (w, h))
            
            frames.append(animated_frame)
        
        logger.info(f"✅ Created {len(frames)} animated frames")
        return frames
    
    def generate_african_tts(self, text: str, voice: str = "sheng_male") -> Optional[str]:
        """
        // [TASK]: Generate TTS audio in African languages using ai_model_manager
        // [GOAL]: Centralize TTS generation and leverage fallback mechanisms
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        logger.info(f"🎤 Generating {voice} TTS for: {text[:30]}...")
        
        try:
            audio_bytes = asyncio.run(text_to_speech(
                text=text,
                model_id=config.models.voice_synthesis.hf_api_id,
                use_local_fallback=True
            ))
            
            if audio_bytes:
                audio_path = self.output_folder / f"tts_{voice}_{int(time.time())}.wav"
                with open(audio_path, "wb") as f:
                    f.write(audio_bytes)
                logger.info(f"✅ TTS audio: {audio_path}")
                return str(audio_path)
            else:
                log_and_raise(Exception("text_to_speech returned no bytes"), "TTS generation failed")
            
        except Exception as e:
            log_and_raise(e, f"TTS generation failed")
    
    def create_cartoon_video(self, scenes: List[Dict], style: str, voice: str) -> Optional[str]:
        """Create complete cartoon video with parallel scene processing"""
        
        logger.info(f"🎬 Creating cartoon video: {style} style, {voice} voice")
        
        # Model loading is now handled by ai_model_manager

        from utils.parallel_processing import ParallelProcessor
        import asyncio

        async def scene_worker(scene_data):
            loop = asyncio.get_running_loop()
            
            def process_scene_assets():
                scene_image = self.generate_cartoon_scene(scene_data, style)
                if scene_image is None:
                    return None, None
                
                audio_path = self.generate_african_tts(scene_data['dialogue'], voice)
                animated_frames = self.create_scene_animation(scene_image, scene_data['duration'])
                return animated_frames, audio_path

            try:
                animated_frames, audio_path = await loop.run_in_executor(None, process_scene_assets)
                if animated_frames is None:
                    log_and_raise(Exception("Image generation failed"), "Scene worker failed")
                return {"status": "success", "frames": animated_frames, "audio": audio_path}
            except Exception as e:
                log_and_raise(e, "Scene worker failed")

        async def run_parallel_processing(all_scenes):
            processor = ParallelProcessor()
            return await processor.run_parallel(all_scenes, scene_worker)

        results = asyncio.run(run_parallel_processing(scenes))
        
        all_frames = []
        all_audio_paths = []
        for res in results:
            if res and res.get("status") == "success":
                all_frames.extend(res["frames"])
                if res.get("audio"):
                    all_audio_paths.append(res["audio"])
        
        if not all_frames:
            log_and_raise(ValueError("No frames generated"), "Video creation failed")
        
        video_path = self.output_folder / f"cartoon_{style}_{voice}_{int(time.time())}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(video_path), fourcc, self.fps, (self.width, self.height))
        
        logger.info(f"📹 Writing {len(all_frames)} frames...")
        for frame in all_frames:
            writer.write(frame)
        writer.release()
        
        # Placeholder: Audio is not yet muxed into the video in this pipeline.
        # This would require a final ffmpeg step.

        if video_path.exists():
            size_mb = video_path.stat().st_size / (1024*1024)
            logger.info(f"✅ Cartoon video created: {size_mb:.1f} MB")
            return str(video_path)
        else:
            log_and_raise(Exception("Video creation failed"), "Video creation failed")
    
    def export_for_mobile(self, video_path: str, preset: str) -> Optional[str]:
        """
        // [TASK]: Export video for mobile platforms
        """
        
        if preset not in self.export_presets:
            log_and_raise(ValueError(f"Unknown preset: {preset}"), "Mobile export failed")
        
        config = self.export_presets[preset]
        output_path = self.output_folder / f"mobile_{preset}_{int(time.time())}.mp4"
        
        try:
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vf", f"scale={config['width']}:{config['height']}",
                "-r", str(config['fps']),
                "-t", str(config['duration']),
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists():
                logger.info(f"✅ Mobile export ({preset}): {output_path}")
                return str(output_path)
            else:
                log_and_raise(Exception(f"Mobile export failed: {result.stderr}"), "Mobile export failed")
                
        except Exception as e:
            log_and_raise(e, f"Export error")


def create_african_cartoon_video(
    script: str,
    style: str = "african_cartoon",
    voice: str = "sheng_male",
    mobile_preset: Optional[str] = None
) -> Dict:
    """
    Main function to create African cartoon video
    
    Args:
        script: Text script to animate
        style: Cartoon style (african_cartoon, anime, kenyan_animation)
        voice: TTS voice (sheng_male, sheng_female, kiswahili, english_news)
        mobile_preset: Export preset (tiktok, whatsapp, youtube_shorts, instagram_reel)
    
    Returns:
        Dict with video paths and metadata
    """
    
    logger.info("🎨 AFRICAN CARTOON VIDEO GENERATOR")
    logger.info("=" * 50)
    
    pipeline = AfricanCartoonPipeline()
    
    # Break script into scenes
    scenes = pipeline.break_script_into_scenes(script)
    
    # Create cartoon video
    video_path = pipeline.create_cartoon_video(scenes, style, voice)
    
    result = {
        "success": video_path is not None,
        "video_path": video_path,
        "scenes": len(scenes),
        "style": style,
        "voice": voice
    }
    
    # Mobile export if requested
    if mobile_preset and video_path:
        mobile_path = pipeline.export_for_mobile(video_path, mobile_preset)
        result["mobile_path"] = mobile_path
        result["mobile_preset"] = mobile_preset
    
    return result


if __name__ == "__main__":    # Test the cartoon pipeline    test_script = """    Welcome to Kenya, the beautiful land of diverse cultures.     Mount Kenya stands majestically with snow-capped peaks.     The Maasai people preserve their rich traditions.     Wildlife roams freely in the vast savannas.     This is our home, this is Kenya.    """        try:        result = create_african_cartoon_video(            script=test_script,            style="african_cartoon",            voice="sheng_male",            mobile_preset="tiktok"        )        logger.info(f"\n🎉 RESULT: {result}")    except Exception as e:        log_and_raise(e, "Error during cartoon video creation")
