#!/bin/bash
# Shujaa Studio Professional Launcher (Cross-Platform)
# Elite Bash script for surgical, token-efficient development workflow
# Compatible with AugmentCode methodology and GEMINI.md contract

set -euo pipefail

# Professional configuration
BACKEND_ONLY=false
FRONTEND_ONLY=false
CHECK_ONLY=false
SHOW_HELP=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only) BACKEND_ONLY=true; shift ;;
        --frontend-only) FRONTEND_ONLY=true; shift ;;
        --check) CHECK_ONLY=true; shift ;;
        --help|-h) SHOW_HELP=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Professional banner
show_banner() {
    echo -e "\033[32m🇰🇪 =============================================\033[0m"
    echo -e "\033[33m🚀 SHUJAA STUDIO PROFESSIONAL LAUNCHER\033[0m"
    echo -e "\033[36m⚡ Elite • Surgical • Token-Efficient\033[0m"
    echo -e "\033[32m🇰🇪 =============================================\033[0m"
    echo ""
}

# Dynamic project root detection
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "\033[36m📁 Project Root: $PROJECT_ROOT\033[0m"

# Professional environment detection
test_python_environment() {
    local python_exe="$PROJECT_ROOT/shujaa_venv/bin/python"
    
    if [[ ! -f "$python_exe" ]]; then
        echo -e "\033[31m❌ shujaa_venv not found. Creating...\033[0m"
        python3 -m venv "$PROJECT_ROOT/shujaa_venv"
    fi
    
    # Test Python environment health
    local test_script='
import sys, os, site
print(f"🐍 Python: {sys.version}")
print(f"🐍 Interpreter: {sys.executable}")
print(f"🐍 Prefix: {sys.prefix}")

# Force venv site-packages into sys.path
venv_site = os.path.join(sys.prefix, "lib", "python" + ".".join(map(str, sys.version_info[:2])), "site-packages")
if venv_site not in sys.path:
    site.addsitedir(venv_site)
    print(f"✅ Added to sys.path: {venv_site}")

# Test critical dependencies
deps = ["fastapi", "uvicorn", "psutil", "requests"]
missing = []
for dep in deps:
    try:
        __import__(dep)
        print(f"✅ {dep}: OK")
    except ImportError:
        missing.append(dep)
        print(f"❌ {dep}: MISSING")

if missing:
    print(f"⚠️ Installing missing: {missing}")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
    print("✅ Dependencies installed")
'
    
    echo -e "\033[33m🔍 Testing Python environment...\033[0m"
    "$python_exe" -c "$test_script"
    
    echo "$python_exe"
}

# Professional Node.js detection
test_node_environment() {
    local node_path=$(which node 2>/dev/null || echo "")
    local npm_path=$(which npm 2>/dev/null || echo "")
    
    if [[ -z "$node_path" ]]; then
        echo -e "\033[31m❌ Node.js not found. Install from https://nodejs.org/\033[0m"
        return 1
    fi
    
    local node_version=$(node --version)
    local npm_version=$(npm --version)
    echo -e "\033[32m🟢 Node.js: $node_version at $node_path\033[0m"
    echo -e "\033[32m🟢 npm: $npm_version at $npm_path\033[0m"
    
    # Check frontend dependencies
    local frontend_path="$PROJECT_ROOT/frontend"
    if [[ -d "$frontend_path" ]]; then
        local node_modules="$frontend_path/node_modules"
        if [[ ! -d "$node_modules" ]]; then
            echo -e "\033[33m📦 Installing frontend dependencies...\033[0m"
            (cd "$frontend_path" && npm install)
        fi
    fi
    
    echo "$node_path:$npm_path"
}

# Professional server launcher
start_backend_server() {
    local python_exe="$1"
    
    echo -e "\033[32m🚀 Launching Backend Server...\033[0m"
    
    # Launch in new terminal (platform-specific)
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd '$PROJECT_ROOT'; echo -e '\033[32m🇰🇪 SHUJAA STUDIO BACKEND\033[0m'; '$python_exe' universal_server.py --backend-only; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd '$PROJECT_ROOT'; echo -e '\033[32m🇰🇪 SHUJAA STUDIO BACKEND\033[0m'; '$python_exe' universal_server.py --backend-only; exec bash" &
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        osascript -e "tell application \"Terminal\" to do script \"cd '$PROJECT_ROOT'; echo -e '\033[32m🇰🇪 SHUJAA STUDIO BACKEND\033[0m'; '$python_exe' universal_server.py --backend-only\""
    else
        echo -e "\033[33m⚠️ Starting backend in current terminal...\033[0m"
        "$python_exe" universal_server.py --backend-only &
    fi
}

