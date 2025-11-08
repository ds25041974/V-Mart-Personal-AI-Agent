#!/bin/bash

################################################################################
# V-Mart Personal AI Agent - macOS Installer
# Automated installation script for macOS 10.15+
# Version: 1.0.0
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="V-Mart-AI-Agent"
INSTALL_DIR="$HOME/Applications/$APP_NAME"
PYTHON_MIN_VERSION="3.8"
REPO_URL="https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git"
SERVICE_NAME="com.vmart.aiagent"
PLIST_PATH="$HOME/Library/LaunchAgents/$SERVICE_NAME.plist"

# Functions
print_header() {
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  V-Mart Personal AI Agent Installer${NC}"
    echo -e "${CYAN}  Version: 1.0.0${NC}"
    echo -e "${CYAN}  Platform: macOS${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}$1${NC}"
}

print_info() {
    echo -e "${CYAN}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

version_ge() {
    test "$(printf '%s\n' "$@" | sort -V | head -n 1)" == "$2"
}

# Main installation process
print_header

# Step 1: Check Python installation
print_step "🔍 Step 1/8: Checking Python installation..."

if check_command python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR_MINOR=$(echo $PYTHON_VERSION | cut -d. -f1,2)
    
    if version_ge $PYTHON_MAJOR_MINOR $PYTHON_MIN_VERSION; then
        print_info "✅ Python $PYTHON_VERSION found"
        PYTHON_CMD="python3"
    else
        print_error "❌ Python version $PYTHON_VERSION is too old. Minimum required: $PYTHON_MIN_VERSION"
        print_warning "Please install Python 3.11+ from https://www.python.org/downloads/"
        print_warning "Or use Homebrew: brew install python@3.11"
        exit 1
    fi
else
    print_error "❌ Python3 not found!"
    print_warning "Please install Python 3.11+ using one of these methods:"
    print_info "  1. Official installer: https://www.python.org/downloads/"
    print_info "  2. Homebrew: brew install python@3.11"
    print_info "  3. Anaconda: https://www.anaconda.com/download"
    exit 1
fi

# Step 2: Check pip
print_step ""
print_step "🔍 Step 2/8: Checking pip installation..."

if $PYTHON_CMD -m pip --version &> /dev/null; then
    PIP_VERSION=$($PYTHON_CMD -m pip --version 2>&1)
    print_info "✅ pip found: $PIP_VERSION"
else
    print_warning "❌ pip not found. Installing pip..."
    $PYTHON_CMD -m ensurepip --upgrade
fi

# Step 3: Create installation directory
print_step ""
print_step "📁 Step 3/8: Creating installation directory..."

if [ -d "$INSTALL_DIR" ]; then
    print_warning "⚠️  Installation directory already exists: $INSTALL_DIR"
    read -p "Do you want to reinstall? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Installation cancelled."
        exit 0
    fi
    print_warning "Removing existing installation..."
    rm -rf "$INSTALL_DIR"
fi

mkdir -p "$INSTALL_DIR"
print_info "✅ Created: $INSTALL_DIR"

# Step 4: Download/Clone repository
print_step ""
print_step "📥 Step 4/8: Downloading V-Mart AI Agent..."

if check_command git; then
    print_info "Cloning repository..."
    git clone $REPO_URL "$INSTALL_DIR"
    if [ $? -ne 0 ]; then
        print_error "❌ Failed to clone repository"
        exit 1
    fi
else
    print_warning "ℹ️  Git not found. Downloading ZIP..."
    ZIP_URL="https://github.com/ds25041974/V-Mart-Personal-AI-Agent/archive/refs/heads/main.zip"
    ZIP_FILE="/tmp/vmart-ai-agent.zip"
    
    if check_command curl; then
        curl -L -o "$ZIP_FILE" "$ZIP_URL"
    elif check_command wget; then
        wget -O "$ZIP_FILE" "$ZIP_URL"
    else
        print_error "❌ Neither curl nor wget found. Cannot download repository."
        print_warning "Please install git: brew install git"
        exit 1
    fi
    
    # Extract ZIP
    unzip -q "$ZIP_FILE" -d "/tmp/vmart-extract"
    mv /tmp/vmart-extract/V-Mart-Personal-AI-Agent-main/* "$INSTALL_DIR/"
    
    # Cleanup
    rm -rf "$ZIP_FILE" "/tmp/vmart-extract"
    
    print_info "✅ Downloaded and extracted successfully"
fi

# Step 5: Create virtual environment
print_step ""
print_step "🐍 Step 5/8: Creating Python virtual environment..."

cd "$INSTALL_DIR"
$PYTHON_CMD -m venv venv

if [ $? -ne 0 ]; then
    print_error "❌ Failed to create virtual environment"
    exit 1
fi

print_info "✅ Virtual environment created"

# Step 6: Install dependencies
print_step ""
print_step "📦 Step 6/8: Installing Python dependencies..."
print_warning "This may take a few minutes..."

source "$INSTALL_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r "$INSTALL_DIR/requirements.txt"

if [ $? -ne 0 ]; then
    print_error "❌ Failed to install dependencies"
    exit 1
fi

print_info "✅ All dependencies installed"
deactivate

# Step 7: Configure environment
print_step ""
print_step "⚙️  Step 7/8: Configuring environment..."

ENV_FILE="$INSTALL_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    cat > "$ENV_FILE" << 'EOF'
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
EOF
    
    print_info "✅ Created .env file: $ENV_FILE"
    echo ""
    print_warning "⚠️  IMPORTANT: You must configure your API keys!"
    print_warning "Edit the file: $ENV_FILE"
    echo ""
    print_info "Required:"
    print_info "  1. GEMINI_API_KEY - Get from https://aistudio.google.com/app/apikey"
    echo ""
    print_info "Optional (for full features):"
    print_info "  2. Google OAuth credentials (for Gmail/Drive)"
    print_info "  3. GitHub token (for repository integration)"
    echo ""
else
    print_info "✅ .env file already exists"
fi

# Step 8: Create LaunchAgent for auto-start
print_step ""
print_step "🔄 Step 8/8: Setting up auto-start service..."

# Create LaunchAgent plist
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$SERVICE_NAME</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$INSTALL_DIR/venv/bin/python</string>
        <string>$INSTALL_DIR/main.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$INSTALL_DIR</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
        <key>NetworkState</key>
        <true/>
    </dict>
    
    <key>ThrottleInterval</key>
    <integer>30</integer>
    
    <key>StandardOutPath</key>
    <string>$INSTALL_DIR/logs/stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>$INSTALL_DIR/logs/stderr.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>$INSTALL_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF

print_info "✅ Created LaunchAgent: $PLIST_PATH"

# Create logs directory
mkdir -p "$INSTALL_DIR/logs"

# Load the LaunchAgent
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"

if [ $? -eq 0 ]; then
    print_info "✅ Auto-start service configured and started"
else
    print_warning "⚠️  Warning: Could not start service automatically"
    print_info "   You can start it manually later with:"
    print_info "   launchctl load $PLIST_PATH"
fi

# Create start/stop/status scripts
cat > "$INSTALL_DIR/start.sh" << 'EOF'
#!/bin/bash
launchctl load "$HOME/Library/LaunchAgents/com.vmart.aiagent.plist"
echo "✅ V-Mart AI Agent started"
echo "Access at: http://localhost:5000"
EOF

cat > "$INSTALL_DIR/stop.sh" << 'EOF'
#!/bin/bash
launchctl unload "$HOME/Library/LaunchAgents/com.vmart.aiagent.plist"
echo "✅ V-Mart AI Agent stopped"
EOF

cat > "$INSTALL_DIR/status.sh" << 'EOF'
#!/bin/bash
launchctl list | grep com.vmart.aiagent
if [ $? -eq 0 ]; then
    echo "✅ V-Mart AI Agent is running"
    echo "Access at: http://localhost:5000"
else
    echo "❌ V-Mart AI Agent is not running"
fi
EOF

cat > "$INSTALL_DIR/restart.sh" << 'EOF'
#!/bin/bash
launchctl unload "$HOME/Library/LaunchAgents/com.vmart.aiagent.plist" 2>/dev/null
sleep 2
launchctl load "$HOME/Library/LaunchAgents/com.vmart.aiagent.plist"
echo "✅ V-Mart AI Agent restarted"
echo "Access at: http://localhost:5000"
EOF

chmod +x "$INSTALL_DIR/start.sh"
chmod +x "$INSTALL_DIR/stop.sh"
chmod +x "$INSTALL_DIR/status.sh"
chmod +x "$INSTALL_DIR/restart.sh"

print_info "✅ Created management scripts"

# Create uninstaller
cat > "$INSTALL_DIR/uninstall.sh" << EOF
#!/bin/bash
echo "Uninstalling V-Mart AI Agent..."
launchctl unload "$PLIST_PATH" 2>/dev/null || true
rm -f "$PLIST_PATH"
read -p "Remove installation directory $INSTALL_DIR? (y/n): " -n 1 -r
echo
if [[ \$REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$INSTALL_DIR"
    echo "✅ V-Mart AI Agent completely uninstalled"
else
    echo "✅ Service uninstalled. Installation files kept."
fi
EOF

chmod +x "$INSTALL_DIR/uninstall.sh"

# Installation complete
echo ""
print_header
print_step "  ✅ Installation Complete!"
print_header
echo ""
print_info "📍 Installation Location: $INSTALL_DIR"
echo ""
print_warning "🚀 Next Steps:"
echo ""
print_info "1. Configure API Keys:"
print_info "   Edit: $ENV_FILE"
print_info "   Add your GEMINI_API_KEY (required)"
echo ""
print_info "2. Service Status:"
print_info "   The service is now running automatically"
print_info "   Access at: http://localhost:5000"
echo ""
print_info "3. Management Commands:"
print_info "   Start:   $INSTALL_DIR/start.sh"
print_info "   Stop:    $INSTALL_DIR/stop.sh"
print_info "   Restart: $INSTALL_DIR/restart.sh"
print_info "   Status:  $INSTALL_DIR/status.sh"
echo ""
print_info "4. Custom Domain (Optional):"
print_info "   Setup: sudo sh -c 'echo \"127.0.0.1 vmartai\" >> /etc/hosts'"
print_info "   Access: http://vmartai:5000"
echo ""
print_warning "📚 Documentation:"
print_info "   User Guide: $INSTALL_DIR/docs/USER_GUIDE.md"
print_info "   Setup Guide: $INSTALL_DIR/docs/SETUP_GUIDE.md"
print_info "   API Reference: $INSTALL_DIR/docs/API_REFERENCE.md"
echo ""
print_warning "💡 Quick Setup for Gemini API Key:"
print_info "   1. Visit: https://aistudio.google.com/app/apikey"
print_info "   2. Create API key"
print_info "   3. Add to .env file: GEMINI_API_KEY=your_key_here"
print_info "   4. Restart: $INSTALL_DIR/restart.sh"
echo ""
print_info "🔧 View Logs:"
print_info "   Stdout: $INSTALL_DIR/logs/stdout.log"
print_info "   Stderr: $INSTALL_DIR/logs/stderr.log"
echo ""
print_info "Need help? Visit: https://github.com/ds25041974/V-Mart-Personal-AI-Agent"
echo ""
