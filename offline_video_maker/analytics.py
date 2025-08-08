#!/usr/bin/env python3
"""
Shujaa Studio - Analytics & Performance Monitoring

Lightweight analytics for generation timing, error rates, and resource usage.
Safe defaults: logs to JSONL in ./debug_logs/shujaa_analytics.jsonl
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Callable

LOG_DIR = Path("debug_logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "shujaa_analytics.jsonl"


def log_event(event: Dict[str, Any]) -> None:
    try:
        event = {**event, "ts": time.time()}
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        # Never fail main pipeline due to analytics
        pass


def timed(name: str) -> Callable:
    """Decorator to time functions and log duration."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start
                log_event({"type": "timing", "name": name, "duration_s": round(duration, 3)})
                return result
            except Exception as e:
                duration = time.time() - start
                log_event({
                    "type": "error", "name": name, "duration_s": round(duration, 3), "error": str(e)
                })
                raise
        return wrapper
    return decorator


def mark_stage(stage: str, extra: Dict[str, Any] | None = None) -> None:
    payload = {"type": "stage", "stage": stage}
    if extra:
        payload.update(extra)
    log_event(payload)
