from huggingface_hub import InferenceClient
from PIL import Image
import io, os, time

MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
PROMPT = (
    "Mt Kenya at sunrise, dramatic lighting over the peaks and glaciers, "
    "lush highlands in the foreground, ultra-detailed, photorealistic, 8k, cinematic"
)
NEGATIVE = "low-res, blurry, artifacts, watermark, text"

client = InferenceClient(model=MODEL)

sizes = [
    (768, 768, "hf_mt_kenya_768_1.png"),
    (768, 768, "hf_mt_kenya_768_2.png"),
    (768, 768, "hf_mt_kenya_768_3.png"),
    (1024, 1024, "hf_mt_kenya_1024.png"),
]

for w, h, out_name in sizes:
    print(f"Requesting {w}x{h} -> {out_name}")
    img_bytes = client.text_to_image(
        prompt=PROMPT,
        negative_prompt=NEGATIVE,
        width=w,
        height=h,
        guidance_scale=7.5,
        num_inference_steps=30,
    )
    if isinstance(img_bytes, (bytes, bytearray)):
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    else:
        img = img_bytes
    img.save(out_name)
    print("Saved:", os.path.abspath(out_name))
    # small pause to avoid rate limits
    time.sleep(1)
