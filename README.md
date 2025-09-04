# 🔥 Shujaa Studio - Kenya-First AI Video Platform

**World-class AI video generation with authentic African cultural elements**

## 🎯 What is Shujaa Studio?

Shujaa Studio is a comprehensive AI video generation platform designed with Kenya-first principles. Features include:

### 🎬 **Core Features**
- **AI Video Generation**: Transform text to engaging videos with cultural authenticity
- **News Video Creation**: Convert news articles, URLs, or scripts into professional videos
- **Watermark Removal**: Clean, professional content generation
- **Multi-language Support**: English, Swahili, and bilingual content
- **Platform Optimization**: Export for TikTok, Instagram, WhatsApp, YouTube
- **Offline Capability**: Complete local processing for privacy and performance

### 🇰🇪 **Kenya-First Design**
- **Cultural Authenticity**: Mount Kenya, Maasai Mara, coastal themes
- **Local Payment**: M-Pesa and Kenyan banking integration
- **Affordable Pricing**: 40-60% cheaper than international competitors
- **Mobile-First**: Optimized for African mobile usage patterns
- **Friendly Fallbacks**: Cultural messaging instead of technical errors

## 🚀 Quick Start - Professional Launcher System

### **🎯 Elite Development Workflow (Recommended)**

**Windows:**
```powershell
# 1. Health check first
.\run.ps1 -Check

# 2. Launch full development environment
.\run.ps1

# 3. Access your applications
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Linux/macOS:**
```bash
# 1. Health check first
./run.sh --check

# 2. Launch full development environment
./run.sh
```

**Individual Services:**
```powershell
.\run.ps1 -BackendOnly    # Backend only
.\run.ps1 -FrontendOnly   # Frontend only
.\run.ps1 -Help           # Show help
```

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/Codegx-Technology/ShujaaStudio.git
cd ShujaaStudio
```

### 2. Activate Environment (from SHUJAA_STUDIO_SETUP_GUIDE.md)
```bash
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies (from SHUJAA_STUDIO_SETUP_GUIDE.md)
```bash
pip install -r requirements.txt
```

### 4. Start API Server (from SHUJAA_STUDIO_SETUP_GUIDE.md)
```bash
pip install fastapi uvicorn pydantic
python simple_api.py
# Server: http://localhost:8000
```

### 5. Start Gradio UI (from SHUJAA_STUDIO_SETUP_GUIDE.md)
```bash
python simple_ui.py
# UI: http://localhost:7860
```

### 6. Test System (from SHUJAA_STUDIO_SETUP_GUIDE.md)
```bash
# Test API
curl http://localhost:8000/health

# Test generation
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Kenyan story", "scenes": 3, "vertical": true}'
```

### 7. Frontend Setup (from existing README.md)
```bash
cd frontend
npm install
npm run dev
```

### 8. Access Application (from existing README.md)
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 🧪 Testing Ready
The application is ready for immediate testing without AI model dependencies. All features work with mock data for comprehensive UI/UX testing.

### 🤖 Optional: AI Model Setup
```bash
# For actual AI generation (optional)
export HF_TOKEN="your_key_here"
python hf_access_check.py

# Download local models for offline use
# - SDXL for image generation
# - Bark for voice synthesis
# - Whisper for speech recognition
```

## 🌐 API Endpoints (from SHUJAA_STUDIO_SETUP_GUIDE.md)

- `GET /health` - Health check
- `POST /generate` - Generate video
- `POST /batch` - Batch processing
- `GET /videos` - List videos
- `GET /config` - Get configuration
- `POST /test` - Test generation

## 🎯 Configuration (from SHUJAA_STUDIO_SETUP_GUIDE.md)

```yaml
# API Settings
api_host: 0.0.0.0
api_port: 8000
ui_port: 7860

# Pipeline Settings
work_base: ./outputs
default_scenes: 3
vertical: true
use_cuda: false

# Model Paths
bark_cli: ./voice_engine.py
sdxl_path: ./models/sdxl
```

## 🛠️ Architecture

### **Modern Full-Stack Architecture**
```
Frontend (Next.js) ↔ Backend (FastAPI) ↔ Enhanced Model Router ↔ AI Pipeline
       ↓                    ↓                      ↓                ↓
   React/TS            Job Management        Smart Fallbacks    HF/Local Models
```

### **Intelligent Generation Flow**
```
User Request → Enhanced Router → Analysis → Method Selection → Generation → Fallback → Result
     ↓              ↓              ↓            ↓              ↓          ↓        ↓
  UI Input    Network Check   Complexity   HF/Local/Cache   AI Models  Friendly  Content
