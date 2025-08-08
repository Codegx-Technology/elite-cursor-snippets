#!/usr/bin/env python3
"""
voice_engine.py
TTS wrapper for Shujaa Studio - supports Bark, pyttsx3, and edge-tts
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

def tts_bark(input_file: str, output_file: str):
    """Generate TTS using Bark"""
    try:
        # Read input text
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            print("[TTS] Empty text, generating silence")
            # Generate 3 seconds of silence
            cmd = f"ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=22050 -t 3 \"{output_file}\""
            subprocess.run(cmd, shell=True, check=True)
            return
        
        print(f"[TTS] Generating audio for: {text[:50]}...")
        
        # For now, use pyttsx3 as fallback since Bark requires more setup
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Save to temporary file first
        temp_file = output_file + ".temp.wav"
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        
        # Convert to target format if needed
        if not output_file.endswith('.wav'):
            cmd = f"ffmpeg -y -i \"{temp_file}\" \"{output_file}\""
            subprocess.run(cmd, shell=True, check=True)
            os.remove(temp_file)
        else:
            os.rename(temp_file, output_file)
            
        print(f"[TTS] Audio generated: {output_file}")
        
    except Exception as e:
        print(f"[TTS] Error: {e}")
        # Fallback to silence
        cmd = f"ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=22050 -t 3 \"{output_file}\""
        subprocess.run(cmd, shell=True, check=True)

def tts_edge(input_file: str, output_file: str, voice: str = "en-US-AriaNeural"):
    """Generate TTS using Edge TTS"""
    try:
        import asyncio
        import edge_tts
        
        # Read input text
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            print("[TTS] Empty text, generating silence")
            cmd = f"ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=22050 -t 3 \"{output_file}\""
            subprocess.run(cmd, shell=True, check=True)
            return
        
        print(f"[TTS] Generating audio with Edge TTS for: {text[:50]}...")
        
        async def generate():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
        
        asyncio.run(generate())
        print(f"[TTS] Audio generated: {output_file}")
        
    except Exception as e:
        print(f"[TTS] Edge TTS error: {e}, falling back to pyttsx3")
        tts_bark(input_file, output_file)

def main():
    parser = argparse.ArgumentParser(description="Shujaa Studio Voice Engine")
    parser.add_argument("--input", required=True, help="Input text file")
    parser.add_argument("--output", required=True, help="Output audio file")
    parser.add_argument("--engine", default="pyttsx3", choices=["bark", "pyttsx3", "edge"], help="TTS engine to use")
    parser.add_argument("--voice", default="en-US-AriaNeural", help="Voice for Edge TTS")
    
    args = parser.parse_args()
    
    # Ensure input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found")
        sys.exit(1)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    if args.engine == "edge":
        tts_edge(args.input, args.output, args.voice)
    elif args.engine == "bark":
        # Bark implementation would go here
        print("[TTS] Bark not implemented yet, using pyttsx3")
        tts_bark(args.input, args.output)
    else:
        tts_bark(args.input, args.output)

if __name__ == "__main__":
    main()
