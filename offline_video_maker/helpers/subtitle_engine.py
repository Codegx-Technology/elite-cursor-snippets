#!/usr/bin/env python3
"""
🎬 Subtitle Engine - Combo Pack D Whisper Integration
Auto-generate and format subtitles from audio using Whisper

// [TASK]: Create comprehensive subtitle generation system
// [GOAL]: Whisper-based SRT generation with Kenya-first formatting
// [SNIPPET]: surgicalfix + refactorclean + kenyafirst
// [CONTEXT]: Elite subtitle generation for video content
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import tempfile
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubtitleEngine:
    """Professional subtitle generation using Whisper"""
    
    def __init__(self):
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Initialize Whisper models
        self.whisper_model = None
        self.faster_whisper_model = None
        
        # Try to load faster-whisper first (more efficient)
        try:
            from faster_whisper import WhisperModel
            self.faster_whisper_model = WhisperModel("small", device="auto")
            self.use_faster_whisper = True
            logger.info("[SUBTITLES] ✅ Faster-Whisper model loaded")
        except ImportError:
            logger.warning("[SUBTITLES] Faster-Whisper not available, trying OpenAI Whisper")
            self.use_faster_whisper = False
            
            # Fallback to OpenAI Whisper
            try:
                import whisper
                self.whisper_model = whisper.load_model("small")
                logger.info("[SUBTITLES] ✅ OpenAI Whisper model loaded")
            except ImportError:
                logger.error("[SUBTITLES] ❌ No Whisper models available")
                self.whisper_model = None
    
    def transcribe_audio(self, audio_path: str) -> Optional[List[Dict]]:
        """
        Transcribe audio file to text with timestamps
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            List of segments with text and timestamps, or None if failed
        """
        try:
            logger.info(f"[SUBTITLES] Transcribing audio: {audio_path}")
            
            if not os.path.exists(audio_path):
                logger.error(f"[SUBTITLES] Audio file not found: {audio_path}")
                return None
            
            if self.use_faster_whisper and self.faster_whisper_model:
                return self._transcribe_with_faster_whisper(audio_path)
            elif self.whisper_model:
                return self._transcribe_with_openai_whisper(audio_path)
            else:
                logger.error("[SUBTITLES] No Whisper model available")
                return None
                
        except Exception as e:
            logger.error(f"[SUBTITLES] ❌ Transcription failed: {e}")
            return None
    
    def _transcribe_with_faster_whisper(self, audio_path: str) -> List[Dict]:
        """Transcribe using faster-whisper"""
        segments = []
        
        segments_iter, info = self.faster_whisper_model.transcribe(
            audio_path,
            beam_size=5,
            language="en"  # Can be auto-detected or set to specific language
        )
        
        for segment in segments_iter:
            segments.append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text.strip()
            })
        
        logger.info(f"[SUBTITLES] ✅ Transcribed {len(segments)} segments")
        return segments
    
    def _transcribe_with_openai_whisper(self, audio_path: str) -> List[Dict]:
        """Transcribe using OpenAI Whisper"""
        result = self.whisper_model.transcribe(audio_path)
        
        segments = []
        for segment in result['segments']:
            segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip()
            })
        
        logger.info(f"[SUBTITLES] ✅ Transcribed {len(segments)} segments")
        return segments
    
    def generate_srt(self, segments: List[Dict], output_path: str) -> bool:
        """
        Generate SRT subtitle file from segments
        
        Args:
            segments: List of segments with start, end, text
            output_path: Output SRT file path
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[SUBTITLES] Generating SRT file: {output_path}")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments, 1):
                    start_time = self._format_timestamp(segment['start'])
                    end_time = self._format_timestamp(segment['end'])
                    text = segment['text']
                    
                    # Apply Kenya-first formatting
                    text = self._format_kenya_text(text)
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            logger.info(f"[SUBTITLES] ✅ SRT file generated with {len(segments)} subtitles")
            return True
            
        except Exception as e:
            logger.error(f"[SUBTITLES] ❌ SRT generation failed: {e}")
            return False
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp for SRT format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def _format_kenya_text(self, text: str) -> str:
        """
        Apply Kenya-first formatting to subtitle text
        
        Args:
            text: Raw subtitle text
            
        Returns:
            Formatted text with Kenya-specific improvements
        """
        # Clean up common transcription issues
        text = text.strip()
        
        # Capitalize first letter of sentences
        if text and not text[0].isupper():
            text = text[0].upper() + text[1:]
        
        # Add period if missing at end of sentence
        if text and text[-1] not in '.!?':
            text += '.'
        
        # Handle common Kenyan English patterns
        replacements = {
            ' uhm ': ' um ',
            ' uh ': ' ',
            ' like ': ' ',
            ' you know ': ' ',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Remove extra spaces
        text = ' '.join(text.split())
        
        return text
    
    def generate_subtitles_from_audio(self, audio_path: str, output_srt: str) -> bool:
        """
        Complete subtitle generation pipeline from audio to SRT
        
        Args:
            audio_path: Input audio file path
            output_srt: Output SRT file path
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[SUBTITLES] Starting subtitle generation pipeline")
            
            # Step 1: Transcribe audio
            segments = self.transcribe_audio(audio_path)
            if not segments:
                logger.error("[SUBTITLES] ❌ Transcription failed")
                return False
            
            # Step 2: Generate SRT file
            success = self.generate_srt(segments, output_srt)
            if not success:
                logger.error("[SUBTITLES] ❌ SRT generation failed")
                return False
            
            logger.info(f"[SUBTITLES] ✅ Complete subtitle pipeline successful")
            return True
            
        except Exception as e:
            logger.error(f"[SUBTITLES] ❌ Subtitle pipeline failed: {e}")
            return False
    
    def create_vtt_from_srt(self, srt_path: str, vtt_path: str) -> bool:
        """
        Convert SRT to WebVTT format for web players
        
        Args:
            srt_path: Input SRT file path
            vtt_path: Output VTT file path
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"[SUBTITLES] Converting SRT to VTT: {vtt_path}")
            
            with open(srt_path, 'r', encoding='utf-8') as srt_file:
                srt_content = srt_file.read()
            
            # Convert SRT timestamps to VTT format
            vtt_content = "WEBVTT\n\n"
            
            # Replace comma with dot in timestamps
            vtt_content += srt_content.replace(',', '.')
            
            with open(vtt_path, 'w', encoding='utf-8') as vtt_file:
                vtt_file.write(vtt_content)
            
            logger.info(f"[SUBTITLES] ✅ VTT conversion successful")
            return True
            
        except Exception as e:
            logger.error(f"[SUBTITLES] ❌ VTT conversion failed: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if subtitle generation is available"""
        return (self.use_faster_whisper and self.faster_whisper_model is not None) or \
               (self.whisper_model is not None)
