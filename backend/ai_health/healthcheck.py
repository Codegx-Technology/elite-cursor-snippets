import logging
import time
from typing import Dict, Any, List, Tuple
import sqlite3
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# In-memory store for metrics (replace with SQLite or proper DB in production)
# Structure: { (provider, model, tag): [ {timestamp, ok, latency_ms, score}, ... ] }
_metrics_store: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = {}

# SQLite setup (placeholder for a more robust implementation)
DB_PATH = "metrics.db"

def _init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_metrics (
            provider TEXT,
            model TEXT,
            tag TEXT,
            timestamp TEXT,
            ok INTEGER,
            latency_ms REAL,
            score REAL
        );
    """)
    conn.commit()
    conn.close()

_init_db() # Initialize DB on module load

def score_inference(result: Dict[str, Any]) -> float:
    """
    Scores the inference result (0.0 to 1.0).
    This is a pluggable function, basic implementation: non-empty, within SLA.
    """
    # Example: Check if 'error' key exists or if result is empty
    if result.get("error") or not result.get("content"):
        return 0.0 # Failed inference
    
    # Example: Check latency against a hypothetical SLA (e.g., 500ms)
    latency_ms = result.get("latency_ms", 0)
    if latency_ms > 500:
        return 0.5 # Partial score for slow inference
    
    return 1.0 # Healthy inference

def record_metric(provider: str, model: str, tag: str, ok: bool, latency_ms: float, score: float):
    """
    Records a single inference metric.
    """
    timestamp = datetime.now().isoformat()
    metric = {
        "timestamp": timestamp,
        "ok": 1 if ok else 0,
        "latency_ms": latency_ms,
        "score": score
    }
    
    # Store in-memory (for quick access in aggregate)
    key = (provider, model, tag)
    if key not in _metrics_store:
        _metrics_store[key] = []
    _metrics_store[key].append(metric)

    # Store in SQLite
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO model_metrics (provider, model, tag, timestamp, ok, latency_ms, score) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (provider, model, tag, timestamp, metric["ok"], metric["latency_ms"], metric["score"])
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to record metric to DB: {e}")

def aggregate(provider: str, model: str, tag: str, last_n: int = 200) -> Dict[str, Any]:
    """
    Aggregates metrics for a given model tag over the last_n inferences.
    """
    key = (provider, model, tag)
    metrics = _metrics_store.get(key, [])
    
    # Filter to last_n (or fewer if not enough)
    recent_metrics = metrics[-last_n:]

    if not recent_metrics:
        return {"error_rate": 1.0, "p50": 0.0, "score": 0.0, "count": 0}

    total_count = len(recent_metrics)
    error_count = sum(1 for m in recent_metrics if not m["ok"])
    latencies = [m["latency_ms"] for m in recent_metrics if m["ok"]]
    scores = [m["score"] for m in recent_metrics]

    error_rate = error_count / total_count
    p50_latency = sorted(latencies)[len(latencies) // 2] if latencies else 0.0
    avg_score = sum(scores) / total_count

    return {
        "error_rate": round(error_rate, 4),
        "p50_latency_ms": round(p50_latency, 2),
        "avg_score": round(avg_score, 4),
        "count": total_count
    }