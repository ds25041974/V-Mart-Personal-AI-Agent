@echo off
REM ============================================================================
REM V-Mart AI Agent - Chatbot Agent Installer for Windows
REM Version: 2.0.0
REM Description: Automated installer for chatbot agent (user-facing interface)
REM ============================================================================

setlocal enabledelayedexpansion

REM Color codes for output
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "NC=[0m"

REM Configuration
set "APP_NAME=V-Mart-Chatbot-Agent"
set "VERSION=2.0.0"
set "INSTALL_DIR=%USERPROFILE%\%APP_NAME%"
set "GITHUB_REPO=https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git"
set "PYTHON_MIN_VERSION=3.8"

REM ============================================================================
REM Banner
REM ============================================================================
cls
echo.
echo %BLUE%===================================================================%NC%
echo %BLUE%          V-Mart AI Agent - Chatbot Agent Installer            %NC%
echo %BLUE%                        Version 2.0.0                            %NC%
echo %BLUE%===================================================================%NC%
echo.
echo  %GREEN%User-Facing Chatbot Interface%NC%
echo  %YELLOW%Platform: Windows 10/11%NC%
echo.
echo %BLUE%===================================================================%NC%
echo.

REM ============================================================================
REM Check Python Installation
REM ============================================================================
echo %YELLOW%[1/8]%NC% Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%✗ Python not found%NC%
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %GREEN%✓ Python %PYTHON_VERSION% found%NC%
echo.

REM ============================================================================
REM Check pip
REM ============================================================================
echo %YELLOW%[2/8]%NC% Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo %RED%✗ pip not found%NC%
    echo Installing pip...
    python -m ensurepip --upgrade
)
echo %GREEN%✓ pip is available%NC%
echo.

REM ============================================================================
REM Create Installation Directory
REM ============================================================================
echo %YELLOW%[3/8]%NC% Creating installation directory...
if exist "%INSTALL_DIR%" (
    echo %YELLOW%⚠ Directory already exists: %INSTALL_DIR%%NC%
    set /p "OVERWRITE=Do you want to overwrite? (y/n): "
    if /i not "!OVERWRITE!"=="y" (
        echo Installation cancelled
        pause
        exit /b 1
    )
    rmdir /s /q "%INSTALL_DIR%"
)

mkdir "%INSTALL_DIR%"
echo %GREEN%✓ Created: %INSTALL_DIR%%NC%
echo.

REM ============================================================================
REM Clone Repository
REM ============================================================================
echo %YELLOW%[4/8]%NC% Downloading V-Mart AI Agent from GitHub...
git --version >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%⚠ Git not found. Downloading as ZIP...%NC%
    REM Fallback to downloading ZIP
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/ds25041974/V-Mart-Personal-AI-Agent/archive/refs/heads/main.zip' -OutFile '%TEMP%\vmart-agent.zip'"
    powershell -Command "Expand-Archive -Path '%TEMP%\vmart-agent.zip' -DestinationPath '%TEMP%\vmart-agent' -Force"
    xcopy /E /I /Y "%TEMP%\vmart-agent\V-Mart-Personal-AI-Agent-main\*" "%INSTALL_DIR%"
    del "%TEMP%\vmart-agent.zip"
    rmdir /s /q "%TEMP%\vmart-agent"
) else (
    git clone %GITHUB_REPO% "%INSTALL_DIR%"
)
echo %GREEN%✓ Downloaded successfully%NC%
echo.

REM ============================================================================
REM Create Virtual Environment
REM ============================================================================
echo %YELLOW%[5/8]%NC% Creating virtual environment...
cd /d "%INSTALL_DIR%"
python -m venv venv
if errorlevel 1 (
    echo %RED%✗ Failed to create virtual environment%NC%
    pause
    exit /b 1
)
echo %GREEN%✓ Virtual environment created%NC%
echo.

REM ============================================================================
REM Install Dependencies (Chatbot Only)
REM ============================================================================
echo %YELLOW%[6/8]%NC% Installing dependencies (Chatbot Agent)...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip

REM Install chatbot requirements
if exist "chatbot_requirements.txt" (
    python -m pip install -r chatbot_requirements.txt
) else (
    echo Installing core dependencies...
    python -m pip install Flask==3.0.0 Werkzeug==3.0.1
    python -m pip install google-api-python-client==2.108.0 google-auth-oauthlib==1.2.0
    python -m pip install google-generativeai==0.3.1
    python -m pip install authlib==1.3.0 requests==2.31.0
    python -m pip install schedule==1.2.0 python-dotenv==1.0.0
    python -m pip install pandas==2.1.4 numpy==1.26.2
    python -m pip install openpyxl==3.1.2 python-pptx==0.6.23 PyPDF2==3.0.1
    python -m pip install PyYAML==6.0.1
)

