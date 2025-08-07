#!/usr/bin/env python3
"""
Shujaa Studio - African AI Video Generator
Prompt → Script → Voice → Images → Video
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict
import torch
from transformers import pipeline
import whisper
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
import gradio as gr

class ShujaaStudio:
    def __init__(self):
        self.models_dir = Path("models")
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_script(self, prompt: str) -> Dict:
        """Generate script from prompt using local LLM"""
        # For now, use a template. Later integrate with Mistral/LLaMA
        script = {
            "title": f"Story: {prompt}",
            "scenes": [
                {
                    "description": "Opening scene",
                    "narration": f"This is the story of {prompt}",
                    "duration": 3
                },
                {
                    "description": "Main scene", 
                    "narration": "The journey continues with amazing adventures",
                    "duration": 5
                },
                {
                    "description": "Closing scene",
                    "narration": "And so the story ends with hope and courage",
                    "duration": 3
                }
            ]
        }
        return script
    
    def generate_voice(self, text: str, output_path: str):
        """Generate voice using Bark TTS"""
        try:
            # Simple TTS fallback - replace with Bark when available
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(text, output_path)
            engine.runAndWait()
        except:
            print("⚠️ Voice generation failed - using placeholder")
            # Create silent audio as placeholder
            import numpy as np
            import soundfile as sf
            silence = np.zeros(44100 * 3)  # 3 seconds of silence
            sf.write(output_path, silence, 44100)
    
    def generate_image(self, description: str, output_path: str):
        """Generate image using Stable Diffusion"""
        try:
            # Placeholder - replace with actual SD integration
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple colored image as placeholder
            img = Image.new('RGB', (512, 512), color='#1a4d80')
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            draw.text((50, 250), f"Scene: {description[:50]}", fill='white', font=font)
            img.save(output_path)
            
        except Exception as e:
            print(f"⚠️ Image generation failed: {e}")
    
    def create_video(self, script: Dict, output_path: str):
        """Create final video from script, voice, and images"""
        clips = []
        
        for i, scene in enumerate(script["scenes"]):
            # Generate voice for this scene
            voice_path = f"temp_voice_{i}.wav"
            self.generate_voice(scene["narration"], voice_path)
            
            # Generate image for this scene
            image_path = f"temp_image_{i}.png"
            self.generate_image(scene["description"], image_path)
            
            # Create video clip
            audio = AudioFileClip(voice_path)
            image = ImageClip(image_path).set_duration(audio.duration)
            
            # Combine audio and image
            clip = image.set_audio(audio)
            clips.append(clip)
            
            # Cleanup temp files
            os.remove(voice_path)
            os.remove(image_path)
        
        # Concatenate all clips
        final_video = CompositeVideoClip(clips)
        final_video.write_videofile(output_path, fps=24)
        
        # Cleanup
        final_video.close()
        for clip in clips:
            clip.close()
    
    def generate_video(self, prompt: str) -> str:
        """Main pipeline: Prompt → Script → Voice → Images → Video"""
        print(f"🎬 Generating video for: {prompt}")
        
        # Step 1: Generate script
        script = self.generate_script(prompt)
        
        # Step 2: Create video
        output_path = self.output_dir / f"shujaa_video_{hash(prompt) % 10000}.mp4"
        self.create_video(script, str(output_path))
        
        print(f"✅ Video generated: {output_path}")
        return str(output_path)

def create_gradio_interface():
    """Create Gradio web interface"""
    studio = ShujaaStudio()
    
    def process_prompt(prompt):
        if not prompt.strip():
            return "Please enter a prompt", None
        
        try:
            video_path = studio.generate_video(prompt)
            return f"✅ Video generated successfully!", video_path
        except Exception as e:
            return f"❌ Error: {str(e)}", None
    
    # Create interface
    iface = gr.Interface(
        fn=process_prompt,
        inputs=[
            gr.Textbox(
                label="Enter your story prompt",
                placeholder="Tell a story of a girl from Kibera who becomes Kenya's youngest pilot...",
                lines=3
            )
        ],
        outputs=[
            gr.Textbox(label="Status"),
            gr.Video(label="Generated Video")
        ],
        title="🔥 Shujaa Studio - African AI Video Generator",
        description="Transform your stories into videos with AI",
        theme=gr.themes.Soft()
    )
    
    return iface

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        prompt = " ".join(sys.argv[1:])
        studio = ShujaaStudio()
        video_path = studio.generate_video(prompt)
        print(f"Video saved to: {video_path}")
    else:
        # Web interface mode
        iface = create_gradio_interface()
        iface.launch(share=False, server_name="0.0.0.0", server_port=7860)
