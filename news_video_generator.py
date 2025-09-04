import argparse
import os
import random
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
try:
    from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, TextClip
    import moviepy.audio.fx.all as afx
    MOVIEPY_AVAILABLE = True
except Exception as _moviepy_err:
    MOVIEPY_AVAILABLE = False
    MOVIEPY_IMPORT_ERROR = _moviepy_err
from dotenv import load_dotenv
import asyncio
import feedparser
import pickle
import sys
import logging
from typing import Optional, Any, Dict

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from gpu_fallback import ShujaaGPUIntegration, TaskProfile, HybridGPUManager
from config_loader import get_config
from utils.parallel_processing import ParallelProcessor # Import ParallelProcessor
from error_utils import log_and_raise, retry_on_exception
from enhanced_model_router import EnhancedModelRouter, GenerationRequest
from logging_setup import get_logger, setup_logging

from dotenv import load_dotenv

# Centralized logging (explicit init)
setup_logging()
logger = get_logger(__name__)

load_dotenv()

config = get_config()
HF_TOKEN = config.api_keys.huggingface

gpu_integration = ShujaaGPUIntegration()
gpu_manager = HybridGPUManager()

@retry_on_exception()
def fetch_article(url):
    import requests
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        article = soup.find("article") or soup.find("main")
        if article:
            return article.get_text(separator="\n\n", strip=True)
        return soup.body.get_text(separator="\n\n", strip=True)
    except Exception as e:
        log_and_raise(e, f"Failed to fetch article from {url}")

@retry_on_exception()
def fetch_google_news(query="breaking news", num_results=1):
    try:
        rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-KE&gl=KE&ceid=KE:en"
        feed = feedparser.parse(rss_url)
        if feed.entries:
            entry = feed.entries[0]
            return {"title": entry.title, "link": entry.link}
        return None
    except Exception as e:
        log_and_raise(e, f"Failed to fetch Google News for query {query}")

@retry_on_exception()
def read_script(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        log_and_raise(e, f"Failed to read script file {file_path}")

async def generate_scenes_from_text(text, enhanced_router: Any, dialect: Optional[str] = None):
    prompt_for_llm = f"Split the following text into a list of short, descriptive scenes for a video. Each scene should be a single sentence. Text: {text}"
    
    request = GenerationRequest(
        prompt=prompt_for_llm,
        type="text",
        dialect=dialect
    )
    
    result = await enhanced_router.route_generation(request)
    
    if result.success and result.metadata and "generated_text" in result.metadata:
        generated_text = result.metadata["generated_text"]
        scenes = generated_text.split("\n")
        return [s.strip() for s in scenes if s.strip()]
    else:
        logger.warning(f"Enhanced router failed for scene generation, falling back to local sentence splitting: {result.error_message}")
        sentences = text.split(".")
        return [s.strip() for s in sentences if s.strip()]


async def generate_image(scene_text, output_path, enhanced_router: Any, dialect: Optional[str] = None):
    # Fast path: if model loading is disabled, generate a placeholder immediately.
    if getattr(config.models, 'disable_model_loading', False):
        width, height = 1280, 720
        img = Image.new("RGB", (width, height), color="#1a4d80")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
        words = scene_text.split()
        lines = [" ".join(words[i:i+6]) for i in range(0, len(words), 6)]
        y_offset = (height - (len(lines) * 50)) // 2
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_offset), line, fill="white", font=font)
            y_offset += 50
        img.save(output_path)
        logger.info(f"  Placeholder image generated (models disabled): {output_path}")
        return output_path

    request = GenerationRequest(
        prompt=scene_text,
        type="image",
        dialect=dialect
    )
    
    result = await enhanced_router.route_generation(request)
    
    if result.success and result.content_url:
        # Assuming content_url is a direct path or a data URL that can be saved
        # If it's a data URL, you'd need to decode it. For simplicity, assuming it's a path or bytes.
        # For now, let's simulate saving the image if the router returns a content_url
        # In a real scenario, the router might return image_bytes directly.
        if result.content_url.startswith("data:image"):
            import base64
            header, encoded = result.content_url.split(",", 1)
            image_bytes = base64.b64decode(encoded)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            logger.info(f"  Image generated via router: {output_path}")
            return output_path
        elif os.path.exists(result.content_url): # If router returns a path to a temp file
            import shutil
            shutil.copy(result.content_url, output_path)
            logger.info(f"  Image copied from router temp path: {output_path}")
            return output_path
        else: # Fallback to placeholder if router returns a URL that needs fetching or other format
            logger.warning(f"Router returned content_url but not in expected format for direct save: {result.content_url}. Generating placeholder.")
            width, height = 1280, 720
            img = Image.new("RGB", (width, height), color="#1a4d80")
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except IOError:
                font = ImageFont.load_default()
            words = scene_text.split()
            lines = [" ".join(words[i:i+6]) for i in range(0, len(words), 6)]
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
    else:
        logger.warning(f"Enhanced router failed for image generation: {result.error_message}. Generating placeholder.")
        width, height = 1280, 720
        img = Image.new("RGB", (width, height), color="#1a4d80")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
        words = scene_text.split()
        lines = [" ".join(words[i:i+6]) for i in range(0, len(words), 6)]
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

