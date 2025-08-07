# 🔥 Shujaa Studio - African AI Video Generator

Transform your stories into videos with AI - **100% Offline, 100% African**

## 🎯 What is Shujaa Studio?

Shujaa Studio is an offline AI video generator that creates videos from text prompts. Perfect for:
- **Youth Content**: Sheng cartoons, music videos, storytelling
- **Civic Education**: Anti-corruption explainers, election guides  
- **Cultural Stories**: Luo folktales, Kikuyu legends, Swahili narratives
- **Educational Content**: Localized lessons and edutainment

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Or manually:
mkdir shujaa-studio && cd shujaa-studio
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download Models (Optional)
```bash
# Create model directories
mkdir -p models/tts models/llm models/img models/music

# Download lightweight models (links provided in docs)
# - Bark TTS for voice generation
# - Stable Diffusion for image generation  
# - Whisper for subtitles
```

### 3. Run the App
```bash
# Command line mode
python generate_video.py "Tell a story of a girl from Kibera who becomes Kenya's youngest pilot"

# Web interface mode
python generate_video.py
# Then open http://localhost:7860
```

## 🛠️ Architecture

```
Prompt → Script → Voice → Images → Video
   ↓        ↓       ↓       ↓       ↓
  LLM    Mistral   Bark    SD     FFmpeg
```

### Modules:
1. **Text Generation**: Mistral 7B / LLaMA 3
2. **Voice Synthesis**: Bark / XTTS / Coqui TTS  
3. **Image Generation**: SDXL / SD 1.5
4. **Video Assembly**: FFmpeg / MoviePy
5. **Subtitles**: Whisper
6. **Optional**: Lip sync (SadTalker), Music (MusicGen)

## 📁 Project Structure
```
shujaa-studio/
├── generate_video.py    # Main pipeline
├── setup.sh            # Setup script
├── requirements.txt     # Dependencies
├── models/             # AI models
│   ├── tts/           # Text-to-speech models
│   ├── llm/           # Language models
│   ├── img/           # Image generation models
│   └── music/         # Music generation models
├── output/             # Generated videos
└── bark/              # Bark TTS repository
```

## 🎬 Usage Examples

### Basic Video Generation
```python
from generate_video import ShujaaStudio

studio = ShujaaStudio()
video_path = studio.generate_video("A Luo folktale about the clever hare")
print(f"Video saved to: {video_path}")
```

### Web Interface
```bash
python generate_video.py
# Open browser to http://localhost:7860
```

## 🔧 Configuration

### Model Paths
Edit `generate_video.py` to point to your model locations:
```python
self.models_dir = Path("/path/to/your/models")
```

### External SSD Setup
```bash
# Mount external drive in WSL
sudo mount /dev/sdX /mnt/external

# Symlink models to external drive
ln -s /mnt/external/ai_models models
```

## 🎯 Use Cases

### Kenyan Context
- **Youth Content**: AI Sheng cartoons, music videos
- **Civic Education**: Anti-corruption explainers, election guides
- **Cultural Stories**: Luo/Kikuyu/Luhya legends
- **Educational**: Localized edutainment lessons
- **Entertainment**: Benga music video generator

### NGO Applications
- Community empowerment animations
- Health education videos
- Agricultural training content
- Women empowerment stories

## 🚀 Advanced Features

### Local Language Support
- Swahili voice synthesis
- Sheng text generation
- Local accent training
- Cultural context awareness

### Offline Deployment
- Docker containerization
- PyInstaller packaging
- LAN server deployment
- Mobile app integration

## 🤝 Contributing

This is an open-source project for African AI sovereignty. Contributions welcome!

### Development Setup
```bash
git clone <repository>
cd shujaa-studio
pip install -r requirements.txt
python generate_video.py
```

## 📄 License

MIT License - Free for African content creators

## 🔗 Related Projects

- **Astella Plug**: OSINT toolkit integration
- **GhostCivic**: Civic tech platform
- **LuoNation**: Cultural preservation

---

**Built with ❤️ for African storytelling sovereignty**
