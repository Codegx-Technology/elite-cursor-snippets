import logging
import threading
import time
import sys
import os
from pathlib import Path

# Add project root to sys.path to allow imports from ai_health_scanner and backend
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from ai_health_scanner import AIHealthScanner, ScannerConfig, ScanMode, send_admin_notification
from backend.dependency_watcher.dependency_watcher import DependencyWatcher, run_dependency_check as run_dep_check_standalone

logger = logging.getLogger(__name__)

class MonitoringService:
    def __init__(self):
        self.health_scanner_config = ScannerConfig(
            scan_mode=ScanMode.STANDARD,
            notifications=True,
            scan_interval=120 # Default to 2 minutes for health checks
        )
        self.health_scanner = AIHealthScanner(self.health_scanner_config)
        
        # Dependency Watcher config path
        self.dep_watcher_config_path = str(project_root / 'backend' / 'dependency_watcher' / 'config' / 'dependency_config.yaml')
        self.dependency_watcher = DependencyWatcher(self.dep_watcher_config_path)

        self.is_running = False

    def _run_health_scanner_loop(self):
        """Runs the health scanner in its own scheduled loop."""
        self.health_scanner.start_scanner()
        # The AIHealthScanner's start_scanner already handles its own scheduling loop
        # We just need to keep this thread alive while the scanner runs
        while self.health_scanner.is_running:
            time.sleep(1) # Sleep to prevent busy-waiting

    def _run_dependency_watcher_job(self):
        """Runs the dependency check job."""
        logger.info("Running scheduled dependency check.")
        self.dependency_watcher.check_dependencies()

    def start_all(self):
        """Starts all monitoring services."""
        if self.is_running:
            logger.warning("MonitoringService is already running!")
            return

        self.is_running = True
        logger.info("🚀 Starting unified MonitoringService!")

        # Start Health Scanner in a separate thread
        health_thread = threading.Thread(target=self._run_health_scanner_loop, daemon=True)
        health_thread.start()
        logger.info("Health Scanner started.")

        # Schedule dependency check daily at midnight
        schedule.every().day.at("00:00").do(self._run_dependency_watcher_job)
        self.logger.info("Dependency check scheduled daily at 00:00.")

        # Initial run of dependency check
        self._run_dependency_watcher_job() # Run once on startup

    def stop_all(self):
        """Stops all monitoring services."""
        if not self.is_running:
            logger.warning("MonitoringService is not running!")
            return
        self.is_running = False
        self.health_scanner.stop_scanner()
        schedule.clear() # Clear all scheduled jobs
        logger.info("🛑 Unified MonitoringService stopped.")
