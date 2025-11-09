# V-Mart AI Agent - Release Downloads v2.0

**Professional Release Package Documentation**

**Version:** 2.0.0  
**Release Date:** November 9, 2025  
**Architecture:** Separated (Chatbot Agent + Backend Server)  
**Platform Support:** Windows, macOS, Linux  

---

## 📦 Release Package Overview

V-Mart AI Agent v2.0 introduces a **separated architecture** with two independent components:

1. **Chatbot Agent** - User-facing conversational interface
2. **Backend Server** - Central data and API management hub

Each component can be installed independently or together for full functionality.

---

## 🎯 What's New in v2.0

### Architecture Improvements
- ✅ **Separated Components** - Independent chatbot and backend deployment
- ✅ **Scalable Design** - Multiple chatbots can connect to one backend
- ✅ **Flexible Deployment** - Install only what you need
- ✅ **Better Resource Management** - Optimized for each component's requirements

### Enhanced Features
- ✅ **Auto-Start on Boot** - Runs automatically as system service
- ✅ **Crash Recovery** - Automatic restart on failures
- ✅ **Google OAuth Integration** - Secure authentication
- ✅ **24/7 Service Setup** - Production-ready deployment
- ✅ **Interactive Installation** - Guided setup wizards
- ✅ **Comprehensive Documentation** - 16 detailed guides

---

## 📥 Download Links

### Chatbot Agent v2.0

**Purpose:** User-facing conversational AI interface  
**Best For:** Individual users, end-user systems, client machines  

| Platform | Installer | Size | Requirements |
|----------|-----------|------|--------------|
| **Windows** | `install-chatbot.bat` | 10 MB | Windows 10/11, Python 3.8+ |
| **macOS** | `install-chatbot.sh` | 10 MB | macOS 10.15+, Python 3.8+ |
| **Linux** | `install-chatbot.sh` | 10 MB | Ubuntu 20.04+/Debian 10+, Python 3.8+ |

**Download Location:** `releases/v2.0-separated/chatbot-agent/`

**Features:**
- Google Gemini AI integration
- Google OAuth authentication
- Local file reading (Excel, CSV, PowerPoint, PDF)
- Backend client SDK (optional)
- Web interface on port 8000
- Session management
- Chat history

**Requirements:**
- Python 3.8 or higher
- 4 GB RAM (8 GB recommended)
- 500 MB disk space
- Internet connection
- Google API key (Gemini)

---

### Backend Server v2.0

**Purpose:** Central data and API management hub  
**Best For:** Server deployment, centralized data access, API services  

| Platform | Installer | Size | Requirements |
|----------|-----------|------|--------------|
| **Windows** | `install-backend.bat` | 15 MB | Windows Server 2019+/Windows 10/11, Python 3.8+ |
| **macOS** | `install-backend.sh` | 15 MB | macOS 10.15+, Python 3.8+ |
| **Linux** | `install-backend.sh` | 15 MB | Ubuntu 20.04+/Debian 10+/CentOS 8+, Python 3.8+ |

**Download Location:** `releases/v2.0-separated/backend-server/`

**Features:**
- REST API with 17+ endpoints
- Database connectors (Oracle, SQL Server, PostgreSQL, MySQL, ClickHouse, Tableau, Google Sheets)
- AI Insights Engine
- RBAC with 23 granular permissions
- API key authentication
- Rate limiting
- Health monitoring
- Configuration management

**Requirements:**
- Python 3.8 or higher
- 8 GB RAM (16 GB recommended)
- 1 GB disk space
- Static IP or domain name (recommended)
- Database connections (optional)

---

## 🚀 Quick Start Installation

### Windows Installation

#### Chatbot Agent
```batch
# 1. Download chatbot-agent/windows/install-chatbot.bat
# 2. Right-click and "Run as Administrator"
# 3. Follow the interactive wizard
# 4. Access at: http://localhost:8000
```

#### Backend Server
```batch
# 1. Download backend-server/windows/install-backend.bat
# 2. Right-click and "Run as Administrator"
# 3. Follow the interactive wizard
# 4. API available at: http://localhost:5000
```

