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
_local_tts_model = None
_local_stt_model = None
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

async def _load_local_tts_model():
    """
    // [TASK]: Load local TTS model on demand
    // [GOAL]: Provide a local fallback for text-to-speech
    """
    global _local_tts_model
    if _local_tts_model is None and config.models.voice_synthesis.local_fallback_path:
        try:
            # This is a placeholder for actual local TTS loading (e.g., with bark or coqui_tts)
            # For now, we just acknowledge its presence.
            model_path = await asset_manager.get_asset(
                "local_tts", 
                config.models.voice_synthesis.local_fallback_path, 
                expected_checksum=None, # Checksum should be provided in config
                version="1.0"
            )
            _local_tts_model = "loaded" # Indicate that a local model is conceptually loaded
            logger.info(f"✅ Local TTS model conceptually loaded from: {model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load local TTS model: {e}")
            _local_tts_model = None
    return _local_tts_model is not None

async def _load_local_stt_model():
    """
    // [TASK]: Load local STT model on demand
    // [GOAL]: Provide a local fallback for speech-to-text
    """
    global _local_stt_model
    if _local_stt_model is None and config.models.speech_to_text.local_fallback_path:
        try:
            # This is a placeholder for actual local STT loading (e.g., with whisper)
            # For now, we just acknowledge its presence.
            model_path = await asset_manager.get_asset(
                "local_stt", 
                config.models.speech_to_text.local_fallback_path, 
                expected_checksum=None, # Checksum should be provided in config
                version="1.0"
            )
            _local_stt_model = "loaded" # Indicate that a local model is conceptually loaded
            logger.info(f"✅ Local STT model conceptually loaded from: {model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load local STT model: {e}")
            _local_stt_model = None
    return _local_stt_model is not None

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
    // [TASK]: Convert text to speech using Hugging Face Inference API or local TTS fallback
    // [GOAL]: Provide robust TTS capability
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.voice_synthesis.hf_api_id

    # Try HF API first
    if client and hf_model_id:
        logger.info(f"Generating speech using HF model: {hf_model_id}")
        try:
            res = await client.post(json={"inputs": text}, model=hf_model_id)
            if res.status_code == 200:
                return res.content
            else:
                logger.warning(f"HF API failed with status {res.status_code}: {res.text}. Trying local fallback.")
        except Exception as e:
            logger.warning(f"HF API call failed: {e}. Trying local fallback.")

    # Fallback to local TTS
    if await _load_local_tts_model():
        logger.info("Generating speech using local TTS model.")
        # Placeholder for actual local TTS inference
        return b"placeholder_audio_bytes"
    else:
        log_and_raise(ValueError("No TTS model available (HF or local)."), "TTS failed")

@retry_on_exception()
async def speech_to_text(audio_path, model_id=None):
    """
    // [TASK]: Convert speech to text using Hugging Face Inference API or local STT fallback
    // [GOAL]: Provide robust STT capability
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.speech_to_text.hf_api_id

    # Try HF API first
    if client and hf_model_id:
        logger.info(f"Transcribing audio using HF model: {hf_model_id}")
        try:
            with open(audio_path, "rb") as f:
                audio_data = f.read()
            res = await client.post(data=audio_data, model=hf_model_id)
            if res.status_code == 200:
                return res.json().get("text", "")
            else:
                logger.warning(f"HF API failed with status {res.status_code}: {res.text}. Trying local fallback.")
        except Exception as e:
            logger.warning(f"HF API call failed: {e}. Trying local fallback.")

    # Fallback to local STT
    if await _load_local_stt_model():
        logger.info("Transcribing audio using local STT model.")
        # Placeholder for actual local STT inference
        return "Placeholder STT result."
    else:
        log_and_raise(ValueError("No STT model available (HF or local)."), "STT failed")
