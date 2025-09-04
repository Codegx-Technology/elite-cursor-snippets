# utils/notify.py

from typing import Dict, Any

def notify_admin(subject: str, message: str, metadata: Dict[str, Any] = None):
    """
    Placeholder for admin notification function.
    In a real system, this would send emails, Slack messages, etc.
    """
    print(f"[ADMIN NOTIFICATION] Subject: {subject}\nMessage: {message}\nMetadata: {metadata}")
