#!/bin/bash
# ============================================================================
# V-Mart AI Agent - Backend Server Installer for macOS
# Version: 2.0.0
# Description: Automated installer for Backend Management System
# ============================================================================

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}     V-Mart Backend Server Installer for macOS${NC}"
echo -e "${BLUE}     Version: 2.0.0${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""

# ============================================================================
# Step 1: Check Python Installation
# ============================================================================
echo -e "${YELLOW}[1/9]${NC} Checking Python installation..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    echo "Or install via Homebrew: brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

# Check version (must be 3.8+)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}Error: Python 3.8+ is required. Found Python $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION is compatible${NC}"
echo ""

# ============================================================================
# Step 2: Check pip
# ============================================================================
echo -e "${YELLOW}[2/9]${NC} Checking pip..."

if ! python3 -m pip --version &> /dev/null; then
    echo "pip not found. Installing pip..."
    python3 -m ensurepip --upgrade
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install pip${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓ pip is available${NC}"
echo ""

# ============================================================================
# Step 3: Set Installation Directory
# ============================================================================
INSTALL_DIR="$HOME/Applications/V-Mart-Backend-Server"

echo -e "${YELLOW}[3/9]${NC} Setting up installation directory..."
echo "Installation directory: $INSTALL_DIR"
echo ""

# ============================================================================
# Step 4: Clone or Download Repository
# ============================================================================
echo -e "${YELLOW}[4/9]${NC} Downloading V-Mart Backend Server..."

if [ -d "$INSTALL_DIR" ]; then
    echo "Directory $INSTALL_DIR already exists."
    read -p "Overwrite existing installation? (y/N): " OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    rm -rf "$INSTALL_DIR"
fi

# Try git clone first
if command -v git &> /dev/null; then
    echo "Cloning from GitHub..."
    git clone https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git "$INSTALL_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Repository cloned successfully${NC}"
    else
        echo "Git clone failed. Trying download..."
        rm -rf "$INSTALL_DIR"
        NEED_DOWNLOAD=1
    fi
else
    NEED_DOWNLOAD=1
fi

# Fallback to ZIP download
if [ ! -z "$NEED_DOWNLOAD" ]; then
    echo "Downloading ZIP archive..."
    mkdir -p "$INSTALL_DIR"
    curl -L "https://github.com/ds25041974/V-Mart-Personal-AI-Agent/archive/refs/heads/main.zip" -o "/tmp/vmart-backend.zip"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to download repository${NC}"
        exit 1
    fi
    
    unzip -q "/tmp/vmart-backend.zip" -d "/tmp/vmart-backend-extract"
    mv "/tmp/vmart-backend-extract/V-Mart-Personal-AI-Agent-main"/* "$INSTALL_DIR/"
    rm -rf "/tmp/vmart-backend-extract" "/tmp/vmart-backend.zip"
    echo -e "${GREEN}✓ Backend server downloaded${NC}"
fi

cd "$INSTALL_DIR"
echo ""

# ============================================================================
# Step 5: Create Virtual Environment
# ============================================================================
echo -e "${YELLOW}[5/9]${NC} Creating Python virtual environment..."

python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment created${NC}"
echo ""

# ============================================================================
# Step 6: Install Dependencies
# ============================================================================
echo -e "${YELLOW}[6/9]${NC} Installing Python dependencies..."
echo "This may take several minutes..."

source .venv/bin/activate

if [ -f "backend_requirements.txt" ]; then
    python -m pip install --upgrade pip
    python -m pip install -r backend_requirements.txt
else
    echo "Installing dependencies manually..."
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
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}Error installing dependencies${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
echo ""

# ============================================================================
# Step 7: Create Configuration Files
# ============================================================================
echo -e "${YELLOW}[7/9]${NC} Creating configuration files..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << 'EOFENV'
# V-Mart Backend Server Configuration

# Backend Server Settings
BACKEND_PORT=5000
BACKEND_HOST=0.0.0.0
SECRET_KEY=your-secret-key-here

# Google Gemini AI
GOOGLE_API_KEY=your-gemini-api-key-here

# Database Connections (Optional)
# ORACLE_DSN=host:port/service_name
# ORACLE_USER=username
# ORACLE_PASSWORD=password

# MSSQL_SERVER=server_name
# MSSQL_DATABASE=database_name
# MSSQL_USER=username
# MSSQL_PASSWORD=password

# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432
# POSTGRES_DB=database_name
# POSTGRES_USER=username
# POSTGRES_PASSWORD=password

# MYSQL_HOST=localhost
# MYSQL_PORT=3306
# MYSQL_DB=database_name
# MYSQL_USER=username
# MYSQL_PASSWORD=password

# CLICKHOUSE_HOST=localhost
# CLICKHOUSE_PORT=9000
# CLICKHOUSE_USER=default
# CLICKHOUSE_PASSWORD=

# Tableau Configuration
# TABLEAU_SERVER=https://tableau.example.com
# TABLEAU_SITE=site_name
# TABLEAU_USERNAME=username
# TABLEAU_PASSWORD=password

# Google Drive Configuration
# GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json
EOFENV
fi

# Create config directory and copy backend_config.yaml
mkdir -p config
if [ ! -f "config/backend_config.yaml" ]; then
    echo "Backend config file will be created by the application."
fi

echo -e "${GREEN}✓ Configuration files created${NC}"
echo ""

# ============================================================================
# Step 8: Create Management Scripts
# ============================================================================
echo -e "${YELLOW}[8/9]${NC} Creating management scripts..."

# Create start script
cat > start-backend.sh << 'EOFSTART'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
echo "Starting V-Mart Backend Server on port 5000..."
python backend_server.py
EOFSTART
chmod +x start-backend.sh

# Create stop script
cat > stop-backend.sh << 'EOFSTOP'
#!/bin/bash
echo "Stopping V-Mart Backend Server..."
pkill -f "python.*backend_server.py"
echo "Backend server stopped."
EOFSTOP
chmod +x stop-backend.sh

# Create restart script
cat > restart-backend.sh << 'EOFRESTART'
#!/bin/bash
cd "$(dirname "$0")"
./stop-backend.sh
sleep 2
./start-backend.sh
EOFRESTART
chmod +x restart-backend.sh

# Create status script
cat > status-backend.sh << 'EOFSTATUS'
#!/bin/bash
if pgrep -f "python.*backend_server.py" > /dev/null; then
    echo "V-Mart Backend Server is running"
    echo "Process ID(s):"
    pgrep -f "python.*backend_server.py"
else
    echo "V-Mart Backend Server is not running"
fi
EOFSTATUS
chmod +x status-backend.sh

echo -e "${GREEN}✓ Management scripts created${NC}"
echo ""

# ============================================================================
# Step 9: Configure Auto-Start (Optional)
# ============================================================================
echo -e "${YELLOW}[9/9]${NC} Configuring auto-start..."

read -p "Enable auto-start on macOS startup? (y/N): " AUTOSTART

if [[ "$AUTOSTART" =~ ^[Yy]$ ]]; then
    echo "Setting up LaunchAgent..."
    
    PLIST_FILE="$HOME/Library/LaunchAgents/com.vmart.backend.plist"
    
    cat > "$PLIST_FILE" << EOFPLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vmart.backend</string>
    <key>ProgramArguments</key>
    <array>
        <string>$INSTALL_DIR/start-backend.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$INSTALL_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>StandardOutPath</key>
    <string>$INSTALL_DIR/logs/backend.out.log</string>
    <key>StandardErrorPath</key>
    <string>$INSTALL_DIR/logs/backend.err.log</string>
</dict>
</plist>
EOFPLIST
    
    mkdir -p logs
    
    launchctl load "$PLIST_FILE" 2>/dev/null
    
    echo -e "${GREEN}✓ Auto-start configured${NC}"
    echo "LaunchAgent will restart the server automatically on crash."
else
    echo "Auto-start not configured. You can run ./start-backend.sh manually."
fi

echo ""

# ============================================================================
# Configuration Wizard
# ============================================================================
echo ""
echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}                 Configuration Wizard${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""

read -p "Would you like to configure the backend server now? (y/N): " RUN_WIZARD

if [[ "$RUN_WIZARD" =~ ^[Yy]$ ]]; then
    echo ""
    echo "--- Google Gemini API Key ---"
    read -p "Enter your Google Gemini API key (or press Enter to skip): " GEMINI_KEY
    if [ ! -z "$GEMINI_KEY" ]; then
        sed -i.bak "s/GOOGLE_API_KEY=.*/GOOGLE_API_KEY=$GEMINI_KEY/" .env
    fi
    
    echo ""
    echo "--- Secret Key ---"
    echo "Generating a random secret key..."
    SECRET_KEY=$(uuidgen)
    sed -i.bak "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    
    echo ""
    echo "--- Port Configuration ---"
    read -p "Backend server port [5000]: " BACKEND_PORT
    BACKEND_PORT=${BACKEND_PORT:-5000}
    sed -i.bak "s/BACKEND_PORT=.*/BACKEND_PORT=$BACKEND_PORT/" .env
    
    rm -f .env.bak
    
    echo -e "${GREEN}✓ Configuration saved${NC}"
fi

echo ""

# ============================================================================
# Installation Complete
# ============================================================================
echo ""
echo -e "${BLUE}================================================================${NC}"
echo -e "${GREEN}         Installation Complete!${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""
echo "Installation directory: $INSTALL_DIR"
echo "Backend server port: 5000 (default)"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Edit .env file to configure database connections"
echo "2. Create default admin user (see BACKEND_MANAGER.md)"
echo "3. Configure firewall to allow port 5000"
echo "4. For production, set up SSL/TLS certificates"
echo "5. Review docs/API_REFERENCE.md for API endpoints"
echo ""
echo -e "${YELLOW}To manage the backend server:${NC}"
echo "  Start:   ./start-backend.sh"
echo "  Stop:    ./stop-backend.sh"
echo "  Restart: ./restart-backend.sh"
echo "  Status:  ./status-backend.sh"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo "  See releases/v2.0-separated/backend-server/docs/ for guides"
echo ""

read -p "Would you like to start the backend server now? (y/N): " START_NOW

if [[ "$START_NOW" =~ ^[Yy]$ ]]; then
    echo "Starting backend server..."
    ./start-backend.sh &
    sleep 2
    ./status-backend.sh
fi

echo ""
echo "Thank you for installing V-Mart Backend Server!"
echo ""
