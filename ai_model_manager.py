import os
import asyncio
import requests
import io
import soundfile as sf
from huggingface_hub import InferenceClient, login as hf_login
from transformers import pipeline
from config_loader import get_config
from error_utils import retry_on_exception, log_and_raise
from logging_setup import get_logger
from asset_manager import AssetManager

logger = get_logger(__name__)
config = get_config()

HF_API_KEY = config.api_keys.huggingface

# --- Module-level Globals for Model Caching ---
_hf_client = None
_local_llm_pipeline = None
_local_image_pipeline = None
_local_tts_pipeline = None
_local_stt_pipeline = None
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
    global _local_llm_pipeline
    model_name = config.models.text_generation.local_fallback_path
    if _local_llm_pipeline is None and model_name:
        try:
            logger.info(f"Attempting to load local LLM pipeline for model: {model_name}")
            def do_load():
                return pipeline("text-generation", model=model_name, device_map="auto")
            loop = asyncio.get_running_loop()
            _local_llm_pipeline = await loop.run_in_executor(None, do_load)
            logger.info(f"✅ Local LLM pipeline loaded successfully for model: {model_name}")
        except Exception as e:
            logger.exception(f"❌ Failed to load local LLM model '{model_name}': {e}")
            _local_llm_pipeline = None
    return _local_llm_pipeline is not None

async def _load_local_image_model():
    """
    // [TASK]: Load local image generation model on demand
    // [GOAL]: Provide a local fallback for image generation
    """
    global _local_image_pipeline
    model_name = config.models.image_generation.local_fallback_path
    if _local_image_pipeline is None and model_name:
        try:
            logger.info(f"Attempting to load local image generation pipeline for model: {model_name}")
            def do_load():
                return pipeline("text-to-image", model=model_name, device_map="auto")
            loop = asyncio.get_running_loop()
            _local_image_pipeline = await loop.run_in_executor(None, do_load)
            logger.info(f"✅ Local image generation pipeline loaded successfully for model: {model_name}")
        except Exception as e:
            logger.exception(f"❌ Failed to load local image generation model '{model_name}': {e}")
            _local_image_pipeline = None
    return _local_image_pipeline is not None

async def _load_local_tts_model():
    """
    // [TASK]: Load local TTS model on demand
    // [GOAL]: Provide a local fallback for text-to-speech
    """
    global _local_tts_pipeline
    model_name = config.models.voice_synthesis.local_fallback_path
    if _local_tts_pipeline is None and model_name:
        try:
            logger.info(f"Attempting to load local TTS pipeline for model: {model_name}")
            def do_load():
                return pipeline("text-to-speech", model=model_name, device_map="auto")
            loop = asyncio.get_running_loop()
            _local_tts_pipeline = await loop.run_in_executor(None, do_load)
            logger.info(f"✅ Local TTS pipeline loaded successfully for model: {model_name}")
        except Exception as e:
            logger.exception(f"❌ Failed to load local TTS model '{model_name}': {e}")
            _local_tts_pipeline = None
    return _local_tts_pipeline is not None

async def _load_local_stt_model():
    """
    // [TASK]: Load local STT model (e.g., Whisper) on demand
    // [GOAL]: Provide a local fallback for speech-to-text
    """
    global _local_stt_pipeline
    model_name = config.models.speech_to_text.local_fallback_path
    if _local_stt_pipeline is None and model_name:
        try:
            logger.info(f"Attempting to load local STT pipeline for model: {model_name}")
            def do_load():
                return pipeline("automatic-speech-recognition", model=model_name, device_map="auto")
            loop = asyncio.get_running_loop()
            _local_stt_pipeline = await loop.run_in_executor(None, do_load)
            logger.info(f"✅ Local STT pipeline loaded successfully for model: {model_name}")
        except Exception as e:
            logger.exception(f"❌ Failed to load local STT model '{model_name}': {e}")
            _local_stt_pipeline = None
    return _local_stt_pipeline is not None

