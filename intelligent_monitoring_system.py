#!/usr/bin/env python3
"""
Shujaa Studio - Intelligent Monitoring & Auto-Healing System
Enterprise-grade monitoring with Kenya-first user experience
"""

import asyncio
import json
import time
import logging
import subprocess
import requests
import smtplib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import psutil
import websockets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent + augmentsearch
# [CONTEXT]: Enterprise monitoring system with intelligent auto-healing and Kenya-first UX
# [GOAL]: Prevent user-facing issues with proactive monitoring and friendly fallbacks
# [TASK]: Create comprehensive monitoring with notifications and auto-fixes

class IssueType(Enum):
    FRONTEND_ERROR = "frontend_error"
    BACKEND_ERROR = "backend_error"
    API_FAILURE = "api_failure"
    DATABASE_ERROR = "database_error"
    PERFORMANCE_ISSUE = "performance_issue"
    MEMORY_LEAK = "memory_leak"
    DISK_SPACE = "disk_space"
    NETWORK_ISSUE = "network_issue"

class IssueSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Issue:
    id: str
    type: IssueType
    severity: IssueSeverity
    message: str
    timestamp: datetime
    component: str
    details: Dict[str, Any]
    auto_fixable: bool = False
    fix_attempted: bool = False
    resolved: bool = False

@dataclass
class SystemHealth:
    frontend_status: str
    backend_status: str
    api_status: str
    database_status: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    response_time: float
    active_users: int
    error_rate: float

class KenyaFriendlyMessages:
    """Kenya-first friendly messages for different scenarios"""
    
    LOADING_MESSAGES = [
        "Pole sana! Our smart engine is getting a quick fix... 🔧",
        "Harambee! We're working together to solve this... 🤝",
        "Hakuna matata! Our AI is climbing Mount Kenya to get better... 🏔️",
        "Asante for your patience! Like a safari, good things take time... 🦁",
        "Karibu! Our system is having a quick chai break... ☕",
        "Jambo! We're fine-tuning like a Maasai warrior... 🛡️",
        "Twende! Our engineers are on it faster than a matatu... 🚌"
    ]
    
    ERROR_MESSAGES = [
        "Pole sana! Something went wrong, but we're fixing it... 🛠️",
        "Harambee! Our team is working together to resolve this... 👥",
        "Hakuna matata! Every challenge makes us stronger... 💪",
        "Asante for your patience during this quick fix... 🙏"
    ]
    
    SUCCESS_MESSAGES = [
        "Asante sana! Everything is working perfectly now... ✅",
        "Harambee! We fixed it together... 🎉",
        "Hakuna matata! All systems are go... 🚀",
        "Karibu back! Everything is running smoothly... 😊"
    ]

