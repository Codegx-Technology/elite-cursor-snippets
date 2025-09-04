import logging
import time
import sys
import signal
from core.monitoring.__init__ import MonitoringService # Corrected import path
import schedule # Import schedule library

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

monitoring_service = MonitoringService()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Received shutdown signal. Stopping monitoring services...")
    monitoring_service.stop_all()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        monitoring_service.start_all()
        logger.info("MonitoringService started. Press Ctrl+C to stop.")
        
        # Keep the main thread alive to allow scheduled jobs to run
        while True:
            schedule.run_pending() # Run pending jobs from the schedule library
            time.sleep(1)

    except Exception as e:
        logger.error(f"MonitoringService failed to start or encountered an error: {e}")
        monitoring_service.stop_all()
        sys.exit(1)
