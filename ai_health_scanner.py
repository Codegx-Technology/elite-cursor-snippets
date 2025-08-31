#!/usr/bin/env python3
"""
Shujaa Studio - AI Health Scanner
Intelligent system health monitoring with auto-healing capabilities
Like an antivirus but for application health
"""

import asyncio
import json
import time
import logging
import subprocess
import requests
import psutil
import schedule
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import signal
import sys
from pathlib import Path

# [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent + augmentsearch
# [CONTEXT]: AI-powered health scanner with intelligent monitoring and auto-healing
# [GOAL]: Proactive system health management with Kenya-first user experience
# [TASK]: Create comprehensive health scanner with scheduling and muting capabilities

def send_admin_notification(subject: str, body: str, logger: logging.Logger):
    """Send a private notification to super admin via SMTP (Gmail). Fail-soft on errors."""
    try:
        host = os.getenv("SMTP_HOST", "")
        port = int(os.getenv("SMTP_PORT", "0") or 0)
        username = os.getenv("SMTP_USERNAME", "")
        password = os.getenv("SMTP_PASSWORD", "")
        sender = os.getenv("SMTP_FROM", username)
        recipient = os.getenv("SMTP_TO", username)

        if not (host and port and username and password and sender and recipient):
            # Missing configuration; log and return
            logger.debug("SMTP not configured; skipping admin notification")
            return

        msg = MIMEText(body, _charset="utf-8")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        context = ssl.create_default_context()
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls(context=context)
            server.login(username, password)
            server.send_message(msg)
    except Exception as e:
        # Do not crash scans due to email errors
        logger.debug(f"Admin notification failed: {e}")

class HealthStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    DOWN = "down"

class ScanMode(Enum):
    QUICK = "quick"          # 30 seconds - basic checks
    STANDARD = "standard"    # 2 minutes - comprehensive
    DEEP = "deep"           # 5 minutes - full system scan
    CUSTOM = "custom"       # User-defined

@dataclass
class HealthMetrics:
    timestamp: datetime
    frontend_status: HealthStatus
    backend_status: HealthStatus
    api_response_time: float
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_latency: float
    error_count: int
    active_connections: int
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'frontend_status': self.frontend_status.value,
            'backend_status': self.backend_status.value,
            'api_response_time': self.api_response_time,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'disk_usage': self.disk_usage,
            'network_latency': self.network_latency,
            'error_count': self.error_count,
            'active_connections': self.active_connections
        }

@dataclass
class ScannerConfig:
    scan_mode: ScanMode = ScanMode.STANDARD
    scan_interval: int = 120  # seconds
    auto_heal: bool = True
    notifications: bool = True
    muted: bool = False
    mute_until: Optional[datetime] = None
    log_level: str = "INFO"
    max_auto_fixes: int = 3
    
class KenyaFriendlyNotifier:
    """Kenya-first friendly notifications and user messages"""
    
    SCANNING_MESSAGES = [
        "🔍 Hakuna matata! Our AI is checking system health...",
        "🏔️ Like climbing Mount Kenya, we're checking every step...",
        "🦁 Safari mode: Our AI is hunting for issues...",
        "🤝 Harambee! Working together to keep things smooth...",
        "☕ Quick chai break while we scan the system...",
        "🛡️ Maasai warrior mode: Protecting your experience..."
    ]
    
    HEALING_MESSAGES = [
        "🔧 Pole sana! Our smart engine is getting a quick fix...",
        "⚡ Twende! Fixing this faster than a Nairobi matatu...",
        "🏥 Our AI doctor is treating the system...",
        "🔨 Harambee! Our team is working on this together...",
        "🌟 Making everything shine like the Kenyan sun..."
    ]
    
    SUCCESS_MESSAGES = [
        "✅ Asante sana! Everything is working perfectly now!",
        "🎉 Harambee! We fixed it together!",
        "🚀 All systems go - smoother than Diani Beach!",
        "😊 Karibu back! Everything is running like clockwork!",
        "🇰🇪 Proudly Kenyan and perfectly functional!"
    ]
    
    @staticmethod
    def get_random_message(message_type: str) -> str:
        import random
        messages = getattr(KenyaFriendlyNotifier, f"{message_type.upper()}_MESSAGES", [])
        return random.choice(messages) if messages else "System is being checked..."

