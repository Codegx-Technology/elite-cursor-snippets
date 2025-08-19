"""
Enhanced Model Router for Shujaa Studio
Implements intelligent fallback strategy with Kenya-first approach
"""

import asyncio
import time
import hashlib
import json
import uuid # ADD THIS LINE
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import requests
from logging_setup import get_logger
from config_loader import get_config
from dialect_rag_manager import DialectRAGManager
from datetime import datetime # Added for rollback notification timestamp

# New imports for rollback and notifications
from backend.ai_health.rollback import should_rollback, perform_rollback
from backend.notifications.admin_notify import send_admin_notification

# [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent + augmentsearch
# [CONTEXT]: Enhanced model routing with intelligent fallbacks and Kenya-first design
# [GOAL]: Provide optimal video generation experience with cultural authenticity
# [TASK]: Implement smart routing, caching, and fallback strategies

logger = get_logger(__name__)
config = get_config()

class GenerationMethod(Enum):
    HUGGINGFACE_API = "huggingface_api"
    RUNPOD_API = "runpod_api"
    REPLICATE_API = "replicate_api"
    LOCAL_MODELS = "local_models"
    CACHED_CONTENT = "cached_content"
    FRIENDLY_FALLBACK = "friendly_fallback"
    GEMINI_API = "gemini_api"

@dataclass
class GenerationRequest:
    prompt: str
    type: str  # 'video', 'image', 'audio'
    user_id: Optional[str] = None
    preferences: Optional[Dict] = None
    cultural_preset: Optional[str] = None
    dialect: Optional[str] = None
    quality: str = "standard"  # 'draft', 'standard', 'premium'

@dataclass
class GenerationResult:
    success: bool
    content_url: Optional[str] = None
    method_used: Optional[GenerationMethod] = None
    generation_time: float = 0.0
    error_message: Optional[str] = None
    cached: bool = False
    metadata: Optional[Dict] = None
    provider_response_time: float = 0.0
    resource_usage: Optional[Dict] = None
    attempt_number: int = 1

