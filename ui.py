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

from offline_video_maker.generate_video import VideoGenerator
from offline_video_maker.helpers import MediaUtils, SubtitleEngine, MusicIntegration, VerticalExport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ShujaaStudioUI:
    """Professional Gradio UI for Shujaa Studio video generation"""
    
    def __init__(self):
        self.video_generator = VideoGenerator()
        self.media_utils = MediaUtils()
        self.subtitle_engine = SubtitleEngine()
        self.music_integration = MusicIntegration()
        self.vertical_export = VerticalExport()
        
        # UI state
        self.current_video_path = None
        self.current_scenes = []
        
        logger.info("[UI] Shujaa Studio UI initialized")
    
    def generate_video_with_progress(self, prompt: str, enable_subtitles: bool = True,
                                   enable_music: bool = True, 
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
        """Create the Gradio interface"""
        
        # Custom CSS for Kenya-first branding
        css = """
        .gradio-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .header {
            text-align: center;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .example-prompt {
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        }
        """
        
        with gr.Blocks(css=css, title="Shujaa Studio - AI Video Generator") as interface:
            
            # Header
            gr.HTML("""
            <div class="header">
                <h1>🎬 Shujaa Studio</h1>
                <h3>Elite AI Video Generation with Kenya-First Storytelling</h3>
                <p>Transform your stories into professional videos with SDXL images, voice narration, and mobile-optimized export</p>
            </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Input section
                    gr.Markdown("## 📝 Story Input")
                    
                    prompt_input = gr.Textbox(
                        label="Enter your story prompt",
                        placeholder="Tell a compelling story with Kenya-first themes...",
                        lines=4,
                        max_lines=8
                    )
                    
                    # Options
                    with gr.Row():
                        enable_subtitles = gr.Checkbox(
                            label="Add Subtitles",
                            value=True,
                            info="Generate and burn subtitles using Whisper"
                        )
                        enable_music = gr.Checkbox(
                            label="Background Music",
                            value=True,
                            info="Add Kenya-appropriate background music"
                        )
                    
                    # Platform export options
                    platform_options = gr.CheckboxGroup(
                        choices=["tiktok", "instagram_stories", "whatsapp", "youtube_shorts"],
                        label="Export Platforms",
                        info="Select platforms for optimized export"
                    )
                    
                    # Generate button
                    generate_btn = gr.Button(
                        "🎬 Generate Video",
                        variant="primary",
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    # Example prompts
                    gr.Markdown("## 💡 Example Prompts")
                    
                    example_prompts = self.get_example_prompts()
                    
                    for i, example in enumerate(example_prompts):
                        gr.HTML(f"""
                        <div class="example-prompt">
                            <strong>Example {i+1}:</strong><br>
                            {example[:150]}...
                        </div>
                        """)
                        
                        if i == 0:  # Add click functionality for first example
                            gr.Button(
                                f"Use Example {i+1}",
                                size="sm"
                            ).click(
                                lambda: example,
                                outputs=prompt_input
                            )
            
            # Output section
            gr.Markdown("## 🎥 Generated Video")
            
            with gr.Row():
                with gr.Column(scale=2):
                    video_output = gr.Video(
                        label="Generated Video",
                        height=400
                    )
                
                with gr.Column(scale=1):
                    status_output = gr.Textbox(
                        label="Status",
                        lines=3,
                        interactive=False
                    )
                    
                    scene_info_output = gr.Textbox(
                        label="Scene Information",
                        lines=8,
                        interactive=False
                    )
            
            # Connect the generate button
            generate_btn.click(
                fn=self.generate_video_with_progress,
                inputs=[prompt_input, enable_subtitles, enable_music, platform_options],
                outputs=[video_output, status_output, scene_info_output]
            )
            
            # Footer
            gr.HTML("""
            <div style="text-align: center; margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
                <p><strong>🇰🇪 Shujaa Studio</strong> - Empowering African storytellers with AI technology</p>
                <p>Built with ❤️ for Kenya-first content creation</p>
            </div>
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
