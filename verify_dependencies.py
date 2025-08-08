"""
Script to verify all required dependencies for Shujaa Studio are installed and compatible
"""
import sys
import subprocess
from pathlib import Path

def check_package(package_name, min_version=None):
    """Check if a package is installed and meets version requirements"""
    try:
        if package_name == 'torch' or package_name == 'torchaudio' or package_name == 'torchvision':
            # Special handling for PyTorch packages to check for CPU-only version
            import torch
            import torchaudio
            import torchvision
            
            torch_version = torch.__version__
            torch_has_cuda = torch.cuda.is_available()
            torch_cuda = "(CUDA enabled)" if torch_has_cuda else "(CPU only)"
            print(f"✓ torch: {torch_version} {torch_cuda}")
            
            torchaudio_version = torchaudio.__version__
            print(f"✓ torchaudio: {torchaudio_version}")
            
            torchvision_version = torchvision.__version__
            print(f"✓ torchvision: {torchvision_version}")
            
            if torch_has_cuda:
                print("  WARNING: CUDA is available but we want CPU-only for this environment")
            
            return True
            
        elif package_name == 'ffmpeg':
            # Check if FFmpeg is installed and in PATH
            try:
                result = subprocess.run(
                    ['ffmpeg', '-version'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                if result.returncode == 0 and 'ffmpeg version' in result.stdout:
                    version_line = result.stdout.split('\n')[0].strip()
                    print(f"✓ {package_name}: {version_line}")
                    return True
                else:
                    print(f"✗ {package_name}: Not found or not working")
                    return False
            except (FileNotFoundError, subprocess.SubprocessError):
                print(f"✗ {package_name}: Not found in PATH")
                return False
                
        else:
            # For all other packages
            module = __import__(package_name)
            version = getattr(module, '__version__', 'unknown version')
            print(f"✓ {package_name}: {version}")
            
            # Check minimum version if specified
            if min_version:
                from packaging import version
                if version.parse(version) < version.parse(min_version):
                    print(f"  WARNING: {package_name} version {version} is below minimum required {min_version}")
                    return False
            return True
            
    except ImportError:
        print(f"✗ {package_name}: Not installed")
        return False
    except Exception as e:
        print(f"✗ {package_name}: Error checking - {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Shujaa Studio Dependency Checker")
    print("=" * 60)
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Current directory: {Path.cwd()}")
    print("\nChecking required packages...\n")
    
    # List of required packages with optional minimum versions
    required_packages = [
        ('torch', '2.0.0'),
        ('torchaudio', '2.0.0'),
        ('torchvision', '0.15.0'),
        ('numpy', '1.20.0'),
        ('Pillow', '8.0.0'),
        ('moviepy', '1.0.0'),
        ('soundfile', '0.10.0'),
        ('transformers', '4.25.0'),
        ('diffusers', '0.10.0'),
        ('gradio', '3.0.0'),
        ('numba', '0.56.0'),
        ('ffmpeg', None),  # Special case, checked separately
        ('ffmpeg-python', '0.2.0'),
        ('pyttsx3', '2.90'),
    ]
    
    all_ok = True
    for pkg in required_packages:
        if len(pkg) == 2:
            pkg_name, min_version = pkg
            if not check_package(pkg_name, min_version):
                all_ok = False
        else:
            if not check_package(pkg[0]):
                all_ok = False
    
    # Check for CUDA
    try:
        import torch
        if torch.cuda.is_available():
            print("\nWARNING: CUDA is available but we're using CPU-only mode")
            print("If you want to use GPU, ensure all PyTorch packages are CUDA-enabled")
    except:
        pass
    
    # Check FFmpeg in PATH
    print("\nChecking FFmpeg in PATH...")
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if result.returncode == 0 and 'ffmpeg version' in result.stdout:
            version_line = result.stdout.split('\n')[0].strip()
            print(f"✓ FFmpeg found in PATH: {version_line}")
        else:
            print("✗ FFmpeg not found in PATH or not working")
            all_ok = False
    except (FileNotFoundError, subprocess.SubprocessError):
        print("✗ FFmpeg not found in PATH")
        all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ All dependencies are installed and compatible!")
    else:
        print("❌ Some dependencies are missing or incompatible. Please check the warnings above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
