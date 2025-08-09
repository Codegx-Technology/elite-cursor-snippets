#!/usr/bin/env python3
"""
🧪 Complete Pipeline Integration Test
Test all components: Standard + News + Elite Movies
"""

import asyncio
import json
from pathlib import Path


# Test without gradio first
def test_elite_movie_pipeline():
    """Test elite movie generation directly"""
    print("🎬 Testing Elite Script-to-Movie Pipeline")
    print("=" * 60)

    try:
        from elite_script_movie_pipeline import EliteMovieGenerator

        # Test with African story
        test_script = """
        TECH ENTREPRENEUR'S DREAM
        
        In the heart of Nairobi's bustling tech scene, Zawadi, a brilliant young programmer, 
        dreams of creating an app that connects rural farmers with urban markets.
        
        "Ubuntu means 'I am because we are'," her grandmother tells her. 
        "Your success must lift the entire community."
        
        Despite facing funding challenges and skeptical investors, Zawadi perseveres.
        She codes late into the night, fueled by chapati and determination.
        
        When she finally launches "Mazao Connect," it revolutionizes agriculture across Kenya.
        Her app becomes the bridge between tradition and technology.
        
        Zawadi's story proves that African innovation can change the world.
        """

        async def run_test():
            generator = EliteMovieGenerator()
            result = await generator.generate_movie_from_script(
                test_script, "cinematic", 8  # 8 minute limit
            )

            print(f"\n🎯 Result: {result['status']}")
            if result["status"] == "success":
                print(f"📊 Movie: {result['movie_path']}")
                print(f"🎬 Scenes: {result['scenes_generated']}")
                print(f"⏱️ Time: {result['processing_time']:.2f}s")
                print(f"🚀 GPU: {result['gpu_accelerated']}")

                # Check actual files
                movie_dir = Path("output/movies")
                if movie_dir.exists():
                    files = list(movie_dir.glob("*zawadi*"))
                    if not files:
                        files = list(movie_dir.glob("*tech_entrepreneur*"))
                    if not files:
                        files = list(movie_dir.glob("*.json"))[-3:]  # Last 3 files

                    print(f"\n📁 Generated Files:")
                    for file in files:
                        print(f"   {file.name}")

                # Test GPU + News integration
                print(f"\n🧪 Testing News Integration...")
                from news_to_video import NewsVideoInterface

                news_interface = NewsVideoInterface()

                news_result = await news_interface.quick_news_video(
                    "Kenya's tech sector shows 40% growth with young entrepreneurs leading innovation",
                    "business",
                    25,
                )

                print(f"📰 News Result: {news_result['status']}")
                if news_result["status"] == "success":
                    print(f"📊 News Output: {news_result['output_path']}")

                return True
            else:
                print(f"❌ Error: {result.get('error', 'Unknown')}")
                return False

        return asyncio.run(run_test())

    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False


def test_system_integration():
    """Test system components integration"""
    print(f"\n🔧 Testing System Integration")
    print("=" * 40)

    # Test GPU fallback
    try:
        from gpu_fallback import ShujaaGPUIntegration

        gpu = ShujaaGPUIntegration()
        status = gpu.get_integration_status()
        print(f"✅ GPU Integration: {status['status']}")
    except Exception as e:
        print(f"❌ GPU Integration: {e}")

    # Test news processor
    try:
        from news_to_video import NewsContentProcessor

        processor = NewsContentProcessor()
        print(f"✅ News Processor: Ready")
    except Exception as e:
        print(f"❌ News Processor: {e}")

    # Test elite movie processor
    try:
        from elite_script_movie_pipeline import EliteScriptProcessor

        script_processor = EliteScriptProcessor()
        print(f"✅ Elite Script Processor: Ready")
    except Exception as e:
        print(f"❌ Elite Script Processor: {e}")


def test_file_outputs():
    """Check what files have been generated"""
    print(f"\n📁 Checking Generated Files")
    print("=" * 40)

    output_dir = Path("output")
    if output_dir.exists():
        # Check news videos
        news_dir = output_dir / "news_videos"
        if news_dir.exists():
            news_files = list(news_dir.glob("*"))
            print(f"📰 News files: {len(news_files)}")
            for file in news_files[-3:]:  # Last 3
                print(f"   {file.name}")

        # Check movies
        movie_dir = output_dir / "movies"
        if movie_dir.exists():
            movie_files = list(movie_dir.glob("*"))
            print(f"🎬 Movie files: {len(movie_files)}")
            for file in movie_files[-3:]:  # Last 3
                print(f"   {file.name}")
    else:
        print("❌ No output directory found")


if __name__ == "__main__":
    print("🚀 SHUJAA COMPLETE PIPELINE TEST")
    print("🇰🇪 African AI Video Generation System")
    print("=" * 60)

    # Run all tests
    success = test_elite_movie_pipeline()
    test_system_integration()
    test_file_outputs()

    print(f"\n" + "=" * 60)
    if success:
        print("🎉 COMPLETE PIPELINE: ✅ SUCCESS!")
        print("🚀 Ready for Enhanced App with Gradio UI")
    else:
        print("⚠️ PIPELINE: Partial success - needs attention")
    print("=" * 60)
