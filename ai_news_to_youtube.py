import os
import requests
import textwrap
import moviepy.editor as mp
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import InferenceClient
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google_auth_oauthlib.flow
import googleapiclient.errors

load_dotenv(find_dotenv())

HF_API_KEY = os.getenv("HF_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
VIDEO_OUTPUT_DIR = os.getenv("VIDEO_OUTPUT_DIR", "./output_videos")
os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

# 1️⃣ Get news headlines
def get_top_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['articles']

# 2️⃣ Summarize into a video script using a Hugging Face LLM
def summarize_with_llm(text_to_summarize):
    client = InferenceClient(token=HF_API_KEY)
    try:
        prompt = f"Summarize the following news article into a concise video script, suitable for a 30-second news segment:

{text_to_summarize}

Video Script:"
        response = client.text_generation(prompt, max_new_tokens=150, temperature=0.7)
        return response.strip()
    except Exception as e:
        print(f"Error summarizing with LLM: {e}")
        return None

# 3️⃣ Generate narration with TTS
def generate_narration(text_to_narrate):
    try:
        from gtts import gTTS
        tts = gTTS(text=text_to_narrate, lang='en')
        audio_filename = os.path.join(VIDEO_OUTPUT_DIR, f"narration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
        tts.save(audio_filename)
        print(f"Narration saved to {audio_filename}. (Using gTTS)")
        return audio_filename
    except ImportError:
        print("gTTS not installed. Please install it (`pip install gTTS`) or integrate another TTS solution.")
        # Create a silent audio file as a fallback
        audio_filename = os.path.join(VIDEO_OUTPUT_DIR, f"narration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
        # Estimate duration for silent audio
        dummy_duration = len(text_to_narrate) * 0.1
        mp.AudioFileClip(filename=None, duration=dummy_duration).write_audiofile(audio_filename)
        print(f"Silent dummy narration saved to {audio_filename}. (gTTS not found)")
        return audio_filename
    except Exception as e:
        print(f"Error generating narration: {e}")
        return None

# 4️⃣ Create simple video
def create_simple_video(video_script, audio_path):
    audio = mp.AudioFileClip(audio_path)
    video_width = 1280
    video_height = 720
    background_clip = mp.ColorClip(size=(video_width, video_height), color=(0,0,0)).set_duration(audio.duration)

    wrapped_text = textwrap.fill(video_script, width=80)
    txt_clip = mp.TextClip(wrapped_text, fontsize=40, color='white', bg_color='black',
                           size=(video_width * 0.9, None), method='caption')
    txt_clip = txt_clip.set_position(('center', 'center')).set_duration(audio.duration)

    final_video = mp.CompositeVideoClip([background_clip, txt_clip])
    final_video = final_video.set_audio(audio)

    filename = os.path.join(VIDEO_OUTPUT_DIR, f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
    final_video.write_videofile(filename, fps=24)
    return filename

# 5️⃣ Upload to YouTube
def upload_to_youtube(video_path, title, description="AI Generated News Update"):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        os.getenv("YOUTUBE_CLIENT_SECRET_FILE"), scopes)
    creds = flow.run_local_server(port=0)

    youtube = build("youtube", "v3", credentials=creds)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description, "tags": ["AI News", "Automation"]},
            "status": {"privacyStatus": "public"},
        },
        media_body=MediaFileUpload(video_path)
    )
    response = request.execute()
    print(f"Video uploaded: {response.get('id')}")
    return response.get('id')

# Main execution flow
def main():
    print("Fetching top news headlines...")
    articles = get_top_news()
    if not articles:
        print("No articles found. Exiting.")
        return

    # For simplicity, let's take the first article
    article_title = articles[0]['title']
    article_description = articles[0]['description'] or articles[0]['content'] or "No description available."

    print(f"Summarizing news: {article_title}")
    video_script = summarize_with_llm(article_description)
    if not video_script:
        print("Failed to generate video script. Exiting.")
        return

    print("Generating narration...")
    audio_path = generate_narration(video_script)
    if not audio_path:
        print("Failed to generate narration. Exiting.")
        return

    print("Creating video...")
    video_path = create_simple_video(video_script, audio_path)
    if not video_path:
        print("Failed to create video. Exiting.")
        return

    print(f"Uploading video to YouTube: {article_title}")
    youtube_video_id = upload_to_youtube(video_path, article_title)
    if youtube_video_id:
        print(f"Video successfully uploaded! YouTube ID: {youtube_video_id}")
    else:
        print("Video upload failed.")

if __name__ == "__main__":
    main()
