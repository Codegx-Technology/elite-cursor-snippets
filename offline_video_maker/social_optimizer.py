#!/usr/bin/env python3
"""
Shujaa Studio - Social Optimizer

Generates platform-ready titles, descriptions, and hashtags from a story prompt
with Kenya-first context patterns.
"""
from __future__ import annotations
import re
from typing import Dict, List

PLATFORMS = ["tiktok", "instagram", "youtube_shorts", "facebook", "whatsapp"]

HASHTAG_BANK = {
    "kenya": ["#Kenya", "#AfricanTech", "#MadeInKenya", "#Nairobi", "#Kisumu", "#Mombasa"],
    "education": ["#Education", "#STEM", "#GirlsInTech", "#Scholarship", "#Coding"],
    "community": ["#Community", "#Impact", "#Youth", "#Innovation", "#AfricaRising"],
    "water": ["#CleanWater", "#SolarTech", "#Sustainability", "#ClimateAction"],
    "tech": ["#AI", "#Software", "#Engineering", "#TechForGood"],
}

PLATFORM_LIMITS = {
    "tiktok": {"title": 150, "desc": 2200, "hashtags": 30},
    "instagram": {"title": 150, "desc": 2200, "hashtags": 30},
    "youtube_shorts": {"title": 100, "desc": 5000, "hashtags": 15},
    "facebook": {"title": 200, "desc": 63206, "hashtags": 20},
    "whatsapp": {"title": 140, "desc": 1024, "hashtags": 10},
}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def _infer_topics(prompt: str) -> List[str]:
    topics = []
    low = prompt.lower()
    if any(k in low for k in ["kenya", "nairobi", "kisumu", "mombasa", "turkana", "maasai", "kibera"]):
        topics.append("kenya")
    if any(k in low for k in ["school", "education", "university", "scholarship", "engineer"]):
        topics.append("education")
    if any(k in low for k in ["community", "village", "orphan", "youth", "elders"]):
        topics.append("community")
    if any(k in low for k in ["water", "purification", "borehole", "solar"]):
        topics.append("water")
    if any(k in low for k in ["tech", "software", "coding", "ai", "engineer"]):
        topics.append("tech")
    return topics or ["kenya", "community"]


def generate_metadata(prompt: str, platform: str = "tiktok") -> Dict:
    platform = platform.lower()
    if platform not in PLATFORMS:
        platform = "tiktok"

    limits = PLATFORM_LIMITS[platform]
    prompt_clean = _clean(prompt)

    # Title
    title_base = f"{prompt_clean.split('.')[0]}" if "." in prompt_clean else prompt_clean
    title = _truncate(title_base, limits["title"])  # keep it punchy

    # Description
    desc_lines = [
        prompt_clean,
        "",
        "Watch till the end and share to inspire someone today.",
        "Built with Shujaa Studio — African AI Video Generation.",
    ]
    desc = _truncate("\n".join(desc_lines), limits["desc"])

    # Hashtags
    topics = _infer_topics(prompt)
    tags: List[str] = []
    for t in topics:
        tags.extend(HASHTAG_BANK.get(t, []))
    # Ensure uniqueness and limit count
    seen = set()
    hashtags = []
    for tag in tags:
        if tag not in seen:
            hashtags.append(tag)
            seen.add(tag)
        if len(hashtags) >= limits["hashtags"]:
            break

    return {
        "platform": platform,
        "title": title,
        "description": desc,
        "hashtags": hashtags,
    }


def generate_all(prompt: str) -> Dict[str, Dict]:
    return {p: generate_metadata(prompt, p) for p in PLATFORMS}
