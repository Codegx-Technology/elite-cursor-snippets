#!/usr/bin/env python3
"""
🚀 Quick AI Test - Generate ONE real Kenya image to verify models work
10-second test to confirm AI models are properly synchronized

// [SNIPPET]: surgicalfix + thinkwithai + kenyafirst
// [CONTEXT]: Quick test to verify AI models work before full video generation
// [GOAL]: Generate one real AI image to confirm models are synchronized
"""

import torch
from diffusers import AutoPipelineForText2Image
import time
from pathlib import Path

def quick_ai_test():
    """Generate one real AI image quickly"""
    
    print("🚀 QUICK AI TEST - GENERATING REAL KENYA IMAGE")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Load SDXL-Turbo
        print("🔄 Loading SDXL-Turbo...")
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float32,  # CPU compatible
            variant=None
        )
        
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.1f}s")
        
        # Generate ONE real Kenya image
        print("🎨 Generating real Kenya image...")
        gen_start = time.time()
        
        image = pipe(
            prompt="Mount Kenya with snow-capped peaks, beautiful landscape, photorealistic, high quality",
            num_inference_steps=2,  # Fast generation
            guidance_scale=0.0,     # Turbo mode
            height=512,
            width=512
        ).images[0]
        
        gen_time = time.time() - gen_start
        print(f"🎉 Image generated in {gen_time:.1f}s")
        
        # Save the real AI image
        output_path = Path("test_real_ai_kenya.png")
        image.save(output_path)
        
        # Check file size
        file_size = output_path.stat().st_size / 1024
        print(f"💾 Saved: {output_path} ({file_size:.1f} KB)")
        
        total_time = time.time() - start_time
        print(f"⏱️ Total time: {total_time:.1f}s")
        
        if file_size > 100:  # Real AI images are > 100KB
            print("🎉 SUCCESS! Real AI image generated!")
            print("✅ Models are working correctly")
            return True
        else:
            print("❌ Image too small - might be placeholder")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_ai_test()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("✅ AI models work - fix video generation timeout issues")
        print("🔧 Increase timeout or optimize generation process")
    else:
        print("\n🔧 TROUBLESHOOTING NEEDED:")
        print("❌ AI models not working properly")
        print("🔍 Check model installation and dependencies")
