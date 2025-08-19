from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from auth.user_models import Base # Assuming Base is defined here or in database.py

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    version = Column(String(255), index=True)
    checksum = Column(String(255), nullable=True)
    released_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ModelVersion(name='{self.name}', version='{self.version}')>"

class VoiceVersion(Base):
    __tablename__ = "voice_versions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    version = Column(String(255), index=True)
    released_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<VoiceVersion(name='{self.name}', version='{self.version}')>"

class UsageCost(Base):
    __tablename__ = "usage_costs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(36), index=True, nullable=False) # UUID
    user_id = Column(String(36), index=True, nullable=False) # UUID
    tier_code = Column(String(50), nullable=False)
    task_type = Column(String(100), nullable=False)
    model_name = Column(String(255), nullable=True)
    model_version = Column(String(255), nullable=True)
    provider = Column(String(100), nullable=False)
    metric = Column(String(50), nullable=False) # e.g., chars, tokens, gpu_mins
    amount = Column(Float, nullable=False)
    estimated_cost_usd = Column(Float, nullable=False)
    actual_cost_usd = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UsageCost(job_id='{self.job_id}', user_id='{self.user_id}', cost='{self.estimated_cost_usd}')>"