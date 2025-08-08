#!/usr/bin/env python3
"""
🧪 Test Script for Shujaa Studio One-Click Video Generator
Following Elite Cursor Snippets Testing Patterns

// [TASK]: Test the video generation pipeline
// [GOAL]: Verify end-to-end functionality
// [SNIPPET]: writetest + surgicalfix
"""

import subprocess
import sys
from pathlib import Path

def test_video_generation():
    """
    // [TASK]: Test video generation with sample prompts
    // [GOAL]: Ensure CLI tool works correctly
    // [SNIPPET]: writetest
    """
    print("🧪 Testing Shujaa Studio Video Generation")
    print("=" * 50)
    
    test_prompts = [
        "A young Kenyan girl from Turkana becomes a software engineer",
        "Maasai warrior learns coding in Nairobi tech hub",
        "Story of innovation in African villages"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🎯 Test {i}: {prompt}")
        print("-" * 40)
        
        try:
            # Run the video generation
            cmd = [sys.executable, "generate_video.py", prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ Test {i} PASSED")
                print("📁 Output files created successfully")
            else:
                print(f"❌ Test {i} FAILED")
                print(f"Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Test {i} TIMEOUT (5 minutes)")
        except Exception as e:
            print(f"❌ Test {i} ERROR: {e}")
    
    print("\n🏁 Testing complete!")

if __name__ == "__main__":
    test_video_generation()
