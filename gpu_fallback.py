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
    performance_score: float = 0.0


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
    // [TASK]: Intelligent, cost-aware GPU resource management
    // [GOAL]: Optimal performance, cost efficiency, and intelligent routing
    // [SNIPPET]: thinkwithai + surgicalfix + perfcheck + costaware
    """

    def __init__(self, config_path: Optional[str] = None, cost_optimization_strategy: str = "balanced"):
        self.config_path = config_path or "config.yaml"
        self.session_id = str(int(time.time()))
        self.processing_stats = {"local_gpu": 0, "local_cpu": 0, "cloud_gpu": 0}
        self.cost_optimization_strategy = cost_optimization_strategy # new attribute

        self.local_gpu = self._detect_local_gpu()
        self.cloud_providers = self._load_cloud_config()
        self.task_queue = []
        self.active_tasks = {}

        self.performance_log = []
        self.cost_tracking = {"total_cost": 0.0}

        logger.info(f"🚀 Hybrid GPU Manager initialized")
        logger.info(f"   Local GPU: {self.local_gpu.name if self.local_gpu.available else '❌'}")
        logger.info(f"   Cloud providers: {len(self.cloud_providers)}")

    def _detect_local_gpu(self) -> GPUResource:
        try:
            if not TORCH_AVAILABLE or not torch.cuda.is_available():
                return GPUResource("none", 0, 0, 0, 0, False)
            device = torch.cuda.current_device()
            name = torch.cuda.get_device_name(device)
            total_memory, free_memory = check_gpu_memory()
            utilization = ((total_memory - free_memory) / total_memory * 100) if total_memory > 0 else 0
            # Assign a conceptual performance score based on memory and utilization
            # In a real system, this would be based on benchmarks or historical data
            performance_score = (free_memory / total_memory) * (100 - utilization) # Higher is better
            
            gpu = GPUResource(
                name=name, memory_total=total_memory, memory_free=free_memory,
                utilization=utilization, temperature=0, available=free_memory > 0.5,
                cost_per_hour=config.get('local_gpu_cost_per_hour', 0.0),
                performance_score=performance_score # ADD THIS
            )
            logger.info(f"   GPU: {name} ({total_memory:.1f}GB total, {free_memory:.1f}GB free, Score: {performance_score:.2f})")
            return gpu
        except Exception as e:
            logger.warning(f"GPU detection failed: {e}")
            return GPUResource("error", 0, 0, 0, 0, False)

    def _load_cloud_config(self) -> List[Dict]:
        config_file = Path("gpu_cloud_config.json")
        if config_file.exists():
            try:
                with open(config_file) as f:
                    cloud_config = json.load(f)
                    # Add conceptual performance score to loaded cloud providers
                    for provider in cloud_config:
                        for gpu_type, specs in provider.get("gpus", {}).items():
                            # Simple score based on memory, higher memory = higher score
                            specs["performance_score"] = specs["memory"] * 10 # Example
                    return cloud_config
            except Exception as e:
                logger.warning(f"Failed to load cloud config: {e}")
        default_providers = [
            {
                "name": "runpod", "available": False,
                "gpus": {
                    "RTX4090": {"memory": 24, "cost_per_hour": 0.79, "performance_score": 240},
                    "A100": {"memory": 80, "cost_per_hour": 2.19, "performance_score": 800}
                }
            }
        ]
        try:
            with open(config_file, "w") as f:
                json.dump(default_providers, f, indent=2)
            logger.info(f"📝 Created default cloud config: {config_file}")
        except Exception as e:
            logger.warning(f"Failed to save default config: {e}")
        return default_providers

    def select_best_resource(self, task_profile: TaskProfile) -> Dict:
        """
        Selects the best available resource (local or cloud) based on task requirements and cost.
        """
        best_resource = sorted(eligible_resources, key=lambda x: x["cost"])[0]
        logger.info(f"🎯 Selected best resource: {best_resource['name']} from {best_resource['provider']} at ${best_resource['cost']:.2f}/hr")
        return best_resource

    def _get_eligible_resources(self, task_profile: TaskProfile) -> List[Dict]:
        eligible_resources = []
        if self.local_gpu.available and self.local_gpu.memory_free >= task_profile.estimated_memory:
            eligible_resources.append({
                "name": self.local_gpu.name, "mode": ProcessingMode.LOCAL_GPU,
                "cost": self.local_gpu.cost_per_hour, "provider": "local",
                "performance_score": self.local_gpu.performance_score
            })

        for provider in self.cloud_providers:
            if not provider.get("available", False):
                continue
            for gpu_type, specs in provider.get("gpus", {}).items():
                if specs["memory"] >= task_profile.estimated_memory:
                    eligible_resources.append({
                        "name": gpu_type, "mode": ProcessingMode.CLOUD_GPU,
                        "cost": specs["cost_per_hour"], "provider": provider["name"],
                        "performance_score": specs["performance_score"]
                    })
        return eligible_resources

    def select_best_resource(self, task_profile: TaskProfile) -> Dict:
        """
        Selects the best available resource (local or cloud) based on task requirements and cost.
        """
        eligible_resources = self._get_eligible_resources(task_profile)

        if not eligible_resources:
            if task_profile.can_use_cpu:
                logger.info("No suitable GPU found, falling back to Local CPU.")
                return {"name": "cpu", "mode": ProcessingMode.LOCAL_CPU, "cost": 0, "provider": "local", "performance_score": 0} # Add performance_score
            else:
                raise RuntimeError(f"No resource found that meets memory requirement of {task_profile.estimated_memory}GB")

        if self.cost_optimization_strategy == "low_cost":
            # Prioritize CPU if possible and cost is paramount
            if task_profile.can_use_cpu:
                return {"name": "cpu", "mode": ProcessingMode.LOCAL_CPU, "cost": 0, "provider": "local", "performance_score": 0} # Add performance_score
            best_resource = sorted(eligible_resources, key=lambda x: x["cost"])[0]
        elif self.cost_optimization_strategy == "balanced":
            # Balance between cost and performance (e.g., prefer local GPU if available)
            local_gpu_option = next((r for r in eligible_resources if r["mode"] == ProcessingMode.LOCAL_GPU), None)
            if local_gpu_option:
                best_resource = local_gpu_option
            else:
                best_resource = sorted(eligible_resources, key=lambda x: x["cost"])[0]
        elif self.cost_optimization_strategy == "high_performance":
            # Prioritize highest performance score
            best_resource = sorted(eligible_resources, key=lambda x: x["performance_score"], reverse=True)[0] # Sort by performance_score
        else:
            best_resource = sorted(eligible_resources, key=lambda x: x["cost"])[0]

        logger.info(f"🎯 Selected best resource: {best_resource['name']} from {best_resource['provider']} at ${best_resource['cost']:.2f}/hr (Strategy: {self.cost_optimization_strategy}, Performance Score: {best_resource.get('performance_score', 'N/A')})")
        return best_resource

    async def process_task(self, task_profile: TaskProfile, task_function: Callable, *args, **kwargs):
        task_id = f"task_{int(time.time())}_{len(self.active_tasks)}"
        start_time = time.time()

        try:
            selected_resource = self.select_best_resource(task_profile)
            mode = selected_resource["mode"]
            
            result = None
            if mode == ProcessingMode.LOCAL_GPU:
                result = await self._execute_local_gpu(task_function, *args, **kwargs)
            elif mode == ProcessingMode.LOCAL_CPU:
                result = await self._execute_local_cpu(task_function, *args, **kwargs)
            elif mode == ProcessingMode.CLOUD_GPU:
                result = await self._execute_cloud_gpu(task_profile, task_function, selected_resource, *args, **kwargs)

            processing_time_sec = time.time() - start_time
            task_cost = selected_resource["cost"] * (processing_time_sec / 3600)
            provider = selected_resource["provider"]
            
            self.cost_tracking[provider] = self.cost_tracking.get(provider, 0.0) + task_cost
            self.cost_tracking["total_cost"] += task_cost
            self.processing_stats[mode.value] += 1

            self.performance_log.append({
                "task_id": task_id, "mode": mode.value, "provider": provider,
                "resource": selected_resource['name'], "processing_time": processing_time_sec,
                "cost": task_cost, "success": result is not None, "timestamp": time.time(),
            })

            logger.info(f"✅ Task {task_id} ({task_profile.task_type}) completed in {processing_time_sec:.2f}s on {provider}:{selected_resource['name']} (Cost: ${task_cost:.4f})")
            return result

        except Exception as e:
            logger.error(f"❌ Task {task_id} failed: {e}")
            if task_profile.can_use_cpu:
                logger.info(f"🔄 Attempting fallback to CPU for task {task_id}")
                try:
                    return await self._execute_local_cpu(task_function, *args, **kwargs)
                except Exception as fallback_error:
                    logger.error(f"❌ Fallback also failed: {fallback_error}")
            raise e

    async def _execute_local_gpu(self, task_function: Callable, *args, **kwargs):
        if not (TORCH_AVAILABLE and torch.cuda.is_available()):
            raise RuntimeError("Local GPU not available")
        with torch.cuda.device(0):
            return await asyncio.get_event_loop().run_in_executor(None, lambda: task_function(*args, device="cuda", **kwargs))

    async def _execute_local_cpu(self, task_function: Callable, *args, **kwargs):
        return await asyncio.get_event_loop().run_in_executor(None, lambda: task_function(*args, device="cpu", **kwargs))

    async def _execute_cloud_gpu(self, task_profile: TaskProfile, task_function: Callable, resource: Dict, *args, **kwargs):
        logger.info(f"🌥️  Executing task on cloud provider: {resource['provider']} (GPU: {resource['name']})")
        # Placeholder for actual cloud API integration
        logger.warning("Cloud GPU processing not yet implemented - using local CPU as simulation fallback.")
        return await self._execute_local_cpu(task_function, *args, **kwargs)

    def get_performance_stats(self) -> Dict:
        total_tasks = sum(self.processing_stats.values())
        return {
            "total_tasks": total_tasks,
            "task_distribution": self.processing_stats,
            "cost_tracking": self.cost_tracking,
            "local_gpu_status": asdict(self.local_gpu),
            "session_id": self.session_id,
            "performance_log": self.performance_log
        }

    def update_cloud_costs(self, new_cloud_config: List[Dict]):
        # // [TASK]: Dynamically update cloud provider costs
        # // [GOAL]: Allow real-time cost adjustments for cloud resources
        # // [ELITE_CURSOR_SNIPPET]: costaware
        logger.info("Updating cloud provider costs dynamically.")
        self.cloud_providers = new_cloud_config

    def optimize_for_mobile(self) -> Dict:
        # This method remains conceptually the same but now benefits from the new resource selector
        recommendations = []
        if self.local_gpu.available and self.local_gpu.memory_total < 4:
            recommendations.append("Local GPU memory is low. Consider cloud GPUs for larger models.")
        
        mobile_tasks = [
            TaskProfile("image_generation", 2.0, 30, 8, True, 2.0),
            TaskProfile("voice_synthesis", 0.5, 10, 9, True, 1.0),
        ]
        mobile_config = {}
        for task in mobile_tasks:
            try:
                best_resource = self.select_best_resource(task)
                mobile_config[task.task_type] = f"{best_resource['provider']}:{best_resource['name']}"
            except RuntimeError as e:
                mobile_config[task.task_type] = f"No resource available ({e})"

        return {
            "mobile_optimized_modes": mobile_config,
            "recommendations": recommendations,
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
