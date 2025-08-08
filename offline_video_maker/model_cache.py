#!/usr/bin/env python3
"""
🔥 Shujaa Studio - Model Caching System
Elite-level model management for faster video generation

// [TASK]: Implement intelligent model caching and pre-loading
// [GOAL]: Reduce generation time by 60-80% through smart caching
// [CONSTRAINTS]: Memory-efficient, GPU-aware, fallback-ready
// [SNIPPET]: thinkwithai + refactorclean + surgicalfix
"""

import os
import json
import time
import psutil
import threading
from pathlib import Path
from typing import Dict, Optional, Any, List
import torch
import gc

class ModelCache:
    """
    // [TASK]: Intelligent model caching and memory management
    // [GOAL]: Pre-load models, manage GPU memory, optimize performance
    // [SNIPPET]: surgicalfix + refactorclean
    """
    
    def __init__(self):
        self.cache = {}
        self.load_times = {}
        self.usage_stats = {}
        self.max_memory_gb = self._get_available_memory()
        self.cache_dir = Path("models/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache configuration
        self.config = {
            "sdxl_priority": "high",
            "voice_priority": "medium", 
            "whisper_priority": "low",
            "preload_on_startup": True,
            "memory_threshold": 0.8  # 80% memory usage threshold
        }
        
        print(f"[CACHE] Model cache initialized - {self.max_memory_gb:.1f}GB available")
    
    def _get_available_memory(self) -> float:
        """Get available system memory in GB"""
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            return min(gpu_memory * 0.7, psutil.virtual_memory().available / (1024**3))
        return psutil.virtual_memory().available / (1024**3)
    
    def preload_models(self, models_to_load: List[str] = None):
        """
        // [TASK]: Pre-load commonly used models
        // [GOAL]: Reduce first-generation latency
        // [SNIPPET]: thinkwithai + surgicalfix
        """
        if models_to_load is None:
            models_to_load = ["sdxl", "whisper-small", "bark"]
        
        print("[CACHE] Pre-loading models for faster generation...")
        
        for model_name in models_to_load:
            try:
                start_time = time.time()
                
                if model_name == "sdxl" and self._should_load_model("sdxl"):
                    self._load_sdxl_model()
                elif model_name.startswith("whisper") and self._should_load_model("whisper"):
                    self._load_whisper_model(model_name.split("-")[1] if "-" in model_name else "small")
                elif model_name == "bark" and self._should_load_model("bark"):
                    self._load_bark_model()
                
                load_time = time.time() - start_time
                self.load_times[model_name] = load_time
                print(f"[CACHE] ✅ {model_name} loaded in {load_time:.1f}s")
                
            except Exception as e:
                print(f"[CACHE] ⚠️ Failed to preload {model_name}: {e}")
    
    def _should_load_model(self, model_type: str) -> bool:
        """Check if model should be loaded based on memory and priority"""
        current_memory = psutil.virtual_memory().percent / 100
        
        if current_memory > self.config["memory_threshold"]:
            print(f"[CACHE] Memory usage too high ({current_memory:.1%}), skipping {model_type}")
            return False
        
        priority = self.config.get(f"{model_type}_priority", "medium")
        if priority == "high":
            return True
        elif priority == "medium" and current_memory < 0.6:
            return True
        elif priority == "low" and current_memory < 0.4:
            return True
        
        return False
    
    def _load_sdxl_model(self):
        """Load SDXL model into cache"""
        try:
            from diffusers import StableDiffusionXLPipeline
            
            if "sdxl" not in self.cache:
                pipeline = StableDiffusionXLPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-xl-base-1.0",
                    torch_dtype=torch.float16,
                    use_safetensors=True
                )
                
                if torch.cuda.is_available():
                    pipeline = pipeline.to("cuda")
                    pipeline.enable_memory_efficient_attention()
                    pipeline.enable_xformers_memory_efficient_attention()
                
                self.cache["sdxl"] = pipeline
                self.usage_stats["sdxl"] = {"loads": 0, "generations": 0}
                
        except Exception as e:
            print(f"[CACHE] SDXL load failed: {e}")
    
    def _load_whisper_model(self, size: str = "small"):
        """Load Whisper model into cache"""
        try:
            import whisper
            
            model_key = f"whisper-{size}"
            if model_key not in self.cache:
                model = whisper.load_model(size)
                self.cache[model_key] = model
                self.usage_stats[model_key] = {"loads": 0, "transcriptions": 0}
                
        except Exception as e:
            print(f"[CACHE] Whisper load failed: {e}")
    
    def _load_bark_model(self):
        """Load Bark model into cache"""
        try:
            # Bark model loading would go here
            # This is a placeholder for when Bark is properly integrated
            self.cache["bark"] = "bark_model_placeholder"
            self.usage_stats["bark"] = {"loads": 0, "generations": 0}
            
        except Exception as e:
            print(f"[CACHE] Bark load failed: {e}")
    
    def get_model(self, model_name: str) -> Optional[Any]:
        """
        // [TASK]: Retrieve cached model or load on demand
        // [GOAL]: Provide fast model access with fallback loading
        // [SNIPPET]: surgicalfix
        """
        if model_name in self.cache:
            self.usage_stats[model_name]["loads"] += 1
            return self.cache[model_name]
        
        # Load on demand if not cached
        print(f"[CACHE] Loading {model_name} on demand...")
        
        if model_name == "sdxl":
            self._load_sdxl_model()
        elif model_name.startswith("whisper"):
            size = model_name.split("-")[1] if "-" in model_name else "small"
            self._load_whisper_model(size)
        elif model_name == "bark":
            self._load_bark_model()
        
        return self.cache.get(model_name)
    
    def clear_cache(self, model_name: str = None):
        """Clear specific model or entire cache"""
        if model_name:
            if model_name in self.cache:
                del self.cache[model_name]
                print(f"[CACHE] Cleared {model_name}")
        else:
            self.cache.clear()
            print("[CACHE] Cleared all cached models")
        
        # Force garbage collection
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def get_cache_stats(self) -> Dict:
        """Get cache performance statistics"""
        stats = {
            "cached_models": list(self.cache.keys()),
            "memory_usage_gb": self._get_memory_usage(),
            "load_times": self.load_times,
            "usage_stats": self.usage_stats,
            "cache_hits": sum(stats.get("loads", 0) for stats in self.usage_stats.values())
        }
        return stats
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in GB"""
        if torch.cuda.is_available():
            return torch.cuda.memory_allocated() / (1024**3)
        return psutil.Process().memory_info().rss / (1024**3)

# Global cache instance
model_cache = ModelCache()

def initialize_cache():
    """Initialize model cache on startup"""
    if model_cache.config["preload_on_startup"]:
        threading.Thread(target=model_cache.preload_models, daemon=True).start()

if __name__ == "__main__":
    # Test cache functionality
    initialize_cache()
    time.sleep(2)  # Let preloading start
    print("\n📊 Cache Stats:")
    stats = model_cache.get_cache_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
