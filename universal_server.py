#!/usr/bin/env python3
"""
// [TASK]: Universal Server Manager for Shujaa Studio
// [GOAL]: Unified server management with port conflict resolution
// [SNIPPET]: surgicalfix + perfcheck + kenyafirst
// [CONTEXT]: Manage frontend (port 3000), backend (port 8000), and all other services
// [PROGRESS]: Creating universal server controller
// [NEXT]: Implement port management and process control
// [LOCATION]: Root directory - universal_server.py
"""

import asyncio
import subprocess
import sys
import os
import signal
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import requests

# Force venv site-packages into sys.path before dependency checks
import site
import shutil

# Ensure virtual environment site-packages are in sys.path
venv_site_packages = os.path.join(sys.prefix, "Lib", "site-packages")
if venv_site_packages not in sys.path:
    site.addsitedir(venv_site_packages)

# Debug: Print environment information (Windows-safe)
try:
    print(f"Python Using Python interpreter: {sys.executable}")
    print(f"Python Python version: {sys.version}")
    print(f"Python Python prefix: {sys.prefix}")
    print(f"Python Site packages: {venv_site_packages}")
except UnicodeEncodeError:
    print("Python interpreter:", sys.executable)
    print("Python version:", sys.version)
    print("Python prefix:", sys.prefix)
    print("Site packages:", venv_site_packages)

# Enhanced Node.js/npm detection
node_path = shutil.which("node")
npm_path = shutil.which("npm")

if not node_path or not npm_path:
    # Try adding common Node.js installation path
    nodejs_path = "C:\\Program Files\\nodejs"
    if os.path.exists(nodejs_path) and nodejs_path not in os.environ.get("PATH", ""):
        os.environ["PATH"] = nodejs_path + os.pathsep + os.environ.get("PATH", "")
        node_path = shutil.which("node")
        npm_path = shutil.which("npm")

print(f"🟢 Node.js path: {node_path or 'Not found'}")
print(f"🟢 npm path: {npm_path or 'Not found'}")