if errorlevel 1 (
    echo %RED%✗ Failed to install dependencies%NC%
    pause
    exit /b 1
)
echo %GREEN%✓ Dependencies installed%NC%
echo.

REM ============================================================================
REM Configure Environment
REM ============================================================================
echo %YELLOW%[7/8]%NC% Configuring environment...

REM Create .env file if not exists
if not exist ".env" (
    echo Creating .env file...
    (
        echo # V-Mart AI Agent - Chatbot Configuration
        echo # Version: 2.0.0
        echo.
        echo # Google Gemini API
        echo GEMINI_API_KEY=your-gemini-api-key-here
        echo.
        echo # Google OAuth 2.0
        echo GOOGLE_CLIENT_ID=your-client-id-here
        echo GOOGLE_CLIENT_SECRET=your-client-secret-here
        echo GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
        echo.
        echo # Backend Server ^(Optional - for database features^)
        echo BACKEND_URL=http://localhost:5000
        echo BACKEND_API_KEY=your-backend-api-key-here
        echo.
        echo # Chatbot Settings
        echo CHATBOT_PORT=8000
        echo CHATBOT_HOST=0.0.0.0
        echo SESSION_TIMEOUT=3600
        echo.
        echo # Local Files
        echo LOCAL_FILES_BASE_PATH=%USERPROFILE%\Documents
    ) > .env
)

REM Create chatbot_config.yaml if not exists
if not exist "config\chatbot_config.yaml" (
    if not exist "config" mkdir config
    (
        echo # V-Mart AI Agent - Chatbot Configuration
        echo # Version: 2.0.0
        echo.
        echo chatbot:
        echo   port: 8000
        echo   host: 0.0.0.0
        echo   debug: false
        echo   session_timeout: 3600
        echo.
        echo backend:
        echo   url: http://localhost:5000
        echo   api_key: ""
        echo   timeout: 30
        echo   retry_attempts: 3
        echo   cache_ttl: 300
        echo.
        echo google_oauth:
        echo   client_id: ""
        echo   client_secret: ""
        echo   redirect_uri: http://localhost:8000/auth/callback
        echo.
        echo local_files:
        echo   base_path: %USERPROFILE%\Documents
        echo   max_file_size: 52428800
        echo.
        echo logging:
        echo   level: INFO
        echo   file: logs/chatbot.log
        echo   format: "%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s"
    ) > config\chatbot_config.yaml
)

echo %GREEN%✓ Configuration files created%NC%
echo.

REM ============================================================================
REM Create Start Scripts
REM ============================================================================
echo Creating start scripts...

REM Create start-chatbot.bat
(
    echo @echo off
    echo cd /d "%%~dp0"
    echo call venv\Scripts\activate.bat
    echo python src\web\app.py
    echo pause
) > start-chatbot.bat

REM Create start-chatbot-background.vbs (silent start)
(
    echo Set oShell = CreateObject^("WScript.Shell"^)
    echo oShell.Run """%INSTALL_DIR%\start-chatbot.bat""", 0, False
) > start-chatbot-background.vbs

echo %GREEN%✓ Start scripts created%NC%
echo.

REM ============================================================================
REM Create Desktop Shortcut
REM ============================================================================
echo Creating desktop shortcut...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%USERPROFILE%\Desktop\V-Mart Chatbot.lnk'); $s.TargetPath = '%INSTALL_DIR%\start-chatbot.bat'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.IconLocation = 'imageres.dll,103'; $s.Description = 'V-Mart AI Chatbot Agent'; $s.Save()"
echo %GREEN%✓ Desktop shortcut created%NC%
echo.

REM ============================================================================
REM Setup Auto-Start (Task Scheduler)
REM ============================================================================
echo %YELLOW%[8/8]%NC% Setting up auto-start...
set /p "AUTOSTART=Do you want to auto-start chatbot on Windows login? (y/n): "
if /i "!AUTOSTART!"=="y" (
    schtasks /create /tn "V-Mart Chatbot Agent" /tr "%INSTALL_DIR%\start-chatbot-background.vbs" /sc onlogon /rl highest /f >nul 2>&1
    if errorlevel 1 (
        echo %YELLOW%⚠ Auto-start setup failed (requires admin rights)%NC%
        echo   You can manually add to Windows Startup folder
    ) else (
        echo %GREEN%✓ Auto-start configured%NC%
    )
) else (
    echo %YELLOW%⚠ Auto-start skipped%NC%
)
echo.