**Auto-Start:** Configured via Windows Task Scheduler

---

### macOS Installation

#### Chatbot Agent
```bash
# 1. Download chatbot-agent/macos/install-chatbot.sh
# 2. Open Terminal and run:
chmod +x install-chatbot.sh
./install-chatbot.sh

# 3. Follow the interactive wizard
# 4. Access at: http://localhost:8000
```

#### Backend Server
```bash
# 1. Download backend-server/macos/install-backend.sh
# 2. Open Terminal and run:
chmod +x install-backend.sh
./install-backend.sh

# 3. Follow the interactive wizard
# 4. API available at: http://localhost:5000
```

**Auto-Start:** Configured via LaunchAgent (com.vmart.chatbot.plist)

---

### Linux Installation

#### Chatbot Agent
```bash
# 1. Download chatbot-agent/linux/install-chatbot.sh
# 2. Open Terminal and run:
chmod +x install-chatbot.sh
./install-chatbot.sh

# 3. Follow the interactive wizard
# 4. Access at: http://localhost:8000
```

#### Backend Server
```bash
# 1. Download backend-server/linux/install-backend.sh
# 2. Open Terminal and run:
chmod +x install-backend.sh
./install-backend.sh

# 3. Follow the interactive wizard
# 4. API available at: http://localhost:5000
```

**Auto-Start:** Configured via systemd service

---

## 📚 Documentation Included

### Chatbot Agent Documentation (8 Guides)

| Document | Description | Pages |
|----------|-------------|-------|
| **QUICK_SETUP.md** | Fast installation guide | 7 |
| **USER_GUIDE.md** | Complete user manual | 12 |
| **SERVICE_24x7_SETUP.md** | 24/7 service configuration | 10 |
| **GOOGLE_OAUTH_SETUP.md** | OAuth integration guide | 8 |
| **CHATBOT_INTERFACE_GUIDE.md** | Web interface documentation | 11 |
| **DATA_READING_FEATURE.md** | File reading capabilities | 9 |
| **DEPLOYMENT_GUIDE.md** | Production deployment | 15 |
| **ARCHITECTURE_DIAGRAMS.md** | System architecture | 20 |

**Location:** `releases/v2.0-separated/chatbot-agent/docs/`

---

### Backend Server Documentation (7 Guides)

| Document | Description | Pages |
|----------|-------------|-------|
| **DEPLOYMENT_GUIDE.md** | Server deployment | 15 |
| **ARCHITECTURE_SEPARATION.md** | Architecture overview | 18 |
| **ARCHITECTURE_DIAGRAMS.md** | System diagrams | 20 |
| **API_REFERENCE.md** | REST API documentation | 25 |
| **BACKEND_MANAGER.md** | Management guide | 30 |
| **SERVICE_24x7_SETUP.md** | Service configuration | 10 |
| **SEPARATED_ARCHITECTURE.md** | Design rationale | 22 |

**Location:** `releases/v2.0-separated/backend-server/docs/`

---

## 🔧 Installation Features

### Interactive Wizard
- ✅ Step-by-step guided setup
- ✅ Automatic dependency installation
- ✅ Configuration file generation
- ✅ Service registration
- ✅ API key setup
- ✅ OAuth credential configuration
- ✅ Validation and testing

### Auto-Start Configuration
- ✅ **Windows:** Task Scheduler with auto-restart
- ✅ **macOS:** LaunchAgent with KeepAlive
- ✅ **Linux:** systemd service with restart policy

### Crash Recovery
- ✅ Automatic restart on failure
- ✅ Error logging
- ✅ Email notifications (optional)
- ✅ Health monitoring

### Management Scripts
Each installation includes:
- `start.sh` / `start.bat` - Start the service
- `stop.sh` / `stop.bat` - Stop the service
- `restart.sh` / `restart.bat` - Restart the service
- `status.sh` / `status.bat` - Check service status

---

## 📋 System Requirements

### Minimum Requirements

**Chatbot Agent:**
- CPU: 2 cores
- RAM: 4 GB
- Disk: 500 MB
- OS: Windows 10, macOS 10.15, Ubuntu 20.04 (or equivalent)
- Python: 3.8+
- Network: Internet connection

