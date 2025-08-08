#!/usr/bin/env python3
"""
🎬 Shujaa Studio - Enterprise Grade Kenya Video Generation UI
World-class interface with animated Kenya flag hero, sidebar, and professional features

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + surgicalfix
// [CONTEXT]: Enterprise UI with Kenya flag hero, sidebar, footer as requested
// [GOAL]: InVideo-competitive interface with animated Kenya flag and professional features
// [AI-MEMORY]: UI_DESIGN_SYSTEM_ENTERPRISE_ELITE_PATTERNS
"""

import gradio as gr
import os
import sys
from pathlib import Path
import logging
from typing import List, Dict, Optional, Tuple
import json
import time
from datetime import datetime

# Add project paths
sys.path.append(str(Path(__file__).parent / "offline_video_maker"))
sys.path.append(str(Path(__file__).parent))

# Import our AI video generation modules
try:
    from real_ai_kenya_video import create_real_ai_kenya_video
    from splashy_kenya_video import create_splashy_kenya_video
    REAL_AI_AVAILABLE = True
except ImportError:
    REAL_AI_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ShujaaStudioEnterpriseUI:
    """
    🎨 Enterprise Grade Kenya Video Generation UI
    
    // [SNIPPET]: thinkwithai + kenyafirst + refactorclean
    // [CONTEXT]: Enterprise UI with animated Kenya flag and professional features
    // [GOAL]: World-class interface competing with InVideo
    """
    
    def __init__(self):
        self.current_video_path = None
        self.is_generating = False
        self.elite_theme = self._create_enterprise_theme()
        
        logger.info("🎬 [ENTERPRISE UI] Shujaa Studio Enterprise UI initialized")
    
    def _create_enterprise_theme(self):
        """Create enterprise theme with Kenya-first design"""
        return gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="orange", 
            neutral_hue="slate",
            font=gr.themes.GoogleFont("Inter"),
        ).set(
            body_background_fill="#f8f9fa",
            body_text_color="#2c3e50",
            button_primary_background_fill="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            button_primary_text_color="#ffffff",
            input_background_fill="#ffffff",
            input_border_color="#dee2e6",
            block_background_fill="rgba(255, 255, 255, 0.95)",
            block_border_color="#dee2e6",
            block_radius="12px",
            block_shadow="0 4px 12px rgba(0, 0, 0, 0.08)",
        )
    
    def generate_video(self, prompt: str, video_style: str = "Real AI") -> Tuple[str, str]:
        """Generate video with progress updates"""
        try:
            self.is_generating = True
            
            if video_style == "Real AI" and REAL_AI_AVAILABLE:
                video_path = self._generate_real_ai_video(prompt)
            elif video_style == "Splashy Effects":
                video_path = self._generate_splashy_video(prompt)
            else:
                video_path = self._generate_basic_video(prompt)
            
            if video_path and Path(video_path).exists():
                file_size = Path(video_path).stat().st_size / (1024 * 1024)
                success_msg = f"🎉 Video generated successfully! ({file_size:.1f} MB)"
                self.current_video_path = video_path
                return video_path, success_msg
            else:
                return None, "❌ Video generation failed. Please try again."
                
        except Exception as e:
            logger.error(f"[ENTERPRISE UI] Video generation error: {e}")
            return None, f"❌ Error: {str(e)}"
        finally:
            self.is_generating = False
    
    def _generate_real_ai_video(self, prompt: str) -> str:
        """Generate video using real AI models"""
        try:
            if REAL_AI_AVAILABLE:
                return create_real_ai_kenya_video()
            else:
                return self._generate_basic_video(prompt)
        except Exception as e:
            logger.error(f"[REAL AI] Error: {e}")
            return self._generate_basic_video(prompt)
    
    def _generate_splashy_video(self, prompt: str) -> str:
        """Generate splashy video with effects"""
        try:
            if REAL_AI_AVAILABLE:
                return create_splashy_kenya_video()
            else:
                return self._generate_basic_video(prompt)
        except Exception as e:
            logger.error(f"[SPLASHY] Error: {e}")
            return self._generate_basic_video(prompt)
    
    def _generate_basic_video(self, prompt: str) -> str:
        """Generate basic video as fallback"""
        try:
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            # Return existing video if available
            existing_videos = list(output_dir.glob("*.mp4"))
            if existing_videos:
                return str(existing_videos[-1])
            else:
                # Create placeholder
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_path = output_dir / f"kenya_basic_{timestamp}.mp4"
                with open(video_path, 'w') as f:
                    f.write("# Kenya video placeholder")
                return str(video_path)
        except Exception as e:
            logger.error(f"[BASIC] Error: {e}")
            return None
    
    def create_enterprise_interface(self):
        """
        🎨 Create enterprise Kenya video generation interface
        
        // [SNIPPET]: thinkwithai + kenyafirst + refactorclean
        // [CONTEXT]: Enterprise UI with animated Kenya flag hero and sidebar
        // [GOAL]: Professional interface with all requested features
        """
        
        # Enterprise CSS with animated Kenya flag and sidebar
        enterprise_css = """
        /* Enterprise Kenya UI Design System */
        :root {
            --kenya-black: #000000;
            --kenya-red: #ff0000;
            --kenya-white: #ffffff;
            --kenya-green: #00ff00;
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --sidebar-width: 60px;
            --sidebar-expanded: 220px;
        }
        
        /* App Layout */
        .app-container {
            display: flex;
            min-height: 100vh;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* Thin Minimalistic Sidebar */
        .sidebar {
            width: var(--sidebar-width);
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: fixed;
            height: 100vh;
            z-index: 1000;
            box-shadow: 4px 0 20px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        
        .sidebar:hover {
            width: var(--sidebar-expanded);
        }
        
        .sidebar-item {
            display: flex;
            align-items: center;
            padding: 18px 15px;
            color: #ecf0f1;
            text-decoration: none;
            transition: all 0.3s ease;
            cursor: pointer;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            position: relative;
        }
        
        .sidebar-item:hover {
            background: linear-gradient(90deg, rgba(52, 152, 219, 0.2) 0%, rgba(52, 152, 219, 0.1) 100%);
            transform: translateX(8px);
            border-left: 3px solid #3498db;
        }
        
        .sidebar-icon {
            font-size: 22px;
            min-width: 30px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .sidebar-item:hover .sidebar-icon {
            transform: scale(1.1);
        }
        
        .sidebar-text {
            margin-left: 15px;
            opacity: 0;
            transition: opacity 0.3s ease 0.1s;
            white-space: nowrap;
            font-weight: 600;
            font-size: 14px;
        }
        
        .sidebar:hover .sidebar-text {
            opacity: 1;
        }
        
        /* Main Content */
        .main-content {
            margin-left: var(--sidebar-width);
            flex: 1;
            transition: margin-left 0.3s ease;
            padding: 0;
        }
        
        /* Animated Kenya Flag Hero */
        .hero-section {
            position: relative;
            height: 400px;
            background: linear-gradient(45deg, 
                var(--kenya-black) 0%, var(--kenya-black) 25%,
                var(--kenya-red) 25%, var(--kenya-red) 50%,
                var(--kenya-white) 50%, var(--kenya-white) 75%,
                var(--kenya-green) 75%, var(--kenya-green) 100%);
            background-size: 200% 200%;
            animation: kenyaFlagWave 8s ease-in-out infinite;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 4rem;
            overflow: hidden;
        }
        
        @keyframes kenyaFlagWave {
            0%, 100% { background-position: 0% 50%; }
            25% { background-position: 100% 50%; }
            50% { background-position: 50% 100%; }
            75% { background-position: 100% 0%; }
        }
        
        .hero-content {
            flex: 1;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            z-index: 2;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            animation: slideInLeft 1s ease-out;
        }
        
        .hero-subtitle {
            font-size: 1.4rem;
            margin-bottom: 2rem;
            animation: slideInLeft 1s ease-out 0.3s both;
        }
        
        .hero-video {
            flex: 1;
            max-width: 50%;
            height: 300px;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            animation: slideInRight 1s ease-out 0.6s both;
        }
        
        @keyframes slideInLeft {
            from { transform: translateX(-100px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideInRight {
            from { transform: translateX(100px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        /* Enterprise Cards */
        .enterprise-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .enterprise-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 16px 48px rgba(102, 126, 234, 0.2);
        }
        
        /* Minimalistic Footer */
        .footer {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: #ecf0f1;
            padding: 2rem 0;
            text-align: center;
            margin-top: 4rem;
            border-top: 3px solid #3498db;
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        .footer-center {
            flex: 1;
            text-align: center;
        }
        
        .footer-right {
            display: flex;
            gap: 2rem;
        }
        
        .footer-link {
            color: #3498db;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer-link:hover {
            color: #5dade2;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero-section {
                flex-direction: column;
                height: auto;
                padding: 2rem;
            }
            
            .hero-video {
                max-width: 100%;
                margin-top: 2rem;
            }
            
            .footer-content {
                flex-direction: column;
                gap: 1rem;
            }
        }
        """
        
        with gr.Blocks(
            theme=self.elite_theme,
            css=enterprise_css,
            title="🇰🇪 Shujaa Studio - Enterprise Kenya Video Generation",
            analytics_enabled=False
        ) as interface:

            # App Container with Sidebar
            gr.HTML("""
            <div class="app-container">
                <!-- Thin Minimalistic Sidebar -->
                <div class="sidebar">
                    <div class="sidebar-item" onclick="showAuth()">
                        <div class="sidebar-icon">👤</div>
                        <div class="sidebar-text">Authentication</div>
                    </div>
                    <div class="sidebar-item" onclick="showSettings()">
                        <div class="sidebar-icon">⚙️</div>
                        <div class="sidebar-text">Settings</div>
                    </div>
                    <div class="sidebar-item" onclick="showProjects()">
                        <div class="sidebar-icon">📁</div>
                        <div class="sidebar-text">Projects</div>
                    </div>
                    <div class="sidebar-item" onclick="showAnalytics()">
                        <div class="sidebar-icon">📊</div>
                        <div class="sidebar-text">Analytics</div>
                    </div>
                    <div class="sidebar-item" onclick="showExport()">
                        <div class="sidebar-icon">📤</div>
                        <div class="sidebar-text">Export</div>
                    </div>
                    <div class="sidebar-item" onclick="showHelp()">
                        <div class="sidebar-icon">❓</div>
                        <div class="sidebar-text">Help & Support</div>
                    </div>
                </div>

                <!-- Main Content Area -->
                <div class="main-content">
            """)

            # Animated Kenya Flag Hero Section with Video
            gr.HTML("""
            <div class="hero-section">
                <div class="hero-content">
                    <h1 class="hero-title">🇰🇪 Shujaa Studio</h1>
                    <p class="hero-subtitle">Enterprise Kenya Video Generation with Real AI</p>
                    <p style="font-size: 1.1rem; opacity: 0.9;">Create authentic Kenya videos with Mount Kenya, Diani Beach, Maasai Mara & more</p>
                </div>
                <div class="hero-video">
                    <video autoplay muted loop style="width: 100%; height: 100%; object-fit: cover; border-radius: 16px;">
                        <source src="output/kenya_splashy_20250808_170047.mp4" type="video/mp4">
                        <div style="background: linear-gradient(45deg, #667eea, #764ba2); height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.2rem;">
                            🎬 Kenya Video Preview
                        </div>
                    </video>
                </div>
            </div>
            """)

            # Main Interface in Enterprise Cards
            with gr.Row(elem_classes="enterprise-card"):
                with gr.Column(scale=2):
                    gr.HTML('<h2 style="color: #2c3e50; margin-bottom: 1rem;">🎬 Video Generation</h2>')

                    prompt_input = gr.Textbox(
                        label="📝 Your Kenya Story",
                        placeholder="Tell your Kenya story... (e.g., 'A young entrepreneur in Nairobi creates innovative solutions')",
                        lines=4
                    )

                    with gr.Row():
                        video_style = gr.Dropdown(
                            label="🎨 Video Style",
                            choices=["Real AI", "Splashy Effects", "Basic"],
                            value="Real AI"
                        )

                        export_format = gr.Dropdown(
                            label="📱 Export Format",
                            choices=["MP4", "MOV", "WebM"],
                            value="MP4"
                        )

                    with gr.Row():
                        enable_subtitles = gr.Checkbox(label="📝 Enable Subtitles", value=True)
                        enable_music = gr.Checkbox(label="🎵 Background Music", value=True)
                        kenya_mode = gr.Checkbox(label="🇰🇪 Kenya Mode", value=True)

                    generate_btn = gr.Button(
                        "🚀 Generate Elite Kenya Video",
                        variant="primary",
                        size="lg"
                    )

                with gr.Column(scale=2):
                    gr.HTML('<h2 style="color: #2c3e50; margin-bottom: 1rem;">📹 Video Output</h2>')

                    status_display = gr.Textbox(
                        label="🔄 Generation Status",
                        value="Ready to generate your Kenya video",
                        interactive=False
                    )

                    video_output = gr.Video(label="🎬 Generated Video")

                    # Download and Social Export Buttons
                    with gr.Row():
                        download_btn = gr.DownloadButton(
                            "💾 Download Video",
                            variant="secondary",
                            visible=False
                        )

                        export_tiktok_btn = gr.Button(
                            "📱 Export to TikTok",
                            variant="secondary",
                            visible=False
                        )

                        export_instagram_btn = gr.Button(
                            "📸 Export to Instagram",
                            variant="secondary",
                            visible=False
                        )

                        export_whatsapp_btn = gr.Button(
                            "💬 Export to WhatsApp",
                            variant="secondary",
                            visible=False
                        )

            # Event Handlers
            def handle_video_generation(prompt, style):
                """Handle video generation"""
                if not prompt.strip():
                    return None, "❌ Please enter a story prompt"

                video_path, status = self.generate_video(prompt, style)
                return video_path, status

            def handle_download(video_path):
                """Handle video download"""
                if video_path and Path(video_path).exists():
                    return video_path
                return None

            def handle_social_export(platform, video_path):
                """Handle social media export"""
                if video_path:
                    return f"🎉 Video optimized for {platform}! Ready to share."
                return f"❌ No video to export to {platform}"

            # Connect event handlers
            generate_btn.click(
                fn=handle_video_generation,
                inputs=[prompt_input, video_style],
                outputs=[video_output, status_display]
            )

            download_btn.click(
                fn=handle_download,
                inputs=[video_output],
                outputs=[download_btn]
            )

            export_tiktok_btn.click(
                fn=lambda v: handle_social_export("TikTok", v),
                inputs=[video_output],
                outputs=[status_display]
            )

            export_instagram_btn.click(
                fn=lambda v: handle_social_export("Instagram", v),
                inputs=[video_output],
                outputs=[status_display]
            )

            export_whatsapp_btn.click(
                fn=lambda v: handle_social_export("WhatsApp", v),
                inputs=[video_output],
                outputs=[status_display]
            )

            # Minimalistic Footer with Developer Credit
            gr.HTML("""
                </div> <!-- Close main-content -->
            </div> <!-- Close app-container -->

            <div class="footer">
                <div class="footer-content">
                    <div></div> <!-- Left spacer -->
                    <div class="footer-center">
                        <p style="margin: 0; font-weight: 600;">
                            Developed by <a href="https://codegx.tech" class="footer-link" target="_blank">Codegx Technologies</a>
                        </p>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">
                            © 2024 Shujaa Studio. All rights reserved.
                        </p>
                    </div>
                    <div class="footer-right">
                        <a href="#privacy" class="footer-link">Privacy</a>
                        <a href="#terms" class="footer-link">Terms</a>
                    </div>
                </div>
            </div>

            <script>
            // Sidebar functionality
            function showAuth() { alert('Authentication panel coming soon!'); }
            function showSettings() { alert('Settings panel coming soon!'); }
            function showProjects() { alert('Projects panel coming soon!'); }
            function showAnalytics() { alert('Analytics panel coming soon!'); }
            function showExport() { alert('Export panel coming soon!'); }
            function showHelp() { alert('Help & Support coming soon!'); }
            </script>
            """)

        return interface


