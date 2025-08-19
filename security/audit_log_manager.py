import logging
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from auth.user_models import AuditLog # Assuming AuditLog model is defined here
import hashlib # For hashing log entries

logger = logging.getLogger(__name__)

class AuditLogManager:
    """
    // [TASK]: Centralize and enhance security audit logging
    // [GOAL]: Provide a consistent and robust mechanism for recording security-related events
    // [ELITE_CURSOR_SNIPPET]: securitycheck
    """
    def __init__(self):
        pass # No specific initialization needed for now

    def _get_last_log_hash(self, db: Session) -> str:
        """Retrieves the hash of the last audit log entry for chaining."""
        last_log = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).first()
        return last_log.current_hash if last_log else "0" * 64 # Default hash if no previous logs

    def log_event(self, db: Session, event_type: str, message: str, user_id: Optional[int] = None, tenant_id: Optional[int] = None, ip_address: Optional[str] = None, event_details: Optional[Dict[str, Any]] = None):
        """
        Records a security audit event.
        
        Args:
            db (Session): Database session.
            event_type (str): Standardized type of the event (e.g., "USER_LOGIN_SUCCESS").
            message (str): Detailed message describing the event.
            user_id (Optional[int]): ID of the user associated with the event.
            tenant_id (Optional[int]): ID of the tenant associated with the event.
            ip_address (Optional[str]): IP address from which the event originated.
            event_details (Optional[Dict[str, Any]]): Additional structured details about the event.
        """
        try:
            previous_hash = self._get_last_log_hash(db)
            
            log_entry = AuditLog(
                timestamp=datetime.utcnow(),
                user_id=user_id,
                event_type=event_type,
                message=message,
                previous_hash=previous_hash,
                # current_hash will be set by set_hash method
            )
            
            log_entry.set_hash(previous_hash) # Calculate and set current_hash
            
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)
            
            logger.info(f"AUDIT_LOG: Event='{event_type}', User={user_id}, Tenant={tenant_id}, IP={ip_address}, Message='{message}'")
            # For external audit systems, you might send this log_entry to a SIEM here.
        except Exception as e:
            logger.error(f"Failed to record audit log event '{event_type}': {e}", exc_info=True)

# Standardized Audit Event Types
class AuditEventType:
    USER_LOGIN_SUCCESS = "USER_LOGIN_SUCCESS"
    USER_LOGIN_FAILURE = "USER_LOGIN_FAILURE"
    USER_REGISTER = "USER_REGISTER"
    USER_PROFILE_UPDATE = "USER_PROFILE_UPDATE"
    USER_DATA_EXPORT = "USER_DATA_EXPORT"
    USER_DATA_DELETE = "USER_DATA_DELETE"
    API_ACCESS = "API_ACCESS"
    BILLING_LIMIT_EXCEEDED = "BILLING_LIMIT_EXCEEDED"
    CHAOS_INJECTED = "CHAOS_INJECTED"
    WEBHOOK_RECEIVED = "WEBHOOK_RECEIVED"
    WEBHOOK_SIGNATURE_MISMATCH = "WEBHOOK_SIGNATURE_MISMATCH"
    MODEL_VERSION_DETECTED = "MODEL_VERSION_DETECTED"
    VOICE_VERSION_DETECTED = "VOICE_VERSION_DETECTED"
    # Add more as needed

audit_log_manager = AuditLogManager()