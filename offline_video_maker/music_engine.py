#!/usr/bin/env python3
"""
🎵 Music Engine - Background Music for Professional Videos
Royalty-free music system for InVideo competition
"""

import os
import random
import logging
from pathlib import Path
from typing import Optional, List, Dict
import tempfile

# Audio processing
try:
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.audio.AudioClip import CompositeAudioClip, concatenate_audioclips

    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MusicEngine:
    """Background music system for video generation"""

    def __init__(self, music_dir: Optional[Path] = None):
        self.music_dir = music_dir or Path("music_library")
        self.music_dir.mkdir(exist_ok=True)

        # Music categories for different moods
        self.categories = {
            "inspirational": ["uplifting", "motivational", "success"],
            "storytelling": ["narrative", "gentle", "emotional"],
            "technology": ["modern", "innovative", "digital"],
            "community": ["warm", "together", "unity"],
            "african": ["traditional", "ethnic", "cultural"],
        }

        # Initialize with generated music if no library exists
        self._ensure_music_library()

        logger.info(f"[MUSIC] Music engine initialized: {self.music_dir}")

    def _ensure_music_library(self):
        """Ensure we have basic music tracks"""

        # Check if we have any music files
        music_files = list(self.music_dir.glob("*.mp3")) + list(
            self.music_dir.glob("*.wav")
        )

        if not music_files:
            logger.info("[MUSIC] No music library found, creating basic tracks...")
            self._create_basic_music_library()

    def _create_basic_music_library(self):
        """Create basic procedural music tracks"""

        try:
            # Generate simple background tones using numpy
            import numpy as np
            from scipy.io.wavfile import write as write_wav

            # Basic music parameters
            sample_rate = 44100
            duration = 30  # 30 seconds per track

            # Different musical scales for different moods
            scales = {
                "inspirational": [
                    261.63,
                    293.66,
                    329.63,
                    349.23,
                    392.00,
                    440.00,
                    493.88,
                ],  # C major
                "storytelling": [
                    220.00,
                    246.94,
                    277.18,
                    293.66,
                    329.63,
                    369.99,
                    415.30,
                ],  # A minor
                "african": [
                    261.63,
                    277.18,
                    311.13,
                    349.23,
                    369.99,
                    415.30,
                    466.16,
                ],  # African pentatonic
            }

            for category, frequencies in scales.items():
                logger.info(f"[MUSIC] Generating {category} track...")

                # Create time array
                t = np.linspace(0, duration, int(sample_rate * duration), False)

                # Generate harmonious tones
                wave = np.zeros_like(t)
                for i, freq in enumerate(frequencies):
                    # Add harmonic with decreasing amplitude
                    amplitude = 0.3 / (i + 1)
                    wave += amplitude * np.sin(2 * np.pi * freq * t)

                # Add gentle rhythm
                rhythm = 0.1 * np.sin(2 * np.pi * 2 * t)  # 2 Hz rhythm
                wave = wave * (1 + rhythm)

                # Fade in/out to avoid clicks
                fade_samples = int(0.1 * sample_rate)  # 0.1 second fade
                wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
                wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)

                # Normalize and convert to int16
                wave = wave / np.max(np.abs(wave))
                wave = (wave * 32767).astype(np.int16)

                # Save track
                track_file = self.music_dir / f"{category}_background.wav"
                write_wav(str(track_file), sample_rate, wave)

                logger.info(f"[MUSIC] Created: {track_file.name}")

        except Exception as e:
            logger.warning(f"[MUSIC] Could not generate music: {e}")
            # Create placeholder files
            for category in ["inspirational", "storytelling", "african"]:
                placeholder = self.music_dir / f"{category}_background.txt"
                placeholder.write_text(f"Placeholder for {category} background music")

    def get_music_for_story(self, story_text: str, duration: float) -> Optional[Path]:
        """Get appropriate background music for story"""

        if not MOVIEPY_AVAILABLE:
            logger.warning("[MUSIC] MoviePy not available, skipping music")
            return None

        # Analyze story for appropriate music category
        story_lower = story_text.lower()

        category = "storytelling"  # Default

        if any(
            word in story_lower
            for word in ["technology", "engineer", "computer", "innovation"]
        ):
            category = "technology"
        elif any(
            word in story_lower for word in ["community", "village", "together", "help"]
        ):
            category = "community"
        elif any(
            word in story_lower for word in ["success", "achievement", "dream", "goal"]
        ):
            category = "inspirational"
        elif any(
            word in story_lower for word in ["kenya", "africa", "kibera", "turkana"]
        ):
            category = "african"

        return self._get_music_track(category, duration)

    def _get_music_track(self, category: str, duration: float) -> Optional[Path]:
        """Get music track for specific category and duration"""

        # Find music files for category
        pattern_files = []
        patterns = [f"*{category}*"] + [
            f"*{cat}*" for cat in self.categories.get(category, [])
        ]
        for pattern in patterns:
            pattern_files.extend(self.music_dir.glob(f"{pattern}.wav"))
            pattern_files.extend(self.music_dir.glob(f"{pattern}.mp3"))

        if not pattern_files:
            # Fallback to any music file
            pattern_files = list(self.music_dir.glob("*.wav")) + list(
                self.music_dir.glob("*.mp3")
            )

        if not pattern_files:
            logger.warning(f"[MUSIC] No music found for category: {category}")
            return None

        # Select random track
        selected_track = random.choice(pattern_files)

        try:
            # Load and adjust duration
            audio_clip = AudioFileClip(str(selected_track))

            if audio_clip.duration < duration:
                # Loop the track if it's shorter than needed
                loops_needed = int(duration / audio_clip.duration) + 1
                audio_clip = concatenate_audioclips([audio_clip] * loops_needed)

            # Trim to exact duration
            audio_clip = audio_clip.subclipped(0, duration)

            # Reduce volume for background music (20% of original)
            audio_clip = audio_clip.with_volume_scaled(0.2)

            # Save processed version
            output_file = self.music_dir / f"processed_{category}_{int(duration)}s.wav"
            audio_clip.write_audiofile(str(output_file))
            audio_clip.close()

            logger.info(f"[MUSIC] Prepared background music: {output_file.name}")
            return output_file

        except Exception as e:
            logger.error(f"[MUSIC] Error processing music: {e}")
            return None

    def combine_voice_and_music(
        self, voice_file: Path, music_file: Path, output_file: Path
    ) -> bool:
        """Combine voice narration with background music"""

        if not MOVIEPY_AVAILABLE:
            logger.warning("[MUSIC] MoviePy not available, copying voice only")
            import shutil

            shutil.copy(voice_file, output_file)
            return True

        try:
            # Load audio files
            voice_clip = AudioFileClip(str(voice_file))
            music_clip = AudioFileClip(str(music_file))

            # Ensure music matches voice duration
            if music_clip.duration != voice_clip.duration:
                music_clip = music_clip.subclip(0, voice_clip.duration)

            # Combine with voice prominent
            final_audio = CompositeAudioClip(
                [
                    voice_clip.with_volume_scaled(1.0),  # Full volume voice
                    music_clip.with_volume_scaled(0.15),  # Quiet background music
                ]
            )

            # Save combined audio
            final_audio.write_audiofile(str(output_file))

            # Cleanup
            voice_clip.close()
            music_clip.close()
            final_audio.close()

            logger.info(f"[MUSIC] Combined audio: {output_file.name}")
            return True

        except Exception as e:
            logger.error(f"[MUSIC] Error combining audio: {e}")
            return False

    def get_available_categories(self) -> List[str]:
        """Get available music categories"""
        return list(self.categories.keys())


# Test function
def test_music_engine():
    """Test music engine functionality"""
    print("🧪 Testing Music Engine...")

    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    engine = MusicEngine(temp_dir / "music")

    test_story = "Grace from Kibera studies computer science and starts a coding school"
    music_file = engine.get_music_for_story(test_story, 10.0)  # 10 seconds

    if music_file and music_file.exists():
        print(f"✅ Music generation successful: {music_file}")
    else:
        print("❌ Music generation failed")


if __name__ == "__main__":
    test_music_engine()
