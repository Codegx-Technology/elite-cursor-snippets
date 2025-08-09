#!/usr/bin/env python3
"""
🔧 Test Timeout Patch - Verify Real AI Generation Works
Test the surgical timeout fix to ensure we get real Kenya AI content

// [SNIPPET]: surgicalfix + thinkwithai + kenyafirst
// [CONTEXT]: Test the timeout patch to verify real AI generation
// [GOAL]: Confirm we get authentic Kenya AI images, not placeholders
"""

import sys
import time
from pathlib import Path

# Add project paths
sys.path.append(str(Path(__file__).parent))

def test_timeout_patch():
    """Test the timeout patch with one scene"""
    
    print("🔧 TESTING TIMEOUT PATCH")
    print("=" * 50)
    print("🎯 Goal: Generate ONE real Kenya AI image")
    print("⏱️ Expected time: 60-120 seconds on CPU")
    print("✅ Success criteria: Image > 100KB (real AI content)")
    print("=" * 50)
    
    try:
        # Import our fixed real AI generator
        from real_ai_kenya_video import initialize_ai_generator
        
        # Test the AI generator initialization
        print("🤖 Testing AI generator initialization...")
        start_time = time.time()
        
        generator = initialize_ai_generator()
        
        if generator is None:
            print("❌ AI generator failed to initialize")
            return False
        
        init_time = time.time() - start_time
        print(f"✅ AI generator initialized in {init_time:.1f}s")
        
        # Test one image generation
        print("\n🎨 Testing image generation with timeout patch...")
        gen_start = time.time()
        
        # Generate one Kenya image
        image = generator(
            prompt="Mount Kenya with snow-capped peaks, beautiful landscape, photorealistic, high quality, Kenya",
            num_inference_steps=2,
            guidance_scale=0.0,
            height=512,
            width=512
        ).images[0]
        
        gen_time = time.time() - gen_start
        print(f"🎉 Image generated in {gen_time:.1f}s")
        
        # Save and check the image
        output_path = Path("test_timeout_patch_output.png")
        image.save(output_path)
        
        file_size = output_path.stat().st_size / 1024
        print(f"💾 Saved: {output_path} ({file_size:.1f} KB)")
        
        total_time = time.time() - start_time
        print(f"⏱️ Total time: {total_time:.1f}s")
        
        # Verify it's real AI content
        if file_size > 100:  # Real AI images are > 100KB
            print("\n🎉 SUCCESS! TIMEOUT PATCH WORKS!")
            print("✅ Generated REAL AI content (not placeholder)")
            print(f"📏 Image size: {file_size:.1f} KB (confirms real AI)")
            print("🇰🇪 Ready for authentic Kenya video generation!")
            return True
        else:
            print(f"\n❌ Image too small ({file_size:.1f} KB)")
            print("🔧 Still getting placeholder - need more investigation")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the timeout patch test"""
    
    success = test_timeout_patch()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("✅ Timeout patch successful - run full video generation")
        print("🎬 python real_ai_kenya_video.py")
        print("🇰🇪 Expect authentic Kenya AI content!")
    else:
        print("\n🔧 TROUBLESHOOTING:")
        print("❌ Timeout patch needs more work")
        print("🔍 Check model loading and generation logic")

if __name__ == "__main__":
    main()
