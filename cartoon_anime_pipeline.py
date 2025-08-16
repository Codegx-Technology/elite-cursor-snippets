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
    
    def __init__(self, enhanced_router: Any = None, dialect: Optional[str] = None):
        self.output_folder = Path("cartoon_studio")
        self.output_folder.mkdir(exist_ok=True)
        
        # Animation settings
        self.fps = 24  # Standard animation FPS
        self.width = 1280
        self.height = 720
        
        self.enhanced_router = enhanced_router
        self.dialect = dialect
        
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
    async def break_script_into_scenes(self, script: str) -> List[Dict]: # Make it async
        """Break script into cartoon scenes with dialogue using enhanced_router"""
        
        logger.info("📝 Breaking script into cartoon scenes using enhanced_router...")
        
        if self.enhanced_router:
            request = GenerationRequest(
                prompt=f"Break down the following script into 3-5 distinct cartoon scenes, each with a dialogue and a visual description. Script: {script}",
                type="text",
                dialect=self.dialect
            )
            
            result = await self.enhanced_router.route_generation(request)
            
            if result.success and result.metadata and "generated_text" in result.metadata:
                generated_text = result.metadata["generated_text"]
                logger.info(f"Raw generated scenes text: {generated_text}")
                
                scenes = []
                # Simple parsing, assuming "Scene X: Dialogue. Visual: Description."
                scene_blocks = generated_text.split("Scene ")
                for block in scene_blocks:
                    if not block.strip():
                        continue
                    try:
                        parts = block.split(":", 1)
                        scene_id = int(parts[0].strip())
                        content_parts = parts[1].split("Visual:", 1)
                        dialogue = content_parts[0].strip()
                        visual_description = content_parts[1].strip() if len(content_parts) > 1 else dialogue
                        
                        scenes.append({
                            "id": scene_id,
                            "dialogue": dialogue,
                            "visual_description": visual_description,
                            "duration": max(3.0, min(8.0, len(dialogue.split()) * 0.5)), # Duration based on dialogue length
                            "character_emotion": "neutral" # Default emotion
                        })
                    except Exception as e:
                        logger.warning(f"Failed to parse scene block: {block}. Error: {e}")
                
                if scenes:
                    logger.info(f"✅ Created {len(scenes)} cartoon scenes via enhanced_router")
                    return scenes
                else:
                    logger.warning("Enhanced router returned no parsable scenes. Falling back to simple splitting.")
            else:
                logger.warning(f"Enhanced router failed for scene breakdown: {result.error_message}. Falling back to simple splitting.")
        
        # Fallback to simple scene breakdown (original logic)
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
        
        logger.info(f"✅ Created {len(scenes)} cartoon scenes via simple splitting")
        return scenes
    
    @retry_on_exception()
    async def generate_cartoon_scene(self, scene: Dict, style: str) -> Optional[np.ndarray]: # Make it async
        """
        // [TASK]: Generate single cartoon scene image using enhanced_router
        // [GOAL]: Centralize image generation and leverage fallback mechanisms
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        logger.info(f"🎨 Generating cartoon scene {scene['id']}: {scene['visual_description'][:40]}...")
        
        if self.enhanced_router:
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
            
            request = GenerationRequest(
                prompt=prompt,
                type="image",
                dialect=self.dialect,
                preferences={"negative_prompt": negative_prompt, "height": self.height, "width": self.width} # Pass preferences
            )
            
            result = await self.enhanced_router.route_generation(request)
            
            if result.success and result.content_url:
                from PIL import Image
                if result.content_url.startswith("data:image"):
                    import base64
                    header, encoded = result.content_url.split(",", 1)
                    image_bytes = base64.b64decode(encoded)
                    image = Image.open(io.BytesIO(image_bytes))
                elif Path(result.content_url).exists():
                    image = Image.open(result.content_url)
                else:
                    logger.warning(f"Router returned content_url but not in expected format for direct load: {result.content_url}. Using placeholder image.")
                    return self._create_placeholder_image_cv2(scene) # Fallback to placeholder
                
                # Save scene image
                scene_path = self.output_folder / f"scene_{scene['id']:02d}_cartoon.png"
                image.save(scene_path)
                
                file_size = scene_path.stat().st_size / 1024
                logger.info(f"✅ Scene {scene['id']} generated: {file_size:.1f} KB")
                
                # Convert to OpenCV format
                cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                return cv_image
            else:
                logger.warning(f"Enhanced router failed for image generation: {result.error_message}. Using placeholder image.")
        
        # Fallback to placeholder image if router not available or failed
        return self._create_placeholder_image_cv2(scene)

    def _create_placeholder_image_cv2(self, scene: Dict) -> np.ndarray:
        """Creates a simple placeholder image using OpenCV."""
        width, height = self.width, self.height
        img = np.zeros((height, width, 3), dtype=np.uint8) # Black image
        img.fill(random.randint(50, 200)) # Random color
        
        # Add text
        text = f"Scene {scene['id']}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
        
        return img
    
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
    
    async def generate_african_tts(self, text: str, voice: str = "sheng_male") -> Optional[str]: # Make it async
        """
        // [TASK]: Generate TTS audio in African languages using enhanced_router
        // [GOAL]: Centralize TTS generation and leverage fallback mechanisms
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        logger.info(f"🎤 Generating {voice} TTS for: {text[:30]}...")
        
        if self.enhanced_router:
            request = GenerationRequest(
                prompt=text,
                type="audio",
                dialect=self.dialect,
                preferences={"voice": voice} # Pass voice preference
            )
            
            result = await self.enhanced_router.route_generation(request)
            
            if result.success and result.content_url:
                if result.content_url.startswith("data:audio"):
                    import base64
                    header, encoded = result.content_url.split(",", 1)
                    audio_bytes = base64.b64decode(encoded)
                    audio_path = self.output_folder / f"tts_{voice}_{int(time.time())}.wav"
                    with open(audio_path, "wb") as f:
                        f.write(audio_bytes)
                    logger.info(f"✅ TTS audio generated via router: {audio_path}")
                    return str(audio_path)
                elif Path(result.content_url).exists():
                    import shutil
                    audio_path = self.output_folder / f"tts_{voice}_{int(time.time())}.wav"
                    shutil.copy(result.content_url, audio_path)
                    logger.info(f"✅ TTS audio copied from router temp path: {audio_path}")
                    return str(audio_path)
                else:
                    logger.warning(f"Router returned content_url but not in expected format for direct save: {result.content_url}. Falling back to silent audio.")
            else:
                logger.warning(f"Enhanced router failed for TTS generation: {result.error_message}. Falling back to silent audio.")
        
        # Fallback to silent audio if router not available or failed
        logger.warning("Generating silent audio as fallback for TTS.")
        audio_path = self.output_folder / f"tts_silent_{int(time.time())}.wav"
        try:
            # Create a silent audio file as placeholder
            subprocess.run(
                [
                    "ffmpeg",
                    "-f",
                    "lavfi",
                    "-i",
                    "anullsrc=duration=5",
                    "-ar",
                    "22050",
                    "-ac",
                    "1",
                    str(audio_path),
                ],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(f"✅ Silent audio generated: {audio_path}")
            return str(audio_path)
        except Exception as e:
            logger.error(f"Failed to create silent audio fallback: {e}")
            return None
    
    async def create_cartoon_video(self, scenes: List[Dict], style: str, voice: str) -> Optional[str]: # Make it async
        """Create complete cartoon video with parallel scene processing"""
        
        logger.info(f"🎬 Creating cartoon video: {style} style, {voice} voice")
        
        # Model loading is now handled by ai_model_manager

        from utils.parallel_processing import ParallelProcessor
        import asyncio

        async def scene_worker(scene_data):
            # Direct async calls to generate_cartoon_scene and generate_african_tts
            scene_image = await self.generate_cartoon_scene(scene_data, style)
            if scene_image is None:
                return None, None
            
            audio_path = await self.generate_african_tts(scene_data['dialogue'], voice)
            animated_frames = self.create_scene_animation(scene_image, scene_data['duration'])
            return {"status": "success", "frames": animated_frames, "audio": audio_path}

        async def run_parallel_processing(all_scenes):
            # Use passed parallel_processor, or create if not provided (for standalone testing)
            _parallel_processor = parallel_processor or ParallelProcessor()
            return await _parallel_processor.run_parallel(all_scenes, scene_worker)

        results = await run_parallel_processing(scenes) # Await the parallel processing
        
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
    mobile_preset: Optional[str] = None,
    enhanced_router: Any = None,
    dialect: Optional[str] = None,
    parallel_processor: Any = None,
    scene_processor: Any = None
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
    
    pipeline = AfricanCartoonPipeline(enhanced_router=enhanced_router, dialect=dialect)
    
    # Break script into scenes
    scenes = await pipeline.break_script_into_scenes(script)
    
    # Create cartoon video
    video_path = await pipeline.create_cartoon_video(scenes, style, voice, parallel_processor=parallel_processor, scene_processor=scene_processor)
    
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