class NotificationService:
    """Send notifications to admins when issues occur"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.email_config = config.get('email', {})
        self.slack_config = config.get('slack', {})
        self.sms_config = config.get('sms', {})
        
    async def send_email_alert(self, issue: Issue):
        """Send email notification to admin"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config.get('from_email')
            msg['To'] = ', '.join(self.email_config.get('admin_emails', []))
            msg['Subject'] = f"🚨 Shujaa Studio Alert: {issue.severity.value.upper()} - {issue.type.value}"
            
            body = f"""
            🇰🇪 SHUJAA STUDIO SYSTEM ALERT
            
            Issue ID: {issue.id}
            Type: {issue.type.value}
            Severity: {issue.severity.value}
            Component: {issue.component}
            Time: {issue.timestamp}
            
            Message: {issue.message}
            
            Details: {json.dumps(issue.details, indent=2)}
            
            Auto-fixable: {'Yes' if issue.auto_fixable else 'No'}
            Fix Attempted: {'Yes' if issue.fix_attempted else 'No'}
            
            Harambee! 🚀
            Shujaa Studio Monitoring System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config.get('smtp_server'), self.email_config.get('smtp_port'))
            server.starttls()
            server.login(self.email_config.get('username'), self.email_config.get('password'))
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Email alert sent for issue {issue.id}")
            
        except Exception as e:
            logging.error(f"Failed to send email alert: {e}")
    
    async def send_slack_alert(self, issue: Issue):
        """Send Slack notification"""
        try:
            webhook_url = self.slack_config.get('webhook_url')
            if not webhook_url:
                return
                
            severity_emoji = {
                IssueSeverity.CRITICAL: "🔴",
                IssueSeverity.HIGH: "🟠", 
                IssueSeverity.MEDIUM: "🟡",
                IssueSeverity.LOW: "🟢"
            }
            
            message = {
                "text": f"{severity_emoji[issue.severity]} Shujaa Studio Alert",
                "attachments": [
                    {
                        "color": "danger" if issue.severity in [IssueSeverity.CRITICAL, IssueSeverity.HIGH] else "warning",
                        "fields": [
                            {"title": "Issue Type", "value": issue.type.value, "short": True},
                            {"title": "Severity", "value": issue.severity.value, "short": True},
                            {"title": "Component", "value": issue.component, "short": True},
                            {"title": "Auto-fixable", "value": "Yes" if issue.auto_fixable else "No", "short": True},
                            {"title": "Message", "value": issue.message, "short": False}
                        ],
                        "footer": "Shujaa Studio Monitoring 🇰🇪",
                        "ts": int(issue.timestamp.timestamp())
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=message)
            response.raise_for_status()
            
            logging.info(f"Slack alert sent for issue {issue.id}")
            
        except Exception as e:
            logging.error(f"Failed to send Slack alert: {e}")

class AutoHealingEngine:
    """Intelligent auto-healing system for common issues"""
    
    def __init__(self):
        self.fix_strategies = {
            IssueType.FRONTEND_ERROR: self._fix_frontend_error,
            IssueType.BACKEND_ERROR: self._fix_backend_error,
            IssueType.API_FAILURE: self._fix_api_failure,
            IssueType.MEMORY_LEAK: self._fix_memory_leak,
            IssueType.DISK_SPACE: self._fix_disk_space,
            IssueType.PERFORMANCE_ISSUE: self._fix_performance_issue
        }
    
    async def attempt_fix(self, issue: Issue) -> bool:
        """Attempt to automatically fix the issue"""
        if not issue.auto_fixable or issue.fix_attempted:
            return False
            
        try:
            issue.fix_attempted = True
            fix_strategy = self.fix_strategies.get(issue.type)
            
            if fix_strategy:
                success = await fix_strategy(issue)
                if success:
                    issue.resolved = True
                    logging.info(f"Successfully auto-fixed issue {issue.id}")
                    return True
                    
        except Exception as e:
            logging.error(f"Auto-fix failed for issue {issue.id}: {e}")
            
        return False
    
    async def _fix_frontend_error(self, issue: Issue) -> bool:
        """Fix frontend errors"""
        try:
            # Restart frontend development server
            subprocess.run(["pkill", "-f", "npm.*dev"], check=False)
            await asyncio.sleep(2)
            
            # Start frontend again
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd="frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            await asyncio.sleep(5)
            
            # Check if frontend is responding
            try:
                response = requests.get("http://localhost:3000", timeout=10)
                return response.status_code == 200
            except:
                return False
                
        except Exception as e:
            logging.error(f"Frontend fix failed: {e}")
            return False
    
    async def _fix_backend_error(self, issue: Issue) -> bool:
        """Fix backend errors"""
        try:
            # Restart backend server
            subprocess.run(["pkill", "-f", "python.*api.py"], check=False)
            await asyncio.sleep(2)
            
            # Start backend again
            process = subprocess.Popen(
                ["python", "api.py"],
                cwd="backend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            await asyncio.sleep(5)
            
            # Check if backend is responding
            try:
                response = requests.get("http://localhost:8000", timeout=10)
                return response.status_code == 200
            except:
                return False
                
        except Exception as e:
            logging.error(f"Backend fix failed: {e}")
            return False
    
    async def _fix_api_failure(self, issue: Issue) -> bool:
        """Fix API failures"""
        try:
            # Clear API cache
            subprocess.run(["redis-cli", "FLUSHALL"], check=False)
            
            # Restart API services
            await self._fix_backend_error(issue)
            
            return True
            
        except Exception as e:
            logging.error(f"API fix failed: {e}")
            return False
    
    async def _fix_memory_leak(self, issue: Issue) -> bool:
        """Fix memory leaks"""
        try:
            # Restart services to clear memory
            await self._fix_frontend_error(issue)
            await self._fix_backend_error(issue)
            
            # Clear system cache
            subprocess.run(["sync"], check=False)
            subprocess.run(["echo", "3", ">", "/proc/sys/vm/drop_caches"], shell=True, check=False)
            
            return True
            
        except Exception as e:
            logging.error(f"Memory fix failed: {e}")
            return False
    
    async def _fix_disk_space(self, issue: Issue) -> bool:
        """Fix disk space issues"""
        try:
            # Clean temporary files
            subprocess.run(["find", "/tmp", "-type", "f", "-atime", "+7", "-delete"], check=False)
            
            # Clean logs
            subprocess.run(["find", ".", "-name", "*.log", "-size", "+100M", "-delete"], check=False)
            
            # Clean node_modules cache
            subprocess.run(["npm", "cache", "clean", "--force"], cwd="frontend", check=False)
            
            return True
            
        except Exception as e:
            logging.error(f"Disk space fix failed: {e}")
            return False
    
    async def _fix_performance_issue(self, issue: Issue) -> bool:
        """Fix performance issues"""
        try:
            # Restart services
            await self._fix_frontend_error(issue)
            await self._fix_backend_error(issue)
            
            # Clear caches
            subprocess.run(["npm", "cache", "clean", "--force"], cwd="frontend", check=False)
            
            return True
            
        except Exception as e:
            logging.error(f"Performance fix failed: {e}")
            return False

class SystemMonitor:
    """Comprehensive system monitoring"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.notification_service = NotificationService(config.get('notifications', {}))
        self.auto_healing = AutoHealingEngine()
        self.issues: List[Issue] = []
        self.health_history: List[SystemHealth] = []
        
    async def get_system_health(self) -> SystemHealth:
        """Get current system health metrics"""
        try:
            # Check frontend
            frontend_status = await self._check_frontend()
            
            # Check backend
            backend_status = await self._check_backend()
            
            # Check API endpoints
            api_status = await self._check_api_endpoints()
            
            # System metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Response time check
            response_time = await self._measure_response_time()
            
            health = SystemHealth(
                frontend_status=frontend_status,
                backend_status=backend_status,
                api_status=api_status,
                database_status="healthy",  # Add database check if needed
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                response_time=response_time,
                active_users=0,  # Add user tracking if needed
                error_rate=0.0   # Add error rate calculation
            )
            
            self.health_history.append(health)
            
            # Keep only last 100 health checks
            if len(self.health_history) > 100:
                self.health_history = self.health_history[-100:]
                
            return health
            
        except Exception as e:
            logging.error(f"Health check failed: {e}")
            raise
    
    async def _check_frontend(self) -> str:
        """Check frontend health"""
        try:
            response = requests.get("http://localhost:3000", timeout=10)
            return "healthy" if response.status_code == 200 else "unhealthy"
        except:
            return "down"
    
    async def _check_backend(self) -> str:
        """Check backend health"""
        try:
            response = requests.get("http://localhost:8000", timeout=10)
            return "healthy" if response.status_code == 200 else "unhealthy"
        except:
            return "down"
    
    async def _check_api_endpoints(self) -> str:
        """Check critical API endpoints"""
        try:
            endpoints = [
                "http://localhost:8000/api/generate/video",
                "http://localhost:8000/api/projects",
                "http://localhost:8000/api/gallery"
            ]
            
            for endpoint in endpoints:
                response = requests.get(endpoint, timeout=5)
                if response.status_code not in [200, 405]:  # 405 for POST-only endpoints
                    return "unhealthy"
                    
            return "healthy"
            
        except:
            return "down"
    
    async def _measure_response_time(self) -> float:
        """Measure average response time"""
        try:
            start_time = time.time()
            requests.get("http://localhost:3000", timeout=10)
            return (time.time() - start_time) * 1000  # Convert to milliseconds
        except:
            return 9999.0  # High value for failed requests
    
    async def detect_issues(self, health: SystemHealth) -> List[Issue]:
        """Detect issues based on system health"""
        issues = []
        timestamp = datetime.now()
        
        # Frontend issues
        if health.frontend_status == "down":
            issues.append(Issue(
                id=f"frontend_{int(timestamp.timestamp())}",
                type=IssueType.FRONTEND_ERROR,
                severity=IssueSeverity.CRITICAL,
                message="Frontend server is down",
                timestamp=timestamp,
                component="frontend",
                details={"status": health.frontend_status},
                auto_fixable=True
            ))
        
        # Backend issues
        if health.backend_status == "down":
            issues.append(Issue(
                id=f"backend_{int(timestamp.timestamp())}",
                type=IssueType.BACKEND_ERROR,
                severity=IssueSeverity.CRITICAL,
                message="Backend server is down",
                timestamp=timestamp,
                component="backend",
                details={"status": health.backend_status},
                auto_fixable=True
            ))
        
        # Performance issues
        if health.cpu_usage > 90:
            issues.append(Issue(
                id=f"cpu_{int(timestamp.timestamp())}",
                type=IssueType.PERFORMANCE_ISSUE,
                severity=IssueSeverity.HIGH,
                message=f"High CPU usage: {health.cpu_usage}%",
                timestamp=timestamp,
                component="system",
                details={"cpu_usage": health.cpu_usage},
                auto_fixable=True
            ))
        
        if health.memory_usage > 90:
            issues.append(Issue(
                id=f"memory_{int(timestamp.timestamp())}",
                type=IssueType.MEMORY_LEAK,
                severity=IssueSeverity.HIGH,
                message=f"High memory usage: {health.memory_usage}%",
                timestamp=timestamp,
                component="system",
                details={"memory_usage": health.memory_usage},
                auto_fixable=True
            ))
        
        if health.disk_usage > 90:
            issues.append(Issue(
                id=f"disk_{int(timestamp.timestamp())}",
                type=IssueType.DISK_SPACE,
                severity=IssueSeverity.MEDIUM,
                message=f"Low disk space: {health.disk_usage}% used",
                timestamp=timestamp,
                component="system",
                details={"disk_usage": health.disk_usage},
                auto_fixable=True
            ))
        
        if health.response_time > 5000:  # 5 seconds
            issues.append(Issue(
                id=f"response_{int(timestamp.timestamp())}",
                type=IssueType.PERFORMANCE_ISSUE,
                severity=IssueSeverity.MEDIUM,
                message=f"Slow response time: {health.response_time}ms",
                timestamp=timestamp,
                component="performance",
                details={"response_time": health.response_time},
                auto_fixable=True
            ))
        
        return issues
    
    async def handle_issues(self, issues: List[Issue]):
        """Handle detected issues"""
        for issue in issues:
            # Add to issues list
            self.issues.append(issue)
            
            # Send notifications
            await self.notification_service.send_email_alert(issue)
            await self.notification_service.send_slack_alert(issue)
            
            # Attempt auto-fix
            if issue.auto_fixable:
                success = await self.auto_healing.attempt_fix(issue)
                if success:
                    logging.info(f"Auto-fixed issue: {issue.id}")
                else:
                    logging.warning(f"Auto-fix failed for issue: {issue.id}")
    
    async def start_monitoring(self, interval: int = 30):
        """Start continuous monitoring"""
        logging.info("🇰🇪 Shujaa Studio Monitoring System Started - Harambee!")
        
        while True:
            try:
                # Get system health
                health = await self.get_system_health()
                
                # Detect issues
                issues = await self.detect_issues(health)
                
                # Handle issues
                if issues:
                    await self.handle_issues(issues)
                
                # Log health status
                logging.info(f"System Health: Frontend={health.frontend_status}, Backend={health.backend_status}, CPU={health.cpu_usage}%, Memory={health.memory_usage}%")
                
                # Wait for next check
                await asyncio.sleep(interval)
                
            except Exception as e:
                logging.error(f"Monitoring error: {e}")
                await asyncio.sleep(interval)

# Configuration
MONITORING_CONFIG = {
    "notifications": {
        "email": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "your-email@gmail.com",
            "password": "your-app-password",
            "from_email": "shujaa-monitoring@yourdomain.com",
            "admin_emails": ["admin@yourdomain.com"]
        },
        "slack": {
            "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
        },
        "sms": {
            "api_key": "your-sms-api-key",
            "admin_phones": ["+254700000000"]
        }
    },
    "monitoring": {
        "interval": 30,  # seconds
        "health_check_timeout": 10,
        "auto_healing_enabled": True
    }
}

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('shujaa_monitoring.log'),
            logging.StreamHandler()
        ]
    )
    
    # Start monitoring
    monitor = SystemMonitor(MONITORING_CONFIG)
    asyncio.run(monitor.start_monitoring())
