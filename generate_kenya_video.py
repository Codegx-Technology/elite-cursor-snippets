#!/usr/bin/env python3
"""
Generate Kenya Sheng Patriotic Video
Simplified version with better error handling
"""

import os
import sys
from pathlib import Path
import traceback

print("🇰🇪 GENERATING KENYA SHENG PATRIOTIC VIDEO")
print("=" * 60)

# Add the offline_video_maker to path
sys.path.append(str(Path(__file__).parent / "offline_video_maker"))

try:
    from offline_video_maker.generate_video import OfflineVideoMaker
    print("✅ Video generator imported successfully")
    
    # Kenya Sheng script - shorter version for faster generation
    kenya_script = """
    Eeh bana, Kenya yetu ni nchi ya ajabu! From the snow-capped peaks za Mount Kenya hadi the white sandy beaches za Diani, our motherland ni paradise kabisa.
    
    Hapa Kenya, hospitality ni kitu ya kawaida. Ukifika hapa as a visitor, utapokewa na mikono miwili. Karibu sana! Our people wana moyo wa upendo.
    
    Safari hapa Kenya ni experience ya lifetime. Maasai Mara ina the Great Migration, Amboseli ina elephants wakitembea chini ya Kilimanjaro.
    
    Nairobi ni the Green City in the Sun. Technology hub inakua, young entrepreneurs wanafanya miracles. From Kibera to Karen, innovation inaongezeka.
    
    Our athletes - Eliud Kipchoge, David Rudisha, Faith Kipyegon - wameweka Kenya kwa map ya dunia. Harambee! Spirit ya working together.
    
    Nations nyingi zinapenda Kenya. Tourism inaongezeka, investments zinaongezeka. Kenya ni blessed kabisa. Kenya yetu, tunakupenda!
    """
    
    print("📝 Script prepared:")
    print(f"   Length: {len(kenya_script)} characters")
    print(f"   Estimated scenes: 6")
    print(f"   Estimated duration: 30-60 seconds")
    
    print("\n🎬 Initializing video generator...")
    video_maker = OfflineVideoMaker()
    
    print("🚀 Starting video generation...")
    print("   This may take 5-15 minutes depending on your system...")
    print("   AI models will be downloaded on first run...")
    
    # Generate the video
    video_path = video_maker.generate_video(kenya_script.strip())
    
    if video_path and os.path.exists(video_path):
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        
        print("\n🎉 SUCCESS! Video generated successfully!")
        print("=" * 60)
        print(f"📁 Video saved at: {video_path}")
        print(f"📏 File size: {file_size:.1f} MB")
        print(f"📂 Directory: {os.path.dirname(video_path)}")
        
        # Check if file exists and is readable
        if os.access(video_path, os.R_OK):
            print("✅ Video file is accessible and ready to view")
        else:
            print("⚠️  Video file may have permission issues")
            
        print("\n🎬 Video Features:")
        print("✅ Authentic Sheng-English code-switching")
        print("✅ Kenya's natural beauty and landmarks")
        print("✅ Cultural pride and hospitality")
        print("✅ Modern innovation and global recognition")
        print("✅ Emotional patriotic journey")
        
        print("\n📱 Ready for mobile export to:")
        print("   • TikTok (1080x1920)")
        print("   • WhatsApp Status (720x1280)")
        print("   • Instagram Stories (1080x1920)")
        print("   • YouTube Shorts (1080x1920)")
        
        print("\n🇰🇪 KENYA YETU - VIDEO READY! 🎉")
        
    else:
        print("\n❌ Video generation failed")
        print("   No video file was created")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("   Make sure all dependencies are installed")
    
except Exception as e:
    print(f"\n❌ Error during video generation: {e}")
    print("\nFull error details:")
    traceback.print_exc()
    
    print("\n🔧 Troubleshooting tips:")
    print("1. Ensure you have sufficient disk space (>2GB)")
    print("2. Check internet connection for model downloads")
    print("3. Verify all dependencies are installed")
    print("4. Try running with administrator privileges")

print("\n" + "=" * 60)
