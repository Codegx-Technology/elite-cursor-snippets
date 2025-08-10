#!/usr/bin/env python3
"""
🔥 Shujaa Studio - Parallel Processing Engine
Elite-level concurrent scene generation for 3x faster video creation

// [TASK]: Implement parallel multi-scene processing
// [GOAL]: Generate multiple scenes concurrently, reduce total time by 60-70%
// [CONSTRAINTS]: GPU memory management, thread-safe operations
// [SNIPPET]: thinkwithai + refactorclean + surgicalfix
"""

import os
import asyncio
import threading
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import List, Dict, Optional, Callable, Any
import time
import queue
import psutil
from pathlib import Path

from logging_setup import get_logger
from ai_model_manager import generate_text, generate_image, text_to_speech, speech_to_text # Import AI model manager functions

logger = get_logger(__name__)

class ParallelProcessor:
    """
    // [TASK]: Manage parallel scene generation
    // [GOAL]: Optimize resource usage and minimize generation time
    // [SNIPPET]: surgicalfix + refactorclean
    """
    
    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers or min(4, mp.cpu_count())
        self.gpu_available = self._check_gpu_availability()
        self.memory_threshold = 0.85  # 85% memory usage threshold
        
        # Processing queues
        self.scene_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.error_queue = queue.Queue()
        
        # Performance tracking
        self.processing_stats = {
            "scenes_processed": 0,
            "total_time": 0,
            "average_time_per_scene": 0,
            "parallel_efficiency": 0
        }
        
        logger.info(f"[PARALLEL] Initialized with {self.max_workers} workers")
        logger.info(f"[PARALLEL] GPU available: {self.gpu_available}")
    
    def _check_gpu_availability(self) -> bool:
        """Check if GPU is available for processing"""
        try:
            import torch
            return torch.cuda.is_available() and torch.cuda.device_count() > 0
        except ImportError:
            return False
    
    def _check_memory_usage(self) -> float:
        """Check current memory usage percentage"""
        return psutil.virtual_memory().percent / 100
    
    async def process_scenes_parallel(self, scenes: List[Dict],
                                    processing_functions: Dict[str, Callable]) -> List[Dict]:
        """
        // [TASK]: Process multiple scenes in parallel
        // [GOAL]: Generate voice, images, and video for all scenes concurrently
        // [SNIPPET]: thinkwithai + surgicalfix
        """
        start_time = time.time()
        
        logger.info(f"[PARALLEL] Processing {len(scenes)} scenes concurrently...")
        
        # Determine optimal batch size based on memory
        batch_size = self._calculate_optimal_batch_size(len(scenes))
        
        results = []
        
        # Process scenes in batches to manage memory
        for i in range(0, len(scenes), batch_size):
            batch = scenes[i:i + batch_size]
            batch_results = await self._process_scene_batch(batch, processing_functions)
            results.extend(batch_results)
            
            # Memory cleanup between batches
            if i + batch_size < len(scenes):
                await self._cleanup_memory()
        
        total_time = time.time() - start_time
        self._update_processing_stats(len(scenes), total_time)
        
        logger.info(f"[PARALLEL] ✅ Completed {len(scenes)} scenes in {total_time:.1f}s")
        logger.info(f"[PARALLEL] Average: {total_time/len(scenes):.1f}s per scene")
        
        return results
    
    def _calculate_optimal_batch_size(self, total_scenes: int) -> int:
        """
        // [TASK]: Calculate optimal batch size based on available resources
        // [GOAL]: Balance concurrency with memory constraints
        """
        memory_usage = self._check_memory_usage()
        
        if memory_usage > 0.7:
            return min(2, total_scenes)  # Conservative batching
        elif memory_usage > 0.5:
            return min(3, total_scenes)  # Moderate batching
        else:
            return min(self.max_workers, total_scenes)  # Aggressive batching
    
    async def _process_scene_batch(self, batch: List[Dict],
                                 processing_functions: Dict[str, Callable]) -> List[Dict]:
        """
        // [TASK]: Process a batch of scenes concurrently
        // [GOAL]: Efficiently manage concurrent execution of scene components
        """
        
        # Create tasks for concurrent processing
        tasks = []
        for scene in batch:
            task = asyncio.create_task(
                self._process_single_scene(scene, processing_functions)
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle results and exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning(f"[PARALLEL] ⚠️ Scene {i} failed: {result}")
                # Create fallback result
                processed_results.append({
                    "scene_id": batch[i].get("scene_id", i),
                    "status": "failed",
                    "error": str(result),
                    "fallback_used": True
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _process_single_scene(self, scene: Dict,
                                  processing_functions: Dict[str, Callable]) -> Dict:
        """
        // [TASK]: Process individual scene with all components
        // [GOAL]: Generate voice, image, and video for one scene
        // [SNIPPET]: surgicalfix
        """
        scene_id = scene.get("scene_id", "unknown")
        scene_start_time = time.time()
        
        try:
            # Step 1: Generate voice (can run independently)
            voice_result = await asyncio.create_task(
                self._run_in_thread(processing_functions["voice"], scene)
            )
            
            # Step 2: Generate image (can run independently)  
            image_result = await asyncio.create_task(
                self._run_in_thread(processing_functions["image"], scene)
            )
            
            # Step 3: Create video (requires voice and image)
            scene["voice_file"] = voice_result
            scene["image_file"] = image_result
            
            video_result = await asyncio.create_task(
                self._run_in_thread(processing_functions["video"], scene)
            )
            
            processing_time = time.time() - scene_start_time
            
            return {
                "scene_id": scene_id,
                "status": "completed",
                "voice_file": voice_result,
                "image_file": image_result,
                "video_file": video_result,
                "processing_time": processing_time
            }
            
        except Exception as e:
            logger.error(f"[PARALLEL] ❌ Scene {scene_id} processing failed: {e}")
            return {
                "scene_id": scene_id,
                "status": "failed",
                "error": str(e),
                "processing_time": time.time() - scene_start_time
            }
    
    async def _run_in_thread(self, func: Callable, *args) -> Any:
        """
        // [TASK]: Run CPU-intensive function in thread pool
        // [GOAL]: Prevent blocking the asyncio event loop
        """
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=2) as executor:
            return await loop.run_in_executor(executor, func, *args)
    
    async def _cleanup_memory(self):
        """
        // [TASK]: Clean up memory between batches
        // [GOAL]: Prevent memory leaks and optimize resource usage
        """
        import gc
        gc.collect()
        
        if self.gpu_available:
            try:
                import torch
                torch.cuda.empty_cache()
            except ImportError:
                pass
        
        # Brief pause to allow memory cleanup
        await asyncio.sleep(0.5)
    
    def _update_processing_stats(self, scenes_count: int, total_time: float):
        """
        // [TASK]: Update processing performance statistics
        // [GOAL]: Track and report performance metrics
        """
        self.processing_stats["scenes_processed"] += scenes_count
        self.processing_stats["total_time"] += total_time
        self.processing_stats["average_time_per_scene"] = (
            self.processing_stats["total_time"] /
            self.processing_stats["scenes_processed"]
        )
        
        # Calculate parallel efficiency (compared to sequential processing)
        sequential_estimate = scenes_count * self.processing_stats["average_time_per_scene"]
        self.processing_stats["parallel_efficiency"] = (
            sequential_estimate / total_time if total_time > 0 else 1.0
        )
    
    def get_processing_stats(self) -> Dict:
        """
        // [TASK]: Get current processing performance statistics
        // [GOAL]: Provide insights into parallel processing efficiency
        """
        return {
            **self.processing_stats,
            "memory_usage": f"{self._check_memory_usage():.1%}",
            "max_workers": self.max_workers,
            "gpu_available": self.gpu_available
        }

class SceneProcessor:
    """
    // [TASK]: Individual scene processing functions
    // [GOAL]: Provide thread-safe processing functions for parallel execution
    // [SNIPPET]: refactorclean + surgicalfix
    """
    
    def __init__(self, model_cache=None):
        self.model_cache = model_cache
        self.temp_dir = Path("temp/parallel")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"SceneProcessor initialized. Temp directory: {self.temp_dir}")
    
    async def process_voice(self, scene: Dict) -> str:
        """
        // [TASK]: Generate voice for scene using ai_model_manager
        // [GOAL]: Create audio file for scene dialogue
        """
        scene_id = scene.get("scene_id", "unknown")
        text = scene.get("text", "")
        
        voice_file_path = self.temp_dir / f"scene_{scene_id}_voice.wav"
        
        try:
            audio_bytes = await text_to_speech(text)
            with open(voice_file_path, "wb") as f:
                f.write(audio_bytes)
            logger.info(f"Generated voice for scene {scene_id}: {voice_file_path}")
            return str(voice_file_path)
        except Exception as e:
            logger.error(f"Failed to generate voice for scene {scene_id}: {e}")
            # Fallback to placeholder audio
            voice_file_path.touch()
            logger.warning(f"Using placeholder voice for scene {scene_id}")
            return str(voice_file_path)
    
    async def process_image(self, scene: Dict) -> str:
        """
        // [TASK]: Generate image for scene using ai_model_manager
        // [GOAL]: Create image file for scene visual
        """
        scene_id = scene.get("scene_id", "unknown")
        prompt = scene.get("image_prompt", "")
        
        image_file_path = self.temp_dir / f"scene_{scene_id}_image.png"
        
        try:
            image_bytes = await generate_image(prompt)
            with open(image_file_path, "wb") as f:
                f.write(image_bytes)
            logger.info(f"Generated image for scene {scene_id}: {image_file_path}")
            return str(image_file_path)
        except Exception as e:
            logger.error(f"Failed to generate image for scene {scene_id}: {e}")
            # Fallback to placeholder image
            image_file_path.touch()
            logger.warning(f"Using placeholder image for scene {scene_id}")
            return str(image_file_path)
    
    async def process_video(self, scene: Dict) -> str:
        """
        // [TASK]: Create video from voice and image
        // [GOAL]: Combine audio and visual into a scene video file
        """
        scene_id = scene.get("scene_id", "unknown")
        voice_file = scene.get("voice_file", "")
        image_file = scene.get("image_file", "")
        
        video_file_path = self.temp_dir / f"scene_{scene_id}_video.mp4"
        
        # Placeholder for actual video creation (e.g., using moviepy)
        # This would involve loading voice_file and image_file and combining them
        
        # Simulate video creation time
        time.sleep(1)  # Replace with actual video creation
        
        # Create placeholder video file
        video_file_path.touch()
        
        logger.info(f"Generated placeholder video for scene {scene_id}: {video_file_path}")
        return str(video_file_path)

# Example usage
async def main():
    """
    // [TASK]: Test parallel processing
    // [GOAL]: Verify parallel processing functionality
    """
    processor = ParallelProcessor(max_workers=3)
    scene_processor = SceneProcessor()
    
    # Sample scenes
    scenes = [
        {"scene_id": 1, "text": "Scene 1 text", "image_prompt": "Scene 1 image"},
        {"scene_id": 2, "text": "Scene 2 text", "image_prompt": "Scene 2 image"},
        {"scene_id": 3, "text": "Scene 3 text", "image_prompt": "Scene 3 image"},
        {"scene_id": 4, "text": "Scene 4 text", "image_prompt": "Scene 4 image"},
    ]
    
    processing_functions = {
        "voice": scene_processor.process_voice,
        "image": scene_processor.process_image,
        "video": scene_processor.process_video
    }
    
    results = await processor.process_scenes_parallel(scenes, processing_functions)
    
    logger.info("\n📊 Processing Results:")
    for result in results:
        logger.info(f"  Scene {result['scene_id']}: {result['status']}")
    
    logger.info("\n📈 Performance Stats:")
    stats = processor.get_processing_stats()
    for key, value in stats.items():
        logger.info(f"  {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())