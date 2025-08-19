from config_loader import get_config
from logging_setup import get_logger
import asyncio
import functools
from enhanced_model_router import enhanced_router

# Import pipeline entrypoints (do not call them yet)
import news_video_generator
import offline_video_maker.generate_video
import cartoon_anime_pipeline
import generate_video # Original basic pipeline

# Import parallel processing utilities
from utils.parallel_processing import ParallelProcessor, SceneProcessor

logger = get_logger(__name__)
config = get_config()

class PipelineOrchestrator:
    """
    // [TASK]: Orchestrate pipeline selection and execution based on configuration and input
    // [GOAL]: Provide a single entry point for video generation, routing to the appropriate pipeline
    """
    def __init__(self):
        self.pipelines = {
            "news_video_generator": news_video_generator.main,
            "offline_video_maker": offline_video_maker.generate_video.main,
            "cartoon_anime_pipeline": cartoon_anime_pipeline.create_african_cartoon_video,
            "basic_video_generator": generate_video.create_gradio_interface
        }
        self.parallel_processor = ParallelProcessor()
        self.scene_processor = SceneProcessor()
        logger.info("PipelineOrchestrator initialized.")

    def decide_pipeline(self, config_dict: dict):
        """
        // [TASK]: Implement pipeline selection logic based on a single config dict
        // [GOAL]: Choose the best pipeline based on mode, resources, priority, and user-specified style
        // [ELITE_CURSOR_SNIPPET]: aihandle
        """
        mode = config_dict.get("mode")
        resources = config_dict.get("resources", "local") # Default to local
        priority = config_dict.get("priority", []) # Default to empty list
        user_style = config_dict.get("style") # For cartoon_prompt

        chosen_pipeline = None
        reason = ""

        # Prioritize based on mode
        if mode == "api":
            chosen_pipeline = "news_video_generator"
            reason = "API mode requested, routing to API-first news pipeline."
        elif mode == "offline":
            chosen_pipeline = "offline_video_maker"
            reason = "Offline mode requested, routing to advanced offline pipeline."
        elif mode == "cartoon":
            chosen_pipeline = "cartoon_anime_pipeline"
            reason = "Cartoon mode requested, routing to specialized cartoon pipeline."
        elif mode == "basic":
            chosen_pipeline = "basic_video_generator"
            reason = "Basic mode requested, routing to basic video generator."
        else: # Default decision based on input_type if mode is not explicit
            input_type = config_dict.get("input_type") # Assuming input_type is still passed for content
            api_call = config_dict.get("api_call", False)

            if input_type == "news_url":
                chosen_pipeline = "news_video_generator"
                reason = "Input is a news URL, best handled by the API-first news pipeline."
            elif input_type == "script_file":
                chosen_pipeline = "news_video_generator"
                reason = "Input is a script file, routing to news pipeline."
            elif input_type == "cartoon_prompt":
                chosen_pipeline = "cartoon_anime_pipeline"
                reason = "Input is a cartoon prompt, routing to specialized cartoon pipeline."
            elif input_type == "general_prompt":
                if config.models.image_generation.local_fallback_path and config.models.voice_synthesis.local_fallback_path:
                    chosen_pipeline = "offline_video_maker"
                    reason = "General prompt, routing to advanced offline pipeline due to local model availability."
                elif api_call:
                    chosen_pipeline = "news_video_generator"
                    reason = "General prompt from API, falling back to news_video_generator as advanced offline models are not configured."
                else:
                    chosen_pipeline = "basic_video_generator"
                    reason = "General prompt, routing to basic video generator as no advanced offline models configured."
            else:
                chosen_pipeline = None
                reason = "Unknown input type."

        # Further refine based on resources and priority if chosen_pipeline is still generic
        # This part would become more complex with a full priority array
        if chosen_pipeline == "news_video_generator" and resources == "local" and not config.models.text_generation.hf_api_id:
            # If API pipeline chosen but local resources preferred and no HF API key, try offline
            if config.models.image_generation.local_fallback_path and config.models.voice_synthesis.local_fallback_path:
                chosen_pipeline = "offline_video_maker"
                reason += " Overriding to offline due to local resource preference and missing HF API."

        logger.info(f"Decision: Chosen pipeline: {chosen_pipeline}, Reason: {reason}")
        return {"chosen": chosen_pipeline, "reason": reason}

    async def run_pipeline(self, input_type, input_data, user_preferences=None, api_call=False, request: Any = None): # Added request: Any
        """
        // [TASK]: Run the chosen pipeline with appropriate arguments and execution model (sync/async)
        // [GOAL]: Execute the selected pipeline and return its result
        """
        # Construct config_dict for decide_pipeline
        config_dict = {
            "input_type": input_type,
            "api_call": api_call,
            **(user_preferences or {})
        }
        decision = self.decide_pipeline(config_dict)
        chosen = decision["chosen"]
        reason = decision["reason"]

        if not chosen:
            logger.error(f"Failed to decide pipeline: {reason}")
            return {"status": "error", "message": f"Failed to decide pipeline: {reason}"}

        logger.info(f"Orchestrator will run pipeline: {chosen} (Reason: {reason})")
        
        result = None
        pipeline_kwargs = user_preferences or {}
        pipeline_kwargs['enhanced_router'] = enhanced_router
        pipeline_kwargs['parallel_processor'] = self.parallel_processor
        pipeline_kwargs['scene_processor'] = self.scene_processor
        pipeline_kwargs['request'] = request # Pass the request object

        try:
            if chosen == "news_video_generator":
                # This async pipeline can handle all input types and extra preferences
                result = await self.pipelines[chosen](
                    news=(input_data if input_type == 'news_url' else None),
                    script_file=(input_data if input_type == 'script_file' else None),
                    prompt=(input_data if input_type in ['general_prompt', 'cartoon_prompt'] else None),
                    **pipeline_kwargs
                )
            elif chosen == "offline_video_maker":
                # Run sync function in a separate thread to avoid blocking the event loop
                loop = asyncio.get_running_loop()
                func = functools.partial(self.pipelines[chosen], prompt=input_data, **pipeline_kwargs)
                result = await loop.run_in_executor(None, func)
            elif chosen == "cartoon_anime_pipeline":
                # Run sync function in a separate thread
                loop = asyncio.get_running_loop()
                func = functools.partial(self.pipelines[chosen], script=input_data, **pipeline_kwargs)
                result = await loop.run_in_executor(None, func)
            elif chosen == "basic_video_generator":
                logger.warning("Basic_video_generator (Gradio UI) cannot be executed from the API.")
                return {"status": "error", "message": "The selected pipeline is interactive and cannot be run from the API."}

            return {"status": "success", "pipeline": chosen, "result": result}

        except Exception as e:
            logger.exception(f"An error occurred while running pipeline '{chosen}': {e}")
            return {"status": "error", "pipeline": chosen, "message": f"An error occurred: {e}"}

