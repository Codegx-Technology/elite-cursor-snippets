#!/usr/bin/env python3
"""
🎬 Video Effects Engine - Professional Polish for InVideo Competition
Text overlays, transitions, and multi-aspect ratio support
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

try:
    from moviepy.editor import *
    from moviepy.video.fx import resize, fadeout, fadein

    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoEffects:
    """Professional video effects for InVideo competition"""

    def __init__(self):
        self.aspect_ratios = {
            "landscape": (16, 9),  # YouTube, Facebook
            "portrait": (9, 16),  # TikTok, Instagram Stories
            "square": (1, 1),  # Instagram Posts
            "cinema": (21, 9),  # Ultra-wide
        }

        self.standard_sizes = {
            "landscape": (1920, 1080),
            "portrait": (1080, 1920),
            "square": (1080, 1080),
            "cinema": (2560, 1080),
        }

        logger.info("[EFFECTS] Video effects engine initialized")

    def add_text_overlay(
        self, video_clip, text: str, position: str = "bottom", style: str = "modern"
    ) -> object:
        """Add professional text overlay to video"""

        if not MOVIEPY_AVAILABLE:
            logger.warning("[EFFECTS] MoviePy not available, skipping text overlay")
            return video_clip

        try:
            # Text styling based on style
            text_configs = {
                "modern": {
                    "fontsize": 72,
                    "color": "white",
                    "stroke_color": "black",
                    "stroke_width": 3,
                    "font": "Arial-Bold",
                },
                "elegant": {
                    "fontsize": 64,
                    "color": "#f0f0f0",
                    "stroke_color": "#333",
                    "stroke_width": 2,
                    "font": "Times-Roman",
                },
                "kenya_pride": {
                    "fontsize": 68,
                    "color": "#FFD700",  # Gold
                    "stroke_color": "#C41E3A",  # Kenya red
                    "stroke_width": 4,
                    "font": "Arial-Bold",
                },
            }

            config = text_configs.get(style, text_configs["modern"])

            # Position mapping
            position_map = {
                "top": ("center", "top"),
                "bottom": ("center", "bottom"),
                "center": ("center", "center"),
                "bottom_left": ("left", "bottom"),
                "top_right": ("right", "top"),
            }

            pos = position_map.get(position, ("center", "bottom"))

            # Create text clip
            text_clip = (
                TextClip(
                    text,
                    fontsize=config["fontsize"],
                    color=config["color"],
                    stroke_color=config["stroke_color"],
                    stroke_width=config["stroke_width"],
                    font=config.get("font", "Arial-Bold"),
                )
                .set_duration(video_clip.duration)
                .set_position(pos)
            )

            # Add fade in/out
            text_clip = text_clip.fadein(0.5).fadeout(0.5)

            # Composite with video
            final_clip = CompositeVideoClip([video_clip, text_clip])

            logger.info(f"[EFFECTS] Added text overlay: '{text[:30]}...'")
            return final_clip

        except Exception as e:
            logger.error(f"[EFFECTS] Text overlay failed: {e}")
            return video_clip

    def add_scene_transition(
        self, clip1, clip2, transition_type: str = "crossfade", duration: float = 1.0
    ) -> object:
        """Add professional transition between scenes"""

        if not MOVIEPY_AVAILABLE:
            logger.warning(
                "[EFFECTS] MoviePy not available, concatenating without transition"
            )
            return concatenate_videoclips([clip1, clip2])

        try:
            transitions = {
                "crossfade": self._crossfade_transition,
                "slide_left": self._slide_transition,
                "fade_black": self._fade_black_transition,
                "zoom_out": self._zoom_transition,
            }

            transition_func = transitions.get(transition_type, transitions["crossfade"])
            result = transition_func(clip1, clip2, duration)

            logger.info(f"[EFFECTS] Added {transition_type} transition ({duration}s)")
            return result

        except Exception as e:
            logger.error(f"[EFFECTS] Transition failed: {e}")
            return concatenate_videoclips([clip1, clip2])

    def _crossfade_transition(self, clip1, clip2, duration: float):
        """Crossfade transition effect"""

        # Fade out first clip
        clip1_faded = clip1.fadeout(duration)

        # Fade in second clip and overlay
        clip2_faded = clip2.fadein(duration).set_start(clip1.duration - duration)

        return CompositeVideoClip([clip1_faded, clip2_faded])

    def _slide_transition(self, clip1, clip2, duration: float):
        """Slide transition effect"""

        w, h = clip1.size

        # Slide clip2 in from right
        clip2_slide = clip2.set_position(
            lambda t: (w * (1 - t / duration), 0) if t < duration else (0, 0)
        )
        clip2_slide = clip2_slide.set_start(clip1.duration - duration)

        return CompositeVideoClip([clip1, clip2_slide])

    def _fade_black_transition(self, clip1, clip2, duration: float):
        """Fade to black transition"""

        # Fade clip1 to black
        clip1_fade = clip1.fadeout(duration / 2)

        # Fade clip2 from black
        clip2_fade = clip2.fadein(duration / 2).set_start(clip1.duration + duration / 2)

        return concatenate_videoclips([clip1_fade, clip2_fade])

    def _zoom_transition(self, clip1, clip2, duration: float):
        """Zoom out transition"""

        # Zoom out clip1
        def zoom_effect(t):
            return 1 + 0.5 * (t / duration) if t < duration else 1.5

        clip1_zoom = clip1.resize(zoom_effect).fadeout(duration / 2)
        clip2_zoom = clip2.fadein(duration / 2).set_start(clip1.duration - duration / 2)

        return CompositeVideoClip([clip1_zoom, clip2_zoom])

    def convert_aspect_ratio(
        self,
        video_clip,
        target_ratio: str = "landscape",
        background_color: Tuple[int, int, int] = (0, 0, 0),
    ) -> object:
        """Convert video to different aspect ratios"""

        if not MOVIEPY_AVAILABLE:
            logger.warning(
                "[EFFECTS] MoviePy not available, skipping aspect conversion"
            )
            return video_clip

        try:
            target_size = self.standard_sizes.get(
                target_ratio, self.standard_sizes["landscape"]
            )
            target_w, target_h = target_size

            # Get current dimensions
            current_w, current_h = video_clip.size
            current_aspect = current_w / current_h
            target_aspect = target_w / target_h

            if abs(current_aspect - target_aspect) < 0.01:
                # Already correct aspect ratio, just resize
                return video_clip.resize(target_size)

            # Determine if we need to fit width or height
            if current_aspect > target_aspect:
                # Current is wider, fit to height
                new_height = target_h
                new_width = int(new_height * current_aspect)
                resized = video_clip.resize(height=new_height)
            else:
                # Current is taller, fit to width
                new_width = target_w
                new_height = int(new_width / current_aspect)
                resized = video_clip.resize(width=new_width)

            # Create background
            background = ColorClip(
                size=target_size, color=background_color, duration=video_clip.duration
            )

            # Center the resized video
            final_clip = CompositeVideoClip(
                [background, resized.set_position("center")]
            )

            logger.info(
                f"[EFFECTS] Converted to {target_ratio} ({target_w}x{target_h})"
            )
            return final_clip

        except Exception as e:
            logger.error(f"[EFFECTS] Aspect ratio conversion failed: {e}")
            return video_clip

    def create_intro_outro(
        self, duration: float = 3.0, title: str = "Shujaa Studio"
    ) -> Dict[str, object]:
        """Create professional intro and outro clips"""

        if not MOVIEPY_AVAILABLE:
            return {"intro": None, "outro": None}

        try:
            # Intro: Animated text with Kenya colors
            intro_bg = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=duration)

            intro_text = (
                TextClip(
                    title,
                    fontsize=96,
                    color="#FFD700",  # Gold
                    stroke_color="#C41E3A",  # Kenya red
                    stroke_width=6,
                    font="Arial-Bold",
                )
                .set_duration(duration)
                .set_position("center")
            )

            # Add fade and scale animation
            intro_text = (
                intro_text.resize(lambda t: 0.5 + 0.5 * (t / duration))
                .fadein(1.0)
                .fadeout(1.0)
            )
            intro = CompositeVideoClip([intro_bg, intro_text])

            # Outro: Thank you message
            outro_bg = ColorClip(
                size=(1920, 1080), color=(20, 20, 20), duration=duration
            )
            outro_text = (
                TextClip(
                    "Thank you for watching!\nShujaa Studio - Kenya First",
                    fontsize=72,
                    color="white",
                    stroke_color="#C41E3A",
                    stroke_width=3,
                    font="Arial-Bold",
                )
                .set_duration(duration)
                .set_position("center")
            )

            outro_text = outro_text.fadein(1.0).fadeout(1.0)
            outro = CompositeVideoClip([outro_bg, outro_text])

            logger.info(f"[EFFECTS] Created intro/outro clips ({duration}s each)")
            return {"intro": intro, "outro": outro}

        except Exception as e:
            logger.error(f"[EFFECTS] Intro/outro creation failed: {e}")
            return {"intro": None, "outro": None}

    def apply_kenya_branding(self, video_clip, watermark: bool = True) -> object:
        """Apply Kenya-first branding to video"""

        if not MOVIEPY_AVAILABLE:
            return video_clip

        try:
            clips = [video_clip]

            if watermark:
                # Add subtle watermark
                watermark_text = (
                    TextClip(
                        "Shujaa Studio",
                        fontsize=32,
                        color="white",
                        stroke_color="black",
                        stroke_width=1,
                        font="Arial",
                    )
                    .set_duration(video_clip.duration)
                    .set_position(("right", "bottom"))
                    .set_opacity(0.7)
                )

                clips.append(watermark_text)

            # Add Kenya flag colors as subtle border
            flag_stripe = ColorClip(
                size=(1920, 20), color=(196, 30, 58), duration=video_clip.duration
            )  # Kenya red
            flag_stripe = flag_stripe.set_position(("center", "bottom")).set_opacity(
                0.8
            )
            clips.append(flag_stripe)

            result = CompositeVideoClip(clips)

            logger.info("[EFFECTS] Applied Kenya branding")
            return result

        except Exception as e:
            logger.error(f"[EFFECTS] Branding failed: {e}")
            return video_clip


# Test function
def test_video_effects():
    """Test video effects functionality"""
    print("🎬 Testing Video Effects Engine...")

    effects = VideoEffects()

    print(f"✅ Aspect ratios available: {list(effects.aspect_ratios.keys())}")
    print(f"✅ Standard sizes: {effects.standard_sizes}")

    if MOVIEPY_AVAILABLE:
        print("✅ MoviePy available - full effects support")
    else:
        print("⚠️ MoviePy not available - limited functionality")

    return effects


if __name__ == "__main__":
    test_video_effects()
