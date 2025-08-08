#!/usr/bin/env python3
"""
🗣️ Voice Engine - Multiple TTS Options for InVideo Competition
Supports Edge TTS, Bark, and pyttsx3 fallback
"""

import os
import asyncio
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceEngine:
    """Multi-engine voice synthesis system"""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Voice engine priorities (best to fallback)
        self.engines = {
            "edge_tts": self._check_edge_tts(),
            "bark": self._check_bark(),
            "pyttsx3": self._check_pyttsx3(),
        }

        # Kenya-first voices
        self.kenyan_voices = {
            "edge_tts": [
                "en-KE-AsiliaNeural",
                "en-KE-ChilembaNeural",
                "en-US-AriaNeural",
            ],
            "bark": ["v2/en_speaker_6", "v2/en_speaker_9"],  # African-sounding voices
            "pyttsx3": ["english"],  # System default
        }

        logger.info(
            f"[VOICE] Available engines: {list(k for k, v in self.engines.items() if v)}"
        )

    def _check_edge_tts(self) -> bool:
        """Check if Edge TTS is available"""
        try:
            import edge_tts

            return True
        except ImportError:
            return False

    def _check_bark(self) -> bool:
        """Check if Bark is available"""
        try:
            import bark

            return True
        except ImportError:
            return False

    def _check_pyttsx3(self) -> bool:
        """Check if pyttsx3 is available"""
        try:
            import pyttsx3

            return True
        except ImportError:
            return False

    async def generate_voice_async(self, text: str, scene_id: str) -> Optional[Path]:
        """Generate voice using best available engine (async)"""

        output_file = self.output_dir / f"voice_{scene_id}.wav"

        # Try engines in order of preference
        if self.engines["edge_tts"]:
            try:
                return await self._generate_edge_tts(text, output_file)
            except Exception as e:
                logger.warning(f"[VOICE] Edge TTS failed: {e}")

        if self.engines["bark"]:
            try:
                return await self._generate_bark(text, output_file)
            except Exception as e:
                logger.warning(f"[VOICE] Bark failed: {e}")

        if self.engines["pyttsx3"]:
            try:
                return self._generate_pyttsx3(text, output_file)
            except Exception as e:
                logger.warning(f"[VOICE] pyttsx3 failed: {e}")

        logger.error("[VOICE] All voice engines failed!")
        return None

    def generate_voice(self, text: str, scene_id: str) -> Optional[Path]:
        """Generate voice (sync wrapper)"""
        return asyncio.run(self.generate_voice_async(text, scene_id))

    async def _generate_edge_tts(self, text: str, output_file: Path) -> Path:
        """Generate using Edge TTS (best quality)"""
        try:
            import edge_tts

            # Use Kenya-first voice selection
            voice = self.kenyan_voices["edge_tts"][0]

            logger.info(f"[EDGE-TTS] Generating with voice: {voice}")

            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(output_file))

            logger.info(f"[EDGE-TTS] Generated: {output_file.name}")
            return output_file

        except Exception as e:
            logger.error(f"[EDGE-TTS] Error: {e}")
            raise

    async def _generate_bark(self, text: str, output_file: Path) -> Path:
        """Generate using Bark (neural voice)"""
        try:
            from bark import generate_audio, SAMPLE_RATE
            from scipy.io.wavfile import write as write_wav
            import numpy as np

            voice_preset = self.kenyan_voices["bark"][0]

            logger.info(f"[BARK] Generating with preset: {voice_preset}")

            # Generate audio
            audio_array = generate_audio(text, history_prompt=voice_preset)

            # Convert to int16 and save
            audio_array = (audio_array * 32767).astype(np.int16)
            write_wav(str(output_file), SAMPLE_RATE, audio_array)

            logger.info(f"[BARK] Generated: {output_file.name}")
            return output_file

        except Exception as e:
            logger.error(f"[BARK] Error: {e}")
            raise

    def _generate_pyttsx3(self, text: str, output_file: Path) -> Path:
        """Generate using pyttsx3 (fallback)"""
        try:
            import pyttsx3

            logger.info("[PYTTSX3] Generating fallback voice...")

            engine = pyttsx3.init()

            # Set Kenya-appropriate voice properties
            voices = engine.getProperty("voices")
            if voices:
                # Prefer female voices for storytelling
                for voice in voices:
                    if "female" in voice.name.lower() or "zira" in voice.name.lower():
                        engine.setProperty("voice", voice.id)
                        break

            # Optimize for storytelling
            engine.setProperty("rate", 160)  # Slightly slower for clarity
            engine.setProperty("volume", 0.9)

            # Save to file
            engine.save_to_file(text, str(output_file))
            engine.runAndWait()

            logger.info(f"[PYTTSX3] Generated: {output_file.name}")
            return output_file

        except Exception as e:
            logger.error(f"[PYTTSX3] Error: {e}")
            raise

    def get_available_engines(self) -> List[str]:
        """Get list of available voice engines"""
        return [engine for engine, available in self.engines.items() if available]

    def install_edge_tts(self) -> bool:
        """Install Edge TTS if not available"""
        if self.engines["edge_tts"]:
            return True

        try:
            import subprocess
            import sys

            logger.info("[VOICE] Installing Edge TTS...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])

            # Refresh engine status
            self.engines["edge_tts"] = self._check_edge_tts()
            logger.info("[VOICE] Edge TTS installed successfully!")
            return True

        except Exception as e:
            logger.error(f"[VOICE] Failed to install Edge TTS: {e}")
            return False


# Quick test function
async def test_voice_engine():
    """Test voice engine functionality"""
    print("🧪 Testing Voice Engine...")

    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    engine = VoiceEngine(temp_dir)

    test_text = (
        "Grace from Kibera studies computer science and transforms her community"
    )

    voice_file = await engine.generate_voice_async(test_text, "test_1")

    if voice_file and voice_file.exists():
        print(f"✅ Voice generation successful: {voice_file}")
    else:
        print("❌ Voice generation failed")


if __name__ == "__main__":
    asyncio.run(test_voice_engine())
