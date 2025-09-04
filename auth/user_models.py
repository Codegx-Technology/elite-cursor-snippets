from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import hashlib # Elite Cursor Snippet: hashlib_import

from database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    plan = Column(String, default="free")
    # New branding fields
    theme_name = Column(String, default="default")
    primary_color = Column(String, default="#667eea") # Example default color
    logo_url = Column(String, nullable=True)
    custom_domain = Column(String, unique=True, nullable=True)
    tls_status = Column(String, default="pending") # pending, active, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="tenant")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant", back_populates="users")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Nullable for system events
    event_type = Column(String, index=True) # e.g., "login", "video_gen", "plan_change"
    message = Column(Text) # Detailed log message
    previous_hash = Column(String, default="0" * 64) # Hash of the previous log entry for chaining
    current_hash = Column(String, unique=True) # Hash of this log entry

    user = relationship("User") # Relationship to User model

    def calculate_hash(self, previous_hash: str) -> str:
        # // [TASK]: Calculate SHA256 hash for audit log entry
        # // [GOAL]: Ensure tamper detection for audit logs
        # // [ELITE_CURSOR_SNIPPET]: securitycheck
        data = f"{self.timestamp}{self.user_id}{self.event_type}{self.message}{previous_hash}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def set_hash(self, previous_hash: str):
        self.previous_hash = previous_hash
        self.current_hash = self.calculate_hash(previous_hash)

class Consent(Base):
    __tablename__ = "consents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    consent_type = Column(String, index=True) # e.g., "marketing_email", "data_analytics", "pii_sharing"
    is_granted = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

class WebhookAttempt(Base):
    __tablename__ = "webhook_attempts"

    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(String, index=True) # Unique ID for the webhook event
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    payload = Column(Text, nullable=False)
    status = Column(String, default="pending") # e.g., "pending", "success", "failed"
    retries = Column(Integer, default=0)
    last_attempt_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    next_attempt_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)

    tenant = relationship("Tenant")
