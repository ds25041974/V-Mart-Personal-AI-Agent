#!/bin/bash
# ============================================================================
# V-Mart AI Agent - Chatbot Agent Installer for macOS
# Version: 2.0.0
# Description: Automated installer for chatbot agent (user-facing interface)
# ============================================================================

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="V-Mart-Chatbot-Agent"
VERSION="2.0.0"
INSTALL_DIR="$HOME/Applications/$APP_NAME"
GITHUB_REPO="https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git"
PYTHON_MIN_VERSION="3.8"

# ============================================================================
# Banner
# ============================================================================
clear
echo -e "${BLUE}===================================================================${NC}"
echo -e "${BLUE}          V-Mart AI Agent - Chatbot Agent Installer            ${NC}"
echo -e "${BLUE}                        Version 2.0.0                            ${NC}"
echo -e "${BLUE}===================================================================${NC}"
echo ""
echo -e "  ${GREEN}User-Facing Chatbot Interface${NC}"
echo -e "  ${YELLOW}Platform: macOS 10.15+${NC}"
echo ""
echo -e "${BLUE}===================================================================${NC}"
echo ""

# ============================================================================
# Check Python Installation
# ============================================================================
echo -e "${YELLOW}[1/8]${NC} Checking Python installation..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
    PYTHON_CMD="python3"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "1. Using Homebrew: brew install python@3"
    echo "2. Or download from: https://www.python.org/downloads/"
    exit 1
fi
echo ""

# ============================================================================
# Check pip
# ============================================================================
echo -e "${YELLOW}[2/8]${NC} Checking pip..."
if $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${GREEN}✓ pip is available${NC}"
else
    echo -e "${YELLOW}Installing pip...${NC}"
    $PYTHON_CMD -m ensurepip --upgrade
fi
echo ""

# ============================================================================
# Create Installation Directory
# ============================================================================
echo -e "${YELLOW}[3/8]${NC} Creating installation directory..."
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠ Directory already exists: $INSTALL_DIR${NC}"
    read -p "Do you want to overwrite? (y/n): " OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
        echo "Installation cancelled"
        exit 1
    fi
    rm -rf "$INSTALL_DIR"
fi

mkdir -p "$INSTALL_DIR"
echo -e "${GREEN}✓ Created: $INSTALL_DIR${NC}"
echo ""

# ============================================================================
# Clone Repository
# ============================================================================
echo -e "${YELLOW}[4/8]${NC} Downloading V-Mart AI Agent from GitHub..."
if command -v git &> /dev/null; then
    git clone $GITHUB_REPO "$INSTALL_DIR"
