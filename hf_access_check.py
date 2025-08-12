import requests
import os

HF_API_KEY = os.environ.get("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")


MODELS = [
    "meta-llama/Meta-Llama-3-8B-Instruct",  # LLaMA
    "mistralai/Mistral-7B-Instruct-v0.2",   # Mistral
    "tiiuae/falcon-7b-instruct",            # Falcon
    "bigscience/bloomz-7b1",                # BLOOMZ
    "google/flan-t5-large"                  # FLAN-T5
]

headers = {"Authorization": f"Bearer {HF_TOKEN}"}
data = {"inputs": "Test access"}

for model in MODELS:
    print(f"\nChecking {model}...")
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers=headers,
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            print(f"Access granted for {model}")
        elif response.status_code == 403:
            print(f"Access denied for {model} (not approved yet)")
        elif response.status_code == 401:
            print(f"Invalid/expired API token -- check Hugging Face account")
            break
        else:
            print(f"Unexpected response {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error checking {model}: {e}")