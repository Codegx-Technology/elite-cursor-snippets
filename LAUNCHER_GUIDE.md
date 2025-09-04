# 🚀 Shujaa Studio Professional Launcher Guide

## 🎯 **Quick Start**

### **Windows (PowerShell)**
```powershell
# Health check first
.\run.ps1 -Check

# Launch both backend and frontend
.\run.ps1

# Launch only backend
.\run.ps1 -BackendOnly

# Launch only frontend
.\run.ps1 -FrontendOnly

# Show help
.\run.ps1 -Help
```

### **Linux/macOS (Bash)**
```bash
# Health check first
./run.sh --check

# Launch both backend and frontend
./run.sh

# Launch only backend
./run.sh --backend-only

# Launch only frontend
./run.sh --frontend-only

# Show help
./run.sh --help
```

## 🔧 **Prerequisites**

### **Required Software**
- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **PowerShell 5.1+** (Windows) or **Bash 4.0+** (Linux/macOS)

### **Environment Setup**
1. **Virtual Environment**: `shujaa_venv` (auto-created if missing)
2. **Frontend Dependencies**: `node_modules` (auto-installed if missing)
3. **Python Dependencies**: Auto-installed from `requirements.txt`

## 🌐 **Access URLs**

After successful launch, access your applications at:

- **🎬 Frontend UI**: http://localhost:3000
- **🔧 Backend API**: http://localhost:8000
- **📖 API Documentation**: http://localhost:8000/docs
- **❤️ Health Check**: http://localhost:8000/health

## 🎛️ **Launcher Features**

### ✅ **Automatic Environment Detection**
- Detects Python virtual environment (`shujaa_venv`)
- Finds Node.js and npm in PATH or common locations
- Validates all dependencies before launch

### ✅ **Separate Terminal Windows**
- Backend runs in dedicated PowerShell/terminal window
- Frontend runs in separate PowerShell/terminal window
- Easy monitoring of logs and errors

### ✅ **Professional Error Handling**
- Clear error messages with solutions
- Graceful fallbacks for missing dependencies
- Health check validation before launch

### ✅ **Cross-Platform Support**
- `run.ps1` for Windows PowerShell
- `run.sh` for Linux/macOS Bash
- Consistent behavior across platforms

## 🚨 **Troubleshooting**

### **Problem: "shujaa_venv not found"**
```powershell
# Solution: Create virtual environment
python -m venv shujaa_venv
shujaa_venv\Scripts\pip install -r requirements.txt
```

### **Problem: "Node.js not found"**
```powershell
# Solution: Install Node.js
# Download from: https://nodejs.org/
# Or use package manager:
winget install OpenJS.NodeJS  # Windows
brew install node             # macOS
sudo apt install nodejs npm   # Ubuntu
```

### **Problem: "Frontend dependencies missing"**
```powershell
# Solution: Install frontend dependencies
cd frontend
npm install
```

### **Problem: "Permission denied" (PowerShell)**
```powershell
# Solution: Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Problem: "Port already in use"**
```powershell
# Solution: Kill processes on ports
netstat -ano | findstr :8000  # Find process using port 8000
taskkill /PID <process_id> /F  # Kill the process
```

## 🔍 **Health Check Details**

The health check validates:
- ✅ Python virtual environment exists
- ✅ Python dependencies are installed
- ✅ Node.js and npm are available
- ✅ Frontend dependencies are installed
- ✅ All required files are present

## 🎯 **Development Workflow**

### **Recommended Daily Workflow**
1. **Health Check**: `.\run.ps1 -Check`
2. **Launch Development**: `.\run.ps1`
3. **Access Frontend**: http://localhost:3000
4. **Access API Docs**: http://localhost:8000/docs
5. **Monitor Logs**: Check separate terminal windows

### **Backend-Only Development**
```powershell
# For API development only
.\run.ps1 -BackendOnly
```

### **Frontend-Only Development**
```powershell
# For UI development only (requires backend running separately)
.\run.ps1 -FrontendOnly
```

## 🇰🇪 **GEMINI.md Contract Compliance**

This launcher follows the GEMINI.md contract:
- ✅ Uses `shujaa_venv` as primary Python environment
- ✅ Keeps `venv312-lama` isolated for lama-cleaner
- ✅ Wraps all servers in unified management
- ✅ Follows elite cursor snippets methodology
- ✅ Maintains surgical, token-efficient approach

## 🚀 **Advanced Usage**

### **Custom Port Configuration**
Edit `universal_server.py` to change default ports:
```python
# Backend: Default port 8000
# Frontend: Default port 3000
```

### **Environment Variables**
Set these for enhanced functionality:
```powershell
$env:SHUJAA_DEBUG = "true"          # Enable debug mode
$env:SHUJAA_LOG_LEVEL = "INFO"      # Set log level
$env:HF_TOKEN = "your_token_here"   # Hugging Face token
```

### **Production Deployment**
For production, use:
```powershell
# Use universal_server.py directly for production
shujaa_venv\Scripts\python.exe universal_server.py --production
```

## 📊 **Performance Tips**

1. **First Launch**: May take 2-3 minutes for dependency installation
2. **Subsequent Launches**: Should start in 10-15 seconds
3. **Memory Usage**: ~2GB RAM for full stack
4. **Disk Space**: ~5GB for all models and dependencies

## 🔐 **Security Notes**

- Launchers run with current user permissions
- No elevated privileges required
- All network access is localhost only
- API endpoints are development-mode only

## 🆘 **Support**

If you encounter issues:
1. Run health check: `.\run.ps1 -Check`
2. Check error messages in terminal windows
3. Verify all prerequisites are installed
4. Consult troubleshooting section above

**Harambee! Elite development workflow ready! 🇰🇪**
