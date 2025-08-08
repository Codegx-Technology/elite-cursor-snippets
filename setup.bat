@echo off
REM 🔥 Shujaa Studio Setup Script for Windows
REM Complete AI Video Generator Setup for African Content Creation

echo 🔥 Welcome to Shujaa Studio Setup!
echo Setting up your African AI Video Generator...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [INFO] Python found

REM Create virtual environment
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install core dependencies
echo [INFO] Installing core dependencies...
pip install -r requirements.txt

REM Create directory structure
echo [INFO] Creating directory structure...
if not exist "models" mkdir models
if not exist "models\tts" mkdir models\tts
if not exist "models\llm" mkdir models\llm
if not exist "models\img" mkdir models\img
if not exist "models\music" mkdir models\music
if not exist "output" mkdir output
if not exist "temp" mkdir temp
if not exist "scripts" mkdir scripts

echo [SUCCESS] Directory structure created

REM Test Python modules
echo [INFO] Testing Python modules...
python -c "import whisper; print('Whisper ready')"
python -c "import pyttsx3; print('TTS ready')"
python -c "from PIL import Image; print('PIL ready')"
python -c "import moviepy.editor; print('MoviePy ready')"

REM Create configuration file
echo [INFO] Creating configuration file...
echo {> config.json
echo     "models_dir": "models",>> config.json
echo     "output_dir": "output",>> config.json
echo     "temp_dir": "temp",>> config.json
echo     "default_language": "English",>> config.json
echo     "default_style": "African storytelling",>> config.json
echo     "video_settings": {>> config.json
echo         "fps": 24,>> config.json
echo         "resolution": "512x512",>> config.json
echo         "codec": "libx264">> config.json
echo     },>> config.json
echo     "audio_settings": {>> config.json
echo         "sample_rate": 22050,>> config.json
echo         "codec": "aac">> config.json
echo     }>> config.json
echo }>> config.json

echo [SUCCESS] Configuration file created

REM Create quick start script
echo [INFO] Creating quick start script...
echo @echo off> run_studio.bat
echo REM Quick start script for Shujaa Studio>> run_studio.bat
echo.>> run_studio.bat
echo echo 🔥 Starting Shujaa Studio...>> run_studio.bat
echo.>> run_studio.bat
echo REM Activate virtual environment>> run_studio.bat
echo call venv\Scripts\activate.bat>> run_studio.bat
echo.>> run_studio.bat
echo REM Check if prompt provided>> run_studio.bat
echo if "%%1"=="" (>> run_studio.bat
echo     echo 🌐 Launching web interface...>> run_studio.bat
echo     python generate_video.py>> run_studio.bat
echo ) else (>> run_studio.bat
echo     echo 🎬 Generating video from prompt: %%*>> run_studio.bat
echo     python generate_video.py "%%*">> run_studio.bat
echo )>> run_studio.bat

echo [SUCCESS] Quick start script created

REM Test the main application
echo [INFO] Testing Shujaa Studio...
python -c "from generate_video import ShujaaStudio; studio = ShujaaStudio(); print('✅ Shujaa Studio initialized successfully!')"

REM Final setup summary
echo.
echo [SUCCESS] 🎉 Shujaa Studio setup complete!
echo.
echo 📁 Directory structure:
echo   ├── models\          # AI models (optional downloads)
echo   ├── output\          # Generated videos
echo   ├── temp\            # Temporary files
echo   ├── scripts\         # Additional scripts
echo   ├── venv\            # Virtual environment
echo   ├── generate_video.py # Main application
echo   └── run_studio.bat   # Quick start script
echo.
echo 🚀 Quick Start:
echo   run_studio.bat                    # Launch web interface
echo   run_studio.bat "Your story here"  # Generate video from prompt
echo.
echo 🌐 Web Interface:
echo   http://localhost:7860              # When running web mode
echo.
echo 🔥 Ready to create African AI videos!
echo.
pause 