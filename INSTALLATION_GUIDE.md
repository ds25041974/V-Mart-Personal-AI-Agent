# 🚀 V-Mart Personal AI Agent - User Installation Setup

**Complete automated installation packages for Windows, macOS, and Linux**

---

## 📋 Overview

Welcome to the V-Mart Personal AI Agent installation guide! This document provides automated installers for all major operating systems with one-click setup that includes:

✅ **Automated Dependency Installation** - Python, pip, and all required packages  
✅ **24x7 Service Setup** - Auto-start on boot and network availability  
✅ **Environment Configuration** - Pre-configured .env templates  
✅ **Web Interface** - Full 4-tab chatbot interface  
✅ **API Integrations** - Google Workspace (Gmail, Drive), GitHub, Gemini AI  
✅ **Management Scripts** - Start, stop, restart, status, logs  
✅ **Complete Documentation** - User guides, API reference, setup guides  

---

## 📥 Download Installation Packages

Choose your operating system below:

### Windows (10/11)

**📦 Package**: [`installers/windows/INSTALL.bat`](installers/windows/INSTALL.bat)

**Download Links**:
- **Direct Download**: [INSTALL.bat](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/windows/INSTALL.bat)
- **PowerShell Script**: [install.ps1](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/windows/install.ps1)

**Requirements**:
- Windows 10 or Windows 11
- 4 GB RAM minimum (8 GB recommended)
- 500 MB free disk space
- Internet connection

### macOS (10.15+)

**📦 Package**: [`installers/macos/install.sh`](installers/macos/install.sh)

**Download Link**:
- **Direct Download**: [install.sh](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/macos/install.sh)

**Requirements**:
- macOS 10.15 (Catalina) or later
- 4 GB RAM minimum (8 GB recommended)
- 500 MB free disk space
- Internet connection

### Linux (Ubuntu 20.04+, Debian, Fedora, CentOS)

**📦 Package**: [`installers/linux/install.sh`](installers/linux/install.sh)

**Download Link**:
- **Direct Download**: [install.sh](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh)

**Requirements**:
- Ubuntu 20.04+, Debian 10+, Fedora 34+, or CentOS 8+
- 4 GB RAM minimum (8 GB recommended)
- 500 MB free disk space
- Internet connection

---

## 🪟 Windows Installation

### Quick Start

1. **Download** the installer:
   - Download [`INSTALL.bat`](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/windows/INSTALL.bat)
   - Save to your `Downloads` folder

2. **Run** the installer:
   - Double-click `INSTALL.bat`
   - Or right-click → "Run as Administrator" (recommended)

3. **Follow** the installation wizard:
   - Python version check
   - Download V-Mart AI Agent
   - Create virtual environment
   - Install dependencies
   - Configure environment
   - Setup auto-start service

4. **Configure** API keys:
   - Edit `.env` file (location shown in installer)
   - Add your `GEMINI_API_KEY` (required)
   - Add Google OAuth and GitHub tokens (optional)

5. **Start** the application:
   - Double-click "V-Mart AI Agent" desktop shortcut
   - Or run `start_vmart.bat` in installation directory
   - Or wait for auto-start on next login

6. **Access** the web interface:
   - Open browser: http://localhost:5000
   - Or custom domain: http://vmartai:5000

### What Gets Installed

- **Location**: `C:\Users\YourUsername\Documents\V-Mart-AI-Agent`
- **Python Environment**: Isolated virtual environment with all dependencies
- **Auto-Start Service**: Windows Task Scheduler task (runs at login)
- **Desktop Shortcut**: Quick access to start the application
- **Management Scripts**:
  - `start_vmart.bat` - Start the application
  - `start_vmart_hidden.bat` - Start without console window
- **Logs**: `logs\` directory

### Manual Installation (Alternative)

If the automated installer doesn't work:

```powershell
# 1. Install Python 3.11+ from python.org (check "Add to PATH")

# 2. Download and extract V-Mart AI Agent
git clone https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git
cd V-Mart-Personal-AI-Agent

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure .env file
copy .env.example .env
notepad .env

