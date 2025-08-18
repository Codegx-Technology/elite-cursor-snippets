#!/bin/bash

# Shujaa Studio - AI Health Scanner Setup Script
# Sets up intelligent monitoring system with Kenya-first approach

echo "🇰🇪 Setting up Shujaa Studio AI Health Scanner..."
echo "Harambee! Let's build something amazing together!"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

# Check if Python 3 is installed
print_header "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 is required but not installed."
    exit 1
fi

# Install required Python packages
print_header "Installing Python dependencies..."
pip3 install --user psutil requests schedule

if [ $? -eq 0 ]; then
    print_status "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Make the health scanner executable
print_header "Setting up health scanner permissions..."
chmod +x ai_health_scanner.py

if [ $? -eq 0 ]; then
    print_status "Health scanner permissions set"
else
    print_warning "Could not set executable permissions"
fi

# Create systemd service file (optional)
print_header "Creating systemd service (optional)..."
cat > shujaa-health-scanner.service << EOF
[Unit]
Description=Shujaa Studio AI Health Scanner
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/ai_health_scanner.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

print_status "Systemd service file created: shujaa-health-scanner.service"
print_status "To install as system service, run:"
print_status "  sudo cp shujaa-health-scanner.service /etc/systemd/system/"
print_status "  sudo systemctl enable shujaa-health-scanner"
print_status "  sudo systemctl start shujaa-health-scanner"

