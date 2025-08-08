#!/usr/bin/env python3
"""
🔥 Shujaa Studio - One-Click Script-to-Video CLI Tool (Combo Pack B)
Following Elite Cursor Snippets Context Patterns

// [TASK]: Fully automated script-to-video pipeline CLI tool
// [GOAL]: One user prompt → complete video with scenes, voices, visuals, merge (offline)
// [CONSTRAINTS]: Must work offline, follow elite-cursor-snippets patterns
// [SNIPPET]: thinkwithai + refactorclean + kenyafirst
// [CONTEXT]: Enhanced version of existing generate_video.py for full automation
// [PROGRESS]: Implementing Combo Pack B specification
// [NEXT]: Complete CLI implementation with voice, image, and video generation
// [LOCATION]: offline_video_maker/generate_video.py
"""

import os
import sys
import subprocess
import json
import uuid
from pathlib import Path
from time import sleep
import tempfile
from typing import List, Dict, Optional

class OfflineVideoMaker:
    """
    // [TASK]: One-click video generation from text prompt
    // [GOAL]: Complete offline video pipeline
    // [CONSTRAINTS]: No internet required, all processing local
    """
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.output_dir = self.project_dir / "output"
        self.temp_dir = self.project_dir / "temp"
        self.models_dir = self.project_dir.parent / "models"
        
        # Create directories
        for dir_path in [self.output_dir, self.temp_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Configuration paths (to be updated with actual model paths)
        self.bark_path = self.models_dir / "bark"
        self.sdxl_path = self.models_dir / "stable-diffusion-xl"
        self.default_image = self.project_dir.parent / "temp" / "default_scene.png"
        
        print("[INIT] Shujaa Studio Offline Video Maker initialized!")
        print(f"[CONTEXT] Working directory: {self.project_dir}")
        print(f"[CONTEXT] Output directory: {self.output_dir}")
    
    def generate_story_breakdown(self, prompt: str) -> List[Dict[str, str]]:
        """
        // [TASK]: Break down user prompt into scenes
        // [GOAL]: Create structured scene data for video generation
        // [SNIPPET]: thinkwithai
        """
        print(f"[STORY] Generating story breakdown from prompt: {prompt}")
        
        # For now, create a simple scene breakdown
        # TODO: Integrate with LLM for intelligent scene splitting
        scenes = [
            {
                "id": "scene1",
                "text": f"Scene 1: {prompt}",
                "description": f"Visual representation of: {prompt}",
                "duration": 5.0
            }
        ]
        
        # Save scene data
        scene_file = self.temp_dir / "scenes.json"
        with open(scene_file, "w", encoding="utf-8") as f:
            json.dump(scenes, f, indent=2, ensure_ascii=False)
        
        print(f"[PROGRESS] Generated {len(scenes)} scenes")
        return scenes
    
    def generate_voice(self, scene: Dict[str, str]) -> Path:
        """
        // [TASK]: Generate voice audio for scene
        // [GOAL]: Create high-quality speech from text
        // [SNIPPET]: surgicalfix + kenyafirst
        """
        scene_id = scene["id"]
        text = scene["text"]
        
        print(f"[VOICE] Generating voice for {scene_id}...")
        
        # Create text file for Bark
        text_file = self.temp_dir / f"{scene_id}.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        # Output audio file
        audio_file = self.temp_dir / f"{scene_id}.wav"
        
        # Check if Bark is available
        if self.bark_path.exists():
            bark_cmd = f"python3 {self.bark_path}/gen.py --input {text_file} --output {audio_file}"
            print(f"[CMD] Running: {bark_cmd}")
            try:
                result = subprocess.run(bark_cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"[SUCCESS] Voice generated: {audio_file}")
                else:
                    print(f"[WARNING] Bark failed, using TTS fallback")
                    self._generate_fallback_voice(text, audio_file)
            except Exception as e:
                print(f"[WARNING] Bark error: {e}, using TTS fallback")
                self._generate_fallback_voice(text, audio_file)
        else:
            print("[WARNING] Bark not found, using TTS fallback")
            self._generate_fallback_voice(text, audio_file)
        
        return audio_file
    
    def _generate_fallback_voice(self, text: str, output_file: Path):
        """
        // [TASK]: Fallback TTS when Bark is not available
        // [GOAL]: Ensure voice generation always works
        // [SNIPPET]: surgicalfix
        """
        try:
            # Try using system TTS (Windows SAPI)
            if os.name == 'nt':  # Windows
                import pyttsx3
                engine = pyttsx3.init()
                engine.save_to_file(text, str(output_file))
                engine.runAndWait()
                print(f"[FALLBACK] System TTS voice generated: {output_file}")
            else:
                # Create a silent audio file as placeholder
                print("[WARNING] No TTS available, creating silent audio")
                subprocess.run([
                    "ffmpeg", "-f", "lavfi", "-i", "anullsrc=duration=5", 
                    "-ar", "22050", "-ac", "1", str(output_file)
                ], check=True)
        except Exception as e:
            print(f"[ERROR] Fallback TTS failed: {e}")
            # Create minimal silent audio
            subprocess.run([
                "ffmpeg", "-f", "lavfi", "-i", "anullsrc=duration=5", 
                "-ar", "22050", "-ac", "1", str(output_file)
            ], check=True)
    
    def generate_image(self, scene: Dict[str, str]) -> Path:
        """
        // [TASK]: Generate or use image for scene
        // [GOAL]: Create visual content for video
        // [SNIPPET]: refactorclean + kenyafirst
        """
        scene_id = scene["id"]
        description = scene["description"]
        
        print(f"[IMAGE] Generating image for {scene_id}...")
        
        image_file = self.temp_dir / f"{scene_id}.png"
        
        # Check if SDXL is available
        if self.sdxl_path.exists():
            # TODO: Implement SDXL image generation
            sdxl_cmd = f"python3 {self.sdxl_path}/generate.py --prompt \"{description}\" --output {image_file}"
            print(f"[CMD] SDXL command (placeholder): {sdxl_cmd}")
            print("[TODO] SDXL integration pending - using placeholder")
            self._use_placeholder_image(image_file)
        else:
            print("[WARNING] SDXL not found, using placeholder image")
            self._use_placeholder_image(image_file)
        
        return image_file
    
    def _use_placeholder_image(self, output_file: Path):
        """
        // [TASK]: Create or copy placeholder image
        // [GOAL]: Ensure image generation always works
        // [SNIPPET]: surgicalfix
        """
        if self.default_image.exists():
            # Copy existing default image
            subprocess.run(["copy" if os.name == 'nt' else "cp", str(self.default_image), str(output_file)], shell=True)
            print(f"[PLACEHOLDER] Using default image: {output_file}")
        else:
            # Create a simple colored placeholder
            try:
                from PIL import Image, ImageDraw, ImageFont
                
                # Create 1920x1080 image with gradient background
                img = Image.new('RGB', (1920, 1080), color='#2E8B57')  # Sea green
                draw = ImageDraw.Draw(img)
                
                # Add text
                try:
                    font = ImageFont.truetype("arial.ttf", 60)
                except:
                    font = ImageFont.load_default()
                
                text = "Shujaa Studio\nAfrican AI Video"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (1920 - text_width) // 2
                y = (1080 - text_height) // 2
                
                draw.text((x, y), text, fill='white', font=font, align='center')
                
                img.save(output_file)
                print(f"[CREATED] Generated placeholder image: {output_file}")
                
            except Exception as e:
                print(f"[ERROR] Could not create placeholder: {e}")
                # Create minimal image with ffmpeg
                subprocess.run([
                    "ffmpeg", "-f", "lavfi", "-i", "color=c=green:size=1920x1080:duration=1",
                    "-frames:v", "1", str(output_file)
                ], check=True)
    
    def create_scene_video(self, scene: Dict[str, str], audio_file: Path, image_file: Path) -> Path:
        """
        // [TASK]: Combine audio and image into video scene
        // [GOAL]: Create individual scene video file
        // [SNIPPET]: refactorclean
        """
        scene_id = scene["id"]
        video_file = self.temp_dir / f"{scene_id}.mp4"
        
        print(f"[VIDEO] Creating video scene: {scene_id}")
        
        # Use ffmpeg to combine image and audio
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(image_file),
            "-i", str(audio_file),
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(video_file)
        ]
        
        print(f"[CMD] Running ffmpeg: {' '.join(ffmpeg_cmd)}")
        
        try:
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print(f"[SUCCESS] Scene video created: {video_file}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] FFmpeg failed: {e}")
            print(f"❌ [STDERR] {e.stderr}")
            raise
        
        return video_file
    
    def merge_scenes(self, scene_videos: List[Path]) -> Path:
        """
        // [TASK]: Merge all scene videos into final output
        // [GOAL]: Create complete video file
        // [SNIPPET]: refactorclean
        """
        print("[MERGE] Finalizing output video...")
        
        # Create concat file for ffmpeg
        concat_file = self.temp_dir / "scenes_list.txt"
        with open(concat_file, "w") as f:
            for video_file in scene_videos:
                f.write(f"file '{video_file.absolute()}'\n")
        
        # Final output file
        final_output = self.output_dir / f"shujaa_video_{uuid.uuid4().hex[:8]}.mp4"
        
        # Merge videos
        merge_cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            str(final_output)
        ]
        
        print(f"[CMD] Merging videos: {' '.join(merge_cmd)}")
        
        try:
            result = subprocess.run(merge_cmd, capture_output=True, text=True, check=True)
            print(f"[SUCCESS] Final video created: {final_output}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Video merge failed: {e}")
            print(f"❌ [STDERR] {e.stderr}")
            raise
        
        return final_output
    
    def generate_video(self, prompt: str) -> Path:
        """
        // [TASK]: Main pipeline - prompt to video
        // [GOAL]: Complete end-to-end video generation
        // [SNIPPET]: thinkwithai + taskchain
        """
        print(f"\n[START] Shujaa Studio Video Generation Pipeline")
        print(f"[PROMPT] {prompt}")
        print("=" * 60)
        
        try:
            # Step 1: Generate story breakdown
            scenes = self.generate_story_breakdown(prompt)
            
            # Step 2: Process each scene
            scene_videos = []
            for scene in scenes:
                print(f"\n[SCENE] Processing {scene['id']}...")
                
                # Generate voice
                audio_file = self.generate_voice(scene)
                
                # Generate image
                image_file = self.generate_image(scene)
                
                # Create scene video
                video_file = self.create_scene_video(scene, audio_file, image_file)
                scene_videos.append(video_file)
            
            # Step 3: Merge all scenes
            final_video = self.merge_scenes(scene_videos)
            
            print("\n" + "=" * 60)
            print(f"\n[COMPLETE] Video generation successful!")
            print(f"[OUTPUT] {final_video}")
            print(f"[READY] Your Shujaa Studio video is ready!")
            
            return final_video
            
        except Exception as e:
            print(f"\n[ERROR] Video generation failed: {e}")
            raise

