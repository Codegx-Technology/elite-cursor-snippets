#!/usr/bin/env python3
"""
📱 Mobile Export Presets - Combo Pack D Quick Export Tool
One-click export to WhatsApp, TikTok, Instagram, and other mobile platforms

// [TASK]: Create quick mobile export presets tool
// [GOAL]: Easy command-line tool for mobile platform optimization
// [SNIPPET]: surgicalfix + refactorclean + kenyafirst
// [CONTEXT]: Elite mobile export for social media platforms
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional

# Add offline_video_maker to path
sys.path.append(str(Path(__file__).parent / "offline_video_maker"))

from offline_video_maker.helpers import VerticalExport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MobilePresets:
    """Quick mobile export presets for social media platforms"""
    
    def __init__(self):
        self.vertical_export = VerticalExport()
        
        # Quick preset configurations
        self.quick_presets = {
            "whatsapp": {
                "name": "WhatsApp Status",
                "description": "720x1280, <16MB, optimized for WhatsApp",
                "platform": "whatsapp",
                "icon": "💬"
            },
            "tiktok": {
                "name": "TikTok Video",
                "description": "1080x1920, <287MB, optimized for TikTok",
                "platform": "tiktok",
                "icon": "🎵"
            },
            "instagram": {
                "name": "Instagram Stories",
                "description": "1080x1920, <100MB, optimized for Instagram",
                "platform": "instagram_stories",
                "icon": "📸"
            },
            "youtube": {
                "name": "YouTube Shorts",
                "description": "1080x1920, <256MB, optimized for YouTube",
                "platform": "youtube_shorts",
                "icon": "📺"
            },
            "facebook": {
                "name": "Facebook Stories",
                "description": "1080x1920, <150MB, optimized for Facebook",
                "platform": "facebook_stories",
                "icon": "👥"
            }
        }
        
        logger.info("[MOBILE] Mobile presets initialized")
    
    def export_single(self, input_video: str, output_path: str, preset: str,
                     background_color: str = "black", 
                     add_blur_background: bool = False) -> bool:
        """
        Export video using a single preset
        
        Args:
            input_video: Input video path
            output_path: Output video path
            preset: Preset name (whatsapp, tiktok, instagram, youtube, facebook)
            background_color: Background color for padding
            add_blur_background: Whether to use blurred background
            
        Returns:
            bool: Success status
        """
        try:
            if preset not in self.quick_presets:
                logger.error(f"[MOBILE] Unknown preset: {preset}")
                return False
            
            preset_config = self.quick_presets[preset]
            platform = preset_config["platform"]
            
            logger.info(f"[MOBILE] {preset_config['icon']} Exporting to {preset_config['name']}")
            
            success = self.vertical_export.convert_to_vertical(
                input_video=input_video,
                output_video=output_path,
                platform=platform,
                background_color=background_color,
                add_blur_background=add_blur_background
            )
            
            if success:
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                logger.info(f"[MOBILE] ✅ {preset_config['name']} export successful ({file_size:.1f}MB)")
            else:
                logger.error(f"[MOBILE] ❌ {preset_config['name']} export failed")
            
            return success
            
        except Exception as e:
            logger.error(f"[MOBILE] Export error: {e}")
            return False
    
    def export_all_presets(self, input_video: str, output_dir: str,
                          presets: List[str] = None,
                          background_color: str = "black",
                          add_blur_background: bool = False) -> Dict[str, bool]:
        """
        Export video to multiple presets
        
        Args:
            input_video: Input video path
            output_dir: Output directory
            presets: List of presets to export (default: all)
            background_color: Background color for padding
            add_blur_background: Whether to use blurred background
            
        Returns:
            Dictionary with export results for each preset
        """
        if presets is None:
            presets = list(self.quick_presets.keys())
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        base_name = Path(input_video).stem
        results = {}
        
        logger.info(f"[MOBILE] Exporting to {len(presets)} presets...")
        
        for preset in presets:
            if preset not in self.quick_presets:
                logger.warning(f"[MOBILE] Skipping unknown preset: {preset}")
                results[preset] = False
                continue
            
            preset_config = self.quick_presets[preset]
            output_file = output_path / f"{base_name}_{preset}.mp4"
            
            success = self.export_single(
                input_video=input_video,
                output_path=str(output_file),
                preset=preset,
                background_color=background_color,
                add_blur_background=add_blur_background
            )
            
            results[preset] = success
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        logger.info(f"[MOBILE] 🎉 Export complete: {successful}/{len(presets)} successful")
        
        return results
    
    def get_preset_info(self, preset: str = None) -> Dict:
        """
        Get information about presets
        
        Args:
            preset: Specific preset name (optional)
            
        Returns:
            Preset information
        """
        if preset:
            if preset in self.quick_presets:
                preset_info = self.quick_presets[preset].copy()
                platform_info = self.vertical_export.get_platform_info(preset_info["platform"])
                preset_info.update(platform_info)
                return preset_info
            else:
                return {}
        
        return self.quick_presets
    
    def validate_input(self, input_video: str) -> Dict[str, bool]:
        """
        Validate input video for mobile export
        
        Args:
            input_video: Input video path
            
        Returns:
            Validation results
        """
        validation = {
            "file_exists": os.path.exists(input_video),
            "is_video": False,
            "readable": False
        }
        
        if validation["file_exists"]:
            # Check if it's a video file
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
            file_ext = Path(input_video).suffix.lower()
            validation["is_video"] = file_ext in video_extensions
            
            # Check if readable
            try:
                validation["readable"] = os.access(input_video, os.R_OK)
            except:
                validation["readable"] = False
        
        return validation
    
    def print_preset_summary(self):
        """Print summary of available presets"""
        print("\n📱 Available Mobile Presets:")
        print("=" * 50)
        
        for preset_key, preset_config in self.quick_presets.items():
            platform_info = self.vertical_export.get_platform_info(preset_config["platform"])
            
            print(f"\n{preset_config['icon']} {preset_key.upper()}")
            print(f"   Name: {preset_config['name']}")
            print(f"   Description: {preset_config['description']}")
            
            if platform_info:
                resolution = platform_info.get('resolution', 'Unknown')
                max_size = platform_info.get('max_file_size', 0) / (1024 * 1024)  # MB
                print(f"   Resolution: {resolution[0]}x{resolution[1]}")
                print(f"   Max Size: {max_size:.0f}MB")
        
        print("\n" + "=" * 50)
    
    def create_export_script(self, input_video: str, output_dir: str = "mobile_exports"):
        """
        Create a batch script for easy mobile exports
        
        Args:
            input_video: Input video path
            output_dir: Output directory
        """
        script_content = f"""#!/bin/bash
