#!/usr/bin/env python3
"""
gpu_news_video_pipeline.py
Usage:
  python gpu_news_video_pipeline.py --mode news --query "Kibera story" --out ./outputs/final.mp4 --scenes 4 --upload False

Behavior:
 - HF-first: tries Hugging Face Inference API for images & text models.
 - If HF unavailable or user opts, and if CUDA available, uses local diffusers.
 - TTS: tries Bark via HF API (if available), then local Bark CLI (if installed), then gTTS fallback.
 - Assembles final mp4 via ffmpeg / moviepy.

Environment variables:
 - HF_TOKEN
 - NEWSAPI_KEY
"""

import argparse
import sys
import os
import subprocess
import uuid
import requests
from pathlib import Path
from PIL import Image
import io
import base64
from typing import List

# Ensure FFMPEG is available
FFMPEG = os.environ.get("FFMPEG_PATH", "ffmpeg")
try:
    subprocess.run([FFMPEG, "-version"], check=True, capture_output=True)
except (subprocess.CalledProcessError, FileNotFoundError):
    print(f"Error: FFmpeg not found. Please install FFmpeg and ensure it's in your PATH, or set the FFMPEG_PATH environment variable.", file=sys.stderr)
    sys.exit(1)

# Google API for YouTube upload
try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    GOOGLE_API_AVAILABLE = True
except ImportError:
    print("Google API client libraries not installed. YouTube upload will be unavailable.")
    GOOGLE_API_AVAILABLE = False

# gTTS for TTS fallback
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    print("gTTS not installed. Will not be able to use gTTS fallback for TTS.")
    GTTS_AVAILABLE = False

# pydub for audio processing
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    print("pydub not installed. Some audio processing features may be limited.")
    PYDUB_AVAILABLE = False

# faster-whisper for local STT
try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    print("faster-whisper not installed. Local STT will be unavailable.")
    FASTER_WHISPER_AVAILABLE = False

# Hugging Face credentials
HF_TOKEN = os.getenv("HF_TOKEN")
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")

# HF Model IDs
HF_IMG_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
HF_TEXT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
HF_TTS_MODEL = "suno/bark"
HF_STT_MODEL = "openai/whisper-large-v2"

# Directories
TMP_DIR_NAME = "tmp_pipeline"
OUT_DIR_NAME = "outputs"
MODELS_DIR_NAME = "models"

TMP = Path(TMP_DIR_NAME)
OUT_DIR = Path(OUT_DIR_NAME)
MODELS_DIR = Path(MODELS_DIR_NAME)

TMP.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

def log(*a, **k):
    print("[pipeline]", *a, **k)
    sys.stdout.flush()

# ---------- Utilities ----------
def run_cmd(cmd):
    log("CMD>", cmd)
    r = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    if r.returncode != 0:
        log("STDOUT:", r.stdout)
        log("STDERR:", r.stderr)
        raise RuntimeError(f"cmd failed: {cmd}")
    return r.stdout

# ---------- HF Inference helpers ----------
def hf_inference_model_request(model_id, payload_json=None, timeout=30):
    if not HF_TOKEN:
        return None, "no-token"
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        r = requests.post(url, headers=headers, json=payload_json, timeout=timeout)
        if r.status_code == 200:
            return r, None
        else:
            return None, f"status:{r.status_code}:{r.text[:200]}"
    except Exception as e:
        return None, str(e)

def hf_image_generate(prompt, out_path:Path):
    r, err = hf_inference_model_request(HF_IMG_MODEL, {"inputs": prompt})
    if r is None:
        log("HF image failed:", err)
        return False
    try:
        img = Image.open(io.BytesIO(r.content))
        img.save(out_path)
        log("HF image saved", out_path)
        return True
    except Exception as e:
        log("HF image save failed", e)
        return False

def hf_text_generate(prompt):
    r, err = hf_inference_model_request(HF_TEXT_MODEL, {"inputs": prompt})
    if r is None:
        log("HF text failed:", err)
        return None
    try:
        return r.json()[0]["generated_text"]
    except Exception:
        return r.text

def hf_tts_generate(text, out_wav:Path):
    # Bark endpoints often return audio bytes.
    r, err = hf_inference_model_request(HF_TTS_MODEL, {"inputs": text})
    if r is None:
        log("HF tts failed:", err)
        return False
    try:
        with open(out_wav, "wb") as f:
            f.write(r.content)
        log("HF tts saved", out_wav)
        return True
    except Exception as e:
        log("HF tts save failed", e)
        return False

# ---------- Local GPU image generation (diffusers) ----------
USE_CUDA = False
try:
    import torch
    USE_CUDA = torch.cuda.is_available()
    log("CUDA available:", USE_CUDA)
