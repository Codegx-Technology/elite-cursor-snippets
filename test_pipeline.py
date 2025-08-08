#!/usr/bin/env python3
"""
Test script for Shujaa Studio Pipeline
"""

import subprocess
import os
import sys

def test_pipeline():
    """Test the pipeline with a simple prompt"""
    print("🧪 Testing Shujaa Studio Pipeline...")
    
    # Test command
    test_cmd = [
        "python", "pipeline.py",
        "--prompt", "A young Kenyan entrepreneur builds an AI startup in Nairobi",
        "--out", "./test_output.mp4",
        "--scenes", "2",
        "--vertical"
    ]
    
    print(f"Running: {' '.join(test_cmd)}")
    
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Pipeline test successful!")
            if os.path.exists("./test_output.mp4"):
                print(f"📹 Video generated: ./test_output.mp4")
                print(f"📊 File size: {os.path.getsize('./test_output.mp4')} bytes")
            else:
                print("⚠️ Video file not found")
        else:
            print(f"❌ Pipeline test failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Pipeline test timed out")
    except Exception as e:
        print(f"❌ Pipeline test error: {e}")

def test_voice_engine():
    """Test the voice engine"""
    print("\n🎤 Testing Voice Engine...")
    
    # Create test text file
    test_text = "This is a test of the Shujaa Studio voice engine."
    with open("test_input.txt", "w") as f:
        f.write(test_text)
    
    test_cmd = [
        "python", "voice_engine.py",
        "--input", "test_input.txt",
        "--output", "test_voice.wav"
    ]
    
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Voice engine test successful!")
            if os.path.exists("test_voice.wav"):
                print(f"🎵 Audio generated: test_voice.wav")
            else:
                print("⚠️ Audio file not found")
        else:
            print(f"❌ Voice engine test failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Voice engine test error: {e}")

def test_music_engine():
    """Test the music engine"""
    print("\n🎵 Testing Music Engine...")
    
    test_cmd = [
        "python", "music_engine.py",
        "--prompt", "African traditional music",
        "--out", "test_music.mp3"
    ]
    
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Music engine test successful!")
            if os.path.exists("test_music.mp3"):
                print(f"🎶 Music generated: test_music.mp3")
            else:
                print("⚠️ Music file not found")
        else:
            print(f"❌ Music engine test failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Music engine test error: {e}")

if __name__ == "__main__":
    print("🚀 Shujaa Studio Pipeline Test Suite")
    print("=" * 50)
    
    # Test individual components
    test_voice_engine()
    test_music_engine()
    
    # Test full pipeline
    test_pipeline()
    
    print("\n" + "=" * 50)
    print("🏁 Test suite completed!")
