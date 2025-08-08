#!/usr/bin/env python3
"""
📊 Batch Video Generator - Combo Pack D CSV Processing
Generate multiple videos from CSV input with progress tracking

// [TASK]: Create comprehensive batch processing system
// [GOAL]: CSV-based video generation with progress tracking and export options
// [SNIPPET]: thinkwithai + refactorclean + kenyafirst
// [CONTEXT]: Elite batch processing for video generation
"""

import csv
import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime
import argparse

# Add offline_video_maker to path
sys.path.append(str(Path(__file__).parent / "offline_video_maker"))

from offline_video_maker.generate_video import VideoGenerator
from offline_video_maker.helpers import MediaUtils, SubtitleEngine, MusicIntegration, VerticalExport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchVideoGenerator:
    """Professional batch video generation from CSV input"""
    
    def __init__(self, output_dir: str = "batch_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.video_generator = VideoGenerator()
        self.media_utils = MediaUtils()
        self.subtitle_engine = SubtitleEngine()
        self.music_integration = MusicIntegration()
        self.vertical_export = VerticalExport()
        
        # Batch processing state
        self.current_batch = None
        self.results = []
        
        logger.info(f"[BATCH] Batch generator initialized: {self.output_dir}")
    
    def load_csv(self, csv_path: str) -> List[Dict]:
        """
        Load video prompts from CSV file
        
        Expected CSV columns:
        - prompt (required): Story prompt
        - title (optional): Video title
        - description (optional): Video description
        - category (optional): Content category
        - platforms (optional): Comma-separated export platforms
        - enable_subtitles (optional): true/false
        - enable_music (optional): true/false
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            List of video generation tasks
        """
        try:
            logger.info(f"[BATCH] Loading CSV: {csv_path}")
            
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"CSV file not found: {csv_path}")
            
            tasks = []
            
            with open(csv_path, 'r', encoding='utf-8', newline='') as csvfile:
                # Detect delimiter
                sample = csvfile.read(1024)
                csvfile.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                
                for row_num, row in enumerate(reader, 1):
                    # Validate required fields
                    if not row.get('prompt', '').strip():
                        logger.warning(f"[BATCH] Row {row_num}: Missing prompt, skipping")
                        continue
                    
                    # Parse platforms
                    platforms = []
                    if row.get('platforms'):
                        platforms = [p.strip() for p in row['platforms'].split(',')]
                    
                    # Parse boolean options
                    enable_subtitles = row.get('enable_subtitles', 'true').lower() == 'true'
                    enable_music = row.get('enable_music', 'true').lower() == 'true'
                    
                    task = {
                        'id': row_num,
                        'prompt': row['prompt'].strip(),
                        'title': row.get('title', f"Video_{row_num}").strip(),
                        'description': row.get('description', '').strip(),
                        'category': row.get('category', 'general').strip(),
                        'platforms': platforms,
                        'enable_subtitles': enable_subtitles,
                        'enable_music': enable_music,
                        'status': 'pending'
                    }
                    
                    tasks.append(task)
            
            logger.info(f"[BATCH] Loaded {len(tasks)} tasks from CSV")
            return tasks
            
        except Exception as e:
            logger.error(f"[BATCH] Failed to load CSV: {e}")
            raise
    
    def process_batch(self, csv_path: str, 
                     enable_subtitles: bool = True,
                     enable_music: bool = True,
                     export_platforms: List[str] = None,
                     max_concurrent: int = 1) -> Dict:
        """
        Process batch of videos from CSV
        
        Args:
            csv_path: Path to CSV file
            enable_subtitles: Global subtitle setting (overridden by CSV)
            enable_music: Global music setting (overridden by CSV)
            export_platforms: Global platform list (overridden by CSV)
            max_concurrent: Maximum concurrent video generations
            
        Returns:
            Batch processing results
        """
        try:
            logger.info(f"[BATCH] Starting batch processing: {csv_path}")
            
            # Load tasks
            tasks = self.load_csv(csv_path)
            
            if not tasks:
                raise ValueError("No valid tasks found in CSV")
            
            # Initialize batch
            batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_dir = self.output_dir / f"batch_{batch_id}"
            batch_dir.mkdir(exist_ok=True)
            
            self.current_batch = {
                'id': batch_id,
                'csv_path': csv_path,
                'output_dir': str(batch_dir),
                'total_tasks': len(tasks),
                'completed': 0,
                'failed': 0,
                'start_time': datetime.now(),
                'tasks': tasks
            }
            
            # Process tasks
            results = []
            
            for i, task in enumerate(tasks, 1):
                logger.info(f"[BATCH] Processing task {i}/{len(tasks)}: {task['title']}")
                
                try:
                    # Update task status
                    task['status'] = 'processing'
                    task['start_time'] = datetime.now()
                    
                    # Generate video
                    result = self._process_single_task(task, batch_dir, 
                                                     enable_subtitles, enable_music, 
                                                     export_platforms)
                    
                    task['status'] = 'completed' if result['success'] else 'failed'
                    task['end_time'] = datetime.now()
                    task['result'] = result
                    
                    if result['success']:
                        self.current_batch['completed'] += 1
                        logger.info(f"[BATCH] ✅ Task {i} completed: {result['video_path']}")
                    else:
                        self.current_batch['failed'] += 1
                        logger.error(f"[BATCH] ❌ Task {i} failed: {result['error']}")
                    
                    results.append(result)
                    
                    # Save progress
                    self._save_batch_progress()
                    
                except Exception as e:
                    logger.error(f"[BATCH] Task {i} error: {e}")
                    task['status'] = 'failed'
                    task['error'] = str(e)
                    self.current_batch['failed'] += 1
                    
                    results.append({
                        'success': False,
                        'task_id': task['id'],
                        'error': str(e)
                    })
            
            # Finalize batch
            self.current_batch['end_time'] = datetime.now()
            self.current_batch['duration'] = (self.current_batch['end_time'] - self.current_batch['start_time']).total_seconds()
            
            # Save final results
            self._save_batch_results(results)
            
            logger.info(f"[BATCH] Batch completed: {self.current_batch['completed']}/{len(tasks)} successful")
            
            return {
                'batch_id': batch_id,
                'total_tasks': len(tasks),
                'completed': self.current_batch['completed'],
                'failed': self.current_batch['failed'],
                'duration': self.current_batch['duration'],
                'output_dir': str(batch_dir),
                'results': results
            }
            
        except Exception as e:
            logger.error(f"[BATCH] Batch processing failed: {e}")
            raise
    
    def _process_single_task(self, task: Dict, batch_dir: Path,
                           global_subtitles: bool, global_music: bool,
                           global_platforms: List[str]) -> Dict:
        """Process a single video generation task"""
        try:
            # Determine settings (task-specific overrides global)
            enable_subtitles = task.get('enable_subtitles', global_subtitles)
            enable_music = task.get('enable_music', global_music)
            platforms = task.get('platforms') or global_platforms or []
            
            # Create task directory
            task_dir = batch_dir / f"task_{task['id']:03d}_{task['title'][:20]}"
            task_dir.mkdir(exist_ok=True)
            
            # Generate base video
            video_path = self.video_generator.generate_video(task['prompt'])
            
            if not video_path or not os.path.exists(video_path):
                return {
                    'success': False,
                    'task_id': task['id'],
                    'error': 'Video generation failed'
                }
            
            # Move video to task directory
            final_video_path = task_dir / f"{task['title']}.mp4"
            os.rename(video_path, str(final_video_path))
            video_path = str(final_video_path)
            
            # Add subtitles if enabled
            if enable_subtitles and self.subtitle_engine.is_available():
                video_path = self._add_subtitles(video_path, task_dir)
            
            # Export to platforms if specified
            exported_files = {}
            if platforms:
                export_dir = task_dir / "exports"
                results = self.vertical_export.batch_convert_to_platforms(
                    video_path, str(export_dir), platforms
                )
                exported_files = {platform: success for platform, success in results.items()}
            
            # Create task metadata
            metadata = {
                'task': task,
                'video_path': video_path,
                'exported_files': exported_files,
                'settings': {
                    'subtitles': enable_subtitles,
                    'music': enable_music,
                    'platforms': platforms
                }
            }
            
            # Save metadata
            metadata_path = task_dir / "metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            return {
                'success': True,
                'task_id': task['id'],
                'video_path': video_path,
                'exported_files': exported_files,
                'metadata_path': str(metadata_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'task_id': task['id'],
                'error': str(e)
            }
    
    def _add_subtitles(self, video_path: str, task_dir: Path) -> str:
        """Add subtitles to video"""
        try:
            # Extract audio
            audio_path = task_dir / "audio.wav"
            
            import subprocess
            cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", str(audio_path)]
            subprocess.run(cmd, capture_output=True, check=True)
            
            # Generate subtitles
            srt_path = task_dir / "subtitles.srt"
            if self.subtitle_engine.generate_subtitles_from_audio(str(audio_path), str(srt_path)):
                # Burn subtitles
                subtitled_video = task_dir / "video_with_subtitles.mp4"
                if self.media_utils.burn_subtitles(video_path, str(srt_path), str(subtitled_video)):
                    return str(subtitled_video)
            
            return video_path
            
        except Exception as e:
            logger.error(f"[BATCH] Subtitle addition failed: {e}")
            return video_path
    
    def _save_batch_progress(self):
        """Save current batch progress"""
        if not self.current_batch:
            return
        
        progress_file = Path(self.current_batch['output_dir']) / "progress.json"
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_batch, f, indent=2, default=str)
    
    def _save_batch_results(self, results: List[Dict]):
        """Save final batch results"""
        if not self.current_batch:
            return
        
        results_file = Path(self.current_batch['output_dir']) / "results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'batch_info': self.current_batch,
                'results': results
            }, f, indent=2, default=str)
    
    def create_example_csv(self, output_path: str = "example_batch.csv"):
        """Create an example CSV file for batch processing"""
        example_data = [
            {
                'prompt': 'Grace from Kibera dreams of becoming a software engineer. Despite challenges, she studies hard and gets a scholarship to Strathmore University.',
                'title': 'Grace_Coding_Journey',
                'description': 'Inspirational story about education and technology',
                'category': 'education',
                'platforms': 'tiktok,instagram_stories',
                'enable_subtitles': 'true',
                'enable_music': 'true'
            },
            {
                'prompt': 'Young inventor Juma from Mombasa creates a low-cost water filtration system using local materials.',
                'title': 'Juma_Water_Innovation',
                'description': 'Innovation story about solving water problems',
                'category': 'innovation',
                'platforms': 'youtube_shorts,whatsapp',
                'enable_subtitles': 'true',
                'enable_music': 'true'
            },
            {
                'prompt': 'Maria starts a small business selling vegetables in Kawangware market. Using mobile money, she grows into a supply chain.',
                'title': 'Maria_Business_Growth',
                'description': 'Entrepreneurship story about market innovation',
                'category': 'business',
                'platforms': 'tiktok,facebook_stories',
                'enable_subtitles': 'true',
                'enable_music': 'true'
            }
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['prompt', 'title', 'description', 'category', 'platforms', 'enable_subtitles', 'enable_music']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in example_data:
                writer.writerow(row)
        
        logger.info(f"[BATCH] Example CSV created: {output_path}")


def main():
    """Command-line interface for batch processing"""
    parser = argparse.ArgumentParser(description="Batch Video Generator for Shujaa Studio")
    parser.add_argument("csv_file", help="Path to CSV file with video prompts")
    parser.add_argument("--output-dir", default="batch_output", help="Output directory for generated videos")
    parser.add_argument("--no-subtitles", action="store_true", help="Disable subtitle generation")
    parser.add_argument("--no-music", action="store_true", help="Disable background music")
    parser.add_argument("--platforms", nargs="+", help="Export platforms", 
                       choices=["tiktok", "instagram_stories", "whatsapp", "youtube_shorts", "facebook_stories"])
    parser.add_argument("--create-example", action="store_true", help="Create example CSV file")
    
    args = parser.parse_args()
    
    # Create example CSV if requested
    if args.create_example:
        generator = BatchVideoGenerator()
        generator.create_example_csv("example_batch.csv")
        print("✅ Example CSV created: example_batch.csv")
        return
    
    # Process batch
    try:
        generator = BatchVideoGenerator(args.output_dir)
        
        results = generator.process_batch(
            csv_path=args.csv_file,
            enable_subtitles=not args.no_subtitles,
            enable_music=not args.no_music,
            export_platforms=args.platforms
        )
        
        print(f"\n🎉 Batch processing completed!")
        print(f"📊 Results: {results['completed']}/{results['total_tasks']} successful")
        print(f"⏱️  Duration: {results['duration']:.1f} seconds")
        print(f"📁 Output: {results['output_dir']}")
        
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
