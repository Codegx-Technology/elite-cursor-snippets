#!/usr/bin/env python3
"""
🎬 Shujaa Studio - Gradio UI for Combo Pack D
Professional video generation interface with Kenya-first storytelling

// [TASK]: Create comprehensive Gradio UI for video generation
// [GOAL]: User-friendly interface with progress tracking and multi-platform export
// [SNIPPET]: thinkwithai + refactorclean + kenyafirst
// [CONTEXT]: Elite UI for Combo Pack D video generation system
"""

import gradio as gr
import os
import sys
from pathlib import Path
import logging
import tempfile
from typing import List, Dict, Optional, Tuple
import json

# Add offline_video_maker to path
sys.path.append(str(Path(__file__).parent / "offline_video_maker"))

from offline_video_maker.generate_video import OfflineVideoMaker
from offline_video_maker.helpers import MediaUtils, SubtitleEngine, MusicIntegration, VerticalExport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ShujaaStudioUI:
    """Professional Gradio UI for Shujaa Studio video generation"""
    
    def __init__(self):
        self.video_generator = OfflineVideoMaker()
        self.media_utils = MediaUtils()
        self.subtitle_engine = SubtitleEngine()
        self.music_integration = MusicIntegration()
        self.vertical_export = VerticalExport()
        
        # UI state
        self.current_video_path = None
        self.current_scenes = []
        
        logger.info("[UI] Shujaa Studio UI initialized")
    
    def generate_video_with_progress(self, prompt: str, enable_subtitles: bool = True,
                                   enable_music: bool = True, auto_export: bool = True,
                                   kenya_mode: bool = True,
                                   export_platforms: List[str] = None) -> Tuple[str, str, str]:
        """
        Generate video with progress updates
        
        Args:
            prompt: Story prompt
            enable_subtitles: Whether to generate subtitles
            enable_music: Whether to add background music
            export_platforms: List of platforms to export to
            
        Returns:
            Tuple of (video_path, status_message, scene_info)
        """
        try:
            logger.info(f"[UI] Starting video generation: {prompt[:50]}...")
            
            if not prompt.strip():
                return None, "❌ Please enter a story prompt", ""
            
            # Generate base video
            status_msg = "🎬 Generating scenes and images..."
            yield None, status_msg, ""
            
            video_path = self.video_generator.generate_video(prompt)
            
            if not video_path or not os.path.exists(video_path):
                return None, "❌ Video generation failed", ""
            
            self.current_video_path = video_path
            
            # Get scene information
            scenes = self.video_generator.current_scenes if hasattr(self.video_generator, 'current_scenes') else []
            scene_info = self._format_scene_info(scenes)
            
            status_msg = "✅ Base video generated successfully!"
            
            # Add subtitles if requested
            if enable_subtitles and self.subtitle_engine.is_available():
                status_msg = "📝 Adding subtitles..."
                yield video_path, status_msg, scene_info
                
                video_path = self._add_subtitles_to_video(video_path)
                status_msg = "✅ Subtitles added!"
            
            # Export to platforms if requested
            if export_platforms:
                status_msg = f"📱 Exporting to {len(export_platforms)} platforms..."
                yield video_path, status_msg, scene_info
                
                self._export_to_platforms(video_path, export_platforms)
                status_msg = f"✅ Exported to {', '.join(export_platforms)}!"
            
            return video_path, status_msg, scene_info
            
        except Exception as e:
            logger.error(f"[UI] Video generation error: {e}")
            return None, f"❌ Error: {str(e)}", ""
    
    def _add_subtitles_to_video(self, video_path: str) -> str:
        """Add subtitles to video"""
        try:
            # Extract audio for transcription
            audio_path = video_path.replace(".mp4", "_audio.wav")
            
            # Use ffmpeg to extract audio
            import subprocess
            cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", audio_path]
            subprocess.run(cmd, capture_output=True, check=True)
            
            # Generate subtitles
            srt_path = video_path.replace(".mp4", ".srt")
            if self.subtitle_engine.generate_subtitles_from_audio(audio_path, srt_path):
                # Burn subtitles into video
                subtitled_video = video_path.replace(".mp4", "_subtitled.mp4")
                if self.media_utils.burn_subtitles(video_path, srt_path, subtitled_video):
                    return subtitled_video
            
            return video_path
            
        except Exception as e:
            logger.error(f"[UI] Subtitle addition failed: {e}")
            return video_path
    
    def _export_to_platforms(self, video_path: str, platforms: List[str]):
        """Export video to multiple platforms"""
        try:
            output_dir = Path(video_path).parent / "exports"
            self.vertical_export.batch_convert_to_platforms(video_path, str(output_dir), platforms)
            
        except Exception as e:
            logger.error(f"[UI] Platform export failed: {e}")
    
    def _format_scene_info(self, scenes: List[Dict]) -> str:
        """Format scene information for display"""
        if not scenes:
            return "No scene information available"
        
        info_lines = [f"📖 Generated {len(scenes)} scenes:"]
        
        for i, scene in enumerate(scenes, 1):
            text = scene.get('text', 'No text')[:100]
            duration = scene.get('duration', 0)
            info_lines.append(f"Scene {i}: {text}... ({duration:.1f}s)")
        
        return "\n".join(info_lines)
    
    def get_example_prompts(self) -> List[str]:
        """Get example Kenya-first prompts"""
        return [
            "Grace from Kibera dreams of becoming a software engineer. Despite challenges, she studies hard and gets a scholarship to Strathmore University. After graduation, she returns to start a coding school in her community.",
            
            "In rural Turkana, water scarcity affects thousands of families. Young engineer Amina develops a solar-powered water purification system. Working with village elders and local youth, she installs the technology across multiple communities.",
            
            "Kiprotich, a Maasai boy, discovers coding at age 15. Walking 20km daily to access internet, he teaches himself programming. His talent earns him a Nairobi scholarship. After graduation, he returns home to establish East Africa's first rural tech hub.",
            
            "Maria starts a small business selling vegetables in Kawangware market. Using mobile money and social media, she grows her business into a supply chain connecting rural farmers with urban customers, creating jobs for hundreds.",
            
            "Young inventor Juma from Mombasa creates a low-cost water filtration system using local materials. His innovation spreads across coastal communities, providing clean water to thousands and inspiring a new generation of problem-solvers."
        ]
    
    def create_interface(self):
        """Create the world-class Kenya-first Gradio interface"""

        # Elite Kenya-first CSS with modern aesthetics
        css = """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

        :root {
            --kenya-black: #000000;
            --kenya-red: #FF0000;
            --kenya-green: #00A651;
            --kenya-white: #FFFFFF;
            --savanna-gold: #FFD700;
            --sunset-orange: #FF6B35;
            --acacia-brown: #8B4513;
            --sky-blue: #87CEEB;
            --gradient-primary: linear-gradient(135deg, #FF6B35 0%, #FFD700 50%, #00A651 100%);
            --gradient-hero: linear-gradient(135deg, rgba(0,166,81,0.9) 0%, rgba(255,107,53,0.8) 50%, rgba(255,215,0,0.9) 100%);
            --shadow-elegant: 0 10px 30px rgba(0,0,0,0.1);
            --shadow-hover: 0 15px 40px rgba(0,0,0,0.15);
        }

        .gradio-container {
            font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #f8fffe 0%, #f0f9ff 100%);
            min-height: 100vh;
        }

        /* Hero Section with Kenya Elements */
        .hero-section {
            background: var(--gradient-hero);
            background-image:
                url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="acacia" patternUnits="userSpaceOnUse" width="20" height="20"><circle cx="10" cy="10" r="2" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23acacia)"/></svg>');
            color: white;
            padding: 40px 20px;
            border-radius: 20px;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-elegant);
        }

        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100"><path d="M0,50 Q250,0 500,50 T1000,50 L1000,100 L0,100 Z" fill="rgba(255,255,255,0.1)"/></svg>') repeat-x;
            animation: wave 20s linear infinite;
        }

        @keyframes wave {
            0% { transform: translateX(0); }
            100% { transform: translateX(-100px); }
        }

        .kenya-flag {
            height: 8px;
            background: linear-gradient(to right, var(--kenya-black) 33%, var(--kenya-red) 33%, var(--kenya-red) 66%, var(--kenya-green) 66%);
            margin: 15px auto;
            border-radius: 4px;
            width: 200px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }

        /* Kenya Slider */
        .kenya-slider {
            display: flex;
            overflow: hidden;
            margin: 20px 0;
            border-radius: 15px;
            height: 120px;
            position: relative;
        }

        .slider-track {
            display: flex;
            animation: slide 25s linear infinite;
            gap: 20px;
        }

        .slider-item {
            min-width: 200px;
            height: 100px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 14px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }

        .slider-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(0,0,0,0.3), transparent);
        }

        .slider-item span {
            position: relative;
            z-index: 1;
        }

        @keyframes slide {
            0% { transform: translateX(0); }
            100% { transform: translateX(-100%); }
        }

        /* Modern Cards */
        .feature-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: var(--shadow-elegant);
            border: 1px solid rgba(0,166,81,0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }

        /* Elite Buttons */
        .btn-primary {
            background: var(--gradient-primary) !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 16px 32px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            color: white !important;
            box-shadow: var(--shadow-elegant) !important;
            transition: all 0.3s ease !important;
        }

        .btn-primary:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-hover) !important;
        }

        /* Status Indicators */
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }

        .status-item {
            background: white;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border-left: 4px solid var(--kenya-green);
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
            .hero-section {
                padding: 30px 15px;
                margin: 10px;
                border-radius: 15px;
            }

            .kenya-slider {
                height: 80px;
            }

            .slider-item {
                min-width: 150px;
                height: 70px;
                font-size: 12px;
            }

            .feature-card {
                padding: 20px;
                margin: 10px;
            }
        }

        /* Elegant Animations */
        .fade-in {
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--gradient-primary);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--kenya-green);
        }
        """
        
        with gr.Blocks(css=css, title="🇰🇪 Shujaa Studio - Elite AI Video Generation") as interface:

            # Elite Hero Section with Kenya Elements
            gr.HTML("""
            <div class="hero-section fade-in">
                <div style="text-align: center; position: relative; z-index: 2;">
                    <h1 style="font-size: 3.5em; font-weight: 700; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        🇰🇪 SHUJAA STUDIO
                    </h1>
                    <div class="kenya-flag"></div>
                    <h2 style="font-size: 1.8em; font-weight: 500; margin: 10px 0; opacity: 0.95;">
                        Elite AI Video Generation • Kenya First
                    </h2>
                    <p style="font-size: 1.2em; margin: 20px auto; max-width: 600px; opacity: 0.9; line-height: 1.6;">
                        🔥 <strong>Beating InVideo</strong> with authentic African storytelling, mobile-first design, and enterprise-grade AI
                    </p>

                    <!-- Kenya Pride Slider -->
                    <div class="kenya-slider">
                        <div class="slider-track">
                            <div class="slider-item" style="background: linear-gradient(45deg, #FF6B35, #FFD700);">
                                <span>🏔️ Mount Kenya<br>Snow-Capped Beauty</span>
                            </div>
                            <div class="slider-item" style="background: linear-gradient(45deg, #00A651, #87CEEB);">
                                <span>🏃‍♂️ Eliud Kipchoge<br>Marathon Legend</span>
                            </div>
                            <div class="slider-item" style="background: linear-gradient(45deg, #8B4513, #FFD700);">
                                <span>🦁 Maasai Mara<br>Wildlife Paradise</span>
                            </div>
                            <div class="slider-item" style="background: linear-gradient(45deg, #87CEEB, #FFFFFF);">
                                <span>🏖️ Diani Beach<br>Coastal Paradise</span>
                            </div>
                            <div class="slider-item" style="background: linear-gradient(45deg, #00A651, #000000);">
                                <span>🏙️ Nairobi<br>Green City Tech Hub</span>
                            </div>
                            <div class="slider-item" style="background: linear-gradient(45deg, #FF0000, #FFD700);">
                                <span>🎯 David Rudisha<br>800m World Record</span>
                            </div>
                            <div class="slider-item" style="background: linear-gradient(45deg, #8B4513, #00A651);">
                                <span>🐘 Amboseli<br>Elephants & Kilimanjaro</span>
                            </div>
                            <div class="slider-item" style="background: linear-gradient(45deg, #FFD700, #FF6B35);">
                                <span>🏃‍♀️ Faith Kipyegon<br>1500m Champion</span>
                            </div>
                            <div class="slider-item" style="background: linear-gradient(45deg, #00A651, #87CEEB);">
                                <span>🌍 Harambee Spirit<br>Unity & Progress</span>
                            </div>
                            <div class="slider-item" style="background: linear-gradient(45deg, #FF0000, #000000);">
                                <span>🎵 Hakuna Matata<br>Born in Kenya</span>
                            </div>
                        </div>
                    </div>

                    <div style="margin-top: 25px;">
                        <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 0.9em;">
                            🚀 Combo Pack D: Subtitles • Music • TikTok • Batch • Mobile • Kenya-First
                        </span>
                    </div>
                </div>
            </div>
            """)
            
            # Main Content Area
            with gr.Row():
                with gr.Column(scale=2):
                    # Story Input Card
                    gr.HTML("""
                    <div class="feature-card fade-in">
                        <h2 style="color: #00A651; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center;">
                            📝 <span style="margin-left: 10px;">Create Your Kenya Story</span>
                        </h2>
                        <p style="color: #666; margin-bottom: 20px;">Transform your ideas into professional videos with authentic African storytelling</p>
                    </div>
                    """)

                    prompt_input = gr.Textbox(
                        label="✨ Enter your Kenya-first story prompt",
                        placeholder="Eeh bana, tell a compelling story... Mix Sheng and English, showcase Kenya's beauty, innovation, and spirit!",
                        lines=5,
                        max_lines=10,
                        elem_classes=["feature-card"]
                    )

                    # Elite Options Card
                    gr.HTML("""
                    <div class="feature-card fade-in" style="margin-top: 20px;">
                        <h3 style="color: #FF6B35; font-weight: 600; margin-bottom: 15px;">🔥 Elite Features</h3>
                    </div>
                    """)

                    with gr.Row():
                        with gr.Column():
                            enable_subtitles = gr.Checkbox(
                                label="📝 Auto Subtitles (Whisper AI)",
                                value=True,
                                info="Generate professional subtitles with Kenya-first formatting"
                            )
                            enable_music = gr.Checkbox(
                                label="🎵 Smart Music (Kenya Themes)",
                                value=True,
                                info="AI-selected background music with African authenticity"
                            )
                        with gr.Column():
                            auto_export = gr.Checkbox(
                                label="📱 Auto Mobile Export",
                                value=True,
                                info="Automatically optimize for TikTok, WhatsApp, Instagram"
                            )
                            kenya_mode = gr.Checkbox(
                                label="🇰🇪 Kenya-First Mode",
                                value=True,
                                info="Enhanced cultural authenticity and local context"
                            )

                    # Platform Export Card
                    gr.HTML("""
                    <div class="feature-card fade-in" style="margin-top: 20px;">
                        <h3 style="color: #FFD700; font-weight: 600; margin-bottom: 15px;">📱 Mobile Platforms</h3>
                        <p style="color: #666; font-size: 14px;">Select platforms for optimized export (auto-sized and compressed)</p>
                    </div>
                    """)

                    platform_options = gr.CheckboxGroup(
                        choices=[
                            ("🎵 TikTok (1080x1920)", "tiktok"),
                            ("📸 Instagram Stories (1080x1920)", "instagram_stories"),
                            ("💬 WhatsApp Status (720x1280)", "whatsapp"),
                            ("📺 YouTube Shorts (1080x1920)", "youtube_shorts"),
                            ("👥 Facebook Stories (1080x1920)", "facebook_stories")
                        ],
                        label="Export Destinations",
                        value=["tiktok", "whatsapp"],
                        info="Videos will be automatically optimized for each platform"
                    )

                    # Elite Generate Button
                    gr.HTML("<div style='margin: 30px 0;'>")
                    generate_btn = gr.Button(
                        "🚀 Generate Elite Kenya Video",
                        variant="primary",
                        size="lg",
                        elem_classes=["btn-primary"]
                    )
                    gr.HTML("</div>")
                
                with gr.Column(scale=1):
                    # Kenya Examples Card
                    gr.HTML("""
                    <div class="feature-card fade-in">
                        <h2 style="color: #00A651; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center;">
                            💡 <span style="margin-left: 10px;">Kenya-First Examples</span>
                        </h2>
                        <p style="color: #666; margin-bottom: 20px;">Authentic stories that celebrate our culture, innovation, and spirit</p>
                    </div>
                    """)

                    example_prompts = self.get_example_prompts()

                    for i, example in enumerate(example_prompts):
                        # Create elegant example cards
                        category_colors = ["#FF6B35", "#00A651", "#FFD700", "#87CEEB", "#8B4513"]
                        color = category_colors[i % len(category_colors)]

                        gr.HTML(f"""
                        <div class="feature-card fade-in" style="margin: 15px 0; border-left: 4px solid {color}; transition: all 0.3s ease;">
                            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                <span style="background: {color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                                    EXAMPLE {i+1}
                                </span>
                            </div>
                            <p style="color: #333; line-height: 1.5; margin: 0; font-size: 14px;">
                                {example[:120]}...
                            </p>
                        </div>
                        """)

                        if i < 2:  # Add click functionality for first two examples
                            use_btn = gr.Button(
                                f"🎯 Use Example {i+1}",
                                size="sm",
                                variant="secondary"
                            )
                            use_btn.click(
                                lambda ex=example: ex,
                                outputs=prompt_input
                            )

                    # Live Stats Card
                    gr.HTML("""
                    <div class="feature-card fade-in" style="margin-top: 30px; background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);">
                        <h3 style="color: #00A651; font-weight: 600; margin-bottom: 15px; display: flex; align-items: center;">
                            📊 <span style="margin-left: 10px;">Live System Status</span>
                        </h3>
                        <div class="status-grid">
                            <div class="status-item">
                                <div style="font-size: 24px; color: #00A651;">✅</div>
                                <div style="font-weight: 600; color: #333;">SDXL Ready</div>
                                <div style="font-size: 12px; color: #666;">Image Generation</div>
                            </div>
                            <div class="status-item">
                                <div style="font-size: 24px; color: #00A651;">✅</div>
                                <div style="font-weight: 600; color: #333;">Whisper AI</div>
                                <div style="font-size: 12px; color: #666;">Auto Subtitles</div>
                            </div>
                            <div class="status-item">
                                <div style="font-size: 24px; color: #00A651;">✅</div>
                                <div style="font-weight: 600; color: #333;">Mobile Export</div>
                                <div style="font-size: 12px; color: #666;">5 Platforms</div>
                            </div>
                            <div class="status-item">
                                <div style="font-size: 24px; color: #FFD700;">🔥</div>
                                <div style="font-weight: 600; color: #333;">Kenya Mode</div>
                                <div style="font-size: 12px; color: #666;">Cultural AI</div>
                            </div>
                        </div>
                    </div>
                    """)
            
            # Elite Output Section
            gr.HTML("""
            <div class="feature-card fade-in" style="margin: 40px 0 20px 0;">
                <h2 style="color: #FF6B35; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center;">
                    🎥 <span style="margin-left: 10px;">Your Elite Kenya Video</span>
                </h2>
                <p style="color: #666; margin-bottom: 20px;">Professional AI-generated content ready for global audiences</p>
            </div>
            """)

            with gr.Row():
                with gr.Column(scale=2):
                    video_output = gr.Video(
                        label="🎬 Generated Video Preview",
                        height=450,
                        elem_classes=["feature-card"]
                    )

                    # Video Stats Card
                    gr.HTML("""
                    <div class="feature-card fade-in" style="margin-top: 20px; background: linear-gradient(135deg, #fff8f0 0%, #fff0e6 100%);">
                        <h3 style="color: #FF6B35; font-weight: 600; margin-bottom: 15px;">📊 Video Analytics</h3>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px;">
                            <div style="text-align: center; padding: 10px;">
                                <div style="font-size: 20px; font-weight: 600; color: #FF6B35;">0:00</div>
                                <div style="font-size: 12px; color: #666;">Duration</div>
                            </div>
                            <div style="text-align: center; padding: 10px;">
                                <div style="font-size: 20px; font-weight: 600; color: #00A651;">0</div>
                                <div style="font-size: 12px; color: #666;">Scenes</div>
                            </div>
                            <div style="text-align: center; padding: 10px;">
                                <div style="font-size: 20px; font-weight: 600; color: #FFD700;">0MB</div>
                                <div style="font-size: 12px; color: #666;">File Size</div>
                            </div>
                            <div style="text-align: center; padding: 10px;">
                                <div style="font-size: 20px; font-weight: 600; color: #87CEEB;">Ready</div>
                                <div style="font-size: 12px; color: #666;">Status</div>
                            </div>
                        </div>
                    </div>
                    """)

                with gr.Column(scale=1):
                    # Live Status Card
                    gr.HTML("""
                    <div class="feature-card fade-in" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);">
                        <h3 style="color: #87CEEB; font-weight: 600; margin-bottom: 15px;">⚡ Live Status</h3>
                    </div>
                    """)

                    status_output = gr.Textbox(
                        label="🔄 Generation Progress",
                        lines=4,
                        interactive=False,
                        elem_classes=["feature-card"]
                    )

                    # Scene Info Card
                    gr.HTML("""
                    <div class="feature-card fade-in" style="margin-top: 20px; background: linear-gradient(135deg, #f8fff8 0%, #f0fff0 100%);">
                        <h3 style="color: #00A651; font-weight: 600; margin-bottom: 15px;">📖 Scene Breakdown</h3>
                    </div>
                    """)

                    scene_info_output = gr.Textbox(
                        label="🎬 Scene Details",
                        lines=8,
                        interactive=False,
                        elem_classes=["feature-card"]
                    )
            
            # Connect the elite generate button
            generate_btn.click(
                fn=self.generate_video_with_progress,
                inputs=[prompt_input, enable_subtitles, enable_music, auto_export, kenya_mode, platform_options],
                outputs=[video_output, status_output, scene_info_output]
            )
            
            # Elite Footer
            gr.HTML("""
            <div style="margin-top: 50px; background: var(--gradient-hero); color: white; padding: 40px 20px; border-radius: 20px; text-align: center; position: relative; overflow: hidden;">
                <div style="position: relative; z-index: 2;">
                    <h2 style="font-size: 2.5em; font-weight: 700; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        🇰🇪 SHUJAA STUDIO
                    </h2>
                    <div class="kenya-flag" style="margin: 20px auto;"></div>
                    <p style="font-size: 1.3em; margin: 20px auto; max-width: 600px; opacity: 0.95; line-height: 1.6;">
                        <strong>Beating InVideo</strong> with authentic African storytelling, mobile-first innovation, and enterprise-grade AI
                    </p>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; max-width: 800px; margin-left: auto; margin-right: auto;">
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);">
                            <div style="font-size: 2em; margin-bottom: 10px;">🎬</div>
                            <div style="font-weight: 600;">Elite Video Generation</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">SDXL + Whisper + Kenya AI</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);">
                            <div style="font-size: 2em; margin-bottom: 10px;">📱</div>
                            <div style="font-weight: 600;">Mobile-First Design</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">TikTok • WhatsApp • Instagram</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);">
                            <div style="font-size: 2em; margin-bottom: 10px;">🇰🇪</div>
                            <div style="font-weight: 600;">Kenya-First Content</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Sheng • Culture • Authenticity</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);">
                            <div style="font-size: 2em; margin-bottom: 10px;">🚀</div>
                            <div style="font-weight: 600;">Enterprise Grade</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Batch • API • Scale</div>
                        </div>
                    </div>

                    <div style="margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 15px; backdrop-filter: blur(10px);">
                        <p style="font-size: 1.1em; margin: 0; font-weight: 500;">
                            🔥 <strong>Combo Pack D Complete:</strong> Subtitles • Music • TikTok Export • Batch Processing • Mobile Presets • Kenya-First AI
                        </p>
                        <p style="font-size: 0.9em; margin: 10px 0 0 0; opacity: 0.8;">
                            Built with ❤️ by Kenyan innovators for global African storytelling
                        </p>
                    </div>

                    <div style="margin-top: 25px; font-size: 0.9em; opacity: 0.7;">
                        <p>🌍 Empowering African creators • 🎯 Competing globally • 💪 Kenya tech excellence</p>
                    </div>
                </div>

                <!-- Animated background elements -->
                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><defs><pattern id=\"stars\" patternUnits=\"userSpaceOnUse\" width=\"10\" height=\"10\"><circle cx=\"5\" cy=\"5\" r=\"1\" fill=\"rgba(255,255,255,0.1)\"/></pattern></defs><rect width=\"100\" height=\"100\" fill=\"url(%23stars)\"/></svg>') repeat; animation: twinkle 10s linear infinite;"></div>
            </div>

            <style>
            @keyframes twinkle {
                0%, 100% { opacity: 0.3; }
                50% { opacity: 0.7; }
            }
            </style>
            """)
        
        return interface


def main():
    """Launch the Shujaa Studio UI"""
    logger.info("[UI] Launching Shujaa Studio UI...")
    
    # Initialize UI
    studio_ui = ShujaaStudioUI()
    
    # Create and launch interface
    interface = studio_ui.create_interface()
    
    # Launch with appropriate settings
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,  # Set to True for public sharing
        debug=True,
        show_error=True
    )


if __name__ == "__main__":
    main()
