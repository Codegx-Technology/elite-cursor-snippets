import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

from config_loader import get_config

# Optional imports to avoid circular dependencies during tools/standalone scripts
try:
    from database import SessionLocal  # Elite Cursor Snippet: db_session_import
    from auth.user_models import AuditLog  # Elite Cursor Snippet: audit_log_model_import
    _DB_AVAILABLE = True
except Exception:
    SessionLocal = None
    AuditLog = None
    _DB_AVAILABLE = False

logger = logging.getLogger(__name__)
config = get_config()

# Global variable to store the hash of the last audit log entry
_last_audit_log_hash = "0" * 64 # Initial hash for the first log entry

class DatabaseAuditHandler(logging.Handler):
    """
    A logging handler that writes audit logs to the database with hash chaining.
    // [TASK]: Implement database logging for audit events
    // [GOAL]: Store audit logs securely with tamper detection
    // [ELITE_CURSOR_SNIPPET]: securitycheck
    """
    def emit(self, record):
        global _last_audit_log_hash
        try:
            if not _DB_AVAILABLE or SessionLocal is None or AuditLog is None:
                # Gracefully skip if DB layer is unavailable
                return
            db = SessionLocal()
            try:
                # Get the last audit log entry to calculate the previous hash
                last_log = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
                previous_hash = last_log.current_hash if last_log else "0" * 64

                # Create new AuditLog entry
                audit_log = AuditLog(
                    timestamp=datetime.fromtimestamp(record.created),
                    user_id=getattr(record, 'user_id', None), # Custom attribute for user ID
                    event_type=record.levelname, # Use log level as event type for simplicity
                    message=self.format(record)
                )
                audit_log.set_hash(previous_hash) # Calculate and set hashes

                db.add(audit_log)
                db.commit()
                _last_audit_log_hash = audit_log.current_hash # Update global hash
            except Exception as e:
                db.rollback()
                logger.error(f"Failed to write audit log to database: {e}", exc_info=True)
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Failed to get database session for audit logging: {e}", exc_info=True)


def setup_logging():
    if hasattr(setup_logging, '_has_run'):
        return
    setup_logging._has_run = True

    # Create logs directory if it doesn't exist
    logs_dir = os.path.dirname(config.logging.log_file)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(config.logging.level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler for general logs
    file_handler = RotatingFileHandler(
        config.logging.log_file,
        maxBytes=config.logging.max_bytes,
        backupCount=config.logging.backup_count
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    # --- Audit Log Handler ---
    if getattr(config, 'logging', None) and getattr(config.logging, 'enable_audit_log', False):
        audit_logger = logging.getLogger('audit')
        audit_logger.setLevel(config.logging.audit_log_level)
        audit_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Use DatabaseAuditHandler only if DB layer is available
        if _DB_AVAILABLE:
            db_audit_handler = DatabaseAuditHandler()
            db_audit_handler.setFormatter(audit_formatter)
            audit_logger.addHandler(db_audit_handler)
            audit_logger.propagate = False # Prevent audit logs from going to root_logger
            logger.info(f"Audit logging enabled to database.")
        else:
            logger.info("Audit logging disabled (database unavailable during setup).")

    # Prevent duplicate logs from imported modules
    root_logger.propagate = False

def get_logger(name):
    return logging.getLogger(name)

# Do not auto-setup on import to avoid circular import side-effects
# Enable auto-setup only when explicitly requested via env flag
if os.environ.get("SHUJAA_AUTO_LOG_SETUP", "0") == "1":
    setup_logging()

def get_audit_logger():
    """
    // [TASK]: Get the dedicated audit logger
    // [GOAL]: Provide a separate logger for security audit events
    """
    return logging.getLogger('audit')