else
    echo -e "${YELLOW}⚠ Git not found. Downloading as ZIP...${NC}"
    curl -L "https://github.com/ds25041974/V-Mart-Personal-AI-Agent/archive/refs/heads/main.zip" -o /tmp/vmart-agent.zip
    unzip -q /tmp/vmart-agent.zip -d /tmp/vmart-agent
    cp -r /tmp/vmart-agent/V-Mart-Personal-AI-Agent-main/* "$INSTALL_DIR/"
    rm -rf /tmp/vmart-agent /tmp/vmart-agent.zip
fi
echo -e "${GREEN}✓ Downloaded successfully${NC}"
echo ""

# ============================================================================
# Create Virtual Environment
# ============================================================================
echo -e "${YELLOW}[5/8]${NC} Creating virtual environment..."
cd "$INSTALL_DIR" || exit 1
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to create virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment created${NC}"
echo ""

# ============================================================================
# Install Dependencies (Chatbot Only)
# ============================================================================
echo -e "${YELLOW}[6/8]${NC} Installing dependencies (Chatbot Agent)..."
source venv/bin/activate
$PYTHON_CMD -m pip install --upgrade pip

if [ -f "chatbot_requirements.txt" ]; then
    $PYTHON_CMD -m pip install -r chatbot_requirements.txt
else
    echo "Installing core dependencies..."
    $PYTHON_CMD -m pip install Flask==3.0.0 Werkzeug==3.0.1
    $PYTHON_CMD -m pip install google-api-python-client==2.108.0 google-auth-oauthlib==1.2.0
    $PYTHON_CMD -m pip install google-generativeai==0.3.1
    $PYTHON_CMD -m pip install authlib==1.3.0 requests==2.31.0
    $PYTHON_CMD -m pip install schedule==1.2.0 python-dotenv==1.0.0
    $PYTHON_CMD -m pip install pandas==2.1.4 numpy==1.26.2
    $PYTHON_CMD -m pip install openpyxl==3.1.2 python-pptx==0.6.23 PyPDF2==3.0.1
    $PYTHON_CMD -m pip install PyYAML==6.0.1
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# ============================================================================
# Configure Environment
# ============================================================================
echo -e "${YELLOW}[7/8]${NC} Configuring environment..."

# Create .env file
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# V-Mart AI Agent - Chatbot Configuration
# Version: 2.0.0

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Google OAuth 2.0
GOOGLE_CLIENT_ID=your-client-id-here
GOOGLE_CLIENT_SECRET=your-client-secret-here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# Backend Server (Optional - for database features)
BACKEND_URL=http://localhost:5000
BACKEND_API_KEY=your-backend-api-key-here

# Chatbot Settings
CHATBOT_PORT=8000
CHATBOT_HOST=0.0.0.0
SESSION_TIMEOUT=3600

# Local Files
LOCAL_FILES_BASE_PATH=$HOME/Documents
EOF
fi

# Create config directory and chatbot_config.yaml
if [ ! -f "config/chatbot_config.yaml" ]; then
    mkdir -p config
    cat > config/chatbot_config.yaml << 'EOF'
# V-Mart AI Agent - Chatbot Configuration
# Version: 2.0.0

chatbot:
  port: 8000
  host: 0.0.0.0
  debug: false
  session_timeout: 3600

backend:
  url: http://localhost:5000
  api_key: ""
  timeout: 30
  retry_attempts: 3
  cache_ttl: 300

google_oauth:
  client_id: ""
  client_secret: ""
  redirect_uri: http://localhost:8000/auth/callback

local_files:
  base_path: ~/Documents
  max_file_size: 52428800  # 50MB

logging:
  level: INFO
  file: logs/chatbot.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
EOF
fi

echo -e "${GREEN}✓ Configuration files created${NC}"
echo ""

# ============================================================================
# Create Start Scripts
# ============================================================================
echo "Creating start scripts..."

# Create start-chatbot.sh
cat > start-chatbot.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 src/web/app.py
EOF
chmod +x start-chatbot.sh

# Create stop-chatbot.sh
cat > stop-chatbot.sh << 'EOF'
#!/bin/bash
pkill -f "python3 src/web/app.py"
echo "Chatbot stopped"
EOF
chmod +x stop-chatbot.sh

# Create restart-chatbot.sh
cat > restart-chatbot.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./stop-chatbot.sh
sleep 2
./start-chatbot.sh
EOF
chmod +x restart-chatbot.sh

# Create status-chatbot.sh
cat > status-chatbot.sh << 'EOF'
#!/bin/bash
if pgrep -f "python3 src/web/app.py" > /dev/null; then
    echo "✓ Chatbot is running"
    echo "PID: $(pgrep -f 'python3 src/web/app.py')"
    echo "Access at: http://localhost:8000"
else
    echo "✗ Chatbot is not running"
fi
EOF
chmod +x status-chatbot.sh

echo -e "${GREEN}✓ Start scripts created${NC}"
echo ""

# ============================================================================
# Setup Auto-Start (LaunchAgent)
# ============================================================================
echo -e "${YELLOW}[8/8]${NC} Setting up auto-start..."
read -p "Do you want to auto-start chatbot on macOS login? (y/n): " AUTOSTART
if [[ "$AUTOSTART" =~ ^[Yy]$ ]]; then
    LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
    mkdir -p "$LAUNCH_AGENT_DIR"
    
    cat > "$LAUNCH_AGENT_DIR/com.vmart.chatbot.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vmart.chatbot</string>
    <key>ProgramArguments</key>
    <array>
        <string>$INSTALL_DIR/start-chatbot.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>StandardOutPath</key>
    <string>$INSTALL_DIR/logs/chatbot-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$INSTALL_DIR/logs/chatbot-stderr.log</string>
</dict>
</plist>
EOF
    
    launchctl load "$LAUNCH_AGENT_DIR/com.vmart.chatbot.plist" 2>/dev/null
    echo -e "${GREEN}✓ Auto-start configured${NC}"
else
    echo -e "${YELLOW}⚠ Auto-start skipped${NC}"
fi
echo ""

# ============================================================================
# Configuration Wizard
# ============================================================================
echo -e "${BLUE}===================================================================${NC}"
echo "                      CONFIGURATION WIZARD"
echo -e "${BLUE}===================================================================${NC}"
echo ""
echo "The chatbot requires configuration before first use."
echo ""
read -p "Configure now? (y/n): " CONFIGURE_NOW
if [[ "$CONFIGURE_NOW" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}Step 1: Google Gemini API Key${NC}"
    echo ""
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Enter your Gemini API key: " GEMINI_KEY
    
    echo ""
    echo -e "${YELLOW}Step 2: Google OAuth Credentials${NC}"
    echo ""
    echo "Get OAuth credentials from: https://console.cloud.google.com/apis/credentials"
    echo ""
    read -p "Enter Google Client ID: " CLIENT_ID
    read -p "Enter Google Client Secret: " CLIENT_SECRET
    
    echo ""
    echo -e "${YELLOW}Step 3: Backend Server (Optional)${NC}"
    echo ""
    echo "If you have a Backend Server running, enter its URL"
    echo "Leave blank to skip backend features"
    echo ""
    read -p "Enter Backend URL (e.g., http://192.168.1.100:5000): " BACKEND_URL
    
    if [ -n "$BACKEND_URL" ]; then
        read -p "Enter Backend API Key: " BACKEND_KEY
    fi
    
    # Update .env file
    sed -i.bak "s|GEMINI_API_KEY=.*|GEMINI_API_KEY=$GEMINI_KEY|" .env
    sed -i.bak "s|GOOGLE_CLIENT_ID=.*|GOOGLE_CLIENT_ID=$CLIENT_ID|" .env
    sed -i.bak "s|GOOGLE_CLIENT_SECRET=.*|GOOGLE_CLIENT_SECRET=$CLIENT_SECRET|" .env
    
    if [ -n "$BACKEND_URL" ]; then
        sed -i.bak "s|BACKEND_URL=.*|BACKEND_URL=$BACKEND_URL|" .env
        sed -i.bak "s|BACKEND_API_KEY=.*|BACKEND_API_KEY=$BACKEND_KEY|" .env
    fi
    
    rm .env.bak
    
    echo ""
    echo -e "${GREEN}✓ Configuration saved${NC}"
fi
echo ""

# ============================================================================
# Installation Complete
# ============================================================================
echo -e "${BLUE}===================================================================${NC}"
echo -e "${GREEN}              INSTALLATION COMPLETED SUCCESSFULLY!${NC}"
echo -e "${BLUE}===================================================================${NC}"
echo ""
echo -e "${GREEN}✓${NC} Chatbot Agent installed to: $INSTALL_DIR"
echo -e "${GREEN}✓${NC} Virtual environment configured"
echo -e "${GREEN}✓${NC} Dependencies installed"
echo -e "${GREEN}✓${NC} Management scripts created"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Complete configuration (if not done):"
echo "   nano $INSTALL_DIR/.env"
echo ""
echo "2. Start the chatbot:"
echo "   $INSTALL_DIR/start-chatbot.sh"
echo ""
echo "3. Access the chatbot:"
echo "   Open browser: http://localhost:8000"
echo ""
echo "4. Management commands:"
echo "   Start:   $INSTALL_DIR/start-chatbot.sh"
echo "   Stop:    $INSTALL_DIR/stop-chatbot.sh"
echo "   Restart: $INSTALL_DIR/restart-chatbot.sh"
echo "   Status:  $INSTALL_DIR/status-chatbot.sh"
echo ""
echo -e "${BLUE}===================================================================${NC}"
echo "              📖 DOCUMENTATION INCLUDED"
echo -e "${BLUE}===================================================================${NC}"
echo ""
echo "✓ Setup Guide               - docs/QUICK_SETUP.md"
echo "✓ User Guide                - docs/USER_GUIDE.md"
echo "✓ Service 24x7 Setup        - docs/SERVICE_24x7_SETUP.md"
echo "✓ Google OAuth Setup        - docs/GOOGLE_OAUTH_SETUP.md"
echo "✓ Chatbot Interface Guide   - docs/CHATBOT_INTERFACE_GUIDE.md"
echo "✓ Data Reading Feature      - docs/DATA_READING_FEATURE.md"
echo "✓ Deployment Guide          - docs/DEPLOYMENT_GUIDE.md"
echo "✓ Architecture Diagrams     - docs/ARCHITECTURE_DIAGRAMS.md"
echo ""
echo -e "${BLUE}===================================================================${NC}"
echo ""
read -p "Start chatbot now? (y/n): " START_NOW
if [[ "$START_NOW" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${GREEN}Starting chatbot...${NC}"
    echo -e "${GREEN}Access at: http://localhost:8000${NC}"
    ./start-chatbot.sh &
    sleep 2
else
    echo ""
    echo "Start chatbot anytime using:"
    echo "$INSTALL_DIR/start-chatbot.sh"
fi
echo ""
echo "Thank you for installing V-Mart AI Agent!"
echo ""
