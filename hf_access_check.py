import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
HF_TOKEN = (
    os.getenv("HF_API_KEY")
    or os.getenv("HUGGINGFACEHUB_API_TOKEN")
    or os.getenv("HF_TOKEN")
    or ""
)


MODELS = [
    "openai-community/gpt2",                 # public baseline (no gating)
    "meta-llama/Meta-Llama-3-8B-Instruct",  # LLaMA
    "mistralai/Mistral-7B-Instruct-v0.2",   # Mistral
    "tiiuae/falcon-7b-instruct",            # Falcon
    "bigscience/bloomz-7b1",                # BLOOMZ
    "google/flan-t5-large"                  # FLAN-T5
]

if not HF_TOKEN:
    print("⚠ Missing HF token. Set HF_API_KEY or HUGGINGFACEHUB_API_TOKEN (or HF_TOKEN) in your .env.")
    raise SystemExit(1)

headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
data = {"inputs": "Test access"}

print("Baseline: checking public model 'openai-community/gpt2' first to validate token & Inference API permission...")
for model in MODELS:
    print(f"\n🔍 Checking {model}...")
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers=headers,
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ Access granted for {model}")
        elif response.status_code == 403:
            body = response.text or ""
            if "Inference Providers" in body or "sufficient permissions" in body:
                print(
                    f"❌ Access denied for {model}: token lacks Inference API permission. "
                    f"Create a new token with Inference/Providers permission."
                )
            else:
                print(f"❌ Access denied for {model} (likely gated/private model or org access required)")
        elif response.status_code == 401:
            print(f"❌ Invalid/expired API token — check Hugging Face account")
            break
        else:
            if response.status_code == 404:
                print(
                    f"⚠ 404 Not Found for {model}. Ensure the repo ID is correct (e.g., 'openai-community/gpt2'). "
                    f"If it's a private/org model, verify access or use the full namespace."
                )
            else:
                print(f"⚠ Unexpected response {response.status_code}: {response.text}")
    except Exception as e:
        print(f"⚠ Error checking {model}: {e}")
