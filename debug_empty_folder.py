#!/usr/bin/env python3
"""
🔍 Debug Empty Folder Issue
Investigate why real-ai-peter-test folder is empty despite success messages

// [SNIPPET]: surgicalfix + thinkwithai + kenyafirst
// [CONTEXT]: Debug empty folder issue, find edge cases
// [GOAL]: Identify and fix why video generation fails silently
"""

import os
import sys
from pathlib import Path
import traceback
import time

def debug_empty_folder():
    """Debug the empty folder issue step by step"""
    
    print("🔍 DEBUGGING EMPTY FOLDER ISSUE")
    print("=" * 50)
    
    # Step 1: Check folder status
    print("📁 STEP 1: Folder Status")
    folder = Path('real-ai-peter-test')
    print(f"   Folder exists: {folder.exists()}")
    
    if folder.exists():
        files = list(folder.iterdir())
        print(f"   Files count: {len(files)}")
        for f in files:
            size = f.stat().st_size if f.is_file() else 0
            print(f"   - {f.name}: {size} bytes")
    else:
        print("   Creating folder for testing...")
        folder.mkdir(exist_ok=True)
    
    # Step 2: Test basic file operations
    print("\n📝 STEP 2: File Operations Test")
    try:
        test_file = folder / "test_file.txt"
        test_file.write_text("Test content")
        print(f"   ✅ File creation: {test_file.exists()}")
        
        # Clean up
        test_file.unlink()
        print("   ✅ File deletion: Success")
        
    except Exception as e:
        print(f"   ❌ File operations failed: {e}")
        return False
    
    # Step 3: Test AI imports
    print("\n🤖 STEP 3: AI Dependencies Test")
    try:
        import torch
        print(f"   ✅ PyTorch: {torch.__version__}")
        print(f"   🔥 CUDA: {torch.cuda.is_available()}")
        
        from diffusers import AutoPipelineForText2Image
        print("   ✅ Diffusers: Available")
        
        # Test model loading (quick check)
        print("   🔄 Testing model loading...")
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float32,
            variant=None,
            use_safetensors=True,
            low_cpu_mem_usage=True
        )
        print("   ✅ Model loading: Success")
        
        return True
        
    except Exception as e:
        print(f"   ❌ AI dependencies failed: {e}")
        traceback.print_exc()
        return False
    
    # Step 4: Test image generation
    print("\n🎨 STEP 4: Image Generation Test")
    try:
        print("   🔄 Generating test image...")
        
        image = pipe(
            prompt="Mount Kenya snow peaks",
            num_inference_steps=1,  # Minimal for testing
            guidance_scale=0.0,
            height=256,  # Small for speed
            width=256
        ).images[0]
        
        # Save test image
        test_image = folder / "debug_test_image.png"
        image.save(test_image)
        
        if test_image.exists():
            size = test_image.stat().st_size / 1024
            print(f"   ✅ Image generation: Success ({size:.1f} KB)")
            return True
        else:
            print("   ❌ Image not saved")
            return False
            
    except Exception as e:
        print(f"   ❌ Image generation failed: {e}")
        traceback.print_exc()
        return False

def fix_real_ai_peter_test():
    """Create a fixed version of the real AI Peter test"""
    
    print("\n🔧 CREATING FIXED REAL AI PETER TEST")
    print("=" * 50)
    
    try:
        import torch
        from diffusers import AutoPipelineForText2Image
        import cv2
        import numpy as np
        
        # Create output folder
        output_folder = Path("real-ai-peter-test")
        output_folder.mkdir(exist_ok=True)
        
        print("🤖 Loading SDXL-Turbo...")
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float32,
            variant=None,
            use_safetensors=True,
            low_cpu_mem_usage=True
        )
        
        print("🎨 Generating real AI Kenya image...")
        image = pipe(
            prompt="Mount Kenya with snow-capped peaks, Kenya flag, beautiful landscape, photorealistic",
            num_inference_steps=2,
            guidance_scale=0.0,
            height=720,
            width=1280
        ).images[0]
        
        # Save AI image
        ai_image_path = output_folder / "real_ai_kenya_fixed.png"
        image.save(ai_image_path)
        
        file_size = ai_image_path.stat().st_size / 1024
        print(f"✅ AI image saved: {ai_image_path} ({file_size:.1f} KB)")
        
        # Create simple video
        print("🎬 Creating video...")
        
        # Convert to OpenCV
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Video settings
        fps = 30
        duration = 3
        total_frames = fps * duration
        
        video_path = output_folder / "real_ai_peter_fixed.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(video_path), fourcc, fps, (1280, 720))
        
        if not writer.isOpened():
            print("❌ Video writer failed")
            return False
        
        # Create frames
        for frame_num in range(total_frames):
            frame = cv_image.copy()
            
            # Add frame number for verification
            cv2.putText(frame, f"Frame {frame_num}", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            writer.write(frame)
        
        writer.release()
        
        if video_path.exists():
            video_size = video_path.stat().st_size / (1024*1024)
            print(f"✅ Video created: {video_path} ({video_size:.1f} MB)")
            
            # List all files
            print(f"\n📋 FILES IN {output_folder}:")
            for file in output_folder.iterdir():
                if file.is_file():
                    size = file.stat().st_size / 1024
                    print(f"   📄 {file.name}: {size:.1f} KB")
            
            return True
        else:
            print("❌ Video not created")
            return False
            
    except Exception as e:
        print(f"❌ Fixed generation failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run debugging and fix"""
    
    print("🔍 REAL AI PETER TEST DEBUGGING & FIX")
    print("=" * 60)
    
    # Debug the issue
    debug_success = debug_empty_folder()
    
    if debug_success:
        print("\n🔧 Debugging successful, creating fixed version...")
        fix_success = fix_real_ai_peter_test()
        
        if fix_success:
            print("\n🎉 FIXED REAL AI PETER TEST COMPLETE!")
            print("📁 Check real-ai-peter-test folder for results")
        else:
            print("\n❌ Fix failed")
    else:
        print("\n❌ Debugging failed - AI models not working")

if __name__ == "__main__":
    main()
