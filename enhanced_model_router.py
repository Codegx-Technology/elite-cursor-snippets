"""
Enhanced Model Router for Shujaa Studio
Implements intelligent fallback strategy with Kenya-first approach
"""

import asyncio
import time
import hashlib
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import requests
from logging_setup import get_logger
from config_loader import get_config

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

@dataclass
class GenerationRequest:
    prompt: str
    type: str  # 'video', 'image', 'audio'
    user_id: Optional[str] = None
    preferences: Optional[Dict] = None
    cultural_preset: Optional[str] = None
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
        
        # Default fallback chain - can be customized per user
        self.default_fallback_chain = [
            GenerationMethod.HUGGINGFACE_API,
            GenerationMethod.RUNPOD_API,
            GenerationMethod.LOCAL_MODELS,
            GenerationMethod.CACHED_CONTENT,
            GenerationMethod.FRIENDLY_FALLBACK
        ]
    
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
            'network': False
        }
        
        # Check network connectivity
        availability['network'] = self.network_status.check_connectivity()
        
        if availability['network']:
            # Check HuggingFace API
            availability['hf_api'] = self.network_status.check_huggingface_status()
            
            # Check RunPod API (if configured)
            if hasattr(config.api_keys, 'runpod') and config.api_keys.runpod:
                availability['runpod_api'] = True  # Assume available if key exists
        
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
    
    async def route_generation(self, request: GenerationRequest) -> GenerationResult:
        """Route generation request through optimal fallback chain"""
        start_time = time.time()
        
        # Analyze request
        analysis = await self.analyze_request(request)
        logger.info(f"Request analysis: {analysis['recommended_method']}")
        
        # Check cache first if enabled
        if analysis['user_preferences']['fallback_to_cache']:
            cached_result = self.cache.find_similar_content(request)
            if cached_result:
                logger.info("Serving cached content")
                return cached_result
        
        # Get fallback chain based on analysis
        fallback_chain = self._get_fallback_chain(analysis)
        
        # Try each method in the fallback chain
        for method in fallback_chain:
            try:
                logger.info(f"Trying generation method: {method.value}")
                result = await self._try_generation_method(method, request, analysis)
                
                if result.success:
                    result.generation_time = time.time() - start_time
                    
                    # Store successful result in cache
                    if method != GenerationMethod.CACHED_CONTENT:
                        self.cache.store_content(request, result)
                    
                    logger.info(f"Generation successful with {method.value} in {result.generation_time:.2f}s")
                    return result
                
            except Exception as e:
                logger.warning(f"Generation method {method.value} failed: {e}")
                continue
        
        # All methods failed, return friendly fallback
        return await self._kenya_friendly_fallback(request)
    
    def _get_fallback_chain(self, analysis: Dict[str, Any]) -> List[GenerationMethod]:
        """Get customized fallback chain based on analysis"""
        chain = []
        
        # Start with recommended method
        if analysis['recommended_method']:
            chain.append(analysis['recommended_method'])
        
        # Add other methods based on availability
        availability = analysis['model_availability']
        
        if availability['hf_api'] and GenerationMethod.HUGGINGFACE_API not in chain:
            chain.append(GenerationMethod.HUGGINGFACE_API)
        
        if availability['runpod_api'] and GenerationMethod.RUNPOD_API not in chain:
            chain.append(GenerationMethod.RUNPOD_API)
        
        if availability['local_models'] and GenerationMethod.LOCAL_MODELS not in chain:
            chain.append(GenerationMethod.LOCAL_MODELS)
        
        # Always include cache and friendly fallback
        if GenerationMethod.CACHED_CONTENT not in chain:
            chain.append(GenerationMethod.CACHED_CONTENT)
        
        chain.append(GenerationMethod.FRIENDLY_FALLBACK)
        
        return chain
    
    async def _try_generation_method(
        self, 
        method: GenerationMethod, 
        request: GenerationRequest, 
        analysis: Dict[str, Any]
    ) -> GenerationResult:
        """Try specific generation method"""
        
        if method == GenerationMethod.HUGGINGFACE_API:
            return await self._try_huggingface_generation(request)
        elif method == GenerationMethod.RUNPOD_API:
            return await self._try_runpod_generation(request)
        elif method == GenerationMethod.LOCAL_MODELS:
            return await self._try_local_generation(request)
        elif method == GenerationMethod.CACHED_CONTENT:
            cached = self.cache.find_similar_content(request)
            return cached or GenerationResult(success=False, error_message="No cached content found")
        elif method == GenerationMethod.FRIENDLY_FALLBACK:
            return await self._kenya_friendly_fallback(request)
        else:
            return GenerationResult(success=False, error_message=f"Unknown method: {method}")
    
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
            
            return GenerationResult(success=False, error_message="HF generation returned no content")
            
        except Exception as e:
            return GenerationResult(success=False, error_message=f"HF API error: {str(e)}")
    
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
