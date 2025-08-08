#!/usr/bin/env python3
"""
🎵 Music Integration - Combo Pack D Enhanced Music System
Advanced background music mixing with volume control and synchronization

// [TASK]: Create enhanced music integration for Combo Pack D
// [GOAL]: Professional audio mixing with Kenya-first music selection
// [SNIPPET]: surgicalfix + refactorclean + kenyafirst
// [CONTEXT]: Elite music integration for video content
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MusicIntegration:
    """Enhanced music integration for Combo Pack D"""
    
    def __init__(self, music_dir: Optional[Path] = None):
        self.music_dir = music_dir or Path("music_library")
        self.music_dir.mkdir(exist_ok=True)
        
        # Enhanced music categories for Kenya-first content
        self.categories = {
            "inspirational": {
                "keywords": ["success", "achievement", "dream", "goal", "motivation", "inspire"],
                "volume": 0.25,
                "description": "Uplifting and motivational"
            },
            "storytelling": {
                "keywords": ["story", "tale", "narrative", "journey", "experience"],
                "volume": 0.20,
                "description": "Gentle narrative background"
            },
            "technology": {
                "keywords": ["technology", "engineer", "computer", "innovation", "coding", "digital"],
                "volume": 0.30,
                "description": "Modern and innovative"
            },
            "community": {
                "keywords": ["community", "village", "together", "help", "unity", "family"],
                "volume": 0.22,
                "description": "Warm and communal"
            },
            "african": {
                "keywords": ["kenya", "africa", "kibera", "turkana", "maasai", "swahili", "sheng"],
                "volume": 0.28,
                "description": "Traditional African themes"
            },
            "education": {
                "keywords": ["school", "learn", "study", "education", "knowledge", "university"],
                "volume": 0.20,
                "description": "Educational and focused"
            },
            "entrepreneurship": {
                "keywords": ["business", "startup", "entrepreneur", "hustle", "market", "innovation"],
                "volume": 0.32,
                "description": "Dynamic business energy"
            }
        }
        
        logger.info(f"[MUSIC+] Enhanced music integration initialized")
    
    def analyze_story_mood(self, story_text: str) -> Dict[str, float]:
        """
        Analyze story text to determine appropriate music mood
        
        Args:
            story_text: Story content to analyze
            
        Returns:
            Dictionary with category scores
        """
        story_lower = story_text.lower()
        mood_scores = {}
        
        for category, config in self.categories.items():
            score = 0
            keywords = config["keywords"]
            
            # Count keyword matches
            for keyword in keywords:
                score += story_lower.count(keyword)
            
            # Bonus for exact phrase matches
            if any(keyword in story_lower for keyword in keywords):
                score += 2
            
            mood_scores[category] = score
        
        # Normalize scores
        total_score = sum(mood_scores.values())
        if total_score > 0:
            mood_scores = {k: v/total_score for k, v in mood_scores.items()}
        
        logger.info(f"[MUSIC+] Story mood analysis: {mood_scores}")
        return mood_scores
    
    def select_music_category(self, story_text: str) -> str:
        """
        Select the best music category for a story
        
        Args:
            story_text: Story content
            
        Returns:
            Selected category name
        """
        mood_scores = self.analyze_story_mood(story_text)
        
        if not mood_scores or max(mood_scores.values()) == 0:
            # Default to storytelling if no clear match
            return "storytelling"
        
        # Select category with highest score
        selected_category = max(mood_scores, key=mood_scores.get)
        
        logger.info(f"[MUSIC+] Selected category: {selected_category}")
        return selected_category
    
    def get_music_files(self, category: str) -> List[Path]:
        """
        Get available music files for a category
        
        Args:
            category: Music category
            
        Returns:
            List of available music files
        """
        music_files = []
        
        # Look for category-specific files
        patterns = [f"*{category}*"]
        
        # Add keyword patterns
        if category in self.categories:
            keywords = self.categories[category]["keywords"][:3]  # Top 3 keywords
            patterns.extend([f"*{keyword}*" for keyword in keywords])
        
        # Search for files
        for pattern in patterns:
            music_files.extend(self.music_dir.glob(f"{pattern}.wav"))
            music_files.extend(self.music_dir.glob(f"{pattern}.mp3"))
            music_files.extend(self.music_dir.glob(f"{pattern}.m4a"))
        
        # Remove duplicates
        music_files = list(set(music_files))
        
        # Fallback to any available music
        if not music_files:
            music_files = list(self.music_dir.glob("*.wav"))
            music_files.extend(self.music_dir.glob("*.mp3"))
            music_files.extend(self.music_dir.glob("*.m4a"))
        
        logger.info(f"[MUSIC+] Found {len(music_files)} files for category: {category}")
        return music_files
    
    def get_optimal_volume(self, category: str, scene_type: str = "normal") -> float:
        """
        Get optimal volume for music category and scene type
        
        Args:
            category: Music category
            scene_type: Type of scene (normal, dramatic, quiet, energetic)
            
        Returns:
            Optimal volume level (0.0 to 1.0)
        """
        base_volume = self.categories.get(category, {}).get("volume", 0.25)
        
        # Adjust based on scene type
        volume_adjustments = {
            "normal": 1.0,
            "dramatic": 1.3,
            "quiet": 0.7,
            "energetic": 1.4,
            "emotional": 0.8,
            "action": 1.5
        }
        
        adjustment = volume_adjustments.get(scene_type, 1.0)
        final_volume = min(base_volume * adjustment, 0.5)  # Cap at 50%
        
        logger.info(f"[MUSIC+] Volume for {category}/{scene_type}: {final_volume:.2f}")
        return final_volume
    
    def create_music_plan(self, scenes: List[Dict], story_text: str) -> List[Dict]:
        """
        Create a comprehensive music plan for all scenes
        
        Args:
            scenes: List of scene dictionaries
            story_text: Full story text
            
        Returns:
            List of music plans for each scene
        """
        music_plans = []
        
        # Analyze overall story mood
        primary_category = self.select_music_category(story_text)
        
        for i, scene in enumerate(scenes):
            scene_text = scene.get('text', '')
            scene_duration = scene.get('duration', 5.0)
            
            # Analyze individual scene
            scene_category = self.select_music_category(scene_text)
            
            # Determine scene type based on content
            scene_type = self._determine_scene_type(scene_text)
            
            # Select final category (prefer scene-specific, fallback to story-wide)
            final_category = scene_category if scene_category != "storytelling" else primary_category
            
            # Get music files and volume
            music_files = self.get_music_files(final_category)
            volume = self.get_optimal_volume(final_category, scene_type)
            
            music_plan = {
                "scene_index": i,
                "category": final_category,
                "scene_type": scene_type,
                "volume": volume,
                "duration": scene_duration,
                "available_files": music_files,
                "selected_file": random.choice(music_files) if music_files else None
            }
            
            music_plans.append(music_plan)
            
            logger.info(f"[MUSIC+] Scene {i+1} plan: {final_category} at {volume:.2f} volume")
        
        return music_plans
    
    def _determine_scene_type(self, scene_text: str) -> str:
        """
        Determine scene type based on content analysis
        
        Args:
            scene_text: Scene text content
            
        Returns:
            Scene type classification
        """
        text_lower = scene_text.lower()
        
        # Scene type indicators
        type_indicators = {
            "dramatic": ["challenge", "difficult", "struggle", "overcome", "crisis"],
            "energetic": ["action", "running", "building", "creating", "achieving"],
            "emotional": ["love", "family", "loss", "hope", "dream", "heart"],
            "quiet": ["thinking", "planning", "studying", "reading", "peaceful"],
            "action": ["building", "working", "coding", "developing", "implementing"]
        }
        
        for scene_type, indicators in type_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                return scene_type
        
        return "normal"
    
    def validate_music_setup(self) -> Dict[str, bool]:
        """
        Validate music integration setup
        
        Returns:
            Dictionary with validation results
        """
        validation = {
            "music_directory_exists": self.music_dir.exists(),
            "has_music_files": False,
            "categories_covered": {},
            "total_files": 0
        }
        
        if validation["music_directory_exists"]:
            # Count music files
            music_files = list(self.music_dir.glob("*.wav"))
            music_files.extend(self.music_dir.glob("*.mp3"))
            music_files.extend(self.music_dir.glob("*.m4a"))
            
            validation["total_files"] = len(music_files)
            validation["has_music_files"] = len(music_files) > 0
            
            # Check category coverage
            for category in self.categories.keys():
                category_files = self.get_music_files(category)
                validation["categories_covered"][category] = len(category_files) > 0
        
        logger.info(f"[MUSIC+] Validation results: {validation}")
        return validation
    
    def get_category_info(self) -> Dict[str, Dict]:
        """Get information about all music categories"""
        return {
            category: {
                "description": config["description"],
                "keywords": config["keywords"][:5],  # Top 5 keywords
                "default_volume": config["volume"]
            }
            for category, config in self.categories.items()
        }
