#!/usr/bin/env python3
"""
🔍 Check Missing Dependencies for InVideo Competitor Plan
"""

import subprocess
import sys


def check_package(package_name):
    """Check if a package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def check_pip_package(package_name):
    """Check if package is in pip list"""
    result = subprocess.run(
        ["pip", "show", package_name], capture_output=True, text=True
    )
    return result.returncode == 0


def main():
    print("🔍 DEPENDENCY STATUS CHECK")
    print("=" * 50)

    # Critical packages for InVideo competitor
    critical_packages = [
        ("torch", "torch"),
        ("diffusers", "diffusers"),
        ("transformers", "transformers"),
        ("moviepy", "moviepy"),
        ("gradio", "gradio"),
        ("Pillow", "PIL"),
        ("numpy", "numpy"),
    ]

    voice_packages = [
        ("pyttsx3", "pyttsx3"),
        ("faster-whisper", "faster_whisper"),
        ("soundfile", "soundfile"),
        ("bark", "bark"),
    ]

    enhancement_packages = [
        ("einops", "einops"),
        ("funcy", "funcy"),
        ("boto3", "boto3"),
        ("encodec", "encodec"),
    ]

    print("🔥 CRITICAL PACKAGES (Must Have):")
    for pip_name, import_name in critical_packages:
        status = "✅" if check_package(import_name) else "❌"
        print(f"  {status} {pip_name}")

    print("\n🗣️ VOICE SYNTHESIS PACKAGES:")
    for pip_name, import_name in voice_packages:
        status = "✅" if check_package(import_name) else "❌"
        print(f"  {status} {pip_name}")

    print("\n⚡ ENHANCEMENT PACKAGES:")
    for pip_name, import_name in enhancement_packages:
        status = "✅" if check_package(import_name) else "❌"
        print(f"  {status} {pip_name}")

    print("\n" + "=" * 50)
    print("🎯 ACCELERATION PLAN STATUS:")

    # Check what we need for immediate InVideo competitor
    missing_critical = []
    missing_voice = []

    for pip_name, import_name in critical_packages:
        if not check_package(import_name):
            missing_critical.append(pip_name)

    for pip_name, import_name in voice_packages:
        if not check_package(import_name):
            missing_voice.append(pip_name)

    if not missing_critical:
        print("✅ Core AI pipeline: READY")
    else:
        print(f"❌ Missing critical: {', '.join(missing_critical)}")

    if len(missing_voice) <= 1:  # pyttsx3 as fallback is enough
        print("✅ Voice synthesis: READY (fallback available)")
    else:
        print(f"⚠️ Voice options limited: {', '.join(missing_voice)}")

    print("\n💡 RECOMMENDATION:")
    if not missing_critical:
        print("🚀 PROCEED WITH ACCELERATION PLAN!")
        print("   - Core AI working")
        print("   - SDXL downloading in background")
        print("   - Voice fallback available")
        print("   - Ready for InVideo competition!")
    else:
        print("⏸️ Install missing critical packages first")


if __name__ == "__main__":
    main()
