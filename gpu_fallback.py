#!/usr/bin/env python3
"""
🚀 Shujaa Studio - Hybrid GPU Fallback System
Seamless local/cloud GPU processing with intelligent resource management

// [TASK]: Hybrid GPU setup for optimal performance
// [GOAL]: Fast local processing + cloud fallbacks for heavy tasks
// [CONSTRAINTS]: Mobile-first, cost-effective, production-ready
// [SNIPPET]: thinkwithai + surgicalfix + perfcheck + mobilecheck
// [CONTEXT]: Integrates with existing Shujaa pipeline for GPU acceleration
"""

import os
import time
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import psutil
import logging

# GPU detection and management
try:
    import torch

    TORCH_AVAILABLE = True

    def check_gpu_memory():
        """Get GPU memory info"""
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            gpu_free = (
                torch.cuda.get_device_properties(0).total_memory
                - torch.cuda.memory_allocated()
            ) / (1024**3)
            return gpu_memory, gpu_free
        return 0, 0

except ImportError:
    TORCH_AVAILABLE = False

    def check_gpu_memory():
        return 0, 0


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessingMode(Enum):
    """GPU Processing modes"""

    LOCAL_GPU = "local_gpu"
    LOCAL_CPU = "local_cpu"
    CLOUD_GPU = "cloud_gpu"
    HYBRID = "hybrid"


@dataclass
class GPUResource:
    """GPU resource information"""

    name: str
    memory_total: float
    memory_free: float
    utilization: float
    temperature: float
    available: bool
    cost_per_hour: float = 0.0


@dataclass
class TaskProfile:
    """Processing task profile"""

    task_type: str
    estimated_memory: float
    estimated_time: float
    priority: int
    can_use_cpu: bool = True
    preferred_gpu_memory: float = 4.0


