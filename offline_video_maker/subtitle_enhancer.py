#!/usr/bin/env python3
"""
Shujaa Studio - Subtitle Enhancer

Auto-caption formatting, positioning, and burning helper utilities.
Safe: Works with existing SRT/WebVTT produced by Whisper pipelines.
"""
from __future__ import annotations
import os
import subprocess
from pathlib import Path
from typing import Optional, Dict

DEFAULT_STYLE = {
    "font": "Arial",
    "font_size": 42,
    "primary_color": "&H00FFFFFF",  # white
    "outline_color": "&H00000000",  # black
    "outline": 2,
    "shadow": 0,
    "alignment": 2,  # 2 = bottom-center (ASS)
    "margin_v": 60,  # vertical margin from bottom
}


def srt_to_ass(srt_path: str | Path, ass_out: str | Path, style: Dict | None = None) -> str:
    """Convert SRT to ASS with styling using ffmpeg filter_complex.
    Returns the ASS file path.
    """
    srt_path = str(srt_path)
    ass_out = str(ass_out)
    style = {**DEFAULT_STYLE, **(style or {})}

    # Build ASS style via ffmpeg drawtext is complex; instead, leverage ffmpeg `-i srt -c:s ass` conversion.
    # Then prepend a simple [V4+ Styles] template.
    template = f"""[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,{style['font']},{style['font_size']},{style['primary_color']},&H000000FF,{style['outline_color']},&H00000000,0,0,0,0,100,100,0,0,1,{style['outline']},{style['shadow']},{style['alignment']},20,20,{style['margin_v']},1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"""

    Path(ass_out).parent.mkdir(parents=True, exist_ok=True)

    # Use ffmpeg to convert SRT -> ASS (without style), then we'll merge templates
    tmp_ass = str(Path(ass_out).with_suffix(".tmp.ass"))
    cmd = [
        "ffmpeg", "-y",
        "-i", srt_path,
        "-c:s", "ass",
        tmp_ass,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(tmp_ass, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        with open(ass_out, "w", encoding="utf-8") as f:
            f.write(template + content.split("[Events]\nFormat:")[-1])
    finally:
        try:
            os.remove(tmp_ass)
        except OSError:
            pass

    return ass_out


def burn_subtitles(video_in: str | Path, ass_subs: str | Path, video_out: str | Path) -> str:
    """Burn ASS subtitles into a video using ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_in),
        "-vf", f"ass={str(ass_subs)}",
        "-c:a", "copy",
        str(video_out),
    ]
    subprocess.run(cmd, check=False)
    return str(video_out)


def auto_position(style_overrides: Optional[Dict] = None) -> Dict:
    """Return a style dict for bottom-center mobile friendly captions."""
    return {**DEFAULT_STYLE, **(style_overrides or {})}
