from config_loader import get_config
from logging_setup import get_logger

# Import pipeline entrypoints (do not call them yet)
import news_video_generator
import offline_video_maker.generate_video
import cartoon_anime_pipeline
import generate_video # Original basic pipeline

logger = get_logger(__name__)
config = get_config()

class PipelineOrchestrator:
    """
    // [TASK]: Orchestrate pipeline selection based on configuration and input
    // [GOAL]: Provide a single entry point for video generation, routing to the appropriate pipeline
    """
    def __init__(self):
        self.pipelines = {
            "news_video_generator": news_video_generator.main, # Reference to the main async function
            "offline_video_maker": offline_video_maker.generate_video.main, # Reference to the main sync function
            "cartoon_anime_pipeline": cartoon_anime_pipeline.create_african_cartoon_video, # Reference to the main sync function
            "basic_video_generator": generate_video.create_gradio_interface # Reference to the gradio interface creator
        }
        logger.info("PipelineOrchestrator initialized.")

    def decide_pipeline(self, input_type, user_preferences=None):
        """
        // [TASK]: Implement pipeline selection logic
        // [GOAL]: Choose the best pipeline based on input type and user preferences
        """
        chosen_pipeline = None
        reason = ""

        if input_type == "news_url":
            chosen_pipeline = "news_video_generator"
            reason = "Input is a news URL, best handled by the API-first news pipeline."
        elif input_type == "script_file":
            # Decision logic for script files
            # For now, default to news_video_generator (which handles script files)
            chosen_pipeline = "news_video_generator"
            reason = "Input is a script file, routing to news pipeline for now."
        elif input_type == "cartoon_prompt":
            chosen_pipeline = "cartoon_anime_pipeline"
            reason = "Input is a cartoon prompt, routing to specialized cartoon pipeline."
        elif input_type == "general_prompt":
            # Decision logic for general prompts
            # Prioritize offline_video_maker if local models are configured and available
            if config.models.image_generation.local_fallback_path and config.models.voice_synthesis.local_fallback_path:
                chosen_pipeline = "offline_video_maker"
                reason = "General prompt, routing to advanced offline pipeline due to local model availability."
            else:
                chosen_pipeline = "basic_video_generator"
                reason = "General prompt, routing to basic video generator as no advanced offline models configured."
        else:
            chosen_pipeline = None
            reason = "Unknown input type."
        
        logger.info(f"Decision: Chosen pipeline: {chosen_pipeline}, Reason: {reason}")
        return {"chosen": chosen_pipeline, "reason": reason}

    async def run_pipeline(self, input_type, input_data, user_preferences=None):
        """
        // [TASK]: Run the chosen pipeline (dry-run for now)
        // [GOAL]: Demonstrate routing without actual execution
        """
        decision = self.decide_pipeline(input_type, user_preferences)
        chosen = decision["chosen"]
        reason = decision["reason"]

        if chosen:
            logger.info(f"Orchestrator will run pipeline: {chosen} (Reason: {reason})")
            # For now, only log the decision, do not call the pipeline
            # if chosen == "news_video_generator":
            #     await self.pipelines[chosen](news=input_data)
            # elif chosen == "offline_video_maker":
            #     self.pipelines[chosen](prompt=input_data)
            # elif chosen == "cartoon_anime_pipeline":
            #     self.pipelines[chosen](script=input_data)
            # elif chosen == "basic_video_generator":
            #     self.pipelines[chosen]() # This one creates a Gradio interface
            return decision
        else:
            logger.error(f"Failed to decide pipeline: {reason}")
            return decision

# Example usage (for dry-run verification)
async def main():
    orchestrator = PipelineOrchestrator()

    # Test cases
    print("\n--- Testing Pipeline Orchestrator (Dry Run) ---")

    # News URL
    decision = await orchestrator.run_pipeline("news_url", "https://example.com/news")
    print(f"Decision for News URL: {decision}")

    # Script File
    decision = await orchestrator.run_pipeline("script_file", "my_script.txt")
    print(f"Decision for Script File: {decision}")

    # Cartoon Prompt
    decision = await orchestrator.run_pipeline("cartoon_prompt", "A happy elephant in a Kenyan village")
    print(f"Decision for Cartoon Prompt: {decision}")

    # General Prompt (assuming no local models configured in config.yaml for advanced offline)
    decision = await orchestrator.run_pipeline("general_prompt", "A story about innovation in Africa")
    print(f"Decision for General Prompt (basic): {decision}")

    # General Prompt (assuming local models configured for advanced offline)
    # Temporarily modify config for testing
    config.models.image_generation.local_fallback_path = "/path/to/local/sdxl"
    config.models.voice_synthesis.local_fallback_path = "/path/to/local/bark"
    decision = await orchestrator.run_pipeline("general_prompt", "A story about innovation in Africa")
    print(f"Decision for General Prompt (advanced offline): {decision}")

    # Unknown type
    decision = await orchestrator.run_pipeline("unknown_type", "some data")
    print(f"Decision for Unknown Type: {decision}")

if __name__ == "__main__":
    asyncio.run(main())
