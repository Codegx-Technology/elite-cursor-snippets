#!/usr/bin/env python3
"""
// [TASK]: Comprehensive Healing Exercise for Shujaa Studio
// [GOAL]: Validate all changes maintain working state without breaking code
// [SNIPPET]: perfcheck + guardon + kenyafirst
// [CONTEXT]: Post-development validation and health check
// [PROGRESS]: Creating comprehensive system validation
// [NEXT]: Run all tests and validate system health
// [LOCATION]: Root directory - healing_exercise.py
"""

import os
import sys
import subprocess
import time
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ShujaaHealingExercise:
    """
    // [TASK]: Comprehensive system health validation
    // [GOAL]: Ensure all changes improve functionality without breaking code
    // [SNIPPET]: guardon + perfcheck + kenyafirst
    """
    
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.test_results = {}
        self.health_score = 0
        self.issues_found = []
        self.improvements_validated = []
        
        logger.info("🇰🇪 Shujaa Studio Healing Exercise Initiated - Harambee!")
    
    def test_universal_server_functionality(self) -> Tuple[bool, str]:
        """
        // [TASK]: Test universal server management system
        // [GOAL]: Validate server orchestration works correctly
        // [SNIPPET]: surgicalfix + perfcheck
        """
        try:
            # Test system health check
            result = subprocess.run(
                ["python", "universal_server.py", "--check"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.project_root)
            )
            
            if result.returncode == 0:
                return True, "Universal server health check passed"
            else:
                return False, f"Universal server health check failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Universal server test error: {e}"
    
    def test_backend_startup(self) -> Tuple[bool, str]:
        """
        // [TASK]: Test backend startup and health
        // [GOAL]: Validate backend can start without errors
        // [SNIPPET]: surgicalfix + perfcheck
        """
        try:
            # Start backend in background
            process = subprocess.Popen(
                ["python", "universal_server.py", "--backend-only"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.project_root)
            )
            
            # Wait for startup
            time.sleep(10)
            
            # Check if process is still running
            if process.poll() is None:
                # Try to connect to health endpoint
                try:
                    response = requests.get("http://localhost:8000/health", timeout=5)
                    if response.status_code == 200:
                        process.terminate()
                        process.wait(timeout=5)
                        return True, "Backend started successfully and health check passed"
                    else:
                        process.terminate()
                        process.wait(timeout=5)
                        return False, f"Backend health check failed with status {response.status_code}"
                except requests.exceptions.RequestException:
                    process.terminate()
                    process.wait(timeout=5)
                    return False, "Backend health endpoint not accessible"
            else:
                stdout, stderr = process.communicate()
                return False, f"Backend failed to start: {stderr}"
                
        except Exception as e:
            return False, f"Backend test error: {e}"
    
    def test_environment_health(self) -> Tuple[bool, str]:
        """
        // [TASK]: Test Python environment health
        // [GOAL]: Validate shujaa_venv is working correctly
        // [SNIPPET]: guardon + perfcheck
        """
        try:
            venv_path = self.project_root / "shujaa_venv"
            python_exe = venv_path / "Scripts" / "python.exe"
            
            if not venv_path.exists():
                return False, "shujaa_venv directory not found"
            
            if not python_exe.exists():
                return False, "Python executable not found in shujaa_venv"
            
            # Test virtual environment
            result = subprocess.run(
                [str(python_exe), "-c", "import sys; print('OK')"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, "Python environment is healthy"
            else:
                return False, f"Python environment test failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Environment test error: {e}"
    
    def test_unicode_encoding_fixes(self) -> Tuple[bool, str]:
        """
        // [TASK]: Test Unicode/emoji encoding fixes
        // [GOAL]: Validate emoji handling works on Windows
        // [SNIPPET]: surgicalfix + perfcheck
        """
        try:
            # Test simple API with emoji handling
            result = subprocess.run(
                [str(self.project_root / "shujaa_venv" / "Scripts" / "python.exe"), 
                 "-c", "import simple_api; print('Emoji test: 🇰🇪 🚀 ✅')"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=str(self.project_root)
            )
            
            if result.returncode == 0:
                return True, "Unicode/emoji encoding fixes working"
            else:
                return False, f"Unicode encoding test failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Unicode encoding test error: {e}"
    
    def test_port_management(self) -> Tuple[bool, str]:
        """
        // [TASK]: Test port management functionality
        // [GOAL]: Validate port conflict resolution works
        // [SNIPPET]: surgicalfix + perfcheck
        """
        try:
            # Test port killing functionality
            result = subprocess.run(
                ["python", "universal_server.py", "--kill-ports"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=str(self.project_root)
            )
            
            if result.returncode == 0:
                return True, "Port management functionality working"
            else:
                return False, f"Port management test failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Port management test error: {e}"
    
    def test_node_detection(self) -> Tuple[bool, str]:
        """
        // [TASK]: Test Node.js detection functionality
        // [GOAL]: Validate frontend dependency detection works
        // [SNIPPET]: surgicalfix + perfcheck
        """
        try:
            # This should fail gracefully since Node.js is not installed
            result = subprocess.run(
                ["python", "universal_server.py", "--frontend-only"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=str(self.project_root)
            )
            
            # Should fail but with proper error message
            if "Node.js" in result.stderr and "https://nodejs.org" in result.stderr:
                return True, "Node.js detection working correctly (proper error message)"
            else:
                return False, f"Node.js detection not working properly: {result.stderr}"
                
        except Exception as e:
            return False, f"Node.js detection test error: {e}"
    
    def run_comprehensive_healing(self) -> Dict[str, Any]:
        """
        // [TASK]: Run all healing tests
        // [GOAL]: Comprehensive system validation
        // [SNIPPET]: taskchain + perfcheck + guardon
        """
        
        print("\n" + "=" * 80)
        print("🇰🇪 SHUJAA STUDIO COMPREHENSIVE HEALING EXERCISE")
        print("=" * 80)
        
        tests = [
            ("Universal Server Functionality", self.test_universal_server_functionality),
            ("Environment Health", self.test_environment_health),
            ("Unicode Encoding Fixes", self.test_unicode_encoding_fixes),
            ("Port Management", self.test_port_management),
            ("Node.js Detection", self.test_node_detection),
            ("Backend Startup", self.test_backend_startup),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing: {test_name}")
            try:
                success, message = test_func()
                if success:
                    print(f"✅ PASS: {message}")
                    passed_tests += 1
                    self.improvements_validated.append(test_name)
                else:
                    print(f"❌ FAIL: {message}")
                    self.issues_found.append(f"{test_name}: {message}")
            except Exception as e:
                print(f"💥 ERROR: {test_name} - {e}")
                self.issues_found.append(f"{test_name}: Exception - {e}")
        
        # Calculate health score
        self.health_score = (passed_tests / total_tests) * 100
        
        # Generate summary
        print("\n" + "=" * 80)
        print("📊 HEALING EXERCISE SUMMARY")
        print("=" * 80)
        print(f"Health Score: {self.health_score:.1f}%")
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Improvements Validated: {len(self.improvements_validated)}")
        print(f"Issues Found: {len(self.issues_found)}")
        
        if self.health_score >= 80:
            print("🎉 EXCELLENT: System is in great health!")
        elif self.health_score >= 60:
            print("👍 GOOD: System is functional with minor issues")
        else:
            print("⚠️ NEEDS ATTENTION: System has significant issues")
        
        print("\n✅ VALIDATED IMPROVEMENTS:")
        for improvement in self.improvements_validated:
            print(f"  - {improvement}")
        
        if self.issues_found:
            print("\n⚠️ ISSUES FOUND:")
            for issue in self.issues_found:
                print(f"  - {issue}")
        
        print("\n🇰🇪 Harambee! Healing exercise complete!")
        print("=" * 80 + "\n")
        
        return {
            "health_score": self.health_score,
            "tests_passed": passed_tests,
            "total_tests": total_tests,
            "improvements_validated": self.improvements_validated,
            "issues_found": self.issues_found,
            "status": "healthy" if self.health_score >= 80 else "needs_attention"
        }


def main():
    """
    // [TASK]: Execute comprehensive healing exercise
    // [GOAL]: Validate system health and improvements
    // [SNIPPET]: elitemode + kenyafirst + guardon
    """
    
    healer = ShujaaHealingExercise()
    results = healer.run_comprehensive_healing()
    
    # Save results to file
    results_file = Path("healing_exercise_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"📄 Healing results saved to: {results_file}")
    
    # Exit with appropriate code
    sys.exit(0 if results["health_score"] >= 80 else 1)


if __name__ == "__main__":
    main()
