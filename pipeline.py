#!/usr/bin/env python3
"""
pipeline.py
One-file script: prompt -> multi-scene video (voice, images, music, subtitles)
Usage:
    python3 pipeline.py --prompt "Your long story here" --out ./outputs/story.mp4
    python3 pipeline.py --batch prompts.csv
"""

import os
import sys
import argparse
import subprocess
import uuid
import json
import shutil
from pathlib import Path
from typing import List, Optional

# Optional imports (will fail gracefully if not present)
try:
    import torch
    from diffusers import StableDiffusionXLPipeline, StableDiffusionPipeline
except Exception:
    StableDiffusionXLPipeline = None
    StableDiffusionPipeline = None

try:
    import soundfile as sf
except Exception:
    sf = None

# -------------------------
#  CONFIG - EDIT THESE
# -------------------------
CONFIG = {
    # Local model/script paths - update these
    "BARK_CLI": "./voice_engine.py",         # CLI entry that accepts --input --output
    "SDXL_PRETRAINED": "./models/sdxl",              # path to SDXL diffusers pretrained folder (or SD1.5 ckpt)
    "MUSICGEN_SCRIPT": "./music_engine.py",  # optional wrapper script for MusicGen
    "WHISPER_CMD": "whisper",                                # command if whisper CLI installed (or faster-whisper)
    "FFMPEG": "ffmpeg",
    "WORK_BASE": "./temp",
    "USE_CUDA": False,  # set False if no GPU
    "DEFAULT_SCENES": 3,
    # SD fallback (if SDXL pipeline unavailable, you can use AUTOMATIC1111 saved images)
    "FALLBACK_IMAGE": "./temp/default_scene.png",
    # Default mux settings
    "VIDEO_FPS": 24,
    "VIDEO_WIDTH": 1080,   # for TikTok set 1080x1920; default used only for resizing
    "VIDEO_HEIGHT": 1920,
}

# -------------------------
#  Utilities
# -------------------------
def ensure_dir(p: str):
    Path(p).mkdir(parents=True, exist_ok=True)

def run_cmd(cmd: str, silent=False):
    print(f"[CMD] {cmd}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")
    return res.returncode

def safe_path(p: str) -> str:
    return os.path.abspath(str(p))

