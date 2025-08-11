"""
Debug script for Shujaa Studio with detailed output and error handling
"""
import os
import sys
import time
import logging
import traceback
import platform
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

# Set up console output to handle encoding issues
if platform.system() == 'Windows':
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def setup_logging() -> Path:
    """Set up logging configuration and return the log file path"""
    try:
        # Create logs directory with error handling
        log_dir = Path("debug_logs")
        try:
            log_dir.mkdir(exist_ok=True)
            print(f"Successfully created/accessed log directory: {log_dir.absolute()}")
        except Exception as e:
            print(f"Error creating log directory: {e}")
            # Try to use current directory if log directory creation fails
            log_dir = Path(".")
            print(f"Using current directory for logs: {log_dir.absolute()}")
        
        # Create a timestamp for the log file
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"debug_{timestamp}.log"
        print(f"Log file will be created at: {log_file.absolute()}")
        
        # Clear existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            try:
                handler.close()
                root_logger.removeHandler(handler)
            except Exception as e:
                print(f"Error removing handler: {e}")
        
        # Create handlers
        handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        handlers.append(console_handler)
        
        # File handler
        try:
            file_handler = logging.FileHandler(str(log_file), encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            handlers.append(file_handler)
            print(f"Successfully created file handler for: {log_file.absolute()}")
        except Exception as e:
            print(f"Error creating file handler: {e}")
        
        # Configure root logger
        root_logger.setLevel(logging.DEBUG)
        for handler in handlers:
            root_logger.addHandler(handler)
        
        # Set log level for specific noisy loggers
        logging.getLogger('PIL').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('moviepy').setLevel(logging.INFO)
        
        # Test logging
        logger = logging.getLogger('ShujaaDebug')
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        
        print(f"Logging test complete. Check {log_file} for debug messages.")
        return log_file
        
    except Exception as e:
        print(f"CRITICAL ERROR in setup_logging: {e}")
        print("Falling back to basic console logging only.")
        logging.basicConfig(level=logging.INFO)
        return Path("debug_fallback.log")

# Initialize logging
log_file = setup_logging()
logger = logging.getLogger('ShujaaDebug')
logger.info(f"Debug logging initialized. Log file: {log_file.absolute()}")

def print_section(title: str) -> None:
    """Print a section header"""
    header = f"\n{'=' * 60}\n{title}\n{'=' * 60}"
    logger.info(header)
    try:
        print(header)
    except UnicodeEncodeError:
        # Fallback for systems with encoding issues
        print(header.encode('ascii', 'replace').decode('ascii'))

def check_imports() -> Tuple[bool, List[str]]:
    """Check if all required imports are available"""
    print_section("Checking Required Imports")
    
    required_imports = [
        ('torch', 'torch'),
        ('torchvision', 'torchvision'),
        ('torchaudio', 'torchaudio'),
        ('PIL', 'Pillow'),
        ('moviepy', 'moviepy'),
        ('numpy', 'numpy'),
        ('soundfile', 'soundfile'),
        ('transformers', 'transformers'),
        ('diffusers', 'diffusers'),
        ('gradio', 'gradio'),
        ('numba', 'numba'),
        ('pyttsx3', 'pyttsx3'),
        ('ffmpeg', 'ffmpeg-python')
    ]
    
    missing_imports = []
    
    for module, pkg_name in required_imports:
        try:
            __import__(module)
            version = 'unknown'
            if hasattr(sys.modules[module], '__version__'):
                version = sys.modules[module].__version__
            elif hasattr(sys.modules[module], 'version'):
                version = sys.modules[module].version
                
            logger.info(f"✓ {module} (v{version})")
            try:
                print(f"✓ {module} (v{version})")
            except UnicodeEncodeError:
                print(f"✓ {module} (v{version.encode('ascii', 'replace').decode('ascii')})")
        except ImportError as e:
            error_msg = str(e)
            logger.error(f"✗ {module} - {error_msg}")
            print(f"✗ {module} - {error_msg}")
            missing_imports.append((module, pkg_name))
    
    if missing_imports:
        logger.error(f"Missing {len(missing_imports)} required packages")
        print(f"\n❌ Missing {len(missing_imports)} required packages:")
        for module, pkg_name in missing_imports:
            print(f"  - {module} (install with: pip install {pkg_name})")
        return False, [m[0] for m in missing_imports]
    
    logger.info("All required imports are available")
    print("\n✅ All required imports are available")
    return True, []

def check_ffmpeg_installed() -> bool:
    """Check if FFmpeg is installed and available in PATH"""
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
            logger.info(f"FFmpeg found: {version_line}")
            print(f"✓ FFmpeg found: {version_line}")
            return True
    except (FileNotFoundError, subprocess.SubprocessError) as e:
        pass
    
    logger.warning("FFmpeg not found in PATH")
    print("⚠️  FFmpeg not found in PATH. Video processing may not work correctly.")
    print("   On Windows, download it from: https://ffmpeg.org/download.html")
    print("   Make sure to add it to your system PATH.")
    return False

def test_shujaa_studio() -> bool:
    """Test ShujaaStudio functionality"""
    print_section("Testing ShujaaStudio")
    
    try:
        logger.info("Importing ShujaaStudio from generate_video")
        print("\nImporting ShujaaStudio...")
        
        # Try to import the module with error handling
        try:
            from generate_video import ShujaaStudio
            logger.info("Successfully imported ShujaaStudio")
            print("✅ Successfully imported ShujaaStudio")
        except Exception as e:
            logger.exception("Failed to import ShujaaStudio:")
            print(f"❌ Failed to import ShujaaStudio: {str(e)}")
            print("\nError details have been logged. Common issues:")
            print("1. Missing dependencies (check above)")
            print("2. Syntax errors in generate_video.py")
            print("3. Missing model files or incorrect paths")
            return False
        
        # Create output directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"Output directory: {output_dir.absolute()}")
        print(f"\nOutput directory: {output_dir.absolute()}")
        
        # Initialize ShujaaStudio
        logger.info("Initializing ShujaaStudio with SDXL support")
        print("\nInitializing ShujaaStudio with SDXL support...")
        
        try:
            studio = ShujaaStudio()
            logger.info("ShujaaStudio initialized successfully")
            print("✅ ShujaaStudio initialized successfully")
        except Exception as e:
            logger.exception("Failed to initialize ShujaaStudio:")
            print(f"❌ Failed to initialize ShujaaStudio: {str(e)}")
            print("\nCommon initialization issues:")
            print("1. Missing or corrupted model files")
            print("2. Insufficient GPU memory")
            print("3. Incompatible dependency versions")
            return False
        
        # Test script generation
        test_prompt = "A beautiful sunset over the savannah"
        logger.info(f"Testing script generation with prompt: {test_prompt}")
        print(f"\nTesting script generation with prompt: {test_prompt}")
        
        try:
            script = studio.generate_script(test_prompt)
            if script and 'scenes' in script:
                logger.info(f"Successfully generated script with {len(script['scenes'])} scenes")
                print(f"✅ Successfully generated script with {len(script['scenes'])} scenes")
                
                # Print scene details
                for i, scene in enumerate(script['scenes'], 1):
                    scene_desc = scene.get('description', 'No description')
                    scene_narr = scene.get('narration', 'No narration')
                    
                    logger.info(f"Scene {i}: {scene_desc}")
                    print(f"\nScene {i}:")
                    try:
                        print(f"  Description: {scene_desc}")
                        print(f"  Narration: {scene_narr}")
                    except UnicodeEncodeError:
                        # Fallback for systems with encoding issues
                        print(f"  Description: {scene_desc.encode('ascii', 'replace').decode('ascii')}")
                        print(f"  Narration: {scene_narr.encode('ascii', 'replace').decode('ascii')}")
                
                return True
            else:
                logger.error("Failed to generate script or invalid script format")
                print("❌ Failed to generate script or invalid script format")
                return False
                
        except Exception as e:
            logger.exception("Error during script generation:")
            print(f"\n❌ Error during script generation: {str(e)}")
            print("\nCheck the log file for more details.")
            return False
            
    except Exception as e:
        logger.exception("Unexpected error during ShujaaStudio test:")
        print(f"\n❌ An unexpected error occurred: {str(e)}")
        print("\nCheck the log file for the full traceback.")
        return False

def main() -> int:
    """Main function"""
    print_section("🚀 Shujaa Studio Debug Tool")
    
    # Log system information
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Current working directory: {Path.cwd()}")
    logger.info(f"Python path: {sys.path}")
    
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    print(f"Current working directory: {Path.cwd()}")
    
    # Add current directory to path
    sys.path.insert(0, str(Path(__file__).parent))
    
    # Check imports
    imports_ok, missing_imports = check_imports()
    if not imports_ok:
        print("\n❌ Please install the missing packages and try again.")
        print("   You can install them with: pip install " + " ".join(missing_imports))
        return 1
    
    # Check FFmpeg
    check_ffmpeg_installed()
    
    # Test ShujaaStudio
    if not test_shujaa_studio():
        print("\n❌ ShujaaStudio test failed. Check the log file for details:")
        print(f"   {log_file.absolute()}")
        return 1
    
    print("\n✅ Debug test completed successfully!")
    print(f"Log file: {log_file.absolute()}")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.exception("Unhandled exception in main:")
        print(f"\n❌ Unhandled exception: {str(e)}")
        print(f"Check the log file for details: {log_file.absolute()}")
        sys.exit(1)
