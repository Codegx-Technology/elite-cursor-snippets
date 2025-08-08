#!/usr/bin/env python3
"""
music_engine.py
Music generation wrapper for Shujaa Studio - supports MusicGen and fallback options
"""

import argparse
import os
import sys
import subprocess
import random
from pathlib import Path

def generate_music_musicgen(prompt: str, output_file: str):
    """Generate music using MusicGen"""
    try:
        # For now, we'll use a simple approach with existing music files
        # In a full implementation, this would call MusicGen API or local model
        
        # Check if we have music library
        music_dir = Path("./music_library")
        if music_dir.exists():
            music_files = list(music_dir.glob("*.wav")) + list(music_dir.glob("*.mp3"))
            if music_files:
                # Select random music file
                selected_music = random.choice(music_files)
                print(f"[MUSIC] Using existing music: {selected_music}")
                
                # Copy and convert to target format
                cmd = f"ffmpeg -y -i \"{selected_music}\" -t 8 \"{output_file}\""
                subprocess.run(cmd, shell=True, check=True)
                return
        
        # Fallback: generate simple tone
        print("[MUSIC] No music library found, generating simple tone")
        cmd = f"ffmpeg -y -f lavfi -i \"sine=frequency=440:duration=8\" -c:a aac -b:a 192k \"{output_file}\""
        subprocess.run(cmd, shell=True, check=True)
        
    except Exception as e:
        print(f"[MUSIC] Error: {e}")
        # Generate silence as fallback
        cmd = f"ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t 8 \"{output_file}\""
        subprocess.run(cmd, shell=True, check=True)

def generate_music_simple(prompt: str, output_file: str):
    """Generate simple background music based on prompt"""
    try:
        # Analyze prompt for mood
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["african", "kenya", "tribal", "traditional"]):
            # African-inspired tone
            cmd = f"ffmpeg -y -f lavfi -i \"sine=frequency=220:duration=8\" -c:a aac -b:a 192k \"{output_file}\""
        elif any(word in prompt_lower for word in ["technology", "future", "ai", "digital"]):
            # Tech-inspired tone
            cmd = f"ffmpeg -y -f lavfi -i \"sine=frequency=880:duration=8\" -c:a aac -b:a 192k \"{output_file}\""
        elif any(word in prompt_lower for word in ["story", "narrative", "tale"]):
            # Story-inspired tone
            cmd = f"ffmpeg -y -f lavfi -i \"sine=frequency=440:duration=8\" -c:a aac -b:a 192k \"{output_file}\""
        else:
            # Default tone
            cmd = f"ffmpeg -y -f lavfi -i \"sine=frequency=330:duration=8\" -c:a aac -b:a 192k \"{output_file}\""
        
        subprocess.run(cmd, shell=True, check=True)
        print(f"[MUSIC] Generated background music: {output_file}")
        
    except Exception as e:
        print(f"[MUSIC] Error: {e}")
        # Generate silence as fallback
        cmd = f"ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t 8 \"{output_file}\""
        subprocess.run(cmd, shell=True, check=True)

def main():
    parser = argparse.ArgumentParser(description="Shujaa Studio Music Engine")
    parser.add_argument("--prompt", required=True, help="Text prompt for music generation")
    parser.add_argument("--out", required=True, help="Output music file")
    parser.add_argument("--engine", default="simple", choices=["musicgen", "simple"], help="Music generation engine")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    
    if args.engine == "musicgen":
        generate_music_musicgen(args.prompt, args.out)
    else:
        generate_music_simple(args.prompt, args.out)

if __name__ == "__main__":
    main()
