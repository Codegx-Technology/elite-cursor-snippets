#!/usr/bin/env python3
"""
🚀 Quick Peter Test - Immediate 3-Second Video
Ultra-fast version for immediate testing

// [SNIPPET]: surgicalfix + thinkwithai + kenyafirst
// [CONTEXT]: Create immediate 3-second test video
// [GOAL]: Fast 3-second video with all features in peter-test folder
"""

import cv2
import numpy as np
from pathlib import Path
import time
import wave
import struct

def create_quick_peter_test():
    """Create quick 3-second test video immediately"""
    
    print("🚀 QUICK PETER TEST - 3-SECOND VIDEO")
    print("=" * 50)
    
    # Create peter-test folder
    output_folder = Path("peter-test")
    output_folder.mkdir(exist_ok=True)
    
    print(f"📁 Output folder: {output_folder.absolute()}")
    
    # Video settings
    fps = 30
    duration = 3
    total_frames = fps * duration  # 90 frames
    width, height = 1280, 720
    
    print(f"⏱️ Creating {duration}-second video ({total_frames} frames)")
    
    # Step 1: Create test image (Kenya flag style)
    print("🎨 Creating Kenya flag image...")
    
    # Create Kenya flag-inspired image
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Kenya flag colors (black, red, white, green)
    stripe_height = height // 4
    
    # Black stripe
    image[0:stripe_height] = [0, 0, 0]
    # Red stripe  
    image[stripe_height:stripe_height*2] = [0, 0, 255]
    # White stripe
    image[stripe_height*2:stripe_height*3] = [255, 255, 255]
    # Green stripe
    image[stripe_height*3:] = [0, 255, 0]
    
    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "KENYA MAJESTY"
    font_scale = 3.0
    thickness = 4
    
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    x = (width - text_size[0]) // 2
    y = height // 2
    
    # Add text with outline
    cv2.putText(image, text, (x+3, y+3), font, font_scale, (0, 0, 0), thickness+3)
    cv2.putText(image, text, (x, y), font, font_scale, (255, 255, 255), thickness)
    
    # Save image
    image_path = output_folder / "kenya_flag_image.png"
    cv2.imwrite(str(image_path), image)
    print(f"✅ Image saved: {image_path}")
    
    # Step 2: Create 3-second audio
    print("🎵 Creating 3-second audio...")
    
    audio_path = output_folder / "kenya_audio_3sec.wav"
    sample_rate = 44100
    
    # Create Kenya anthem-style melody
    frames = []
    notes = [440, 494, 523, 587, 659]  # A, B, C, D, E
    
    for i in range(int(sample_rate * duration)):
        # Create melody
        note_duration = sample_rate * 0.6  # 0.6 seconds per note
        note_index = int(i / note_duration) % len(notes)
        frequency = notes[note_index]
        
        # Add some harmony
        value1 = 0.3 * np.sin(2 * np.pi * frequency * i / sample_rate)
        value2 = 0.2 * np.sin(2 * np.pi * frequency * 1.5 * i / sample_rate)
        
        combined = int(32767 * (value1 + value2))
        combined = max(-32767, min(32767, combined))
        
        frames.append(struct.pack('<h', combined))
    
    with wave.open(str(audio_path), 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(frames))
    
    print(f"✅ Audio saved: {audio_path}")
    
    # Step 3: Create video
    print("🎬 Creating 3-second video...")
    
    video_path = output_folder / "peter_test_video.mp4"
    
    # Use proper codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(video_path), fourcc, fps, (width, height))
    
    if not writer.isOpened():
        print("❌ Video writer failed")
        return None
    
    for frame_num in range(total_frames):
        # Create dynamic frame
        frame = image.copy()
        
        progress = frame_num / total_frames
        
        # Add zoom effect
        zoom_factor = 1.0 + (progress * 0.1)
        center_x, center_y = width // 2, height // 2
        
        crop_w = int(width / zoom_factor)
        crop_h = int(height / zoom_factor)
        x1 = max(0, center_x - crop_w // 2)
        y1 = max(0, center_y - crop_h // 2)
        x2 = min(width, x1 + crop_w)
        y2 = min(height, y1 + crop_h)
        
        cropped = frame[y1:y2, x1:x2]
        frame = cv2.resize(cropped, (width, height))
        
        # Add progress bar
        bar_width = int(width * 0.8)
        bar_height = 10
        bar_x = (width - bar_width) // 2
        bar_y = height - 30
        
        # Background bar
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
        
        # Progress bar
        progress_width = int(bar_width * progress)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), (0, 255, 0), -1)
        
        writer.write(frame)
        
        if frame_num % 15 == 0:  # Every 0.5 seconds
            print(f"   📊 Frame {frame_num}/{total_frames} ({progress*100:.1f}%)")
    
    writer.release()
    
    # Step 4: Combine video and audio using ffmpeg
    print("🎵 Adding audio to video...")
    
    try:
        import subprocess
        
        final_video = output_folder / "peter_test_final.mp4"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            "-movflags", "+faststart",
            str(final_video)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and final_video.exists():
            print(f"✅ Final video created: {final_video}")
            final_path = final_video
        else:
            print("⚠️ Audio merge failed, using video without audio")
            final_path = video_path
            
    except Exception as e:
        print(f"⚠️ ffmpeg not available: {e}")
        final_path = video_path
    
    # Step 5: Summary
    print(f"\n🎉 QUICK PETER TEST COMPLETE!")
    print(f"📁 Folder: {output_folder.absolute()}")
    print(f"📹 Video: {final_path}")
    
    print(f"\n📋 ALL FILES:")
    for file in output_folder.iterdir():
        if file.is_file():
            size = file.stat().st_size / 1024
            print(f"   📄 {file.name}: {size:.1f} KB")
    
    return str(final_path)

if __name__ == "__main__":
    start_time = time.time()
    result = create_quick_peter_test()
    total_time = time.time() - start_time
    
    if result:
        print(f"\n🎯 SUCCESS in {total_time:.1f} seconds!")
        print(f"📹 {result}")
    else:
        print(f"\n❌ Failed after {total_time:.1f} seconds")
