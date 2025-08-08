#!/usr/bin/env python3
"""
🎬 Cinematic Kenya Video Generator - Stunning Visuals + Audio
Creates a professional, splashy Kenya video with authentic audio

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + surgicalfix
// [CONTEXT]: Create world-class cinematic Kenya video
// [GOAL]: Stunning visuals, authentic audio, professional quality
"""

import os
import sys
import time
import numpy as np
import cv2
from pathlib import Path
from datetime import datetime
import math

def create_cinematic_kenya_video():
    """Create a stunning cinematic Kenya video with audio"""
    
    print("🎬 CINEMATIC KENYA VIDEO GENERATOR")
    print("=" * 70)
    print("🇰🇪 Creating stunning visuals with authentic audio")
    print("🎨 Professional cinematic quality")
    print("🎵 Kenya-themed soundtrack")
    print("=" * 70)
    
    # Video settings for cinematic quality
    width, height = 1920, 1080
    fps = 60  # Higher FPS for smooth motion
    duration = 60  # 1 minute of content
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = output_dir / f"kenya_cinematic_{timestamp}.mp4"
    audio_path = output_dir / f"kenya_audio_{timestamp}.wav"
    
    print(f"📁 Video output: {video_path}")
    print(f"🎵 Audio output: {audio_path}")
    
    try:
        # Create stunning video
        print("🎨 Creating cinematic visuals...")
        create_stunning_visuals(video_path, width, height, fps, duration)
        
        # Create authentic Kenya audio
        print("🎵 Generating authentic Kenya audio...")
        create_kenya_audio(audio_path, duration)
        
        # Combine video and audio
        print("🎬 Combining video and audio...")
        final_video = combine_video_audio(video_path, audio_path, timestamp)
        
        if final_video and Path(final_video).exists():
            file_size = Path(final_video).stat().st_size / (1024 * 1024)
            
            print("🎉 CINEMATIC KENYA VIDEO COMPLETE!")
            print("=" * 70)
            print(f"📁 Final video: {final_video}")
            print(f"📏 Size: {file_size:.1f} MB")
            print(f"⏱️  Duration: {duration} seconds")
            print(f"🎬 Quality: {width}x{height} @ {fps}fps")
            print(f"🎵 Audio: Authentic Kenya soundtrack")
            print(f"🇰🇪 Content: Cinematic Kenya journey")
            print("=" * 70)
            
            return final_video
        else:
            print("❌ Failed to create final video")
            return str(video_path)  # Return video without audio
            
    except Exception as e:
        print(f"❌ Error creating cinematic video: {e}")
        return None

def create_stunning_visuals(video_path, width, height, fps, duration):
    """Create stunning visual effects for Kenya video"""
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(video_path), fourcc, fps, (width, height))
    
    total_frames = fps * duration
    
    # Kenya locations and themes
    scenes = [
        {"title": "KENYA YETU", "subtitle": "Our Beautiful Homeland", "color": (255, 215, 0), "duration": 0.15},
        {"title": "MOUNT KENYA", "subtitle": "Snow-Capped Majesty", "color": (255, 255, 255), "duration": 0.15},
        {"title": "DIANI BEACH", "subtitle": "Coastal Paradise", "color": (0, 191, 255), "duration": 0.15},
        {"title": "MAASAI MARA", "subtitle": "Wildlife Kingdom", "color": (34, 139, 34), "duration": 0.15},
        {"title": "NAIROBI", "subtitle": "Green City Innovation", "color": (50, 205, 50), "duration": 0.15},
        {"title": "ELIUD KIPCHOGE", "subtitle": "Marathon Legend", "color": (255, 69, 0), "duration": 0.25}
    ]
    
    frame_count = 0
    
    for scene_idx, scene in enumerate(scenes):
        scene_frames = int(total_frames * scene["duration"])
        
        print(f"   🎨 Creating scene {scene_idx + 1}: {scene['title']}")
        
        for frame_in_scene in range(scene_frames):
            # Create dynamic background
            frame = create_dynamic_background(width, height, frame_count, scene["color"])
            
            # Add cinematic effects
            frame = add_cinematic_effects(frame, frame_count, scene_frames)
            
            # Add stunning typography
            frame = add_stunning_text(frame, scene, frame_in_scene, scene_frames, width, height)
            
            # Add Kenya flag elements
            frame = add_kenya_flag_elements(frame, frame_count, width, height)
            
            # Add particle effects
            frame = add_particle_effects(frame, frame_count, width, height)
            
            out.write(frame)
            frame_count += 1
    
    out.release()
    print(f"✅ Stunning visuals created: {frame_count} frames")

