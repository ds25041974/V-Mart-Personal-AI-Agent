# 🚀 V-Mart AI Agent - Complete Setup Guide

**Developed by: DSR | Inspired by: LA | Powered by: Gemini AI**

This comprehensive guide walks you through setting up the V-Mart Personal AI Agent on **Windows**, **macOS**, and **Linux**.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Platform-Specific Setup](#platform-specific-setup)
   - [Windows Setup](#windows-setup)
   - [macOS Setup](#macos-setup)
   - [Linux Setup](#linux-setup)
3. [Google Cloud Configuration](#google-cloud-configuration)
4. [Environment Configuration](#environment-configuration)
5. [Running the Application](#running-the-application)
6. [Network Access](#network-access)
7. [Auto-Start Configuration](#auto-start-configuration)
8. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10+, macOS 10.15+, Ubuntu 20.04+ |
| **Python** | 3.8 or higher |
| **RAM** | 4 GB |
| **Storage** | 500 MB free space |
| **Network** | Internet connection |

### Recommended Specifications

| Component | Recommendation |
|-----------|----------------|
| **OS** | Windows 11, macOS 13+, Ubuntu 22.04+ |
| **Python** | 3.11 (latest stable) |
| **RAM** | 8 GB or more |
| **Storage** | 1 GB free space |
| **Network** | Broadband connection |

---

## 🪟 Platform-Specific Setup

Choose your operating system below:

---

### Windows Setup

#### Step 1: Install Python

1. **Download Python:**
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.11 (or latest 3.x)

2. **Run the installer:**
   - ✅ Check **"Add Python to PATH"** (IMPORTANT!)
   - Click **"Install Now"**
   - Wait for installation to complete
   - Click **"Close"**

3. **Verify installation:**
   ```powershell
   python --version
   # Should show: Python 3.11.x
   
   pip --version
   # Should show: pip 23.x.x
   ```

#### Step 2: Install Git (Optional)

1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Run installer with default options
3. Verify: `git --version`

#### Step 3: Download the Project

**Option A: Using Git** (Recommended)
```powershell
cd C:\Users\YourUsername\Documents
git clone https://github.com/YOUR_REPO/V-Mart-AI-Agent.git
cd V-Mart-AI-Agent
```

**Option B: Download ZIP**
1. Download ZIP from repository
2. Extract to `C:\Users\YourUsername\Documents\V-Mart-AI-Agent`
3. Open PowerShell in that folder

#### Step 4: Create Virtual Environment

```powershell
# Navigate to project folder
cd "C:\Users\YourUsername\Documents\V-Mart-AI-Agent"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Your prompt should now show (venv)
```

**If you get an error about execution policy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try activating again
```

#### Step 5: Install Dependencies

```powershell
# Make sure venv is activated (you should see (venv) in prompt)
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- Flask 3.0.0 (web framework)
- google-generativeai (Gemini AI)
- google-auth, google-api-python-client
- authlib, requests
- All other dependencies

**Continue to [Environment Configuration](#environment-configuration)**

---

### macOS Setup

#### Step 1: Install Homebrew (Recommended)

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the post-installation instructions to add brew to PATH
```

#### Step 2: Install Python

**Option A: Using Homebrew** (Recommended)
```bash
# Install Python 3.11
brew install python@3.11

# Verify installation
python3 --version
# Should show: Python 3.11.x

pip3 --version
# Should show: pip 23.x.x
```

**Option B: Official Installer**
1. Download from [python.org](https://www.python.org/downloads/macos/)
2. Run the `.pkg` installer
3. Follow installation wizard

#### Step 3: Install Git

```bash
# Git comes with Xcode Command Line Tools
xcode-select --install

# Or install via Homebrew
brew install git

# Verify
git --version
```

#### Step 4: Download the Project

```bash
# Navigate to Documents
cd ~/Documents

# Clone repository
git clone https://github.com/YOUR_REPO/V-Mart-AI-Agent.git
cd V-Mart-AI-Agent
```

#### Step 5: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your prompt should now show (venv)
```

#### Step 6: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Common macOS Issue: pandas/numpy errors**

If you see errors installing pandas or numpy:
```bash
# Install Xcode Command Line Tools first
xcode-select --install

# Then try again
pip install -r requirements.txt
```

**Continue to [Environment Configuration](#environment-configuration)**

---

### Linux Setup

Instructions for **Ubuntu/Debian**, **Fedora/RHEL**, and **Arch Linux**.

#### Ubuntu/Debian Setup

**Step 1: Update System**
```bash
sudo apt update
sudo apt upgrade -y
```

**Step 2: Install Python and Dependencies**
```bash
# Install Python 3.11 (or latest available)
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Verify installation
python3 --version
pip3 --version
```

**Step 3: Download Project**
```bash
cd ~/Documents
git clone https://github.com/YOUR_REPO/V-Mart-AI-Agent.git
cd V-Mart-AI-Agent
```

**Step 4: Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 5: Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Fedora/RHEL/CentOS Setup

**Step 1: Update System**
```bash
sudo dnf update -y
```

**Step 2: Install Python**
```bash
sudo dnf install python3.11 python3-pip git -y

# Verify
python3 --version
pip3 --version
```

**Step 3-5: Same as Ubuntu**
Follow steps 3-5 from Ubuntu section above.

#### Arch Linux Setup

**Step 1: Update System**
```bash
sudo pacman -Syu
```

**Step 2: Install Python**
```bash
sudo pacman -S python python-pip git

# Verify
python --version
pip --version
```

**Step 3: Download and Setup**
```bash
cd ~/Documents
git clone https://github.com/YOUR_REPO/V-Mart-AI-Agent.git
cd V-Mart-AI-Agent

python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Continue to [Environment Configuration](#environment-configuration)**

---

## 🔐 Google Cloud Configuration

**(Optional - Required only for Gmail, Google Drive, Docs, Sheets, Slides integration)**

For local document search only, skip to [Environment Configuration](#environment-configuration).

For complete setup with Google services integration, see:
📄 **[GOOGLE_OAUTH_SETUP.md](./GOOGLE_OAUTH_SETUP.md)** - Complete OAuth setup guide

**Quick Overview:**
1. Create Google Cloud project
2. Enable APIs (Gmail, Drive, Docs, Sheets, Slides)
3. Configure OAuth consent screen
4. Create OAuth 2.0 credentials
5. Add credentials to `.env` file

---

## ⚙️ Environment Configuration

### Step 1: Create .env File

**All Platforms:**
```bash
# Copy the example file
cp .env.example .env

# Or create manually
touch .env
```

### Step 2: Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)

### Step 3: Edit .env File

Open `.env` in your text editor:

**Windows:**
```powershell
notepad .env
```

**macOS/Linux:**
```bash
nano .env
# or
code .env  # if using VS Code
```

### Step 4: Add Configuration

**Minimum Configuration** (for local document search):
```env
# Gemini API Key (REQUIRED)
GEMINI_API_KEY=AIzaSy...your_actual_key_here

# Flask Configuration
SECRET_KEY=your_random_secret_key_here
FLASK_ENV=production
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

**Full Configuration** (with Google OAuth):
```env
# Gemini API Key (REQUIRED)
GEMINI_API_KEY=AIzaSy...your_actual_key_here

# Google OAuth (Optional - for Gmail, Drive, etc.)
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret

# GitHub Integration (Optional)
GITHUB_TOKEN=ghp_your_github_token

# Flask Configuration
SECRET_KEY=your_random_secret_key_here
FLASK_ENV=production
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Domain Restrictions (Optional)
ALLOWED_DOMAINS=example.com,company.com
```

### Step 5: Generate SECRET_KEY

**Any Platform:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste as `SECRET_KEY` in `.env`

**Example Output:**
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
```

---

## ▶️ Running the Application

### First Run

**All Platforms (with venv activated):**
```bash
python main.py
```

You should see:
```
╔══════════════════════════════════════════════════════════╗
║        V-Mart Personal AI Agent Starting...              ║
║      Developed by: DSR | Inspired by: LA                 ║
║      Powered by: Gemini AI                               ║
╚══════════════════════════════════════════════════════════╝

🚀 Server running on http://0.0.0.0:8000
🌐 Access locally: http://localhost:8000
📱 Access from network: http://YOUR_IP:8000
```

### Access the Application

1. **Open browser**
2. **Navigate to:** http://localhost:8000
3. **Login:**
   - **Demo Mode:** Click "Demo Login" (no setup required)
   - **Full Mode:** Click "Login with Google" (requires OAuth setup)

### Stop the Server

Press `Ctrl + C` in the terminal

---

## 🌐 Network Access

Access the agent from other devices on your network (phones, tablets, other computers).

### Find Your IP Address

**Windows:**
```powershell
ipconfig
# Look for "IPv4 Address" under your active network adapter
# Example: 192.168.1.100
```

**macOS:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
# Or use the GUI: System Preferences → Network
```

**Linux:**
```bash
hostname -I
# Or
ip addr show
```

### Configure Firewall

**Windows:**
```powershell
# Allow port 8000 through firewall
netsh advfirewall firewall add rule name="V-Mart AI Agent" dir=in action=allow protocol=TCP localport=8000
```

**macOS:**
```bash
# System Preferences → Security & Privacy → Firewall
# Click "Firewall Options" → Add Python/your app
```

**Linux (ufw):**
```bash
sudo ufw allow 8000/tcp
sudo ufw reload
```

**Linux (firewalld):**
```bash
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### Access from Other Devices

1. Make sure devices are on **same WiFi network**
2. Open browser on other device
3. Navigate to: `http://YOUR_IP:8000`
   - Example: `http://192.168.1.100:8000`

---

## 🔄 Auto-Start Configuration

Configure the agent to start automatically on system boot.

### Windows - Task Scheduler

**Method 1: GUI Method**

1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click **"Create Task"**
3. **General Tab:**
   - Name: `V-Mart AI Agent`
   - Description: `Auto-start V-Mart AI Agent`
   - ✅ Check: "Run whether user is logged on or not"
   - ✅ Check: "Run with highest privileges"

4. **Triggers Tab:**
   - Click **"New"**
   - Begin the task: **"At startup"**
   - Click **"OK"**

5. **Actions Tab:**
   - Click **"New"**
   - Action: **"Start a program"**
   - Program/script: `C:\Path\To\Python\python.exe`
   - Arguments: `"C:\Path\To\V-Mart-AI-Agent\main.py"`
   - Start in: `C:\Path\To\V-Mart-AI-Agent`
   - Click **"OK"**

6. **Conditions Tab:**
   - ❌ Uncheck: "Start only if on AC power"

7. **Settings Tab:**
   - ✅ Check: "Allow task to be run on demand"
   - ✅ Check: "If task fails, restart every 1 minute"
   - Set attempts: **3 times**

8. Click **"OK"**

**Method 2: PowerShell Script**

Save as `install-autostart.ps1`:
```powershell
$taskName = "V-Mart AI Agent"
$pythonPath = (Get-Command python).Path
$scriptPath = Join-Path $PSScriptRoot "main.py"

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$scriptPath`"" -WorkingDirectory $PSScriptRoot
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
Write-Host "Task '$taskName' registered successfully!" -ForegroundColor Green
```

Run as Administrator:
```powershell
cd "C:\Path\To\V-Mart-AI-Agent"
.\install-autostart.ps1
```

### macOS - LaunchAgent

1. **Create plist file:**

```bash
nano ~/Library/LaunchAgents/com.vmart.aiagent.plist
```

2. **Add content** (replace YOUR_USERNAME):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vmart.aiagent</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/Documents/V-Mart-AI-Agent/venv/bin/python</string>
        <string>/Users/YOUR_USERNAME/Documents/V-Mart-AI-Agent/main.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/Documents/V-Mart-AI-Agent</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/tmp/vmart-agent.log</string>
    
    <key>StandardErrorPath</key>
    <string>/tmp/vmart-agent-error.log</string>
    
    <key>ThrottleInterval</key>
    <integer>30</integer>
</dict>
</plist>
```

3. **Load and start:**

```bash
# Load the agent
launchctl load ~/Library/LaunchAgents/com.vmart.aiagent.plist

# Start immediately
launchctl start com.vmart.aiagent

# Verify it's running
launchctl list | grep vmart
```

**Management Commands:**
```bash
# Stop
launchctl stop com.vmart.aiagent

# Unload (disable auto-start)
launchctl unload ~/Library/LaunchAgents/com.vmart.aiagent.plist

# View logs
tail -f /tmp/vmart-agent.log
tail -f /tmp/vmart-agent-error.log
```

### Linux - systemd Service

1. **Create service file:**

```bash
sudo nano /etc/systemd/system/vmart-agent.service
```

2. **Add content** (replace YOUR_USERNAME and paths):

```ini
[Unit]
Description=V-Mart Personal AI Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=YOUR_USERNAME
Group=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/Documents/V-Mart-AI-Agent
ExecStart=/home/YOUR_USERNAME/Documents/V-Mart-AI-Agent/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=vmart-agent

# Environment
Environment="PATH=/home/YOUR_USERNAME/Documents/V-Mart-AI-Agent/venv/bin:/usr/local/bin:/usr/bin:/bin"

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/YOUR_USERNAME/Documents/V-Mart-AI-Agent

[Install]
WantedBy=multi-user.target
```

3. **Enable and start:**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable vmart-agent.service

# Start now
sudo systemctl start vmart-agent.service

# Check status
sudo systemctl status vmart-agent.service
```

**Management Commands:**
```bash
# Stop
sudo systemctl stop vmart-agent.service

# Restart
sudo systemctl restart vmart-agent.service

# Disable auto-start
sudo systemctl disable vmart-agent.service

# View logs (live)
sudo journalctl -u vmart-agent.service -f

# View recent logs
sudo journalctl -u vmart-agent.service -n 50

# View logs since boot
sudo journalctl -u vmart-agent.service -b
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### ❌ "Module not found" or Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'google'
```

**Solution:**
```bash
# 1. Make sure virtual environment is activated
# You should see (venv) in your prompt

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

# 2. Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

#### ❌ API Key Errors

**Symptoms:**
```
Invalid API key
API_KEY_INVALID
Gemini API error
```

**Solution:**
1. Check `.env` file exists in project root
2. Verify `GEMINI_API_KEY=AIza...` is correct (no spaces, quotes)
3. Get new key from [Google AI Studio](https://aistudio.google.com/app/apikey)
4. Restart the server after editing `.env`

---

#### ❌ Port Already in Use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
Port 8000 is already in use
```

**Solution Option 1: Change Port**
```env
# Edit .env file
PORT=8001  # or any port between 8000-9000
```

**Solution Option 2: Kill Process Using Port**

**Windows:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

---

#### ❌ Permission Denied Errors

**Windows:**
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
# Fix file permissions
chmod +x main.py
chmod -R 755 .
```

---

#### ❌ Virtual Environment Activation Fails

**Windows PowerShell:**
```powershell
# If "cannot be loaded because running scripts is disabled"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
# If activation script not found
python3 -m venv venv --clear
source venv/bin/activate
```

---

#### ❌ Document Search Not Finding Files

**Symptoms:**
- "No documents found"
- Files exist but not showing up

**Solution:**
1. **Check file locations:**
   - Windows: `C:\Users\YourName\Documents`, `Desktop`, `Downloads`
   - macOS/Linux: `~/Documents`, `~/Desktop`, `~/Downloads`

2. **Verify file extensions:**
   - Supported: .pdf, .doc, .docx, .xlsx, .xls, .ppt, .pptx, .txt, .csv, .md

3. **Use specific keywords:**
   ```
   Instead of: "find files"
   Try: "find my Excel spreadsheets"
   Try: "show me PDF reports on desktop"
   ```

4. **Check file permissions:**
   ```bash
   # macOS/Linux
   ls -la ~/Documents
   
   # Windows
   dir "C:\Users\YourName\Documents"
   ```

---

#### ❌ OAuth / Google Login Errors

**Symptoms:**
```
redirect_uri_mismatch
invalid_client
API has not been used
```

**Solution:**
1. **Verify redirect URI:**
   - In Google Cloud Console, check Authorized redirect URIs
   - Must match exactly: `http://localhost:8000/auth/callback`
   - If you changed port, update OAuth settings

2. **Enable APIs:**
   - Go to Google Cloud Console → APIs & Services → Library
   - Enable: Gmail API, Drive API, Docs API, Sheets API, Slides API
   - Wait 1-2 minutes for propagation

3. **Check credentials in .env:**
   ```env
   GOOGLE_CLIENT_ID=...apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=...
   ```

4. **See detailed guide:**
   - Read `docs/GOOGLE_OAUTH_SETUP.md`

---

#### ❌ Network Access Issues

**Can't access from other devices**

**Solution:**

1. **Verify same WiFi network**
   ```bash
   # Find your IP address
   
   # Windows
   ipconfig
   
   # macOS
   ifconfig | grep "inet "
   
   # Linux
   hostname -I
   ```

2. **Configure firewall:**

   **Windows:**
   ```powershell
   netsh advfirewall firewall add rule name="V-Mart Agent" dir=in action=allow protocol=TCP localport=8000
   ```

   **macOS:**
   - System Preferences → Security & Privacy → Firewall
   - Firewall Options → Add Python

   **Linux:**
   ```bash
   sudo ufw allow 8000/tcp
   ```

3. **Check HOST in .env:**
   ```env
   HOST=0.0.0.0  # Not 127.0.0.1 or localhost
   PORT=8000
   ```

---

#### ❌ Server Crashes or Stops

**Check logs:**

**Windows (Task Scheduler):**
- Task Scheduler → Task Scheduler Library
- Right-click "V-Mart AI Agent" → Properties → History

**macOS:**
```bash
tail -f /tmp/vmart-agent-error.log
```

**Linux:**
```bash
sudo journalctl -u vmart-agent.service -n 100
```

**Common fixes:**
```bash
# Restart server

# Windows Task Scheduler
# Right-click task → Run

# macOS
launchctl stop com.vmart.aiagent
launchctl start com.vmart.aiagent

# Linux
sudo systemctl restart vmart-agent.service
```

---

#### ❌ High CPU/Memory Usage

**Solution:**
1. **Restart server regularly**
2. **Clear conversation history** in web interface
3. **Check for large files** being scanned
4. **Limit document search depth**

---

#### ❌ Slow Response Times

**Causes:**
- Large number of documents
- Slow internet connection
- API rate limits

**Solution:**
1. **Organize files:**
   - Keep folder structure shallow (max 2 levels)
   - Move rarely used files to non-scanned locations

2. **Check internet speed:**
   - Minimum recommended: 10 Mbps

3. **Monitor API usage:**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Check quota limits

---

### Platform-Specific Issues

#### Windows

**Issue: Python not found**
```powershell
# Add Python to PATH
# Reinstall Python and CHECK "Add Python to PATH"
```

**Issue: pip not recognized**
```powershell
python -m pip install --upgrade pip
```

#### macOS

**Issue: SSL Certificate errors**
```bash
# Install certificates
/Applications/Python\ 3.11/Install\ Certificates.command
```

**Issue: pandas/numpy installation fails**
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Then reinstall requirements
pip install -r requirements.txt
```

**Issue: Port 8000 used by AirPlay**
```bash
# Disable AirPlay Receiver
# System Preferences → Sharing → Uncheck "AirPlay Receiver"

# Or use different port in .env
PORT=8001
```

#### Linux

**Issue: python3-venv not found**
```bash
# Ubuntu/Debian
sudo apt install python3-venv python3-pip

# Fedora
sudo dnf install python3-virtualenv

# Arch
sudo pacman -S python-virtualenv
```

**Issue: Permission denied for systemd**
```bash
# Fix permissions
sudo chown YOUR_USERNAME:YOUR_USERNAME /home/YOUR_USERNAME/Documents/V-Mart-AI-Agent -R

# Then restart service
sudo systemctl restart vmart-agent.service
```

---

### 📊 Diagnostic Commands

**Check Python installation:**
```bash
python --version  # or python3 --version
pip --version     # or pip3 --version
```

**Check virtual environment:**
```bash
# Should show (venv) in prompt when activated
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

**Check installed packages:**
```bash
pip list
pip show flask
pip show google-generativeai
```

**Test API key:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('GEMINI_API_KEY')[:10] + '...')"
```

**Check server status:**
```bash
# See if port is in use
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
```

**Test network connectivity:**
```bash
# Ping your own IP from another device
ping YOUR_IP_ADDRESS

# Or use curl
curl http://YOUR_IP:8000
```

---

## 📚 Additional Resources

### Documentation Files

| File | Description |
|------|-------------|
| **USER_GUIDE.md** | Complete user manual for using the agent |
| **GOOGLE_OAUTH_SETUP.md** | Step-by-step OAuth configuration |
| **DOCUMENT_SEARCH_FEATURE.md** | Document search functionality details |
| **QUICK_SETUP.md** | Quick start guide (5 minutes) |
| **README.md** | Project overview and features |

### External Resources

- **Python Documentation:** [docs.python.org](https://docs.python.org/3/)
- **Flask Documentation:** [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- **Gemini API Docs:** [ai.google.dev](https://ai.google.dev/)
- **Google Cloud Console:** [console.cloud.google.com](https://console.cloud.google.com/)
- **Google AI Studio:** [aistudio.google.com](https://aistudio.google.com/)

---

## 🆘 Getting Help

### Before Asking for Help

1. ✅ Check this troubleshooting section
2. ✅ Read error messages carefully
3. ✅ Search documentation files
4. ✅ Try basic fixes (restart, check .env, check logs)
5. ✅ Verify Python and dependencies installed

### Information to Provide

When reporting issues, include:

1. **Operating System:** Windows/macOS/Linux version
2. **Python Version:** `python --version`
3. **Error Message:** Full text or screenshot
4. **Steps to Reproduce:** What you did before error
5. **Log Files:** Recent logs from terminal or system
6. **Configuration:** Anonymized .env file (hide API keys!)

**Example Issue Report:**
```
OS: macOS 13.2
Python: 3.11.5
Error: ModuleNotFoundError: No module named 'google.generativeai'

Steps:
1. Activated venv
2. Ran python main.py
3. Got error above

Logs:
[full error traceback here]

.env config:
GEMINI_API_KEY=AIza... (hidden)
PORT=8000
DEBUG=False
```

---

## ✅ Post-Setup Checklist

After completing setup, verify:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip list` shows packages)
- [ ] `.env` file exists with API key
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000
- [ ] Demo login works
- [ ] Document search finds local files
- [ ] (Optional) Google OAuth configured
- [ ] (Optional) Auto-start configured
- [ ] (Optional) Firewall configured for network access

---

## 🎯 Quick Reference

### Essential Commands

**Start Server:**
```bash
# Activate venv first, then:
python main.py
```

**Update Application:**
```bash
git pull
pip install --upgrade -r requirements.txt
python main.py
```

**Restart Auto-Start Service:**

**Windows:**
```powershell
# Task Scheduler → Right-click task → End → Run
```

**macOS:**
```bash
launchctl stop com.vmart.aiagent && launchctl start com.vmart.aiagent
```

**Linux:**
```bash
sudo systemctl restart vmart-agent.service
```

**View Logs:**

**macOS:**
```bash
tail -f /tmp/vmart-agent.log
```

**Linux:**
```bash
sudo journalctl -u vmart-agent.service -f
```

---

## 🎓 Next Steps

After successful setup:

1. 📖 **Read USER_GUIDE.md** - Learn all features
2. 🧪 **Test document search** - Add files and search
3. ⚙️ **Configure OAuth** (optional) - For Gmail, Drive access
4. 🔄 **Set up auto-start** - Launch on boot
5. 📱 **Enable network access** - Use from other devices
6. 🎨 **Customize responses** - Train for your use case

---

**Setup complete! 🎉**

**Access your AI agent at: http://localhost:8000**

**Developed by: DSR | Inspired by: LA | Powered by: Gemini AI**

---

*Last Updated: January 2025*  
*Version: 2.0*  
*Platforms: Windows 10+, macOS 10.15+, Ubuntu 20.04+*

## Getting Help

### Internal Support
- **Email**: support@vmartretail.com
- **Slack**: #ai-agent-support
- **IT Helpdesk**: ext. 1234

### Documentation
- Check `docs/architecture.md` for system design
- Review `README.md` for feature overview

### Logs Location

| Platform | Log Location |
|----------|-------------|
| Windows | Task Scheduler → History |
| macOS | `/tmp/vmart-agent.log` and `/tmp/vmart-agent-error.log` |
| Linux | `sudo journalctl -u vmart-agent.service` |

---

## Next Steps

After successful setup:

1. ✅ Test all features (chat, analysis, file management)
2. ✅ Configure scheduled tasks
3. ✅ Set up email templates
4. ✅ Connect GitHub repositories
5. ✅ Customize agent responses for your department
6. ✅ Train team members on usage

---

**Setup Version**: 1.0  
**Last Updated**: 2024  
**Maintained by**: V-Mart IT Department
