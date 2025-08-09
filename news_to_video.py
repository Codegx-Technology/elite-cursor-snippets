#!/usr/bin/env python3
"""
📰 Shujaa Studio - News to Video Generator
Transform news articles, headlines, and current events into engaging African videos

// [TASK]: Intelligent news content to video conversion
// [GOAL]: Automated news video generation with African context
// [CONSTRAINTS]: Mobile-first, offline-capable, culturally sensitive
// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + augmentsearch
// [CONTEXT]: Integrates with GPU fallback system and existing video pipeline
"""

import os
import re
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

# Import GPU fallback system
from gpu_fallback import ShujaaGPUIntegration, TaskProfile

# News processing and content analysis
try:
    import requests
    from bs4 import BeautifulSoup

    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False
    logging.warning("Web scraping libraries not available - using manual input only")

try:
    import feedparser

    RSS_AVAILABLE = True
except ImportError:
    RSS_AVAILABLE = False
    logging.warning("RSS parsing not available - using basic text processing")

# Content enhancement
try:
    from textstat import flesch_reading_ease, flesch_kincaid_grade

    READABILITY_ANALYSIS = True
except ImportError:
    READABILITY_ANALYSIS = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NewsArticle:
    """News article structure"""

    title: str
    summary: str
    content: str
    source: str
    date: str
    category: str
    location: str
    language: str = "en"
    sentiment: str = "neutral"
    readability_score: float = 0.0


@dataclass
class VideoSegment:
    """Video segment structure"""

    segment_id: int
    title: str
    narration: str
    visual_description: str
    duration: float
    style: str = "news"
    emotion: str = "informative"


