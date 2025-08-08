# 🚀 Combo Pack 5: Offline + Portable AI Video Lab

## 📋 Overview

Combo Pack 5 transforms Shujaa Studio into a complete offline AI video generation system with API capabilities for Astella integration.

### 🎯 Key Features

- ✅ **FastAPI Service**: RESTful API for video generation
- ✅ **Offline Pipeline**: Complete video generation without internet
- ✅ **Portable Environment**: Works on any machine with SSD
- ✅ **Voice Engine**: TTS with multiple engines (pyttsx3, Edge TTS, Bark)
- ✅ **Music Engine**: Background music generation
- ✅ **Batch Processing**: CSV-based batch video generation
- ✅ **Vertical Video**: TikTok-ready output format

## 🏗️ Architecture

```
Shujaa Studio API (FastAPI)
├── video_api.py          # REST API endpoints
├── pipeline.py           # Main video generation pipeline
├── voice_engine.py       # TTS wrapper (pyttsx3, Edge TTS, Bark)
├── music_engine.py       # Music generation wrapper
└── test_pipeline.py      # Test suite
```

## 🚀 Quick Start

### 1. Activate Virtual Environment
```bash
.\venv\Scripts\Activate.ps1
```

### 2. Start the API Server
```bash
python video_api.py
```
Server runs at: `http://localhost:8000`

### 3. Test the Pipeline
```bash
python test_pipeline.py
```

### 4. Generate Video via API
```bash
curl -X POST "http://localhost:8000/generate-video" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "A young Kenyan entrepreneur builds an AI startup in Nairobi",
       "lang": "sheng",
       "scenes": 3,
       "vertical": true
     }'
```

## 📁 File Structure

### Core Files
- **`video_api.py`**: FastAPI service with endpoints
  - `POST /generate-video`: Generate video from prompt
  - `GET /videos/{video_id}`: Get video info
  - `GET /list-videos`: List all generated videos
  - `GET /health`: Health check

- **`pipeline.py`**: Main video generation pipeline
  - Scene splitting
  - TTS generation
  - Image generation (SDXL/SD1.5)
  - Music generation
  - Video composition
  - Subtitle generation

- **`voice_engine.py`**: TTS wrapper
  - pyttsx3 (offline)
  - Edge TTS (online)
  - Bark (future implementation)

- **`music_engine.py`**: Music generation
  - Simple tone generation
  - Music library integration
  - Mood-based music selection

## 🔧 Configuration

### Pipeline Configuration (`pipeline.py`)
```python
CONFIG = {
    "BARK_CLI": "./voice_engine.py",
    "SDXL_PRETRAINED": "./models/sdxl",
    "MUSICGEN_SCRIPT": "./music_engine.py",
    "WHISPER_CMD": "whisper",
    "FFMPEG": "ffmpeg",
    "WORK_BASE": "./temp",
    "USE_CUDA": False,
    "DEFAULT_SCENES": 3,
    "FALLBACK_IMAGE": "./temp/default_scene.png",
    "VIDEO_FPS": 24,
    "VIDEO_WIDTH": 1080,
    "VIDEO_HEIGHT": 1920,
}
```

## 🎬 Usage Examples

### 1. Direct Pipeline Usage
```bash
# Single video generation
python pipeline.py --prompt "A boy in Kibera learns AI and builds a startup" \
                   --out ./outputs/kibera_story.mp4 \
                   --scenes 3 --vertical

# Batch processing
python pipeline.py --batch prompts.csv
```

### 2. API Usage
```python
import requests

# Generate video
response = requests.post("http://localhost:8000/generate-video", json={
    "prompt": "African innovation story",
    "lang": "sheng",
    "scenes": 3,
    "vertical": True
})

video_id = response.json()["video_id"]
print(f"Video generated: {video_id}")
```

### 3. Voice Engine Usage
```bash
# Generate TTS
python voice_engine.py --input text.txt --output audio.wav --engine pyttsx3

# Edge TTS
python voice_engine.py --input text.txt --output audio.wav --engine edge --voice en-US-AriaNeural
```