except Exception:
    USE_CUDA = False

SD_PIPELINE = None
def local_image_generate(prompt, out_path:Path):
    global SD_PIPELINE
    if not USE_CUDA:
        log("No CUDA for local generation")
        return False
    try:
        from diffusers import StableDiffusionPipeline
        if SD_PIPELINE is None:
            # change model_dir to your local path if needed
            model_id = MODELS_DIR / "stable-diffusion-v1-5" # Example local model path
            if not model_id.exists():
                log(f"Local SD model not found at {model_id}. Please download it.")
                return False
            SD_PIPELINE = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
            SD_PIPELINE.to("cuda")
        
        image = SD_PIPELINE(prompt).images[0]
        image.save(out_path)
        log("Local SD image saved", out_path)
        return True
    except Exception as e:
        log("Local SD image failed", e)
        return False

# ---------- Local TTS (gTTS) ----------
def gtts_tts(text, out_wav:Path):
    if not GTTS_AVAILABLE:
        log("gTTS not available for local TTS fallback.")
        return False
    try:
        t = gTTS(text=text, lang='en')
        tmp_mp3 = str(out_wav.with_suffix(".mp3"))
        t.save(tmp_mp3)
        # convert to wav
        run_cmd(f'{FFMPEG} -y -i "{tmp_mp3}" -ar 22050 -ac 1 "{out_wav}"')
        Path(tmp_mp3).unlink(missing_ok=True)
        return True
    except Exception as e:
        log("gTTS failed", e)
        return False

# ---------- Local STT (faster-whisper) ----------
WHISPER_MODEL = None
def local_stt_transcribe(audio_path:Path):
    global WHISPER_MODEL
    if not FASTER_WHISPER_AVAILABLE:
        log("faster-whisper not available for local STT fallback.")
        return None
    try:
        if WHISPER_MODEL is None:
            # You might need to specify a model size like "base", "small", etc.
            # and potentially a device like "cuda" or "cpu"
            WHISPER_MODEL = WhisperModel("base", device="cuda" if USE_CUDA else "cpu", compute_type="int8")
            log("Faster Whisper model loaded.")
        
        segments, info = WHISPER_MODEL.transcribe(str(audio_path), beam_size=5)
        transcription = " ".join([segment.text for segment in segments])
        log("Local STT transcribed:", transcription[:100])
        return transcription
    except Exception as e:
        log("Local STT failed", e)
        return None

# ---------- Video Composition ----------
def make_scene_clip(img_path:Path, audio_path:Path, duration:float, out_mp4:Path):
    # Use moviepy if available, otherwise fallback to ffmpeg directly
    try:
        from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
        img_clip = ImageClip(str(img_path)).set_duration(duration)
        audio_clip = AudioFileClip(str(audio_path))
        final_clip = img_clip.set_audio(audio_clip)
        final_clip.write_videofile(str(out_mp4), fps=24, codec="libx264", audio_codec="aac")
        log("MoviePy scene clip created", out_mp4)
    except ImportError:
        log("MoviePy not available, falling back to FFmpeg for scene clip.")
        run_cmd(f'{FFMPEG} -y -loop 1 -i "{img_path}" -i "{audio_path}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "{out_mp4}"')
        log("FFmpeg scene clip created", out_mp4)

def compose_final(scene_videos:List[Path], out_file:Path):
    listf = TMP / "filelist.txt"
    with open(listf, "w") as f:
        for sv in scene_videos:
            f.write(f"file '{sv}'\n")
    run_cmd(f'{FFMPEG} -y -f concat -safe 0 -i "{listf}" -c copy "{out_file}"')
    listf.unlink(missing_ok=True)

# ---------- News fetching ----------
def fetch_news_headlines(query="Kenya", cnt=3):
    if NEWSAPI_KEY:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize={cnt}&apiKey={NEWSAPI_KEY}"
        r = requests.get(url, timeout=20)
        if r.status_code==200:
            items = r.json().get("articles", [])
            return items
        log("NewsAPI failed:", r.status_code, r.text)
    # fallback: Google News RSS
    rss = f"https://news.google.com/rss/search?q={query}+when:7d&hl=en-KE&gl=KE&ceid=KE:en"
    try:
        r = requests.get(rss, timeout=20)
        if r.status_code==200:
            # Basic XML parsing for RSS
            from xml.etree import ElementTree as ET
            root = ET.fromstring(r.content)
            items = []
            for item in root.findall('.//item'):
                title = item.find('title').text if item.find('title') is not None else ""
                description = item.find('description').text if item.find('description') is not None else ""
                items.append({"title": title, "description": description})
            return items
        log("Google News RSS failed:", r.status_code, r.text)
    except Exception as e:
        log("News fetching error:", e)
    return []

