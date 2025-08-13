import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("HF_API_KEY") or os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN") or ""
assert TOKEN, "Missing HF_API_KEY / HUGGINGFACEHUB_API_TOKEN / HF_TOKEN in environment/.env"

MODEL = "gpt2"
URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
DATA = {"inputs": "Hello from our Shujaa check"}

print(f"Checking model: {MODEL}")
try:
    r = requests.post(URL, headers=HEADERS, json=DATA, timeout=20)
    print("Status:", r.status_code)
    if r.status_code == 200:
        print("OK -> First 200 chars:\n", (r.text or "")[:200])
    else:
        print("Body:\n", r.text)
except Exception as e:
    print("Error:", e)
