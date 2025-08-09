#!/usr/bin/env python3
"""
🔄 Restart Downloads - Resume AI Model Downloads After Computer Restart
Handle FFmpeg installation and resume SDXL-Turbo download

// [SNIPPET]: surgicalfix + thinkwithai + kenyafirst
// [CONTEXT]: Resume downloads after computer restart
// [GOAL]: Get all AI models and FFmpeg working again
"""

import os
import sys
import subprocess
import zipfile
from pathlib import Path
import shutil

def restart_downloads():
    """Restart all necessary downloads and installations"""
    
    print("🔄 RESTARTING DOWNLOADS AFTER COMPUTER RESTART")
    print("=" * 70)
    
    # 1. Handle FFmpeg installation
    handle_ffmpeg_installation()
    
    # 2. Check and install Python packages
    install_python_packages()
    
    # 3. Download AI models
    download_ai_models()
    
    # 4. Test everything
    test_installations()

def handle_ffmpeg_installation():
    """Handle FFmpeg installation from desktop file"""
    
    print("🎬 HANDLING FFMPEG INSTALLATION")
    print("-" * 40)
    
    desktop_path = Path.home() / "Desktop"
    ffmpeg_files = list(desktop_path.glob("ffmpeg*"))
    
    if ffmpeg_files:
        ffmpeg_file = ffmpeg_files[0]
        print(f"📁 Found FFmpeg file: {ffmpeg_file.name}")
        
        if ffmpeg_file.suffix.lower() == '.zip':
            print("📦 Extracting FFmpeg ZIP file...")
            try:
                # Extract to a temporary location
                extract_dir = Path.home() / "ffmpeg_temp"
                extract_dir.mkdir(exist_ok=True)
                
                with zipfile.ZipFile(ffmpeg_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                
                # Find the ffmpeg.exe file
                ffmpeg_exe = None
                for exe_file in extract_dir.rglob("ffmpeg.exe"):
                    ffmpeg_exe = exe_file
                    break
                
                if ffmpeg_exe:
                    # Copy to a permanent location
                    ffmpeg_dir = Path("C:/ffmpeg/bin")
                    ffmpeg_dir.mkdir(parents=True, exist_ok=True)
                    
                    shutil.copy2(ffmpeg_exe, ffmpeg_dir / "ffmpeg.exe")
                    
                    # Add to PATH (for current session)
                    current_path = os.environ.get("PATH", "")
                    if str(ffmpeg_dir) not in current_path:
                        os.environ["PATH"] = f"{ffmpeg_dir};{current_path}"
                    
                    print(f"✅ FFmpeg installed to: {ffmpeg_dir}")
                    print("✅ Added to PATH for current session")
                    
                    # Clean up
                    shutil.rmtree(extract_dir)
                    
                    # Test FFmpeg
                    try:
                        result = subprocess.run(["ffmpeg", "-version"], 
                                              capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            print("✅ FFmpeg working correctly")
                        else:
                            print("⚠️ FFmpeg installed but not responding")
                    except:
                        print("⚠️ FFmpeg installed but not in PATH")
                else:
                    print("❌ Could not find ffmpeg.exe in ZIP file")
                    
            except Exception as e:
                print(f"❌ Error extracting FFmpeg: {e}")
        else:
            print("📁 FFmpeg file is not a ZIP, checking if it's executable...")
            
    else:
        print("📁 No FFmpeg file found on desktop")
        print("🔄 Installing FFmpeg via winget...")
        try:
            subprocess.run(["winget", "install", "ffmpeg"], check=True)
            print("✅ FFmpeg installed via winget")
        except:
            print("⚠️ Winget installation failed, FFmpeg may need manual installation")

def install_python_packages():
    """Install/reinstall necessary Python packages"""
    
    print("\n📚 INSTALLING PYTHON PACKAGES")
    print("-" * 40)
    
    packages = [
        "torch",
        "torchvision", 
        "torchaudio",
        "diffusers",
        "transformers",
        "accelerate",
        "opencv-python",
        "pillow",
        "librosa",
        "soundfile",
        "gradio"
    ]
    
    for package in packages:
        print(f"📦 Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package, "--upgrade"], 
                          check=True, capture_output=True)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"   ⚠️ {package} installation failed")

def download_ai_models():
    """Download AI models that were lost after restart"""
    
    print("\n🤖 DOWNLOADING AI MODELS")
    print("-" * 40)
    
    try:
        # Import after package installation
        from diffusers import AutoPipelineForText2Image
        import torch
        
        print("🔄 Downloading SDXL-Turbo (this will take a few minutes)...")
        
        # Download SDXL-Turbo
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            variant="fp16" if torch.cuda.is_available() else None
        )
        
        print("✅ SDXL-Turbo downloaded successfully")
        
        # Test generation
        print("🎨 Testing image generation...")
        test_image = pipe(
            "Mount Kenya snow-capped peak, beautiful landscape, photorealistic",
            num_inference_steps=1,
            guidance_scale=0.0,
            height=512,
            width=512
        ).images[0]
        
        # Save test image
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        test_image.save(output_dir / "test_mount_kenya.png")
        
        print("✅ Test image generated and saved")
        print(f"📁 Test image: {output_dir / 'test_mount_kenya.png'}")
        
    except Exception as e:
        print(f"❌ Error downloading AI models: {e}")
        import traceback
        traceback.print_exc()

def test_installations():
    """Test all installations"""
    
    print("\n🧪 TESTING INSTALLATIONS")
    print("-" * 40)
    
    # Test Python packages
    test_packages = ["torch", "cv2", "PIL", "diffusers"]
    for package in test_packages:
        try:
            __import__(package)
            print(f"✅ {package}: Working")
        except ImportError:
            print(f"❌ {package}: Missing")
    
    # Test FFmpeg
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg: Working")
        else:
            print("❌ FFmpeg: Not responding")
    except:
        print("❌ FFmpeg: Not found")
    
    # Test CUDA
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA: Available ({torch.cuda.get_device_name(0)})")
        else:
            print("⚠️ CUDA: Not available (using CPU)")
    except:
        print("❌ CUDA: Cannot check")

def main():
    """Main function"""
    
    print("🔄 STARTING DOWNLOAD RESTART PROCESS")
    print("🖥️ Handling post-restart system recovery")
    print("=" * 70)
    
    restart_downloads()
    
    print("\n🎉 DOWNLOAD RESTART COMPLETE!")
    print("=" * 70)
    print("✅ All systems should now be operational")
    print("🎬 Ready to generate Kenya videos with AI")
    print("📁 Check output/ folder for test image")
    print("=" * 70)

if __name__ == "__main__":
    main()
