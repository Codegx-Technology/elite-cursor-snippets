from __future__ import annotations
import io
import os
import typing as t
from PIL import Image
import numpy as np
import cv2
from logging_setup import get_logger
from config_loader import get_config, get_secret
from error_utils import retry_on_exception
from functools import lru_cache

# Elite Cursor Snippet: Imports for Watermark Removal
# ELITE_CURSOR_SNIPPET_START: watermark_removal_imports
try:
    from segment_anything import sam_model_registry, SamPredictor
except ImportError:
    sam_model_registry = None
    SamPredictor = None
    print("segment_anything not installed. SAM features will be unavailable.")

try:
    # Assuming lama_cleaner is installed and provides a LaMa model
    from lama_cleaner.model.lama import LaMa
    import torch
except ImportError:
    LaMa = None
    torch = None
    print("lama_cleaner or torch not installed. LaMa features will be unavailable.")

# ELITE_CURSOR_SNIPPET_END: watermark_removal_imports

logger = get_logger(__name__)
cfg = get_config()

def encode_image_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    """Encodes a PIL Image to bytes."""
    byte_arr = io.BytesIO()
    image.save(byte_arr, format=fmt)
    return byte_arr.getvalue()

def decode_image_bytes(image_bytes: bytes) -> Image.Image:
    """Decodes image bytes to a PIL Image."""
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")

@lru_cache(maxsize=1)
def load_sam_predictor():
    """Load SAM predictor."""
    if sam_model_registry is None or SamPredictor is None:
        raise ImportError("segment_anything is not installed.")
    try:
        model_type = cfg['sam_model_type']
        sam_checkpoint = cfg['sam_checkpoint_path']
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=cfg.get('device', 'cpu'))
        predictor = SamPredictor(sam)
        return predictor
    except Exception as e:
        logger.error(f"Failed to load SAM predictor: {e}")
        raise

@lru_cache(maxsize=1)
def load_lama():
    """
    Load LaMa inpainting model.
    Implementation depends on which library you pick.
    We'll assume `lama_cleaner` exposes `inpaint_image_pil(image, mask)`.
    """
    if LaMa is None or torch is None:
        raise ImportError("lama_cleaner or torch is not installed.")
    try:
        # Example: lama-cleaner provides LamaInpainting (this is illustrative)
        # from lama_cleaner import LaMaInpaint  # adjust to real import
        # impl = LaMaInpaint(model_path=cfg.get('lama_model_path'))
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        impl = LaMa(device=device) # Assuming LaMa class from lama_cleaner.model.lama
        return impl
    except Exception as e:
        logger.debug("LaMa load failed", exc_info=e)
        raise

@lru_cache(maxsize=1)
def load_sd_inpaint():
    """Load diffusers inpainting pipeline as fallback."""
    try:
        from diffusers import StableDiffusionInpaintPipeline
        import torch
        model_id = cfg['default_model_ids'].get('image_inpaint') or cfg['default_model_ids'].get('image')
        pipe = StableDiffusionInpaintPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe = pipe.to("cuda") if torch.cuda.is_available() else pipe.to("cpu")
        return pipe
    except Exception as e:
        logger.debug("SD Inpaint load failed", exc_info=e)
        raise

def detect_watermark_sam(image: Image.Image) -> np.ndarray:
    """
    Detects watermark using SAM.
    """
    predictor = load_sam_predictor()
    img_cv2 = np.array(image) # expects RGB numpy; predictor has set_image
    predictor.set_image(np.array(image.convert("RGB")))
    # Heuristic: sample likely watermark anchors - small white-ish regions at bottom/right
    H, W = img_cv2.shape[:2]
    # Provide prompt points: sample bottom-right area grid (improves detection for logos)
    points = []
    # sample a small grid across bottom & right edges
    for dx in (0.2, 0.5, 0.8):
        for dy in (0.2, 0.5, 0.8):
            px = int(W * dx)
            py = int(H * (0.88 if dy > 0.5 else 0.78))
            points.append([px, py])
    input_points = np.array(points)
    input_labels = np.ones(len(points))
    masks, scores, logits = predictor.predict(point_coords=input_points, point_labels=input_labels, multimask_output=True)
    # choose mask with highest mean score (heuristic)
    best_mask = masks[np.argmax([m.mean() for m in masks])]
    return (best_mask.astype(np.uint8) * 255)

def detect_watermark_heuristic(image: Image.Image) -> np.ndarray:
    """
    Simple heuristic detection for watermarks (e.g., based on color, position).
    This is a placeholder and can be improved.
    Returns a binary mask (255 for watermark, 0 otherwise).
    """
    # Example: detect white/light areas in the bottom right corner
    width, height = image.size
    mask = np.zeros((height, width), dtype=np.uint8)
    # Define a region of interest (e.g., bottom 20% of the image)
    roi_top = int(height * 0.8)
    roi_left = int(width * 0.7)
    
    img_np = np.array(image.convert("L")) # Convert to grayscale
    
    # Simple thresholding for light areas in ROI
    # You might need to adjust the threshold based on typical watermark appearance
    _, thresh = cv2.threshold(img_np[roi_top:, roi_left:], 200, 255, cv2.THRESH_BINARY)
    mask[roi_top:, roi_left:] = thresh
    
    return mask


