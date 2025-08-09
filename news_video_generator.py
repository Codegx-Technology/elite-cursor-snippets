#!/usr/bin/env python3
"""
// [TASK]: Create a news-to-video generator with GPU support
// [GOAL]: Generate a video from a news URL or a script file
// [SNIPPET]: thinkwithai + refactorclean + kenyafirst
"""

import argparse
import os
import random
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
import moviepy.audio.fx.all as afx
from gpu_fallback import get_device

def fetch_article(url):
    """
    // [TASK]: Fetch and parse the article from a URL
    // [GOAL]: Extract the main text content of the article
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the main article content
        article = soup.find("article")
        if not article:
            article = soup.find("main")

        if article:
            # Get all the text from the article
            text = article.get_text(separator="\n\n", strip=True)
        else:
            # Fallback to getting all the text from the body
            text = soup.body.get_text(separator="\n\n", strip=True)

        return text
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

def split_into_scenes(text):
    """
    // [TASK]: Split the text into scenes
    // [GOAL]: Create a list of strings, where each string is a scene
    // [NOTE]: This is a placeholder for a real GPT API call
    """
    # Split the text into sentences
    sentences = text.split(".")
    
    # Filter out empty sentences
    scenes = [s.strip() for s in sentences if s.strip()]
    
    return scenes

def generate_image(scene_text, output_path):
    """
    // [TASK]: Generate an image for a scene
    // [GOAL]: Create a placeholder image with the scene text
    // [NOTE]: This is a placeholder for a real image generation model
    """
    try:
        # Create a blank image
        width, height = 1280, 720
        img = Image.new("RGB", (width, height), color="#1a4d80")
        draw = ImageDraw.Draw(img)

        # Add text to the image
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Split text into lines
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
        
        # Draw text
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

def generate_voiceover(text, output_file):
    """
    // [TASK]: Generate a voiceover from text
    // [GOAL]: Create an MP3 file with the voiceover
    """
    try:
        tts = gTTS(text)
        tts.save(output_file)
        print(f"Voiceover generated: {output_file}")
        return output_file
    except Exception as e:
        print(f"[ERROR] Failed to generate voiceover: {e}")
        return None

def get_background_music(music_dir="music"):
    """
    // [TASK]: Get a random background music file
    // [GOAL]: Return the path to a random music file
    """
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
        print(f"[INFO] Created music directory: {music_dir}")
        return None

    music_files = [f for f in os.listdir(music_dir) if f.endswith((".mp3", ".wav"))]
    if not music_files:
        print(f"[WARNING] No music files found in: {music_dir}")
        return None

    return os.path.join(music_dir, random.choice(music_files))

def compile_video(image_files, audio_file, music_file, output_file):
    """
    // [TASK]: Compile the video from images, audio, and music
    // [GOAL]: Create the final MP4 video file
    """
    try:
        # Create video clips from images
        clips = [ImageClip(img).set_duration(3) for img in image_files]
        video = concatenate_videoclips(clips, method="compose")

        # Add voiceover
        audio = AudioFileClip(audio_file)
        video = video.set_audio(audio)

        # Add background music
        if music_file:
            music = AudioFileClip(music_file).fx(afx.volumex, 0.1) # Lower the volume of the music
            final_audio = CompositeAudioClip([video.audio, music])
            video = video.set_audio(final_audio)

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

    device = get_device()
    print(f"Running on device: {device}")

    text_content = None
    if args.news:
        print(f"News mode: {args.news}")
        text_content = fetch_article(args.news)
    elif args.script:
        print(f"Script mode: {args.script}")
        text_content = read_script(args.script)
    else:
        print("Please provide either a news URL or a script file.")
        return

    if text_content:
        print("Content processed successfully.")
        scenes = split_into_scenes(text_content)
        print(f"{len(scenes)} scenes created.")

        # Create output directory
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        # Generate images for each scene
        image_files = []
        for i, scene in enumerate(scenes):
            print(f"Scene {i+1}: {scene}")
            image_path = os.path.join(output_dir, f"image_{i+1}.png")
            generated_image = generate_image(scene, image_path)
            if generated_image:
                image_files.append(generated_image)
        
        # Generate voiceover
        voiceover_file = os.path.join(output_dir, "voice.mp3")
        generate_voiceover(text_content, voiceover_file)

        # Get background music
        music_file = get_background_music()

        # Compile video
        output_file = os.path.join(output_dir, "final_video.mp4")
        compile_video(image_files, voiceover_file, music_file, output_file)

if __name__ == "__main__":
    main()