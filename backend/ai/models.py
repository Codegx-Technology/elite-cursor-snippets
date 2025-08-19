from sqlalchemy import Column, Integer, String, DateTime
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