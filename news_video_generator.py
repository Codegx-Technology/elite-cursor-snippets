#!/usr/bin/env python3
"""
// [TASK]: Integrate Hugging Face Inference APIs for video generation
// [GOAL]: Use Bark, Whisper, and LLaMA 3 APIs for voice, captions, and scenes
// [SNIPPET]: thinkwithai + refactorclean + kenyafirst
"""

import argparse
import os
import random
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, TextClip
import moviepy.audio.fx.all as afx
from dotenv import load_dotenv
from gpu_fallback import get_device

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

def fetch_article(url):
    """
    // [TASK]: Fetch and parse the article from a URL
    // [GOAL]: Extract the main text content of the article
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        article = soup.find("article") or soup.find("main")
        if article:
            return article.get_text(separator="\n\n", strip=True)
        return soup.body.get_text(separator="\n\n", strip=True)
    except Exception as e:
        print(f"[ERROR] Failed to fetch article: {e}")
        return None

def read_script(file_path):
    """
    // [TASK]: Read a script from a text file
    // [GOAL]: Return the content of the file as a string
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"[ERROR] Failed to read script file: {e}")
        return None

def generate_scenes_from_text(text):
    """
    // [TASK]: Generate scenes from text using LLaMA 3 API
    // [GOAL]: Create a list of strings, where each string is a scene
    """
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    data = {"inputs": f"Split the following text into a list of short, descriptive scenes for a video. Each scene should be a single sentence. Text: {text}"}
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        scenes = response.json()[0]["generated_text"].split("\n")
        return [s.strip() for s in scenes if s.strip()]
    except Exception as e:
        print(f"[ERROR] Failed to generate scenes: {e}")
        return text.split(".") # Fallback to sentence splitting

def generate_image(scene_text, output_path):
    """
    // [TASK]: Generate an image for a scene
    // [GOAL]: Create a placeholder image with the scene text
    """
    try:
        width, height = 1280, 720
        img = Image.new("RGB", (width, height), color="#1a4d80")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        words = scene_text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) < 40:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        y_offset = (height - (len(lines) * 50)) // 2
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_offset), line, fill="white", font=font)
            y_offset += 50
        img.save(output_path)
        print(f"  Image generated: {output_path}")
        return output_path
    except Exception as e:
        print(f"[ERROR] Failed to generate image: {e}")
        return None

def generate_voiceover_from_text(text, output_file):
    """
    // [TASK]: Generate a voiceover from text using Bark API
    // [GOAL]: Create a WAV file with the voiceover
    """
    API_URL = "https://api-inference.huggingface.co/models/suno/bark"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    data = {"inputs": text}
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Voiceover generated: {output_file}")
        return output_file
    except Exception as e:
        print(f"[ERROR] Failed to generate voiceover: {e}")
        return None

def generate_captions_from_audio(audio_file):
    """
    // [TASK]: Generate captions from an audio file using Whisper API
    // [GOAL]: Return the captions as a string
    """
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    with open(audio_file, "rb") as f:
        audio_data = f.read()
    try:
        response = requests.post(API_URL, headers=headers, data=audio_data)
        response.raise_for_status()
        return response.json().get("text", "")
    except Exception as e:
        print(f"[ERROR] Failed to generate captions: {e}")
        return ""

def get_background_music(music_dir="music"):
    """
    // [TASK]: Get a random background music file
    // [GOAL]: Return the path to a random music file
    """
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
        return None
    music_files = [f for f in os.listdir(music_dir) if f.endswith((".mp3", ".wav"))]
    if not music_files:
        return None
    return os.path.join(music_dir, random.choice(music_files))

def compile_video(image_files, audio_file, music_file, captions, output_file):
    """
    // [TASK]: Compile the video from images, audio, music, and captions
    // [GOAL]: Create the final MP4 video file
    """
    try:
        clips = [ImageClip(img).set_duration(3) for img in image_files]
        video = concatenate_videoclips(clips, method="compose")
        audio = AudioFileClip(audio_file)
        video = video.set_audio(audio)
        if music_file:
            music = AudioFileClip(music_file).fx(afx.volumex, 0.1)
            final_audio = CompositeAudioClip([video.audio, music])
            video = video.set_audio(final_audio)
        if captions:
            caption_clip = TextClip(captions, fontsize=24, color='white', bg_color='black').set_pos(('center', 'bottom')).set_duration(video.duration)
            video = CompositeVideoClip([video, caption_clip])
        video.write_videofile(output_file, fps=24)
        print(f"Video compiled: {output_file}")
        return output_file
    except Exception as e:
        print(f"[ERROR] Failed to compile video: {e}")
        return None

def main():
    """
    // [TASK]: Main function to parse arguments and run the pipeline
    // [GOAL]: Orchestrate the video generation process
    """
    parser = argparse.ArgumentParser(description="News-to-Video Generator")
    parser.add_argument("--news", type=str, help="URL of the news article")
    parser.add_argument("--script", type=str, help="Path to the script file")
    args = parser.parse_args()

    if not HF_API_KEY:
        print("[ERROR] Hugging Face API key not found. Please set the HF_API_KEY environment variable.")
        return

    device = get_device()
    print(f"Running on device: {device}")

    text_content = None
    if args.news:
        text_content = fetch_article(args.news)
    elif args.script:
        text_content = read_script(args.script)
    else:
        print("Please provide either a news URL or a script file.")
        return

    if text_content:
        scenes = generate_scenes_from_text(text_content)
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        image_files = []
        for i, scene in enumerate(scenes):
            image_path = os.path.join(output_dir, f"image_{i+1}.png")
            generated_image = generate_image(scene, image_path)
            if generated_image:
                image_files.append(generated_image)
        
        voiceover_file = os.path.join(output_dir, "voice.wav")
        generate_voiceover_from_text(text_content, voiceover_file)

        captions = generate_captions_from_audio(voiceover_file)

        music_file = get_background_music()

        output_file = os.path.join(output_dir, "final_video.mp4")
        compile_video(image_files, voiceover_file, music_file, captions, output_file)

if __name__ == "__main__":
    main()
