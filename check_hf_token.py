"""This script verifies that your Hugging Face API token is valid and retrieves account info."""

import os
import sys
import requests
from dotenv import load_dotenv

def check_hf_token():
    """
    Verifies the Hugging Face API token and retrieves account info.
    """
    load_dotenv()
    token = os.getenv("HF_TOKEN")

    if not token:
        print("❌ HF_TOKEN not found in .env file.")
        sys.exit(1)

    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get("https://huggingface.co/api/whoami-v2", headers=headers)

        if response.status_code == 200:
            user_info = response.json()
            print("✅ Hugging Face token is valid.")
            print(f"   - Username: {user_info.get('name')}")
            if user_info.get('email'):
                print(f"   - Email: {user_info.get('email')}")
            print(f"   - Plan: {user_info.get('plan')}")
            sys.exit(0)
        elif response.status_code == 401:
            print("❌ Invalid or expired Hugging Face token.")
            sys.exit(1)
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_hf_token()