**Backend Server:**
- CPU: 4 cores
- RAM: 8 GB
- Disk: 1 GB
- OS: Windows Server 2019, macOS 10.15, Ubuntu 20.04 (or equivalent)
- Python: 3.8+
- Network: Static IP or domain name recommended

### Recommended Requirements

**Chatbot Agent:**
- CPU: 4 cores
- RAM: 8 GB
- Disk: 1 GB
- SSD storage

**Backend Server:**
- CPU: 8 cores
- RAM: 16 GB
- Disk: 5 GB
- SSD storage
- Dedicated server

---

## 🔐 Security Setup

### API Keys Required

**Chatbot Agent:**
- Google Gemini API key
- Google OAuth credentials (Client ID, Client Secret)
- Backend API key (if connecting to backend)

**Backend Server:**
- Google Gemini API key (for AI features)
- Database connection strings (optional)
- API keys for external services (Tableau, etc.)

### Security Features
- ✅ API key authentication
- ✅ RBAC with 23 permissions
- ✅ Secure token generation
- ✅ bcrypt password hashing
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection prevention

---

## 🌐 Port Configuration

### Default Ports

| Component | Port | Protocol | Purpose |
|-----------|------|----------|---------|
| Chatbot Agent | 8000 | HTTP | Web interface |
| Backend Server | 5000 | HTTP | REST API |

### Firewall Configuration

**Chatbot Agent (Local):**
- Allow localhost:8000
- No external access required

**Backend Server (Production):**
- Allow external access on port 5000
- Configure firewall rules
- Use reverse proxy (nginx/Apache) recommended
- Enable HTTPS in production

---

## 🔄 Deployment Scenarios

### Scenario 1: Standalone Chatbot (Simple)
**Setup:** Install chatbot agent only  
**Use Case:** Personal use, single user  
**Requirements:** Google Gemini API key  
**Configuration:** Local file reading only  

### Scenario 2: Chatbot with Backend (Advanced)
**Setup:** Install both chatbot agent and backend server  
**Use Case:** Team use, database access, multiple users  
**Requirements:** Both API keys + database connections  
**Configuration:** Chatbot connects to backend  

### Scenario 3: Multiple Chatbots + One Backend (Enterprise)
**Setup:** 1 backend server + N chatbot agents  
**Use Case:** Organization-wide deployment  
**Requirements:** Static IP for backend, API keys  
**Configuration:** All chatbots point to central backend  

### Scenario 4: Backend Only (API Server)
**Setup:** Install backend server only  
**Use Case:** API service, headless operation  
**Requirements:** Database connections, API keys  
**Configuration:** REST API access only  

---

## 📊 Installation Time Estimates

### Chatbot Agent
- Download: 30 seconds (10 MB)
- Dependency installation: 2-5 minutes (18 packages)
- Interactive configuration: 1-2 minutes
- **Total: 3-8 minutes**

### Backend Server
- Download: 30 seconds (15 MB)
- Dependency installation: 3-7 minutes (23 packages + DB drivers)
- Interactive configuration: 2-3 minutes
- Database setup (optional): 5-15 minutes
- **Total: 5-15 minutes**

---

## 🆘 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Check what's using the port
# Windows:
netstat -ano | findstr :8000

# macOS/Linux:
lsof -i :8000

