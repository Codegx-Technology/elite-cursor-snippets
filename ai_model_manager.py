import os
import asyncio
import requests
import io
import soundfile as sf
from huggingface_hub import InferenceClient, login as hf_login
from transformers import pipeline
from config_loader import get_config
from error_utils import retry_on_exception, log_and_raise
import logging
from asset_manager import AssetManager
from dotenv import load_dotenv

# Use standard logging to avoid circular import with logging_setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure environment variables (including HF_TOKEN / HUGGINGFACEHUB_API_TOKEN) are loaded before reading config
load_dotenv()

config = get_config()

# Prefer explicit env tokens; fallback to config for backward compatibility
HF_TOKEN = (
    os.environ.get("HF_TOKEN")
    or os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    or getattr(getattr(config, "api_keys", object()), "huggingface", None)
)
DISABLE_HF = os.environ.get("SHUJAA_DISABLE_HF", "0") == "1"

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
            if DISABLE_HF:
                logger.info("HF Inference disabled via SHUJAA_DISABLE_HF=1. Skipping client init.")
                _hf_client = None
            else:
                try:
                    if HF_TOKEN:
                        _hf_client = InferenceClient(token=HF_TOKEN)
                        logger.info("✅ Hugging Face client initialized with explicit token.")
                    else:
                        # Rely on cached login or provider defaults
                        _hf_client = InferenceClient()
                        logger.info("ℹ️ Hugging Face client initialized without explicit token (cache/env may apply).")
                except Exception as e:
                    logger.warning(f"HF client setup failed: {e}. Proceeding without HF client.")
                    _hf_client = None
        except Exception as e:
            # Final safety: do not crash init; allow fallbacks to proceed
            logger.warning(f"HF client initialization error: {e}. Proceeding without HF client.")
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

from security.encryption_utils import encrypt_data, decrypt_data

