import logging
import sys
import os
from pathlib import Path

# Add project root to sys.path to allow imports
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Configure logging for this script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import necessary components
from ai_health_scanner import AIHealthScanner, ScannerConfig, HealthStatus
from backend.dependency_watcher.dependency_watcher import DependencyWatcher, load_config as load_dep_config

def run_check_system():
    """
    Runs a comprehensive system check including health and dependency status.
    Outputs a summary to the console.
    """
    logger.info("Starting comprehensive system check...")

    # --- Health Check ---
    health_scanner_config = ScannerConfig(
        scan_mode=ScanMode.STANDARD,
        notifications=False # Don't send notifications for a manual check
    )
    health_scanner = AIHealthScanner(health_scanner_config)
    
    health_scanner._run_scan() # Run a synchronous scan
    health_report = health_scanner.get_health_report()

    health_status_overall = health_report.get("overall_health", "unknown")
    health_issues = health_report.get("last_scan", {}).get("issues", [])

    print("\n--- Health Report ---")
    if health_status_overall == "healthy":
        print("✅ Health OK")
    else:
        print(f"❌ Health Issues: {health_status_overall.upper()}")
        for issue in health_issues:
            print(f"  - {issue}")
    print("---------------------")

    # --- Dependency Check ---
    dep_watcher_config_path = str(project_root / 'backend' / 'dependency_watcher' / 'config' / 'dependency_config.yaml')
    dependency_watcher = DependencyWatcher(dep_watcher_config_path)
    
    dependency_status_report = dependency_watcher.check_dependencies()

    print("\n--- Dependency Report ---")
    all_deps_healthy = True
    for dep in dependency_status_report:
        print(f"  {dep['name']:<15} | Installed: {dep['installed_version']:<10} | Required: {dep['required_range']:<10} | Status: {dep['status']:<10} | Message: {dep['message']}")
        if dep['status'] != "HEALTHY":
            all_deps_healthy = False
    
    if all_deps_healthy:
        print("✅ Dependencies OK")
    else:
        print("❌ Dependency Issues Detected")
    print("-------------------------")

    if health_status_overall != "healthy" or not all_deps_healthy:
        sys.exit(1) # Exit with error if any issues found
    else:
        sys.exit(0) # Exit successfully

if __name__ == "__main__":
    run_check_system()