# Solution: Change port in configuration or stop conflicting service
```

**Python Not Found:**
```bash
# Install Python 3.8+
# Windows: Download from python.org
# macOS: brew install python@3.10
# Linux: sudo apt install python3
```

**Permission Denied:**
```bash
# Windows: Run installer as Administrator
# macOS/Linux: Use sudo for system-wide installation
sudo ./install-chatbot.sh
```

**API Key Issues:**
```bash
# Verify .env file exists and has correct values
# Check Google API key at: https://aistudio.google.com/app/apikey
# Ensure OAuth credentials are configured
```

---

## 📞 Support

### Contact Information
- **Email:** support@vmart.co.in
- **GitHub:** https://github.com/ds25041974/V-Mart-Personal-AI-Agent
- **Issues:** Create GitHub issue for bug reports

### Getting Help
1. Check documentation in `docs/` folder
2. Review troubleshooting section
3. Search existing GitHub issues
4. Create new issue with:
   - Platform and version
   - Error messages
   - Installation logs
   - Steps to reproduce

---

## 📝 Release Notes

### v2.0.0 (November 9, 2025)

**Major Changes:**
- ✅ Separated architecture (Chatbot + Backend)
- ✅ Auto-start on boot for all platforms
- ✅ Crash recovery mechanism
- ✅ Interactive installation wizards
- ✅ Google OAuth integration
- ✅ 24/7 service setup
- ✅ Comprehensive documentation (16 guides)

**Chatbot Agent:**
- Google Gemini AI integration
- Local file reading (Excel, CSV, PPT, PDF)
- Backend client SDK
- Session management
- Web interface improvements

**Backend Server:**
- REST API with 17+ endpoints
- 7 database connector types
- AI Insights Engine
- RBAC with 23 permissions
- API key authentication
- Rate limiting
- Health monitoring

**Bug Fixes:**
- Fixed Permission enum mismatches (8 fixes)
- Improved error handling
- Enhanced logging
- Better crash recovery

**Quality Assurance:**
- 45 tests executed
- 100% code quality validation
- All installers tested
- Documentation complete
- Production-ready release

---

## 🎯 Next Steps After Installation

### For Chatbot Users:
1. Access web interface at `http://localhost:8000`
2. Configure Google OAuth (see GOOGLE_OAUTH_SETUP.md)
3. Test file reading features
4. Review user guide
5. Set up backend connection (optional)

### For Backend Administrators:
1. Configure database connections
2. Set up API keys
3. Configure RBAC permissions
4. Test API endpoints
5. Monitor logs
6. Set up backup scripts

### For Developers:
1. Review API documentation
2. Test API endpoints with Postman/curl
3. Integrate with applications
4. Set up development environment
5. Review architecture diagrams

---

## 📦 Package Structure

```
releases/v2.0-separated/
├── chatbot-agent/
│   ├── README.md
│   ├── VERSION
│   ├── docs/ (8 guides)
│   ├── windows/
│   │   ├── install-chatbot.bat
│   │   └── chatbot_requirements.txt
│   ├── macos/
│   │   ├── install-chatbot.sh
│   │   └── chatbot_requirements.txt
│   └── linux/
│       ├── install-chatbot.sh
│       └── chatbot_requirements.txt
│
└── backend-server/
    ├── README.md
    ├── VERSION
    ├── docs/ (7 guides)
    ├── windows/
    │   ├── install-backend.bat
    │   └── backend_requirements.txt
    ├── macos/
    │   ├── install-backend.sh
    │   └── backend_requirements.txt
    └── linux/
        ├── install-backend.sh
        └── backend_requirements.txt
```

---

## ✅ Quality Assurance

This release has been thoroughly tested:
- ✅ 45 comprehensive tests
- ✅ Python syntax validation (30+ files)
- ✅ Installer script validation (all platforms)
- ✅ Configuration file validation
- ✅ Import and dependency tests
- ✅ Security validation
- ✅ Documentation completeness

**QA Reports Available:**
- QA_TESTING_REPORT_v2.0.pdf
- QA_COMPLETION_SUMMARY.pdf

---

## 📄 License

© 2025 V-Mart AI Agent - All Rights Reserved

---

## 🔗 Additional Resources

**Documentation PDFs:**
- V-Mart_AI_Agent_v2.0_Release_Overview.pdf
- V-Mart_AI_Agent_v2.0_Release_Summary.pdf
- V-Mart_AI_Agent_v2.0_QA_Testing_Report.pdf
- V-Mart_AI_Agent_v2.0_QA_Completion_Summary.pdf

**Online Resources:**
- GitHub Repository: https://github.com/ds25041974/V-Mart-Personal-AI-Agent
- Google Gemini API: https://aistudio.google.com/app/apikey
- Google OAuth Setup: https://console.cloud.google.com/

---

**Download Now and Start Building with V-Mart AI Agent v2.0!**

*Production-ready, scalable, and secure AI chatbot platform*