```

### **Technology Stack**
#### **Frontend**
- **Next.js 15.4.6**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling with Kenya-first design
- **Inline SVG Icons**: Zero external dependencies for bulletproof UI stability
- **PWA Support**: Offline capability and mobile optimization

#### **Backend**
- **FastAPI**: High-performance Python API framework
- **Enhanced Model Router**: Intelligent fallback system
- **Job Management**: Real-time status tracking
- **Paystack Integration**: M-Pesa and local payment support

#### **AI Pipeline**
- **HuggingFace API**: Primary AI generation service
- **Local Models**: SDXL, Bark, Whisper for offline use
- **Smart Caching**: Semantic similarity matching
- **Fallback Chain**: HF → Paid APIs → Local → Cache → Friendly UI

## 📁 Project Structure
```
ShujaaStudio/
├── frontend/                    # Next.js React application
│   ├── src/
│   │   ├── app/                # App Router pages
│   │   │   ├── video-generate/ # Video generation interface
│   │   │   ├── news-generate/  # News video generation
│   │   │   ├── projects/       # Project management
│   │   │   ├── gallery/        # Content gallery
│   │   │   ├── analytics/      # Analytics dashboard
│   │   │   └── pricing/        # Subscription plans
│   │   ├── components/         # Reusable UI components
│   │   └── lib/               # Utilities and API client
├── backend/                    # FastAPI backend
│   ├── api.py                 # Main API endpoints
│   ├── enhanced_model_router.py # Intelligent routing system
│   ├── pipeline_orchestrator.py # AI pipeline management
│   └── services/              # Core services
├── docs/                      # Comprehensive documentation
│   ├── UI_IMPLEMENTATION_STATUS.md
│   ├── COMPREHENSIVE_TESTING_PLAN.md
│   └── VIDEO_GENERATION_FLOW_DESIGN.md
└── README.md                  # This file
```

## 🆚 Competitive Advantage

### **vs InVideo/Pictory/Synthesia**

| Feature | Competitors | Shujaa Studio | Advantage |
|---------|-------------|---------------|-----------|
| **Pricing** | $30-60 USD/month | **KES 2,500-15,000** | **40-60% cheaper** |
| **Cultural Content** | Generic Western | **Kenya-first authentic** | **Unique positioning** |
| **Payment Methods** | Credit cards only | **M-Pesa + local banking** | **Accessible to Africans** |
| **Offline Capability** | Cloud-only | **Complete offline mode** | **Privacy + performance** |
| **Mobile Optimization** | Desktop-first | **Mobile-first design** | **African usage patterns** |
| **AI Intelligence** | Template-based | **Semantic scene detection** | **Superior technology** |
| **Fallback Experience** | Technical errors | **Friendly Kenya messaging** | **Better UX** |

### **Market Position**
- **Primary**: Kenya and East Africa
- **Secondary**: African diaspora globally
- **Advantage**: Cultural authenticity + affordability + local payment methods

## 🧪 Testing & Quality Assurance

### **Testing Readiness: 100% Complete**
- ✅ **Frontend**: All UI components and workflows
- ✅ **Backend**: All API endpoints with mock responses
- ✅ **Integration**: End-to-end user flows
- ✅ **Mobile**: Perfect responsiveness across devices
- ✅ **Payment**: Paystack/M-Pesa integration ready

### **Testing Plan**
```bash
# Phase 1: Frontend Testing (No dependencies)
cd frontend && npm run dev
# Test: UI, navigation, forms, responsiveness

# Phase 2: Backend Testing (Minimal dependencies)
cd backend && python api.py
# Test: API endpoints, job management, status tracking

# Phase 3: Integration Testing
# Test: Complete user workflows, payment flows, content generation
```

### **Quality Metrics**
- **Performance**: Page load < 3 seconds
- **Mobile**: Perfect responsiveness on all devices
- **Accessibility**: WCAG 2.1 AA compliance
- **Security**: Payment integration security validated
- **UX**: Kenya-first cultural authenticity verified
- **UI Stability**: Zero external icon dependencies with inline SVGs

## 🎬 Usage Examples

### **Video Generation**
```python
from generate_video import ShujaaStudio

studio = ShujaaStudio()
video_path = studio.generate_video("A Luo folktale about the clever hare")
print(f"Video saved to: {video_path}")
```

### Web Interface
```bash
python generate_video.py
# Open browser to http://localhost:7860
```

## 🔧 Configuration

### Model Paths
Edit `generate_video.py` to point to your model locations:
```python
self.models_dir = Path("/path/to/your/models")
```

### External SSD Setup
```bash
# Mount external drive in WSL
sudo mount /dev/sdX /mnt/external

# Symlink models to external drive
ln -s /mnt/external/ai_models models
```

## 🎯 Use Cases

### Kenyan Context
- **Youth Content**: AI Sheng cartoons, music videos
- **Civic Education**: Anti-corruption explainers, election guides
- **Cultural Stories**: Luo/Kikuyu/Luhya legends
- **Educational**: Localized edutainment lessons
- **Entertainment**: Benga music video generator

### NGO Applications
- Community empowerment animations
- Health education videos
- Agricultural training content
- Women empowerment stories

## 🚀 Advanced Features

### Local Language Support
- Swahili voice synthesis
- Sheng text generation
- Local accent training
- Cultural context awareness

### Offline Deployment
- Docker containerization
- PyInstaller packaging
- LAN server deployment
- Mobile app integration

## 🤝 Contributing

This is an open-source project for African AI sovereignty. Contributions welcome!

### Development Setup
```bash
git clone <repository>
cd shujaa-studio
pip install -r requirements.txt
python generate_video.py
```

## 📄 Legal & Compliance

Shujaa Studio is committed to user privacy and data protection. Please review our policies:

*   [Privacy Policy](docs/PRIVACY_POLICY.md)
*   [Terms of Service](docs/TERMS_OF_SERVICE.md)
*   [GDPR Compliance Statement](docs/GDPR_COMPLIANCE.md)

## 📄 License

MIT License - Free for African content creators

## 🔗 Related Projects

- **Astella Plug**: OSINT toolkit integration
- **GhostCivic**: Civic tech platform
- **LuoNation**: Cultural preservation

---

**Built with ❤️ for African storytelling sovereignty**
