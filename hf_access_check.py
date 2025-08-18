import os
from hf_utils import validate_hf_model_access, check_hf_inference_endpoint
from logging_setup import get_logger

logger = get_logger(__name__)

HF_TOKEN = os.environ.get("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")

MODELS = [
    "meta-llama/Meta-Llama-3-8B-Instruct",  # LLaMA
    "mistralai/Mistral-7B-Instruct-v0.2",   # Mistral
    "tiiuae/falcon-7b-instruct",            # Falcon
    "bigscience/bloomz-7b1",                # BLOOMZ
    "google/flan-t5-large"                  # FLAN-T5
]

if not HF_TOKEN:
    logger.error("HUGGING_FACE_TOKEN environment variable not set. Please set it to your Hugging Face token.")
else:
    for model in MODELS:
        logger.info(f"--- Checking Model: {model} ---")
        if validate_hf_model_access(model, HF_TOKEN):
            check_hf_inference_endpoint(model, HF_TOKEN)