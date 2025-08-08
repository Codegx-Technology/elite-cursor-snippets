#!/usr/bin/env python3
"""
🔍 AI Model Diagnostic Test
Quick test to identify why AI models aren't being used properly

// [SNIPPET]: surgicalfix + thinkwithai + kenyafirst
// [CONTEXT]: Diagnose AI model synchronization issues
// [GOAL]: Identify why fallback images are being used instead of real AI
"""

import sys
import os
import time
from pathlib import Path

def test_imports():
    """Test if all required packages are available"""
    print("📦 TESTING IMPORTS:")
    print("-" * 30)
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"🔥 CUDA available: {torch.cuda.is_available()}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        from diffusers import AutoPipelineForText2Image
        print("✅ Diffusers: Available")
    except ImportError as e:
        print(f"❌ Diffusers import failed: {e}")
        return False
    
    try:
        import PIL
        print(f"✅ PIL: {PIL.__version__}")
    except ImportError as e:
        print(f"❌ PIL import failed: {e}")
        return False
    
    return True

def test_model_cache():
    """Test if SDXL-Turbo model is properly cached"""
    print("\n🗂️ TESTING MODEL CACHE:")
    print("-" * 30)
    
    # Check HuggingFace cache
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    if cache_dir.exists():
        print(f"📁 Cache directory exists: {cache_dir}")
        
        # Look for SDXL-Turbo
        sdxl_dirs = list(cache_dir.glob("*sdxl-turbo*"))
        if sdxl_dirs:
            print(f"✅ Found SDXL-Turbo cache: {len(sdxl_dirs)} directories")
            for dir_path in sdxl_dirs:
                size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                print(f"   📂 {dir_path.name}: {size / (1024**3):.1f} GB")
        else:
            print("❌ No SDXL-Turbo cache found")
            return False
    else:
        print("❌ HuggingFace cache directory not found")
        return False
    
    return True

def test_quick_load():
    """Test quick model loading"""
    print("\n🤖 TESTING QUICK MODEL LOAD:")
    print("-" * 30)
    
    try:
        import torch
        from diffusers import AutoPipelineForText2Image
        
        print("🔄 Loading SDXL-Turbo (quick test)...")
        start_time = time.time()
        
        # Try to load with minimal configuration
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float32,
            variant=None,
            use_safetensors=True
        )
        
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.1f} seconds")
        
        # Test if we can move to device
        if torch.cuda.is_available():
            print("🔄 Moving to GPU...")
            pipe = pipe.to("cuda")
            print("✅ Moved to GPU successfully")
        else:
            print("🖥️ Using CPU (no GPU available)")
        
        return True
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_generation():
    """Test actual image generation"""
    print("\n🎨 TESTING IMAGE GENERATION:")
    print("-" * 30)
    
    try:
        import torch
        from diffusers import AutoPipelineForText2Image
        
        # Load model
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float32,
            variant=None
        )
        
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        
        # Generate test image
        print("🔄 Generating test image...")
        start_time = time.time()
        
        image = pipe(
            prompt="A beautiful mountain landscape in Kenya with snow-capped peaks",
            num_inference_steps=2,
            guidance_scale=0.0,
            height=512,
            width=512
        ).images[0]
        
        gen_time = time.time() - start_time
        print(f"✅ Image generated in {gen_time:.1f} seconds")
        print(f"📏 Image size: {image.size}")
        
        # Save test image
        test_output = Path("test_ai_output.png")
        image.save(test_output)
        print(f"💾 Test image saved: {test_output}")
        
        return True
        
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic tests"""
    print("🔍 AI MODEL DIAGNOSTIC TEST")
    print("=" * 50)
    
    # Run tests
    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Import tests failed - check package installation")
        return
    
    cache_ok = test_model_cache()
    if not cache_ok:
        print("\n❌ Model cache tests failed - model may not be downloaded")
        return
    
    load_ok = test_quick_load()
    if not load_ok:
        print("\n❌ Model loading failed - check model compatibility")
        return
    
    gen_ok = test_image_generation()
    if not gen_ok:
        print("\n❌ Image generation failed - check model functionality")
        return
    
    print("\n🎉 ALL TESTS PASSED!")
    print("✅ AI models are working correctly")
    print("🔧 The issue might be in the video generation logic")

if __name__ == "__main__":
    main()
