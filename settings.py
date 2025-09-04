# settings.py - Placeholder for application settings
import os

# Notification settings (reusing admin email from .env.example)
# This should ideally come from .env or a secure config
ADMIN_EMAIL = os.getenv("SMTP_TO", "admin@example.com") 

# Feature flags
ENABLE_DEPWATCHER = os.getenv("ENABLE_DEPWATCHER", "True").lower() in ('true', '1', 't', 'y', 'yes')
ALLOW_AUTOPATCH = os.getenv("ALLOW_AUTOPATCH", "False").lower() in ('true', '1', 't', 'y', 'yes') # Default off in prod
PATCH_WINDOW_CRON = os.getenv("PATCH_WINDOW_CRON", "0 2 * * SUN") # Default: Sunday 02:00