async def generate_voiceover_from_text(text, output_file, enhanced_router: Any, dialect: Optional[str] = None):
    # Fast path: if model loading is disabled, use gTTS or silence immediately.
    if getattr(config.models, 'disable_model_loading', False):
        from gtts import gTTS
        try:
            tts = gTTS(text)
            tts.save(output_file)
            logger.info(f"Voiceover generated (gTTS fast path, models disabled): {output_file}")
            return output_file
        except Exception as gtts_e:
            logger.error(f"gTTS fast path failed: {gtts_e}")
            # Create 2s silence WAV
            try:
                import io as _io
                import wave as _wave
                import struct as _struct
                sample_rate = 22050
                duration_sec = 2
                num_channels = 1
                sampwidth = 2
                num_frames = sample_rate * duration_sec
                buf = _io.BytesIO()
                with _wave.open(buf, 'wb') as wf:
                    wf.setnchannels(num_channels)
                    wf.setsampwidth(sampwidth)
                    wf.setframerate(sample_rate)
                    silence_frame = _struct.pack('<h', 0)
                    wf.writeframes(silence_frame * num_frames)
                with open(output_file, 'wb') as f:
                    f.write(buf.getvalue())
                logger.warning(f"Created placeholder silence audio (models disabled): {output_file}")
                return output_file
            except Exception as silent_e:
                logger.exception(f"Failed to create silence fallback: {silent_e}")
                return None

    request = GenerationRequest(
        prompt=text,
        type="audio",
        dialect=dialect
    )
    
    result = await enhanced_router.route_generation(request)
    
    if result.success and result.content_url:
        # Assuming content_url is a direct path or a data URL that can be saved
        if result.content_url.startswith("data:audio"):
            import base64
            header, encoded = result.content_url.split(",", 1)
            audio_bytes = base64.b64decode(encoded)
            with open(output_file, "wb") as f:
                f.write(audio_bytes)
            logger.info(f"Voiceover generated via router: {output_file}")
            return output_file
        elif os.path.exists(result.content_url): # If router returns a path to a temp file
            import shutil
            shutil.copy(result.content_url, output_file)
            logger.info(f"Voiceover copied from router temp path: {output_file}")
            return output_file
        else: # Fallback to gTTS if router returns a URL that needs fetching or other format
            logger.warning(f"Router returned content_url but not in expected format for direct save: {result.content_url}. Falling back to gTTS.")
            from gtts import gTTS
            try:
                tts = gTTS(text)
                tts.save(output_file)
                logger.info(f"Voiceover generated (gTTS fallback): {output_file}")
                return output_file
            except Exception as gtts_e:
                logger.error(f"gTTS fallback failed: {gtts_e}")
                # Final fallback: write 2s silence WAV so pipeline can proceed
                try:
                    import io as _io
                    import wave as _wave
                    import struct as _struct
                    sample_rate = 22050
                    duration_sec = 2
                    num_channels = 1
                    sampwidth = 2
                    num_frames = sample_rate * duration_sec
                    buf = _io.BytesIO()
                    with _wave.open(buf, 'wb') as wf:
                        wf.setnchannels(num_channels)
                        wf.setsampwidth(sampwidth)
                        wf.setframerate(sample_rate)
                        silence_frame = _struct.pack('<h', 0)
                        wf.writeframes(silence_frame * num_frames)
                    with open(output_file, 'wb') as f:
                        f.write(buf.getvalue())
                    logger.warning(f"Created placeholder silence audio: {output_file}")
                    return output_file
                except Exception as silent_e:
                    logger.exception(f"Failed to create silence fallback: {silent_e}")
                    return None
    else:
        logger.warning(f"Enhanced router failed for voiceover generation: {result.error_message}. Falling back to gTTS.")
        from gtts import gTTS
        try:
            tts = gTTS(text)
            tts.save(output_file)
            logger.info(f"Voiceover generated (gTTS fallback): {output_file}")
            return output_file
        except Exception as gtts_e:
            logger.error(f"gTTS fallback failed: {gtts_e}")
            # Final fallback: write 2s silence WAV so pipeline can proceed
            try:
                import io as _io
                import wave as _wave
                import struct as _struct
                sample_rate = 22050
                duration_sec = 2
                num_channels = 1
                sampwidth = 2
                num_frames = sample_rate * duration_sec
                buf = _io.BytesIO()
                with _wave.open(buf, 'wb') as wf:
                    wf.setnchannels(num_channels)
                    wf.setsampwidth(sampwidth)
                    wf.setframerate(sample_rate)
                    silence_frame = _struct.pack('<h', 0)
                    wf.writeframes(silence_frame * num_frames)
                with open(output_file, 'wb') as f:
                    f.write(buf.getvalue())
                logger.warning(f"Created placeholder silence audio: {output_file}")
                return output_file
            except Exception as silent_e:
                logger.exception(f"Failed to create silence fallback: {silent_e}")
                return None