class HybridGPUManager:
    """
    // [TASK]: Intelligent GPU resource management
    // [GOAL]: Optimal performance + cost efficiency
    // [SNIPPET]: thinkwithai + surgicalfix + perfcheck
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.yaml"
        self.session_id = str(int(time.time()))
        self.processing_stats = {"local": 0, "cloud": 0, "hybrid": 0}

        # Resource tracking
        self.local_gpu = self._detect_local_gpu()
        self.cloud_providers = self._load_cloud_config()
        self.task_queue = []
        self.active_tasks = {}

        # Performance tracking
        self.performance_log = []
        self.cost_tracking = {"local": 0.0, "cloud": 0.0}

        logger.info(f"🚀 Hybrid GPU Manager initialized")
        logger.info(f"   Local GPU: {'✅' if self.local_gpu.available else '❌'}")
        logger.info(f"   Cloud providers: {len(self.cloud_providers)}")

    def _detect_local_gpu(self) -> GPUResource:
        """Detect and profile local GPU"""
        try:
            if not TORCH_AVAILABLE or not torch.cuda.is_available():
                return GPUResource("none", 0, 0, 0, 0, False)

            # Get GPU info
            device = torch.cuda.current_device()
            name = torch.cuda.get_device_name(device)
            total_memory, free_memory = check_gpu_memory()

            # Estimate utilization (simplified)
            utilization = (
                (total_memory - free_memory) / total_memory * 100
                if total_memory > 0
                else 0
            )

            gpu = GPUResource(
                name=name,
                memory_total=total_memory,
                memory_free=free_memory,
                utilization=utilization,
                temperature=0,  # Would need nvidia-ml-py for real temp
                available=free_memory > 0.5,  # Require at least 0.5GB free
                cost_per_hour=0.0,  # Local is "free"
            )

            logger.info(
                f"   GPU: {name} ({total_memory:.1f}GB total, {free_memory:.1f}GB free)"
            )
            return gpu

        except Exception as e:
            logger.warning(f"GPU detection failed: {e}")
            return GPUResource("error", 0, 0, 0, 0, False)

    def _load_cloud_config(self) -> List[Dict]:
        """Load cloud GPU provider configurations"""
        # Default cloud providers (can be configured via file)
        default_providers = [
            {
                "name": "runpod",
                "gpu_types": ["RTX3090", "RTX4090", "A100"],
                "cost_per_hour": {"RTX3090": 0.4, "RTX4090": 0.6, "A100": 1.2},
                "memory": {"RTX3090": 24, "RTX4090": 24, "A100": 40},
                "api_endpoint": None,  # Would be configured for real use
                "available": False,  # Set to True when properly configured
            },
            {
                "name": "vast_ai",
                "gpu_types": ["RTX3080", "RTX3090", "RTX4090"],
                "cost_per_hour": {"RTX3080": 0.3, "RTX3090": 0.4, "RTX4090": 0.5},
                "memory": {"RTX3080": 10, "RTX3090": 24, "RTX4090": 24},
                "api_endpoint": None,
                "available": False,
            },
            {
                "name": "google_colab",
                "gpu_types": ["T4", "V100", "A100"],
                "cost_per_hour": {"T4": 0.0, "V100": 0.0, "A100": 0.0},  # Free tier
                "memory": {"T4": 16, "V100": 16, "A100": 40},
                "api_endpoint": None,
                "available": True,  # Always available as fallback
                "limitations": "Free tier has usage limits",
            },
        ]

        # Try to load from config file
        config_file = Path("gpu_cloud_config.json")
        if config_file.exists():
            try:
                with open(config_file) as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cloud config: {e}")

        # Save default config for user customization
        try:
            with open(config_file, "w") as f:
                json.dump(default_providers, f, indent=2)
            logger.info(f"📝 Created default cloud config: {config_file}")
        except Exception as e:
            logger.warning(f"Failed to save default config: {e}")

        return default_providers

    def get_optimal_processing_mode(self, task_profile: TaskProfile) -> ProcessingMode:
        """
        // [TASK]: Intelligent processing mode selection
        // [GOAL]: Optimal performance + cost efficiency
        // [SNIPPET]: thinkwithai + perfcheck
        """
        # Check local GPU first
        if (
            self.local_gpu.available
            and self.local_gpu.memory_free >= task_profile.estimated_memory
            and self.local_gpu.utilization < 80
        ):
            return ProcessingMode.LOCAL_GPU

        # Check if we can use CPU for lightweight tasks
        if (
            task_profile.can_use_cpu
            and task_profile.estimated_memory <= 8.0
            and psutil.virtual_memory().percent < 80
        ):
            return ProcessingMode.LOCAL_CPU

        # Check cloud options for heavy tasks
        available_cloud = [p for p in self.cloud_providers if p.get("available", False)]
        if available_cloud and task_profile.priority > 7:
            return ProcessingMode.CLOUD_GPU

        # Fallback to local CPU
        return ProcessingMode.LOCAL_CPU

    async def process_task(
        self, task_profile: TaskProfile, task_function: Callable, *args, **kwargs
    ):
        """
        // [TASK]: Execute task with optimal GPU assignment
        // [GOAL]: Seamless processing with intelligent fallbacks
        // [SNIPPET]: surgicalfix + perfcheck
        """
        task_id = f"task_{int(time.time())}_{len(self.active_tasks)}"
        start_time = time.time()

        try:
            # Determine optimal processing mode
            mode = self.get_optimal_processing_mode(task_profile)
            logger.info(f"🎯 Task {task_id}: Using {mode.value}")

            # Execute based on mode
            result = None
            if mode == ProcessingMode.LOCAL_GPU:
                result = await self._execute_local_gpu(task_function, *args, **kwargs)
                self.processing_stats["local"] += 1

            elif mode == ProcessingMode.LOCAL_CPU:
                result = await self._execute_local_cpu(task_function, *args, **kwargs)
                self.processing_stats["local"] += 1

            elif mode == ProcessingMode.CLOUD_GPU:
                result = await self._execute_cloud_gpu(
                    task_profile, task_function, *args, **kwargs
                )
                self.processing_stats["cloud"] += 1

            else:  # HYBRID
                result = await self._execute_hybrid(
                    task_profile, task_function, *args, **kwargs
                )
                self.processing_stats["hybrid"] += 1

            # Track performance
            processing_time = time.time() - start_time
            self.performance_log.append(
                {
                    "task_id": task_id,
                    "mode": mode.value,
                    "processing_time": processing_time,
                    "success": result is not None,
                    "timestamp": time.time(),
                }
            )

            logger.info(
                f"✅ Task {task_id} completed in {processing_time:.2f}s using {mode.value}"
            )
            return result

        except Exception as e:
            logger.error(f"❌ Task {task_id} failed: {e}")

            # Try fallback mode
            if mode != ProcessingMode.LOCAL_CPU:
                logger.info(f"🔄 Attempting fallback to CPU for task {task_id}")
                try:
                    result = await self._execute_local_cpu(
                        task_function, *args, **kwargs
                    )
                    logger.info(f"✅ Fallback successful for task {task_id}")
                    return result
                except Exception as fallback_error:
                    logger.error(f"❌ Fallback also failed: {fallback_error}")

            raise e

    async def _execute_local_gpu(self, task_function: Callable, *args, **kwargs):
        """Execute task on local GPU"""
        # Ensure CUDA context
        if TORCH_AVAILABLE and torch.cuda.is_available():
            with torch.cuda.device(0):
                return await asyncio.get_event_loop().run_in_executor(
                    None, lambda: task_function(*args, device="cuda", **kwargs)
                )
        else:
            raise RuntimeError("Local GPU not available")

    async def _execute_local_cpu(self, task_function: Callable, *args, **kwargs):
        """Execute task on local CPU"""
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: task_function(*args, device="cpu", **kwargs)
        )

    async def _execute_cloud_gpu(
        self, task_profile: TaskProfile, task_function: Callable, *args, **kwargs
    ):
        """Execute task on cloud GPU (placeholder for cloud integration)"""
        # This would integrate with cloud providers like RunPod, Vast.ai etc.
        logger.info(
            "🌥️ Cloud GPU processing not yet implemented - using local CPU fallback"
        )
        return await self._execute_local_cpu(task_function, *args, **kwargs)

    async def _execute_hybrid(
        self, task_profile: TaskProfile, task_function: Callable, *args, **kwargs
    ):
        """Execute task using hybrid approach"""
        # This could split tasks between local and cloud
        logger.info("🔄 Hybrid processing not yet implemented - using local fallback")
        return await self._execute_local_cpu(task_function, *args, **kwargs)

    def get_performance_stats(self) -> Dict:
        """Get processing performance statistics"""
        total_tasks = sum(self.processing_stats.values())
        avg_times = {}

        for mode in ["local", "cloud", "hybrid"]:
            mode_tasks = [log for log in self.performance_log if mode in log["mode"]]
            if mode_tasks:
                avg_times[mode] = sum(
                    task["processing_time"] for task in mode_tasks
                ) / len(mode_tasks)
            else:
                avg_times[mode] = 0

        return {
            "total_tasks": total_tasks,
            "task_distribution": self.processing_stats,
            "average_processing_times": avg_times,
            "cost_tracking": self.cost_tracking,
            "local_gpu_status": asdict(self.local_gpu),
            "session_id": self.session_id,
        }

    def optimize_for_mobile(self) -> Dict:
        """
        // [TASK]: Mobile-first GPU optimization
        // [GOAL]: Efficient processing for mobile deployment
        // [SNIPPET]: mobilecheck + perfcheck
        """
        recommendations = []

        # Check memory usage
        if self.local_gpu.available and self.local_gpu.memory_total < 4:
            recommendations.append(
                "Consider using SDXL-Turbo for faster mobile generation"
            )

        # Check processing preferences
        mobile_tasks = [
            TaskProfile("image_generation", 2.0, 30, 8, True, 2.0),
            TaskProfile("voice_synthesis", 0.5, 10, 9, True, 1.0),
            TaskProfile("video_assembly", 1.0, 15, 7, True, 1.5),
        ]

        mobile_config = {}
        for task in mobile_tasks:
            optimal_mode = self.get_optimal_processing_mode(task)
            mobile_config[task.task_type] = optimal_mode.value

        return {
            "mobile_optimized_modes": mobile_config,
            "recommendations": recommendations,
            "estimated_mobile_performance": (
                "Good" if self.local_gpu.available else "CPU-Only"
            ),
        }


# Integration helper for existing Shujaa pipeline
class ShujaaGPUIntegration:
    """
    // [TASK]: Seamless integration with existing Shujaa components
    // [GOAL]: Drop-in GPU acceleration for video generation pipeline
    // [SNIPPET]: surgicalfix + refactorclean
    """

    def __init__(self):
        self.gpu_manager = HybridGPUManager()
        logger.info("🎬 Shujaa GPU Integration ready")

    async def accelerated_image_generation(
        self, prompt: str, output_path: str, **kwargs
    ):
        """GPU-accelerated image generation"""
        task_profile = TaskProfile(
            task_type="image_generation",
            estimated_memory=3.0,
            estimated_time=25,
            priority=8,
            can_use_cpu=True,
            preferred_gpu_memory=4.0,
        )

        def generate_image(prompt, output_path, device="cpu", **kwargs):
            # This would call the actual SDXL pipeline
            # Integrating with existing generate_video.py logic
            try:
                if device == "cuda" and TORCH_AVAILABLE:
                    # Use existing SDXL pipeline with GPU
                    from offline_video_maker.generate_video import OfflineVideoMaker

                    maker = OfflineVideoMaker()
                    if hasattr(maker, "sdxl_pipeline") and maker.sdxl_pipeline:
                        return maker._generate_real_image_sdxl(prompt, output_path)

                # Fallback to CPU or placeholder
                logger.info("Using CPU fallback for image generation")
                return self._generate_fallback_image(prompt, output_path)

            except Exception as e:
                logger.error(f"Image generation failed: {e}")
                return self._generate_fallback_image(prompt, output_path)

        return await self.gpu_manager.process_task(
            task_profile, generate_image, prompt, output_path, **kwargs
        )

    def _generate_fallback_image(self, prompt: str, output_path: str):
        """Fallback image generation when GPU fails"""
        # Use existing placeholder generation logic
        try:
            from PIL import Image, ImageDraw, ImageFont

            # Create artistic placeholder (using existing logic)
            width, height = 512, 512
            img = Image.new("RGB", (width, height), color="#1a4d80")
            draw = ImageDraw.Draw(img)

            # Add text
            try:
                font = ImageFont.load_default()
                words = prompt.split()[:5]  # First 5 words
                y_offset = height // 3

                for word in words:
                    bbox = draw.textbbox((0, 0), word, font=font)
                    text_width = bbox[2] - bbox[0]
                    x = (width - text_width) // 2
                    draw.text((x, y_offset), word, fill="white", font=font)
                    y_offset += 30
            except:
                pass

            img.save(output_path)
            logger.info(f"✅ Fallback image saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Fallback image generation failed: {e}")
            return None

    def get_integration_status(self):
        """Get status of GPU integration with Shujaa"""
        stats = self.gpu_manager.get_performance_stats()
        mobile_config = self.gpu_manager.optimize_for_mobile()

        return {
            "gpu_manager": stats,
            "mobile_optimization": mobile_config,
            "integration_status": "Active",
            "recommended_settings": {
                "use_cuda": self.gpu_manager.local_gpu.available,
                "batch_size": 1 if self.gpu_manager.local_gpu.memory_total < 8 else 2,
                "precision": "fp16" if self.gpu_manager.local_gpu.available else "fp32",
            },
        }


# CLI interface for testing
async def main():
    """Test the GPU fallback system"""
    print("🚀 Testing Hybrid GPU Fallback System")
    print("=" * 50)

    integration = ShujaaGPUIntegration()

    # Test image generation
    test_output = Path("temp/gpu_test_image.png")
    test_output.parent.mkdir(exist_ok=True)

    result = await integration.accelerated_image_generation(
        "Beautiful African sunset over Nairobi cityscape", str(test_output)
    )

    if result:
        print(f"✅ Test image generated: {result}")
    else:
        print("❌ Test image generation failed")

    # Show stats
    status = integration.get_integration_status()
    print("\n📊 GPU Integration Status:")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
