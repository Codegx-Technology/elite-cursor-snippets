import logging
from ai_health_scanner import send_admin_notification
from config_loader import get_config

logger = logging.getLogger(__name__)
cfg = get_config()

def notify_admin(message: str, subject: str):
    """
    Notifies the admin via email and system logs.
    """
    admin_email = cfg.get("ADMIN_EMAIL", "admin@example.com") # Default value for safety
    
    # Log the notification
    logger.info(f"Admin Notification: {subject} - {message}")
    
    # Send the email
    send_admin_notification(subject=subject, body=message, logger=logger)