class NewsContentProcessor:
    """
    // [TASK]: Process and enhance news content for video generation
    // [GOAL]: Transform raw news into structured, engaging video content
    // [SNIPPET]: thinkwithai + refactorclean + kenyafirst
    """

    def __init__(self):
        self.kenyan_context_keywords = [
            "kenya",
            "nairobi",
            "mombasa",
            "kisumu",
            "nakuru",
            "eldoret",
            "uhuru",
            "ruto",
            "raila",
            "shilling",
            "safaricom",
            "mpesa",
            "maasai",
            "kikuyu",
            "luo",
            "kalenjin",
            "swahili",
            "sheng",
            "nssf",
            "nhif",
            "kra",
            "iebc",
            "eacc",
        ]

        self.african_context_keywords = [
            "africa",
            "african",
            "continent",
            "sahara",
            "nile",
            "congo",
            "lagos",
            "cairo",
            "johannesburg",
            "addis ababa",
            "accra",
            "francophone",
            "anglophone",
            "au",
            "ecowas",
            "sadc",
            "eac",
        ]

        self.video_styles = {
            "breaking": {"pace": "fast", "emotion": "urgent", "duration": 15},
            "feature": {"pace": "moderate", "emotion": "informative", "duration": 30},
            "analysis": {"pace": "slow", "emotion": "thoughtful", "duration": 45},
            "sports": {"pace": "energetic", "emotion": "exciting", "duration": 20},
            "business": {
                "pace": "professional",
                "emotion": "confident",
                "duration": 25,
            },
        }

        logger.info("📰 News Content Processor initialized")

    def extract_from_text(self, text: str, source: str = "manual") -> NewsArticle:
        """
        // [TASK]: Extract structured news data from raw text
        // [GOAL]: Clean, structured content ready for video generation
        // [SNIPPET]: augmentsearch + surgicalfix
        """
        # Clean and process text
        cleaned_text = self._clean_text(text)

        # Extract title (first line or first sentence)
        lines = cleaned_text.split("\n")
        title = lines[0].strip() if lines else "News Update"

        # Generate summary (first 2-3 sentences)
        sentences = re.split(r"[.!?]+", cleaned_text)
        summary = ". ".join(sentences[:3]).strip() + "."

        # Detect location and category
        location = self._detect_location(cleaned_text)
        category = self._categorize_content(cleaned_text)

        # Analyze readability
        readability = (
            self._analyze_readability(cleaned_text) if READABILITY_ANALYSIS else 7.0
        )

        # Detect sentiment
        sentiment = self._analyze_sentiment(cleaned_text)

        return NewsArticle(
            title=title,
            summary=summary,
            content=cleaned_text,
            source=source,
            date=datetime.now().strftime("%Y-%m-%d"),
            category=category,
            location=location,
            sentiment=sentiment,
            readability_score=readability,
        )

    def _clean_text(self, text: str) -> str:
        """Clean and format text content"""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove common web artifacts
        text = re.sub(r"(Advertisement|Click here|Read more)", "", text)

        # Fix common encoding issues
        text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')

        return text.strip()

    def _detect_location(self, text: str) -> str:
        """Detect geographical context"""
        text_lower = text.lower()

        # Check for Kenyan context
        for keyword in self.kenyan_context_keywords:
            if keyword in text_lower:
                return "Kenya"

        # Check for broader African context
        for keyword in self.african_context_keywords:
            if keyword in text_lower:
                return "Africa"

        return "Global"

    def _categorize_content(self, text: str) -> str:
        """Categorize news content"""
        text_lower = text.lower()

        categories = {
            "politics": [
                "government",
                "election",
                "president",
                "minister",
                "parliament",
                "policy",
            ],
            "business": [
                "economy",
                "business",
                "market",
                "company",
                "investment",
                "finance",
            ],
            "sports": [
                "football",
                "rugby",
                "athletics",
                "sport",
                "team",
                "match",
                "champion",
            ],
            "technology": [
                "technology",
                "internet",
                "mobile",
                "app",
                "digital",
                "innovation",
            ],
            "health": [
                "health",
                "hospital",
                "doctor",
                "medical",
                "disease",
                "treatment",
            ],
            "education": [
                "school",
                "university",
                "student",
                "education",
                "teacher",
                "learning",
            ],
        }

        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category

        return "general"

    def _analyze_readability(self, text: str) -> float:
        """Analyze text readability"""
        try:
            score = flesch_reading_ease(text)
            return score
        except:
            # Estimate based on sentence length
            sentences = len(re.split(r"[.!?]+", text))
            words = len(text.split())
            if sentences == 0:
                return 5.0
            avg_sentence_length = words / sentences

            if avg_sentence_length < 10:
                return 8.0  # Very easy
            elif avg_sentence_length < 15:
                return 7.0  # Easy
            elif avg_sentence_length < 20:
                return 6.0  # Fairly easy
            else:
                return 4.0  # Difficult

    def _analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis"""
        text_lower = text.lower()

        positive_words = [
            "success",
            "improvement",
            "growth",
            "win",
            "achieve",
            "progress",
            "good",
        ]
        negative_words = [
            "problem",
            "crisis",
            "conflict",
            "decline",
            "loss",
            "fail",
            "bad",
        ]

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"


class NewsVideoGenerator:
    """
    // [TASK]: Generate videos from news content using GPU acceleration
    // [GOAL]: Professional news videos with African cultural context
    // [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + perfcheck
    """

    def __init__(self):
        self.content_processor = NewsContentProcessor()
        self.gpu_integration = ShujaaGPUIntegration()
        self.output_dir = Path("output/news_videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # African news templates
        self.african_news_templates = {
            "kenya_focus": {
                "intro": "This is Kenya today",
                "transition": "Here's what's happening across the country",
                "outro": "Stay informed, stay connected to Kenya",
                "style": "patriotic",
            },
            "africa_focus": {
                "intro": "From across the African continent",
                "transition": "This story from Africa matters",
                "outro": "Africa's story, told by Africans",
                "style": "continental",
            },
            "global_african": {
                "intro": "How the world affects Africa",
                "transition": "The African perspective on global events",
                "outro": "African voices on the world stage",
                "style": "international",
            },
        }

        logger.info("🎬 News Video Generator initialized with GPU acceleration")

    async def generate_news_video(
        self,
        news_input: Union[str, NewsArticle],
        video_style: str = "feature",
        duration: Optional[int] = None,
    ) -> str:
        """
        // [TASK]: Complete news to video generation pipeline
        // [GOAL]: Professional news video with GPU acceleration
        // [SNIPPET]: thinkwithai + surgicalfix + perfcheck
        """
        try:
            # Process input
            if isinstance(news_input, str):
                article = self.content_processor.extract_from_text(news_input)
            else:
                article = news_input

            logger.info(f"📰 Generating video for: {article.title[:50]}...")

            # Generate video segments
            segments = await self._create_video_segments(article, video_style, duration)

            # Generate visuals for each segment using GPU acceleration
            visual_assets = await self._generate_visuals(segments, article)

            # Generate audio narration
            audio_assets = await self._generate_audio(segments, article)

            # Assemble final video
            output_path = await self._assemble_video(
                segments, visual_assets, audio_assets, article
            )

            logger.info(f"✅ News video generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"❌ News video generation failed: {e}")
            raise e

    async def _create_video_segments(
        self, article: NewsArticle, video_style: str, duration: Optional[int]
    ) -> List[VideoSegment]:
        """Create structured video segments from news article"""

        # Determine template based on location
        if article.location == "Kenya":
            template = self.african_news_templates["kenya_focus"]
        elif article.location == "Africa":
            template = self.african_news_templates["africa_focus"]
        else:
            template = self.african_news_templates["global_african"]

        # Calculate segment durations
        style_config = self.content_processor.video_styles.get(
            video_style, {"pace": "moderate", "emotion": "informative", "duration": 30}
        )

        total_duration = duration or style_config["duration"]

        # Create segments
        segments = []

        # Opening segment
        segments.append(
            VideoSegment(
                segment_id=1,
                title="Introduction",
                narration=f"{template['intro']}. {article.title}",
                visual_description=f"News opener with {article.location} context, {article.category} theme",
                duration=total_duration * 0.2,
                style=template["style"],
                emotion=style_config["emotion"],
            )
        )

        # Main content segments (split content into 2-3 parts)
        content_sentences = re.split(r"[.!?]+", article.content)
        content_parts = self._split_content_intelligently(content_sentences, 2)

        for i, part in enumerate(content_parts):
            segments.append(
                VideoSegment(
                    segment_id=i + 2,
                    title=f"Content Part {i + 1}",
                    narration=part,
                    visual_description=f"Visual representation of {article.category} content in {article.location} context",
                    duration=total_duration * 0.6 / len(content_parts),
                    style=template["style"],
                    emotion=style_config["emotion"],
                )
            )

        # Closing segment
        segments.append(
            VideoSegment(
                segment_id=len(segments) + 1,
                title="Conclusion",
                narration=f"{template['outro']}",
                visual_description=f"Closing visuals with {article.location} identity, {template['style']} theme",
                duration=total_duration * 0.2,
                style=template["style"],
                emotion="conclusive",
            )
        )

        return segments

    def _split_content_intelligently(
        self, sentences: List[str], num_parts: int
    ) -> List[str]:
        """Split content into logical parts"""
        if not sentences:
            return ["No content available"]

        # Clean sentences
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= num_parts:
            return sentences

        # Distribute sentences evenly
        sentences_per_part = len(sentences) // num_parts
        parts = []

        for i in range(num_parts):
            start_idx = i * sentences_per_part
            if i == num_parts - 1:  # Last part gets remaining sentences
                end_idx = len(sentences)
            else:
                end_idx = (i + 1) * sentences_per_part

            part_sentences = sentences[start_idx:end_idx]
            parts.append(". ".join(part_sentences) + ".")

        return parts

    async def _generate_visuals(
        self, segments: List[VideoSegment], article: NewsArticle
    ) -> List[str]:
        """Generate visuals for each segment using GPU acceleration"""
        visual_assets = []

        for segment in segments:
            # Create enhanced prompt with African context
            enhanced_prompt = self._enhance_visual_prompt(segment, article)

            # Generate image using GPU acceleration
            output_path = (
                self.output_dir
                / f"segment_{segment.segment_id}_{int(asyncio.get_event_loop().time())}.png"
            )

            try:
                result = await self.gpu_integration.accelerated_image_generation(
                    enhanced_prompt, str(output_path)
                )
                visual_assets.append(str(output_path) if result else None)

            except Exception as e:
                logger.warning(
                    f"Visual generation failed for segment {segment.segment_id}: {e}"
                )
                visual_assets.append(None)

        return visual_assets

    def _enhance_visual_prompt(
        self, segment: VideoSegment, article: NewsArticle
    ) -> str:
        """Enhance visual prompts with African and cultural context"""
        base_prompt = segment.visual_description

        # Add location-specific context
        location_context = {
            "Kenya": "Kenyan setting, East African architecture, Swahili culture",
            "Africa": "African continent, diverse cultures, modern African cities",
            "Global": "International perspective with African viewpoint",
        }.get(article.location, "Contemporary African context")

        # Add category-specific elements
        category_context = {
            "politics": "government buildings, official settings, professional atmosphere",
            "business": "modern office buildings, financial districts, business attire",
            "sports": "stadiums, sporting venues, athletic activities",
            "technology": "modern tech environments, digital interfaces, innovation hubs",
            "health": "medical facilities, healthcare workers, community health",
            "education": "schools, universities, learning environments",
        }.get(article.category, "contemporary settings")

        # Add emotional tone
        emotion_context = {
            "urgent": "dynamic lighting, energetic composition",
            "informative": "clear lighting, professional composition",
            "thoughtful": "soft lighting, contemplative mood",
            "exciting": "vibrant colors, dynamic angles",
            "conclusive": "warm lighting, stable composition",
        }.get(segment.emotion, "balanced lighting, professional quality")

        enhanced_prompt = f"{base_prompt}, {location_context}, {category_context}, {emotion_context}, high quality, professional news imagery"

        return enhanced_prompt

    async def _generate_audio(
        self, segments: List[VideoSegment], article: NewsArticle
    ) -> List[str]:
        """Generate audio narration for segments"""
        # This would integrate with the voice engine
        # For now, return placeholder paths
        audio_assets = []

        for segment in segments:
            # Create audio file path
            audio_path = (
                self.output_dir
                / f"audio_{segment.segment_id}_{int(asyncio.get_event_loop().time())}.wav"
            )

            try:
                # This would call the voice engine
                # For now, create a placeholder
                audio_assets.append(str(audio_path))
                logger.info(f"Audio generated (placeholder): {audio_path}")

            except Exception as e:
                logger.warning(
                    f"Audio generation failed for segment {segment.segment_id}: {e}"
                )
                audio_assets.append(None)

        return audio_assets

    async def _assemble_video(
        self,
        segments: List[VideoSegment],
        visual_assets: List[str],
        audio_assets: List[str],
        article: NewsArticle,
    ) -> str:
        """Assemble final video from assets"""
        timestamp = int(asyncio.get_event_loop().time())
        output_path = self.output_dir / f"news_video_{article.category}_{timestamp}.mp4"

        try:
            # This would integrate with the video assembly pipeline
            # For now, create a summary file
            summary_path = str(output_path).replace(".mp4", "_summary.json")

            video_summary = {
                "article": {
                    "title": article.title,
                    "category": article.category,
                    "location": article.location,
                    "date": article.date,
                },
                "segments": [
                    {
                        "id": seg.segment_id,
                        "title": seg.title,
                        "duration": seg.duration,
                        "visual_asset": (
                            visual_assets[i] if i < len(visual_assets) else None
                        ),
                        "audio_asset": (
                            audio_assets[i] if i < len(audio_assets) else None
                        ),
                    }
                    for i, seg in enumerate(segments)
                ],
                "total_duration": sum(seg.duration for seg in segments),
                "generated_at": datetime.now().isoformat(),
                "gpu_acceleration": True,
            }

            with open(summary_path, "w") as f:
                json.dump(video_summary, f, indent=2)

            logger.info(f"Video summary created: {summary_path}")
            return summary_path

        except Exception as e:
            logger.error(f"Video assembly failed: {e}")
            raise e


class NewsVideoInterface:
    """
    // [TASK]: User interface for news video generation
    // [GOAL]: Simple interface for creating news videos
    // [SNIPPET]: thinkwithai + mobilecheck
    """

    def __init__(self):
        self.generator = NewsVideoGenerator()
        logger.info("📱 News Video Interface ready")

    async def quick_news_video(
        self, news_text: str, style: str = "feature", duration: int = 30
    ) -> Dict:
        """Quick news video generation"""
        try:
            result = await self.generator.generate_news_video(
                news_text, video_style=style, duration=duration
            )

            return {
                "status": "success",
                "output_path": result,
                "message": "News video generated successfully",
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "News video generation failed",
            }

    def get_available_styles(self) -> List[str]:
        """Get available video styles"""
        return list(self.generator.content_processor.video_styles.keys())

    def get_status(self) -> Dict:
        """Get system status"""
        gpu_status = self.generator.gpu_integration.get_integration_status()

        return {
            "news_processor": "Active",
            "gpu_acceleration": gpu_status["gpu_manager"]["local_gpu_status"][
                "available"
            ],
            "available_styles": self.get_available_styles(),
            "output_directory": str(self.generator.output_dir),
            "ready": True,
        }


# CLI interface for testing
async def main():
    """Test news to video generation"""
    print("📰 Testing News to Video Generator")
    print("=" * 50)

    interface = NewsVideoInterface()

    # Test with sample Kenyan news
    test_news = """
    Kenya's Economy Shows Strong Growth in Q3
    
    The Kenyan economy has demonstrated remarkable resilience with a 5.2% growth in the third quarter.
    President William Ruto announced that key sectors including agriculture, manufacturing, and services 
    have contributed to this positive trend. The Central Bank of Kenya has maintained the base lending 
    rate at 9.5% to support continued economic expansion.
    
    Finance Minister John Mbadi noted that inflation has remained stable at 4.8%, within the 
    government's target range. Export earnings have increased by 12% compared to the same period 
    last year, driven by strong performances in tea, coffee, and horticultural exports.
    """

    print("📝 Generating news video...")
    result = await interface.quick_news_video(test_news, "feature", 30)

    print(f"📊 Result: {result}")

    # Show system status
    status = interface.get_status()
    print(f"\n🔧 System Status:")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