# Auto-install missing Python dependencies
def ensure_python_dependency(package_name, import_name=None):
    """Ensure a Python package is installed, auto-install if missing"""
    if import_name is None:
        import_name = package_name

    try:
        __import__(import_name)
        print(f"✅ {package_name} imported successfully")
        return True
    except ImportError as e:
        print(f"⚠️ {package_name} not found, installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            __import__(import_name)
            print(f"✅ {package_name} installed and imported successfully")
            return True
        except Exception as install_error:
            print(f"❌ Failed to install {package_name}: {install_error}")
            return False

# Ensure critical dependencies
ensure_python_dependency("psutil")
ensure_python_dependency("requests")

# Import dependencies after ensuring they're available
import psutil
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ServiceType(Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    GRADIO = "gradio"
    MONITORING = "monitoring"

@dataclass
class ServiceConfig:
    name: str
    type: ServiceType
    port: int
    command: List[str]
    cwd: Optional[str] = None
    env: Optional[Dict[str, str]] = None
    health_check_url: Optional[str] = None
    startup_delay: int = 5
    required: bool = True

class UniversalServerManager:
    """
    // [TASK]: Elite server management for Shujaa Studio
    // [GOAL]: Zero-conflict multi-service orchestration
    // [SNIPPET]: thinkwithai + perfcheck + kenyafirst
    """
    
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.processes: Dict[str, subprocess.Popen] = {}
        self.services: Dict[str, ServiceConfig] = {}
        self.running = False
        
        # Initialize services configuration
        self._setup_services()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("KE Universal Shujaa Studio Server Manager Initialized - Harambee!")
    
    def _setup_services(self):
        """Configure all services with their startup parameters"""
        
        # Frontend Service (React/Next.js) - Only if Node.js is available
        frontend_available = self._check_node_available()
        if frontend_available:
            npm_path = shutil.which("npm")
            self.services["frontend"] = ServiceConfig(
                name="Shujaa Studio Frontend",
                type=ServiceType.FRONTEND,
                port=3000,
                command=[npm_path or "npm", "run", "dev"],
                cwd=str(self.project_root / "frontend"),
                health_check_url="http://localhost:3000",
                startup_delay=10,
                required=True
            )
        else:
            logger.warning("⚠️ Frontend service disabled - Node.js not available")
            logger.info("💡 Install Node.js from https://nodejs.org/ to enable frontend")
        
        # Backend API Service (FastAPI) - Use simple API for reliability
        # The full api_server.py has complex dependencies that may fail
        # simple_api.py provides core functionality with fewer dependencies
        self.services["backend"] = ServiceConfig(
            name="Shujaa Studio Backend API",
            type=ServiceType.BACKEND,
            port=8000,
            command=[
                str(self.project_root / "shujaa_venv" / "Scripts" / "python.exe"),
                "simple_api.py"
            ],
            cwd=str(self.project_root),
            health_check_url="http://localhost:8000/health",
            startup_delay=8,
            required=True
        )
        
        # Gradio UI Service (Legacy/Backup)
        self.services["gradio"] = ServiceConfig(
            name="Shujaa Studio Gradio UI",
            type=ServiceType.GRADIO,
            port=7860,
            command=[
                str(self.project_root / "shujaa_venv" / "Scripts" / "python.exe"),
                "ui_clean.py"
            ],
            cwd=str(self.project_root),
            health_check_url="http://localhost:7860",
            startup_delay=6,
            required=False
        )
        
        logger.info(f"📋 Configured {len(self.services)} services for orchestration")

    def _check_node_available(self) -> bool:
        """Quick check if Node.js is available using enhanced detection"""
        node_path = shutil.which("node")
        if node_path:
            try:
                result = subprocess.run([node_path, "--version"], capture_output=True, timeout=5)
                return result.returncode == 0
            except Exception:
                return False
        return False

    def kill_port_processes(self, port: int) -> bool:
        """
        // [TASK]: Kill any processes using specified port
        // [GOAL]: Free ports for clean startup
        // [SNIPPET]: surgicalfix
        """
        killed = False
        try:
            for proc in psutil.process_iter():
                try:
                    # Get process connections safely
                    connections = proc.connections()
                    for conn in connections:
                        if conn.laddr.port == port:
                            logger.warning(f"🔥 Killing process {proc.pid} ({proc.name()}) using port {port}")
                            proc.kill()
                            killed = True
                            time.sleep(1)  # Give process time to die
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
                    continue
                except Exception:
                    continue
        except Exception as e:
            logger.error(f"Error killing processes on port {port}: {e}")

        return killed

    def check_port_available(self, port: int) -> bool:
        """Check if a port is available"""
        try:
            for proc in psutil.process_iter():
                try:
                    connections = proc.connections()
                    for conn in connections:
                        if conn.laddr.port == port:
                            return False
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
                    continue
                except Exception:
                    continue
            return True
        except Exception:
            return False

    def ensure_environment(self) -> bool:
        """
        // [TASK]: Ensure shujaa_venv is active and healthy
        // [GOAL]: Validate Python environment before startup
        // [SNIPPET]: guardon + kenyacheck
        """
        venv_path = self.project_root / "shujaa_venv"
        python_exe = venv_path / "Scripts" / "python.exe"
        
        if not venv_path.exists():
            logger.error("❌ shujaa_venv not found! Please run setup first.")
            return False
            
        if not python_exe.exists():
            logger.error("❌ Python executable not found in shujaa_venv!")
            return False
            
        # Test virtual environment
        try:
            result = subprocess.run(
                [str(python_exe), "-c", "import sys; print(sys.prefix)"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"✅ shujaa_venv is healthy: {result.stdout.strip()}")
                return True
            else:
                logger.error(f"❌ shujaa_venv test failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to test shujaa_venv: {e}")
            return False

    def check_node_installed(self) -> bool:
        """Check if Node.js and npm are installed using enhanced detection"""
        node_path = shutil.which("node")
        npm_path = shutil.which("npm")

        if not node_path:
            logger.error("❌ Node.js is not installed or not in PATH")
            logger.info("💡 Install Node.js from https://nodejs.org/")
            return False

        if not npm_path:
            logger.error("❌ npm is not installed or not in PATH")
            logger.info("💡 Install Node.js from https://nodejs.org/")
            return False

        try:
            # Test Node.js
            result = subprocess.run([node_path, "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                logger.error("❌ Node.js is not working properly")
                return False

            # Test npm
            result = subprocess.run([npm_path, "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                logger.error("❌ npm is not working properly")
                return False

            logger.info(f"✅ Node.js and npm are available: {node_path}, {npm_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Error checking Node.js/npm: {e}")
            return False

    def check_frontend_deps(self) -> bool:
        """Check if frontend dependencies are installed"""
        frontend_path = self.project_root / "frontend"
        node_modules = frontend_path / "node_modules"

        if not frontend_path.exists():
            logger.error("❌ Frontend directory not found!")
            return False

        # Check if Node.js is installed first
        if not self.check_node_installed():
            logger.error("❌ Please install Node.js from https://nodejs.org/")
            return False

        if not node_modules.exists():
            logger.warning("⚠️ Frontend node_modules not found. Installing...")
            try:
                result = subprocess.run(
                    ["npm", "install"],
                    cwd=str(frontend_path),
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutes timeout
                )
                if result.returncode == 0:
                    logger.info("✅ Frontend dependencies installed successfully")
                    return True
                else:
                    logger.error(f"❌ Failed to install frontend deps: {result.stderr}")
                    return False
            except Exception as e:
                logger.error(f"❌ Error installing frontend deps: {e}")
                return False

        logger.info("✅ Frontend dependencies are ready")
        return True

    async def start_service(self, service_name: str) -> bool:
        """
        // [TASK]: Start individual service with health monitoring
        // [GOAL]: Robust service startup with validation
        // [SNIPPET]: surgicalfix + perfcheck
        """
        if service_name not in self.services:
            logger.error(f"❌ Unknown service: {service_name}")
            return False
            
        service = self.services[service_name]
        
        # Kill any existing processes on the port
        if not self.check_port_available(service.port):
            logger.warning(f"🔥 Port {service.port} is busy. Clearing...")
            self.kill_port_processes(service.port)
            time.sleep(2)
        
        # Start the service
        try:
            logger.info(f"Starting {service.name} on port {service.port}...")
            
            env = os.environ.copy()
            if service.env:
                env.update(service.env)
            
            process = subprocess.Popen(
                service.command,
                cwd=service.cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[service_name] = process
            
            # Wait for startup
            await asyncio.sleep(service.startup_delay)
            
            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                logger.error(f"❌ {service.name} failed to start:")
                logger.error(f"STDOUT: {stdout}")
                logger.error(f"STDERR: {stderr}")
                return False
            
            # Health check if URL provided
            if service.health_check_url:
                if await self._health_check(service.health_check_url):
                    logger.info(f"✅ {service.name} is healthy and ready!")
                    return True
                else:
                    logger.warning(f"⚠️ {service.name} started but health check failed")
                    return not service.required  # Non-required services can fail health check
            else:
                logger.info(f"✅ {service.name} started successfully!")
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to start {service.name}: {e}")
            return False

    async def _health_check(self, url: str, max_retries: int = 10) -> bool:
        """Perform health check with retries"""
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    logger.info(f"✅ Health check passed for {url}")
                    return True
                else:
                    logger.warning(f"⚠️ Health check failed with status {response.status_code} for {url}")
            except requests.exceptions.ConnectionError:
                logger.debug(f"🔄 Health check attempt {attempt + 1}/{max_retries} - connection refused for {url}")
            except Exception as e:
                logger.debug(f"🔄 Health check attempt {attempt + 1}/{max_retries} - error: {e}")

            if attempt < max_retries - 1:
                await asyncio.sleep(3)

        logger.error(f"❌ Health check failed after {max_retries} attempts for {url}")
        return False

    async def start_all_services(self) -> bool:
        """
        // [TASK]: Start all services in correct order
        // [GOAL]: Orchestrated startup with dependency management
        // [SNIPPET]: taskchain + perfcheck + kenyafirst
        """
        logger.info("KE Starting Shujaa Studio Universal Server - Harambee!")

        # Pre-flight checks
        if not self.ensure_environment():
            logger.error("❌ Environment check failed!")
            return False

        # Only check frontend deps if frontend service is configured
        if "frontend" in self.services:
            if not self.check_frontend_deps():
                logger.error("❌ Frontend dependencies check failed!")
                return False
        else:
            logger.info("⏭️ Skipping frontend dependency check (frontend service not configured)")

        # Start services in order: Backend first, then Frontend, then optional services
        startup_order = ["backend", "frontend", "gradio"]

        for service_name in startup_order:
            if service_name in self.services:
                success = await self.start_service(service_name)
                if not success and self.services[service_name].required:
                    logger.error(f"❌ Required service {service_name} failed to start!")
                    await self.stop_all_services()
                    return False
                elif not success:
                    logger.warning(f"⚠️ Optional service {service_name} failed to start, continuing...")

        self.running = True
        logger.info("🎉 All services started successfully!")
        self._print_service_status()
        return True

    def _print_service_status(self):
        """Print current status of all services"""
        print("\n" + "=" * 80)
        print("KE SHUJAA STUDIO - UNIVERSAL SERVER STATUS")
        print("=" * 80)

        for service_name, service in self.services.items():
            if service_name in self.processes:
                process = self.processes[service_name]
                if process.poll() is None:
                    status = "✅ RUNNING"
                else:
                    status = "❌ STOPPED"
            else:
                status = "⏸️ NOT STARTED"

            print(f"  {service.name:<30} | Port {service.port:<5} | {status}")

        print("=" * 80)
        print("🌐 Access URLs:")
        print(f"  Frontend (React):     http://localhost:3000")
        print(f"  Backend API:          http://localhost:8000")
        print(f"  API Documentation:    http://localhost:8000/docs")
        print(f"  Gradio UI (Legacy):   http://localhost:7860")
        print("=" * 80)
        print("💡 Press Ctrl+C to stop all services")
        print("KE Harambee! - Together we build amazing AI videos!")
        print("=" * 80 + "\n")

    async def stop_service(self, service_name: str):
        """Stop a specific service"""
        if service_name in self.processes:
            process = self.processes[service_name]
            try:
                # Try graceful shutdown first
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful shutdown fails
                    process.kill()
                    process.wait()

                logger.info(f"🛑 Stopped {self.services[service_name].name}")
            except Exception as e:
                logger.error(f"Error stopping {service_name}: {e}")
            finally:
                del self.processes[service_name]

    async def stop_all_services(self):
        """Stop all running services"""
        logger.info("🛑 Stopping all services...")

        # Stop in reverse order
        service_names = list(self.processes.keys())
        service_names.reverse()

        for service_name in service_names:
            await self.stop_service(service_name)

        self.running = False
        logger.info("✅ All services stopped")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"🛑 Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop_all_services())
        sys.exit(0)

    async def monitor_services(self):
        """
        // [TASK]: Monitor service health and restart if needed
        // [GOAL]: Automatic recovery and health monitoring
        // [SNIPPET]: perfcheck + guardon
        """
        while self.running:
            try:
                for service_name, process in list(self.processes.items()):
                    if process.poll() is not None:
                        logger.warning(f"⚠️ Service {service_name} has stopped unexpectedly")

                        # Try to restart required services
                        service = self.services[service_name]
                        if service.required:
                            logger.info(f"🔄 Attempting to restart {service.name}...")
                            await self.start_service(service_name)

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"Error in service monitoring: {e}")
                await asyncio.sleep(30)

    async def run(self):
        """
        // [TASK]: Main execution loop
        // [GOAL]: Start services and monitor until shutdown
        // [SNIPPET]: taskchain + perfcheck
        """
        try:
            # Start all services
            if not await self.start_all_services():
                logger.error("❌ Failed to start services")
                return False

            # Start monitoring task
            monitor_task = asyncio.create_task(self.monitor_services())

            # Keep running until interrupted
            try:
                await monitor_task
            except KeyboardInterrupt:
                logger.info("🛑 Keyboard interrupt received")

        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
        finally:
            await self.stop_all_services()

        return True


def main():
    """
    // [TASK]: Entry point for universal server
    // [GOAL]: Command-line interface for server management
    // [SNIPPET]: kenyafirst + elitemode
    """
    import argparse

    # Fix Windows console encoding for emojis
    if sys.platform == "win32":
        try:
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Shujaa Studio Universal Server Manager - Harambee!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python universal_server.py                    # Start all services
  python universal_server.py --frontend-only   # Start only frontend
  python universal_server.py --backend-only    # Start only backend
  python universal_server.py --check           # Check system health
        """
    )

    parser.add_argument("--frontend-only", action="store_true",
                       help="Start only the frontend service")
    parser.add_argument("--backend-only", action="store_true",
                       help="Start only the backend service")
    parser.add_argument("--check", action="store_true",
                       help="Check system health and exit")
    parser.add_argument("--kill-ports", action="store_true",
                       help="Kill processes on ports 3000 and 8000")
    parser.add_argument("--full-api", action="store_true",
                       help="Use full api_server.py instead of simple_api.py")

    args = parser.parse_args()

    manager = UniversalServerManager()

    if args.check:
        try:
            print("🔍 Checking system health...")
        except UnicodeEncodeError:
            print("Checking system health...")

        env_ok = manager.ensure_environment()
        frontend_ok = manager.check_frontend_deps()

        try:
            print(f"Environment: {'✅' if env_ok else '❌'}")
            print(f"Frontend:    {'✅' if frontend_ok else '❌'}")
        except UnicodeEncodeError:
            print(f"Environment: {'OK' if env_ok else 'FAIL'}")
            print(f"Frontend:    {'OK' if frontend_ok else 'FAIL'}")

        if env_ok and frontend_ok:
            try:
                print("🎉 System is ready!")
            except UnicodeEncodeError:
                print("System is ready!")
            sys.exit(0)
        else:
            try:
                print("❌ System has issues")
            except UnicodeEncodeError:
                print("System has issues")
            sys.exit(1)

    if args.kill_ports:
        try:
            print("🔥 Killing processes on ports 3000 and 8000...")
        except UnicodeEncodeError:
            print("Killing processes on ports 3000 and 8000...")

        manager.kill_port_processes(3000)
        manager.kill_port_processes(8000)

        try:
            print("✅ Ports cleared")
        except UnicodeEncodeError:
            print("Ports cleared")
        sys.exit(0)

    if args.frontend_only:
        # Remove non-frontend services
        services_to_remove = [k for k in manager.services.keys() if k != "frontend"]
        for service in services_to_remove:
            del manager.services[service]

    if args.full_api and "backend" in manager.services:
        # Switch to full API server
        manager.services["backend"].command[-1] = "api_server.py"
        logger.info("🔧 Switched to full api_server.py")

    if args.backend_only:
        # Remove non-backend services
        services_to_remove = [k for k in manager.services.keys() if k != "backend"]
        for service in services_to_remove:
            del manager.services[service]

    # Run the server manager
    try:
        asyncio.run(manager.run())
    except KeyboardInterrupt:
        try:
            print("\n🛑 Shutdown complete. Asante sana!")
        except UnicodeEncodeError:
            print("\nShutdown complete. Asante sana!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