async def generate_captions_from_audio(audio_file, enhanced_router: Any, dialect: Optional[str] = None):
    # For speech-to-text, the prompt would be the audio content itself, or a description.
    # Since enhanced_router.route_generation expects a text prompt, we'll use a generic one.
    # In a real scenario, the router would need to handle audio input for STT.
    request = GenerationRequest(
        prompt=f"Transcribe audio from file: {audio_file}", # Generic prompt
        type="text", # STT typically returns text
        dialect=dialect # Pass dialect
    )
    
    result = await enhanced_router.route_generation(request)
    
    if result.success and result.metadata and "generated_text" in result.metadata:
        captions = result.metadata["generated_text"]
        logger.info(f"Captions generated via router: {captions}")
        return captions
    else:
        logger.warning(f"Enhanced router failed for caption generation: {result.error_message}. Falling back to empty captions.")
        return ""

def get_background_music(music_dir="music"):
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
        return None
    music_files = [f for f in os.listdir(music_dir) if f.endswith((".mp3", ".wav"))]
    if not music_files:
        return None
    return os.path.join(music_dir, random.choice(music_files))

async def compile_video(image_files, audio_file, music_file, captions, output_file):
    if not MOVIEPY_AVAILABLE:
        logger.warning(f"MoviePy not available ({MOVIEPY_IMPORT_ERROR}). Skipping video compilation and returning None.")
        return None
    try:
        if not image_files:
            logger.error("Cannot compile video, no image files.")
            return None
        # Ensure we have an audio file; if missing, create a short silence WAV
        if not audio_file or not os.path.exists(audio_file):
            try:
                out_dir = os.path.dirname(output_file) or "."
                os.makedirs(out_dir, exist_ok=True)
                audio_file = os.path.join(out_dir, "voice.wav")
                import wave as _wave, struct as _struct
                sample_rate = 22050
                duration_sec = 2
                num_channels = 1
                sampwidth = 2
                num_frames = sample_rate * duration_sec
                with _wave.open(audio_file, 'wb') as wf:
                    wf.setnchannels(num_channels)
                    wf.setsampwidth(sampwidth)
                    wf.setframerate(sample_rate)
                    silence_frame = _struct.pack('<h', 0)
                    wf.writeframes(silence_frame * num_frames)
                logger.warning(f"Main audio missing. Created placeholder silence: {audio_file}")
            except Exception as gen_silent_e:
                logger.exception(f"Failed to create placeholder silence audio: {gen_silent_e}")
                return None
        clips = [ImageClip(img).set_duration(3) for img in image_files]
        video = concatenate_videoclips(clips, method="compose")
        audio = AudioFileClip(audio_file)
        video = video.set_audio(audio)
        if music_file and os.path.exists(music_file):
            music = AudioFileClip(music_file).fx(afx.volumex, 0.1)
            final_audio = CompositeAudioClip([video.audio, music])
            video = video.set_audio(final_audio)
        if captions:
            caption_clip = TextClip(captions, fontsize=24, color='white', bg_color='black', size=video.size).set_pos(('center', 'bottom')).set_duration(video.duration)
            video = CompositeVideoClip([video, caption_clip])
        video.write_videofile(output_file, fps=24, codec='libx264')
        logger.info(f"Video compiled: {output_file}")
        return output_file
    except Exception as e:
        log_and_raise(e, f"Failed to compile video: {output_file}")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

