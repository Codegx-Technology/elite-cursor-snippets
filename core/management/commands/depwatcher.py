from django.core.management.base import BaseCommand
from backend.dependency_watcher.dependency_watcher import DependencyWatcher # Assuming DependencyWatcher is importable from here
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Run Dependency Watcher checks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--approve",
            action="store_true",
            help="Automatically apply safe patches",
        )

    def handle(self, *args, **options):
        # Instantiate DependencyWatcher with its config path
        # Assuming config is at backend/dependency_watcher/config/dependency_config.yaml
        watcher = DependencyWatcher('backend/dependency_watcher/config/dependency_config.yaml')
        
        if options["approve"]:
            self.stdout.write(self.style.WARNING("Running Dependency Watcher (auto-approve mode)"))
            # This will trigger the patching logic within DependencyWatcher
            watcher.run_checks(auto_approve=True) 
        else:
            self.stdout.write(self.style.SUCCESS("Running Dependency Watcher (dry-run mode)"))
            watcher.run_checks(auto_approve=False) # Default behavior is dry-run
