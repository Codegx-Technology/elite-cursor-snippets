# GPU-Optimized Image Processor (SAM + LaMa + Diffusers + rembg + kornia)
# Note: Large image (~>5GB) due to models

FROM nvidia/cuda:12.1.105-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TORCH_CUDA_ARCH_LIST="8.6"  # Adjust for your GPU arch (8.6 = RTX 30xx)

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 python3.10-dev python3-pip git curl ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create app user
RUN useradd -m appuser

# Install torch with CUDA support (specific version for CUDA 12.1)
# This ensures compatibility and avoids issues with default pip installs
RUN pip3 install --extra-index-url https://download.pytorch.org/whl/cu121 \
    torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --no-deps

# Install ML & processing libs
RUN pip3 install --no-cache-dir \
    opencv-python-headless \
    pillow \
    numpy \
    scipy \
    tqdm \
    "transformers>=4.30.0" \
    "diffusers[torch]" \
    accelerate \
    safetensors \
    timm \
    kornia \
    rembg \
    uvicorn[standard] \
    fastapi \
    aiofiles \
    python-multipart \
    onnxruntime-gpu \
    git+https://github.com/facebookresearch/segment-anything.git@main \
    git+https://github.com/saic-mdal/lama.git@main \
    && pip3 cache purge

# Copy app code (assumes remove_watermark app & helpers exist)
COPY ./remove_watermark_app /app/remove_watermark_app
COPY ./model_downloader.py /app/model_downloader.py
RUN chown -R appuser:appuser /app

USER appuser
ENV PATH="/app:${PATH}"

# Pre-warm models (optional, executed at container start if MODEL_PREWARM=true)
# This is a placeholder. Actual pre-warming logic would be in the app startup.
CMD ["/bin/bash", "-c", "if [ \"$MODEL_PREWARM\" = \"true\" ]; then python3 model_downloader.py; fi && uvicorn remove_watermark_app.main:app --host 0.0.0.0 --port 8000"]