@retry_on_exception()
async def youtube_upload(video_file, title, description, tags):
    try:
        credentials = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                credentials = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)
        youtube = build('youtube', 'v3', credentials=credentials)
        body = {
            'snippet': {'title': title, 'description': description, 'tags': tags},
            'status': {'privacyStatus': 'public'}
        }
        media_file = MediaFileUpload(video_file)
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media_file)
        logger.info("Uploading video to YouTube...")
        response = request.execute()
        logger.info(f"✅ Uploaded to YouTube: https://youtu.be/{response['id']}")
        return response['id']
    except Exception as e:
        log_and_raise(e, f"Failed to upload video to YouTube: {video_file}")

async def main(news: str = None, script_file: str = None, prompt: str = None, upload_youtube: bool = False, user_preferences: Dict = None, enhanced_router: Any = None, parallel_processor: Any = None, scene_processor: Any = None):
    # Initialize HF client only if model loading is enabled (avoid heavy imports otherwise)
    if not getattr(config.models, 'disable_model_loading', False):
        try:
            from ai_model_manager import init_hf_client
            init_hf_client()
        except Exception as e:
            logger.warning(f"Skipping HF client init due to error: {e}")
    logger.info(f"GPU Integration Status: {gpu_integration.get_integration_status()}")

    text_content = None
    video_title = "AI Generated Video"
    
    # Extract dialect from user_preferences
    dialect = user_preferences.get("dialect") if user_preferences else None
    # Initialize enhanced router if not provided
    if enhanced_router is None:
        enhanced_router = EnhancedModelRouter()
    if news:
        logger.info(f"Fetching news for query: {news}")
        try:
            news_item = fetch_google_news(news)
            if news_item:
                logger.info(f"News found: {news_item['title']}")
                video_title = news_item['title']
                text_content = fetch_article(news_item["link"])
            else:
                log_and_raise(ValueError("No news found for the given query."), "News fetch failed")
        except Exception as e:
            log_and_raise(e, "Error fetching news")
    elif script_file:
        logger.info(f"Reading script from: {script_file}")
        try:
            video_title = os.path.splitext(os.path.basename(script_file))[0]
            text_content = read_script(script_file)
        except Exception as e:
            log_and_raise(e, "Error reading script file")
    elif prompt:
        logger.info(f"Using prompt: {prompt}")
        video_title = prompt[:50]
        text_content = prompt
    else:
        log_and_raise(ValueError("Please provide either a news URL, a script file, or a prompt."), "Missing input")

    if text_content:
        logger.info("Content processed successfully. Generating video...")
        try:
            scenes = await generate_scenes_from_text(text_content, enhanced_router, dialect)
            if not scenes:
                log_and_raise(ValueError("Could not generate scenes from text."), "Scene generation failed")
        except Exception as e:
            log_and_raise(e, "Error generating scenes")
            
        output_dir = config.video.output_dir
        os.makedirs(output_dir, exist_ok=True)

        logger.info(f"Generating {len(scenes)} scene images in parallel...")
        
        async def image_worker(scene_data):
            index = scene_data['index']
            scene_text = scene_data['text']
            image_path = os.path.join(output_dir, f"image_{index+1}.png")
            try:
                generated_path = await generate_image(scene_text, image_path, enhanced_router, dialect)
                return {"status": "success" if generated_path else "failed", "path": generated_path}
            except Exception as e:
                log_and_raise(e, f"Error generating image for scene {index}")

        scene_items = [{"index": i, "text": scene} for i, scene in enumerate(scenes)]
        _parallel_processor = parallel_processor or ParallelProcessor()
        image_results = await _parallel_processor.run_parallel(scene_items, image_worker)
        image_files = [res["path"] for res in image_results if res and res["status"] == "success"]
        
        if not image_files:
            log_and_raise(ValueError("All image generation failed."), "Image generation failed")

        voiceover_file = os.path.join(output_dir, "voice.wav")
        try:
            await generate_voiceover_from_text(text_content, voiceover_file, enhanced_router, dialect)
        except Exception as e:
            log_and_raise(e, "Error generating voiceover")

        captions = None
        if os.environ.get('SHUJAA_DISABLE_STT', '1') == '1':
            captions = ""
            logger.info("STT disabled via SHUJAA_DISABLE_STT. Skipping captions generation.")
        else:
            try:
                captions = await generate_captions_from_audio(voiceover_file, enhanced_router, dialect)
            except Exception as e:
                log_and_raise(e, "Error generating captions")

        music_file = get_background_music(config.video.music_dir)
        output_file = os.path.join(output_dir, "final_video.mp4")
        try:
            await compile_video(image_files, voiceover_file, music_file, captions, output_file)
        except Exception as e:
            log_and_raise(e, "Error compiling video")

        logger.info(f"🎉 Video generation complete! Output: {output_file}")

        if upload_youtube:
            logger.info("Attempting to upload to YouTube...")
            video_description = f"AI-generated video based on: {text_content[:200]}..."
            video_tags = ["AI News", "Shujaa Studio", "Automated Video"]
            try:
                await youtube_upload(output_file, video_title, video_description, video_tags)
            except Exception as e:
                log_and_raise(e, "Error uploading to YouTube")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="News-to-Video Generator")
    parser.add_argument("--news", type=str, help="URL of the news article or search query")
    parser.add_argument("--script", type=str, help="Path to the script file")
    parser.add_argument("--prompt", type=str, help="A text prompt to generate video from")
    parser.add_argument("--upload-youtube", action="store_true", help="Upload the generated video to YouTube")
    args = parser.parse_args()
    
    try:
        print("ENTRY: Starting news_video_generator main run...")
        logger.info("Starting news_video_generator main run...")
        asyncio.run(main(news=args.news, script_file=args.script, prompt=args.prompt, upload_youtube=args.upload_youtube))
    except Exception as e:
        logger.exception(f"Fatal error in main: {e}")
        sys.exit(1)
