
Unified API Access Test
- Tests Hugging Face Inference API
- Tests Google/YouTube Data API
Works on: Kaggle, Colab, Local


import requests
from googleapiclient.discovery import build

# ======== CONFIG ========
HF_TOKEN = "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"        # Hugging Face Access Token
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

YOUTUBE_API_KEY = "your_youtube_api_key_here"  # Google API Key
YOUTUBE_TEST_USERNAME = "Google"
# ========================

def test_huggingface():
    print(" Testing Hugging Face API access...")
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
