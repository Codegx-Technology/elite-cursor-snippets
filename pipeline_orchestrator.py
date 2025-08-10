from config_loader import get_config
from logging_setup import get_logger
import asyncio
import functools

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

    def decide_pipeline(self, input_type, user_preferences=None, api_call=False):
        """
        // [TASK]: Implement pipeline selection logic
        // [GOAL]: Choose the best pipeline based on input type, preferences, and execution context (API vs. other)
        """
        chosen_pipeline = None
        reason = ""

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
                # For API calls, fallback to the versatile news_video_generator if offline models aren't ready
                chosen_pipeline = "news_video_generator"
                reason = "General prompt from API, falling back to news_video_generator as advanced offline models are not configured."
            else:
                # For non-API calls (e.g., CLI), the Gradio UI is an acceptable fallback
                chosen_pipeline = "basic_video_generator"
                reason = "General prompt, routing to basic video generator as no advanced offline models configured."
        else:
            chosen_pipeline = None
            reason = "Unknown input type."
        
        logger.info(f"Decision: Chosen pipeline: {chosen_pipeline}, Reason: {reason}")
        return {"chosen": chosen_pipeline, "reason": reason}

    async def run_pipeline(self, input_type, input_data, user_preferences=None, api_call=False):
        """
        // [TASK]: Run the chosen pipeline with appropriate arguments and execution model (sync/async)
        // [GOAL]: Execute the selected pipeline and return its result
        """
        decision = self.decide_pipeline(input_type, user_preferences, api_call=api_call)
        chosen = decision["chosen"]
        reason = decision["reason"]

        if not chosen:
            logger.error(f"Failed to decide pipeline: {reason}")
            return {"status": "error", "message": f"Failed to decide pipeline: {reason}"}

        logger.info(f"Orchestrator will run pipeline: {chosen} (Reason: {reason})")
        
        result = None
        pipeline_kwargs = user_preferences or {}

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

    print("
--- Testing Pipeline Orchestrator (Execution) ---")

    # News URL
    decision = await orchestrator.run_pipeline("news_url", "https://example.com/news", api_call=True)
    print(f"Decision for News URL: {decision}")

    # Script File
    decision = await orchestrator.run_pipeline("script_file", "my_script.txt", api_call=True)
    print(f"Decision for Script File: {decision}")

    # Cartoon Prompt
    decision = await orchestrator.run_pipeline("cartoon_prompt", "A happy elephant in a Kenyan village", api_call=True)
    print(f"Decision for Cartoon Prompt: {decision}")

    # General Prompt (API call, no local models -> news_video_generator)
    decision = await orchestrator.run_pipeline("general_prompt", "A story about innovation in Africa", api_call=True)
    print(f"Decision for General Prompt (API Fallback): {decision}")
    
    # General Prompt (non-API call, no local models -> basic_video_generator)
    decision = await orchestrator.run_pipeline("general_prompt", "A story about innovation in Africa")
    print(f"Decision for General Prompt (Basic Fallback): {decision}")

    # General Prompt (assuming local models configured for advanced offline)
    config.models.image_generation.local_fallback_path = "/path/to/local/sdxl"
    config.models.voice_synthesis.local_fallback_path = "/path/to/local/bark"
    decision = await orchestrator.run_pipeline("general_prompt", "A story about innovation in Africa", api_call=True)
    print(f"Decision for General Prompt (Advanced Offline): {decision}")
    # Reset for other tests
    config.models.image_generation.local_fallback_path = ""
    config.models.voice_synthesis.local_fallback_path = ""

    # Unknown type
    decision = await orchestrator.run_pipeline("unknown_type", "some data", api_call=True)
    print(f"Decision for Unknown Type: {decision}")

if __name__ == "__main__":
    asyncio.run(main())