REM ============================================================================
REM Configuration Wizard
REM ============================================================================
echo %BLUE%===================================================================%NC%
echo                      CONFIGURATION WIZARD
echo %BLUE%===================================================================%NC%
echo.
echo The chatbot requires configuration before first use.
echo.
set /p "CONFIGURE_NOW=Configure now? (y/n): "
if /i "!CONFIGURE_NOW!"=="y" (
    echo.
    echo %YELLOW%Step 1: Google Gemini API Key%NC%
    echo.
    echo Get your API key from: https://aistudio.google.com/app/apikey
    echo.
    set /p "GEMINI_KEY=Enter your Gemini API key: "
    
    echo.
    echo %YELLOW%Step 2: Google OAuth Credentials%NC%
    echo.
    echo Get OAuth credentials from: https://console.cloud.google.com/apis/credentials
    echo.
    set /p "CLIENT_ID=Enter Google Client ID: "
    set /p "CLIENT_SECRET=Enter Google Client Secret: "
    
    echo.
    echo %YELLOW%Step 3: Backend Server ^(Optional^)%NC%
    echo.
    echo If you have a Backend Server running, enter its URL
    echo Leave blank to skip backend features
    echo.
    set /p "BACKEND_URL=Enter Backend URL (e.g., http://192.168.1.100:5000): "
    
    if not "!BACKEND_URL!"=="" (
        set /p "BACKEND_KEY=Enter Backend API Key: "
    )
    
    REM Update .env file
    powershell -Command "(Get-Content .env) -replace 'GEMINI_API_KEY=.*', 'GEMINI_API_KEY=!GEMINI_KEY!' | Set-Content .env"
    powershell -Command "(Get-Content .env) -replace 'GOOGLE_CLIENT_ID=.*', 'GOOGLE_CLIENT_ID=!CLIENT_ID!' | Set-Content .env"
    powershell -Command "(Get-Content .env) -replace 'GOOGLE_CLIENT_SECRET=.*', 'GOOGLE_CLIENT_SECRET=!CLIENT_SECRET!' | Set-Content .env"
    
    if not "!BACKEND_URL!"=="" (
        powershell -Command "(Get-Content .env) -replace 'BACKEND_URL=.*', 'BACKEND_URL=!BACKEND_URL!' | Set-Content .env"
        powershell -Command "(Get-Content .env) -replace 'BACKEND_API_KEY=.*', 'BACKEND_API_KEY=!BACKEND_KEY!' | Set-Content .env"
    )
    
    echo.
    echo %GREEN%✓ Configuration saved%NC%
)
echo.

REM ============================================================================
REM Installation Complete
REM ============================================================================
echo %BLUE%===================================================================%NC%
echo %GREEN%              INSTALLATION COMPLETED SUCCESSFULLY!%NC%
echo %BLUE%===================================================================%NC%
echo.
echo %GREEN%✓%NC% Chatbot Agent installed to: %INSTALL_DIR%
echo %GREEN%✓%NC% Desktop shortcut created
echo %GREEN%✓%NC% Virtual environment configured
echo %GREEN%✓%NC% Dependencies installed
echo.
echo %YELLOW%Next Steps:%NC%
echo.
echo 1. Complete configuration (if not done):
echo    Edit: %INSTALL_DIR%\.env
echo.
echo 2. Start the chatbot:
echo    - Double-click desktop shortcut "V-Mart Chatbot"
echo    - Or run: %INSTALL_DIR%\start-chatbot.bat
echo.
echo 3. Access the chatbot:
echo    Open browser: http://localhost:8000
echo.
echo 4. Read documentation:
echo    Location: %INSTALL_DIR%\docs\
echo.
echo %BLUE%===================================================================%NC%
echo              📖 DOCUMENTATION INCLUDED
echo %BLUE%===================================================================%NC%
echo.
echo ✓ Setup Guide               - docs/QUICK_SETUP.md
echo ✓ User Guide                - docs/USER_GUIDE.md
echo ✓ Service 24x7 Setup        - docs/SERVICE_24x7_SETUP.md
echo ✓ Google OAuth Setup        - docs/GOOGLE_OAUTH_SETUP.md
echo ✓ Chatbot Interface Guide   - docs/CHATBOT_INTERFACE_GUIDE.md
echo ✓ Data Reading Feature      - docs/DATA_READING_FEATURE.md
echo ✓ Deployment Guide          - docs/DEPLOYMENT_GUIDE.md
echo ✓ Architecture Diagrams     - docs/ARCHITECTURE_DIAGRAMS.md
echo.
echo %BLUE%===================================================================%NC%
echo.
set /p "START_NOW=Start chatbot now? (y/n): "
if /i "!START_NOW!"=="y" (
    start "" "%INSTALL_DIR%\start-chatbot.bat"
    echo.
    echo %GREEN%Chatbot starting...%NC%
    echo %GREEN%Access at: http://localhost:8000%NC%
    timeout /t 3
) else (
    echo.
    echo Start chatbot anytime using desktop shortcut or:
    echo %INSTALL_DIR%\start-chatbot.bat
)
echo.
echo Thank you for installing V-Mart AI Agent!
echo.
pause