# 6. Run the application
python main.py
```

---

## 🍎 macOS Installation

### Quick Start

1. **Download** the installer:
   ```bash
   curl -O https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/macos/install.sh
   ```

2. **Make executable**:
   ```bash
   chmod +x install.sh
   ```

3. **Run** the installer:
   ```bash
   ./install.sh
   ```

4. **Follow** the prompts:
   - Python version check
   - Clone repository
   - Create virtual environment
   - Install dependencies
   - Configure LaunchAgent
   - Start service

5. **Configure** API keys:
   ```bash
   nano ~/Applications/V-Mart-AI-Agent/.env
   # Add your GEMINI_API_KEY
   ```

6. **Restart** the service:
   ```bash
   ~/Applications/V-Mart-AI-Agent/restart.sh
   ```

7. **Access** the web interface:
   - Browser: http://localhost:5000

### What Gets Installed

- **Location**: `~/Applications/V-Mart-AI-Agent`
- **Python Environment**: Isolated virtual environment
- **LaunchAgent**: `~/Library/LaunchAgents/com.vmart.aiagent.plist`
- **Auto-Start**: Starts at login and network availability
- **Management Scripts**:
  - `start.sh` - Start the service
  - `stop.sh` - Stop the service
  - `restart.sh` - Restart the service
  - `status.sh` - Check service status
  - `uninstall.sh` - Remove the service
- **Logs**: `logs/` directory

### Manual Installation (Alternative)

```bash
# 1. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python 3.11
brew install python@3.11

# 3. Clone repository
git clone https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git
cd V-Mart-Personal-AI-Agent

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Configure .env file
cp .env.example .env
nano .env

# 7. Run the application
python main.py
```

---

## 🐧 Linux Installation

### Quick Start (Ubuntu/Debian/Fedora/CentOS)

1. **Download** the installer:
   ```bash
   wget https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh
   ```
   
   Or using curl:
   ```bash
   curl -O https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh
   ```

2. **Make executable**:
   ```bash
   chmod +x install.sh
   ```

3. **Run** the installer:
   ```bash
   ./install.sh
   ```

4. **Follow** the prompts:
   - Python version check
   - Install system dependencies (requires sudo)
   - Clone repository
   - Create virtual environment
   - Install Python dependencies
   - Configure systemd service
   - Start service

5. **Configure** API keys:
   ```bash
   nano ~/opt/V-Mart-AI-Agent/.env
   # Add your GEMINI_API_KEY
   ```

6. **Restart** the service:
   ```bash
   ~/opt/V-Mart-AI-Agent/restart.sh
   # Or: systemctl --user restart vmart-aiagent
   ```

7. **Access** the web interface:
   - Browser: http://localhost:5000

### What Gets Installed

- **Location**: `~/opt/V-Mart-AI-Agent`
- **Python Environment**: Isolated virtual environment
- **Systemd Service**: `~/.config/systemd/user/vmart-aiagent.service`
- **Auto-Start**: Starts at boot and after network is online
- **Management Scripts**:
  - `start.sh` - Start the service
  - `stop.sh` - Stop the service
  - `restart.sh` - Restart the service
  - `status.sh` - Check service status
  - `logs.sh` - View live logs
  - `uninstall.sh` - Remove the service
- **Logs**: `logs/` directory and `journalctl`

### Distribution-Specific Notes

#### Ubuntu/Debian
```bash
# The installer will automatically run:
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip build-essential git
```

#### Fedora
```bash
# The installer will automatically run:
sudo dnf install python3.11 python3-pip @development-tools git
```

#### CentOS/RHEL
```bash
# The installer will automatically run:
sudo yum install python3.11 python3-pip groupinstall "Development Tools" git
```

### Manual Installation (Alternative)

```bash
# 1. Install Python 3.11 and dependencies
sudo apt update  # Ubuntu/Debian
sudo apt install python3.11 python3.11-venv python3-pip git

# 2. Clone repository
git clone https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git
cd V-Mart-Personal-AI-Agent

# 3. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure .env file
cp .env.example .env
nano .env

