#!/usr/bin/env python3
"""
// [TASK]: Detect GPU availability and set a flag
// [GOAL]: Create a reusable module for GPU detection
// [SNIPPET]: thinkwithai + refactorclean
"""

import torch

def is_gpu_available():
    """
    // [TASK]: Check for NVIDIA GPU with CUDA support
    // [GOAL]: Return True if GPU is available, False otherwise
    """
    try:
        return torch.cuda.is_available()
    except Exception as e:
        print(f"[ERROR] PyTorch not found or CUDA not available: {e}")
        return False

def get_device():
    """
    // [TASK]: Get the appropriate device (GPU or CPU)
    // [GOAL]: Return 'cuda' if GPU is available, 'cpu' otherwise
    """
    return "cuda" if is_gpu_available() else "cpu"

if __name__ == "__main__":
    if is_gpu_available():
        print("✅ GPU is available.")
        print(f"Device: {get_device()}")
    else:
        print("❌ GPU not available, falling back to CPU.")
        print(f"Device: {get_device()}")
