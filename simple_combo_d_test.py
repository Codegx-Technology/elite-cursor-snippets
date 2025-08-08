#!/usr/bin/env python3
"""
Simple test for Combo Pack D implementation (no model downloads)
"""

import sys
from pathlib import Path

print("🧪 Simple Combo Pack D Test")
print("=" * 40)

success_count = 0
total_tests = 0

def test_result(name, success):
    global success_count, total_tests
    total_tests += 1
    if success:
        success_count += 1
        print(f"✅ {name}")
    else:
        print(f"❌ {name}")

# Test 1: File structure
try:
    required_files = [
        "ui.py",
        "batch_generator.py", 
        "mobile_presets.py",
        "offline_video_maker/helpers/__init__.py",
        "offline_video_maker/helpers/media_utils.py",
        "offline_video_maker/helpers/subtitle_engine.py",
        "offline_video_maker/helpers/music_integration.py",
        "offline_video_maker/helpers/vertical_export.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = Path(__file__).parent / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    test_result("File Structure", len(missing_files) == 0)
    if missing_files:
        print(f"   Missing: {', '.join(missing_files)}")
        
except Exception as e:
    test_result("File Structure", False)
    print(f"   Error: {e}")

# Test 2: Import helpers (without model loading)
try:
    sys.path.append(str(Path(__file__).parent / "offline_video_maker"))
    
    # Test individual imports
    from offline_video_maker.helpers.media_utils import MediaUtils
    from offline_video_maker.helpers.music_integration import MusicIntegration
    from offline_video_maker.helpers.vertical_export import VerticalExport
    
    test_result("Helper Imports", True)
except Exception as e:
    test_result("Helper Imports", False)
    print(f"   Error: {e}")

# Test 3: Initialize components (without heavy models)
try:
    media_utils = MediaUtils()
    music_integration = MusicIntegration()
    vertical_export = VerticalExport()
    
    test_result("Component Initialization", True)
except Exception as e:
    test_result("Component Initialization", False)
    print(f"   Error: {e}")

# Test 4: Music analysis functionality
try:
    test_story = "Grace from Kibera studies technology and starts a coding school"
    mood_scores = music_integration.analyze_story_mood(test_story)
    category = music_integration.select_music_category(test_story)
    
    success = isinstance(mood_scores, dict) and isinstance(category, str)
    test_result("Music Analysis", success)
    if success:
        print(f"   Selected category: {category}")
except Exception as e:
    test_result("Music Analysis", False)
    print(f"   Error: {e}")

# Test 5: Platform configurations
try:
    platform_info = vertical_export.get_platform_info("tiktok")
    platforms = vertical_export.get_platform_info()
    
    success = isinstance(platform_info, dict) and isinstance(platforms, dict)
    test_result("Platform Configurations", success)
    if success:
        print(f"   Available platforms: {len(platforms)}")
except Exception as e:
    test_result("Platform Configurations", False)
    print(f"   Error: {e}")

# Test 6: Music categories
try:
    categories = music_integration.get_category_info()
    validation = music_integration.validate_music_setup()
    
    success = isinstance(categories, dict) and isinstance(validation, dict)
    test_result("Music Categories", success)
    if success:
        print(f"   Available categories: {len(categories)}")
except Exception as e:
    test_result("Music Categories", False)
    print(f"   Error: {e}")

# Test 7: Basic dependencies
try:
    import gradio
    import pathlib
    from PIL import Image
    
    test_result("Core Dependencies", True)
except ImportError as e:
    test_result("Core Dependencies", False)
    print(f"   Missing: {e}")

# Test 8: Batch generator import
try:
    from batch_generator import BatchVideoGenerator
    test_result("Batch Generator Import", True)
except Exception as e:
    test_result("Batch Generator Import", False)
    print(f"   Error: {e}")

# Test 9: Mobile presets import
try:
    from mobile_presets import MobilePresets
    mobile_presets = MobilePresets()
    preset_info = mobile_presets.get_preset_info("tiktok")
    
    success = isinstance(preset_info, dict) and len(preset_info) > 0
    test_result("Mobile Presets", success)
except Exception as e:
    test_result("Mobile Presets", False)
    print(f"   Error: {e}")

# Summary
print("\n" + "=" * 40)
print("📊 TEST SUMMARY")
print("=" * 40)
print(f"Total Tests: {total_tests}")
print(f"✅ Passed: {success_count}")
print(f"❌ Failed: {total_tests - success_count}")
print(f"Success Rate: {(success_count/total_tests)*100:.1f}%")

if success_count == total_tests:
    print("\n🎉 ALL COMBO PACK D CORE TESTS PASSED!")
    print("✅ File Structure: COMPLETE")
    print("✅ Helper Modules: WORKING") 
    print("✅ Music Integration: WORKING")
    print("✅ Vertical Export: WORKING")
    print("✅ Batch Processing: READY")
    print("✅ Mobile Presets: READY")
    print("✅ Core Dependencies: AVAILABLE")
    print("\n🚀 Combo Pack D is ready for use!")
else:
    print(f"\n⚠️  {total_tests - success_count} tests failed.")
    print("Check the errors above for details.")

print("=" * 40)
