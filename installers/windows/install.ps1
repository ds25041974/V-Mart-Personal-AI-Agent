# V-Mart Personal AI Agent - Windows Installer
# Automated installation script for Windows 10/11
# Version: 1.0.0

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  V-Mart Personal AI Agent Installer" -ForegroundColor Cyan
Write-Host "  Version: 1.0.0" -ForegroundColor Cyan
Write-Host "  Platform: Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  Warning: Not running as Administrator" -ForegroundColor Yellow
    Write-Host "Some features may require elevated privileges" -ForegroundColor Yellow
    Write-Host ""
}

# Configuration
$APP_NAME = "V-Mart-AI-Agent"
$INSTALL_DIR = "$env:USERPROFILE\Documents\$APP_NAME"
$PYTHON_MIN_VERSION = "3.8"
$REPO_URL = "https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git"

# Step 1: Check Python Installation
Write-Host "🔍 Step 1/8: Checking Python installation..." -ForegroundColor Green

try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+)") {
        $version = [version]$matches[1]
        $minVersion = [version]$PYTHON_MIN_VERSION
        
        if ($version -ge $minVersion) {
            Write-Host "✅ Python $version found" -ForegroundColor Green
        } else {
            Write-Host "❌ Python version $version is too old. Minimum required: $PYTHON_MIN_VERSION" -ForegroundColor Red
            Write-Host "Please download Python 3.11+ from https://www.python.org/downloads/" -ForegroundColor Yellow
            exit 1
        }
    }
} catch {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    exit 1
}

# Step 2: Check pip
Write-Host ""
Write-Host "🔍 Step 2/8: Checking pip installation..." -ForegroundColor Green

