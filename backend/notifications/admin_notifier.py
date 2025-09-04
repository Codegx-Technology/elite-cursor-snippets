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
    
    # Send the email using the existing send_admin_notification (which uses SMTP)
    send_admin_notification(subject=subject, body=message, logger=logger)

def alert_admin(message: str):
    """
    Sends an email alert to the admin using SMTP via send_admin_notification.
    """
    subject = "🚨 Dependency Watcher Alert"
    # Use the SMTP-based notifier; if SMTP isn't configured, it will log and skip.
    logger.info(f"Sending admin alert via SMTP: {subject}")
    send_admin_notification(
        subject=subject,
        body=message,
        logger=logger
    )
