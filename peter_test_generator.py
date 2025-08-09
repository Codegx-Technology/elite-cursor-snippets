#!/usr/bin/env python3
"""
🎬 Peter Test - Perfect 3-Second Kenya Video Generator
Fix all issues and create flawless 3-second video with audio, images, everything

// [SNIPPET]: surgicalfix + thinkwithai + kenyafirst + refactorclean
// [CONTEXT]: Fix video corruption, optimize time, create perfect 3-second test
// [GOAL]: Flawless 3-second video with all features in peter-test folder
"""

import torch
from diffusers import AutoPipelineForText2Image
import cv2
import numpy as np
from pathlib import Path
import time
from datetime import datetime
import subprocess
import os
import shutil

class PeterTestGenerator:
    """
    🎯 Perfect 3-Second Kenya Video Generator
    
    Fixes:
    1. Video corruption (proper codec and encoding)
    2. Generation time (optimized for speed)
    3. Process completion (guaranteed finish)
    """
    
    def __init__(self):
        self.fps = 30
        self.duration = 3  # 3 seconds only
        self.total_frames = self.fps * self.duration  # 90 frames
        self.width = 1280  # Optimized resolution
        self.height = 720
        
        # Create peter-test folder
        self.output_folder = Path("peter-test")
        self.output_folder.mkdir(exist_ok=True)
        
        # Single perfect scene for 3 seconds
        self.scene = {
            "name": "Kenya Majesty",
            "prompt": "Mount Kenya snow-capped peaks with Kenya flag, golden hour, cinematic, photorealistic",
            "audio_file": "kenya_anthem_3sec.wav"
        }
        
        print("🎬 PETER TEST GENERATOR INITIALIZED")
        print(f"📁 Output folder: {self.output_folder.absolute()}")
        print(f"⏱️ Duration: {self.duration} seconds ({self.total_frames} frames)")
        print(f"📏 Resolution: {self.width}x{self.height} (optimized)")
    
    def initialize_ai_generator(self):
        """Initialize SDXL-Turbo with speed optimizations"""
        
        try:
            print("🤖 Initializing SDXL-Turbo (optimized for speed)...")
            
            pipe = AutoPipelineForText2Image.from_pretrained(
                "stabilityai/sdxl-turbo",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                variant="fp16" if torch.cuda.is_available() else None,
                use_safetensors=True,
                low_cpu_mem_usage=True
            )
            
            if torch.cuda.is_available():
                pipe = pipe.to("cuda")
                print("🔥 GPU mode - ~10 seconds generation")
            else:
                print("🖥️ CPU mode - ~3-5 minutes generation")
            
            print("✅ SDXL-Turbo ready!")
            return pipe
            
        except Exception as e:
            print(f"❌ AI generator failed: {e}")
            return None
    
    def generate_perfect_image(self, pipe):
        """Generate one perfect Kenya AI image"""
        
        print(f"🎨 Generating: {self.scene['name']}")
        print(f"📝 Prompt: {self.scene['prompt']}")
        
        try:
            start_time = time.time()
            
            # Generate with optimized settings
            image = pipe(
                prompt=self.scene['prompt'],
                num_inference_steps=2,  # Turbo mode
                guidance_scale=0.0,
                height=self.height,
                width=self.width
            ).images[0]
            
            gen_time = time.time() - start_time
            print(f"✅ Generated in {gen_time:.1f}s")
            
            # Save to peter-test folder
            image_path = self.output_folder / "kenya_scene.png"
            image.save(image_path)
            
            file_size = image_path.stat().st_size / 1024
            print(f"💾 Saved: {image_path} ({file_size:.1f} KB)")
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            return cv_image, image_path
            
        except Exception as e:
            print(f"❌ Image generation failed: {e}")
            return None, None
    
    def create_audio(self):
        """Create 3-second audio track"""
        
        print("🎵 Creating 3-second audio...")
        
        try:
            # Use existing audio and trim to 3 seconds
            source_audio = Path("music_library/african_background.wav")
            output_audio = self.output_folder / "kenya_anthem_3sec.wav"
            
            if source_audio.exists():
                # Use ffmpeg to trim audio to exactly 3 seconds
                cmd = [
                    "ffmpeg", "-y",
                    "-i", str(source_audio),
                    "-t", "3",
                    "-acodec", "pcm_s16le",
                    str(output_audio)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Audio created: {output_audio}")
                    return str(output_audio)
                else:
                    print(f"⚠️ ffmpeg failed, creating simple audio")
                    return self.create_simple_audio()
            else:
                return self.create_simple_audio()
                
        except Exception as e:
            print(f"⚠️ Audio creation error: {e}")
            return self.create_simple_audio()
    
    def create_simple_audio(self):
        """Create simple 3-second audio as fallback"""
        
        try:
            import wave
            import struct
            
            output_audio = self.output_folder / "kenya_simple_3sec.wav"
            
            # Create 3-second sine wave (Kenya anthem tone)
            sample_rate = 44100
            duration = 3
            frequency = 440  # A note
            
            frames = []
            for i in range(int(sample_rate * duration)):
                value = int(32767 * 0.3 * np.sin(2 * np.pi * frequency * i / sample_rate))
                frames.append(struct.pack('<h', value))
            
            with wave.open(str(output_audio), 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(b''.join(frames))
            
            print(f"✅ Simple audio created: {output_audio}")
            return str(output_audio)
            
        except Exception as e:
            print(f"❌ Simple audio failed: {e}")
            return None
    
    def create_perfect_video(self, cv_image, audio_path):
        """Create perfect 3-second video with proper encoding"""
        
        print("🎬 Creating perfect video...")
        
        video_path = self.output_folder / "peter_test_perfect.mp4"
        
        # Use proper codec to avoid "moov atom" issues
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(video_path), fourcc, self.fps, (self.width, self.height))
        
        if not writer.isOpened():
            print("❌ Video writer failed to open")
            return None
        
        print(f"📹 Creating {self.total_frames} frames...")
        
        for frame_num in range(self.total_frames):
            # Create dynamic frame
            frame = cv_image.copy()
            
            # Add progress indicator
            progress = frame_num / self.total_frames
            
            # Add zoom effect
            zoom_factor = 1.0 + (progress * 0.05)  # Slight zoom
            h, w = frame.shape[:2]
            center_x, center_y = w // 2, h // 2
            
            crop_w = int(w / zoom_factor)
            crop_h = int(h / zoom_factor)
            x1 = max(0, center_x - crop_w // 2)
            y1 = max(0, center_y - crop_h // 2)
            x2 = min(w, x1 + crop_w)
            y2 = min(h, y1 + crop_h)
            
            cropped = frame[y1:y2, x1:x2]
            frame = cv2.resize(cropped, (w, h))
            
            # Add text overlay
            if frame_num < 60:  # First 2 seconds
                font = cv2.FONT_HERSHEY_SIMPLEX
                text = "KENYA MAJESTY"
                font_scale = 2.0
                thickness = 3
                
                text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                x = (w - text_size[0]) // 2
                y = h - 50
                
                # Add text with outline
                cv2.putText(frame, text, (x+2, y+2), font, font_scale, (0, 0, 0), thickness+2)
                cv2.putText(frame, text, (x, y), font, font_scale, (255, 255, 255), thickness)
            
            writer.write(frame)
            
            # Progress update
            if frame_num % 30 == 0:
                print(f"   📊 Frame {frame_num}/{self.total_frames} ({progress*100:.1f}%)")
        
        writer.release()
        
        # Verify video was created
        if video_path.exists():
            size_mb = video_path.stat().st_size / (1024*1024)
            print(f"✅ Video created: {video_path} ({size_mb:.1f} MB)")
            
            # Add audio using ffmpeg if available
            if audio_path:
                final_video = self.add_audio_to_video(str(video_path), audio_path)
                return final_video
            else:
                return str(video_path)
        else:
            print("❌ Video creation failed")
            return None
    
    def add_audio_to_video(self, video_path, audio_path):
        """Add audio to video using ffmpeg"""
        
        try:
            final_video = self.output_folder / "peter_test_final.mp4"
            
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-shortest",
                "-movflags", "+faststart",  # Fix moov atom issues
                str(final_video)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and final_video.exists():
                print(f"✅ Final video with audio: {final_video}")
                return str(final_video)
            else:
                print("⚠️ Audio merge failed, returning video without audio")
                return video_path
                
        except Exception as e:
            print(f"⚠️ Audio merge error: {e}")
            return video_path
    
    def create_peter_test(self):
        """Create the complete Peter Test"""
        
        print("🎬 CREATING PETER TEST - PERFECT 3-SECOND VIDEO")
        print("=" * 60)
        
        total_start = time.time()
        
        # Step 1: Initialize AI
        pipe = self.initialize_ai_generator()
        if pipe is None:
            print("❌ Cannot proceed without AI generator")
            return None
        
        # Step 2: Generate perfect image
        print("\n🎨 STEP 1: Generate Perfect AI Image")
        cv_image, image_path = self.generate_perfect_image(pipe)
        if cv_image is None:
            print("❌ Image generation failed")
            return None
        
        # Step 3: Create audio
        print("\n🎵 STEP 2: Create Perfect Audio")
        audio_path = self.create_audio()
        
        # Step 4: Create perfect video
        print("\n🎬 STEP 3: Create Perfect Video")
        video_path = self.create_perfect_video(cv_image, audio_path)
        
        total_time = time.time() - total_start
        
        if video_path:
            print(f"\n🎉 PETER TEST COMPLETE!")
            print(f"⏱️ Total time: {total_time:.1f} seconds")
            print(f"📁 All files in: {self.output_folder.absolute()}")
            
            # List all created files
            print("\n📋 CREATED FILES:")
            for file in self.output_folder.iterdir():
                if file.is_file():
                    size = file.stat().st_size / 1024
                    print(f"   📄 {file.name}: {size:.1f} KB")
            
            return str(video_path)
        else:
            print("❌ Peter Test failed")
            return None


def main():
    """Create Peter Test"""
    
    print("🎯 PETER TEST - PERFECT 3-SECOND KENYA VIDEO")
    print("=" * 50)
    print("🔧 Fixes: Video corruption, generation time, completion")
    print("🎬 Output: Perfect 3-second video with audio and images")
    print("📁 Location: peter-test folder")
    print("=" * 50)
    
    try:
        generator = PeterTestGenerator()
        result = generator.create_peter_test()
        
        if result:
            print(f"\n🎉 SUCCESS! Peter Test created:")
            print(f"📹 {result}")
            print("🇰🇪 Perfect 3-second Kenya masterpiece ready!")
        else:
            print("\n❌ Peter Test failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