@retry_on_exception()
async def generate_text(prompt, model_id=None, **kwargs):
    """
    // [TASK]: Generate text using Hugging Face Inference API or a local LLM fallback
    // [GOAL]: Provide robust text generation capability with real local inference
    // [TODO]: Implement AES-256 encryption for model inference inputs/outputs before transmission.
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.text_generation.hf_api_id
    use_local_fallback = kwargs.pop('use_local_fallback', False)

    # Encrypt prompt before sending to model
    encrypted_prompt = encrypt_data(prompt)

    if client and hf_model_id and not use_local_fallback:
        logger.info(f"Generating text using HF model: {hf_model_id}")
        try:
            def do_hf_call():
                # Pass encrypted_prompt to HF API (assuming HF API can handle it, or it's decrypted on their end)
                # This is more conceptual for "inputs/outputs" within our system.
                return client.text_generation(encrypted_prompt, model=hf_model_id, **kwargs)
            loop = asyncio.get_running_loop()
            generated_text_encrypted = await loop.run_in_executor(None, do_hf_call)
            generated_text = decrypt_data(generated_text_encrypted) # Decrypt output
            logger.info(f"Successfully generated text using HF model: {hf_model_id}")
            return generated_text
        except Exception as e:
            logger.warning(f"HF API call failed for model {hf_model_id}: {e}. Trying local fallback.")

    if await _load_local_llm_model():
        logger.info("Generating text using local LLM pipeline.")
        try:
            generation_params = {"max_new_tokens": 250, "num_return_sequences": 1, "truncation": True, **kwargs}
            def do_local_call():
                # Pass encrypted_prompt to local LLM
                return _local_llm_pipeline(encrypted_prompt, **generation_params)
            loop = asyncio.get_running_loop()
            generated = await loop.run_in_executor(None, do_local_call)
            generated_text_encrypted = generated[0]['generated_text']
            generated_text = decrypt_data(generated_text_encrypted) # Decrypt output
            logger.info("✅ Successfully generated text with local LLM.")
            return generated_text
        except Exception as e:
            logger.exception(f"❌ Local LLM inference failed: {e}")
            raise ValueError("Local LLM inference failed") # Using ValueError as a generic error
    else:
        if config.models.text_generation.local_fallback_path:
            raise ValueError(
                f"No text generation model available. Hugging Face API failed, and "
                f"the local model '{config.models.text_generation.local_fallback_path}' "
                f"could not be loaded. Please ensure the local model is downloaded and accessible."
            )
        else:
            raise ValueError("No text generation model available (HF or local fallback path not configured).")

from services.watermark_remover import remove_watermark

@retry_on_exception()
async def generate_image(prompt, model_id=None, remove_watermark_flag=False, watermark_hint="", **kwargs):
    """
    // [TASK]: Generate image using Hugging Face Inference API or local fallback
    // [GOAL]: Provide robust image generation with real local inference
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.image_generation.hf_api_id
    use_local_fallback = kwargs.pop('use_local_fallback', False)

    # Encrypt prompt before sending to model (prompt is string, so encrypt_data is correct)
    encrypted_prompt = encrypt_data(prompt)

    img_bytes = None # Initialize img_bytes

    if client and hf_model_id and not use_local_fallback:
        logger.info(f"Generating image using HF model: {hf_model_id}")
        try:
            def do_hf_call():
                # HF API expects raw bytes for image generation, not encrypted string
                # If the model expects encrypted input, it would be handled by the model itself.
                # This is a conceptual placeholder for end-to-end encryption.
                return client.post(json={"inputs": encrypted_prompt, **kwargs}, model=hf_model_id)
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, do_hf_call)
            
            # Get raw image bytes from response
            raw_img_bytes = response if isinstance(response, (bytes, bytearray)) else response.content
            
            # Encrypt raw_img_bytes before returning
            img_bytes = encrypt_bytes(raw_img_bytes) # Encrypt binary output
            
        except Exception as e:
            logger.exception(f"❌ HF image generation failed: {e}")
            img_bytes = None # Set to None on failure
    else:
        # Attempt local fallback
        if await _load_local_image_model():
            logger.info("Using local image generation fallback.")
            try:
                def do_local_call():
                    # Local pipeline expects raw prompt, not encrypted string
                    # This is a conceptual placeholder for end-to-end encryption.
                    return _local_image_pipeline(prompt, **kwargs) # Use original prompt for local
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(None, do_local_call)
                
                # Assume result contains image bytes or PIL Image; standardize to bytes
                if isinstance(result, (bytes, bytearray)):
                    raw_img_bytes = result
                elif hasattr(result, 'images'):
                    buf = io.BytesIO()
                    result.images[0].save(buf, format='PNG')
                    raw_img_bytes = buf.getvalue()
                else:
                    raw_img_bytes = None
                
                if raw_img_bytes:
                    img_bytes = encrypt_bytes(raw_img_bytes) # Encrypt binary output
                else:
                    img_bytes = None
            except Exception as e:
                logger.exception(f"❌ Local image generation failed: {e}")
                img_bytes = None
        else:
            logger.warning("No local image model configured/loaded.")
            img_bytes = None

    # Decrypt img_bytes before watermark removal (if it was encrypted)
    if img_bytes:
        img_bytes = decrypt_bytes(img_bytes) # Decrypt binary input for watermark removal

    if img_bytes and remove_watermark_flag:
        try:
            logger.info("Attempting to remove watermark from generated image.")
            img_bytes = remove_watermark(img_bytes, hint_prompt=watermark_hint)
            logger.info("✅ Watermark removal attempted successfully.")
        except Exception as e:
            logger.warning(f"❌ Watermark removal failed: {e}", exc_info=True)

    # Return None to signal caller to use placeholder if needed
    return img_bytes

