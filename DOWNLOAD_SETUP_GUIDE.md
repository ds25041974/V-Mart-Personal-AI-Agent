# V-Mart Personal AI Agent - Installation Setup Download Guide

**Version:** 1.0.0  
**Release Date:** November 8, 2025  
**Author:** DSR | Powered by Gemini AI  
**Repository:** https://github.com/ds25041974/V-Mart-Personal-AI-Agent

---

## 📥 Quick Download Links

### Choose Your Operating System

| Operating System | Download Link | File Size | Installation Time |
|-----------------|---------------|-----------|-------------------|
| **Windows 10/11** | [Download INSTALL.bat](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/windows/INSTALL.bat) | 15 KB | 5-10 minutes |
| **macOS 10.15+** | [Download install.sh](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/macos/install.sh) | 25 KB | 5-10 minutes |
| **Linux (All Distros)** | [Download install.sh](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh) | 28 KB | 5-10 minutes |

---

## 🪟 Windows Installation

### System Requirements
- Windows 10 or Windows 11
- 4 GB RAM minimum (8 GB recommended)
- 500 MB free disk space
- Internet connection
- PowerShell (pre-installed on Windows)

### Download Link
```
https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/windows/INSTALL.bat
```

**Direct Download Button:** [Click Here to Download for Windows](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/windows/INSTALL.bat)

### Installation Steps

1. **Download the Installer**
   - Click the download link above
   - Save `INSTALL.bat` to your Downloads folder

2. **Run the Installer**
   - Double-click `INSTALL.bat`
   - Or right-click → "Run as Administrator" (recommended)
   - Windows may show a security warning - click "More info" → "Run anyway"

3. **Follow the Installation Wizard**
   - The installer will automatically:
     - ✅ Check Python installation (installs if needed)
     - ✅ Download V-Mart AI Agent from GitHub
     - ✅ Create isolated virtual environment
     - ✅ Install all required dependencies
     - ✅ Configure auto-start service (Task Scheduler)
     - ✅ Create desktop shortcut
     - ✅ Setup environment configuration

4. **Configure API Keys**
   - Open: `C:\Users\YourUsername\Documents\V-Mart-AI-Agent\.env`
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - Get API key from: https://aistudio.google.com/app/apikey

5. **Start the Application**
   - **Option A**: Double-click "V-Mart AI Agent" desktop shortcut
   - **Option B**: The service will auto-start on next login
   - **Option C**: Run `C:\Users\YourUsername\Documents\V-Mart-AI-Agent\start_vmart.bat`

6. **Access Web Interface**
   - Open browser: http://localhost:5000
   - Or custom domain: http://vmartai:5000 (after hosts file setup)

### What Gets Installed

- **Location**: `C:\Users\YourUsername\Documents\V-Mart-AI-Agent`
- **Components**:
  - V-Mart AI Agent application
  - Python virtual environment
  - All required libraries (Flask, Google APIs, etc.)
  - Windows Task Scheduler service
  - Desktop shortcut
  - Management scripts
  - Complete documentation

---

## 🍎 macOS Installation

### System Requirements
- macOS 10.15 (Catalina) or later
- 4 GB RAM minimum (8 GB recommended)
- 500 MB free disk space
- Internet connection
- Terminal access

### Download Link
```
https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/macos/install.sh
```

**Direct Download Button:** [Click Here to Download for macOS](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/macos/install.sh)

### Installation Steps

1. **Download the Installer**
   ```bash
   curl -O https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/macos/install.sh
   ```

2. **Make Executable**
   ```bash
   chmod +x install.sh
   ```

3. **Run the Installer**
   ```bash
   ./install.sh
   ```

4. **Follow the Prompts**
   - The installer will automatically:
     - ✅ Check Python version (3.8+)
     - ✅ Clone repository from GitHub
     - ✅ Create virtual environment
     - ✅ Install all dependencies
     - ✅ Setup LaunchAgent for auto-start
     - ✅ Start the service

5. **Configure API Keys**
   ```bash
   nano ~/Applications/V-Mart-AI-Agent/.env
   ```
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - Save: `Ctrl+O`, `Enter`, then `Ctrl+X`

6. **Restart Service**
   ```bash
   ~/Applications/V-Mart-AI-Agent/restart.sh
   ```

7. **Access Web Interface**
   - Open browser: http://localhost:5000

### What Gets Installed

- **Location**: `~/Applications/V-Mart-AI-Agent`
- **Components**:
  - V-Mart AI Agent application
  - Python virtual environment
  - All required libraries
  - LaunchAgent plist (auto-start)
  - Management scripts (start.sh, stop.sh, restart.sh, status.sh)
  - Complete documentation

### Management Commands

