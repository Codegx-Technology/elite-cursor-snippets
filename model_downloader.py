import argparse
import os
import logging
from pathlib import Path
from huggingface_hub import snapshot_download

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODELS_DIR = os.environ.get("MODELS_DIR", "./models")

DEFAULTS = {
    # SAM: use official or community repo name if available
    "sam": "facebook/sam-vit-base",
    # LaMa: use official or community repo name if available
    "lama": "saic-mdal/lama",
    # SD inpaint model (choose a smaller inpaint-capable model for speed)
    "sd_inpaint": "runwayml/stable-diffusion-inpainting",
}

def download(model_id, subdir=None):
    outdir = Path(MODELS_DIR) / (subdir or model_id.replace("/", "_"))
    outdir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Downloading {model_id} to {outdir} ...")
    snapshot_download(repo_id=model_id, cache_dir=str(outdir), local_files_only=False)
    logger.info("done")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--models", nargs="+", default=list(DEFAULTS.keys()))
    args = p.parse_args()
    for m in args.models:
        model_id = DEFAULTS.get(m, m)
        download(model_id, subdir=m)