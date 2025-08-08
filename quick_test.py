#!/usr/bin/env python3
"""
Quick test for Combo Pack D implementation
"""

import sys
from pathlib import Path

print("🧪 Quick Combo Pack D Test")
print("=" * 40)

# Test 1: Import helpers
try:
    sys.path.append(str(Path(__file__).parent / "offline_video_maker"))
    from offline_video_maker.helpers import MediaUtils, SubtitleEngine, MusicIntegration, VerticalExport
    print("✅ Helper modules imported successfully")
except Exception as e:
    print(f"❌ Helper import failed: {e}")

# Test 2: Initialize components
try:
    media_utils = MediaUtils()
    subtitle_engine = SubtitleEngine()
    music_integration = MusicIntegration()
    vertical_export = VerticalExport()
    print("✅ Components initialized successfully")
except Exception as e:
    print(f"❌ Component initialization failed: {e}")

# Test 3: Test music analysis
try:
    test_story = "Grace from Kibera studies technology and starts a coding school"
    mood_scores = music_integration.analyze_story_mood(test_story)
    category = music_integration.select_music_category(test_story)
    print(f"✅ Music analysis working: {category}")
except Exception as e:
    print(f"❌ Music analysis failed: {e}")

# Test 4: Test platform info
try:
    platform_info = vertical_export.get_platform_info("tiktok")
    print(f"✅ Platform info working: {platform_info.get('resolution', 'Unknown')}")
except Exception as e:
    print(f"❌ Platform info failed: {e}")

# Test 5: Test subtitle availability
try:
    subtitle_available = subtitle_engine.is_available()
    print(f"✅ Subtitle engine: {'Available' if subtitle_available else 'Not available (Whisper not installed)'}")
except Exception as e:
    print(f"❌ Subtitle check failed: {e}")

print("\n🎉 Quick test completed!")
print("Ready to run full Combo Pack D features!")