```bash
# Start service
~/Applications/V-Mart-AI-Agent/start.sh

# Stop service
~/Applications/V-Mart-AI-Agent/stop.sh

# Restart service
~/Applications/V-Mart-AI-Agent/restart.sh

# Check status
~/Applications/V-Mart-AI-Agent/status.sh

# Uninstall
~/Applications/V-Mart-AI-Agent/uninstall.sh
```

---

## 🐧 Linux Installation

### System Requirements
- Ubuntu 20.04+, Debian 10+, Fedora 34+, or CentOS 8+
- 4 GB RAM minimum (8 GB recommended)
- 500 MB free disk space
- Internet connection
- Terminal access
- sudo privileges (for system dependencies)

### Download Link
```
https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh
```

**Direct Download Button:** [Click Here to Download for Linux](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh)

### Installation Steps

1. **Download the Installer**
   
   Using wget:
   ```bash
   wget https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh
   ```
   
   Or using curl:
   ```bash
   curl -O https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh
   ```

2. **Make Executable**
   ```bash
   chmod +x install.sh
   ```

3. **Run the Installer**
   ```bash
   ./install.sh
   ```

4. **Follow the Prompts**
   - The installer will automatically:
     - ✅ Detect your Linux distribution
     - ✅ Install system dependencies (Python, build tools, git)
     - ✅ Clone repository from GitHub
     - ✅ Create virtual environment
     - ✅ Install all Python dependencies
     - ✅ Setup systemd user service
     - ✅ Start the service

5. **Configure API Keys**
   ```bash
   nano ~/opt/V-Mart-AI-Agent/.env
   ```
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - Save: `Ctrl+O`, `Enter`, then `Ctrl+X`

6. **Restart Service**
   ```bash
   ~/opt/V-Mart-AI-Agent/restart.sh
   ```

7. **Access Web Interface**
   - Open browser: http://localhost:5000

### What Gets Installed

- **Location**: `~/opt/V-Mart-AI-Agent`
- **Components**:
  - V-Mart AI Agent application
  - Python virtual environment
  - All required libraries
  - systemd user service
  - Management scripts (start.sh, stop.sh, restart.sh, status.sh, logs.sh)
  - Complete documentation

### Management Commands

```bash
# Start service
~/opt/V-Mart-AI-Agent/start.sh
# Or: systemctl --user start vmart-aiagent

# Stop service
~/opt/V-Mart-AI-Agent/stop.sh
# Or: systemctl --user stop vmart-aiagent

# Restart service
~/opt/V-Mart-AI-Agent/restart.sh
# Or: systemctl --user restart vmart-aiagent

# Check status
~/opt/V-Mart-AI-Agent/status.sh
# Or: systemctl --user status vmart-aiagent

# View logs
~/opt/V-Mart-AI-Agent/logs.sh
# Or: journalctl --user -u vmart-aiagent -f

# Uninstall
~/opt/V-Mart-AI-Agent/uninstall.sh
```

---

## 🔑 API Key Setup (Required)

### Get Your Gemini API Key

1. **Visit Google AI Studio**
   - URL: https://aistudio.google.com/app/apikey
   - Sign in with your Google account

2. **Create API Key**
   - Click "Create API Key" button
   - Select your project or create new one
   - Copy the generated API key

3. **Add to Configuration**
   - Open `.env` file in installation directory
   - Add line: `GEMINI_API_KEY=your_copied_api_key_here`
   - Save the file

4. **Restart Service**
   - Windows: Restart computer or run start script
   - macOS: Run `~/Applications/V-Mart-AI-Agent/restart.sh`
   - Linux: Run `~/opt/V-Mart-AI-Agent/restart.sh`

### Optional: Google OAuth (for Gmail/Drive Integration)

Follow the complete guide: [GOOGLE_OAUTH_SETUP.md](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/blob/main/docs/GOOGLE_OAUTH_SETUP.md)

### Optional: GitHub Integration

1. Create token at: https://github.com/settings/tokens
2. Add to `.env`: `GITHUB_TOKEN=your_token_here`
3. Restart service

---

## ✨ Features Included

### 🤖 AI-Powered Capabilities
- **Gemini Pro AI** - Advanced language understanding and generation
- **Natural Conversations** - Context-aware multi-turn dialogue
- **Intelligent Analysis** - Financial, sales, and business insights
- **Document Understanding** - PDF, Word, Excel processing
- **Decision Support** - AI-powered recommendations

### 📊 4-Tab Web Interface
1. **💬 Chat Tab** - Interactive AI conversations
2. **📊 Analysis Tab** - Financial and sales analysis
3. **📁 Files Tab** - Document search and management
4. **🎯 Decision Tab** - Business decision support

