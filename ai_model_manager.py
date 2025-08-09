import os
import requests
from huggingface_hub import InferenceClient, login as hf_login
from config_loader import get_config
from error_utils import retry_on_exception, log_and_raise
from logging_setup import get_logger

logger = get_logger(__name__)
config = get_config()

HF_API_KEY = config.api_keys.huggingface

_hf_client = None

def init_hf_client():
    """
    // [TASK]: Initialize and return Hugging Face InferenceClient
    // [GOAL]: Centralize HF client setup and login
    """
    global _hf_client
    if _hf_client is None:
        try:
            if HF_API_KEY:
                hf_login(token=HF_API_KEY)
                _hf_client = InferenceClient()
                logger.info("✅ Hugging Face client initialized and logged in.")
            else:
                logger.warning("Hugging Face API key not found. HF client not initialized.")
        except Exception as e:
            log_and_raise(e, "Failed to initialize Hugging Face client")
    return _hf_client

@retry_on_exception()
async def generate_text(prompt, model_id=None):
    """
    // [TASK]: Generate text using Hugging Face Inference API
    // [GOAL]: Provide text generation capability with retry logic
    """
    client = init_hf_client()
    if not client:
        logger.warning("HF client not available, falling back to local text generation placeholder.")
        return "Placeholder text generation: " + prompt

    model_id = model_id or config.models.text_generation.hf_api_id
    if not model_id:
        log_and_raise(ValueError("No Hugging Face text generation model ID configured."), "Text generation failed")

    logger.info(f"Generating text using HF model: {model_id}")
    try:
        # Assuming the model expects 'inputs' in JSON body
        res = await client.post(json={"inputs": prompt}, model=model_id)
        if res.status_code == 200:
            return res.json()[0]["generated_text"]
        else:
            log_and_raise(requests.exceptions.RequestException(f"HF API failed with status {res.status_code}: {res.text}"), "Text generation failed")
    except Exception as e:
        log_and_raise(e, "Text generation failed via HF API")

@retry_on_exception()
async def generate_image(prompt, model_id=None):
    """
    // [TASK]: Generate image using Hugging Face Inference API
    // [GOAL]: Provide image generation capability with retry logic
    """
    client = init_hf_client()
    if not client:
        logger.warning("HF client not available, falling back to local image generation placeholder.")
        # Placeholder for local image generation
        return "placeholder_image_path.png"

    model_id = model_id or config.models.image_generation.hf_api_id
    if not model_id:
        log_and_raise(ValueError("No Hugging Face image generation model ID configured."), "Image generation failed")

    logger.info(f"Generating image using HF model: {model_id}")
    try:
        # Assuming the model expects 'inputs' in JSON body and returns image bytes
        res = await client.post(json={"inputs": prompt}, model=model_id)
        if res.status_code == 200:
            # Save image bytes to a temporary file or return them
            # For now, just return a placeholder path
            return "generated_image_path.png"
        else:
            log_and_raise(requests.exceptions.RequestException(f"HF API failed with status {res.status_code}: {res.text}"), "Image generation failed")
    except Exception as e:
        log_and_raise(e, "Image generation failed via HF API")

@retry_on_exception()
async def text_to_speech(text, model_id=None):
    """
    // [TASK]: Convert text to speech using Hugging Face Inference API
    // [GOAL]: Provide TTS capability with retry logic
    """
    client = init_hf_client()
    if not client:
        logger.warning("HF client not available, falling back to local TTS placeholder.")
        # Placeholder for local TTS
        return "placeholder_audio.wav"

    model_id = model_id or config.models.voice_synthesis.hf_api_id
    if not model_id:
        log_and_raise(ValueError("No Hugging Face TTS model ID configured."), "TTS failed")

    logger.info(f"Generating speech using HF model: {model_id}")
    try:
        # Assuming the model expects 'inputs' in JSON body and returns audio bytes
        res = await client.post(json={"inputs": text}, model=model_id)
        if res.status_code == 200:
            # Save audio bytes to a temporary file or return them
            # For now, just return a placeholder path
            return "generated_audio.wav"
        else:
            log_and_raise(requests.exceptions.RequestException(f"HF API failed with status {res.status_code}: {res.text}"), "TTS failed")
    except Exception as e:
        log_and_raise(e, "TTS failed via HF API")

@retry_on_exception()
async def speech_to_text(audio_path, model_id=None):
    """
    // [TASK]: Convert speech to text using Hugging Face Inference API
    // [GOAL]: Provide STT capability with retry logic
    """
    client = init_hf_client()
    if not client:
        logger.warning("HF client not available, falling back to local STT placeholder.")
        # Placeholder for local STT
        return "Placeholder STT result."

    model_id = model_id or config.models.speech_to_text.hf_api_id
    if not model_id:
        log_and_raise(ValueError("No Hugging Face STT model ID configured."), "STT failed")

    logger.info(f"Transcribing audio using HF model: {model_id}")
    try:
        with open(audio_path, "rb") as f:
            audio_data = f.read()
        res = await client.post(data=audio_data, model=model_id)
        if res.status_code == 200:
            return res.json().get("text", "")
        else:
            log_and_raise(requests.exceptions.RequestException(f"HF API failed with status {res.status_code}: {res.text}"), "STT failed")
    except Exception as e:
        log_and_raise(e, "STT failed via HF API")
