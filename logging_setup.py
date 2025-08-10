import logging
import os
from logging.handlers import RotatingFileHandler
from config_loader import get_config

logger = logging.getLogger(__name__)
config = get_config()

def setup_logging():
    # Ensure this function is called only once
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

    # File Handler
    file_handler = RotatingFileHandler(
        config.logging.log_file,
        maxBytes=config.logging.max_bytes,
        backupCount=config.logging.backup_count
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Stream Handler (console output)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    # --- Audit Log Handler ---
    if config.logging.enable_audit_log:
        audit_logger = logging.getLogger('audit')
        audit_logger.setLevel(config.logging.audit_log_level)
        audit_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        audit_file_handler = RotatingFileHandler(
            config.logging.audit_log_file,
            maxBytes=config.logging.max_bytes,
            backupCount=config.logging.backup_count
        )
        audit_file_handler.setFormatter(audit_formatter)
        audit_logger.addHandler(audit_file_handler)
        audit_logger.propagate = False # Prevent audit logs from going to root_logger
        logger.info(f"Audit logging enabled to {config.logging.audit_log_file}")

    # Prevent duplicate logs from imported modules
    root_logger.propagate = False

def get_logger(name):
    return logging.getLogger(name)

# Setup logging when the module is imported
setup_logging()

def get_audit_logger():
    """
    // [TASK]: Get the dedicated audit logger
    // [GOAL]: Provide a separate logger for security audit events
    """
    return logging.getLogger('audit')