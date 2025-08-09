#!/usr/bin/env python3
"""
🖼️ Quick Image Viewer for Shujaa Generated Content
View the generated news video images with details
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json


def view_news_video_images():
    """Display information about generated images"""

    news_dir = Path("output/news_videos")

    if not news_dir.exists():
        print("❌ News videos directory not found")
        return

    print("🖼️ Shujaa Generated Images Viewer")
    print("=" * 50)

    # Find the latest summary file
    summary_files = list(news_dir.glob("news_video_*_summary.json"))
    if not summary_files:
        print("❌ No news video summaries found")
        return

    latest_summary = max(summary_files, key=os.path.getmtime)
    print(f"📄 Latest video: {latest_summary.name}")

    # Load summary
    with open(latest_summary) as f:
        summary = json.load(f)

    print(f"📰 Title: {summary['article']['title']}")
    print(f"🏷️ Category: {summary['article']['category']}")
    print(f"🌍 Location: {summary['article']['location']}")
    print(f"⏱️ Total Duration: {summary['total_duration']}s")
    print(f"🚀 GPU Accelerated: {summary['gpu_acceleration']}")

    print(f"\n🎬 Generated Segments:")
    print("-" * 30)

    for i, segment in enumerate(summary["segments"], 1):
        visual_path = Path(segment["visual_asset"])

        if visual_path.exists():
            try:
                img = Image.open(visual_path)
                file_size = visual_path.stat().st_size

                print(f"📸 Segment {i}: {segment['title']}")
                print(f"   📁 File: {visual_path.name}")
                print(f"   📏 Size: {img.width}x{img.height} pixels")
                print(f"   💾 File Size: {file_size:,} bytes")
                print(f"   ⏰ Duration: {segment['duration']}s")
                print(f"   ✅ Status: Valid image file")

                # Try to open with default viewer
                try:
                    os.startfile(str(visual_path))
                    print(f"   🖼️ Opened in default viewer")
                except:
                    print(f"   ⚠️ Could not auto-open")

            except Exception as e:
                print(f"   ❌ Error reading image: {e}")
        else:
            print(f"📸 Segment {i}: {segment['title']} - ❌ File not found")

        print()

    print("🎯 Next Steps:")
    print("  • Images should have opened in your default viewer")
    print("  • You can also navigate to the folder manually")
    print("  • Try: python enhanced_shujaa_app.py for full interface")


if __name__ == "__main__":
    view_news_video_images()
