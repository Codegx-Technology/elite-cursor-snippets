#!/usr/bin/env python3
"""
simple_ui.py
Minimal Gradio UI for Shujaa Studio
Following elite-cursor-snippets patterns for Kenya-specific requirements
"""

import gradio as gr
import requests
import time
import os
import yaml

# Load config
def load_config():
    try:
        with open("config.yaml", 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception:
        return {
            "api_host": "127.0.0.1",
            "api_port": 8000,
            "ui_port": 7860
        }

config = load_config()
API_BASE = f"http://{config.get('api_host', '127.0.0.1')}:{config.get('api_port', 8000)}"

def generate_video_ui(prompt, scenes, vertical, lang):
    """Generate video using local FastAPI"""
    try:
        payload = {
            "prompt": prompt,
            "scenes": scenes if scenes > 0 else None,
            "vertical": vertical,
            "lang": lang
        }
        
        response = requests.post(f"{API_BASE}/generate", json=payload, timeout=300)
        
        if response.status_code != 200:
            return f"❌ API Error: {response.text}"
        
        data = response.json()
        video_path = data.get("video_path")
        
        # Wait for file to exist
        attempts = 0
        while not os.path.exists(video_path) and attempts < 60:
            time.sleep(1)
            attempts += 1
        
        if os.path.exists(video_path):
            return video_path
        else:
            return "❌ Timeout waiting for video file"
            
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to API. Make sure the API server is running."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def test_api_connection():
    """Test API connection"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            return "✅ API connected successfully"
        else:
            return f"❌ API error: {response.text}"
    except Exception as e:
        return f"❌ Cannot connect to API: {str(e)}"

# Create interface
with gr.Blocks(title="🔥 Shujaa Studio - Local Script→Video") as demo:
    gr.Markdown("# 🔥 Shujaa Studio - Local Script→Video")
    
    # API Status
    with gr.Row():
        status_btn = gr.Button("🔧 Check API Status")
        status_text = gr.Textbox(label="API Status", value="Click to check API connection")
        status_btn.click(test_api_connection, outputs=status_text)
    
    # Input Section
    prompt_input = gr.Textbox(
        label="🎬 Your Story Prompt",
        placeholder="Tell a story in Sheng or Kiswahili...",
        lines=4
    )
    
    with gr.Row():
        scenes_input = gr.Slider(minimum=1, maximum=6, step=1, value=3, label="🎬 Scenes")
        vertical_input = gr.Checkbox(value=True, label="📱 Vertical (TikTok/Shorts)")
        lang_input = gr.Dropdown(choices=["sheng", "swahili", "english"], value="sheng", label="🌍 Language")
    
    generate_btn = gr.Button("🚀 Generate Video", variant="primary")
    
    # Output Section
    video_output = gr.Video(label="🎬 Your Created Video")
    status_output = gr.Textbox(label="🔄 Generation Status", lines=3)
    
    # Connect generate button
    generate_btn.click(
        fn=generate_video_ui,
        inputs=[prompt_input, scenes_input, vertical_input, lang_input],
        outputs=[video_output, status_output]
    )
    
    # Examples
    examples = [
        ["A young entrepreneur from Kibera builds a tech startup", 3, True, "sheng"],
        ["A Luo folktale about the clever hare", 3, True, "sheng"],
        ["Kenyan marathon champion training journey", 3, True, "sheng"]
    ]
    
    gr.Examples(examples=examples, inputs=[prompt_input, scenes_input, vertical_input, lang_input])

if __name__ == "__main__":
    print(f"🚀 Starting Shujaa Studio UI")
    print(f"🌐 UI URL: http://127.0.0.1:{config.get('ui_port', 7860)}")
    print(f"🔗 API URL: {API_BASE}")
    print(f"📖 Make sure the API server is running: python simple_api.py")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=config.get("ui_port", 7860),
        share=False
    )
