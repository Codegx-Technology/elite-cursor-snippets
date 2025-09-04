from django.core.management.base import BaseCommand
from backend.dependency_watcher.dependency_watcher import DependencyWatcher # Assuming DependencyWatcher is importable from here
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Run Dependency Watcher checks and model health reports"

    def add_arguments(self, parser):
        parser.add_argument(
            "--approve",
            action="store_true",
            help="Automatically apply safe patches",
        )
        parser.add_argument(
            "--rollback-bad",
            action="store_true",
            help="Automatically rollback degraded canary models",
        )

    def handle(self, *args, **options):
        # Instantiate DependencyWatcher with its config path
        # Assuming config is at backend/dependency_watcher/config/dependency_config.yaml
        watcher = DependencyWatcher('backend/dependency_watcher/config/dependency_config.yaml')
        
        self.stdout.write(self.style.SUCCESS("Running Dependency Watcher checks..."))

        # Run general dependency checks
        watcher.run_checks(auto_approve=options["approve"])

        # Check model store integrity
        self.stdout.write(self.style.SUCCESS("\n--- Checking Model Store Integrity ---"))
        integrity_report = watcher.check_model_store_integrity()
        for report in integrity_report:
            if report["status"] == "HEALTHY":
                self.stdout.write(self.style.SUCCESS(f"  ✅ {report['provider']}/{report['model_name']}: {report['message']}"))
            else:
                self.stdout.write(self.style.ERROR(f"  ❌ {report['provider']}/{report['model_name']}: {report['status']} - {report['message']}"))

        # Report canary health
        self.stdout.write(self.style.SUCCESS("\n--- Reporting Canary Health ---"))
        canary_health_report = watcher.report_canary_health(auto_rollback_bad=options["rollback_bad"])
        for report in canary_health_report:
            if report["health_status"] == "HEALTHY":
                self.stdout.write(self.style.SUCCESS(f"  ✅ {report['provider']}/{report['model_name']} (Canary: {report['canary_tag']}): {report['health_message']}"))
            else:
                self.stdout.write(self.style.ERROR(f"  ❌ {report['provider']}/{report['model_name']} (Canary: {report['canary_tag']}): {report['health_status']} - {report['health_message']}"))
                if options["rollback_bad"] and "Auto-rolled back" in report["health_message"]:
                    self.stdout.write(self.style.WARNING("    (Auto-rollback attempted)"))