### 4. Music Engine Usage
```bash
# Generate background music
python music_engine.py --prompt "African traditional music" --out music.mp3

# Simple tone
python music_engine.py --prompt "technology" --out tech_music.mp3 --engine simple
```

## 📊 API Endpoints

### POST /generate-video
Generate a video from a prompt.

**Request:**
```json
{
  "prompt": "Your story here",
  "lang": "sheng",
  "scenes": 3,
  "vertical": true,
  "output_format": "mp4"
}
```

**Response:**
```json
{
  "status": "success",
  "video_id": "abc12345",
  "video_path": "videos/abc12345.mp4",
  "message": "Video generated successfully"
}
```

### GET /videos/{video_id}
Get information about a generated video.

**Response:**
```json
{
  "video_id": "abc12345",
  "path": "videos/abc12345.mp4",
  "size_bytes": 1024000,
  "exists": true
}
```

### GET /list-videos
List all generated videos.

**Response:**
```json
{
  "videos": [
    {
      "video_id": "abc12345",
      "filename": "abc12345.mp4",
      "size_bytes": 1024000,
      "created": 1640995200
    }
  ]
}
```

## 🔄 Batch Processing

Create a CSV file (`prompts.csv`) for batch processing:

```csv
prompt,lang,out
"A boy in Mathare learns robotics",sheng,./outputs/video1.mp4
"A Luo folktale about a clever hare",luo,./outputs/video2.mp4
"Kenyan tech innovation story",sheng,./outputs/video3.mp4
```

Run batch processing:
```bash
python pipeline.py --batch prompts.csv
```

## 🛠️ Development

### Testing
```bash
# Run test suite
python test_pipeline.py

# Test individual components
python voice_engine.py --input test.txt --output test.wav
python music_engine.py --prompt "test" --out test.mp3
```

### Adding New TTS Engines
1. Add new function in `voice_engine.py`
2. Update argument parser
3. Add to main function

### Adding New Music Engines
1. Add new function in `music_engine.py`
2. Update argument parser
3. Add to main function

## 🚀 Deployment

### Local Development
```bash
# Start API server
python video_api.py

# Access API docs
open http://localhost:8000/docs
```

### Production Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Start with uvicorn
uvicorn video_api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "video_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```bash
   # Install FFmpeg
   # Windows: Download from https://ffmpeg.org/
   # Linux: sudo apt install ffmpeg
   ```

2. **TTS not working**
   ```bash
   # Check pyttsx3 installation
   pip install pyttsx3
   ```

3. **Memory issues with SDXL**
   ```python
   # In pipeline.py, set:
   "USE_CUDA": False
   ```

4. **API timeout**
   ```python
   # Increase timeout in video_api.py
   timeout=600  # 10 minutes
   ```

## 📈 Performance Optimization

### For Production Use
1. **GPU Acceleration**: Set `USE_CUDA: True` in pipeline config
2. **Model Caching**: Pre-load SDXL models
3. **Parallel Processing**: Use multiple workers
4. **SSD Storage**: Store models on SSD for faster access

### Memory Management
- Use attention slicing for SDXL
- Enable memory efficient attention
- Clear GPU cache after each generation

## 🔮 Future Enhancements

### Planned Features
- [ ] Bark TTS integration
- [ ] MusicGen integration
- [ ] Real-time video streaming
- [ ] WebSocket support for progress updates
- [ ] Advanced subtitle styling
- [ ] Multiple video formats (WebM, MOV)
- [ ] Video effects and transitions
- [ ] Multi-language support (Sheng, Swahili, Luo)

### Integration with Astella
- [ ] Authentication and API keys
- [ ] Rate limiting
- [ ] User management
- [ ] Video analytics
- [ ] Content moderation

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Run `python test_pipeline.py` to verify setup
3. Check logs in `temp/` directory
4. Verify all dependencies are installed

---

**🎉 Combo Pack 5 is ready for production use!**

The Shujaa Studio now has a complete offline AI video generation pipeline with API capabilities for seamless integration with Astella and other systems.