start_frontend_server() {
    local node_info="$1"
    local node_path="${node_info%:*}"
    local npm_path="${node_info#*:}"
    
    echo -e "\033[32m🚀 Launching Frontend Server...\033[0m"
    
    local frontend_path="$PROJECT_ROOT/frontend"
    
    # Launch in new terminal (platform-specific)
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd '$frontend_path'; echo -e '\033[32m🇰🇪 SHUJAA STUDIO FRONTEND\033[0m'; echo -e '\033[36m🟢 Node.js: $node_path\033[0m'; echo -e '\033[36m🟢 npm: $npm_path\033[0m'; '$npm_path' run dev; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd '$frontend_path'; echo -e '\033[32m🇰🇪 SHUJAA STUDIO FRONTEND\033[0m'; '$npm_path' run dev; exec bash" &
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        osascript -e "tell application \"Terminal\" to do script \"cd '$frontend_path'; echo -e '\033[32m🇰🇪 SHUJAA STUDIO FRONTEND\033[0m'; '$npm_path' run dev\""
    else
        echo -e "\033[33m⚠️ Starting frontend in current terminal...\033[0m"
        (cd "$frontend_path" && "$npm_path" run dev) &
    fi
}

# Professional help system
show_help() {
    cat << 'EOF'
🇰🇪 SHUJAA STUDIO PROFESSIONAL LAUNCHER

USAGE:
  ./run.sh                  # Launch both backend and frontend
  ./run.sh --backend-only   # Launch only backend server
  ./run.sh --frontend-only  # Launch only frontend server
  ./run.sh --check          # Check system health
  ./run.sh --help           # Show this help

FEATURES:
  ✅ Automatic environment detection
  ✅ Dependency auto-installation
  ✅ Separate terminal windows for monitoring
  ✅ Professional error handling
  ✅ GEMINI.md contract compliance
  ✅ Elite cursor snippets methodology

REQUIREMENTS:
  - Python 3.8+ (for backend)
  - Node.js 16+ (for frontend)
  - Bash 4.0+ (Linux/macOS)

EXAMPLES:
  ./run.sh                  # Full development environment
  ./run.sh --backend-only   # API development only
  ./run.sh --check          # Health check before development

🇰🇪 Harambee! Elite development workflow ready!
EOF
}

# Main execution logic
main() {
    show_banner
    
    if [[ "$SHOW_HELP" == true ]]; then
        show_help
        return 0
    fi
    
    # Professional environment validation
    echo -e "\033[33m🔍 Validating development environment...\033[0m"
    
    local python_exe
    python_exe=$(test_python_environment)
    
    local node_info=""
    if [[ "$BACKEND_ONLY" != true ]]; then
        node_info=$(test_node_environment) || {
            echo -e "\033[31m❌ Node.js required for frontend\033[0m"
            exit 1
        }
    fi
    
    if [[ "$CHECK_ONLY" == true ]]; then
        echo -e "\033[32m✅ Environment validation complete!\033[0m"
        echo -e "\033[33m🎉 Shujaa Studio is ready for elite development!\033[0m"
        return 0
    fi
    
    # Launch services based on parameters
    if [[ "$FRONTEND_ONLY" != true ]]; then
        start_backend_server "$python_exe"
        sleep 2
    fi
    
    if [[ "$BACKEND_ONLY" != true && -n "$node_info" ]]; then
        start_frontend_server "$node_info"
        sleep 2
    fi
    
    # Professional completion message
    echo ""
    echo -e "\033[32m🎉 Shujaa Studio backend and frontend launched successfully!\033[0m"
    echo -e "\033[36m🌐 Backend API: http://localhost:8000\033[0m"
    echo -e "\033[36m🌐 Frontend UI: http://localhost:3000\033[0m"
    echo -e "\033[36m📖 API Docs: http://localhost:8000/docs\033[0m"
    echo ""
    echo -e "\033[33m🇰🇪 Harambee! Elite development environment active!\033[0m"
}

# Execute main function
main "$@"