# -------------------------
#  LLM: Expand prompt -> script/scenes (optional)
#  If you have a local LLM, you can plug it here. Otherwise we naive-split prompt.
# -------------------------
def expand_prompt_to_scenes(prompt: str, n_scenes: int = 3) -> List[str]:
    """
    If you have a local LLM, replace this function to call it and return list of scene texts.
    Default behavior: naive split by length.
    """
    prompt = prompt.strip()
    if not prompt:
        return ["Scene: (empty)"]
    # naive split
    approx = max(1, len(prompt) // n_scenes)
    scenes = []
    for i in range(n_scenes):
        start = i * approx
        end = (i + 1) * approx if i < n_scenes - 1 else len(prompt)
        slice_ = prompt[start:end].strip()
        if not slice_:
            slice_ = prompt
        scenes.append(slice_)
    return scenes

# -------------------------
#  TEXT-TO-SPEECH (Bark)
#  Uses Bark CLI wrapper - ensure your gen.py accepts --input --output
# -------------------------
def tts_bark(input_txt_path: str, output_wav_path: str, bark_cli: str = None):
    bark_cli = bark_cli or CONFIG["BARK_CLI"]
    if not os.path.exists(bark_cli):
        raise FileNotFoundError(f"Bark CLI not found at {bark_cli}")
    cmd = f"python {bark_cli} --input {input_txt_path} --output {output_wav_path}"
    run_cmd(cmd)

# -------------------------
#  IMAGE GENERATION: SDXL or SD1.5
#  Uses Diffusers pipeline if available; else falls back to placeholder image.
# -------------------------
def generate_image_sdxl(prompt: str, out_path: str, sdxl_path: str = None):
    sdxl_path = sdxl_path or CONFIG["SDXL_PRETRAINED"]
    if StableDiffusionXLPipeline is None and StableDiffusionPipeline is None:
        # fallback: copy placeholder
        print("[IMG] Diffusers not installed - using placeholder image.")
        shutil.copy(CONFIG["FALLBACK_IMAGE"], out_path)
        return
    # prefer SDXL
    if StableDiffusionXLPipeline is not None and os.path.exists(sdxl_path):
        print("[IMG] Loading SDXL pipeline...")
        torch_dtype = torch.float16 if CONFIG["USE_CUDA"] else torch.float32
        device = "cuda" if (CONFIG["USE_CUDA"] and torch.cuda.is_available()) else "cpu"
        pipe = StableDiffusionXLPipeline.from_pretrained(sdxl_path, torch_dtype=torch_dtype)
        pipe = pipe.to(device)
        image = pipe(prompt, guidance_scale=7.5).images[0]
        image.save(out_path)
        # free memory
        del pipe
        if device == "cuda":
            torch.cuda.empty_cache()
        return
    # fallback to SD1.5 pipeline if available
    if StableDiffusionPipeline is not None and os.path.exists(sdxl_path):
        print("[IMG] Loading SD (1.5) pipeline...")
        device = "cuda" if (CONFIG["USE_CUDA"] and torch.cuda.is_available()) else "cpu"
        pipe = StableDiffusionPipeline.from_pretrained(sdxl_path)
        pipe = pipe.to(device)
        image = pipe(prompt, guidance_scale=7.5).images[0]
        image.save(out_path)
        del pipe
        if device == "cuda":
            torch.cuda.empty_cache()
        return
    print("[IMG] No supported diffusers pipeline found or model path missing - using placeholder.")
    shutil.copy(CONFIG["FALLBACK_IMAGE"], out_path)

# -------------------------
#  MUSIC GENERATION (optional)
#  Calls MUSICGEN_SCRIPT if present; else creates silence or skips
# -------------------------
def generate_music(prompt: str, out_music: str, music_script: Optional[str] = None):
    music_script = music_script or CONFIG["MUSICGEN_SCRIPT"]
    if music_script and os.path.exists(music_script):
        cmd = f"python {music_script} --prompt \"{prompt}\" --out {out_music}"
        run_cmd(cmd)
        return
    # fallback: generate 8s silence
    cmd = f"{CONFIG['FFMPEG']} -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t 8 {out_music}"
    run_cmd(cmd)

# -------------------------
#  MIX AUDIO: narration + music -> mixed output
# -------------------------
def mix_audio(narration_wav: str, music_file: str, out_mixed: str, music_vol: float = 0.25):
    cmd = (
        f"{CONFIG['FFMPEG']} -y -i \"{narration_wav}\" -i \"{music_file}\" "
        f"-filter_complex \"[1:a]volume={music_vol}[m];[0:a][m]amix=inputs=2:duration=shortest:dropout_transition=2[a]\" "
        f"-map \"[a]\" -c:a aac -b:a 192k \"{out_mixed}\""
    )
    run_cmd(cmd)

# -------------------------
#  SUBTITLES: generate SRT with whisper CLI (faster-whisper recommended)
# -------------------------
def generate_subtitles(audio_file: str, out_srt: str, model: str = "small"):
    # assumes 'whisper' CLI in path OR faster-whisper installed as 'whisper'
    cmd = f"{CONFIG['WHISPER_CMD']} \"{audio_file}\" --model {model} --output_format srt --output_dir {os.path.dirname(out_srt)}"
    run_cmd(cmd)
    # whisper outputs filename.srt in same dir; find it:
    basename = os.path.splitext(os.path.basename(audio_file))[0]
    candidate = os.path.join(os.path.dirname(out_srt), basename + ".srt")
    if os.path.exists(candidate):
        os.rename(candidate, out_srt)
    else:
        # if not found, create a very simple srt from audio as fallback (no timestamps)
        with open(out_srt, "w") as f:
            f.write("1\n00:00:00,000 --> 00:00:10,000\n[Transcript unavailable]\n")

# -------------------------
#  Create scene video (image + mixed audio) using ffmpeg, resized for vertical TikTok default
# -------------------------
def make_scene_video(img_path: str, audio_path: str, out_mp4: str, vertical: bool = True):
    # If vertical output desired, pad image to 1080x1920
    if vertical:
        tmp_img = img_path + ".pad.png"
        # center the image on 1080x1920 canvas
        cmd_pad = (
            f"{CONFIG['FFMPEG']} -y -i \"{img_path}\" -vf \"scale='min(1080,iw)':'min(1080,ih)':force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black\" -q:v 2 \"{tmp_img}\""
        ).format(tmp_img=tmp_img)
        # Use bash formatting directly for safety:
        cmd_pad = (
            f"{CONFIG['FFMPEG']} -y -i \"{img_path}\" -vf \"scale='min(1080,iw)':'min(1080,ih)':force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black\" -q:v 2 \"{tmp_img}\""
        ).replace("{tmp_img}", tmp_img)
        run_cmd(cmd_pad)
        img_for_ff = tmp_img
    else:
        img_for_ff = img_path

    # create mp4 with audio, shorted to audio duration
    cmd = (
        f"{CONFIG['FFMPEG']} -y -loop 1 -i \"{img_for_ff}\" -i \"{audio_path}\" -c:v libx264 -tune stillimage "
        f"-c:a aac -b:a 192k -pix_fmt yuv420p -shortest \"{out_mp4}\""
    )
    run_cmd(cmd)
    # remove pad image if created
    if vertical and os.path.exists(img_for_ff) and img_for_ff.endswith(".pad.png"):
        os.remove(img_for_ff)

# -------------------------
#  CONCAT Scenes into final video
# -------------------------
def concat_videos(video_list: List[str], out_final: str):
    tmp = os.path.join(os.path.dirname(out_final), "concat_list.txt")
    with open(tmp, "w") as f:
        for v in video_list:
            f.write(f"file '{safe_path(v)}'\n")
    cmd = f"{CONFIG['FFMPEG']} -y -f concat -safe 0 -i \"{tmp}\" -c copy \"{out_final}\""
    run_cmd(cmd)
    os.remove(tmp)

# -------------------------
#  High-level pipeline
# -------------------------
def generate_video_from_prompt(prompt: str,
                               out_video: str,
                               scenes_n: int = None,
                               vertical: bool = True,
                               lang: str = "sheng"):
    """
    Full pipeline:
    - Expand prompt -> scenes
    - For each scene: write text file, TTS (Bark), image (SDXL), music, mix audio, make scene video, subtitles
    - Concatenate scenes -> final output
    """
    print("[RUN] Starting pipeline")
    scenes_n = scenes_n or CONFIG["DEFAULT_SCENES"]
    base_run = os.path.join(CONFIG["WORK_BASE"], str(uuid.uuid4()))
    ensure_dir(base_run)
    scenes = expand_prompt_to_scenes(prompt, scenes_n)
    scene_videos = []

    for idx, scene_text in enumerate(scenes, start=1):
        print(f"[SCENE] {idx}/{len(scenes)}")
        scene_base = os.path.join(base_run, f"scene{idx}")
        ensure_dir(scene_base)
        txt_path = os.path.join(scene_base, "scene.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(scene_text)

        # 1) TTS
        wav_path = os.path.join(scene_base, "narration.wav")
        try:
            tts_bark(txt_path, wav_path, bark_cli=CONFIG["BARK_CLI"])
        except Exception as e:
            print(f"[WARN] Bark TTS failed: {e}. Attempting fallback with silence.")
            # create silence
            run_cmd(f"{CONFIG['FFMPEG']} -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=22050 -t 5 \"{wav_path}\"")

        # 2) Image gen
        img_out = os.path.join(scene_base, "image.png")
        try:
            generate_image_sdxl(scene_text, img_out, sdxl_path=CONFIG["SDXL_PRETRAINED"])
        except Exception as e:
            print(f"[WARN] Image generation failed: {e}. Using placeholder.")
            shutil.copy(CONFIG["FALLBACK_IMAGE"], img_out)

        # 3) Music gen
        music_out = os.path.join(scene_base, "music.mp3")
        try:
            generate_music(scene_text, music_out, music_script=CONFIG["MUSICGEN_SCRIPT"])
        except Exception as e:
            print(f"[WARN] MusicGen failed: {e}. Creating silence fallback.")
            run_cmd(f"{CONFIG['FFMPEG']} -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t 8 \"{music_out}\"")

        # 4) Mix narration + music
        mixed_audio = os.path.join(scene_base, "mixed.mp3")
        try:
            mix_audio(wav_path, music_out, mixed_audio, music_vol=0.25)
        except Exception as e:
            print(f"[WARN] Audio mix failed: {e}. Copying narration to mixed.")
            shutil.copy(wav_path, mixed_audio)

        # 5) Make scene video
        scene_mp4 = os.path.join(scene_base, "scene.mp4")
        try:
            make_scene_video(img_out, mixed_audio, scene_mp4, vertical=vertical)
        except Exception as e:
            raise RuntimeError(f"Failed to create scene video: {e}")

        # 6) Generate subtitles and burn
        srt_out = os.path.join(scene_base, "subs.srt")
        try:
            generate_subtitles(mixed_audio, srt_out)
            burned = os.path.join(scene_base, "scene_sub.mp4")
            # burn subtitles
            run_cmd(f"{CONFIG['FFMPEG']} -y -i \"{scene_mp4}\" -vf \"subtitles='{srt_out}':force_style='FontName=Arial,FontSize=36'\" -c:a copy \"{burned}\"")
            scene_mp4 = burned
        except Exception as e:
            print(f"[WARN] Subtitle generation failed: {e}")

        scene_videos.append(scene_mp4)

    # Concat
    out_final = safe_path(out_video)
    concat_videos(scene_videos, out_final)
    print("[DONE] Final video:", out_final)
    return out_final

# -------------------------
#  CLI and Batch support
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Offline Script->Video pipeline")
    parser.add_argument("--prompt", type=str, help="Prompt/story text")
    parser.add_argument("--out", type=str, default="./outputs/final_output.mp4", help="Output MP4 path")
    parser.add_argument("--scenes", type=int, default=CONFIG["DEFAULT_SCENES"], help="Number of scenes")
    parser.add_argument("--vertical", action="store_true", help="Produce vertical video (TikTok)")
    parser.add_argument("--batch", type=str, help="CSV path with prompts (col: prompt,optional:lang,out)")
    parser.add_argument("--lang", type=str, default="sheng", help="Language for TTS")
    args = parser.parse_args()

    ensure_dir(CONFIG["WORK_BASE"])
    if args.batch:
        # simple CSV batch
        import csv
        with open(args.batch, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = row.get("prompt") or row.get("text") or ""
                out_path = row.get("out") or os.path.join(CONFIG["WORK_BASE"], f"{uuid.uuid4()}.mp4")
                print(f"[BATCH] Generating -> {out_path}")
                generate_video_from_prompt(p, out_path, scenes_n=args.scenes, vertical=args.vertical, lang=row.get("lang","sheng"))
        print("[BATCH DONE]")
    else:
        if not args.prompt:
            print("Please provide --prompt or --batch")
            sys.exit(1)
        generate_video_from_prompt(args.prompt, args.out, scenes_n=args.scenes, vertical=args.vertical, lang=args.lang)

if __name__ == "__main__":
    main()