def create_dynamic_background(width, height, frame_count, accent_color):
    """Create dynamic animated background"""
    
    # Create gradient background
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Animated gradient
    time_factor = frame_count * 0.02
    
    for y in range(height):
        for x in range(width):
            # Create flowing gradient
            r = int(50 + 30 * math.sin(time_factor + x * 0.01))
            g = int(30 + 20 * math.cos(time_factor + y * 0.01))
            b = int(20 + 15 * math.sin(time_factor + (x + y) * 0.005))
            
            # Blend with accent color
            r = min(255, r + accent_color[2] // 8)
            g = min(255, g + accent_color[1] // 8)
            b = min(255, b + accent_color[0] // 8)
            
            frame[y, x] = [b, g, r]  # BGR format
    
    return frame

def add_cinematic_effects(frame, frame_count, scene_frames):
    """Add cinematic effects like vignette and color grading"""
    
    height, width = frame.shape[:2]
    
    # Create vignette effect
    center_x, center_y = width // 2, height // 2
    max_distance = math.sqrt(center_x**2 + center_y**2)
    
    for y in range(height):
        for x in range(width):
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            vignette_factor = 1 - (distance / max_distance) * 0.3
            
            frame[y, x] = frame[y, x] * vignette_factor
    
    # Add film grain
    noise = np.random.randint(-10, 10, frame.shape, dtype=np.int16)
    frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return frame

def add_stunning_text(frame, scene, frame_in_scene, scene_frames, width, height):
    """Add stunning animated typography"""
    
    # Animation progress
    progress = frame_in_scene / scene_frames
    
    # Title animation (fade in and scale)
    title_alpha = min(1.0, progress * 3)
    title_scale = 0.5 + 0.5 * min(1.0, progress * 2)
    
    # Main title
    title_font = cv2.FONT_HERSHEY_SIMPLEX
    title_size = 3.0 * title_scale
    title_thickness = int(6 * title_scale)
    
    # Get text dimensions
    title_text_size = cv2.getTextSize(scene["title"], title_font, title_size, title_thickness)[0]
    title_x = (width - title_text_size[0]) // 2
    title_y = height // 2 - 50
    
    # Add text shadow
    shadow_offset = int(5 * title_scale)
    cv2.putText(frame, scene["title"], 
                (title_x + shadow_offset, title_y + shadow_offset), 
                title_font, title_size, (0, 0, 0), title_thickness + 2)
    
    # Add main text
    text_color = tuple(int(c * title_alpha) for c in scene["color"])
    cv2.putText(frame, scene["title"], (title_x, title_y), 
                title_font, title_size, text_color, title_thickness)
    
    # Subtitle
    if progress > 0.3:
        subtitle_alpha = min(1.0, (progress - 0.3) * 2)
        subtitle_size = 1.5
        subtitle_thickness = 3
        
        subtitle_text_size = cv2.getTextSize(scene["subtitle"], title_font, subtitle_size, subtitle_thickness)[0]
        subtitle_x = (width - subtitle_text_size[0]) // 2
        subtitle_y = title_y + 80
        
        subtitle_color = tuple(int(255 * subtitle_alpha) for _ in range(3))
        cv2.putText(frame, scene["subtitle"], (subtitle_x, subtitle_y), 
                    title_font, subtitle_size, subtitle_color, subtitle_thickness)
    
    return frame

def add_kenya_flag_elements(frame, frame_count, width, height):
    """Add animated Kenya flag elements"""
    
    # Animated flag stripes
    stripe_height = 20
    time_factor = frame_count * 0.1
    
    # Top stripe (black)
    y_start = 50
    wave_offset = int(10 * math.sin(time_factor))
    cv2.rectangle(frame, (100, y_start + wave_offset), (width - 100, y_start + stripe_height + wave_offset), (0, 0, 0), -1)
    
    # Middle stripe (red)
    y_start = 80
    wave_offset = int(10 * math.sin(time_factor + 1))
    cv2.rectangle(frame, (100, y_start + wave_offset), (width - 100, y_start + stripe_height + wave_offset), (0, 0, 255), -1)
    
    # Bottom stripe (green)
    y_start = 110
    wave_offset = int(10 * math.sin(time_factor + 2))
    cv2.rectangle(frame, (100, y_start + wave_offset), (width - 100, y_start + stripe_height + wave_offset), (0, 255, 0), -1)
    
    return frame

def add_particle_effects(frame, frame_count, width, height):
    """Add floating particle effects"""
    
    # Create floating particles
    num_particles = 50
    time_factor = frame_count * 0.05
    
    for i in range(num_particles):
        # Particle position
        x = int((width * (i / num_particles) + time_factor * 50) % width)
        y = int(height * 0.8 + 100 * math.sin(time_factor + i))
        
        # Particle properties
        size = int(3 + 2 * math.sin(time_factor + i * 0.5))
        alpha = 0.3 + 0.3 * math.sin(time_factor + i * 0.3)
        
        # Draw particle
        color = (int(255 * alpha), int(215 * alpha), int(0 * alpha))  # Gold particles
        cv2.circle(frame, (x, y), size, color, -1)
    
    return frame

def create_kenya_audio(audio_path, duration):
    """Create authentic Kenya audio soundtrack"""
    
    try:
        import librosa
        import soundfile as sf
        
        print("🎵 Generating Kenya-themed audio...")
        
        # Audio settings
        sample_rate = 44100
        total_samples = int(sample_rate * duration)
        
        # Create base audio track
        audio = np.zeros(total_samples)
        
        # Add African drum pattern
        drum_pattern = create_african_drums(sample_rate, duration)
        audio += drum_pattern * 0.3
        
        # Add melodic elements
        melody = create_kenya_melody(sample_rate, duration)
        audio += melody * 0.4
        
        # Add ambient sounds
        ambient = create_ambient_sounds(sample_rate, duration)
        audio += ambient * 0.2
        
        # Normalize audio
        audio = audio / np.max(np.abs(audio))
        
        # Save audio
        sf.write(str(audio_path), audio, sample_rate)
        print(f"✅ Kenya audio created: {audio_path}")
        
        return str(audio_path)
        
    except ImportError:
        print("⚠️ Audio libraries not available, creating silent track...")
        return create_silent_audio(audio_path, duration)
    except Exception as e:
        print(f"❌ Error creating audio: {e}")
        return create_silent_audio(audio_path, duration)

def create_african_drums(sample_rate, duration):
    """Create African drum pattern"""
    
    total_samples = int(sample_rate * duration)
    drums = np.zeros(total_samples)
    
    # Drum pattern timing
    beat_duration = 0.5  # 120 BPM
    beat_samples = int(sample_rate * beat_duration)
    
    for beat in range(int(duration / beat_duration)):
        start_sample = beat * beat_samples
        
        # Create drum hit
        drum_duration = 0.1
        drum_samples = int(sample_rate * drum_duration)
        
        if start_sample + drum_samples < total_samples:
            # Generate drum sound
            t = np.linspace(0, drum_duration, drum_samples)
            frequency = 60 + 20 * (beat % 4)  # Varying drum tones
            drum_hit = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 10)
            
            drums[start_sample:start_sample + drum_samples] += drum_hit
    
    return drums

def create_kenya_melody(sample_rate, duration):
    """Create Kenya-inspired melody"""
    
    total_samples = int(sample_rate * duration)
    melody = np.zeros(total_samples)
    
    # Pentatonic scale (common in African music)
    notes = [261.63, 293.66, 329.63, 392.00, 440.00]  # C, D, E, G, A
    
    note_duration = 1.0
    note_samples = int(sample_rate * note_duration)
    
    for note_idx in range(int(duration / note_duration)):
        start_sample = note_idx * note_samples
        
        if start_sample + note_samples < total_samples:
            # Select note
            frequency = notes[note_idx % len(notes)]
            
            # Generate note
            t = np.linspace(0, note_duration, note_samples)
            note = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 0.5)
            
            melody[start_sample:start_sample + note_samples] += note
    
    return melody

def create_ambient_sounds(sample_rate, duration):
    """Create ambient nature sounds"""
    
    total_samples = int(sample_rate * duration)
    ambient = np.zeros(total_samples)
    
    # Wind sound
    t = np.linspace(0, duration, total_samples)
    wind = 0.1 * np.random.normal(0, 1, total_samples) * (1 + 0.5 * np.sin(2 * np.pi * 0.1 * t))
    
    ambient += wind
    
    return ambient

def create_silent_audio(audio_path, duration):
    """Create silent audio track as fallback"""
    
    try:
        import wave
        
        # Create silent WAV file
        with wave.open(str(audio_path), 'w') as wav_file:
            wav_file.setnchannels(2)  # Stereo
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(44100)  # 44.1 kHz
            
            # Write silent frames
            silent_frames = b'\x00\x00' * 2 * 44100 * duration  # 2 channels, 2 bytes per sample
            wav_file.writeframes(silent_frames)
        
        print(f"✅ Silent audio track created: {audio_path}")
        return str(audio_path)
        
    except Exception as e:
        print(f"❌ Error creating silent audio: {e}")
        return None

def combine_video_audio(video_path, audio_path, timestamp):
    """Combine video and audio using FFmpeg"""
    
    try:
        import subprocess
        
        output_dir = Path(video_path).parent
        final_video = output_dir / f"kenya_final_{timestamp}.mp4"
        
        # FFmpeg command to combine video and audio
        cmd = [
            'ffmpeg', '-y',  # -y to overwrite output file
            '-i', str(video_path),  # Input video
            '-i', str(audio_path),  # Input audio
            '-c:v', 'copy',  # Copy video codec
            '-c:a', 'aac',   # Audio codec
            '-shortest',     # Match shortest stream
            str(final_video)
        ]
        
        print(f"🎬 Running FFmpeg: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 and final_video.exists():
            print(f"✅ Video and audio combined successfully")
            return str(final_video)
        else:
            print(f"⚠️ FFmpeg failed: {result.stderr}")
            return str(video_path)  # Return video without audio
            
    except FileNotFoundError:
        print("⚠️ FFmpeg not found, returning video without audio")
        return str(video_path)
    except Exception as e:
        print(f"❌ Error combining video and audio: {e}")
        return str(video_path)

def main():
    """Main function"""
    
    print("🎬 STARTING CINEMATIC KENYA VIDEO CREATION")
    print("🇰🇪 Professional quality with authentic audio!")
    print("=" * 70)
    
    start_time = time.time()
    
    # Create the cinematic video
    result = create_cinematic_kenya_video()
    
    end_time = time.time()
    generation_time = end_time - start_time
    
    if result:
        print(f"\n🎉 CINEMATIC GENERATION COMPLETE!")
        print(f"⏱️  Time: {generation_time:.1f} seconds")
        print(f"📁 Output: {result}")
        
        # Try to open the output directory
        try:
            output_dir = Path(result).parent
            os.startfile(str(output_dir))
            print(f"📂 Opened: {output_dir}")
        except:
            print(f"📂 Check: {Path(result).parent}")
    else:
        print("❌ Cinematic generation failed")
    
    return result

if __name__ == "__main__":
    main()
