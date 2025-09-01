# 🇰🇪 Shujaa Studio Server Startup Guide

## 🚀 Universal Server Management

The **universal_server.py** is your one-stop solution for managing all Shujaa Studio services. It wraps and orchestrates all servers as per the project architecture.

## 📋 Quick Start Commands

### 1. **Start All Services** (Recommended)
```bash
# Activate virtual environment first
shujaa_venv\Scripts\activate

# Start all services (frontend + backend + gradio)
python universal_server.py
```

### 2. **Backend Only** (API Server)
```bash
# Start only the backend API server on port 8000
python universal_server.py --backend-only
```

### 3. **Frontend Only** (React/Next.js)
```bash
# Start only the frontend on port 3000 (requires Node.js)
python universal_server.py --frontend-only
```

### 4. **System Health Check**
```bash
# Check if all dependencies and environment are ready
python universal_server.py --check
```

### 5. **Clear Port Conflicts**
```bash
# Kill any processes using ports 3000 and 8000
python universal_server.py --kill-ports
```

## 🔧 Advanced Options

### Use Full API Server (with all features)
```bash
# Use api_server.py instead of simple_api.py
python universal_server.py --backend-only --full-api
```

### Individual Service Management
```bash
# Backend only with simple API (default)
python universal_server.py --backend-only

# Backend with full API features
python universal_server.py --backend-only --full-api

# Frontend only (requires Node.js installation)
python universal_server.py --frontend-only
```

## 📊 Service Overview

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| **Backend API** | 8000 | http://localhost:8000 | FastAPI server with video generation |
| **Frontend** | 3000 | http://localhost:3000 | React/Next.js UI (requires Node.js) |
| **Gradio UI** | 7860 | http://localhost:7860 | Legacy Gradio interface |
| **API Docs** | 8000 | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | 8000 | http://localhost:8000/health | Backend health status |

## 🛠️ Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://localhost:8000/health

# Or use PowerShell
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/health'"

# Check what's using port 8000
netstat -an | findstr :8000
```

### Frontend Issues
```bash
# Install Node.js first from https://nodejs.org/
# Then check if npm is available
npm --version

# Install frontend dependencies
cd frontend
npm install
```

### Environment Issues
```bash
# Check virtual environment health
python universal_server.py --check

# Verify Python environment
shujaa_venv\Scripts\python.exe -c "import sys; print(sys.prefix)"
```

## 🎯 Recommended Workflow

### For Development
1. **Start with health check:**
   ```bash
   python universal_server.py --check
   ```

2. **Start backend for API development:**
   ```bash
   python universal_server.py --backend-only
   ```

3. **Start frontend (if Node.js is installed):**
   ```bash
   python universal_server.py --frontend-only
   ```

4. **Start all services for full testing:**
   ```bash
   python universal_server.py
   ```

### For Production
```bash
# Use full API server with all features
python universal_server.py --full-api
```

## 🔍 Service Status Monitoring

The universal server provides real-time status monitoring:

```
🇰🇪 SHUJAA STUDIO - UNIVERSAL SERVER STATUS
================================================================================
  Shujaa Studio Backend API        | Port 8000  | ✅ RUNNING
  Shujaa Studio Frontend           | Port 3000  | ✅ RUNNING
  Shujaa Studio Gradio UI          | Port 7860  | ✅ RUNNING
================================================================================
🌐 Access URLs:
  Frontend (React):     http://localhost:3000
  Backend API:          http://localhost:8000
  API Documentation:    http://localhost:8000/docs
  Gradio UI (Legacy):   http://localhost:7860
================================================================================
```

## 🚨 Important Notes

1. **Always activate shujaa_venv first:**
   ```bash
   shujaa_venv\Scripts\activate
   ```

2. **Node.js is required for frontend:**
   - Download from https://nodejs.org/
   - Frontend will be disabled if Node.js is not found

3. **Port conflicts are automatically resolved:**
   - Universal server kills conflicting processes
   - Use `--kill-ports` to manually clear ports

4. **Health monitoring is built-in:**
   - Services are automatically restarted if they crash
   - Health checks run every 30 seconds

5. **Graceful shutdown:**
   - Press `Ctrl+C` to stop all services
   - All processes are properly terminated

## 🇰🇪 Harambee! 

The universal server embodies the Harambee spirit - bringing all services together to work as one unified system. Use it as your primary tool for managing the Shujaa Studio infrastructure.

**Asante sana for using Shujaa Studio! 🚀**