try {
    $pipVersion = python -m pip --version 2>&1
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found. Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# Step 3: Create installation directory
Write-Host ""
Write-Host "📁 Step 3/8: Creating installation directory..." -ForegroundColor Green

if (Test-Path $INSTALL_DIR) {
    Write-Host "⚠️  Installation directory already exists: $INSTALL_DIR" -ForegroundColor Yellow
    $response = Read-Host "Do you want to reinstall? (y/n)"
    if ($response -ne "y") {
        Write-Host "Installation cancelled." -ForegroundColor Red
        exit 0
    }
    Write-Host "Removing existing installation..." -ForegroundColor Yellow
    Remove-Item -Path $INSTALL_DIR -Recurse -Force
}

New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
Write-Host "✅ Created: $INSTALL_DIR" -ForegroundColor Green

# Step 4: Download/Clone repository
Write-Host ""
Write-Host "📥 Step 4/8: Downloading V-Mart AI Agent..." -ForegroundColor Green

$useGit = $false
try {
    git --version | Out-Null
    $useGit = $true
} catch {
    Write-Host "ℹ️  Git not found. Will download ZIP instead." -ForegroundColor Yellow
}

if ($useGit) {
    Write-Host "Cloning repository..." -ForegroundColor Cyan
    git clone $REPO_URL $INSTALL_DIR
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to clone repository" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Downloading ZIP from GitHub..." -ForegroundColor Cyan
    $zipUrl = "https://github.com/ds25041974/V-Mart-Personal-AI-Agent/archive/refs/heads/main.zip"
    $zipPath = "$env:TEMP\vmart-ai-agent.zip"
    
    try {
        Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath
        Expand-Archive -Path $zipPath -DestinationPath "$env:TEMP\vmart-extract" -Force
        
        # Move files from extracted folder to install directory
        $extractedFolder = Get-ChildItem "$env:TEMP\vmart-extract" | Select-Object -First 1
        Copy-Item -Path "$($extractedFolder.FullName)\*" -Destination $INSTALL_DIR -Recurse -Force
        
        # Cleanup
        Remove-Item -Path $zipPath -Force
        Remove-Item -Path "$env:TEMP\vmart-extract" -Recurse -Force
        
        Write-Host "✅ Downloaded and extracted successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to download: $_" -ForegroundColor Red
        exit 1
    }
}

# Step 5: Create virtual environment
Write-Host ""
Write-Host "🐍 Step 5/8: Creating Python virtual environment..." -ForegroundColor Green

Set-Location $INSTALL_DIR
python -m venv venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment created" -ForegroundColor Green

# Step 6: Install dependencies
Write-Host ""
Write-Host "📦 Step 6/8: Installing Python dependencies..." -ForegroundColor Green
Write-Host "This may take a few minutes..." -ForegroundColor Yellow

& "$INSTALL_DIR\venv\Scripts\python.exe" -m pip install --upgrade pip
& "$INSTALL_DIR\venv\Scripts\python.exe" -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ All dependencies installed" -ForegroundColor Green

# Step 7: Configure environment
Write-Host ""
Write-Host "⚙️  Step 7/8: Configuring environment..." -ForegroundColor Green

$envFile = "$INSTALL_DIR\.env"
if (-not (Test-Path $envFile)) {
    $envTemplate = @"
# V-Mart AI Agent Environment Configuration

# Gemini AI API Key (Required)
# Get your API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Google Cloud OAuth (Optional - for Gmail/Drive integration)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# GitHub Token (Optional - for GitHub integration)
GITHUB_TOKEN=your_github_token_here

# Application Settings
PORT=5000
DEBUG=False
HOST=0.0.0.0

# Project Information
GOOGLE_CLOUD_PROJECT=gen-lang-client-0157247224
"@
    
    Set-Content -Path $envFile -Value $envTemplate
    Write-Host "✅ Created .env file: $envFile" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: You must configure your API keys!" -ForegroundColor Yellow
    Write-Host "Edit the file: $envFile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Required:" -ForegroundColor Cyan
    Write-Host "  1. GEMINI_API_KEY - Get from https://aistudio.google.com/app/apikey" -ForegroundColor White
    Write-Host ""
    Write-Host "Optional (for full features):" -ForegroundColor Cyan
    Write-Host "  2. Google OAuth credentials (for Gmail/Drive)" -ForegroundColor White
    Write-Host "  3. GitHub token (for repository integration)" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Step 8: Create Windows Service (Task Scheduler)
Write-Host ""
Write-Host "🔄 Step 8/8: Setting up auto-start service..." -ForegroundColor Green

# Create start script
$startScript = @"
@echo off
REM V-Mart AI Agent Startup Script
cd /d "$INSTALL_DIR"
call venv\Scripts\activate.bat
python main.py
pause
"@

$startScriptPath = "$INSTALL_DIR\start_vmart.bat"
Set-Content -Path $startScriptPath -Value $startScript

# Create hidden start script (no window)
$startHiddenScript = @"
@echo off
REM V-Mart AI Agent Silent Startup Script
cd /d "$INSTALL_DIR"
start /B venv\Scripts\pythonw.exe main.py
"@

$startHiddenPath = "$INSTALL_DIR\start_vmart_hidden.bat"
Set-Content -Path $startHiddenPath -Value $startHiddenScript

Write-Host "✅ Created startup scripts" -ForegroundColor Green

# Create scheduled task for auto-start
Write-Host ""
Write-Host "Creating auto-start task..." -ForegroundColor Cyan

$taskName = "V-Mart AI Agent"
$taskDescription = "V-Mart Personal AI Agent - Auto-start service"
$pythonExe = "$INSTALL_DIR\venv\Scripts\pythonw.exe"
$mainScript = "$INSTALL_DIR\main.py"

try {
    # Remove existing task if it exists
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }
    
    # Create new task
    $action = New-ScheduledTaskAction -Execute $pythonExe -Argument $mainScript -WorkingDirectory $INSTALL_DIR
    $trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartInterval (New-TimeSpan -Minutes 1) -RestartCount 3
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Limited
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description $taskDescription -Force | Out-Null
    
    Write-Host "✅ Auto-start service configured" -ForegroundColor Green
    Write-Host "   The AI Agent will start automatically when you log in" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️  Warning: Could not create auto-start task: $_" -ForegroundColor Yellow
    Write-Host "   You can start the agent manually using start_vmart.bat" -ForegroundColor Yellow
}

# Create desktop shortcut
Write-Host ""
Write-Host "Creating desktop shortcut..." -ForegroundColor Cyan

$desktopPath = [System.Environment]::GetFolderPath('Desktop')
$shortcutPath = "$desktopPath\V-Mart AI Agent.lnk"

try {
    $WScriptShell = New-Object -ComObject WScript.Shell
    $shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $startScriptPath
    $shortcut.WorkingDirectory = $INSTALL_DIR
    $shortcut.Description = "V-Mart Personal AI Agent"
    $shortcut.Save()
    
    Write-Host "✅ Desktop shortcut created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not create desktop shortcut" -ForegroundColor Yellow
}

# Installation complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Installation Location: $INSTALL_DIR" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configure API Keys:" -ForegroundColor White
Write-Host "   Edit: $envFile" -ForegroundColor Cyan
Write-Host "   Add your GEMINI_API_KEY (required)" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Start the Application:" -ForegroundColor White
Write-Host "   Option A: Double-click 'V-Mart AI Agent' on your desktop" -ForegroundColor Cyan
Write-Host "   Option B: Run: $startScriptPath" -ForegroundColor Cyan
Write-Host "   Option C: The service will auto-start on next login" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Access Web Interface:" -ForegroundColor White
Write-Host "   Open browser: http://localhost:5000" -ForegroundColor Cyan
Write-Host "   Or custom domain: http://vmartai:5000 (after hosts file setup)" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   User Guide: $INSTALL_DIR\docs\USER_GUIDE.md" -ForegroundColor Cyan
Write-Host "   Setup Guide: $INSTALL_DIR\docs\SETUP_GUIDE.md" -ForegroundColor Cyan
Write-Host "   API Reference: $INSTALL_DIR\docs\API_REFERENCE.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Quick Setup for Gemini API Key:" -ForegroundColor Yellow
Write-Host "   1. Visit: https://aistudio.google.com/app/apikey" -ForegroundColor Cyan
Write-Host "   2. Create API key" -ForegroundColor Cyan
Write-Host "   3. Add to .env file: GEMINI_API_KEY=your_key_here" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 Useful Commands:" -ForegroundColor Yellow
Write-Host "   Start: $startScriptPath" -ForegroundColor Cyan
Write-Host "   Logs: $INSTALL_DIR\logs\" -ForegroundColor Cyan
Write-Host ""
Write-Host "Need help? Check docs or visit: https://github.com/ds25041974/V-Mart-Personal-AI-Agent" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