### 🔗 Integrations
- **Google Workspace** - Gmail and Drive integration
- **GitHub** - Repository management
- **Google Gemini AI** - Advanced AI capabilities
- **RESTful APIs** - Programmatic access

### 🔄 24x7 Operation
- **Auto-Start** - Starts on system boot
- **Auto-Restart** - Recovers from crashes
- **Network Aware** - Waits for network availability
- **Background Service** - Runs continuously
- **Low Resource** - Minimal CPU/memory usage

### 🛡️ Security & Privacy
- **OAuth 2.0** - Secure authentication
- **Local Processing** - Data stays on your machine
- **Environment Variables** - Secure credential storage
- **API Key Protection** - Never exposed in code

---

## 📚 Complete Documentation

All documentation is included in the installation:

### User Documentation
1. **INSTALLATION_GUIDE.md** - Complete installation guide
2. **USER_GUIDE.md** - User manual with tutorials
3. **QUICK_SETUP.md** - Quick start guide

### Technical Documentation
4. **SETUP_GUIDE.md** - Detailed platform setup
5. **SERVICE_24x7_SETUP.md** - Service configuration
6. **API_REFERENCE.md** - API endpoints and integration
7. **DEPENDENCIES.md** - Library documentation
8. **ARCHITECTURE.md** - System architecture
9. **CHATBOT_INTERFACE_GUIDE.md** - Interface guide

### Configuration Guides
10. **GOOGLE_OAUTH_SETUP.md** - OAuth configuration
11. **CUSTOM_DOMAIN_SETUP.md** - Custom domain setup
12. **DOCUMENT_SEARCH_FEATURE.md** - Document search guide

**View All Documentation Online:**  
https://github.com/ds25041974/V-Mart-Personal-AI-Agent/tree/main/docs

---

## 🔍 Verification & Testing

### Check Installation

After installation, verify everything is working:

1. **Check Service Status**
   - Windows: Check Task Scheduler
   - macOS: Run `~/Applications/V-Mart-AI-Agent/status.sh`
   - Linux: Run `~/opt/V-Mart-AI-Agent/status.sh`

2. **Test Health Endpoint**
   ```bash
   curl http://localhost:5000/health
   ```
   - Should return: `{"status": "ok"}`

3. **Access Web Interface**
   - Open browser: http://localhost:5000
   - You should see 4 tabs: Chat, Analysis, Files, Decision

4. **Test AI Chat**
   - Go to Chat tab
   - Type: "Hello"
   - Should receive AI-generated response

### View Logs

**Windows:**
```powershell
type C:\Users\YourUsername\Documents\V-Mart-AI-Agent\logs\stdout.log
```

**macOS:**
```bash
tail -f ~/Applications/V-Mart-AI-Agent/logs/stdout.log
```

**Linux:**
```bash
~/opt/V-Mart-AI-Agent/logs.sh
# Or: journalctl --user -u vmart-aiagent -f
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

#### Issue: "Python not found"
**Solution:**
- **Windows**: Install from python.org, check "Add to PATH"
- **macOS**: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11` (Ubuntu/Debian)

#### Issue: "Port 5000 already in use"
**Solution:**
- Edit `.env` file
- Change `PORT=5001` (or any available port)
- Restart service

#### Issue: "Service not starting"
**Solution:**
1. Check logs for error messages
2. Verify API key is configured in `.env`
3. Ensure all dependencies are installed
4. Try manual start to see errors

#### Issue: "API Key error"
**Solution:**
1. Verify API key in `.env` file
2. Get new key from https://aistudio.google.com/app/apikey
3. Ensure no extra spaces or quotes
4. Restart service

#### Issue: "Cannot access from other devices"
**Solution:**
- Edit `.env` file: `HOST=0.0.0.0`
- Configure firewall to allow port 5000
- Restart service

### Get Help

- **GitHub Issues**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/issues
- **Documentation**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/tree/main/docs
- **Repository**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent

---

## 🔄 Updates & Maintenance

### Update to Latest Version

**If Git is installed:**
```bash
cd <installation-directory>
git pull origin main
source venv/bin/activate  # macOS/Linux
# Or: venv\Scripts\activate  (Windows)
pip install -r requirements.txt --upgrade
# Restart service
```

**Manual Update:**
1. Backup your `.env` file
2. Download latest installer
3. Run installer (will preserve `.env`)
4. Restart service

### Check for Updates

Visit the repository releases page:  
https://github.com/ds25041974/V-Mart-Personal-AI-Agent/releases

---

## 📊 System Requirements Summary

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 10, macOS 10.15, Ubuntu 20.04 |
| **Python** | 3.8 or higher |
| **RAM** | 4 GB |
| **Storage** | 500 MB free space |
| **Network** | Internet connection |
| **Browser** | Any modern browser |

