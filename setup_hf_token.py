#!/usr/bin/env python3
"""
🔑 HuggingFace Token Setup - Elite Cursor Snippets Methodology

// [SNIPPET]: surgicalfix + kenyafirst + guardon
// [CONTEXT]: Set up HuggingFace token for API testing
// [GOAL]: Configure HF token for Shujaa Studio API access
// [TASK]: Create .env file with HF token or guide user to set it up
// [CONSTRAINTS]: Secure token handling, no hardcoded tokens
"""

import os
import sys
from pathlib import Path

def print_header(title: str, emoji: str = "🔑"):
    """Print formatted header"""
    print(f"\n{emoji} {title.upper()}")
    print("=" * 60)

def print_step(step: str, status: str = "🔄"):
    """Print step with status"""
    print(f"{status} {step}")

def check_existing_token():
    """Check if HF token is already configured"""
    print_header("Checking Existing Configuration", "🔍")
    
    # Check environment variable
    env_token = os.getenv('HF_API_KEY')
    if env_token and env_token != "${HF_API_KEY}":
        print_step(f"✅ Found HF_API_KEY in environment (length: {len(env_token)})")
        return True
        
    # Check .env file
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if 'HF_API_KEY=' in content and '${HF_API_KEY}' not in content:
                print_step("✅ Found HF_API_KEY in .env file")
                return True
                
    print_step("❌ No valid HF token found")
    return False

def create_env_file():
    """Create .env file with HF token placeholder"""
    print_header("Creating Environment Configuration", "📝")
    
    env_content = """# Shujaa Studio Environment Configuration
# HuggingFace API Token for model access
HF_API_KEY=your_huggingface_token_here

# Optional: Other API keys
GOOGLE_NEWS_API_KEY=
YOUTUBE_CLIENT_SECRET_FILE=client_secret.json

# Development settings
DEBUG=true
LOG_LEVEL=INFO
"""
    
    env_file = Path('.env')
    
    if env_file.exists():
        print_step("⚠️ .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print_step("❌ Cancelled - keeping existing .env file")
            return False
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print_step(f"✅ Created .env file: {env_file.absolute()}")
        return True
    except Exception as e:
        print_step(f"❌ Failed to create .env file: {e}")
        return False

def show_token_instructions():
    """Show instructions for getting HF token"""
    print_header("HuggingFace Token Setup Instructions", "📚")
    
    instructions = """
🔑 HOW TO GET YOUR HUGGINGFACE TOKEN:

1. 🌐 Go to: https://huggingface.co/settings/tokens
2. 🔐 Log in to your HuggingFace account (create one if needed)
3. ➕ Click "New token"
4. 📝 Give it a name like "Shujaa Studio"
5. 🔓 Select "Read" permissions (sufficient for API access)
6. 📋 Copy the generated token

🔧 HOW TO SET UP THE TOKEN:

Option 1 - Environment Variable (Recommended):
   export HF_API_KEY="your_token_here"

Option 2 - .env File:
   Edit the .env file and replace 'your_huggingface_token_here' with your actual token

Option 3 - Temporary (this session only):
   HF_API_KEY="your_token_here" python test_all_apis.py

⚠️ SECURITY NOTES:
   - Never commit your token to git
   - Keep your token private
   - Use read-only permissions unless you need write access
   - Regenerate tokens if compromised

🇰🇪 KENYA-FIRST TIP:
   Free HuggingFace accounts work perfectly for Shujaa Studio!
   No paid subscription needed for basic video generation.
"""
    
    print(instructions)

def test_token_setup():
    """Test if the token setup works"""
    print_header("Testing Token Setup", "🧪")
    
    try:
        # Try to import and test
        from huggingface_hub import HfApi
        
        token = os.getenv('HF_API_KEY')
        if not token or token == "your_huggingface_token_here":
            print_step("❌ No valid token found for testing")
            return False
            
        api = HfApi(token=token)
        user_info = api.whoami()
        
        print_step(f"✅ Token works! User: {user_info.get('name', 'Unknown')}")
        return True
        
    except Exception as e:
        print_step(f"❌ Token test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🇰🇪 SHUJAA STUDIO - HUGGINGFACE TOKEN SETUP")
    print("🚀 Elite Cursor Snippets Methodology Applied")
    print("=" * 80)
    
    # Check if token already exists
    if check_existing_token():
        print_step("✅ HuggingFace token is already configured!")
        
        # Test the existing token
        if test_token_setup():
            print_step("🎉 Token is working correctly!")
            print_step("🚀 You can now run: python test_all_apis.py")
            return True
        else:
            print_step("⚠️ Token exists but may not be working")
            
    # Create .env file if it doesn't exist
    if not Path('.env').exists():
        create_env_file()
    
    # Show instructions
    show_token_instructions()
    
    print_header("Next Steps", "🎯")
    print("1. 🔑 Get your HuggingFace token from the instructions above")
    print("2. 📝 Set the HF_API_KEY environment variable or edit .env file")
    print("3. 🧪 Run: python test_all_apis.py")
    print("4. 🎬 If tests pass, run: python generate_video.py")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
