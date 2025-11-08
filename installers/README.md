# V-Mart Personal AI Agent - Installation Packages

**One-click installers for Windows, macOS, and Linux**

---

## 📥 Quick Download

Choose your operating system:

| Platform | Download Link | File Size | Requirements |
|----------|---------------|-----------|--------------|
| **Windows 10/11** | [INSTALL.bat](windows/INSTALL.bat) | ~15 KB | PowerShell |
| **macOS 10.15+** | [install.sh](macos/install.sh) | ~25 KB | Bash |
| **Linux (All)** | [install.sh](linux/install.sh) | ~28 KB | Bash |

---

## 🚀 Installation Instructions

### Windows

1. **Download**: [`windows/INSTALL.bat`](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/windows/INSTALL.bat)
2. **Run**: Double-click `INSTALL.bat`
3. **Follow**: On-screen instructions
4. **Configure**: Edit `.env` file with your API keys
5. **Access**: http://localhost:5000

**What it does**:
- ✅ Checks Python installation (3.8+)
- ✅ Downloads V-Mart AI Agent from GitHub
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Sets up Windows Task Scheduler for auto-start
- ✅ Creates desktop shortcut
- ✅ Configures environment variables

**Installation Location**: `C:\Users\YourUsername\Documents\V-Mart-AI-Agent`

---

### macOS

1. **Download**:
   ```bash
   curl -O https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/macos/install.sh
   ```

2. **Make executable**:
   ```bash
   chmod +x install.sh
   ```

3. **Run**:
   ```bash
   ./install.sh
   ```

4. **Configure**: Edit `.env` file
   ```bash
   nano ~/Applications/V-Mart-AI-Agent/.env
   ```

5. **Access**: http://localhost:5000

**What it does**:
- ✅ Checks Python installation (3.8+)
- ✅ Clones V-Mart AI Agent from GitHub
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Sets up LaunchAgent for auto-start
- ✅ Starts service automatically
- ✅ Creates management scripts (start, stop, restart, status)

**Installation Location**: `~/Applications/V-Mart-AI-Agent`

---

### Linux (Ubuntu/Debian/Fedora/CentOS)

1. **Download**:
   ```bash
   wget https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh
   # Or use curl:
   curl -O https://github.com/ds25041974/V-Mart-Personal-AI-Agent/raw/main/installers/linux/install.sh
   ```

2. **Make executable**:
   ```bash
   chmod +x install.sh
   ```

3. **Run**:
   ```bash
   ./install.sh
   ```

4. **Configure**: Edit `.env` file
   ```bash
   nano ~/opt/V-Mart-AI-Agent/.env
   ```

5. **Access**: http://localhost:5000

**What it does**:
- ✅ Detects Linux distribution
- ✅ Installs system dependencies (build tools, Python, git)
- ✅ Clones V-Mart AI Agent from GitHub
- ✅ Creates virtual environment
- ✅ Installs all Python dependencies
- ✅ Sets up systemd user service for auto-start
- ✅ Starts service automatically
- ✅ Creates management scripts (start, stop, restart, status, logs)

**Installation Location**: `~/opt/V-Mart-AI-Agent`

---

## 📋 What Gets Installed

### Common Components (All Platforms)

1. **V-Mart AI Agent Application**
   - Source code from GitHub repository
   - Python virtual environment
   - All required dependencies (Flask, Google APIs, etc.)

2. **Environment Configuration**
   - `.env` template file
   - Pre-configured settings
   - API key placeholders

3. **Documentation**
   - User Guide
   - Setup Guide
   - API Reference
   - Service 24x7 Setup Guide
   - Google OAuth Setup Guide
   - Dependencies Guide

4. **Auto-Start Service**
   - Windows: Task Scheduler task
   - macOS: LaunchAgent
   - Linux: systemd user service

5. **Management Scripts**
   - Start/Stop/Restart commands
   - Status checking
   - Log viewing
   - Uninstall script

### Python Dependencies Installed

```
Flask==3.0.0                    # Web framework
Werkzeug==3.0.1                 # WSGI utilities
google-api-python-client==2.108.0   # Google APIs
google-auth-httplib2==0.2.0     # Google auth transport
google-auth-oauthlib==1.2.0     # OAuth flow
google-generativeai==0.3.1      # Gemini AI
PyGithub==2.1.1                 # GitHub API
authlib==1.3.0                  # Authentication
requests==2.31.0                # HTTP client
schedule==1.2.0                 # Task scheduling
pandas==2.1.4                   # Data processing
numpy==1.26.2                   # Numerical computing
typing-extensions==4.9.0        # Type hints
python-dotenv==1.0.0            # Environment variables
```

---

## ⚙️ Post-Installation Setup

### Required: Configure Gemini API Key