# 6. Run the application
python main.py
```

---

## ⚙️ Post-Installation Configuration

### Required: Gemini API Key

1. **Get API Key**:
   - Visit https://aistudio.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the generated key

2. **Add to .env file**:
   
   **Windows**:
   ```
   Edit: C:\Users\YourUsername\Documents\V-Mart-AI-Agent\.env
   ```
   
   **macOS**:
   ```
   Edit: ~/Applications/V-Mart-AI-Agent/.env
   ```
   
   **Linux**:
   ```
   Edit: ~/opt/V-Mart-AI-Agent/.env
   ```
   
   Add this line:
   ```
   GEMINI_API_KEY=AIzaSyYourActualAPIKeyHere
   ```

3. **Restart the service**:
   - Windows: Restart from Task Scheduler or reboot
   - macOS: `~/Applications/V-Mart-AI-Agent/restart.sh`
   - Linux: `~/opt/V-Mart-AI-Agent/restart.sh`

### Optional: Google OAuth (Gmail/Drive Integration)

1. **Create OAuth Credentials**:
   - Follow guide: [GOOGLE_OAUTH_SETUP.md](docs/GOOGLE_OAUTH_SETUP.md)
   
2. **Add to .env file**:
   ```
   GOOGLE_CLIENT_ID=your_client_id_here
   GOOGLE_CLIENT_SECRET=your_client_secret_here
   ```

3. **Restart service**

### Optional: GitHub Integration

1. **Create GitHub Token**:
   - Visit https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scopes: `repo`, `read:org`
   
2. **Add to .env file**:
   ```
   GITHUB_TOKEN=ghp_YourTokenHere
   ```

3. **Restart service**

### Optional: Custom Domain (vmartai)

**Windows**:
```powershell
# Run as Administrator
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "127.0.0.1 vmartai"
```

**macOS/Linux**:
```bash
sudo sh -c 'echo "127.0.0.1 vmartai" >> /etc/hosts'
```

**Access**:
- http://vmartai:5000

---

## 🎯 Verification & Testing

### Check Installation

1. **Verify service is running**:

   **Windows**:
   ```powershell
   # Check Task Scheduler
   Get-ScheduledTask -TaskName "V-Mart AI Agent"
   
   # Or check if process is running
   Get-Process -Name pythonw | Where-Object {$_.Path -like "*V-Mart-AI-Agent*"}
   ```

   **macOS**:
   ```bash
   ~/Applications/V-Mart-AI-Agent/status.sh
   # Or
   launchctl list | grep com.vmart.aiagent
   ```

   **Linux**:
   ```bash
   ~/opt/V-Mart-AI-Agent/status.sh
   # Or
   systemctl --user status vmart-aiagent
   ```

2. **Test web interface**:
   ```bash
   curl http://localhost:5000/health
   # Should return: {"status": "ok"}
   ```

3. **Open in browser**:
   - Navigate to http://localhost:5000
   - You should see the 4-tab interface:
     - 💬 Chat
     - 📊 Analysis
     - 📁 Files
     - 🎯 Decision

4. **Test Gemini AI**:
   - Go to Chat tab
   - Type: "Hello"
   - Should get AI response

### View Logs

**Windows**:
```powershell
cd C:\Users\YourUsername\Documents\V-Mart-AI-Agent\logs
type stdout.log
type stderr.log
```

**macOS**:
```bash
tail -f ~/Applications/V-Mart-AI-Agent/logs/stdout.log
tail -f ~/Applications/V-Mart-AI-Agent/logs/stderr.log
```

**Linux**:
```bash
# Live logs
~/opt/V-Mart-AI-Agent/logs.sh

# Or using journalctl
journalctl --user -u vmart-aiagent -f

# Log files
tail -f ~/opt/V-Mart-AI-Agent/logs/stdout.log
```

---

## 🔧 Management Commands

### Windows

```powershell
# Start
C:\Users\YourUsername\Documents\V-Mart-AI-Agent\start_vmart.bat

# Start hidden (no console window)
C:\Users\YourUsername\Documents\V-Mart-AI-Agent\start_vmart_hidden.bat

# Or use Task Scheduler
Start-ScheduledTask -TaskName "V-Mart AI Agent"
```

### macOS

```bash
# Start
~/Applications/V-Mart-AI-Agent/start.sh

# Stop
~/Applications/V-Mart-AI-Agent/stop.sh

# Restart
~/Applications/V-Mart-AI-Agent/restart.sh

# Status
~/Applications/V-Mart-AI-Agent/status.sh

# Uninstall
~/Applications/V-Mart-AI-Agent/uninstall.sh
```

### Linux

```bash
# Start
~/opt/V-Mart-AI-Agent/start.sh
# Or: systemctl --user start vmart-aiagent

# Stop
~/opt/V-Mart-AI-Agent/stop.sh
# Or: systemctl --user stop vmart-aiagent

# Restart
~/opt/V-Mart-AI-Agent/restart.sh
# Or: systemctl --user restart vmart-aiagent

# Status
~/opt/V-Mart-AI-Agent/status.sh
# Or: systemctl --user status vmart-aiagent

# Logs
~/opt/V-Mart-AI-Agent/logs.sh
# Or: journalctl --user -u vmart-aiagent -f

# Uninstall
~/opt/V-Mart-AI-Agent/uninstall.sh
```

---

## 🚨 Troubleshooting

### Installation Issues

#### "Python not found"
- **Windows**: Download from python.org, check "Add to PATH"
- **macOS**: Install via Homebrew: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11` (Ubuntu/Debian)

#### "pip not found"
```bash
# Windows
python -m ensurepip --upgrade

# macOS/Linux
python3 -m ensurepip --upgrade
# Or: sudo apt install python3-pip
```

