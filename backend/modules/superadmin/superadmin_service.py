from backend.db.models import User
from backend.utils.auth import hash_password

def seed_superadmins():
    superadmins = [
        {"username": "peter", "password": "aluru742!!"},
        {"username": "apollo", "password": "aluru742!!"},
    ]
    for sa in superadmins:
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
