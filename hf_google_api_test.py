
Unified API Access Test
- Tests Hugging Face Inference API
- Tests Google/YouTube Data API
Works on: Kaggle, Colab, Local


import requests
import os
from dotenv import load_dotenv, find_dotenv
from googleapiclient.discovery import build

# ======== CONFIG ========
load_dotenv(find_dotenv())
HF_TOKEN = os.getenv("HF_API_KEY") or ""        # Hugging Face Access Token
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")  # Google API Key
YOUTUBE_TEST_USERNAME = "Google"
# ========================

def test_huggingface():
    print(" Testing Hugging Face API access...")
    if not HF_TOKEN:
        print("⚠ HF_API_KEY is missing. Set it in your .env at project root.")
        return
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    data = {"inputs": "Test access from environment"}
    try:
        r = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=data,
            timeout=15
        )
        if r.status_code == 200:
            print(f"✅ Hugging Face API access works for {HF_MODEL}")
        else:
            print(f"❌ Status {r.status_code}: {r.text}")
    except Exception as e:
        print(f"⚠ Error: {e}")

def test_youtube():
    print("\n Testing Google/YouTube Data API access...")
    if not YOUTUBE_API_KEY:
        print("⚠ YOUTUBE_API_KEY is missing. Set it in your .env at project root.")
        return
    try:
        # Build a YouTube service object for testing
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
        # Example: Search for a channel
        request = youtube.channels().list(
            part="snippet",
            forUsername=YOUTUBE_TEST_USERNAME
        )
        response = request.execute()
        
        if response and response.get("items"):
            print(f"✅ Google/YouTube Data API access works. Found channel for {YOUTUBE_TEST_USERNAME}.")
        else:
            print(f"❌ Google/YouTube Data API access failed or no channel found for {YOUTUBE_TEST_USERNAME}.")
            print(f"Response: {response}")
    except Exception as e:
        print(f"⚠ Error: {e}")

if __name__ == "__main__":
    test_huggingface()
    test_youtube()
