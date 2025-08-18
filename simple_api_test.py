#!/usr/bin/env python3
"""
🚀 SIMPLE API TESTING - SHUJAA STUDIO
Elite Cursor Snippets Methodology Applied (Minimal Dependencies)

// [SNIPPET]: surgicalfix + thinkwithai + kenyafirst
// [CONTEXT]: Test APIs with minimal dependencies using built-in packages
// [GOAL]: Verify HuggingFace API connectivity without installing heavy packages
// [TASK]: Test basic API connectivity and model availability
// [CONSTRAINTS]: Use only built-in Python packages and system-installed ones
"""

import os
import sys
import time
import json
from pathlib import Path

# Use system-installed requests
try:
    import requests
    print("✅ Requests library available")
except ImportError:
    print("❌ Requests library not available")
    sys.exit(1)

class SimpleAPITester:
    """
    // [SNIPPET]: refactorclean + kenyafirst
    // [GOAL]: Simple API testing with minimal dependencies
    """
    
    def __init__(self):
        """Initialize the simple API tester"""
        self.hf_token = os.getenv('HF_API_KEY')
        self.test_results = {}
        self.start_time = time.time()
        
        # Load token from .env file if available
        env_file = Path('.env')
        if env_file.exists() and not self.hf_token:
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('HF_API_KEY=') and not line.strip().endswith('your_huggingface_token_here'):
                            self.hf_token = line.split('=', 1)[1].strip().strip('"\'')
                            break
            except Exception as e:
                print(f"⚠️ Could not read .env file: {e}")
        
    def print_header(self, title: str, emoji: str = "🚀"):
        """Print formatted header"""
        print(f"\n{emoji} {title.upper()}")
        print("=" * 60)
        
    def print_step(self, step: str, status: str = "🔄"):
        """Print test step"""
        print(f"{status} {step}")
        
    def print_result(self, test_name: str, success: bool, details: str = ""):
        """Print test result"""
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {'PASS' if success else 'FAIL'}")
        if details:
            print(f"   📝 {details}")

    def test_basic_connectivity(self) -> bool:
        """Test basic internet and HuggingFace connectivity"""
        self.print_header("Basic Connectivity Test", "🌐")
        
        # Test 1: Internet connectivity
        try:
            response = requests.get('https://httpbin.org/get', timeout=10)
            internet_ok = response.status_code == 200
            self.print_result("Internet connectivity", internet_ok, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Internet connectivity", False, str(e))
            internet_ok = False
            
        # Test 2: HuggingFace website
        try:
            response = requests.get('https://huggingface.co', timeout=10)
            hf_site_ok = response.status_code == 200
            self.print_result("HuggingFace website", hf_site_ok, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("HuggingFace website", False, str(e))
            hf_site_ok = False
            
        # Test 3: HuggingFace API endpoint
        try:
            response = requests.get('https://api-inference.huggingface.co/status', timeout=10)
            api_ok = response.status_code == 200
            self.print_result("HF API endpoint", api_ok, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("HF API endpoint", False, str(e))
            api_ok = False
            
        overall_success = internet_ok and hf_site_ok and api_ok
        self.test_results['connectivity'] = overall_success
        return overall_success

    def test_token_validation(self) -> bool:
        """Test HuggingFace token validation"""
        self.print_header("Token Validation", "🔑")
        
        if not self.hf_token or self.hf_token == "your_huggingface_token_here":
            self.print_result("Token availability", False, "No valid token found")
            self.test_results['token'] = False
            return False
            
        self.print_result("Token availability", True, f"Token length: {len(self.hf_token)} chars")
        
        # Test token with HF API
        try:
            headers = {"Authorization": f"Bearer {self.hf_token}"}
            response = requests.get(
                "https://api-inference.huggingface.co/whoami",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get('name', 'Unknown')
                self.print_result("Token validation", True, f"User: {username}")
                token_valid = True
            else:
                self.print_result("Token validation", False, f"HTTP {response.status_code}")
                token_valid = False
                
        except Exception as e:
            self.print_result("Token validation", False, str(e))
            token_valid = False
            
        self.test_results['token'] = token_valid
        return token_valid

    def test_model_access(self) -> bool:
        """Test access to specific models"""
        self.print_header("Model Access Test", "🤖")
        
        if not self.hf_token or self.hf_token == "your_huggingface_token_here":
            self.print_result("Model access", False, "No token for model testing")
            self.test_results['models'] = False
            return False
            
        # Test models that are commonly available
        test_models = [
            "gpt2",
            "distilgpt2", 
            "microsoft/DialoGPT-medium",
            "stabilityai/sdxl-turbo"
        ]
        
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        successful_models = 0
        
        for model_id in test_models:
            try:
                response = requests.get(
                    f"https://api-inference.huggingface.co/models/{model_id}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.print_result(f"Model {model_id}", True, "Accessible")
                    successful_models += 1
                else:
                    self.print_result(f"Model {model_id}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.print_result(f"Model {model_id}", False, str(e))
                
        success_rate = (successful_models / len(test_models)) * 100
        overall_success = successful_models > 0
        
        self.print_step(f"Model access rate: {successful_models}/{len(test_models)} ({success_rate:.1f}%)")
        self.test_results['models'] = overall_success
        return overall_success

    def test_inference_api(self) -> bool:
        """Test actual inference API calls"""
        self.print_header("Inference API Test", "⚡")
        
        if not self.hf_token or self.hf_token == "your_huggingface_token_here":
            self.print_result("Inference API", False, "No token for inference testing")
            self.test_results['inference'] = False
            return False
            
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        # Test text generation with a Kenya-first prompt
        try:
            payload = {
                "inputs": "Mount Kenya is a beautiful mountain in Kenya with",
                "parameters": {
                    "max_new_tokens": 20,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                "https://api-inference.huggingface.co/models/gpt2",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    self.print_result("Text generation", True, f"Generated {len(generated_text)} chars")
                    inference_ok = True
                else:
                    self.print_result("Text generation", False, "Invalid response format")
                    inference_ok = False
            else:
                self.print_result("Text generation", False, f"HTTP {response.status_code}")
                inference_ok = False
                
        except Exception as e:
            self.print_result("Text generation", False, str(e))
            inference_ok = False
            
        self.test_results['inference'] = inference_ok
        return inference_ok

def main():
    """Main testing function"""
    print("🇰🇪 SHUJAA STUDIO - SIMPLE API TESTING")
    print("🚀 Elite Cursor Snippets Methodology Applied")
    print("=" * 80)
    
    # Initialize tester
    tester = SimpleAPITester()
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    if tester.test_basic_connectivity():
        tests_passed += 1
        
    if tester.test_token_validation():
        tests_passed += 1
        
    if tester.test_model_access():
        tests_passed += 1
        
    if tester.test_inference_api():
        tests_passed += 1
    
    # Print results
    tester.print_header("Final Results", "🎯")
    
    success_rate = (tests_passed / total_tests) * 100
    print(f"📊 Tests passed: {tests_passed}/{total_tests} ({success_rate:.1f}%)")
    
    total_time = time.time() - tester.start_time
    print(f"⏱️ Total time: {total_time:.1f} seconds")
    
    if tests_passed >= 3:
        print("\n🎉 API TESTING SUCCESSFUL!")
        print("✅ HuggingFace APIs are working")
        print("🎬 Ready to test video generation")
    elif tests_passed >= 1:
        print(f"\n⚠️ PARTIAL SUCCESS ({tests_passed}/{total_tests})")
        print("🔧 Some APIs work, check token setup for full functionality")
    else:
        print("\n❌ API TESTING FAILED")
        print("🔧 Check internet connection and HF token setup")
        
    return tests_passed >= 1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
