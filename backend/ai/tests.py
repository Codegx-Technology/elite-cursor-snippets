import unittest
import os
from pathlib import Path
from backend.core.voices.versioning import register_voice, rollback_voice, get_active_voice, VOICE_STORE_DIR, VERSIONS_FILE

class VoiceVersioningE2ETest(unittest.TestCase):

    def setUp(self):
        # Ensure the voice store directory exists
        VOICE_STORE_DIR.mkdir(parents=True, exist_ok=True)
        # Clear the versions.json file before each test to ensure a clean state
        if VERSIONS_FILE.exists():
            VERSIONS_FILE.unlink()

    def tearDown(self):
        # Clean up the versions.json file after each test
        if VERSIONS_FILE.exists():
            VERSIONS_FILE.unlink()

    def test_e2e_voice_rollback(self):
        voice_name = "XTTS"

        # 1. Register XTTS v2
        register_voice(voice_name, "v2", {"lang": "multi", "source": "HuggingFace"})
        self.assertEqual(get_active_voice(voice_name), "v2")

        # 2. Register XTTS v3 (simulating a new release)
        register_voice(voice_name, "v3", {"lang": "multi", "source": "HuggingFace"})
        self.assertEqual(get_active_voice(voice_name), "v3")

        # 3. Simulate rollback to v2
        rolled_back_version = rollback_voice(voice_name, "v2")
        self.assertEqual(rolled_back_version, "v2")
        self.assertEqual(get_active_voice(voice_name), "v2")

        print(f"\nE2E Rollback Test for {voice_name} Passed: Successfully rolled back to {get_active_voice(voice_name)}")

    def test_e2e_elevenlabs_rollback(self):
        voice_name = "ElevenLabs"

        # 1. Register ElevenLabs v1
        register_voice(voice_name, "v1", {"lang": "en", "source": "ElevenLabs"})
        self.assertEqual(get_active_voice(voice_name), "v1")

        # 2. Register ElevenLabs v2
        register_voice(voice_name, "v2", {"lang": "en", "source": "ElevenLabs"})
        self.assertEqual(get_active_voice(voice_name), "v2")

        # 3. Simulate rollback to v1
        rolled_back_version = rollback_voice(voice_name, "v1")
        self.assertEqual(rolled_back_version, "v1")
        self.assertEqual(get_active_voice(voice_name), "v1")

        print(f"\nE2E Rollback Test for {voice_name} Passed: Successfully rolled back to {get_active_voice(voice_name)}")