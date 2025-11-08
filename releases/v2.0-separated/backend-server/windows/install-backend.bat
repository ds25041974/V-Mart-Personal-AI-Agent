@echo off
REM ============================================================================
REM V-Mart AI Agent - Backend Server Installer for Windows
REM Version: 2.0.0
REM Description: Automated installer for Backend Management System
REM ============================================================================

setlocal enabledelayedexpansion

REM Color codes (using echo with special characters)
set "GREEN=[32m"
set "YELLOW=[33m"
set "RED=[31m"
set "BLUE=[34m"
set "NC=[0m"

echo %BLUE%================================================================%NC%
echo %BLUE%     V-Mart Backend Server Installer for Windows%NC%
echo %BLUE%     Version: 2.0.0%NC%
echo %BLUE%================================================================%NC%
echo.

REM ============================================================================
REM Step 1: Check Python Version
REM ============================================================================
echo %YELLOW%[1/9] Checking Python installation...%NC%

python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%Error: Python is not installed or not in PATH%NC%
    echo Please download and install Python 3.8 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Extract major and minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

if %PYTHON_MAJOR% LSS 3 (
    echo %RED%Error: Python 3.8+ is required. Found Python %PYTHON_VERSION%%NC%
    pause
    exit /b 1
)

if %PYTHON_MAJOR% EQU 3 if %PYTHON_MINOR% LSS 8 (
    echo %RED%Error: Python 3.8+ is required. Found Python %PYTHON_VERSION%%NC%
    pause
    exit /b 1
)

echo %GREEN%✓ Python %PYTHON_VERSION% is compatible%NC%
echo.

REM ============================================================================
REM Step 2: Check pip
REM ============================================================================
echo %YELLOW%[2/9] Checking pip...%NC%

python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo %RED%Error: pip is not installed%NC%
    echo Installing pip...
    python -m ensurepip --upgrade
    if errorlevel 1 (
        echo %RED%Failed to install pip%NC%
        pause
        exit /b 1
    )
)

echo %GREEN%✓ pip is available%NC%
echo.

REM ============================================================================
REM Step 3: Set Installation Directory
REM ============================================================================
set "INSTALL_DIR=%USERPROFILE%\V-Mart-Backend-Server"

echo %YELLOW%[3/9] Setting up installation directory...%NC%
echo Installation directory: %INSTALL_DIR%
echo.

REM ============================================================================
REM Step 4: Clone or Download Repository
REM ============================================================================
echo %YELLOW%[4/9] Downloading V-Mart Backend Server...%NC%

if exist "%INSTALL_DIR%" (
    echo Directory %INSTALL_DIR% already exists.
    set /p OVERWRITE="Overwrite existing installation? (y/N): "
    if /i not "!OVERWRITE!"=="y" (
        echo Installation cancelled.
        pause
        exit /b 0
    )
    rd /s /q "%INSTALL_DIR%"
)

REM Try git clone first
git --version >nul 2>&1
if not errorlevel 1 (
    echo Cloning from GitHub...
    git clone https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git "%INSTALL_DIR%"
    if not errorlevel 1 (
        echo %GREEN%✓ Repository cloned successfully%NC%
        goto :after_download
    )
)

REM Fallback to ZIP download
echo Git not available or clone failed. Downloading ZIP...
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/ds25041974/V-Mart-Personal-AI-Agent/archive/refs/heads/main.zip' -OutFile '%TEMP%\vmart-backend.zip'}"
if errorlevel 1 (
    echo %RED%Failed to download repository%NC%
    pause
    exit /b 1
)

powershell -Command "& {Expand-Archive -Path '%TEMP%\vmart-backend.zip' -DestinationPath '%TEMP%\vmart-backend-extract' -Force}"
move "%TEMP%\vmart-backend-extract\V-Mart-Personal-AI-Agent-main" "%INSTALL_DIR%"
rd /s /q "%TEMP%\vmart-backend-extract"
del "%TEMP%\vmart-backend.zip"

echo %GREEN%✓ Backend server downloaded%NC%

:after_download
cd /d "%INSTALL_DIR%"
echo.

REM ============================================================================
REM Step 5: Create Virtual Environment
REM ============================================================================
echo %YELLOW%[5/9] Creating Python virtual environment...%NC%