### Recommended Specifications

| Component | Recommendation |
|-----------|----------------|
| **Operating System** | Windows 11, macOS 13+, Ubuntu 22.04+ |
| **Python** | 3.11 (latest stable) |
| **RAM** | 8 GB or more |
| **Storage** | 1 GB free space |
| **Network** | Broadband connection |
| **Browser** | Chrome, Firefox, Safari, Edge (latest) |

---

## 📦 What's Included

### Python Dependencies (14 Packages)

All automatically installed:

```
Flask==3.0.0                      # Web framework
Werkzeug==3.0.1                   # WSGI utilities
google-api-python-client==2.108.0 # Google APIs
google-auth-httplib2==0.2.0       # Auth transport
google-auth-oauthlib==1.2.0       # OAuth flow
google-generativeai==0.3.1        # Gemini AI
PyGithub==2.1.1                   # GitHub API
authlib==1.3.0                    # Authentication
requests==2.31.0                  # HTTP client
schedule==1.2.0                   # Task scheduling
pandas==2.1.4                     # Data analysis
numpy==1.26.2                     # Numerical computing
typing-extensions==4.9.0          # Type hints
python-dotenv==1.0.0              # Environment variables
```

### Service Components

- **Windows**: Task Scheduler task (auto-start on login)
- **macOS**: LaunchAgent plist (auto-start on boot)
- **Linux**: systemd user service (auto-start on boot)

### Management Tools

- Start/Stop/Restart scripts
- Status checking utilities
- Log viewing tools
- Uninstall scripts
- Health check endpoints

---

## 🎯 Quick Start Summary

### 3-Step Installation

1. **Download** installer for your OS
2. **Run** the installer (double-click or `./install.sh`)
3. **Configure** API key in `.env` file

### 2-Minute Setup

1. Get Gemini API key: https://aistudio.google.com/app/apikey
2. Add to `.env` file: `GEMINI_API_KEY=your_key`

### Access

Open browser: **http://localhost:5000**

---

## 📞 Support & Community

### Getting Help

1. **Read Documentation** - Check the `/docs` folder
2. **Search Issues** - Look for similar problems
3. **Create Issue** - Report bugs or request features
4. **Community** - Ask questions in discussions

### Reporting Issues

Include in your report:
- Operating system and version
- Python version
- Error messages from logs
- Steps to reproduce
- Configuration (without API keys!)

### Contributing

Contributions are welcome! See:  
https://github.com/ds25041974/V-Mart-Personal-AI-Agent/blob/main/CONTRIBUTING.md

---

## 📄 License

**MIT License**

Copyright (c) 2025 V-Mart Personal AI Agent

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

Full license: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/blob/main/LICENSE

---

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| **Main Repository** | https://github.com/ds25041974/V-Mart-Personal-AI-Agent |
| **Installation Guide** | https://github.com/ds25041974/V-Mart-Personal-AI-Agent/blob/main/INSTALLATION_GUIDE.md |
| **Documentation** | https://github.com/ds25041974/V-Mart-Personal-AI-Agent/tree/main/docs |
| **Releases** | https://github.com/ds25041974/V-Mart-Personal-AI-Agent/releases |
| **Issues** | https://github.com/ds25041974/V-Mart-Personal-AI-Agent/issues |
| **Gemini API** | https://aistudio.google.com/app/apikey |
| **Google OAuth** | https://console.cloud.google.com/ |
| **GitHub Tokens** | https://github.com/settings/tokens |

---

## 🌟 Features at a Glance

✅ One-click automated installation  
✅ 24x7 auto-start service  
✅ 4-tab web interface (Chat, Analysis, Files, Decision)  
✅ Gemini AI integration  
✅ Google Workspace integration (Gmail, Drive)  
✅ GitHub integration  
✅ RESTful API access  
✅ Document search and analysis  
✅ Financial and sales analysis  
✅ Business decision support  
✅ Multi-platform support (Windows, macOS, Linux)  
✅ Complete documentation  
✅ Management scripts  
✅ Security and privacy focused  
✅ Open source (MIT License)  

---

## 🎉 Ready to Get Started?

### Download Now:

- **Windows**: [INSTALL.bat](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/windows/INSTALL.bat)
- **macOS**: [install.sh](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/macos/install.sh)
- **Linux**: [install.sh](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh)

### Installation takes only 5-10 minutes!

---

**Document Version:** 1.0.0  
**Last Updated:** November 8, 2025  
**Published by:** DSR  
**Powered by:** Google Gemini AI  
**Repository:** https://github.com/ds25041974/V-Mart-Personal-AI-Agent
