# V-Mart AI Agent - Release Downloads

**Official installation packages for Windows, macOS, and Linux**

---

## 📦 Available Versions

### Version 2.0 - Separated Architecture (LATEST - Recommended)

**Release Date**: November 9, 2025  
**Architecture**: Client-Server (Chatbot Agent + Backend Server)

| Component | Description | Download |
|-----------|-------------|----------|
| **Chatbot Agent** | User-facing interface for individual systems | [v2.0-chatbot-agent](#v20---chatbot-agent) |
| **Backend Server** | Central data/API management hub | [v2.0-backend-server](#v20---backend-server) |

**✨ New Features**:
- 🔄 Separated architecture for better scalability
- 🌐 Network-based integration (LAN/WAN support)
- 🔐 API key authentication
- 📊 Centralized database management
- 🤖 AI-powered insights engine
- 👥 Role-based access control (RBAC)
- 🔌 Multiple database connectors (ClickHouse, PostgreSQL, Oracle, SQL Server)
- 📁 Data source connectors (Tableau, Google Drive, File System)

---

### Version 1.0 - Monolithic (Legacy)

**Release Date**: October 2025  
**Architecture**: All-in-one chatbot application

| Platform | Download |
|----------|----------|
| **All Platforms** | [v1.0-monolithic](#v10---monolithic-legacy) |

**Note**: Version 1.0 is maintained for backward compatibility. New installations should use Version 2.0.

---

## 🚀 V2.0 - Chatbot Agent

**User-facing chatbot interface for individual systems**

### Features
- ✅ Google Gemini AI integration
- ✅ Google OAuth authentication
- ✅ Local file connector (Excel, CSV, PowerPoint, PDF)
- ✅ Backend client SDK for remote data access
- ✅ Web-based chat interface
- ✅ Session management
- ✅ Auto-start on system boot
- ✅ Crash recovery and restart

### System Requirements
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+, or other Linux distributions
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB free space
- **Network**: Internet connection for Gemini AI and Google OAuth
- **Backend**: Optional - connect to Backend Server for database features

### Download Links

#### Windows (10/11)
```
releases/v2.0-separated/chatbot-agent/windows/
├── install-chatbot.bat          (Automated installer)
├── install-chatbot.ps1          (PowerShell installer)
├── requirements.txt             (Python dependencies)
└── README.md                    (Installation guide)
```
**Quick Install**: Download and run `install-chatbot.bat`

#### macOS (10.15+)
```
releases/v2.0-separated/chatbot-agent/macos/
├── install-chatbot.sh           (Automated installer)
├── requirements.txt             (Python dependencies)
└── README.md                    (Installation guide)
```
**Quick Install**: 
```bash
chmod +x install-chatbot.sh && ./install-chatbot.sh
```

#### Linux (Ubuntu/Debian/Fedora/CentOS)
```
releases/v2.0-separated/chatbot-agent/linux/
├── install-chatbot.sh           (Automated installer)
├── install-chatbot-systemd.sh   (Systemd service installer)
├── requirements.txt             (Python dependencies)
└── README.md                    (Installation guide)
```
**Quick Install**: 
```bash
chmod +x install-chatbot.sh && ./install-chatbot.sh
```

### Installation Steps

1. **Download** installer for your platform
2. **Run** the installer script
3. **Configure** Google OAuth credentials (follow prompts)
4. **Configure** backend URL (if using Backend Server)
5. **Access** chatbot at `http://localhost:8000`

### Documentation Included
- 📖 **Setup Guide** - Step-by-step installation
- 📖 **User Guide** - How to use the chatbot
- 📖 **Service 24x7 Setup** - Auto-start and crash recovery
- 📖 **Google OAuth Setup** - Authentication configuration
- 📖 **Chatbot Interface Guide** - UI/UX walkthrough
- 📖 **Data Reading Feature** - Local file analysis
- 📖 **Deployment Guide** - LAN/WAN deployment
- 📖 **Architecture Diagrams** - System overview

---

## 🖥️ V2.0 - Backend Server

**Central data and API management hub for server deployment**

### Features
- ✅ REST API with 10+ endpoints
- ✅ Database connectors: ClickHouse, PostgreSQL, Oracle, SQL Server
- ✅ Data source connectors: Tableau, Google Drive, File System
- ✅ AI Insights Engine (Gemini-powered)
- ✅ Role-Based Access Control (RBAC) - 23 permissions
- ✅ Configuration management
- ✅ API key authentication
- ✅ Rate limiting (100 requests/hour)
- ✅ Connection pooling
- ✅ Health monitoring

### System Requirements
- **OS**: Windows Server 2016+, macOS Server, Ubuntu Server 20.04+, or other Linux distributions
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 2GB free space
- **Network**: Static IP or domain name (for LAN/WAN access)
- **Databases**: Access to ClickHouse, PostgreSQL, Oracle, or SQL Server (optional)

### Download Links

#### Windows Server (2016+)
```
releases/v2.0-separated/backend-server/windows/
├── install-backend.bat          (Automated installer)
├── install-backend.ps1          (PowerShell installer)
├── requirements.txt             (Python dependencies)
└── README.md                    (Installation guide)
```
**Quick Install**: Download and run `install-backend.bat`

#### macOS Server
```
releases/v2.0-separated/backend-server/macos/
├── install-backend.sh           (Automated installer)
├── requirements.txt             (Python dependencies)
└── README.md                    (Installation guide)
```
**Quick Install**: 
```bash
chmod +x install-backend.sh && ./install-backend.sh
```

#### Linux Server (Ubuntu/Debian/Fedora/CentOS)
```
releases/v2.0-separated/backend-server/linux/
├── install-backend.sh           (Automated installer)
├── install-backend-systemd.sh   (Systemd service installer)
├── requirements.txt             (Python dependencies)
└── README.md                    (Installation guide)
```
**Quick Install**: 
```bash
chmod +x install-backend.sh && ./install-backend.sh
```

### Installation Steps

1. **Download** installer for your platform
2. **Run** the installer script
3. **Configure** database connections (optional)
4. **Generate** API keys for chatbot agents
5. **Start** backend server on port 5000
6. **Configure** firewall rules (allow port 5000)

### API Endpoints
- `GET /api/health` - Health check
- `GET /api/connections` - List database connections
- `POST /api/connections` - Create new connection
- `POST /api/query` - Execute database query
- `GET /api/schema/<name>` - Get database schema
- `POST /api/ai/analyze` - AI data analysis
- `POST /api/ai/recommend` - AI recommendations
- `GET /api/users` - List RBAC users
- `POST /api/users` - Create new user
- `GET /api/stats` - System statistics

### Documentation Included
- 📖 **Setup Guide** - Backend server installation
- 📖 **Deployment Guide** - LAN/WAN deployment strategies
- 📖 **Service 24x7 Setup** - Auto-start and monitoring
- 📖 **Architecture Separation** - Client-server architecture
- 📖 **Architecture Diagrams** - System flow charts
- 📖 **API Reference** - Complete API documentation
- 📖 **Backend Manager Guide** - Database and connector management
- 📖 **RBAC Guide** - Permission and role management

---

## 📚 V1.0 - Monolithic (Legacy)

**All-in-one chatbot application - maintained for backward compatibility**

### Features
- ✅ Google Gemini AI
- ✅ Google OAuth
- ✅ Local file reading
- ✅ Web interface
- ✅ All features in single application

### Download Links

#### All Platforms
```
releases/v1.0-monolithic/
├── windows/
│   ├── INSTALL.bat
│   └── install.ps1
├── macos/
│   └── install.sh
├── linux/
│   └── install.sh
└── README.md
```

### Migration to V2.0

If you're currently using V1.0 and want to migrate to V2.0:

1. **Backup** your current installation
2. **Export** your configuration (`.env` file)
3. **Install** V2.0 Chatbot Agent
4. **Optionally install** V2.0 Backend Server (for database features)
5. **Import** your configuration
6. **Test** the new installation
7. **Uninstall** V1.0 (optional)

See `MIGRATION_GUIDE.md` for detailed instructions.

---

## 📋 Comparison: V1.0 vs V2.0

| Feature | V1.0 Monolithic | V2.0 Chatbot Agent | V2.0 Backend Server |
|---------|----------------|-------------------|-------------------|
| **Architecture** | All-in-one | User interface | Central data hub |
| **Deployment** | Single system | Multiple systems | Central server |
| **Scalability** | Limited | High | Very High |
| **Network** | Local only | LAN/WAN | LAN/WAN |
| **Database Connectors** | None | Via backend | 7 connectors |
| **AI Insights** | Basic | Advanced (via backend) | Built-in engine |
| **RBAC** | No | Via backend | 23 permissions |
| **API Access** | No | REST client | REST server |
| **File Reading** | Yes | Yes | No |
| **Google OAuth** | Yes | Yes | No |
| **Auto-start** | Yes | Yes | Yes |
| **Crash Recovery** | Yes | Yes | Yes |
| **Best For** | Single user, simple use | Multiple users, scalable | Enterprise, centralized |

---

## 🔧 Installation Support

### Pre-installation Checklist

**For Chatbot Agent**:
- [ ] Python 3.8+ installed
- [ ] Internet connection
- [ ] Google OAuth credentials (see Google OAuth Setup guide)
- [ ] Backend Server URL (if using backend features)
- [ ] Backend API key (if using backend features)

**For Backend Server**:
- [ ] Python 3.8+ installed
- [ ] Static IP or domain name
- [ ] Firewall configured (port 5000 open)
- [ ] Database credentials (if using database connectors)
- [ ] Gemini API key (for AI insights)

### Troubleshooting

**Common Issues**:

1. **Python not found**
   - Install Python 3.8+ from python.org
   - Add Python to PATH environment variable

2. **Permission denied**
   - Windows: Run installer as Administrator
   - macOS/Linux: Use `chmod +x` on installer script

3. **Port already in use**
   - Chatbot: Change port in `chatbot_config.yaml`
   - Backend: Change port in `backend_config.yaml`

4. **Connection refused (chatbot → backend)**
   - Check backend server is running
   - Verify backend URL in `chatbot_config.yaml`
   - Check firewall rules on backend server

5. **API key invalid**
   - Regenerate API key on backend server
   - Update API key in `chatbot_config.yaml`

### Support Resources

- 📧 **Email**: support@vmart.co.in
- 🐛 **Issues**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/issues
- 📖 **Documentation**: See included guides in each release package
- 💬 **Community**: GitHub Discussions

---

## 📄 License

**MIT License**

Copyright (c) 2025 DSR

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 🎯 Quick Start

### For Home/Office Users (Recommended)

**Option 1: Chatbot Only** (No database features)
1. Download **V2.0 Chatbot Agent** for your OS
2. Run installer
3. Configure Google OAuth
4. Start using the chatbot

**Option 2: Chatbot + Backend** (Full features)
1. Install **V2.0 Backend Server** on a central computer/server
2. Install **V2.0 Chatbot Agent** on each user computer
3. Configure chatbots to connect to backend
4. Enjoy centralized data access

### For Enterprise (Recommended)

**Deployment Scenario**:
- **Backend Server**: Deploy on cloud (AWS/Azure/GCP) or on-premises server
- **Chatbot Agents**: Install on employee workstations
- **Network**: Configure via VPN or direct internet access with SSL/TLS
- **Databases**: Connect to existing enterprise databases
- **RBAC**: Configure roles and permissions for different teams

See **DEPLOYMENT_GUIDE.md** in Backend Server package for detailed enterprise setup.

---

**Version**: 2.0  
**Last Updated**: November 9, 2025  
**Developed by**: DSR