# Example usage (for dry-run verification)
async def main():
    orchestrator = PipelineOrchestrator()

    print("--- Testing Pipeline Orchestrator (Execution) ---")

    # News URL
    decision = await orchestrator.run_pipeline(input_type="news_url", input_data="https://example.com/news", user_preferences={"mode": "api", "api_call": True})
    print(f"Decision for News URL: {decision}")

    # Script File
    decision = await orchestrator.run_pipeline(input_type="script_file", input_data="my_script.txt", user_preferences={"mode": "api", "api_call": True})
    print(f"Decision for Script File: {decision}")

    # Cartoon Prompt
    decision = await orchestrator.run_pipeline(input_type="cartoon_prompt", input_data="A happy elephant in a Kenyan village", user_preferences={"mode": "cartoon", "api_call": True})
    print(f"Decision for Cartoon Prompt: {decision}")

    # General Prompt (API call, no local models -> news_video_generator)
    decision = await orchestrator.run_pipeline(input_type="general_prompt", input_data="A story about innovation in Africa", user_preferences={"mode": "api", "api_call": True})
    print(f"Decision for General Prompt (API Fallback): {decision}")
    
    # General Prompt (non-API call, no local models -> basic_video_generator)
    decision = await orchestrator.run_pipeline(input_type="general_prompt", input_data="A story about innovation in Africa", user_preferences={"mode": "basic", "api_call": False})
    print(f"Decision for General Prompt (Basic Fallback): {decision}")

    # General Prompt (assuming local models configured for advanced offline)
    config.models.image_generation.local_fallback_path = "/path/to/local/sdxl"
    config.models.voice_synthesis.local_fallback_path = "/path/to/local/bark"
    decision = await orchestrator.run_pipeline(input_type="general_prompt", input_data="A story about innovation in Africa", user_preferences={"mode": "offline", "api_call": True})
    print(f"Decision for General Prompt (Advanced Offline): {decision}")
    # Reset for other tests
    config.models.image_generation.local_fallback_path = ""
    config.models.voice_synthesis.local_fallback_path = ""

    # Unknown type
    decision = await orchestrator.run_pipeline(input_type="unknown_type", input_data="some data", user_preferences={"mode": "unknown", "api_call": True})
    print(f"Decision for Unknown Type: {decision}")

if __name__ == "__main__":
    asyncio.run(main())
