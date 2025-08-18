import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiProvider(BaseProvider):
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.model_name = config.get("model_name")
        self.api_key = config.get("api_key")

        if not self.model_name:
            logger.warning(f"GeminiProvider {self.name}: 'model_name' not configured.")
        if not self.api_key:
            logger.warning(f"GeminiProvider {self.name}: 'api_key' not configured.")
        
        # Initialize Gemini client
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

    async def process_request(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"GeminiProvider {self.name}: Processing {task_type} request for model {self.model_name}.")
        try:
            if not self.model:
                raise ValueError("Gemini model not initialized. API key or model name might be missing.")
            
            if task_type == "text_generation":
                prompt = payload.get("prompt")
                if not prompt:
                    raise ValueError("Prompt is required for text generation.")
                
                # Use generate_content_async for async calls
                response = await self.model.generate_content_async(prompt)
                text_result = response.text
                
                response_data = {
                    "status": "success",
                    "provider": self.name,
                    "task_type": task_type,
                    "result": text_result
                }
            else:
                raise ValueError(f"Unsupported task type for Gemini: {task_type}")

            logger.info(f"GeminiProvider {self.name}: Request processed successfully.")
            return response_data
        except Exception as e:
            logger.error(f"GeminiProvider {self.name}: Failed to process request: {e}")
            raise

    async def check_health(self) -> bool:
        logger.info(f"GeminiProvider {self.name}: Checking health for model {self.model_name}.")
        try:
            if not self.model:
                logger.warning(f"GeminiProvider {self.name}: Model not initialized. Cannot check health.")
                return False
            
            # Attempt to list models as a lightweight health check
            # This requires a configured API key
            await genai.list_models()
            logger.info(f"GeminiProvider {self.name}: Health check successful.")
            return True
        except Exception as e:
            logger.error(f"GeminiProvider {self.name}: Health check failed: {e}")
            return False