@retry_on_exception(max_retries=2)
def inpaint_with_lama(image: Image.Image, mask: np.ndarray) -> Image.Image:
    """
    Inpaint image using LaMa. Assumes load_lama() returns an object with `inpaint_pil(image, mask_pil)`.
    """
    try:
        impl = load_lama()
        from PIL import Image
        mask_pil = Image.fromarray(mask).convert("L")
        # method depends on implementation; this is a common pattern
        # LaMa model expects numpy arrays, not PIL images for inpainting
        # The lama_cleaner library's LaMa model typically has a __call__ method
        # that takes image and mask as numpy arrays.
        # Convert PIL image to numpy array for LaMa
        image_np = np.array(image.convert("RGB"))
        result_np = impl(image_np, mask) # Assuming LaMa model's call method
        result = Image.fromarray(result_np)
        return result
    except Exception as e:
        logger.warning("LaMa inpaint failed", exc_info=e)
        raise

@retry_on_exception(max_retries=2)
def inpaint_with_sd(image: Image.Image, mask: np.ndarray, prompt: str = "") -> Image.Image:
    """
    Fallback using Stable Diffusion inpainting pipeline from diffusers.
    """
    try:
        pipe = load_sd_inpaint()
        # diffusers expects PIL image + mask (white = keep, black = inpaint? Check pipeline API)
        # Standard: image and mask_image (white pixels indicate masked regions)
        mask_pil = Image.fromarray(mask).convert("RGB")  # some pipes expect 3-channel
        # Make prompt guiding to neutral background / reconstruction
        # For inpainting, a simple prompt describing the background or desired fill is often used.
        # If no specific prompt is given, a generic one can be used.
        if not prompt:
            prompt = "a clean background, no text, no logos"
        
        # The pipeline expects a PIL image and a PIL mask
        result_image = pipe(prompt=prompt, image=image, mask_image=mask_pil).images[0]
        return result_image
    except Exception as e:
        logger.warning("SD inpaint failed", exc_info=e)
        raise

@retry_on_exception(max_retries=1)
def remove_watermark(
    image_bytes: bytes,
    preferred_backends: t.List[str] = ["sam+lama", "sd_inpaint", "heuristic"],
    hint_prompt: str = "",
    output_format: str = "PNG"
) -> bytes:
    """
    Removes watermarks from an image using a series of preferred backends.
    """
    image = decode_image_bytes(image_bytes)
    mask = None

    for backend in preferred_backends:
        logger.info(f"Attempting watermark removal with backend: {backend}")
        try:
            if backend == "sam+lama":
                if sam_model_registry is None or SamPredictor is None:
                    logger.warning("SAM not available, skipping sam+lama backend.")
                    continue
                if LaMa is None or torch is None:
                    logger.warning("LaMa not available, skipping sam+lama backend.")
                    continue
                try:
                    mask = detect_watermark_sam(image)
                except Exception as e:
                    logger.debug(f"SAM detection failed: {e}; trying next backend")
                    mask = None
                if mask is not None and mask.sum() > 0:
                    # call LaMa
                    try:
                        out_im = inpaint_with_lama(image, mask)
                        return encode_image_bytes(out_im, fmt=output_format)
                    except Exception as e:
                        logger.debug(f"LaMa failed: {e}; try SD inpaint next")
                        # continue to next backend
            elif backend == "sd_inpaint":
                # if mask not already computed, try heuristic detection to create mask
                if mask is None or mask.sum() == 0:
                    try:
                        mask = detect_watermark_heuristic(image)
                    except Exception as e:
                        logger.debug(f"Heuristic detection failed: {e}; mask remains None")
                        mask = None
                if mask is not None and mask.sum() > 0:
                    try:
                        out_im = inpaint_with_sd(image, mask, prompt=hint_prompt)
                        return encode_image_bytes(out_im, fmt=output_format)
                    except Exception as e:
                        logger.debug(f"SD inpaint failed: {e}; try next backend")
                        # continue to next backend
            elif backend == "heuristic":
                try:
                    mask = detect_watermark_heuristic(image)
                except Exception as e:
                    logger.debug(f"Heuristic detection failed: {e}; mask remains None")
                    mask = None
                if mask is not None and mask.sum() > 0:
                    # For heuristic, if no inpainting model is available,
                    # we might just return the original image or a cropped one.
                    # For now, we'll assume SD inpaint is the fallback for heuristic mask.
                    try:
                        out_im = inpaint_with_sd(image, mask, prompt=hint_prompt)
                        return encode_image_bytes(out_im, fmt=output_format)
                    except Exception as e:
                        logger.debug(f"SD inpaint failed for heuristic mask: {e}; trying next backend")
                        # continue to next backend
            else:
                logger.warning(f"Unknown watermark removal backend: {backend}")
        except Exception as e:
            logger.error(f"Error during watermark removal with backend {backend}: {e}", exc_info=True)
            # Continue to next backend if one fails
            
    logger.warning("All watermark removal backends failed or no watermark detected; returning original image")
    return image_bytes

# Async wrapper (for frameworks that support async)
async def remove_watermark_async(*args, **kwargs) -> bytes:
    # run sync function in threadpool to avoid blocking event loop
    import asyncio
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, remove_watermark, *args, **kwargs)