class AIHealthScanner:
    """AI-powered health scanner with intelligent monitoring"""
    
    def __init__(self, config: ScannerConfig = None):
        self.config = config or ScannerConfig()
        self.is_running = False
        self.is_muted = False
        self.scan_history: List[HealthMetrics] = []
        self.auto_fix_count = 0
        self.last_scan_time = None
        self.notifier = KenyaFriendlyNotifier()
        
        # Setup logging
        # Force stdout to use UTF-8 encoding to handle emojis on Windows
        if sys.stdout.encoding != 'utf-8':
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except TypeError:
                # Fallback for environments where reconfigure might not be available
                import codecs
                sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - 🇰🇪 Shujaa Scanner - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('shujaa_health_scanner.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout) # sys.stdout is now UTF-8 aware
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def _run_dependency_check_job(self):
        """Runs the Django management command for dependency checking."""
        try:
            python_executable = sys.executable
            project_root = Path(__file__).parent.parent
            manage_py_path = project_root / 'manage.py'

            if not manage_py_path.exists():
                self.logger.error(f"manage.py not found at {manage_py_path}. Cannot run dependency check.")
                send_admin_notification(
                    subject="Dependency Check Scheduling Error",
                    body=f"manage.py not found at {manage_py_path}. Dependency check could not be run.",
                    logger=self.logger
                )
                return

            cmd = [
                str(python_executable),
                str(manage_py_path),
                'check_dependencies'
            ]
            
            # Run the command silently, capture output for logging if needed
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)

            if result.returncode != 0:
                error_message = f"Dependency check command failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
                self.logger.error(error_message)
                send_admin_notification(
                    subject="Dependency Check Failed",
                    body=error_message,
                    logger=self.logger
                )
            else:
                self.logger.info("Dependency check command ran successfully.")
                if result.stdout:
                    self.logger.info(f"Dependency check stdout: {result.stdout}")
                if result.stderr:
                    self.logger.warning(f"Dependency check stderr: {result.stderr}")

        except Exception as e:
            self.logger.error(f"Error running dependency check job: {e}")
            send_admin_notification(
                subject="Dependency Check Job Error",
                body=f"An unexpected error occurred while trying to run the dependency check job: {e}",
                logger=self.logger
            )

    def start_scanner(self):
        """Start the AI health scanner"""
        if self.is_running:
            self.logger.warning("Scanner is already running!")
            return
            
        self.is_running = True
        self.logger.info("🚀 Shujaa AI Health Scanner Starting - Harambee!")
        
        # Schedule scans based on mode
        if self.config.scan_mode == ScanMode.QUICK:
            schedule.every(30).seconds.do(self._run_scan)
        elif self.config.scan_mode == ScanMode.STANDARD:
            schedule.every(2).minutes.do(self._run_scan)
        elif self.config.scan_mode == ScanMode.DEEP:
            schedule.every(5).minutes.do(self._run_scan)
        else:
            schedule.every(self.config.scan_interval).seconds.do(self._run_scan)
        
        # Start scheduler in background thread
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        # Schedule dependency check daily at 00:00
        schedule.every().day.at("00:00").do(self._run_dependency_check_job)
        self.logger.info("Dependency check scheduled daily at 00:00.")

        self.logger.info(f"Scanner scheduled every {self.config.scan_interval}s in {self.config.scan_mode.value} mode")
        
    def stop_scanner(self):
        """Stop the AI health scanner"""
        self.is_running = False
        schedule.clear()
        self.logger.info("🛑 Shujaa AI Health Scanner Stopped")
        
    def mute_scanner(self, duration_minutes: int = 60):
        """Mute scanner notifications for specified duration"""
        self.is_muted = True
        self.config.mute_until = datetime.now() + timedelta(minutes=duration_minutes)
        self.logger.info(f"🔇 Scanner muted for {duration_minutes} minutes")
        
    def unmute_scanner(self):
        """Unmute scanner notifications"""
        self.is_muted = False
        self.config.mute_until = None
        self.logger.info("🔊 Scanner unmuted")
        
    def _check_mute_status(self):
        """Check if scanner should be unmuted"""
        if self.is_muted and self.config.mute_until:
            if datetime.now() > self.config.mute_until:
                self.unmute_scanner()
                
    def _run_scan(self):
        """Run a health scan"""
        try:
            self._check_mute_status()
            
            if not self.is_muted:
                self.logger.info(self.notifier.get_random_message("scanning"))
            
            # Perform health scan
            metrics = self._perform_health_scan()
            
            # Store scan results
            self.scan_history.append(metrics)
            self.last_scan_time = datetime.now()
            
            # Keep only last 100 scans
            if len(self.scan_history) > 100:
                self.scan_history = self.scan_history[-100:]
            
            # Analyze results and take action
            issues = self._analyze_health_metrics(metrics)
            
            if issues and not self.is_muted:
                self._handle_issues(issues, metrics)
                
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")
            
    def _perform_health_scan(self) -> HealthMetrics:
        """Perform comprehensive health scan"""
        
        # Frontend health check
        frontend_status = self._check_frontend_health()
        
        # Backend health check
        backend_status = self._check_backend_health()
        
        # API response time
        api_response_time = self._measure_api_response_time()
        
        # System metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Network latency
        network_latency = self._measure_network_latency()
        
        # Error count (from logs)
        error_count = self._count_recent_errors()
        
        # Active connections
        active_connections = len(psutil.net_connections())
        
        return HealthMetrics(
            timestamp=datetime.now(),
            frontend_status=frontend_status,
            backend_status=backend_status,
            api_response_time=api_response_time,
            cpu_usage=cpu_usage,
            memory_usage=memory.percent,
            disk_usage=disk.percent,
            network_latency=network_latency,
            error_count=error_count,
            active_connections=active_connections
        )
        
    def _check_frontend_health(self) -> HealthStatus:
        """Check frontend application health"""
        try:
            response = requests.get("http://localhost:3000", timeout=10)
            if response.status_code == 200:
                return HealthStatus.HEALTHY
            else:
                return HealthStatus.WARNING
        except requests.exceptions.ConnectionError:
            return HealthStatus.DOWN
        except requests.exceptions.Timeout:
            return HealthStatus.CRITICAL
        except Exception:
            return HealthStatus.WARNING
            
    def _check_backend_health(self) -> HealthStatus:
        """Check backend API health"""
        try:
            response = requests.get("http://localhost:8000", timeout=10)
            if response.status_code == 200:
                return HealthStatus.HEALTHY
            else:
                return HealthStatus.WARNING
        except requests.exceptions.ConnectionError:
            return HealthStatus.DOWN
        except requests.exceptions.Timeout:
            return HealthStatus.CRITICAL
        except Exception:
            return HealthStatus.WARNING
            
    def _measure_api_response_time(self) -> float:
        """Measure API response time in milliseconds"""
        try:
            start_time = time.time()
            requests.get("http://localhost:8000", timeout=10)
            return (time.time() - start_time) * 1000
        except:
            return 9999.0  # High value for failed requests
            
    def _measure_network_latency(self) -> float:
        """Measure network latency"""
        try:
            start_time = time.time()
            requests.get("http://google.com", timeout=5)
            return (time.time() - start_time) * 1000
        except:
            return 9999.0
            
    def _count_recent_errors(self) -> int:
        """Count recent errors from logs"""
        try:
            # Count errors in last 5 minutes from log files
            error_count = 0
            log_files = ['shujaa_health_scanner.log', 'frontend/npm-debug.log', 'backend/api.log']
            
            for log_file in log_files:
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        # Count ERROR lines in last 100 lines
                        recent_lines = lines[-100:] if len(lines) > 100 else lines
                        error_count += sum(1 for line in recent_lines if 'ERROR' in line)
                except FileNotFoundError:
                    continue
                    
            return error_count
        except:
            return 0
            
    def _analyze_health_metrics(self, metrics: HealthMetrics) -> List[str]:
        """AI-powered analysis of health metrics"""
        issues = []
        
        # Critical issues
        if metrics.frontend_status == HealthStatus.DOWN:
            issues.append("CRITICAL: Frontend is down")
        if metrics.backend_status == HealthStatus.DOWN:
            issues.append("CRITICAL: Backend is down")
            
        # Performance issues
        if metrics.cpu_usage > 90:
            issues.append(f"HIGH: CPU usage at {metrics.cpu_usage}%")
        if metrics.memory_usage > 90:
            issues.append(f"HIGH: Memory usage at {metrics.memory_usage}%")
        if metrics.disk_usage > 90:
            issues.append(f"MEDIUM: Disk usage at {metrics.disk_usage}%")
            
        # Response time issues
        if metrics.api_response_time > 5000:
            issues.append(f"MEDIUM: Slow API response ({metrics.api_response_time}ms)")
            
        # Error rate issues
        if metrics.error_count > 10:
            issues.append(f"HIGH: High error rate ({metrics.error_count} errors)")
            
        return issues
        
    def _handle_issues(self, issues: List[str], metrics: HealthMetrics):
        """Handle detected issues with AI-powered responses"""
        
        if not self.is_muted:
            self.logger.warning(f"🚨 Issues detected: {len(issues)}")
            for issue in issues:
                self.logger.warning(f"  - {issue}")

            # Private admin notification (email). Keep users unaware; spinner handled on UI.
            if self.config.notifications:
                summary_lines = [
                    "Shujaa Studio - Health Alert",
                    f"Time: {datetime.now().isoformat()}",
                    f"Frontend: {metrics.frontend_status.value}",
                    f"Backend: {metrics.backend_status.value}",
                    f"API latency: {metrics.api_response_time:.0f}ms",
                    f"CPU: {metrics.cpu_usage:.1f}%  MEM: {metrics.memory_usage:.1f}%  DISK: {metrics.disk_usage:.1f}%",
                    f"Network: {metrics.network_latency:.0f}ms  Errors: {metrics.error_count}  Conns: {metrics.active_connections}",
                    "Issues:",
                ] + [f" - {i}" for i in issues]
                send_admin_notification(
                    subject="[Shujaa] Health Alert",
                    body="\n".join(summary_lines),
                    logger=self.logger
                )
        
        # Attempt auto-healing if enabled
        if self.config.auto_heal and self.auto_fix_count < self.config.max_auto_fixes:
            self._attempt_auto_heal(issues, metrics)
            
    def _attempt_auto_heal(self, issues: List[str], metrics: HealthMetrics):
        """Attempt to automatically heal detected issues"""
        
        if not self.is_muted:
            self.logger.info(self.notifier.get_random_message("healing"))
        
        healed_issues = []
        
        for issue in issues:
            try:
                if "Frontend is down" in issue:
                    if self._restart_frontend():
                        healed_issues.append("Frontend restarted successfully")
                        
                elif "Backend is down" in issue:
                    if self._restart_backend():
                        healed_issues.append("Backend restarted successfully")
                        
                elif "CPU usage" in issue:
                    if self._optimize_cpu():
                        healed_issues.append("CPU usage optimized")
                        
                elif "Memory usage" in issue:
                    if self._clear_memory():
                        healed_issues.append("Memory cleared")
                        
                elif "Disk usage" in issue:
                    if self._clean_disk():
                        healed_issues.append("Disk space cleaned")
                        
            except Exception as e:
                self.logger.error(f"Auto-heal failed for '{issue}': {e}")
                
        if healed_issues:
            self.auto_fix_count += 1
            if not self.is_muted:
                self.logger.info(self.notifier.get_random_message("success"))
                for healed in healed_issues:
                    self.logger.info(f"  ✅ {healed}")
                    
    def _restart_frontend(self) -> bool:
        """Restart frontend service"""
        try:
            subprocess.run(["pkill", "-f", "npm.*dev"], check=False)
            time.sleep(2)
            
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd="frontend",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(5)
            return self._check_frontend_health() == HealthStatus.HEALTHY
            
        except Exception as e:
            self.logger.error(f"Frontend restart failed: {e}")
            return False
            
    def _restart_backend(self) -> bool:
        """Restart backend service"""
        try:
            subprocess.run(["pkill", "-f", "python.*api.py"], check=False)
            time.sleep(2)
            
            process = subprocess.Popen(
                ["python", "api.py"],
                cwd="backend",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(5)
            return self._check_backend_health() == HealthStatus.HEALTHY
            
        except Exception as e:
            self.logger.error(f"Backend restart failed: {e}")
            return False
            
    def _optimize_cpu(self) -> bool:
        """Optimize CPU usage"""
        try:
            # Lower process priorities
            subprocess.run(["renice", "+10", "-p", str(psutil.Process().pid)], check=False)
            return True
        except:
            return False
            
    def _clear_memory(self) -> bool:
        """Clear memory"""
        try:
            subprocess.run(["sync"], check=False)
            subprocess.run(["echo", "1", ">", "/proc/sys/vm/drop_caches"], shell=True, check=False)
            return True
        except:
            return False
            
    def _clean_disk(self) -> bool:
        """Clean disk space"""
        try:
            subprocess.run(["find", "/tmp", "-type", "f", "-atime", "+1", "-delete"], check=False)
            subprocess.run(["npm", "cache", "clean", "--force"], cwd="frontend", check=False)
            return True
        except:
            return False
            
    def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report"""
        if not self.scan_history:
            return {"status": "No scans performed yet"}
            
        latest = self.scan_history[-1]
        
        return {
            "scanner_status": "running" if self.is_running else "stopped",
            "muted": self.is_muted,
            "last_scan": latest.to_dict(),
            "auto_fix_count": self.auto_fix_count,
            "scan_history_count": len(self.scan_history),
            "overall_health": self._calculate_overall_health()
        }
        
    def _calculate_overall_health(self) -> str:
        """Calculate overall system health score"""
        if not self.scan_history:
            return "unknown"
            
        latest = self.scan_history[-1]
        
        if (latest.frontend_status == HealthStatus.DOWN or 
            latest.backend_status == HealthStatus.DOWN):
            return "critical"
        elif (latest.cpu_usage > 80 or latest.memory_usage > 80 or 
              latest.api_response_time > 3000):
            return "warning"
        else:
            return "healthy"

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\n🛑 Shujaa AI Health Scanner shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create scanner with default config
    config = ScannerConfig(
        scan_mode=ScanMode.STANDARD,
        scan_interval=120,  # 2 minutes
        auto_heal=True,
        notifications=True,
        muted=False
    )
    
    scanner = AIHealthScanner(config)
    
    try:
        # Start the scanner
        scanner.start_scanner()
        
        print("🇰🇪 Shujaa AI Health Scanner is running!")
        print("Commands:")
        print("  - Type 'status' for health report")
        print("  - Type 'mute 30' to mute for 30 minutes")
        print("  - Type 'unmute' to unmute")
        print("  - Type 'stop' to stop scanner")
        print("  - Type 'quit' to exit")
        
        # Interactive command loop
        while True:
            try:
                command = input("\n🔍 Scanner> ").strip().lower()
                
                if command == "status":
                    report = scanner.get_health_report()
                    print(json.dumps(report, indent=2))
                    
                elif command.startswith("mute"):
                    parts = command.split()
                    minutes = int(parts[1]) if len(parts) > 1 else 60
                    scanner.mute_scanner(minutes)
                    print(f"🔇 Scanner muted for {minutes} minutes")
                    
                elif command == "unmute":
                    scanner.unmute_scanner()
                    print("🔊 Scanner unmuted")
                    
                elif command == "stop":
                    scanner.stop_scanner()
                    print("🛑 Scanner stopped")
                    
                elif command in ["quit", "exit"]:
                    scanner.stop_scanner()
                    print("👋 Asante sana! Goodbye!")
                    break
                    
                else:
                    print("Unknown command. Try: status, mute, unmute, stop, quit")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Scanner failed to start: {e}")
    finally:
        scanner.stop_scanner()
