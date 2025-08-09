#!/usr/bin/env python3
"""
pipeline_wrapper.py
Lightweight wrapper that calls main pipeline.py
Following elite-cursor-snippets patterns for Kenya-specific requirements

// [TASK]: Create lightweight pipeline wrapper
// [GOAL]: Simple interface for video generation
// [SNIPPET]: surgicalfix + refactorclean + kenyafirst
// [CONTEXT]: Production-ready video generation wrapper
"""

import subprocess
import os
import yaml
import uuid
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PipelineWrapper:
    """Lightweight wrapper for Shujaa Studio pipeline"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.pipeline_path = Path("pipeline.py")
        
        # Ensure pipeline exists
        if not self.pipeline_path.exists():
            raise FileNotFoundError(f"Pipeline not found: {self.pipeline_path}")
        
        logger.info(f"[WRAPPER] Pipeline wrapper initialized: {self.pipeline_path}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                logger.warning(f"[WRAPPER] Config not found: {self.config_path}, using defaults")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"[WRAPPER] Config load failed: {e}, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "work_base": "./outputs",
            "bark_cli": "./voice_engine.py",
            "sdxl_path": "./models/sdxl",
            "use_cuda": False,
            "default_scenes": 3,
            "vertical": True,
            "video_fps": 24,
            "video_width": 1080,
            "video_height": 1920
        }
    
    def generate(self, prompt: str, out_path: Optional[str] = None, 
                scenes: Optional[int] = None, vertical: Optional[bool] = None, 
                lang: str = "sheng") -> str:
        """
        Generate video using pipeline.py
        
        Args:
            prompt: Story prompt
            out_path: Output video path (auto-generated if None)
            scenes: Number of scenes (uses config default if None)
            vertical: Vertical video (uses config default if None)
            lang: Language for TTS
            
        Returns:
            str: Path to generated video
        """
        try:
            # Generate output path if not provided
            if out_path is None:
                work_base = self.config.get("work_base", "./outputs")
                os.makedirs(work_base, exist_ok=True)
                out_path = os.path.join(work_base, f"{uuid.uuid4().hex[:8]}.mp4")
            
            # Use config defaults if not specified
            if scenes is None:
                scenes = self.config.get("default_scenes", 3)
            if vertical is None:
                vertical = self.config.get("vertical", True)
            
            # Build pipeline command
            cmd = [
                "python", str(self.pipeline_path),
                "--prompt", prompt,
                "--out", out_path,
                "--scenes", str(scenes),
                "--lang", lang
            ]
            
            if vertical:
                cmd.append("--vertical")
            
            logger.info(f"[WRAPPER] Executing: {' '.join(cmd)}")
            
            # Execute pipeline
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Pipeline failed: {result.stderr}")
            
            # Check if output file exists
            if not os.path.exists(out_path):
                raise RuntimeError("Video file not generated")
            
            logger.info(f"[WRAPPER] ✅ Video generated: {out_path}")
            return out_path
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Video generation timed out")
        except Exception as e:
            logger.error(f"[WRAPPER] ❌ Generation failed: {e}")
            raise
    
    def batch_generate(self, csv_path: str, output_dir: str = None) -> Dict[str, Any]:
        """
        Generate multiple videos from CSV file
        
        Args:
            csv_path: Path to CSV file with prompts
            output_dir: Output directory (uses config default if None)
            
        Returns:
            Dict with batch results
        """
        try:
            if output_dir is None:
                output_dir = self.config.get("work_base", "./outputs")
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Build batch command
            cmd = [
                "python", str(self.pipeline_path),
                "--batch", csv_path
            ]
            
            logger.info(f"[WRAPPER] Executing batch: {' '.join(cmd)}")
            
            # Execute batch pipeline
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=1800  # 30 minute timeout for batch
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Batch pipeline failed: {result.stderr}")
            
            logger.info(f"[WRAPPER] ✅ Batch generation completed")
            return {
                "success": True,
                "output_dir": output_dir,
                "csv_path": csv_path
            }
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Batch generation timed out")
        except Exception as e:
            logger.error(f"[WRAPPER] ❌ Batch generation failed: {e}")
            raise
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config.copy()
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration"""
        try:
            self.config.update(updates)
            
            # Save to file
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            
            logger.info(f"[WRAPPER] ✅ Config updated: {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"[WRAPPER] ❌ Config update failed: {e}")
            return False


# Global instance for easy import
pipeline_wrapper = PipelineWrapper()


def generate_video(prompt: str, **kwargs) -> str:
    """Simple function to generate video"""
    return pipeline_wrapper.generate(prompt, **kwargs)


def batch_generate(csv_path: str, **kwargs) -> Dict[str, Any]:
    """Simple function to batch generate videos"""
    return pipeline_wrapper.batch_generate(csv_path, **kwargs)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Shujaa Studio Pipeline Wrapper")
    parser.add_argument("prompt", help="Story prompt")
    parser.add_argument("--out", help="Output video path")
    parser.add_argument("--scenes", type=int, help="Number of scenes")
    parser.add_argument("--vertical", action="store_true", help="Vertical video")
    parser.add_argument("--lang", default="sheng", help="Language")
    parser.add_argument("--batch", help="CSV file for batch processing")
    
    args = parser.parse_args()
    
    try:
        if args.batch:
            result = batch_generate(args.batch)
            print(f"✅ Batch completed: {result}")
        else:
            video_path = generate_video(
                args.prompt,
                out_path=args.out,
                scenes=args.scenes,
                vertical=args.vertical,
                lang=args.lang
            )
            print(f"✅ Video generated: {video_path}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
