#!/usr/bin/env python3
"""
API-only 1-minute Kenya Patriotic Video Generator
- Uses Hugging Face Inference API for text-to-image and TTS (no local model downloads)
- Stores assets under assets/generated/{images,audio}/<timestamp>/
- Assembles vertical 1080x1920 video with subtitles; tries to mux audio if moviepy is available

Prereqs:
- HF_API_KEY (or HF_TOKEN) must be set with Inference/Serverless permission
- Optional: moviepy installed for audio muxing (pip install moviepy)
"""
import os
import sys
import time
import json
import math
import traceback
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

import requests
try:
    from huggingface_hub import HfFolder  # to read token from local cache
except Exception:
    HfFolder = None

# --------------------------- 
# Config
# --------------------------- 
IMAGES_MODEL = os.getenv("HF_TEXT_TO_IMAGE_MODEL", "stabilityai/stable-diffusion-2-1")
TTS_MODEL = os.getenv("TTS_MODEL", "facebook/mms-tts-eng")
HF_TOKEN = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN") or ""

FPS = 30
WIDTH, HEIGHT = 1080, 1920  # portrait

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "output"
IMG_DIR = ROOT / "assets" / "generated" / "images"
AUDIO_DIR = ROOT / "assets" / "generated" / "audio"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

# --------------------------- 
# Scene script (abridged from kenya_video_preview.md)
# --------------------------- 
SCENES: List[Tuple[str, str]] = [
    (
        "Natural Paradise",
        "Eeh bana, Kenya yetu ni nchi ya ajabu! From the snow-capped peaks za Mount Kenya hadi the white sandy beaches za Diani, our motherland ni paradise kabisa.",
    ),
    (
        "Warm Hospitality",
        "Hapa Kenya, hospitality ni kawaida. Ukifika hapa as a visitor, utapokewa na mikono miwili. Karibu sana! Watu wetu wana moyo wa upendo.",
    ),
    (
        "Wildlife Safari",
        "Safari hapa Kenya ni experience ya lifetime. Maasai Mara ina the Great Migration; Amboseli ina elephants chini ya Kilimanjaro.",
    ),
    (
        "Modern Innovation",
        "Nairobi ni the Green City in the Sun. Technology hub inakua; young entrepreneurs wanafanya miracles.",
    ),
    (
        "Heritage & Heroes",
        "Athletes wetu kama Eliud Kipchoge, David Rudisha, na Faith Kipyegon wameweka Kenya kwa map ya dunia. Swahili heritage inadumu.",
    ),
    (
        "Unity & Love",
        "From the Indian Ocean shores to the Central highlands, Kenya ni blessed kabisa. Kenya yetu, tunakupenda!",
    ),
]

# --------------------------- 
# Helpers
# --------------------------- 

def ensure_env():
    global HF_TOKEN, HEADERS
    if not HF_TOKEN and HfFolder is not None:
        try:
            cached = HfFolder.get_token()
            if cached:
                HF_TOKEN = cached
        except Exception:
            pass
    if HF_TOKEN:
        HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
    else:
        print("WARNING: No HF token detected (env or cache). Will attempt API calls and fall back to placeholders if they fail.")

def mk_dirs(ts: str):
    OUTPUT_DIR.mkdir(exist_ok=True)
    (IMG_DIR / ts).mkdir(parents=True, exist_ok=True)
    (AUDIO_DIR / ts).mkdir(parents=True, exist_ok=True)

def hf_txt2img(prompt: str) -> bytes:
    url = f"https://api-inference.huggingface.co/models/{IMAGES_MODEL}"
    payload = {"inputs": prompt}
    r = requests.post(url, headers=HEADERS, json=payload, timeout=120)
    if r.status_code != 200:
        raise RuntimeError(f"txt2img {r.status_code}: {r.text[:200]}")
    return r.content  # expected image bytes (png/jpeg)

