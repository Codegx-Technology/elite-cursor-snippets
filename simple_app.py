#!/usr/bin/env python3
"""
Shujaa Studio - Simple Web Interface
Basic version without video generation for now
"""

import os
import json
from pathlib import Path
from typing import Dict
import gradio as gr

class SimpleShujaaStudio:
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_script(self, prompt: str) -> Dict:
        """Generate script from prompt"""
        script = {
            "title": f"Story: {prompt}",
            "scenes": [
                {
                    "description": "Opening scene",
                    "narration": f"This is the story of {prompt}",
                    "duration": 3
                },
                {
                    "description": "Main scene", 
                    "narration": "The journey continues with amazing adventures",
                    "duration": 5
                },
                {
                    "description": "Closing scene",
                    "narration": "And so the story ends with hope and courage",
                    "duration": 3
                }
            ]
        }
        return script
    
    def process_prompt(self, prompt: str) -> str:
        """Process prompt and return script as text"""
        if not prompt.strip():
            return "Please enter a prompt"
        
        try:
            script = self.generate_script(prompt)
            
            # Format the script nicely
            result = f"🎬 **Shujaa Studio Script**\n\n"
            result += f"**Title:** {script['title']}\n\n"
            
            for i, scene in enumerate(script['scenes'], 1):
                result += f"**Scene {i}:**\n"
                result += f"- Description: {scene['description']}\n"
                result += f"- Narration: {scene['narration']}\n"
                result += f"- Duration: {scene['duration']} seconds\n\n"
            
            result += "✅ Script generated successfully!\n"
            result += "Next: Add voice, images, and video generation"
            
            return result
            
        except Exception as e:
            return f"❌ Error: {str(e)}"

def create_gradio_interface():
    """Create Gradio web interface"""
    studio = SimpleShujaaStudio()
    
    # Create interface
    iface = gr.Interface(
        fn=studio.process_prompt,
        inputs=[
            gr.Textbox(
                label="Enter your story prompt",
                placeholder="Tell a story of a girl from Kibera who becomes Kenya's youngest pilot...",
                lines=3
            )
        ],
        outputs=[
            gr.Markdown(label="Generated Script")
        ],
        title="🔥 Shujaa Studio - African AI Video Generator",
        description="Transform your stories into videos with AI (Basic Version)",
        theme=gr.themes.Soft(),
        examples=[
            ["A Luo folktale about the clever hare"],
            ["A girl from Kibera who becomes Kenya's youngest pilot"],
            ["A Sheng rap battle in Nairobi streets"],
            ["Traditional Kikuyu wedding ceremony"],
            ["Benga music festival in Kisumu"]
        ]
    )
    
    return iface

if __name__ == "__main__":
    iface = create_gradio_interface()
    print("🚀 Starting Shujaa Studio Web Interface...")
    print("📱 Open your browser to: http://localhost:7860")
    iface.launch(share=False, server_name="0.0.0.0", server_port=7860)
