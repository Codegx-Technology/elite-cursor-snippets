#!/usr/bin/env python3
"""
🔥 Shujaa Studio - Parallel Processing Engine
Elite-level concurrent processing for accelerated AI workflows.

// [TASK]: Generalize and refactor the parallel processing engine.
// [GOAL]: Create a reusable utility for running any async worker function concurrently.
// [CONSTRAINTS]: GPU memory management, thread-safety, non-blocking execution.
"""

import os
import asyncio
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional, Callable, Any, Awaitable
import time
import psutil
from pathlib import Path

import logging
from ai_model_manager import generate_text, generate_image, text_to_speech, speech_to_text

# Use standard logging to avoid circular import with logging_setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ParallelProcessor:
    """
    A generalized parallel processing engine to run a worker function
    concurrently across a list of items, with intelligent batching
    and performance tracking.
    """
    
    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers or min(4, mp.cpu_count())
        self.gpu_available = self._check_gpu_availability()
        self.memory_threshold = 0.85  # 85% memory usage threshold
        
        self.processing_stats = {
            "items_processed": 0,
            "total_time": 0,
            "average_time_per_item": 0,
        }
        
        logger.info(f"[PARALLEL] Initialized with {self.max_workers} workers. GPU available: {self.gpu_available}")
    
    def _check_gpu_availability(self) -> bool:
        try:
            import torch
            return torch.cuda.is_available() and torch.cuda.device_count() > 0
        except ImportError:
            return False
    
    def _check_memory_usage(self) -> float:
        return psutil.virtual_memory().percent / 100
    
    async def run_parallel(self, items: List[Any], worker_function: Callable[[Any], Awaitable[Any]]) -> List[Any]:
        """
        Processes a list of items in parallel using the provided async worker_function.
        """
        if not items:
            return []
            
        start_time = time.time()
        logger.info(f"[PARALLEL] Processing {len(items)} items concurrently...")
        
        batch_size = self._calculate_optimal_batch_size(len(items))
        logger.info(f"[PARALLEL] Using optimal batch size: {batch_size}")
        
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            logger.info(f"[PARALLEL] Processing batch {i//batch_size + 1}/{(len(items) + batch_size - 1)//batch_size}...")
            batch_results = await self._process_batch(batch, worker_function)
            results.extend(batch_results)
            
            if i + batch_size < len(items):
                await self._cleanup_memory()
        
        total_time = time.time() - start_time
        self._update_processing_stats(len(items), total_time)
        
        logger.info(f"[PARALLEL] ✅ Completed {len(items)} items in {total_time:.2f}s")
        
        return results
    
    def _calculate_optimal_batch_size(self, total_items: int) -> int:
        memory_usage = self._check_memory_usage()
        if memory_usage > 0.7:
            batch_size = min(2, total_items)
        elif memory_usage > 0.5:
            batch_size = min(3, total_items)
        else:
            batch_size = min(self.max_workers, total_items)
        return max(1, batch_size) # Ensure batch size is at least 1
    
    async def _process_batch(self, batch: List[Any], worker_function: Callable) -> List[Any]:
        tasks = [asyncio.create_task(worker_function(item)) for item in batch]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning(f"[PARALLEL] ⚠️ Item {i} in batch failed: {result}")
                processed_results.append({"status": "failed", "error": str(result), "item_data": batch[i]})
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _cleanup_memory(self):
        import gc
        gc.collect()
        if self.gpu_available:
            try:
                import torch
                torch.cuda.empty_cache()
            except (ImportError, AttributeError):
                pass
        await asyncio.sleep(0.5)
    
    def _update_processing_stats(self, items_count: int, total_time: float):
        self.processing_stats["items_processed"] += items_count
        self.processing_stats["total_time"] += total_time
        if self.processing_stats["items_processed"] > 0:
            self.processing_stats["average_time_per_item"] = (
                self.processing_stats["total_time"] /
                self.processing_stats["items_processed"]
            )
    
    def get_processing_stats(self) -> Dict:
        return {
            **self.processing_stats,
            "memory_usage": f"{self._check_memory_usage():.1%}",
            "max_workers": self.max_workers,
            "gpu_available": self.gpu_available
        }

