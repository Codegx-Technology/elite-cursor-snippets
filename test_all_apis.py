#!/usr/bin/env python3
"""
🚀 COMPREHENSIVE API TESTING SUITE - SHUJAA STUDIO
Elite Cursor Snippets Methodology Applied

// [SNIPPET]: aihandle + thinkwithai + kenyafirst + surgicalfix
// [CONTEXT]: Complete API validation before video generation testing
// [GOAL]: Verify all HuggingFace APIs work without downloading models
// [TASK]: Test HF API connectivity, model access, and video generation pipeline
// [CONSTRAINTS]: No model downloads, use HF Inference API only
// [PROGRESS]: Phase 1 - API validation and connectivity testing
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

# Add project paths for imports
sys.path.append(str(Path(__file__).parent))

# Elite imports following Kenya-first principles
try:
    from huggingface_hub import HfApi, InferenceClient
    from config_loader import get_config
    from hf_utils import validate_hf_model_access, get_hf_model_info
    from logging_setup import get_logger
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Run: pip install -r requirements.txt")
    sys.exit(1)

# Initialize logger with Kenya-first approach
logger = get_logger(__name__)

class ShujaaAPITester:
    """
    // [SNIPPET]: refactorclean + kenyafirst + thinkwithai
    // [GOAL]: Comprehensive API testing with Kenya-first methodology
    // [CONSTRAINTS]: No model downloads, API-only testing
    """
    
    def __init__(self):
        """Initialize the API tester with elite configuration"""
        self.config = get_config()
        self.hf_token = os.getenv('HF_API_KEY') or self.config.api_keys.huggingface
        self.test_results = {}
        self.start_time = time.time()
        
        # Kenya-first test models (lightweight, API-accessible)
        self.test_models = {
            'text_generation': [
                'microsoft/DialoGPT-medium',
                'gpt2',
                'distilgpt2'
            ],
            'image_generation': [
                'stabilityai/stable-diffusion-xl-base-1.0',
                'runwayml/stable-diffusion-v1-5',
                'stabilityai/sdxl-turbo'
            ],
            'text_to_speech': [
                'microsoft/speecht5_tts',
                'facebook/mms-tts-eng'
            ],
            'speech_to_text': [
                'openai/whisper-tiny',
                'openai/whisper-base',
                'facebook/wav2vec2-base-960h'
            ]
        }
        
    def print_header(self, title: str, emoji: str = "🚀"):
        """Print formatted header with Kenya-first styling"""
        print(f"\n{emoji} {title.upper()}")
        print("=" * 60)
        
    def print_step(self, step: str, status: str = "🔄"):
        """Print test step with status"""
        print(f"{status} {step}")
        
    def print_result(self, test_name: str, success: bool, details: str = ""):
        """Print test result with Kenya-first formatting"""
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {'PASS' if success else 'FAIL'}")
        if details:
            print(f"   📝 {details}")
        
    def test_environment_setup(self) -> bool:
        """
        // [SNIPPET]: surgicalfix + guardon
        // [TASK]: Validate environment and configuration setup
        """
        self.print_header("Environment Setup Validation", "🔧")
        
        # Test 1: Python environment
        python_version = sys.version.split()[0]
        self.print_step(f"Python version: {python_version}")
        
        # Test 2: HuggingFace token
        if self.hf_token and self.hf_token != "${HF_API_KEY}":
            self.print_result("HF Token", True, f"Token length: {len(self.hf_token)} chars")
            token_valid = True
        else:
            self.print_result("HF Token", False, "No valid HF_API_KEY found")
            token_valid = False
            
        # Test 3: Required packages
        required_packages = ['requests', 'huggingface_hub', 'transformers']
        packages_ok = True
        
        for package in required_packages:
            try:
                __import__(package)
                self.print_result(f"Package {package}", True)
            except ImportError:
                self.print_result(f"Package {package}", False)
                packages_ok = False
                
        # Test 4: Internet connectivity
        try:
            response = requests.get('https://huggingface.co', timeout=10)
            internet_ok = response.status_code == 200
            self.print_result("Internet connectivity", internet_ok, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Internet connectivity", False, str(e))
            internet_ok = False
            
        overall_success = token_valid and packages_ok and internet_ok
        self.test_results['environment'] = overall_success
        return overall_success

    def test_hf_api_access(self) -> bool:
        """
        // [SNIPPET]: thinkwithai + surgicalfix
        // [TASK]: Test HuggingFace API access and authentication
        """
        self.print_header("HuggingFace API Access Testing", "🤖")
        
        if not self.hf_token or self.hf_token == "${HF_API_KEY}":
            self.print_result("HF API Access", False, "No valid token available")
            self.test_results['hf_api'] = False
            return False
            
        try:
            # Test HF API connection
            api = HfApi(token=self.hf_token)
            
            # Test 1: Get user info
            try:
                user_info = api.whoami()
                self.print_result("User authentication", True, f"User: {user_info.get('name', 'Unknown')}")
                auth_ok = True
            except Exception as e:
                self.print_result("User authentication", False, str(e))
                auth_ok = False
                
            # Test 2: List models (basic API functionality)
            try:
                models = list(api.list_models(limit=5))
                self.print_result("Model listing", True, f"Found {len(models)} models")
                listing_ok = True
            except Exception as e:
                self.print_result("Model listing", False, str(e))
                listing_ok = False
                
            # Test 3: Inference client initialization
            try:
                client = InferenceClient(token=self.hf_token)
                self.print_result("Inference client", True, "Client initialized successfully")
                client_ok = True
            except Exception as e:
                self.print_result("Inference client", False, str(e))
                client_ok = False
                
            overall_success = auth_ok and listing_ok and client_ok
            self.test_results['hf_api'] = overall_success
            return overall_success

        except Exception as e:
            self.print_result("HF API Access", False, f"General error: {e}")
            self.test_results['hf_api'] = False
            return False

    def test_model_access(self) -> bool:
        """
        // [SNIPPET]: patternmine + thinkwithai + kenyafirst
        // [TASK]: Test access to specific models needed for video generation
        """
        self.print_header("Model Access Validation", "🎨")

        if not self.hf_token or self.hf_token == "${HF_API_KEY}":
            self.print_result("Model Access", False, "No valid token for model testing")
            self.test_results['model_access'] = False
            return False

        successful_models = 0
        total_models = 0

        for category, models in self.test_models.items():
            self.print_step(f"Testing {category} models...")

            for model_id in models:
                total_models += 1
                try:
                    # Use the existing utility function
                    if validate_hf_model_access(model_id, self.hf_token):
                        self.print_result(f"{model_id}", True, "Access granted")
                        successful_models += 1
                    else:
                        self.print_result(f"{model_id}", False, "Access denied or model unavailable")
                except Exception as e:
                    self.print_result(f"{model_id}", False, f"Error: {e}")

        # Calculate success rate
        success_rate = (successful_models / total_models) * 100 if total_models > 0 else 0
        overall_success = success_rate >= 50  # At least 50% of models should be accessible

        self.print_step(f"Model access rate: {successful_models}/{total_models} ({success_rate:.1f}%)")
        self.test_results['model_access'] = overall_success
        return overall_success

    def test_inference_api(self) -> bool:
        """
        // [SNIPPET]: surgicalfix + thinkwithai + kenyafirst
        // [TASK]: Test actual inference API calls with Kenya-first content
        """
        self.print_header("Inference API Testing", "⚡")

        if not self.hf_token or self.hf_token == "${HF_API_KEY}":
            self.print_result("Inference API", False, "No valid token for inference testing")
            self.test_results['inference'] = False
            return False

        client = InferenceClient(token=self.hf_token)
        tests_passed = 0
        total_tests = 0

        # Test 1: Text generation with Kenya-first prompt
        total_tests += 1
        try:
            self.print_step("Testing text generation...")
            prompt = "Write a short story about Mount Kenya and its beautiful landscapes"

            response = client.text_generation(
                prompt=prompt,
                model="gpt2",
                max_new_tokens=50,
                temperature=0.7
            )

            if response and len(response.strip()) > 10:
                self.print_result("Text generation", True, f"Generated {len(response)} characters")
                tests_passed += 1
            else:
                self.print_result("Text generation", False, "Empty or invalid response")

        except Exception as e:
            self.print_result("Text generation", False, f"Error: {e}")

        # Test 2: Image generation (if available)
        total_tests += 1
        try:
            self.print_step("Testing image generation...")
            prompt = "Mount Kenya with snow-capped peaks, beautiful landscape"

            # Try to generate image via API
            response = client.text_to_image(
                prompt=prompt,
                model="stabilityai/sdxl-turbo"
            )

            if response:
                self.print_result("Image generation", True, "Image generated successfully")
                tests_passed += 1
            else:
                self.print_result("Image generation", False, "No image returned")

        except Exception as e:
            self.print_result("Image generation", False, f"Error: {e}")

        # Calculate success rate
        success_rate = (tests_passed / total_tests) * 100 if total_tests > 0 else 0
        overall_success = tests_passed > 0  # At least one inference test should pass

        self.print_step(f"Inference success rate: {tests_passed}/{total_tests} ({success_rate:.1f}%)")
        self.test_results['inference'] = overall_success
        return overall_success

    def test_video_generation_readiness(self) -> bool:
        """
        // [SNIPPET]: thinkwithai + kenyafirst + refactorclean
        // [TASK]: Test readiness for video generation pipeline
        """
        self.print_header("Video Generation Readiness", "🎬")

        readiness_checks = []

        # Check 1: Required directories exist
        required_dirs = ['temp', 'output', 'music']
        dirs_ok = True

        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                self.print_result(f"Directory {dir_name}", True, f"Path: {dir_path.absolute()}")
            else:
                self.print_result(f"Directory {dir_name}", False, "Missing - will be created")
                # Create the directory
                dir_path.mkdir(exist_ok=True)
                dirs_ok = False

        readiness_checks.append(dirs_ok)

        # Check 2: Configuration is valid
        try:
            config_valid = hasattr(self.config, 'models') and hasattr(self.config, 'video')
            self.print_result("Configuration", config_valid, "Config loaded successfully" if config_valid else "Config issues")
            readiness_checks.append(config_valid)
        except Exception as e:
            self.print_result("Configuration", False, f"Error: {e}")
            readiness_checks.append(False)

        # Check 3: Previous test results
        env_ok = self.test_results.get('environment', False)
        api_ok = self.test_results.get('hf_api', False)

        self.print_result("Environment tests", env_ok)
        self.print_result("API tests", api_ok)

        readiness_checks.extend([env_ok, api_ok])

        # Overall readiness
        overall_readiness = all(readiness_checks)
        self.test_results['video_readiness'] = overall_readiness

        if overall_readiness:
            self.print_step("🎉 System is ready for video generation!")
        else:
            self.print_step("🔧 Some issues need to be resolved before video generation")

        return overall_readiness

def main():
    """
    // [SNIPPET]: dailyboost + thinkwithai + kenyafirst
    // [TASK]: Run comprehensive API testing suite
    """
    print("🇰🇪 SHUJAA STUDIO - COMPREHENSIVE API TESTING")
    print("🚀 Elite Cursor Snippets Methodology Applied")
    print("=" * 80)

    # Initialize tester
    tester = ShujaaAPITester()

    # Run tests in sequence
    tests_passed = 0
    total_tests = 5

    # Test 1: Environment setup
    if tester.test_environment_setup():
        tests_passed += 1

    # Test 2: HF API access
    if tester.test_hf_api_access():
        tests_passed += 1

    # Test 3: Model access validation
    if tester.test_model_access():
        tests_passed += 1

    # Test 4: Inference API testing
    if tester.test_inference_api():
        tests_passed += 1

    # Test 5: Video generation readiness
    if tester.test_video_generation_readiness():
        tests_passed += 1

    # Print final results
    tester.print_header("Final Results", "🎯")

    success_rate = (tests_passed / total_tests) * 100
    print(f"📊 Tests passed: {tests_passed}/{total_tests} ({success_rate:.1f}%)")

    total_time = time.time() - tester.start_time
    print(f"⏱️ Total time: {total_time:.1f} seconds")

    # Detailed results breakdown
    print("\n📋 DETAILED RESULTS:")
    for test_name, result in tester.test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name.replace('_', ' ').title()}")

    if tests_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ APIs are ready for video generation testing")
        print("🎬 Next step: Run video generation pipeline tests")
        print("\n🚀 RECOMMENDED NEXT ACTIONS:")
        print("   1. Test video generation: python generate_video.py")
        print("   2. Test news video creation: python news_video_generator.py")
        print("   3. Run UI interface: python enhanced_shujaa_app.py")
    elif tests_passed >= 3:
        print(f"\n⚠️ PARTIAL SUCCESS ({tests_passed}/{total_tests} tests passed)")
        print("🔧 Some features may work, but fix failing tests for full functionality")
        print("✅ You can try basic video generation with limited features")
    else:
        print(f"\n❌ CRITICAL ISSUES ({total_tests - tests_passed} tests failed)")
        print("🔧 Fix the issues above before proceeding with video generation")
        print("📝 Check HuggingFace token and internet connectivity")

    return tests_passed >= 3  # Allow partial success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
