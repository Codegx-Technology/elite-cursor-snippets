import logging
from ai_health_scanner import send_admin_notification
from config_loader import get_config
from django.core.mail import send_mail # Import Django's send_mail

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
    Sends an email alert to the admin using Django's send_mail.
    This assumes Django's email settings are configured.
    """
    subject = "🚨 Dependency Watcher Alert"
    admin_email = cfg.get("ADMIN_EMAIL", "admin@example.com") # Get admin email from config
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=cfg.get("SMTP_FROM", "noreply@yourdomain.com"), # Assuming SMTP_FROM is in config
            recipient_list=[admin_email],
            fail_silently=False,
        )
        logger.info(f"Django email alert sent to {admin_email} with subject: {subject}")
    except Exception as e:
        logger.error(f"Failed to send Django email alert: {e}")
        # Fallback to send_admin_notification if Django mail fails
        send_admin_notification(
            subject=f"CRITICAL: Django Email Alert Failed - {subject}",
            body=f"Failed to send Django email alert: {e}\nOriginal message: {message}",
            logger=logger
        )