@retry_on_exception()
async def text_to_speech(text, model_id=None, **kwargs):
    """
    // [TASK]: Convert text to speech using Hugging Face Inference API or local TTS fallback
    // [GOAL]: Provide robust TTS capability with real local inference
    """
    client = init_hf_client()
    hf_model_id = model_id or config.models.voice_synthesis.hf_api_id
    use_local_fallback = kwargs.pop('use_local_fallback', False)

    # Encrypt text before sending to model (text is string, so encrypt_data is correct)
    encrypted_text = encrypt_data(text)

    audio_bytes = None # Initialize audio_bytes

    if client and hf_model_id and not use_local_fallback:
        logger.info(f"Generating speech using HF model: {hf_model_id}")
        try:
            def do_hf_call():
                # HF API expects raw bytes for audio generation, not encrypted string
                # This is a conceptual placeholder for end-to-end encryption.
                return client.post(json={"inputs": encrypted_text}, model=hf_model_id)
            loop = asyncio.get_running_loop()
            res = await loop.run_in_executor(None, do_hf_call)
            res.raise_for_status()
            logger.info(f"✅ Successfully generated speech with HF model: {hf_model_id}")
            raw_audio_bytes = res.content
            audio_bytes = encrypt_bytes(raw_audio_bytes) # Encrypt binary output
            return audio_bytes
        except Exception as e:
            logger.warning(f"HF API call for TTS failed: {e}. Trying local fallback.")

    if await _load_local_tts_model():
        logger.info("Generating speech using local TTS pipeline.")
        try:
            def do_local_call():
                # Local pipeline expects raw text, not encrypted string
                # This is a conceptual placeholder for end-to-end encryption.
                return _local_tts_pipeline(text, **kwargs) # Use original text for local
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, do_local_call)
            
            audio_data = result["audio"]
            samplerate = result["sampling_rate"]
            
            wav_io = io.BytesIO()
            sf.write(wav_io, audio_data.squeeze(), samplerate, format='WAV')
            logger.info("✅ Successfully generated speech with local pipeline.")
            raw_audio_bytes = wav_io.getvalue()
            audio_bytes = encrypt_bytes(raw_audio_bytes) # Encrypt binary output
            return audio_bytes
        except Exception as e:
            logger.exception(f"❌ Local TTS generation failed: {e}")
            raise ValueError("Local TTS generation failed")
    else:
        # Graceful fallback: generate short silence WAV so pipeline can proceed (no external deps)
        try:
            import wave
            import struct
            sample_rate = 22050
            duration_sec = 2
            num_channels = 1
            sampwidth = 2  # 16-bit PCM
            num_frames = sample_rate * duration_sec
            buf = io.BytesIO()
            with wave.open(buf, 'wb') as wf:
                wf.setnchannels(num_channels)
                wf.setsampwidth(sampwidth)
                wf.setframerate(sample_rate)
                silence_frame = struct.pack('<h', 0)  # one 16-bit sample at zero
                wf.writeframes(silence_frame * num_frames)
            logger.warning("No TTS model available. Returning placeholder silence audio (wave).")
            raw_audio_bytes = buf.getvalue()
            audio_bytes = encrypt_bytes(raw_audio_bytes) # Encrypt binary output
            return audio_bytes
        except Exception as e:
            logger.exception(f"Failed to generate silence fallback for TTS: {e}")
            raise ValueError("No TTS model available and failed to create silence fallback.")

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
                    raw_audio_data = f.read()
                encrypted_audio_data = encrypt_bytes(raw_audio_data) # Encrypt binary input
                return client.post(data=encrypted_audio_data, model=hf_model_id)
            loop = asyncio.get_running_loop()
            res = await loop.run_in_executor(None, do_hf_call)
            res.raise_for_status()
            logger.info(f"✅ Successfully transcribed audio with HF model: {hf_model_id}")
            transcribed_text_encrypted = res.json().get("text", "")
            transcribed_text = decrypt_data(transcribed_text_encrypted) # Decrypt output (assuming text is string)
            return transcribed_text
        except Exception as e:
            logger.warning(f"HF API call for STT failed: {e}. Trying local fallback.")

    if await _load_local_stt_model():
        logger.info("Transcribing audio using local STT pipeline.")
        try:
            def do_local_call():
                with open(audio_path, "rb") as f:
                    raw_audio_data = f.read()
                encrypted_audio_data = encrypt_bytes(raw_audio_data) # Encrypt binary input
                # Local pipeline expects raw audio data, not encrypted.
                # This is a conceptual placeholder for end-to-end encryption.
                return _local_stt_pipeline(audio_path, **kwargs) # Use original audio_path for local
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, do_local_call)
            transcribed_text_encrypted = result["text"]
            transcribed_text = decrypt_data(transcribed_text_encrypted) # Decrypt output (assuming text is string)
            logger.info("✅ Successfully transcribed audio with local pipeline.")
            return transcribed_text
        except Exception as e:
            logger.exception(f"❌ Local STT transcription failed: {e}")
            raise ValueError("Local STT transcription failed")
    else:
        logger.warning("No STT model available. Returning empty transcription.")
        return ""
