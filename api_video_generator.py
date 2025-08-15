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

# 60s, 6 scenes x ~10s
TOTAL_DURATION = 60
SCENE_COUNT = 6
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

assert len(SCENES) == SCENE_COUNT, "Scene count mismatch"

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


def hf_tts(text: str) -> bytes:
    url = f"https://api-inference.huggingface.co/models/{TTS_MODEL}"
    payload = {"inputs": text}
    r = requests.post(url, headers=HEADERS, json=payload, timeout=120)
    if r.status_code != 200:
        raise RuntimeError(f"tts {r.status_code}: {r.text[:200]}")
    return r.content  # expected audio bytes


def save_bytes(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def assemble_video(ts: str, scene_images: List[Path], narration_wav: Path) -> Path:
    """Assemble vertical video; add simple subtitles; try to mux audio with moviepy.
    Falls back to video-only if moviepy missing.
    """
    try:
        import cv2
        import numpy as np
    except Exception:
        print("ERROR: OpenCV (cv2) is required to compose frames. pip install opencv-python-headless")
        return None

    frames_per_scene = (TOTAL_DURATION // SCENE_COUNT) * FPS
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_path = OUTPUT_DIR / f"kenya_patriotic_60s_{ts}.mp4"
    vw = cv2.VideoWriter(str(out_path), fourcc, FPS, (WIDTH, HEIGHT))

    font = cv2.FONT_HERSHEY_SIMPLEX

    for idx, img_path in enumerate(scene_images):
        # Load and letterbox to portrait
        img = cv2.imread(str(img_path))
        if img is None:
            # create placeholder frame
            img = 255 * np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8)
            cv2.putText(img, "Image missing", (80, HEIGHT//2), font, 1, (0,0,255), 2)
        else:
            h, w = img.shape[:2]
            scale = min(WIDTH / w, HEIGHT / h)
            nw, nh = int(w * scale), int(h * scale)
            resized = cv2.resize(img, (nw, nh))
            canvas = 0 * np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8)
            x = (WIDTH - nw) // 2
            y = (HEIGHT - nh) // 2
            canvas[y:y+nh, x:x+nw] = resized
            img = canvas

        # Scene title & subtitle
        title = SCENES[idx][0]
        subtitle = SCENES[idx][1]

        for f in range(frames_per_scene):
            frame = img.copy()
            # Title
            cv2.putText(frame, title, (50, 100), font, 1.2, (255,255,255), 3)
            # Subtitle (wrapped simple)
            lines = wrap_text(subtitle, max_chars=32)
            base_y = HEIGHT - 220
            for li, line in enumerate(lines[:4]):
                cv2.putText(frame, line, (60, base_y + li*40), font, 0.9, (255,255,255), 2)
            vw.write(frame)

    vw.release()

    # Try to mux audio with moviepy
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip
        video = VideoFileClip(str(out_path))
        audio = AudioFileClip(str(narration_wav))
        # Trim/pad audio to video length
        final = video.set_audio(audio.set_duration(video.duration))
        muxed_path = OUTPUT_DIR / f"kenya_patriotic_60s_{ts}_audio.mp4"
        final.write_videofile(str(muxed_path), codec="libx264", audio_codec="aac", verbose=False, logger=None)
        try:
            os.remove(out_path)
        except Exception:
            pass
        return muxed_path
    except Exception as e:
        print(f"WARNING: moviepy mux failed or not installed: {e}")
        print("Video saved without audio. Install moviepy to mux audio: pip install moviepy")
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
    print("KENYA PATRIOTIC 60s - API PIPELINE")
    print("No local model downloads; using HF Inference API only")
    ensure_env()

    # Allow overriding timestamp via CLI arg --ts or env SHUJAA_TS
    ts = None
    try:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--ts', type=str, default=os.getenv('SHUJAA_TS'))
        args, _ = parser.parse_known_args()
        ts = args.ts
    except Exception:
        ts = os.getenv('SHUJAA_TS')
    if not ts:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    mk_dirs(ts)

    # Generate one image per scene
    scene_images: List[Path] = []
    for i, (title, line) in enumerate(SCENES, start=1):
        prompt = (
            f"High-quality vertical photo, Kenya {title.lower()}, cinematic lighting, 1080x1920, detailed, realistic, uplifting. "
            f"Elements: {line}"
        )
        print(f"[scene {i}] requesting image from {IMAGES_MODEL}...")
        try:
            img_bytes = hf_txt2img(prompt)
            img_path = IMG_DIR / ts / f"scene_{i:02d}.png"
            save_bytes(img_path, img_bytes)
            scene_images.append(img_path)
        except Exception as e:
            print(f"scene {i} image error: {e}")
            # create placeholder image
            from PIL import Image, ImageDraw
            ph = Image.new("RGB", (WIDTH, HEIGHT), (0,0,0))
            d = ImageDraw.Draw(ph)
            d.text((40, 40), f"Scene {i}: {title}", fill=(255,255,255))
            ph_path = IMG_DIR / ts / f"scene_{i:02d}_placeholder.png"
            ph.save(ph_path)
            scene_images.append(ph_path)

    # TTS narration (concatenate lines)
    narration_text = " ".join([s[1] for s in SCENES])
    print(f"Requesting TTS from {TTS_MODEL}...")
    try:
        audio_bytes = hf_tts(narration_text)
        wav_path = AUDIO_DIR / ts / "narration.wav"
        save_bytes(wav_path, audio_bytes)
    except Exception as e:
        print(f"TTS error: {e}")
        # create 1s silent wav as fallback
        wav_path = AUDIO_DIR / ts / "narration.wav"
        try:
            import wave, struct
            fr = 16000
            with wave.open(str(wav_path), 'w') as wf:
                wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(fr)
                for _ in range(fr):
                    wf.writeframes(struct.pack('<h', 0))
        except Exception:
            pass

    # Compose video
    out = assemble_video(ts, scene_images, wav_path)
    if out and Path(out).exists():
        print("SUCCESS: Video created:", out)
        print("Images in:", IMG_DIR / ts)
        print("Audio in:", AUDIO_DIR / ts)
    else:
        print("FAILED: Video assembly failed")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Fatal error:", e)
        traceback.print_exc()
        sys.exit(1)