# ---------- YouTube Upload ----------
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "client_secret.json"

def get_authenticated_service():
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token: # Elite Cursor Snippet: token_save
            token.write(credentials.to_json())
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def youtube_upload(file_path:Path, title:str, description:str, tags:List[str]):
    if not GOOGLE_API_AVAILABLE:
        log("Google API client not available for YouTube upload.")
        return
    try:
        youtube = get_authenticated_service()
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22" # People & Blogs
            },
            "status": {
                "privacyStatus": "private" # or "public", "unlisted"
            }
        }
        media_body = {
            "mimeType": "video/mp4",
            "body": file_path.open("rb").read()
        }
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media_body
        )
        response = insert_request.execute()
        log(f"YouTube upload successful! Video ID: {response.get('id')}")
    except Exception as e:
        log("YouTube upload failed", e)

# ---------- Main pipeline ----------
def pipeline_news_to_video(query="Kenya", out_file=None, scenes=3, upload=False, target_duration_minutes=1.0):
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN environment variable is not set. Cannot proceed without Hugging Face API access.")

    # Calculate number of scenes based on target duration (assuming ~15 seconds per scene)
    estimated_scene_duration_seconds = 15
    required_scenes = max(1, int((target_duration_minutes * 60) / estimated_scene_duration_seconds))
    scenes = max(scenes, required_scenes) # Use the larger of user-provided scenes or calculated scenes

    items = fetch_news_headlines(query, cnt=scenes)
    if not items:
        raise RuntimeError("No news items found.")
    scene_videos = []
    for idx, art in enumerate(items, start=1):
        scene_prompt = art.get("title") or art.get("description") or f"{query} news scene {idx}"
        log("Scene prompt:", scene_prompt[:120])
        img_path = TMP / f"scene_{idx}.png"
        audio_path = TMP / f"narration_{idx}.wav"
        
        # 1) Generate image: HF first
        ok = False
        if HF_TOKEN:
            try:
                ok = hf_image_generate(scene_prompt, img_path)
            except Exception as e:
                log("hf image err", e)
        
        if not ok:
            raise RuntimeError(f"Failed to generate/fetch image for: {scene_prompt}")

        # 2) Generate audio: HF TTS first
        ok = False
        if HF_TOKEN:
            try:
                ok = hf_tts_generate(art.get("description") or art.get("title"), audio_path)
            except Exception as e:
                log("hf tts err", e)
        
        if not ok:
            raise RuntimeError(f"Failed to generate audio for: {art.get('title')}")

        # 3) Mix audio (optional music)
        final_audio = TMP / f"final_audio_{idx}.aac"
        music = None # TODO: Add music selection logic
        if music:
            run_cmd(f'{FFMPEG} -y -i "{audio_path}" -i "{music}" -filter_complex "[1:a]volume=0.25[a1];[0:a][a1]amix=inputs=2:duration=shortest" -c:a aac "{final_audio}"')
        else:
            # convert narration to mp3 as final audio
            run_cmd(f'{FFMPEG} -y -i "{audio_path}" -c:a aac "{final_audio}"')
        
        # 4) make scene clip
        scene_mp4 = TMP / f"scene_{idx}.mp4"
        # approximate duration = audio length
        try:
            import math, subprocess
            out = subprocess.check_output([FFMPEG,'-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1', str(final_audio)])
            duration = float(out.strip())
        except Exception:
            duration = 5.0
        make_scene_clip(img_path, final_audio, duration, scene_mp4)
        scene_videos.append(scene_mp4)
    
    out_file = out_file or OUT_DIR / f"news_{uuid.uuid4().hex[:6]}.mp4"
    compose_final(scene_videos, out_file)
    log("Final video", out_file)
    if upload:
        youtube_upload(out_file, f"AI News: {query}", f"AI generated news video about {query}", ["AI News", "Kenya", query])

# ---------- CLI ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["news","url","script"], default="news")
    parser.add_argument("--query", type=str, default="Kenya")
    parser.add_argument("--url", type=str, default=None)
    parser.add_argument("--script", type=str, default=None)
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--scenes", type=int, default=3)
    parser.add_argument("--upload", action="store_true", default=False)
    parser.add_argument("--duration_minutes", type=float, default=1.0, help="Target video duration in minutes")
    args = parser.parse_args()
    if args.mode=="news":
        pipeline_news_to_video(args.query, out_file=Path(args.out) if args.out else None, scenes=args.scenes, upload=args.upload, target_duration_minutes=args.duration_minutes)
    else:
        print("Other modes not implemented in this script")
