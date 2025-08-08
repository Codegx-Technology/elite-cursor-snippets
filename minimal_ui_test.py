#!/usr/bin/env python3
"""
Minimal UI test to debug Gradio issues
"""

print("🔍 Starting minimal UI test...")

try:
    import gradio as gr
    print("✅ Gradio imported successfully")
    
    def hello(name):
        return f"Hello {name}! Shujaa Studio is working!"
    
    print("🎬 Creating interface...")
    
    with gr.Blocks(title="Shujaa Studio Test") as demo:
        gr.Markdown("# 🇰🇪 Shujaa Studio - Minimal Test")
        
        with gr.Row():
            name_input = gr.Textbox(label="Enter your name", placeholder="Type here...")
            output = gr.Textbox(label="Output")
        
        btn = gr.Button("Test")
        btn.click(hello, inputs=name_input, outputs=output)
    
    print("🚀 Launching interface on port 7862...")
    demo.launch(
        server_port=7862,
        share=False,
        debug=True,
        show_error=True
    )
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
