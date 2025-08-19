from django.core.management.base import BaseCommand
from backend.dependency_watcher.dependency_watcher import run_dependency_check
from backend.notifications.admin_notifier import notify_admin
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Checks for missing or outdated dependencies.'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Starting dependency check...')
            run_dependency_check()
            self.stdout.write(self.style.SUCCESS('Dependency check completed successfully.'))
        except Exception as e:
            logger.error(f"Dependency check failed: {e}")
            notify_admin(
                subject="Dependency Check Failed",
                message=f"The dependency check failed with the following error: {e}"
            )
            self.stderr.write(self.style.ERROR('Dependency check failed.'))
