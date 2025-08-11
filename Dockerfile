# ============================================
# GPU-Optimized Image Processor
# With SAM + LaMa + Diffusers
# ============================================
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

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download models for offline readiness
RUN pip install huggingface_hub
RUN huggingface-cli download stabilityai/sdxl-turbo --local-dir /app/models/sdxl-turbo --local-dir-use-symlinks False
RUN huggingface-cli download runwayml/stable-diffusion-v1-5 --local-dir /app/models/stable-diffusion-v1-5 --local-dir-use-symlinks False
RUN huggingface-cli download suno/bark --local-dir /app/models/bark --local-dir-use-symlinks False
RUN huggingface-cli download openai/whisper-base --local-dir /app/models/whisper-base --local-dir-use-symlinks False

# Install torch with CUDA support
RUN pip install --upgrade pip setuptools wheel \
    && pip install --extra-index-url https://download.pytorch.org/whl/cu121 \
        tor