class SceneProcessor:
    """
    A concrete implementation of processing functions for a video scene.
    This can be used to build a worker function for the ParallelProcessor.
    """
    
    def __init__(self, temp_dir: str = "temp/parallel", enhanced_router: Any = None, dialect: Optional[str] = None): # ADD enhanced_router, dialect
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.enhanced_router = enhanced_router # Store router instance
        self.dialect = dialect # Store dialect
        logger.info(f"SceneProcessor initialized. Temp directory: {self.temp_dir}")
    
    async def process_voice(self, scene_text: str, scene_id: Any) -> str:
        voice_file_path = self.temp_dir / f"scene_{scene_id}_voice.wav"
        try:
            if not self.enhanced_router:
                raise ValueError("Enhanced router not provided to SceneProcessor.")
            
            request = GenerationRequest(
                prompt=scene_text,
                type="audio",
                dialect=self.dialect
            )
            
            result = await self.enhanced_router.route_generation(request)
            
            if result.success and result.result: # Assuming result.result contains the audio bytes or path
                # If result.result is bytes, save it. If it's a path, copy it.
                if isinstance(result.result, bytes):
                    audio_bytes = result.result
                    with open(voice_file_path, "wb") as f:
                        f.write(audio_bytes)
                elif os.path.exists(result.result): # Assuming it's a path to a temp file
                    import shutil
                    shutil.copy(result.result, voice_file_path)
                else:
                    raise ValueError(f"Unexpected result format from router for audio: {result.result}")

                logger.info(f"Generated voice for scene {scene_id}: {voice_file_path}")
                return str(voice_file_path)
            else:
                raise ValueError(f"Failed to generate voice for scene {scene_id} via router: {result.error_message}")
        except Exception as e:
            logger.error(f"Failed to generate voice for scene {scene_id}: {e}")
            raise
    
    async def process_image(self, image_prompt: str, scene_id: Any) -> str:
        image_file_path = self.temp_dir / f"scene_{scene_id}_image.png"
        try:
            if not self.enhanced_router:
                raise ValueError("Enhanced router not provided to SceneProcessor.")
            
            request = GenerationRequest(
                prompt=image_prompt,
                type="image",
                dialect=self.dialect
            )
            
            result = await self.enhanced_router.route_generation(request)
            
            if result.success and result.result: # Assuming result.result contains the image bytes or path
                if isinstance(result.result, bytes):
                    image_bytes = result.result
                    with open(image_file_path, "wb") as f:
                        f.write(image_bytes)
                elif os.path.exists(result.result): # Assuming it's a path to a temp file
                    import shutil
                    shutil.copy(result.result, image_file_path)
                else:
                    raise ValueError(f"Unexpected result format from router for image: {result.result}")

                logger.info(f"Generated image for scene {scene_id}: {image_file_path}")
                return str(image_file_path)
            else:
                raise ValueError(f"Failed to generate image for scene {scene_id} via router: {result.error_message}")
        except Exception as e:
            logger.error(f"Failed to generate image for scene {scene_id}: {e}")
            raise
    
    def process_video_compilation(self, image_path: str, audio_path: str, scene_id: Any) -> str:
        video_file_path = self.temp_dir / f"scene_{scene_id}_video.mp4"
        logger.info(f"Compiling video for scene {scene_id}...")
        # This is a placeholder for actual video creation (e.g., using moviepy or ffmpeg)
        # In a real implementation, this would be an async subprocess call.
        try:
            # Example with ffmpeg (requires ffmpeg to be installed)
            import subprocess
            command = [
                'ffmpeg',
                '-y', # Overwrite output file if it exists
                '-loop', '1',
                '-i', image_path,
                '-i', audio_path,
                '-c:v', 'libx264',
                '-tune', 'stillimage',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-shortest',
                str(video_file_path)
            ]
            subprocess.run(command, check=True, capture_output=True)
            logger.info(f"Generated video for scene {scene_id}: {video_file_path}")
            return str(video_file_path)
        except FileNotFoundError:
            logger.warning("ffmpeg not found. Creating placeholder video file.")
            video_file_path.touch()
            return str(video_file_path)
        except Exception as e:
            logger.error(f"Failed to compile video for scene {scene_id}: {e}")
            raise

# Example usage
async def main():
    logger.info("--- Testing ParallelProcessor Engine ---")
    
    parallel_processor = ParallelProcessor(max_workers=2)
    scene_processor = SceneProcessor(temp_dir="temp/parallel_test")
    
    scenes = [
        {"scene_id": 1, "text": "A journey begins in the bustling city of Nairobi.", "image_prompt": "A futuristic Nairobi skyline with flying cars, cinematic lighting"},
        {"scene_id": 2, "text": "Through ancient lands where giants roamed.", "image_prompt": "A majestic elephant walking on the savanna at sunset, Mount Kilimanjaro in the background"},
        {"scene_id": 3, "text": "To the shores of the Indian Ocean, a world of wonder.", "image_prompt": "A pristine white sand beach on the Kenyan coast, with a traditional dhow boat sailing on turquoise water"},
    ]

    async def sample_worker_function(scene: Dict) -> Dict:
        scene_id = scene["scene_id"]
        logger.info(f"Processing scene {scene_id}...")
        
        # Concurrently generate voice and image
        voice_task = asyncio.create_task(scene_processor.process_voice(scene["text"], scene_id))
        image_task = asyncio.create_task(scene_processor.process_image(scene["image_prompt"], scene_id))
        
        voice_path, image_path = await asyncio.gather(voice_task, image_task)
        
        # Once assets are ready, compile the video
        # The compilation itself is synchronous, so we run it in an executor
        loop = asyncio.get_running_loop()
        video_path = await loop.run_in_executor(
            None, scene_processor.process_video_compilation, image_path, voice_path, scene_id
        )
        
        logger.info(f"Finished processing scene {scene_id}")
        return {
            "scene_id": scene_id,
            "status": "completed",
            "voice_file": voice_path,
            "image_file": image_path,
            "video_file": video_path
        }

    results = await parallel_processor.run_parallel(scenes, sample_worker_function)
    
    logger.info("\n📊 Final Results:")
    for res in results:
        logger.info(f"  - {res}")
    
    logger.info("\n📈 Performance Stats:")
    stats = parallel_processor.get_processing_stats()
    for key, value in stats.items():
        logger.info(f"  {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())