# Create configuration file
print_header "Creating configuration file..."
cat > health_scanner_config.json << EOF
{
  "scan_mode": "standard",
  "scan_interval": 120,
  "auto_heal": true,
  "notifications": true,
  "muted": false,
  "log_level": "INFO",
  "max_auto_fixes": 3,
  "thresholds": {
    "cpu_warning": 80,
    "cpu_critical": 90,
    "memory_warning": 80,
    "memory_critical": 90,
    "disk_warning": 80,
    "disk_critical": 90,
    "response_time_warning": 3000,
    "response_time_critical": 5000
  },
  "notifications": {
    "email": {
      "enabled": false,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "username": "your-email@gmail.com",
      "password": "your-app-password",
      "admin_emails": ["admin@yourdomain.com"]
    },
    "slack": {
      "enabled": false,
      "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    }
  }
}
EOF

print_status "Configuration file created: health_scanner_config.json"

# Create startup script
print_header "Creating startup script..."
cat > start_health_scanner.sh << 'EOF'
#!/bin/bash

echo "🇰🇪 Starting Shujaa Studio AI Health Scanner..."
echo "Harambee! Protecting your system with AI intelligence!"

# Check if already running
if pgrep -f "ai_health_scanner.py" > /dev/null; then
    echo "Health scanner is already running!"
    echo "PID: $(pgrep -f ai_health_scanner.py)"
    exit 1
fi

# Start the scanner
python3 ai_health_scanner.py &
SCANNER_PID=$!

echo "Health scanner started with PID: $SCANNER_PID"
echo "Log file: shujaa_health_scanner.log"
echo ""
echo "Commands to control the scanner:"
echo "  - View logs: tail -f shujaa_health_scanner.log"
echo "  - Stop scanner: kill $SCANNER_PID"
echo "  - Check status: ps aux | grep ai_health_scanner"
echo ""
echo "Asante sana! Your system is now protected! 🛡️"
EOF

chmod +x start_health_scanner.sh
print_status "Startup script created: start_health_scanner.sh"

# Create stop script
print_header "Creating stop script..."
cat > stop_health_scanner.sh << 'EOF'
#!/bin/bash

echo "🛑 Stopping Shujaa Studio AI Health Scanner..."

# Find and kill the scanner process
SCANNER_PID=$(pgrep -f "ai_health_scanner.py")

if [ -z "$SCANNER_PID" ]; then
    echo "Health scanner is not running."
    exit 1
fi

kill $SCANNER_PID

if [ $? -eq 0 ]; then
    echo "Health scanner stopped successfully."
    echo "Asante sana! Scanner has been stopped gracefully."
else
    echo "Failed to stop health scanner. Trying force kill..."
    kill -9 $SCANNER_PID
    echo "Health scanner force stopped."
fi
EOF

chmod +x stop_health_scanner.sh
print_status "Stop script created: stop_health_scanner.sh"

# Create status script
print_header "Creating status script..."
cat > check_scanner_status.sh << 'EOF'
#!/bin/bash

echo "🔍 Shujaa Studio AI Health Scanner Status"
echo "========================================"

# Check if scanner is running
SCANNER_PID=$(pgrep -f "ai_health_scanner.py")

if [ -z "$SCANNER_PID" ]; then
    echo "Status: ❌ NOT RUNNING"
    echo ""
    echo "To start the scanner:"
    echo "  ./start_health_scanner.sh"
else
    echo "Status: ✅ RUNNING"
    echo "PID: $SCANNER_PID"
    echo "Started: $(ps -o lstart= -p $SCANNER_PID)"
    echo ""
    
    # Check log file for recent activity
    if [ -f "shujaa_health_scanner.log" ]; then
        echo "Recent log entries:"
        echo "==================="
        tail -5 shujaa_health_scanner.log
    fi
    
    echo ""
    echo "To stop the scanner:"
    echo "  ./stop_health_scanner.sh"
    echo ""
    echo "To view live logs:"
    echo "  tail -f shujaa_health_scanner.log"
fi

echo ""
echo "Harambee! 🇰🇪"
EOF

chmod +x check_scanner_status.sh
print_status "Status script created: check_scanner_status.sh"

# Create README for the health scanner
print_header "Creating documentation..."
cat > HEALTH_SCANNER_README.md << 'EOF'
# 🛡️ Shujaa Studio AI Health Scanner

## Overview
The AI Health Scanner is an intelligent monitoring system that watches over your Shujaa Studio application like an antivirus but for system health. It automatically detects issues and attempts to fix them while providing friendly Kenya-first user experience.

## Features
- 🔍 **Intelligent Monitoring**: Continuous health checks of frontend, backend, and system resources
- 🤖 **Auto-Healing**: Automatically fixes common issues without user intervention
- 🇰🇪 **Kenya-First UX**: Friendly messages in English and Swahili
- 📊 **Real-time Metrics**: CPU, memory, disk usage, and response times
- 🔇 **Mute Capability**: Temporarily disable notifications
- 📧 **Notifications**: Email and Slack alerts for critical issues
- ⏰ **Scheduling**: Configurable scan intervals and modes

## Quick Start

### 1. Setup (one-time)
```bash
./setup_health_scanner.sh
```

### 2. Start Scanner
```bash
./start_health_scanner.sh
```

### 3. Check Status
```bash
./check_scanner_status.sh
```

### 4. Stop Scanner
```bash
./stop_health_scanner.sh
```

## Scan Modes
- **Quick** (30s): Basic health checks
- **Standard** (2min): Comprehensive monitoring (default)
- **Deep** (5min): Full system scan
- **Custom**: User-defined interval

## Interactive Commands
When running the scanner interactively:
- `status` - Get health report
- `mute 30` - Mute for 30 minutes
- `unmute` - Unmute notifications
- `stop` - Stop scanner
- `quit` - Exit

## Configuration
Edit `health_scanner_config.json` to customize:
- Scan intervals and thresholds
- Email/Slack notifications
- Auto-healing settings
- Logging levels

## Auto-Healing Capabilities
The scanner can automatically fix:
- ✅ Frontend/Backend crashes (restart services)
- ✅ High CPU usage (optimize processes)
- ✅ Memory leaks (clear memory)
- ✅ Disk space issues (clean temporary files)
- ✅ Performance problems (restart services)

## Kenya-First Messages
The scanner provides friendly, culturally appropriate messages:
- 🔍 "Hakuna matata! Our AI is checking system health..."
- 🔧 "Pole sana! Our smart engine is getting a quick fix..."
- ✅ "Asante sana! Everything is working perfectly now!"

## Logs
- Main log: `shujaa_health_scanner.log`
- View live: `tail -f shujaa_health_scanner.log`

## System Service (Optional)
To run as a system service:
```bash
sudo cp shujaa-health-scanner.service /etc/systemd/system/
sudo systemctl enable shujaa-health-scanner
sudo systemctl start shujaa-health-scanner
```

## Troubleshooting
- **Scanner won't start**: Check Python dependencies with `pip3 list`
- **No auto-healing**: Verify `auto_heal: true` in config
- **Missing notifications**: Configure email/Slack in config file

Harambee! 🇰🇪 Your system is now protected with AI intelligence!
EOF

print_status "Documentation created: HEALTH_SCANNER_README.md"

# Final setup summary
echo ""
echo "🎉 Setup Complete! Harambee!"
echo "=============================="
echo ""
print_status "✅ AI Health Scanner is ready to use!"
print_status "✅ Configuration file created"
print_status "✅ Control scripts created"
print_status "✅ Documentation available"
echo ""
echo "Next steps:"
echo "1. Start the scanner: ./start_health_scanner.sh"
echo "2. Check status: ./check_scanner_status.sh"
echo "3. Read docs: cat HEALTH_SCANNER_README.md"
echo ""
echo "🇰🇪 Asante sana! Your Shujaa Studio is now protected!"
echo "The AI will watch over your system like a Maasai warrior! 🛡️"