class NetworkStatus:
    """Check network connectivity and service availability"""
    
    @staticmethod
    def check_connectivity() -> bool:
        """Check basic internet connectivity"""
        try:
            response = requests.get("https://httpbin.org/status/200", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def check_huggingface_status() -> bool:
        """Check HuggingFace API availability"""
        try:
            response = requests.get("https://huggingface.co/api/status", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def check_service_status(service_url: str) -> bool:
        """Check specific service availability"""
        try:
            response = requests.get(service_url, timeout=10)
            return response.status_code == 200
        except:
            return False

    @staticmethod
    def check_gemini_status() -> bool:
        """Check Gemini API availability"""
        try:
            # This is a placeholder. A real check would involve a small, quick API call.
            # For now, assume it's available if an API key is configured.
            from config_loader import get_config
            config = get_config()
            return hasattr(config.api_keys, 'gemini') and config.api_keys.gemini is not None
        except Exception as e:
            logger.error(f"Error checking Gemini status: {e}")
            return False

class ContentCache:
    """Intelligent content caching with semantic similarity"""
    
    def __init__(self):
        self.cache_storage = {}  # In production, use Redis or database
        self.similarity_threshold = 0.8
    
    def _generate_cache_key(self, request: GenerationRequest) -> str:
        """Generate cache key from request"""
        content = f"{request.prompt}_{request.type}_{request.cultural_preset}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _calculate_similarity(self, prompt1: str, prompt2: str) -> float:
        """Calculate semantic similarity between prompts"""
        # Simple word overlap similarity (in production, use embeddings)
        words1 = set(prompt1.lower().split())
        words2 = set(prompt2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def find_similar_content(self, request: GenerationRequest) -> Optional[GenerationResult]:
        """Find cached content similar to request"""
        for cached_key, cached_result in self.cache_storage.items():
            if cached_result.get('type') == request.type:
                similarity = self._calculate_similarity(
                    request.prompt, 
                    cached_result.get('prompt', '')
                )
                
                if similarity >= self.similarity_threshold:
                    logger.info(f"Found similar cached content (similarity: {similarity:.2f})")
                    return GenerationResult(
                        success=True,
                        content_url=cached_result['content_url'],
                        method_used=GenerationMethod.CACHED_CONTENT,
                        cached=True,
                        metadata={'similarity': similarity, 'original_prompt': cached_result['prompt']}
                    )
        
        return None
    
    def store_content(self, request: GenerationRequest, result: GenerationResult):
        """Store generated content in cache"""
        cache_key = self._generate_cache_key(request)
        self.cache_storage[cache_key] = {
            'prompt': request.prompt,
            'type': request.type,
            'content_url': result.content_url,
            'timestamp': time.time(),
            'method_used': result.method_used.value if result.method_used else None
        }
        logger.info(f"Stored content in cache: {cache_key}")

class EnhancedModelRouter:
    """Enhanced model router with intelligent fallback strategies"""
    
    def __init__(self):
        self.cache = ContentCache()
        self.network_status = NetworkStatus()
        self.generation_stats = {}
        self.dialect_rag_manager = DialectRAGManager()

        self.modality_fallback_map = {
            "video": ["image_audio", "image", "audio", "text"],
            "image": ["text"],
            "audio": ["text"],
            "text": []
        }
        
        self.historical_performance = {}
        
        # Default fallback chain - can be customized per user
        self.default_fallback_chain = [
            GenerationMethod.HUGGINGFACE_API,
            GenerationMethod.RUNPOD_API,
            GenerationMethod.LOCAL_MODELS,
            GenerationMethod.CACHED_CONTENT,
            GenerationMethod.FRIENDLY_FALLBACK
        ]

        # Rollback thresholds for each provider/model type
        self.rollback_thresholds = {
            "default": {
                "error_rate_threshold": 0.1, # 10% error rate
                "min_success_rate": 0.9,     # 90% success rate
                "max_avg_response_time": 15.0 # 15 seconds average response time
            },
            "huggingface_api": {
                "error_rate_threshold": 0.15,
                "min_success_rate": 0.85,
                "max_avg_response_time": 20.0
            },
            "gemini_api": {
                "error_rate_threshold": 0.08,
                "min_success_rate": 0.92,
                "max_avg_response_time": 10.0
            }
            # Add more specific thresholds for other providers/models as needed
        }
    
    def _assess_prompt_complexity(self, prompt: str) -> str:
        """Assess prompt complexity for resource planning"""
        word_count = len(prompt.split())
        
        if word_count < 10:
            return "simple"
        elif word_count < 30:
            return "moderate"
        else:
            return "complex"
    
    def _detect_kenya_elements(self, prompt: str) -> List[str]:
        """Detect Kenya-specific elements in prompt"""
        kenya_keywords = [
            'kenya', 'nairobi', 'mombasa', 'mount kenya', 'maasai mara', 
            'diani', 'swahili', 'harambee', 'safari', 'acacia', 'baobab',
            'kikuyu', 'luo', 'luhya', 'maasai', 'samburu'
        ]
        
        prompt_lower = prompt.lower()
        detected = [keyword for keyword in kenya_keywords if keyword in prompt_lower]
        
        return detected
    
    def _get_user_preferences(self, user_id: Optional[str]) -> Dict:
        """Get user-specific preferences"""
        # In production, fetch from database
        default_preferences = {
            'quality': 'standard',
            'prefer_local': False,
            'max_wait_time': 300,  # 5 minutes
            'fallback_to_cache': True,
            'cultural_enhancement': True
        }
        
        return default_preferences
    
    def _check_model_availability(self) -> Dict[str, bool]:
        """Check availability of different model types"""
        availability = {
            'hf_api': False,
            'runpod_api': False,
            'local_models': False,
            'network': False,
            'gemini_api': False
        }
        
        # Check network connectivity
        availability['network'] = self.network_status.check_connectivity()
        
        if availability['network']:
            # Check HuggingFace API
            availability['hf_api'] = self.network_status.check_huggingface_status()
            
            # Check RunPod API (if configured)
            if hasattr(config.api_keys, 'runpod') and config.api_keys.runpod:
                availability['runpod_api'] = True  # Assume available if key exists

            # Check Gemini API (if configured)
            availability['gemini_api'] = self.network_status.check_gemini_status()
        
        # Check local models
        try:
            from ai_model_manager import check_local_models_available
            availability['local_models'] = check_local_models_available()
        except ImportError:
            availability['local_models'] = False
        
        return availability
    
    async def analyze_request(self, request: GenerationRequest) -> Dict[str, Any]:
        """Analyze request to determine optimal generation strategy"""
        analysis = {
            'complexity': self._assess_prompt_complexity(request.prompt),
            'cultural_elements': self._detect_kenya_elements(request.prompt),
            'user_preferences': self._get_user_preferences(request.user_id),
            'model_availability': self._check_model_availability(),
            'estimated_resources': self._estimate_resources(request),
            'recommended_method': None
        }
        
        # Perform pre-generation quality check
        analysis['pre_gen_quality_assessment'] = self._pre_generate_quality_check(request, analysis)
        
        # Determine recommended method based on analysis
        if analysis['model_availability']['hf_api'] and not analysis['user_preferences']['prefer_local']:
            analysis['recommended_method'] = GenerationMethod.HUGGINGFACE_API
        elif analysis['model_availability']['local_models']:
            analysis['recommended_method'] = GenerationMethod.LOCAL_MODELS
        elif analysis['user_preferences']['fallback_to_cache']:
            analysis['recommended_method'] = GenerationMethod.CACHED_CONTENT
        else:
            analysis['recommended_method'] = GenerationMethod.FRIENDLY_FALLBACK
        
        return analysis
    
    def _estimate_resources(self, request: GenerationRequest) -> Dict[str, Any]:
        """Estimate resource requirements for request"""
        complexity = self._assess_prompt_complexity(request.prompt)
        
        resource_estimates = {
            'simple': {'time': 30, 'memory': '2GB', 'gpu': False},
            'moderate': {'time': 120, 'memory': '4GB', 'gpu': True},
            'complex': {'time': 300, 'memory': '8GB', 'gpu': True}
        }
        
        return resource_estimates.get(complexity, resource_estimates['moderate'])

    def _pre_generate_quality_check(self, request: GenerationRequest, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Perform quick quality checks on the input request before generation."""
        quality_assessment = {
            "status": "pass",
            "warnings": [],
            "suggestions": []
        }

        # Check 1: Prompt Ambiguity/Length
        if len(request.prompt.split()) < 5:
            quality_assessment["status"] = "warn"
            quality_assessment["warnings"].append("Prompt is very short, may lead to generic results.")
            quality_assessment["suggestions"].append("Try a more descriptive prompt (e.g., 'A vibrant market scene in Nairobi with people in traditional attire').")

        # Check 2: Unsupported Dialect
        # This assumes dialect_rag_manager has a way to check supported dialects
        # For now, a simple check against a hardcoded list or a mock.
        supported_dialects = ["kenyan english", "luo", "swahili"]
        if request.dialect and request.dialect.lower() not in supported_dialects:
            quality_assessment["status"] = "warn"
            quality_assessment["warnings"].append(f"Dialect '{request.dialect}' may not be fully supported, results might lack authenticity.")
            quality_assessment["suggestions"].append(f"Consider using one of the supported dialects: {', '.join(supported_dialects)}.")

        # Check 3: Resource vs. Complexity Mismatch (simple check)
        if analysis['complexity'] == "complex" and not analysis['model_availability'].get('gpu_available', False):
            quality_assessment["status"] = "warn"
            quality_assessment["warnings"].append("Complex prompt detected but GPU resources may be limited, generation might be slow or fail.")
            quality_assessment["suggestions"].append("Try a simpler prompt or ensure GPU resources are available.")

        logger.info(f"Pre-generation quality assessment: {quality_assessment}")
        return quality_assessment
    
    async def route_generation(self, request: GenerationRequest) -> GenerationResult:
        """Route generation request through optimal fallback chain"""
        start_time = time.time()
        all_attempts: List[GenerationResult] = [] # ADD THIS LINE
        
        # Analyze request
        analysis = await self.analyze_request(request)
        logger.info(f"Request analysis: {analysis['recommended_method']}")

        # Check pre-generation quality assessment
        pre_gen_assessment = analysis.get('pre_gen_quality_assessment', {})
        if pre_gen_assessment.get('status') == 'warn':
            logger.warning(f"Pre-generation quality warnings: {pre_gen_assessment.get('warnings')}")
            logger.info(f"Suggestions for prompt improvement: {pre_gen_assessment.get('suggestions')}")
        
        # Check cache first if enabled
        if analysis['user_preferences']['fallback_to_cache']:
            cached_result = self.cache.find_similar_content(request)
            if cached_result:
                cached_result.attempt_number = 1 # Set attempt number for cached result
                all_attempts.append(cached_result) # ADD THIS LINE
                logger.info("Serving cached content")
                # Log analytics for cached hit
                self._log_generation_analytics(request, cached_result, all_attempts) # ADD THIS LINE
                return cached_result
        
        # Get fallback chain based on analysis
        fallback_chain = self._get_fallback_chain(analysis)
        
        # Try each method in the fallback chain
        for i, method in enumerate(fallback_chain): # Modify loop to get attempt number
            attempt_result: GenerationResult = GenerationResult(success=False, method_used=method, attempt_number=i+1) # Initialize attempt result
            try:
                logger.info(f"Trying generation method: {method.value} (Attempt {i+1})") # Modify log message
                attempt_result = await self._try_generation_method(method, request, analysis)
                attempt_result.attempt_number = i+1 # Ensure attempt number is set
                all_attempts.append(attempt_result) # ADD THIS LINE
                
                if attempt_result.success:
                    attempt_result.generation_time = time.time() - start_time
                    
                    # Perform post-generation quality check
                    quality_report = {"status": "pass", "issues": []} # Default
                    if request.type == "image" or request.type == "video":
                        quality_report = self._check_visual_quality(attempt_result.content_url, attempt_result.metadata)
                    elif request.type == "audio":
                        quality_report = self._check_audio_quality(attempt_result.content_url, attempt_result.metadata)
                    elif request.type == "text":
                        quality_report = self._check_text_quality(attempt_result.content_url, attempt_result.metadata)
                    
                    attempt_result.metadata = {**(attempt_result.metadata or {}), "quality_report": quality_report} # Add quality report to metadata

                    if quality_report["status"] == "fail":
                        logger.warning(f"Post-generation quality check failed for {request.type} (Method: {method.value}). Issues: {quality_report['issues']}. Retrying with next method.")
                        attempt_result.success = False # Mark as failed to trigger retry
                        # Do not store in cache if quality failed
                        continue # Continue to next method in fallback chain
                    elif quality_report["status"] == "warn":
                        logger.warning(f"Post-generation quality check warned for {request.type} (Method: {method.value}). Issues: {quality_report['issues']}. Proceeding.")
                        # Still store in cache and return, but log warning
                    
                    # Store successful result in cache
                    if method != GenerationMethod.CACHED_CONTENT:
                        self.cache.store_content(request, attempt_result)
                    
                    logger.info(f"Generation successful with {method.value} in {attempt_result.generation_time:.2f}s (Attempt {i+1})") # Modify log message
                    self._log_generation_analytics(request, attempt_result, all_attempts) # ADD THIS LINE
                    return attempt_result
                
            except Exception as e:
                attempt_result.success = False # Ensure success is false on exception
                attempt_result.error_message = f"Generation method {method.value} failed: {str(e)}" # Capture error message
                attempt_result.generation_time = time.time() - start_time # Capture total time up to failure
                attempt_result.attempt_number = i+1 # Ensure attempt number is set
                all_attempts.append(attempt_result) # ADD THIS LINE
                logger.warning(f"Generation method {method.value} failed: {e} (Attempt {i+1})") # Modify log message
                continue
        
        # If original modality failed, try modality fallbacks
        modality_fallbacks = self.modality_fallback_map.get(request.type, [])
        for fallback_type in modality_fallbacks:
            logger.info(f"Original modality ({request.type}) failed. Trying fallback modality: {fallback_type}")
            fallback_request = GenerationRequest(
                prompt=request.prompt,
                type=fallback_type, # New modality type
                user_id=request.user_id,
                preferences=request.preferences,
                cultural_preset=request.cultural_preset,
                dialect=request.dialect,
                quality=request.quality
            )
            # Recursively call route_generation for the fallback modality
            fallback_result = await self.route_generation(fallback_request)
            if fallback_result.success:
                fallback_result.generation_time = time.time() - start_time # Update total time
                fallback_result.metadata = {"original_type": request.type, **(fallback_result.metadata or {})} # Add original type to metadata
                logger.info(f"Successfully generated content in fallback modality: {fallback_type}")
                # Analytics will be logged by the recursive call, but we can add a note here.
                return fallback_result
        
        # All methods and fallbacks failed, return friendly fallback
        final_result = await self._kenya_friendly_fallback(request)
        final_result.generation_time = time.time() - start_time # Capture total time
        final_result.attempt_number = len(fallback_chain) + 1 # Set attempt number for fallback
        all_attempts.append(final_result) # ADD THIS LINE
        self._log_generation_analytics(request, final_result, all_attempts) # ADD THIS LINE
        return final_result

    def _log_generation_analytics(self, request: GenerationRequest, final_result: GenerationResult, all_attempts: List[GenerationResult]):
        """Logs detailed analytics for a generation request and triggers rollback if necessary."""
        analytics_data = {
            "request_id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "prompt": request.prompt,
            "type": request.type,
            "dialect": request.dialect,
            "final_success": final_result.success,
            "final_method_used": final_result.method_used.value if final_result.method_used else "N/A",
            "total_generation_time": final_result.generation_time,
            "total_attempts": len(all_attempts),
            "attempts_details": []
        }
        
        # Aggregate metrics for the specific provider/model that was used
        # For simplicity, we'll aggregate based on the final_method_used
        # In a more complex system, you might aggregate per model within a provider
        provider_key = final_result.method_used.value if final_result.method_used else "N/A"
        
        # Initialize if not exists
        if provider_key not in self.historical_performance:
            self.historical_performance[provider_key] = {"success_count": 0, "fail_count": 0, "total_time": 0.0, "call_count": 0}
        
        # Update historical performance
        self.historical_performance[provider_key]["call_count"] += 1
        self.historical_performance[provider_key]["total_time"] += final_result.provider_response_time
        if final_result.success:
            self.historical_performance[provider_key]["success_count"] += 1
        else:
            self.historical_performance[provider_key]["fail_count"] += 1
        
        # Calculate aggregated metrics for rollback check
        current_stats = self.historical_performance[provider_key]
        total_calls = current_stats["call_count"]
        
        if total_calls > 0:
            error_rate = current_stats["fail_count"] / total_calls
            success_rate = current_stats["success_count"] / total_calls
            avg_response_time = current_stats["total_time"] / total_calls
        else:
            error_rate = 0.0
            success_rate = 1.0
            avg_response_time = 0.0

        aggregated_metrics = {
            "error_rate": error_rate,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time
        }

        # Get relevant thresholds
        thresholds = self.rollback_thresholds.get(provider_key, self.rollback_thresholds["default"])

        # Check for rollback condition
        if should_rollback(aggregated_metrics, thresholds):
            logger.warning(f"Rollback condition met for {provider_key}. Aggregated metrics: {aggregated_metrics}")
            rolled_back_to_tag = perform_rollback(provider_key, request.type) # Assuming request.type can act as model_name
            
            if rolled_back_to_tag:
                subject = f"🚨 Auto-rollback executed: {provider_key}/{request.type}"
                body = (
                    f"Model {provider_key}/{request.type} has been automatically rolled back.\n"
                    f"Metrics leading to rollback:\n"
                    f"  - Error Rate: {error_rate:.2f} (Threshold: {thresholds['error_rate_threshold']:.2f})\n"
                    f"  - Success Rate: {success_rate:.2f} (Threshold: {thresholds['min_success_rate']:.2f})\n"
                    f"  - Avg Response Time: {avg_response_time:.2f}s (Threshold: {thresholds['max_avg_response_time']:.2f}s)\n"
                    f"Rolled back to version: {rolled_back_to_tag}\n"
                    f"Time: {datetime.now().isoformat()}"
                )
                send_admin_notification(subject, body, metadata=aggregated_metrics)
                logger.info(f"Admin notification sent for rollback of {provider_key}/{request.type}.")
            else:
                logger.info(f"Rollback failed for {provider_key}/{request.type}. No notification sent.")
        
        for attempt in all_attempts:
            attempt_detail = {
                "attempt_number": attempt.attempt_number,
                "method_used": attempt.method_used.value if attempt.method_used else "N/A",
                "success": attempt.success,
                "provider_response_time": attempt.provider_response_time,
                "error_message": attempt.error_message,
                "cached": attempt.cached,
                "metadata": attempt.metadata
            }
            analytics_data["attempts_details"].append(attempt_detail)
            
        logger.info(f"GENERATION_ANALYTICS: {json.dumps(analytics_data, indent=2)}") # Log as JSON
        logger.debug(f"HISTORICAL_PERFORMANCE: {json.dumps(self.historical_performance, indent=2)}") # Log historical performance for debugging

    def _check_visual_quality(self, content_url: str, metadata: Dict) -> Dict:
        """Performs automated quality checks for visual content."""
        quality_report = {"status": "pass", "issues": []}
        # Placeholder for actual visual quality checks
        # In a real scenario, this would involve:
        # - Image analysis (e.g., using OpenCV for blur, contrast, object detection)
        # - Aspect ratio validation
        # - Watermark detection
        # - Checking for black/blank images
        
        if "placeholder" in content_url:
            quality_report["status"] = "fail"
            quality_report["issues"].append("Content is a placeholder image.")
        
        # Example: Check for very low resolution (assuming metadata contains resolution)
        if metadata and metadata.get("resolution"):
            width, height = metadata["resolution"]
            if width < 500 or height < 500:
                quality_report["status"] = "warn"
                quality_report["issues"].append(f"Low resolution detected: {width}x{height}.")

        logger.info(f"Visual quality check: {quality_report}")
        return quality_report

    def _check_audio_quality(self, content_url: str, metadata: Dict) -> Dict:
        """Performs automated quality checks for audio content."""
        quality_report = {"status": "pass", "issues": []}
        # Placeholder for actual audio quality checks
        # In a real scenario, this would involve:
        # - Audio analysis (e.g., using librosa for loudness, noise, silence detection)
        # - Speech recognition for clarity/intelligibility
        # - Dialect fidelity check (if applicable)
        
        if "silent" in content_url:
            quality_report["status"] = "fail"
            quality_report["issues"].append("Content is silent audio.")

        # Example: Check for very short audio (assuming metadata contains duration)
        if metadata and metadata.get("duration"):
            duration = metadata["duration"]
            if duration < 2.0:
                quality_report["status"] = "warn"
                quality_report["issues"].append(f"Very short audio detected: {duration:.2f}s.")

        logger.info(f"Audio quality check: {quality_report}")
        return quality_report

    def _check_text_quality(self, content_url: str, metadata: Dict) -> Dict:
        """Performs automated quality checks for text content."""
        quality_report = {"status": "pass", "issues": []}
        # Placeholder for actual text quality checks
        # In a real scenario, this would involve:
        # - Grammatical error checking (e.g., using language_tool_python)
        # - Coherence and relevance checks
        # - RAG accuracy verification (e.g., comparing generated text with RAG source)
        # - Dialect authenticity (e.g., using NLP models trained on specific dialects)
        
        if metadata and metadata.get("generated_text"):
            text = metadata["generated_text"]
            if len(text.split()) < 10:
                quality_report["status"] = "warn"
                quality_report["issues"].append("Very short generated text.")
            if "[RAG Context: No specific dialect context found" in text:
                quality_report["status"] = "warn"
                quality_report["issues"].append("RAG context was generic, dialect authenticity may be low.")

        logger.info(f"Text quality check: {quality_report}")
        return quality_report
    
    def _get_fallback_chain(self, analysis: Dict[str, Any]) -> List[GenerationMethod]:
        """Get customized fallback chain based on analysis and historical performance"""
        chain = []
        
        # Start with recommended method
        if analysis['recommended_method']:
            chain.append(analysis['recommended_method'])
        
        # Get available methods based on current model availability
        available_methods = []
        availability = analysis['model_availability']
        
        if availability['hf_api']:
            available_methods.append(GenerationMethod.HUGGINGFACE_API)
        if availability['gemini_api']:
            available_methods.append(GenerationMethod.GEMINI_API)
        if availability['runpod_api']:
            available_methods.append(GenerationMethod.RUNPOD_API)
        if availability['local_models']:
            available_methods.append(GenerationMethod.LOCAL_MODELS)
        
        # Sort available methods based on historical performance
        # Prioritize: higher success rate, lower average response time
        def sort_key(method: GenerationMethod):
            stats = self.historical_performance.get(method.value, {"success_count": 0, "fail_count": 0, "total_time": 0.0, "call_count": 0})
            
            success_rate = stats["success_count"] / stats["call_count"] if stats["call_count"] > 0 else 0.0
            average_time = stats["total_time"] / stats["call_count"] if stats["call_count"] > 0 else float('inf')
            
            # Simple scoring: higher success rate is better, lower time is better
            # You might want to adjust weights or use a more complex scoring function
            score = (success_rate * 100) - (average_time / 10) # Example scoring
            
            # Deprioritize methods with recent failures (e.g., if fail_count is high)
            if stats["fail_count"] > 5 and stats["call_count"] > 10: # Example threshold
                score -= 50 # Significant penalty for frequent failures
            
            return score

        # Sort in descending order of score
        sorted_available_methods = sorted(available_methods, key=sort_key, reverse=True)
        
        # Add sorted available methods to the chain, avoiding duplicates
        for method in sorted_available_methods:
            if method not in chain:
                chain.append(method)
        
        # Always include cache and friendly fallback at the end if not already present
        if GenerationMethod.CACHED_CONTENT not in chain:
            chain.append(GenerationMethod.CACHED_CONTENT)
        
        if GenerationMethod.FRIENDLY_FALLBACK not in chain: # Ensure friendly fallback is always last
            chain.append(GenerationMethod.FRIENDLY_FALLBACK)
        
        return chain
    
    async def _try_generation_method(
        self, 
        method: GenerationMethod, 
        request: GenerationRequest, 
        analysis: Dict[str, Any]
    ) -> GenerationResult:
        """Try specific generation method"""
        method_start_time = time.time()
        
        result = GenerationResult(success=False, method_used=method) # Initialize result

        try:
            if method == GenerationMethod.HUGGINGFACE_API:
                result = await self._try_huggingface_generation(request)
            elif method == GenerationMethod.RUNPOD_API:
                result = await self._try_runpod_generation(request)
            elif method == GenerationMethod.LOCAL_MODELS:
                result = await self._try_local_generation(request)
            elif method == GenerationMethod.CACHED_CONTENT:
                cached = self.cache.find_similar_content(request)
                result = cached or GenerationResult(success=False, error_message="No cached content found")
            elif method == GenerationMethod.FRIENDLY_FALLBACK:
                result = await self._kenya_friendly_fallback(request)
            elif method == GenerationMethod.GEMINI_API:
                result = await self._try_gemini_generation(request)
            else:
                result = GenerationResult(success=False, error_message=f"Unknown method: {method}")
            
            # Populate common fields
            result.method_used = method # Ensure method_used is set
            result.provider_response_time = time.time() - method_start_time # ADD THIS LINE
            # Placeholder for resource_usage - would be populated by specific generation methods
            
            return result

        except Exception as e:
            result.success = False
            result.error_message = f"Generation method {method.value} failed: {str(e)}"
            result.provider_response_time = time.time() - method_start_time # ADD THIS LINE
            logger.warning(f"Generation method {method.value} failed: {e}") # Keep existing warning
            return result
    
    async def _try_huggingface_generation(self, request: GenerationRequest) -> GenerationResult:
        """Try HuggingFace API generation"""
        try:
            from ai_model_manager import generate_text, generate_image, generate_speech
            
            if request.type == "video":
                # For video, we need to orchestrate multiple models
                from pipeline_orchestrator import PipelineOrchestrator
                orchestrator = PipelineOrchestrator()
                
                result = await orchestrator.run_pipeline(
                    input_type="general_prompt",
                    input_data=request.prompt,
                    user_preferences=request.preferences or {}
                )
                
                if result.get("status") == "success":
                    return GenerationResult(
                        success=True,
                        content_url=result.get("video_path"),
                        method_used=GenerationMethod.HUGGINGFACE_API
                    )
                else:
                    return GenerationResult(
                        success=False,
                        error_message=result.get("message", "HF generation failed")
                    )
            
            elif request.type == "image":
                image_bytes = await generate_image(request.prompt)
                if image_bytes:
                    # Save image and return URL (implement actual file saving)
                    content_url = f"/generated/images/{int(time.time())}.png"
                    return GenerationResult(
                        success=True,
                        content_url=content_url,
                        method_used=GenerationMethod.HUGGINGFACE_API
                    )
            
            elif request.type == "audio":
                audio_bytes = await generate_speech(request.prompt)
                if audio_bytes:
                    # Save audio and return URL (implement actual file saving)
                    content_url = f"/generated/audio/{int(time.time())}.mp3"
                    return GenerationResult(
                        success=True,
                        content_url=content_url,
                        method_used=GenerationMethod.HUGGINGFACE_API
                    )

            elif request.type == "text": # ADD THIS BLOCK
                generated_text = await generate_text(request.prompt)
                if generated_text:
                    # Enrich text with RAG if dialect is specified
                    if request.dialect:
                        enriched_text = self.dialect_rag_manager.enrich_text(generated_text, request.dialect, request.prompt)
                    else:
                        enriched_text = generated_text
                    
                    # For text, we can return the content directly or save it to a file
                    # For now, let's return it as a data URL or similar for simplicity
                    # In a real scenario, you might save it to a file and return a URL
                    content_url = f"data:text/plain;charset=utf-8,{enriched_text}"
                    return GenerationResult(
                        success=True,
                        content_url=content_url,
                        method_used=GenerationMethod.HUGGINGFACE_API,
                        metadata={"generated_text": enriched_text}
                    )
            
            return GenerationResult(success=False, error_message="HF generation returned no content")
            
        except Exception as e:
            return GenerationResult(success=False, error_message=f"HF API error: {str(e)}")
    
    async def _try_gemini_generation(self, request: GenerationRequest) -> GenerationResult:
        """Try Gemini API generation"""
        try:
            # Assuming a Gemini API client is available or can be imported
            # from ai_model_manager import generate_text_gemini, generate_image_gemini, generate_speech_gemini, generate_video_gemini

            if request.type == "video":
                # Placeholder for Gemini video generation
                # In a real scenario, this would call a Gemini video API
                logger.info(f"Attempting Gemini video generation for: {request.prompt}")
                # Simulate success for now
                content_url = f"/generated/gemini/video/{int(time.time())}.mp4"
                return GenerationResult(
                    success=True,
                    content_url=content_url,
                    method_used=GenerationMethod.GEMINI_API,
                    metadata={"note": "Gemini video generation simulated"}
                )

            elif request.type == "image":
                # Placeholder for Gemini image generation
                logger.info(f"Attempting Gemini image generation for: {request.prompt}")
                # Simulate success for now
                content_url = f"/generated/gemini/images/{int(time.time())}.png"
                return GenerationResult(
                    success=True,
                    content_url=content_url,
                    method_used=GenerationMethod.GEMINI_API,
                    metadata={"note": "Gemini image generation simulated"}
                )

            elif request.type == "audio":
                # Placeholder for Gemini audio generation (TTS)
                logger.info(f"Attempting Gemini audio generation for: {request.prompt}")
                # Simulate success for now
                content_url = f"/generated/gemini/audio/{int(time.time())}.mp3"
                return GenerationResult(
                    success=True,
                    content_url=content_url,
                    method_used=GenerationMethod.GEMINI_API,
                    metadata={"note": "Gemini audio generation simulated"}
                )

            elif request.type == "text":
                # Placeholder for Gemini text generation
                logger.info(f"Attempting Gemini text generation for: {request.prompt}")
                generated_text = f"Gemini generated text for: {request.prompt}" # Simulate text generation
                
                if generated_text:
                    # Enrich text with RAG if dialect is specified
                    if request.dialect:
                        enriched_text = self.dialect_rag_manager.enrich_text(generated_text, request.dialect, request.prompt)
                    else:
                        enriched_text = generated_text
                    
                    content_url = f"data:text/plain;charset=utf-8,{enriched_text}"
                    return GenerationResult(
                        success=True,
                        content_url=content_url,
                        method_used=GenerationMethod.GEMINI_API,
                        metadata={"generated_text": enriched_text, "note": "Gemini text generation simulated"}
                    )
            
            return GenerationResult(success=False, error_message="Gemini generation returned no content")
            
        except Exception as e:
            return GenerationResult(success=False, error_message=f"Gemini API error: {str(e)}")
    
    async def _try_runpod_generation(self, request: GenerationRequest) -> GenerationResult:
        """Try RunPod API generation"""
        # TODO: Implement RunPod API integration
        return GenerationResult(success=False, error_message="RunPod integration not implemented yet")
    
    async def _try_local_generation(self, request: GenerationRequest) -> GenerationResult:
        """Try local model generation"""
        try:
            from ai_model_manager import generate_image, generate_speech
            
            if request.type == "image":
                image_bytes = await generate_image(request.prompt, use_local_fallback=True)
                if image_bytes:
                    content_url = f"/generated/local/images/{int(time.time())}.png"
                    return GenerationResult(
                        success=True,
                        content_url=content_url,
                        method_used=GenerationMethod.LOCAL_MODELS
                    )
            
            elif request.type == "audio":
                audio_bytes = await generate_speech(request.prompt, use_local_fallback=True)
                if audio_bytes:
                    content_url = f"/generated/local/audio/{int(time.time())}.mp3"
                    return GenerationResult(
                        success=True,
                        content_url=content_url,
                        method_used=GenerationMethod.LOCAL_MODELS
                    )
            
            return GenerationResult(success=False, error_message="Local generation returned no content")
            
        except Exception as e:
            return GenerationResult(success=False, error_message=f"Local generation error: {str(e)}")
    
    async def _kenya_friendly_fallback(self, request: GenerationRequest) -> GenerationResult:
        """Provide Kenya-first friendly fallback experience"""
        cultural_messages = [
            "Pole sana! Our AI is taking a short break like a safari rest stop. 🦁",
            "Harambee! Great content takes time, just like climbing Mount Kenya! 🏔️",
            "Hakuna matata! We're working hard to bring you amazing content. 🇰🇪",
            "Like the Maasai Mara migration, good things are worth waiting for! 🦓",
            "Asante for your patience! Our AI is gathering inspiration from Kenya's beauty. 🌅"
        ]
        
        import random
        message = random.choice(cultural_messages)
        
        return GenerationResult(
            success=False,
            method_used=GenerationMethod.FRIENDLY_FALLBACK,
            error_message="Service temporarily unavailable",
            metadata={
                'friendly_message': message,
                'spinner_type': 'kenya_flag',
                'retry_options': [
                    'Try again in a moment',
                    'Use offline mode',
                    'Browse existing content'
                ],
                'estimated_wait': 'A few minutes',
                'support_message': 'Harambee! We\'re working to get you back creating.'
            }
        )

# Global router instance
enhanced_router = EnhancedModelRouter()
