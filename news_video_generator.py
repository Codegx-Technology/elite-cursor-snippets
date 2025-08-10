import argparse
import os
import random
# import requests # Removed direct requests import
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
# from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, TextClip
from moviepy.editor import *
import moviepy.audio.fx.all as afx
from dotenv import load_dotenv
import asyncio
import feedparser
import pickle
import sys

# For Hugging Face Login
from huggingface_hub import login as hf_login

# For YouTube Upload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Import the new GPU management classes
from gpu_fallback import ShujaaGPUIntegration, TaskProfile, ProcessingMode, HybridGPUManager
from ai_model_manager import generate_text, generate_image as ai_generate_image, text_to_speech, speech_to_text, init_hf_client
from logging_setup import get_logger; logger=get_logger(__name__)
from config_loader import get_config

config = get_config()

load_dotenv()
HF_API_KEY = config.api_keys.huggingface # Get HF API key from config_loader

# Initialize GPU integration manager
gpu_integration = ShujaaGPUIntegration()
gpu_manager = HybridGPUManager() # Initialize HybridGPUManager

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
        logger.error(f"Failed to fetch article: {e}")
        return None

def fetch_google_news(query="breaking news", num_results=1):
    """
    // [TASK]: Fetch breaking news from Google News
    // [GOAL]: Return the title and link of the top news article
    """
    try:
        # Google News RSS feed for a query
        rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-KE&gl=KE&ceid=KE:en"
        feed = feedparser.parse(rss_url)
        if feed.entries:
            entry = feed.entries[0]
            return {"title": entry.title, "link": entry.link}
        return None
    except Exception as e:
        logger.error(f"Failed to fetch Google News: {e}")
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
        logger.error(f"Failed to read script file: {e}")
        return None

async def generate_scenes_from_text(text):
    """
    // [TASK]: Generate scenes from text using LLaMA 3 API via HybridGPUManager
    // [GOAL]: Create a list of strings, where each string is a scene
    """
    # API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2" # Moved to config
    # headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    # data = {"inputs": f"Split the following text into a list of short, descriptive scenes for a video. Each scene should be a single sentence. Text: {text}"}

    task_profile = TaskProfile(
        task_type="text_generation",
        estimated_memory=8.0, # LLaMA 3 is large
        estimated_time=60, # Can take time
        priority=10, # High priority for core task
        can_use_cpu=False, # LLaMA 3 is too heavy for CPU fallback
        preferred_gpu_memory=16.0
    )

    async def _llm_api_call(input_data, device="cpu"):
        # This function will be executed by the HybridGPUManager
        # We only use HF API for now, so device argument is not directly used here
        try:
            # Use ai_model_manager.generate_text
            generated_text = await generate_text(input_data["inputs"], model_id=config.models.text_generation.hf_api_id)
            scenes = generated_text.split("\n")
            return [s.strip() for s in scenes if s.strip()]
        except Exception as e:
            logger.error(f"LLaMA 3 API call failed: {e}")
            raise # Re-raise to trigger fallback if any

    try:
        # Use HybridGPUManager to process the task
        scenes = await gpu_manager.process_task(task_profile, _llm_api_call, {"inputs": f"Split the following text into a list of short, descriptive scenes for a video. Each scene should be a single sentence. Text: {text}"})
        return scenes
    except Exception as e:
        logger.warning(f"Falling back to local sentence splitting for scenes: {e}")
        # Fallback to simple sentence splitting if LLaMA 3 fails
        sentences = text.split(".")
        return [s.strip() for s in sentences if s.strip()]

async def generate_image(scene_text, output_path):
    """
    // [TASK]: Generate an image for a scene using GPU integration
    // [GOAL]: Create an image file for the scene
    """
    try:
        # Use ai_model_manager.generate_image
        image_bytes = await ai_generate_image(scene_text, model_id=config.models.image_generation.hf_api_id)
        if image_bytes:
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            logger.info(f"  Image generated: {output_path}")
            return output_path
        else:
            # Fallback to simple placeholder if accelerated generation fails
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
            logger.info(f"  Placeholder image generated: {output_path}")
            return output_path
    except Exception as e:
        logger.error(f"Failed to generate image: {e}")
        return None

async def generate_voiceover_from_text(text, output_file):
    """
    // [TASK]: Generate a voiceover from text using Bark API via HybridGPUManager
    // [GOAL]: Create a WAV file with the voiceover
    """
    # API_URL = "https://api-inference.huggingface.co/models/suno/bark" # Moved to config
    # headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    # data = {"inputs": text}

    task_profile = TaskProfile(
        task_type="voice_synthesis",
        estimated_memory=1.0, # Bark is relatively small
        estimated_time=10, # Can be fast
        priority=9, # High priority
        can_use_cpu=True, # Can fallback to gTTS if needed
        preferred_gpu_memory=2.0
    )

    async def _bark_api_call(input_data, device="cpu"):
        try:
            # Use ai_model_manager.text_to_speech
            audio_bytes = await text_to_speech(input_data["inputs"], model_id=config.models.voice_synthesis.hf_api_id)
            with open(output_file, "wb") as f:
                f.write(audio_bytes)
            return output_file
        except Exception as e:
            logger.error(f"Bark API call failed: {e}")
            raise # Re-raise to trigger fallback if any

    try:
        # Use HybridGPUManager to process the task
        voiceover_path = await gpu_manager.process_task(task_profile, _bark_api_call, {"inputs": text})
        logger.info(f"Voiceover generated: {voiceover_path}")
        return voiceover_path
    except Exception as e:
        logger.warning(f"Falling back to gTTS for voiceover: {e}")
        # Fallback to gTTS if Bark fails
        from gtts import gTTS
        try:
            tts = gTTS(text)
            tts.save(output_file)
            logger.info(f"Voiceover generated (gTTS fallback): {output_file}")
            return output_file
        except Exception as gtts_e:
            logger.error(f"gTTS fallback failed: {gtts_e}")
            return None