python -m venv .venv
if errorlevel 1 (
    echo %RED%Failed to create virtual environment%NC%
    pause
    exit /b 1
)

echo %GREEN%✓ Virtual environment created%NC%
echo.

REM ============================================================================
REM Step 6: Install Dependencies
REM ============================================================================
echo %YELLOW%[6/9] Installing Python dependencies...%NC%
echo This may take several minutes...

call .venv\Scripts\activate.bat

if exist "backend_requirements.txt" (
    python -m pip install --upgrade pip
    python -m pip install -r backend_requirements.txt
) else (
    echo Installing dependencies manually...
    python -m pip install --upgrade pip
    python -m pip install Flask==3.0.0 Flask-CORS==4.0.0
    python -m pip install cx_Oracle==8.3.0 pymssql==2.2.11 clickhouse-driver==0.2.6
    python -m pip install psycopg2-binary==2.9.9 PyMySQL==1.1.0
    python -m pip install tableauserverclient==0.29 google-api-python-client==2.108.0
    python -m pip install google-auth-httplib2==0.2.0 google-auth-oauthlib==1.2.0
    python -m pip install pandas==2.1.4 numpy==1.26.2 openpyxl==3.1.2
    python -m pip install PyYAML==6.0.1 python-dotenv==1.0.0
    python -m pip install cryptography==41.0.7 bcrypt==4.1.2
    python -m pip install google-generativeai==0.3.2
)

if errorlevel 1 (
    echo %RED%Error installing dependencies%NC%
    pause
    exit /b 1
)

echo %GREEN%✓ Dependencies installed successfully%NC%
echo.

REM ============================================================================
REM Step 7: Create Configuration Files
REM ============================================================================
echo %YELLOW%[7/9] Creating configuration files...%NC%

REM Create .env file
if not exist ".env" (
    echo Creating .env file...
    (
        echo # V-Mart Backend Server Configuration
        echo.
        echo # Backend Server Settings
        echo BACKEND_PORT=5000
        echo BACKEND_HOST=0.0.0.0
        echo SECRET_KEY=your-secret-key-here
        echo.
        echo # Google Gemini AI
        echo GOOGLE_API_KEY=your-gemini-api-key-here
        echo.
        echo # Database Connections ^(Optional^)
        echo # ORACLE_DSN=host:port/service_name
        echo # ORACLE_USER=username
        echo # ORACLE_PASSWORD=password
        echo.
        echo # MSSQL_SERVER=server_name
        echo # MSSQL_DATABASE=database_name
        echo # MSSQL_USER=username
        echo # MSSQL_PASSWORD=password
        echo.
        echo # POSTGRES_HOST=localhost
        echo # POSTGRES_PORT=5432
        echo # POSTGRES_DB=database_name
        echo # POSTGRES_USER=username
        echo # POSTGRES_PASSWORD=password
        echo.
        echo # MYSQL_HOST=localhost
        echo # MYSQL_PORT=3306
        echo # MYSQL_DB=database_name
        echo # MYSQL_USER=username
        echo # MYSQL_PASSWORD=password
        echo.
        echo # CLICKHOUSE_HOST=localhost
        echo # CLICKHOUSE_PORT=9000
        echo # CLICKHOUSE_USER=default
        echo # CLICKHOUSE_PASSWORD=
        echo.
        echo # Tableau Configuration
        echo # TABLEAU_SERVER=https://tableau.example.com
        echo # TABLEAU_SITE=site_name
        echo # TABLEAU_USERNAME=username
        echo # TABLEAU_PASSWORD=password
        echo.
        echo # Google Drive Configuration
        echo # GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json
    ) > .env
)

REM Create backend_config.yaml
if not exist "config\backend_config.yaml" (
    mkdir config 2>nul
    copy "config\backend_config.yaml" "config\backend_config.yaml.backup" 2>nul
)

echo %GREEN%✓ Configuration files created%NC%
echo.

REM ============================================================================
REM Step 8: Create Management Scripts
REM ============================================================================
echo %YELLOW%[8/9] Creating management scripts...%NC%

REM Create start-backend.bat
(
    echo @echo off
    echo cd /d "%INSTALL_DIR%"
    echo call .venv\Scripts\activate.bat
    echo echo Starting V-Mart Backend Server on port 5000...
    echo python backend_server.py
    echo pause
) > start-backend.bat

