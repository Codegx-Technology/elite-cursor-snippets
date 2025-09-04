from backend.db.models import User
from backend.utils.auth import hash_password

from config_loader import get_config
from logging_setup import get_logger

logger = get_logger(__name__)
config = get_config()

def seed_superadmins():
    # [SNIPPET]: thinkwithai + kenyafirst + enterprise-secure
    # [CONTEXT]: Seeding superadmin users from a secure configuration source instead of hardcoded values.
    # [GOAL]: Eliminate hardcoded credentials and improve security posture.
    # [TASK]: Replace hardcoded list with a loop over config.auth.super_admins.
    if not config.auth.super_admins:
        logger.warning("No super admins defined in the configuration. Skipping super admin seeding.")
        return

    for sa in config.auth.super_admins:
        if not User.objects.filter(username=sa["username"]).exists():
            User.objects.create(
                username=sa["username"],
                password=hash_password(sa["password"]),
                role="superadmin",
            )

def get_metrics():
    # Placeholder: return any metrics relevant to SuperAdmin
    return {
        "total_users": User.objects.count(),
        "active_widgets": 12,  # Example
    }