def main():
    """
    // [TASK]: CLI entry point
    // [GOAL]: Handle command line arguments and run video generation
    // [SNIPPET]: surgicalfix + kenyafirst
    """
    print("Shujaa Studio - One-Click Script-to-Video Tool")
    print("Proudly African AI Video Generation")
    print()
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("[ERROR] Missing prompt argument")
        print()
        print("Usage:")
        print("  python3 generate_video.py \"Your story prompt here\"")
        print()
        print("Examples:")
        print("  python3 generate_video.py \"Story of a girl from Turkana who becomes an engineer\"")
        print("  python3 generate_video.py \"A Luo girl builds a school in Kisumu to help orphans\"")
        print("  python3 generate_video.py \"Young Maasai warrior learns coding in Nairobi\"")
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    # Validate ffmpeg availability
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] FFmpeg not found. Please install FFmpeg to continue.")
        print("[INSTALL] Visit: https://ffmpeg.org/download.html")
        sys.exit(1)
    
    # Initialize and run video maker
    try:
        video_maker = OfflineVideoMaker()
        final_video = video_maker.generate_video(prompt)
        
        print(f"\n[SUCCESS] Video generation complete!")
        print(f"[FILE] {final_video}")
        print(f"[NEXT] Ready for Combo Pack C enhancements!")
        
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Video generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FATAL] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
