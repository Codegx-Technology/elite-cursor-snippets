import requests

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}
data = {"inputs": "Test access from Colab"}

try:
    r = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers=headers,
        json=data,
        timeout=15
    )
    if r.status_code == 200:
        print(f"✅ Colab → HF API access works for {MODEL}")
    else:
        print(f"❌ Status {r.status_code}: {r.text}")
except Exception as e:
    print(f"⚠ Error: {e}")