1. **Get API Key**:
   - Visit: https://aistudio.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the key

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
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Restart Service**:
   - Windows: Restart computer or run `start_vmart.bat`
   - macOS: `~/Applications/V-Mart-AI-Agent/restart.sh`
   - Linux: `~/opt/V-Mart-AI-Agent/restart.sh`

### Optional: Google OAuth (for Gmail/Drive)

Follow the guide: [`GOOGLE_OAUTH_SETUP.md`](../docs/GOOGLE_OAUTH_SETUP.md)

### Optional: GitHub Integration

1. Create token at: https://github.com/settings/tokens
2. Add to `.env`: `GITHUB_TOKEN=your_token`

---

## 🔍 Verification

### Check if Service is Running

**Windows**:
```powershell
Get-ScheduledTask -TaskName "V-Mart AI Agent"
```

**macOS**:
```bash
~/Applications/V-Mart-AI-Agent/status.sh
```

**Linux**:
```bash
~/opt/V-Mart-AI-Agent/status.sh
# Or: systemctl --user status vmart-aiagent
```

### Test Web Interface

```bash
curl http://localhost:5000/health
# Should return: {"status": "ok"}
```

Open browser: http://localhost:5000

---

## 🛠️ Management

### Start/Stop/Restart

**Windows**:
```powershell
# Start
C:\Users\YourUsername\Documents\V-Mart-AI-Agent\start_vmart.bat

# Or use Task Scheduler
Start-ScheduledTask -TaskName "V-Mart AI Agent"
```

**macOS**:
```bash
~/Applications/V-Mart-AI-Agent/start.sh
~/Applications/V-Mart-AI-Agent/stop.sh
~/Applications/V-Mart-AI-Agent/restart.sh
```

**Linux**:
```bash
~/opt/V-Mart-AI-Agent/start.sh
~/opt/V-Mart-AI-Agent/stop.sh
~/opt/V-Mart-AI-Agent/restart.sh
```

### View Logs

**Windows**:
```powershell
type C:\Users\YourUsername\Documents\V-Mart-AI-Agent\logs\stdout.log
```

**macOS**:
```bash
tail -f ~/Applications/V-Mart-AI-Agent/logs/stdout.log
```

**Linux**:
```bash
~/opt/V-Mart-AI-Agent/logs.sh
# Or: journalctl --user -u vmart-aiagent -f
```

---

## 🔄 Updates

### Update to Latest Version

**All Platforms** (if Git is installed):
```bash
cd <installation-directory>
git pull origin main
source venv/bin/activate  # macOS/Linux
# Or: venv\Scripts\activate  (Windows)
pip install -r requirements.txt --upgrade
# Restart service
```

---

## ❌ Uninstall

**Windows**:
```powershell
# Remove scheduled task
Unregister-ScheduledTask -TaskName "V-Mart AI Agent" -Confirm:$false

# Delete installation directory
Remove-Item -Path "C:\Users\YourUsername\Documents\V-Mart-AI-Agent" -Recurse -Force
```

**macOS**:
```bash
~/Applications/V-Mart-AI-Agent/uninstall.sh
```

**Linux**:
```bash
~/opt/V-Mart-AI-Agent/uninstall.sh
```

---

## 🚨 Troubleshooting

### Common Issues

#### "Python not found"
- Install Python 3.8+ from python.org
- Ensure "Add to PATH" is checked (Windows)

#### "Permission denied"
- Windows: Run as Administrator
- macOS/Linux: `chmod +x install.sh`

#### "Service not starting"
- Check logs for errors
- Verify `.env` configuration
- Ensure API key is set

#### "Port 5000 already in use"
- Edit `.env`: Change `PORT=5001`
- Restart service

---

## 📚 Full Documentation

For complete documentation, see:

- **Installation Guide**: [`INSTALLATION_GUIDE.md`](../INSTALLATION_GUIDE.md)
- **User Guide**: [`docs/USER_GUIDE.md`](../docs/USER_GUIDE.md)
- **Setup Guide**: [`docs/SETUP_GUIDE.md`](../docs/SETUP_GUIDE.md)
- **Service Setup**: [`docs/SERVICE_24x7_SETUP.md`](../docs/SERVICE_24x7_SETUP.md)

---

## 💡 Quick Start Summary

1. Download installer for your OS
2. Run installer
3. Configure API key in `.env`
4. Restart service
5. Access http://localhost:5000

---

## 📊 System Requirements

### Minimum
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **Python**: 3.8+
- **RAM**: 4 GB
- **Disk**: 500 MB
- **Network**: Internet connection

### Recommended
- **OS**: Windows 11, macOS 13+, Ubuntu 22.04+
- **Python**: 3.11
- **RAM**: 8 GB
- **Disk**: 1 GB
- **Network**: Broadband

---

## 🔗 Links

- **Repository**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent
- **Issues**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/issues
- **Releases**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/releases

---

**Version**: 1.0.0  
**Last Updated**: November 8, 2025  
**License**: MIT
