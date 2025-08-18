from huggingface_hub import InferenceClient
from PIL import Image
import io, os

# Uses token from environment/cache if available
MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
PROMPT = (
    "Mt Kenya at sunrise, dramatic lighting over the peaks and glaciers, "
    "lush highlands in the foreground, ultra-detailed, photorealistic, 8k, cinematic"
)
NEGATIVE = "low-res, blurry, artifacts, watermark, text"
OUT = "hf_mt_kenya.png"

client = InferenceClient(model=MODEL)

print(f"Requesting image from HF Inference API: {MODEL}")
img_bytes = client.text_to_image(
    prompt=PROMPT,
    negative_prompt=NEGATIVE,
    width=768,
    height=768,
    guidance_scale=7.5,
    num_inference_steps=30,
)

if isinstance(img_bytes, (bytes, bytearray)):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
else:
    # Newer clients may return PIL.Image directly
    img = img_bytes

img.save(OUT)
print("Saved:", os.path.abspath(OUT))
