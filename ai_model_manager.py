import os
import requests
from huggingface_hub import InferenceClient, login as hf_login
from config_loader import get_config
from error_utils import retry_on_exception, log_and_raise
from logging_setup import get_logger
from asset_manager import AssetManager

logger = get_logger(__name__)
config = get_config()

HF_API_KEY = config.api_keys.huggingface

_hf_client = None
_local_llm_model = None
_local_image_model = None
asset_manager = AssetManager()

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

async def _load_local_llm_model():
    """
    // [TASK]: Load local LLM model on demand
    // [GOAL]: Provide a local fallback for text generation
    """
    global _local_llm_model
    if _local_llm_model is None and config.models.text_generation.local_fallback_path:
        try:
            # This is a placeholder for actual local LLM loading (e.g., with transformers or llama-cpp-python)
            # For now, we just acknowledge its presence.
            model_path = await asset_manager.get_asset(
                "local_llm", 
                config.models.text_generation.local_fallback_path, 
                expected_checksum=None, # Checksum should be provided in config
                version="1.0"
            )
            _local_llm_model = "loaded" # Indicate that a local model is conceptually loaded
            logger.info(f"✅ Local LLM model conceptually loaded from: {model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load local LLM model: {e}")
            _local_llm_model = None
    return _local_llm_model is not None

async def _load_local_image_model():
    """
    // [TASK]: Load local image generation model on demand
    // [GOAL]: Provide a local fallback for image generation
    """
    global _local_image_model
    if _local_image_model is None and config.models.image_generation.local_fallback_path:
        try:
            # This is a placeholder for actual local image model loading (e.g., with diffusers)
            # For now, we just acknowledge its presence.
            model_path = await asset_manager.get_asset(
                "local_image_gen", 
                config.models.image_generation.local_fallback_path, 
                expected_checksum=None, # Checksum should be provided in config
                version="1.0"
            )
            _local_image_model = "loaded" # Indicate that a local model is conceptually loaded
            logger.info(f"✅ Local image generation model conceptually loaded from: {model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load local image generation model: {e}")
            _local_image_model = None
    return _local_image_model is not None

@retry_on_exception()
async def generate_text(prompt, model_id=None):
    """
    // [TASK]: Generate text using Hugging Face Inference API or local LLM fallback
    // [GOAL]: Provide robust text generation capability
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.text_generation.hf_api_id

    # Try HF API first
    if client and hf_model_id:
        logger.info(f"Generating text using HF model: {hf_model_id}")
        try:
            res = await client.post(json={"inputs": prompt}, model=hf_model_id)
            if res.status_code == 200:
                return res.json()[0]["generated_text"]
            else:
                logger.warning(f"HF API failed with status {res.status_code}: {res.text}. Trying local fallback.")
        except Exception as e:
            logger.warning(f"HF API call failed: {e}. Trying local fallback.")

    # Fallback to local LLM
    if await _load_local_llm_model():
        logger.info("Generating text using local LLM model.")
        # Placeholder for actual local LLM inference
        return "Local LLM generated text: " + prompt
    else:
        log_and_raise(ValueError("No text generation model available (HF or local)."), "Text generation failed")

@retry_on_exception()
async def generate_image(prompt, model_id=None):
    """
    // [TASK]: Generate image using Hugging Face Inference API or local image generation fallback
    // [GOAL]: Provide robust image generation capability
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.image_generation.hf_api_id

    # Try HF API first
    if client and hf_model_id:
        logger.info(f"Generating image using HF model: {hf_model_id}")
        try:
            res = await client.post(json={"inputs": prompt}, model=hf_model_id)
            if res.status_code == 200:
                return res.content
            else:
                logger.warning(f"HF API failed with status {res.status_code}: {res.text}. Trying local fallback.")
        except Exception as e:
            logger.warning(f"HF API call failed: {e}. Trying local fallback.")

    # Fallback to local image generation
    if await _load_local_image_model():
        logger.info("Generating image using local image generation model.")
        # Placeholder for actual local image generation inference
        return b"placeholder_image_bytes"
    else:
        log_and_raise(ValueError("No image generation model available (HF or local)."), "Image generation failed")

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
        return b"placeholder_audio.wav"

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
            return res.content
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