#### "Permission denied"
- **Windows**: Right-click installer → "Run as Administrator"
- **macOS/Linux**: `chmod +x install.sh`

### Runtime Issues

#### "API Key error"
- Edit `.env` file
- Add valid `GEMINI_API_KEY=...`
- Restart service

#### "Port 5000 already in use"
- Edit `.env` file
- Change `PORT=5001` (or any available port)
- Restart service

#### "Service not starting"

**Windows**:
```powershell
# Check Task Scheduler logs
Get-ScheduledTaskInfo -TaskName "V-Mart AI Agent"
```

**macOS**:
```bash
# Check logs
tail -f ~/Applications/V-Mart-AI-Agent/logs/stderr.log
```

**Linux**:
```bash
# Check service status
systemctl --user status vmart-aiagent
journalctl --user -u vmart-aiagent -n 50
```

#### "Connection refused"
1. Check if service is running (see verification section)
2. Check logs for errors
3. Verify `.env` configuration
4. Try manual start to see errors:
   ```bash
   # Activate venv and run manually
   source venv/bin/activate  # macOS/Linux
   # Or: venv\Scripts\activate  (Windows)
   python main.py
   ```

### Network Issues

#### "Cannot access from other devices"
- Edit `.env` file
- Change `HOST=0.0.0.0` (allow all connections)
- Configure firewall to allow port 5000
- Restart service

#### "Custom domain not working"
- Verify hosts file entry
- Flush DNS cache:
  - **Windows**: `ipconfig /flushdns`
  - **macOS**: `sudo dscacheutil -flushcache`
  - **Linux**: `sudo systemd-resolve --flush-caches`

---

## 📚 Documentation

All documentation is included in the installation:

| Document | Description | Location |
|----------|-------------|----------|
| **USER_GUIDE.md** | Complete user guide with feature walkthroughs | `docs/USER_GUIDE.md` |
| **SETUP_GUIDE.md** | Detailed setup instructions for all platforms | `docs/SETUP_GUIDE.md` |
| **SERVICE_24x7_SETUP.md** | 24x7 service configuration and management | `docs/SERVICE_24x7_SETUP.md` |
| **API_REFERENCE.md** | API endpoints and integration guide | `docs/API_REFERENCE.md` |
| **GOOGLE_OAUTH_SETUP.md** | Google OAuth setup for Gmail/Drive | `docs/GOOGLE_OAUTH_SETUP.md` |
| **DEPENDENCIES.md** | Complete library documentation | `docs/DEPENDENCIES.md` |
| **ARCHITECTURE.md** | System architecture and design | `docs/ARCHITECTURE.md` |
| **CHATBOT_INTERFACE_GUIDE.md** | Web interface detailed guide | `docs/CHATBOT_INTERFACE_GUIDE.md` |

**View Online**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/tree/main/docs

---

## 🔄 Updates & Upgrades

### Update to Latest Version

**Using Git** (Recommended):
```bash
cd <installation-directory>
git pull origin main
source venv/bin/activate  # macOS/Linux
# Or: venv\Scripts\activate  (Windows)
pip install -r requirements.txt --upgrade
# Restart service
```

**Manual Update**:
1. Download latest release
2. Backup `.env` file
3. Replace all files except `.env`
4. Reinstall dependencies
5. Restart service

---

## ❓ Support & Help

### Getting Help

1. **Documentation**: Check the docs folder
2. **GitHub Issues**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/issues
3. **Repository**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent

### Reporting Issues

When reporting issues, include:
- Operating system and version
- Python version (`python --version`)
- Error messages from logs
- Steps to reproduce
- `.env` configuration (without API keys!)

---

## 📊 System Requirements Summary

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10+, macOS 10.15+, Ubuntu 20.04+ |
| **Python** | 3.8 or higher |
| **RAM** | 4 GB |
| **Disk** | 500 MB free |
| **Network** | Internet connection |

### Recommended Specifications

| Component | Recommendation |
|-----------|----------------|
| **OS** | Windows 11, macOS 13+, Ubuntu 22.04+ |
| **Python** | 3.11 (latest stable) |
| **RAM** | 8 GB or more |
| **Disk** | 1 GB free |
| **Network** | Broadband connection |
| **Browser** | Chrome, Firefox, Safari, Edge (latest) |

---

## 🎉 Quick Start Summary

1. **Download** installer for your OS
2. **Run** the installer (double-click or `./install.sh`)
3. **Configure** API key in `.env` file
4. **Restart** service
5. **Access** http://localhost:5000
6. **Enjoy** your AI agent!

---

**Version**: 1.0.0  
**Last Updated**: November 8, 2025  
**Repository**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent  
**License**: MIT
