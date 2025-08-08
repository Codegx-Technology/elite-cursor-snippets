#!/bin/bash

# 🔥 Shujaa Studio Setup Script
# Complete AI Video Generator Setup for African Content Creation

set -e  # Exit on any error

echo "🔥 Welcome to Shujaa Studio Setup!"
echo "Setting up your African AI Video Generator..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on Windows/WSL
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    print_warning "Detected Windows environment"
    PYTHON_CMD="python"
    PIP_CMD="pip"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

print_status "Using Python command: $PYTHON_CMD"

# 1. Check Python version
print_status "Checking Python version..."
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
print_success "Python version: $PYTHON_VERSION"

if [[ $(echo "$PYTHON_VERSION < 3.8" | bc -l) -eq 1 ]]; then
    print_error "Python 3.8+ required. Current version: $PYTHON_VERSION"
    exit 1
fi

# 2. Create virtual environment
print_status "Creating virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# 3. Activate virtual environment
print_status "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# 4. Upgrade pip
print_status "Upgrading pip..."
$PIP_CMD install --upgrade pip

# 5. Install core dependencies
print_status "Installing core dependencies..."
$PIP_CMD install -r requirements.txt

# 6. Create directory structure
print_status "Creating directory structure..."
mkdir -p models/{tts,llm,img,music}
mkdir -p output
mkdir -p temp
mkdir -p scripts

print_success "Directory structure created"

# 7. Download lightweight models (optional)
print_status "Setting up AI models..."

# Whisper model (for subtitles)
print_status "Downloading Whisper model..."
$PYTHON_CMD -c "
import whisper
print('Downloading Whisper base model...')
model = whisper.load_model('base')
print('Whisper model ready!')
"

# 8. Setup TTS (pyttsx3)
print_status "Testing TTS engine..."
$PYTHON_CMD -c "
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
print(f'TTS engine ready with {len(voices)} voices')
"

# 9. Test image generation capabilities
print_status "Testing image generation..."
$PYTHON_CMD -c "
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Create test image
img = Image.new('RGB', (512, 512), color='#1a4d80')
draw = ImageDraw.Draw(img)
draw.text((50, 250), 'Shujaa Studio Test', fill='white')
img.save('test_image.png')
print('Image generation test successful')
"

# 10. Test video processing
print_status "Testing video processing capabilities..."
$PYTHON_CMD -c "
import moviepy.editor as mpy
import numpy as np

# Create test video
def create_test_video():
    # Create a simple test video
    frames = []
    for i in range(30):  # 1 second at 30fps
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        frames.append(frame)
    
    clip = mpy.ImageSequenceClip(frames, fps=30)
    clip.write_videofile('test_video.mp4', verbose=False, logger=None)
    print('Video processing test successful')

create_test_video()
"

# 11. Create configuration file
print_status "Creating configuration file..."
cat > config.json << EOF
{
    "models_dir": "models",
    "output_dir": "output",
    "temp_dir": "temp",
    "default_language": "English",
    "default_style": "African storytelling",
    "video_settings": {
        "fps": 24,
        "resolution": "512x512",
        "codec": "libx264"
    },
    "audio_settings": {
        "sample_rate": 22050,
        "codec": "aac"
    }
}
EOF

print_success "Configuration file created"

# 12. Create quick start script
print_status "Creating quick start script..."
cat > run_studio.sh << 'EOF'
#!/bin/bash
# Quick start script for Shujaa Studio

echo "🔥 Starting Shujaa Studio..."

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Check if prompt provided
if [ $# -eq 0 ]; then
    echo "🌐 Launching web interface..."
    python generate_video.py
else
    echo "🎬 Generating video from prompt: $*"
    python generate_video.py "$*"
fi
EOF

chmod +x run_studio.sh
print_success "Quick start script created"

# 13. Create model download script
print_status "Creating model download script..."
cat > download_models.sh << 'EOF'
#!/bin/bash
# Model download script for Shujaa Studio

echo "📥 Downloading AI models for Shujaa Studio..."

# Create models directory
mkdir -p models/{tts,llm,img,music}

# Download Stable Diffusion model (optional - large file)
echo "📥 Downloading Stable Diffusion model..."
if [ ! -f "models/img/sd15.ckpt" ]; then
    echo "Downloading Stable Diffusion 1.5 (4GB)..."
    wget -O models/img/sd15.ckpt https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt
else
    echo "Stable Diffusion model already exists"
fi

# Download Bark model (optional)
echo "📥 Downloading Bark TTS model..."
if [ ! -f "models/tts/bark_small.pth" ]; then
    echo "Downloading Bark small model (400MB)..."
    wget -O models/tts/bark_small.pth https://huggingface.co/suno/bark/resolve/main/bark_small.pth
else
    echo "Bark model already exists"
fi

echo "✅ Model download complete!"
echo "Note: You can run without these models - Shujaa Studio will use fallbacks"
EOF

chmod +x download_models.sh
print_success "Model download script created"

# 14. Test the main application
print_status "Testing Shujaa Studio..."
$PYTHON_CMD -c "
from generate_video import ShujaaStudio
studio = ShujaaStudio()
print('✅ Shujaa Studio initialized successfully!')
"

# 15. Final setup summary
print_success "🎉 Shujaa Studio setup complete!"
echo ""
echo "📁 Directory structure:"
echo "  ├── models/          # AI models (optional downloads)"
echo "  ├── output/          # Generated videos"
echo "  ├── temp/            # Temporary files"
echo "  ├── scripts/         # Additional scripts"
echo "  ├── venv/            # Virtual environment"
echo "  ├── generate_video.py # Main application"
echo "  ├── run_studio.sh    # Quick start script"
echo "  └── download_models.sh # Model download script"
echo ""
echo "🚀 Quick Start:"
echo "  ./run_studio.sh                    # Launch web interface"
echo "  ./run_studio.sh 'Your story here'  # Generate video from prompt"
echo ""
echo "📥 Optional Model Downloads:"
echo "  ./download_models.sh               # Download AI models (4GB+)"
echo ""
echo "🌐 Web Interface:"
echo "  http://localhost:7860              # When running web mode"
echo ""
echo "🔥 Ready to create African AI videos!"

# Clean up test files
rm -f test_image.png test_video.mp4

print_success "Setup completed successfully!"
