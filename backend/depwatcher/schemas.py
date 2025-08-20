from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PatchCandidate(BaseModel):
    id: str # Unique ID for the candidate
    kind: str # "pip" | "model" | "asset" | "node"
    env: Optional[str] = None # e.g., "venv311", ".venv312-lama"
    name: str
    fromVersion: Optional[str] = None
    toVersion: str
    source: Optional[str] = None # e.g., "pypi", "huggingface", "local"
    downloadSizeMB: Optional[float] = None
    workdir: Optional[str] = None # For node projects: directory containing package.json

class PatchPlan(BaseModel):
    id: str # Unique ID for the patch plan
    items: List[PatchCandidate]
    mode: str # "dry-run" | "apply"
    createdBy: str
    createdAt: datetime
    status: str = "pending" # "pending" | "approved" | "rejected" | "applied" | "failed" | "rolled_back"
    # Add more fields as needed, e.g., approval_date, applied_date, logs_url