REM Create start-backend-background.vbs (for silent start)
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo WshShell.Run chr^(34^) ^& "%INSTALL_DIR%\start-backend.bat" ^& chr^(34^), 0
    echo Set WshShell = Nothing
) > start-backend-background.vbs

REM Create desktop shortcut
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\V-Mart Backend Server.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\start-backend.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'V-Mart Backend Server'; $Shortcut.Save()}"

echo %GREEN%✓ Management scripts created%NC%
echo.

REM ============================================================================
REM Step 9: Configure Auto-Start (Optional)
REM ============================================================================
echo %YELLOW%[9/9] Configuring auto-start...%NC%
set /p AUTOSTART="Enable auto-start on Windows startup? (y/N): "

if /i "!AUTOSTART!"=="y" (
    echo Setting up Task Scheduler...
    schtasks /create /tn "V-Mart Backend Server" /tr "\"%INSTALL_DIR%\start-backend-background.vbs\"" /sc onlogon /rl highest /f
    if not errorlevel 1 (
        echo %GREEN%✓ Auto-start configured%NC%
    ) else (
        echo %RED%Failed to configure auto-start%NC%
    )
) else (
    echo Auto-start not configured. You can run start-backend.bat manually.
)

echo.

REM ============================================================================
REM Configuration Wizard
REM ============================================================================
echo.
echo %BLUE%================================================================%NC%
echo %BLUE%                 Configuration Wizard%NC%
echo %BLUE%================================================================%NC%
echo.

set /p RUN_WIZARD="Would you like to configure the backend server now? (y/N): "

if /i "!RUN_WIZARD!"=="y" (
    echo.
    echo --- Google Gemini API Key ---
    set /p GEMINI_KEY="Enter your Google Gemini API key (or press Enter to skip): "
    if not "!GEMINI_KEY!"=="" (
        powershell -Command "(Get-Content .env) -replace 'GOOGLE_API_KEY=.*', 'GOOGLE_API_KEY=!GEMINI_KEY!' | Set-Content .env"
    )
    
    echo.
    echo --- Secret Key ---
    echo Generating a random secret key...
    for /f %%i in ('powershell -Command "[guid]::NewGuid().ToString()"') do set SECRET_KEY=%%i
    powershell -Command "(Get-Content .env) -replace 'SECRET_KEY=.*', 'SECRET_KEY=!SECRET_KEY!' | Set-Content .env"
    
    echo.
    echo --- Port Configuration ---
    set /p BACKEND_PORT="Backend server port [5000]: "
    if "!BACKEND_PORT!"=="" set BACKEND_PORT=5000
    powershell -Command "(Get-Content .env) -replace 'BACKEND_PORT=.*', 'BACKEND_PORT=!BACKEND_PORT!' | Set-Content .env"
    
    echo %GREEN%✓ Configuration saved%NC%
)

echo.

REM ============================================================================
REM Installation Complete
REM ============================================================================
echo.
echo %BLUE%================================================================%NC%
echo %GREEN%         Installation Complete!%NC%
echo %BLUE%================================================================%NC%
echo.
echo Installation directory: %INSTALL_DIR%
echo Backend server port: 5000 (default)
echo.
echo %YELLOW%Next Steps:%NC%
echo 1. Edit .env file to configure database connections
echo 2. Create default admin user (see BACKEND_MANAGER.md)
echo 3. Configure firewall to allow port 5000
echo 4. For production, set up SSL/TLS certificates
echo 5. Review docs\API_REFERENCE.md for API endpoints
echo.
echo %YELLOW%To start the backend server:%NC%
echo   - Double-click: start-backend.bat
echo   - Desktop shortcut: V-Mart Backend Server
echo   - Command line: cd "%INSTALL_DIR%" ^& start-backend.bat
echo.
echo %YELLOW%Documentation:%NC%
echo   See releases\v2.0-separated\backend-server\docs\ for guides
echo.

set /p START_NOW="Would you like to start the backend server now? (y/N): "

if /i "!START_NOW!"=="y" (
    echo Starting backend server...
    start "" "%INSTALL_DIR%\start-backend.bat"
)

echo.
echo Thank you for installing V-Mart Backend Server!
echo.
pause
