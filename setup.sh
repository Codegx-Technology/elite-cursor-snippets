#!/bin/bash

echo "🔥 Setting up Shujaa Studio - African AI Video Generator"
echo "========================================================"

# Create project directory
mkdir -p shujaa-studio && cd shujaa-studio
echo "✅ Created project directory"

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate
echo "✅ Created and activated virtual environment"

# Upgrade pip and install core dependencies
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers diffusers moviepy ffmpeg-python gradio faster-whisper
pip install openai-whisper
echo "✅ Installed core Python dependencies"

# Create model directories
mkdir -p models/tts models/llm models/img models/music models/whisper
echo "✅ Created model directories"

# Clone required repositories
echo "📥 Cloning model repositories..."

# Bark TTS
git clone https://github.com/suno-ai/bark
cd bark && pip install -r requirements.txt && cd ..
echo "✅ Installed Bark TTS"

# Stable Diffusion WebUI
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
echo "✅ Cloned Stable Diffusion WebUI"

# SadTalker (optional - for face/lip sync)
git clone https://github.com/OpenTalker/SadTalker
cd SadTalker && pip install -r requirements.txt && cd ..
echo "✅ Installed SadTalker"

echo "🎉 Setup complete! Next steps:"
echo "1. Download models to models/ directory"
echo "2. Run: python generate_video.py"
echo "3. Or launch UI: gradio app.py"