@retry_on_exception()
async def generate_text(prompt, model_id=None, **kwargs):
    """
    // [TASK]: Generate text using Hugging Face Inference API or a local LLM fallback
    // [GOAL]: Provide robust text generation capability with real local inference
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.text_generation.hf_api_id
    use_local_fallback = kwargs.pop('use_local_fallback', False)

    if client and hf_model_id and not use_local_fallback:
        logger.info(f"Generating text using HF model: {hf_model_id}")
        try:
            def do_hf_call():
                return client.text_generation(prompt, model=hf_model_id, **kwargs)
            loop = asyncio.get_running_loop()
            generated_text = await loop.run_in_executor(None, do_hf_call)
            logger.info(f"Successfully generated text using HF model: {hf_model_id}")
            return generated_text
        except Exception as e:
            logger.warning(f"HF API call failed for model {hf_model_id}: {e}. Trying local fallback.")

    if await _load_local_llm_model():
        logger.info("Generating text using local LLM pipeline.")
        try:
            generation_params = {"max_new_tokens": 250, "num_return_sequences": 1, "truncation": True, **kwargs}
            def do_local_call():
                return _local_llm_pipeline(prompt, **generation_params)
            loop = asyncio.get_running_loop()
            generated = await loop.run_in_executor(None, do_local_call)
            generated_text = generated[0]['generated_text']
            logger.info("✅ Successfully generated text with local LLM.")
            return generated_text
        except Exception as e:
            logger.exception(f"❌ Local LLM inference failed: {e}")
            log_and_raise(e, "Local LLM inference failed")
    
    log_and_raise(ValueError("No text generation model available (HF or local)."), "Text generation failed")

@retry_on_exception()
async def generate_image(prompt, model_id=None, **kwargs):
    """
    // [TASK]: Generate image using Hugging Face Inference API or local fallback
    // [GOAL]: Provide robust image generation with real local inference
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.image_generation.hf_api_id
    use_local_fallback = kwargs.pop('use_local_fallback', False)

    if client and hf_model_id and not use_local_fallback:
        logger.info(f"Generating image using HF model: {hf_model_id}")
        try:
            def do_hf_call():
                return client.post(json={"inputs": prompt, **kwargs}, model=hf_model_id)
            loop = asyncio.get_running_loop()
            res = await loop.run_in_executor(None, do_hf_call)
            res.raise_for_status()
            logger.info(f"✅ Successfully generated image with HF model: {hf_model_id}")
            return res.content
        except Exception as e:
            logger.warning(f"HF API call for image generation failed: {e}. Trying local fallback.")

    if await _load_local_image_model():
        logger.info("Generating image using local image generation pipeline.")
        try:
            def do_local_call():
                return _local_image_pipeline(prompt, **kwargs)
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, do_local_call)
            image = result.images[0]
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            logger.info("✅ Successfully generated image with local pipeline.")
            return img_byte_arr.getvalue()
        except Exception as e:
            logger.exception(f"❌ Local image generation failed: {e}")
            log_and_raise(e, "Local image generation failed")
    
    log_and_raise(ValueError("No image generation model available (HF or local)."), "Image generation failed")

@retry_on_exception()
async def text_to_speech(text, model_id=None, **kwargs):
    """
    // [TASK]: Convert text to speech using Hugging Face Inference API or local TTS fallback
    // [GOAL]: Provide robust TTS capability with real local inference
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.voice_synthesis.hf_api_id
    use_local_fallback = kwargs.pop('use_local_fallback', False)

    if client and hf_model_id and not use_local_fallback:
        logger.info(f"Generating speech using HF model: {hf_model_id}")
        try:
            def do_hf_call():
                return client.post(json={"inputs": text}, model=hf_model_id)
            loop = asyncio.get_running_loop()
            res = await loop.run_in_executor(None, do_hf_call)
            res.raise_for_status()
            logger.info(f"✅ Successfully generated speech with HF model: {hf_model_id}")
            return res.content
        except Exception as e:
            logger.warning(f"HF API call for TTS failed: {e}. Trying local fallback.")

    if await _load_local_tts_model():
        logger.info("Generating speech using local TTS pipeline.")
        try:
            def do_local_call():
                return _local_tts_pipeline(text, **kwargs)
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, do_local_call)
            
            audio_data = result["audio"]
            samplerate = result["sampling_rate"]
            
            wav_io = io.BytesIO()
            sf.write(wav_io, audio_data.squeeze(), samplerate, format='WAV')
            logger.info("✅ Successfully generated speech with local pipeline.")
            return wav_io.getvalue()
        except Exception as e:
            logger.exception(f"❌ Local TTS generation failed: {e}")
            log_and_raise(e, "Local TTS generation failed")
    
    log_and_raise(ValueError("No TTS model available (HF or local)."), "TTS failed")

@retry_on_exception()
async def speech_to_text(audio_path, model_id=None, **kwargs):
    """
    // [TASK]: Convert speech to text using Hugging Face Inference API or local STT fallback
    // [GOAL]: Provide robust STT capability with real local inference
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.speech_to_text.hf_api_id
    use_local_fallback = kwargs.pop('use_local_fallback', False)

    if client and hf_model_id and not use_local_fallback:
        logger.info(f"Transcribing audio using HF model: {hf_model_id}")
        try:
            def do_hf_call():
                with open(audio_path, "rb") as f:
                    audio_data = f.read()
                return client.post(data=audio_data, model=hf_model_id)
            loop = asyncio.get_running_loop()
            res = await loop.run_in_executor(None, do_hf_call)
            res.raise_for_status()
            logger.info(f"✅ Successfully transcribed audio with HF model: {hf_model_id}")
            return res.json().get("text", "")
        except Exception as e:
            logger.warning(f"HF API call for STT failed: {e}. Trying local fallback.")

    if await _load_local_stt_model():
        logger.info("Transcribing audio using local STT pipeline.")
        try:
            def do_local_call():
                return _local_stt_pipeline(audio_path, **kwargs)
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, do_local_call)
            transcribed_text = result["text"]
            logger.info("✅ Successfully transcribed audio with local pipeline.")
            return transcribed_text
        except Exception as e:
            logger.exception(f"❌ Local STT transcription failed: {e}")
            log_and_raise(e, "Local STT transcription failed")
    
    log_and_raise(ValueError("No STT model available (HF or local)."), "STT failed")