def save_bytes(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

def assemble_video(ts: str, scene_data: list, transition_frames: int) -> Path:
    """Assemble vertical video with Ken Burns effect and cross-fades; add simple subtitles."""
    try:
        import cv2
        import numpy as np
        import random
    except ImportError:
        print("ERROR: OpenCV (cv2) is required. pip install opencv-python-headless")
        return None

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_path = OUTPUT_DIR / f"kenya_patriotic_synced_{ts}_silent.mp4"
    vw = cv2.VideoWriter(str(out_path), fourcc, FPS, (WIDTH, HEIGHT))

    font = cv2.FONT_HERSHEY_SIMPLEX
    
    buffered_frames = []

    for idx, scene in enumerate(scene_data):
        img = cv2.imread(str(scene['image_path']))
        if img is None:
            img = 255 * np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8)
            cv2.putText(img, "Image missing", (80, HEIGHT // 2), font, 1, (0, 0, 255), 2)

        frames_per_scene = int(scene['duration'] * FPS)
        
        # --- Ken Burns Effect ---
        h, w, _ = img.shape
        zoom_factor = 1.2
        
        start_x = random.randint(0, int(w * (zoom_factor - 1) / 2))
        start_y = random.randint(0, int(h * (zoom_factor - 1) / 2))
        end_x = random.randint(int(w * (zoom_factor - 1) / 2), int(w * (zoom_factor - 1)))
        end_y = random.randint(int(h * (zoom_factor - 1) / 2), int(h * (zoom_factor - 1)))

        scene_frames = []
        for f in range(frames_per_scene):
            progress = f / frames_per_scene
            
            cur_x = int(start_x + (end_x - start_x) * progress)
            cur_y = int(start_y + (end_y - start_y) * progress)
            
            crop_w, crop_h = int(w / zoom_factor), int(h / zoom_factor)
            cropped = img[cur_y:cur_y + crop_h, cur_x:cur_x + crop_w]
            
            frame = cv2.resize(cropped, (WIDTH, HEIGHT))

            # --- Add subtitles ---
            title = scene['title']
            subtitle = scene['text']
            cv2.putText(frame, title, (50, 100), font, 1.2, (255, 255, 255), 3)
            lines = wrap_text(subtitle, max_chars=40)
            base_y = HEIGHT - 220
            for li, line in enumerate(lines[:4]):
                cv2.putText(frame, line, (60, base_y + li * 40), font, 0.9, (255, 255, 255), 2)
            
            scene_frames.append(frame)

        # --- Cross-fade Transition ---
        if buffered_frames:
            for t in range(transition_frames):
                if t < len(buffered_frames) and t < len(scene_frames):
                    alpha = t / transition_frames
                    blended_frame = cv2.addWeighted(buffered_frames[-transition_frames + t], 1 - alpha, scene_frames[t], alpha, 0)
                    buffered_frames[-transition_frames + t] = blended_frame
            
            for frame in buffered_frames[:-transition_frames]:
                vw.write(frame)
            
            buffered_frames = scene_frames
        else:
            buffered_frames = scene_frames

    for frame in buffered_frames:
        vw.write(frame)

    vw.release()
    return out_path

def wrap_text(text: str, max_chars: int = 32) -> List[str]:
    words = text.split()
    lines, cur = [], []
    cur_len = 0
    for w in words:
        if cur_len + (1 if cur else 0) + len(w) <= max_chars:
            cur.append(w)
            cur_len += (1 if cur_len else 0) + len(w)
        else:
            lines.append(" ".join(cur))
            cur, cur_len = [w], len(w)
    if cur:
        lines.append(" ".join(cur))
    return lines

# --------------------------- 
# Main
# --------------------------- 
def main():
    print("KENYA PATRIOTIC SYNCED - API PIPELINE")
    ensure_env()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    mk_dirs(ts)

    # --- 1. Generate Images ---
    scene_images: List[Path] = []
    for i, (title, line) in enumerate(SCENES, start=1):
        prompt = (
            f"High-quality vertical photo, Kenya {title.lower()}, cinematic lighting, 1080x1920, detailed, realistic, uplifting. "
            f"Elements: {line}"
        )
        print(f"[Image {i}] requesting from {IMAGES_MODEL}...")
        try:
            img_bytes = hf_txt2img(prompt)
            img_path = IMG_DIR / ts / f"scene_{i:02d}.png"
            save_bytes(img_path, img_bytes)
            scene_images.append(img_path)
        except Exception as e:
            print(f"  Image {i} error: {e}")
            scene_images.append(None) # Add placeholder

    # --- 2. Generate Audio Scene-by-Scene and Get Durations ---
    scene_data = []
    audio_clips_for_concat = []
    for i, (title, text) in enumerate(SCENES, start=1):
        print(f"[Audio {i}] Generating for scene: {title}")
        
        # Write scene text to a temporary file
        temp_text_path = ROOT / f"temp_scene_{i}.txt"
        with open(temp_text_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        audio_path = AUDIO_DIR / ts / f"scene_{i:02d}.wav"
        
        # Generate audio using voice_engine.py
        voice_engine_cmd = [
            sys.executable, "voice_engine.py",
            "--input", str(temp_text_path),
            "--output", str(audio_path),
            "--engine", "edge"
        ]
        try:
            subprocess.run(voice_engine_cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"  Voice engine failed for scene {i}: {e.stderr}")
            # Fallback: create 1s of silence
            silence_cmd = f'ffmpeg -f lavfi -i anullsrc=r=22050:cl=mono -t 1 -q:a 9 -acodec libmp3lame "{audio_path}"'
            subprocess.run(silence_cmd, shell=True, check=True)

        os.remove(temp_text_path)

        # Get audio duration using ffprobe
        duration = 0
        try:
            ffprobe_cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
            duration_str = subprocess.check_output(ffprobe_cmd, shell=True, text=True).strip()
            duration = float(duration_str)
            print(f"  Duration: {duration:.2f}s")
        except (subprocess.CalledProcessError, ValueError) as e:
            print(f"  Could not get duration for {audio_path}: {e}. Defaulting to 3s.")
            duration = 3.0
            
        scene_data.append({
            "title": title,
            "text": text,
            "image_path": scene_images[i-1],
            "audio_path": audio_path,
            "duration": duration
        })
        audio_clips_for_concat.append(audio_path)

    # --- 3. Assemble Silent Video with Transitions ---
    print("\nAssembling silent video with synced scenes and transitions...")
    transition_duration_seconds = 0.5
    transition_frames = int(transition_duration_seconds * FPS)
    silent_video_path = assemble_video(ts, scene_data, transition_frames)
    print(f"Silent video created: {silent_video_path}")

    # --- 4. Concatenate Audio Clips ---
    print("\nConcatenating audio clips...")
    concat_list_path = ROOT / "concat_list.txt"
    with open(concat_list_path, "w") as f:
        for clip in audio_clips_for_concat:
            f.write(f"file '{clip.resolve()}'\n")
            
    final_audio_path = OUTPUT_DIR / f"kenya_patriotic_synced_{ts}_full_audio.wav"
    concat_cmd = f'ffmpeg -f concat -safe 0 -i "{concat_list_path}" -c copy "{final_audio_path}"'
    try:
        subprocess.run(concat_cmd, shell=True, check=True)
        print(f"Final audio created: {final_audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"Audio concatenation failed: {e}")
        sys.exit(1)
    finally:
        os.remove(concat_list_path)

    # --- 5. Mux Final Video and Audio ---
    print("\nMuxing final video and audio...")
    final_video_path = OUTPUT_DIR / f"kenya_patriotic_synced_{ts}_FINAL.mp4"
    mux_cmd = f'ffmpeg -i "{silent_video_path}" -i "{final_audio_path}" -c:v copy -c:a aac -shortest "{final_video_path}"'
    try:
        subprocess.run(mux_cmd, shell=True, check=True)
        print(f"\nSUCCESS! Final video created: {final_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Final muxing failed: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)