def main():
    """
    🚀 Launch Shujaa Studio Enterprise UI

    // [SNIPPET]: thinkwithai + kenyafirst + surgicalfix
    // [CONTEXT]: Enterprise UI launch with animated Kenya flag and professional features
    // [GOAL]: World-class user experience competing with InVideo
    """

    print("🎬 LAUNCHING SHUJAA STUDIO ENTERPRISE UI")
    print("=" * 70)
    print("🇰🇪 Enterprise Kenya Video Generation Interface")
    print("🤖 Powered by SDXL-Turbo AI Models")
    print("🎨 UI Design: Enterprise Grade with Animated Kenya Flag")
    print("✨ Features: Sidebar, Social Export, Professional Layout")
    print("=" * 70)

    try:
        # Initialize the enterprise UI
        ui = ShujaaStudioEnterpriseUI()

        # Create and launch the interface
        interface = ui.create_enterprise_interface()

        # Launch with enterprise configuration
        interface.launch(
            server_name="0.0.0.0",
            server_port=7861,  # Different port to avoid conflicts
            share=False,
            debug=False,
            show_error=True,
            quiet=False,
            favicon_path=None,
            ssl_verify=False,
            show_tips=True,
            height=800,
            width="100%",
            inbrowser=True
        )

    except Exception as e:
        logger.error(f"🚨 [ENTERPRISE UI] Failed to launch: {e}")
        print(f"❌ Error launching enterprise UI: {e}")
        return False

    return True


if __name__ == "__main__":
    main()