async def generate_captions_from_audio(audio_file):
    """
    // [TASK]: Generate captions from an audio file using Whisper API via HybridGPUManager
    // [GOAL]: Return the captions as a string
    """
    # API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2" # Moved to config
    # headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    task_profile = TaskProfile(
        task_type="speech_to_text",
        estimated_memory=4.0, # Whisper large is memory intensive
        estimated_time=30, # Can take time for long audio
        priority=8, # High priority
        can_use_cpu=True, # Can fallback to a simpler STT if needed
        preferred_gpu_memory=8.0
    )

    async def _whisper_api_call(audio_data, device="cpu"):
        try:
            # Use ai_model_manager.speech_to_text
            captions = await speech_to_text(audio_data, model_id=config.models.speech_to_text.hf_api_id)
            return captions
        except Exception as e:
            logger.error(f"Whisper API call failed: {e}")
            raise # Re-raise to trigger fallback if any

    try:
        with open(audio_file, "rb") as f:
            audio_data = f.read()
        # Use HybridGPUManager to process the task
        captions = await gpu_manager.process_task(task_profile, _whisper_api_call, audio_data)
        return captions
    except Exception as e:
        logger.warning(f"Falling back to empty captions: {e}")
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

async def compile_video(image_files, audio_file, music_file, captions, output_file):
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
        logger.info(f"Video compiled: {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Failed to compile video: {e}")
        return None

# YouTube Upload Automation
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

async def youtube_upload(video_file, title, description, tags):
    """
    // [TASK]: Upload video to YouTube
    // [GOAL]: Automate YouTube video publishing
    """
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'): # Changed from token.json to token.pickle
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    youtube = build('youtube', 'v3', credentials=credentials)

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media_file = MediaFileUpload(video_file)

    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media_file
    )

    logger.info("Uploading video to YouTube...")
    response = request.execute()
    logger.info(f"✅ Uploaded to YouTube: https://youtu.be/{response['id']}")
    return response['id']

async def main():
    """
    // [TASK]: Main function to parse arguments and run the pipeline
    // [GOAL]: Orchestrate the video generation process
    """
    parser = argparse.ArgumentParser(description="News-to-Video Generator")
    parser.add_argument("--news", type=str, help="URL of the news article")
    parser.add_argument("--script", type=str, help="Path to the script file")
    parser.add_argument("--upload-youtube", action="store_true", help="Upload the generated video to YouTube")
    args = parser.parse_args()

    # Initialize HF client (will log in if HF_API_KEY is set)
    init_hf_client()

    # Runtime Detection
    runtime = "Local"
    if "google.colab" in sys.modules:
        runtime = "Colab"
    elif "kaggle" in sys.modules:
        runtime = "Kaggle"
    elif "spaces" in os.getcwd():
        runtime = "HuggingFace Space"
    logger.info(f" Running on: {runtime}")

    # The device is now managed by ShujaaGPUIntegration
    logger.info(f"GPU Integration Status: {gpu_integration.get_integration_status()}")

    text_content = None
    if args.news:
        logger.info(f"Fetching news for query: {args.news}")
        news_item = fetch_google_news(args.news) # Use fetch_google_news for news mode
        if news_item:
            logger.info(f"News found: {news_item["title"]}")
            text_content = fetch_article(news_item["link"]) # Fetch full article content
        else:
            logger.error("No news found for the given query.")
            return
    elif args.script:
        logger.info(f"Reading script from: {args.script}")
        text_content = read_script(args.script)
    else:
        logger.error("Please provide either a news URL or a script file.")
        return

    if text_content:
        logger.info("Content processed successfully. Generating video...")
        scenes = await generate_scenes_from_text(text_content)
        output_dir = config.video.output_dir # Get from config
        os.makedirs(output_dir, exist_ok=True)

        image_files = []
        for i, scene in enumerate(scenes):
            image_path = os.path.join(output_dir, f"image_{i+1}.png")
            generated_image = await generate_image(scene, image_path)
            if generated_image:
                image_files.append(generated_image)
        
        voiceover_file = os.path.join(output_dir, "voice.wav")
        await generate_voiceover_from_text(text_content, voiceover_file)

        captions = await generate_captions_from_audio(voiceover_file)

        music_file = get_background_music(config.video.music_dir) # Get from config

        output_file = os.path.join(output_dir, "final_video.mp4")
        await compile_video(image_files, voiceover_file, music_file, captions, output_file)

        logger.info(f"🎉 Video generation complete! Output: {output_file}")

        if args.upload_youtube:
            logger.info("Attempting to upload to YouTube...")
            # For demonstration, using placeholder title, description, tags
            video_title = news_item["title"] if args.news and news_item else "AI Generated News Video"
            video_description = f"AI-generated news report based on: {text_content[:200]}..."
            video_tags = ["AI News", "Shujaa Studio", "Automated Video"]
            await youtube_upload(output_file, video_title, video_description, video_tags)

if __name__ == "__main__":
    asyncio.run(main())