# Mobile Export Script for {Path(input_video).name}
# Generated by Shujaa Studio Mobile Presets

echo "📱 Starting mobile exports for {Path(input_video).name}..."

# Create output directory
mkdir -p "{output_dir}"

# Export to all platforms
python mobile_presets.py "{input_video}" --output-dir "{output_dir}" --all

echo "✅ Mobile exports completed!"
echo "📁 Check output directory: {output_dir}"
"""
        
        script_path = f"export_{Path(input_video).stem}.sh"
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable on Unix systems
        try:
            os.chmod(script_path, 0o755)
        except:
            pass
        
        logger.info(f"[MOBILE] Export script created: {script_path}")


def main():
    """Command-line interface for mobile presets"""
    parser = argparse.ArgumentParser(description="Mobile Export Presets for Shujaa Studio")
    parser.add_argument("input_video", help="Input video file")
    parser.add_argument("--output-dir", default="mobile_exports", help="Output directory")
    parser.add_argument("--preset", choices=["whatsapp", "tiktok", "instagram", "youtube", "facebook"],
                       help="Specific preset to export")
    parser.add_argument("--all", action="store_true", help="Export to all presets")
    parser.add_argument("--background-color", default="black", help="Background color for padding")
    parser.add_argument("--blur-background", action="store_true", help="Use blurred background instead of solid color")
    parser.add_argument("--info", action="store_true", help="Show preset information")
    parser.add_argument("--create-script", action="store_true", help="Create export script")
    
    args = parser.parse_args()
    
    mobile_presets = MobilePresets()
    
    # Show preset information
    if args.info:
        mobile_presets.print_preset_summary()
        return
    
    # Create export script
    if args.create_script:
        mobile_presets.create_export_script(args.input_video, args.output_dir)
        return
    
    # Validate input
    validation = mobile_presets.validate_input(args.input_video)
    if not validation["file_exists"]:
        print(f"❌ Input video not found: {args.input_video}")
        sys.exit(1)
    
    if not validation["is_video"]:
        print(f"❌ Input file is not a video: {args.input_video}")
        sys.exit(1)
    
    if not validation["readable"]:
        print(f"❌ Cannot read input video: {args.input_video}")
        sys.exit(1)
    
    try:
        if args.all:
            # Export to all presets
            results = mobile_presets.export_all_presets(
                input_video=args.input_video,
                output_dir=args.output_dir,
                background_color=args.background_color,
                add_blur_background=args.blur_background
            )
            
            # Print results
            print(f"\n📊 Export Results:")
            for preset, success in results.items():
                status = "✅" if success else "❌"
                print(f"   {status} {preset}")
            
        elif args.preset:
            # Export to specific preset
            output_file = Path(args.output_dir) / f"{Path(args.input_video).stem}_{args.preset}.mp4"
            output_file.parent.mkdir(exist_ok=True)
            
            success = mobile_presets.export_single(
                input_video=args.input_video,
                output_path=str(output_file),
                preset=args.preset,
                background_color=args.background_color,
                add_blur_background=args.blur_background
            )
            
            if success:
                print(f"✅ Export successful: {output_file}")
            else:
                print(f"❌ Export failed")
                sys.exit(1)
        
        else:
            print("❌ Please specify --preset or --all")
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
