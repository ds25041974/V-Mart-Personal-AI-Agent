#!/bin/bash

################################################################################
# V-Mart Personal AI Agent - Linux Installer
# Automated installation script for Ubuntu 20.04+, Debian, CentOS, Fedora
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
INSTALL_DIR="$HOME/opt/$APP_NAME"
PYTHON_MIN_VERSION="3.8"
REPO_URL="https://github.com/ds25041974/V-Mart-Personal-AI-Agent.git"
SERVICE_NAME="vmart-aiagent"
SERVICE_FILE="$HOME/.config/systemd/user/$SERVICE_NAME.service"

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    DISTRO_VERSION=$VERSION_ID
else
    DISTRO="unknown"
fi

# Functions
print_header() {
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  V-Mart Personal AI Agent Installer${NC}"
    echo -e "${CYAN}  Version: 1.0.0${NC}"
    echo -e "${CYAN}  Platform: Linux ($DISTRO)${NC}"
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
print_step "🔍 Step 1/9: Checking Python installation..."

PYTHON_CMD=""
for cmd in python3.11 python3.10 python3.9 python3.8 python3; do
    if check_command $cmd; then
        PYTHON_VERSION=$($cmd --version 2>&1 | awk '{print $2}')
        PYTHON_MAJOR_MINOR=$(echo $PYTHON_VERSION | cut -d. -f1,2)
        
        if version_ge $PYTHON_MAJOR_MINOR $PYTHON_MIN_VERSION; then
            PYTHON_CMD=$cmd
            print_info "✅ Python $PYTHON_VERSION found ($cmd)"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    print_error "❌ Python 3.8+ not found!"
    print_warning "Installing Python based on your distribution..."
    
    case $DISTRO in
        ubuntu|debian)
            print_info "For Ubuntu/Debian, run:"
            print_info "  sudo apt update"
            print_info "  sudo apt install python3.11 python3.11-venv python3-pip"
            ;;
        fedora)
            print_info "For Fedora, run:"
            print_info "  sudo dnf install python3.11 python3-pip"
            ;;
        centos|rhel)
            print_info "For CentOS/RHEL, run:"
            print_info "  sudo yum install python3.11 python3-pip"
            ;;
        *)
            print_info "Please install Python 3.11+ from your package manager"
            ;;
    esac
    
    read -p "Would you like to try automatic installation? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        case $DISTRO in
            ubuntu|debian)
                sudo apt update
                sudo apt install -y python3.11 python3.11-venv python3-pip
                PYTHON_CMD="python3.11"
                ;;
            fedora)
                sudo dnf install -y python3.11 python3-pip
                PYTHON_CMD="python3.11"
                ;;
            centos|rhel)
                sudo yum install -y python3.11 python3-pip
                PYTHON_CMD="python3.11"
                ;;
        esac
    else
        exit 1
    fi
fi

# Step 2: Check pip
print_step ""
print_step "🔍 Step 2/9: Checking pip installation..."

if $PYTHON_CMD -m pip --version &> /dev/null; then
    PIP_VERSION=$($PYTHON_CMD -m pip --version 2>&1)
    print_info "✅ pip found: $PIP_VERSION"
else
    print_warning "❌ pip not found. Installing pip..."
    case $DISTRO in
        ubuntu|debian)
            sudo apt install -y python3-pip
            ;;
        fedora)
            sudo dnf install -y python3-pip
            ;;
        centos|rhel)
            sudo yum install -y python3-pip
            ;;
        *)
            $PYTHON_CMD -m ensurepip --upgrade
            ;;
    esac
fi

# Step 3: Install system dependencies
print_step ""
print_step "📦 Step 3/9: Installing system dependencies..."

case $DISTRO in
    ubuntu|debian)
        print_info "Installing build essentials and dependencies..."
        sudo apt update
        sudo apt install -y build-essential git curl wget
        ;;
    fedora)
        print_info "Installing development tools..."
        sudo dnf install -y @development-tools git curl wget
        ;;
    centos|rhel)
        print_info "Installing development tools..."
        sudo yum groupinstall -y "Development Tools"
        sudo yum install -y git curl wget
        ;;
esac

print_info "✅ System dependencies installed"

# Step 4: Create installation directory
print_step ""
print_step "📁 Step 4/9: Creating installation directory..."

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

# Step 5: Download/Clone repository
print_step ""
print_step "📥 Step 5/9: Downloading V-Mart AI Agent..."

if check_command git; then
    print_info "Cloning repository..."
    git clone $REPO_URL "$INSTALL_DIR"
    if [ $? -ne 0 ]; then
        print_error "❌ Failed to clone repository"
        exit 1
    fi
else
    print_warning "ℹ️  Git not found. Installing git..."
    case $DISTRO in
        ubuntu|debian)
            sudo apt install -y git
            ;;
        fedora)
            sudo dnf install -y git
            ;;
        centos|rhel)
            sudo yum install -y git
            ;;
    esac
    
    git clone $REPO_URL "$INSTALL_DIR"
fi

# Step 6: Create virtual environment
print_step ""
print_step "🐍 Step 6/9: Creating Python virtual environment..."

cd "$INSTALL_DIR"
$PYTHON_CMD -m venv venv

if [ $? -ne 0 ]; then
    print_error "❌ Failed to create virtual environment"
    print_warning "Installing python3-venv..."
    
    case $DISTRO in
        ubuntu|debian)
            sudo apt install -y python3-venv
            ;;
    esac
    
    $PYTHON_CMD -m venv venv
fi

print_info "✅ Virtual environment created"

# Step 7: Install dependencies
print_step ""
print_step "📦 Step 7/9: Installing Python dependencies..."
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

# Step 8: Configure environment
print_step ""
print_step "⚙️  Step 8/9: Configuring environment..."

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

# Step 9: Create systemd user service for auto-start
print_step ""
print_step "🔄 Step 9/9: Setting up auto-start service..."

# Create systemd user directory
mkdir -p "$HOME/.config/systemd/user"

# Create systemd service file
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=V-Mart Personal AI Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/main.py
Restart=always
RestartSec=30
StandardOutput=append:$INSTALL_DIR/logs/stdout.log
StandardError=append:$INSTALL_DIR/logs/stderr.log
Environment="PATH=$INSTALL_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"

[Install]
WantedBy=default.target
EOF

print_info "✅ Created systemd service: $SERVICE_FILE"

# Create logs directory
mkdir -p "$INSTALL_DIR/logs"

# Enable lingering for user services (allows services to run without login)
if check_command loginctl; then
    loginctl enable-linger $USER 2>/dev/null || true
fi

# Reload systemd and start service
systemctl --user daemon-reload
systemctl --user enable $SERVICE_NAME
systemctl --user start $SERVICE_NAME

if [ $? -eq 0 ]; then
    print_info "✅ Auto-start service configured and started"
else
    print_warning "⚠️  Warning: Could not start service automatically"
    print_info "   You can start it manually later with:"
    print_info "   systemctl --user start $SERVICE_NAME"
fi

# Create management scripts
cat > "$INSTALL_DIR/start.sh" << EOF
#!/bin/bash
systemctl --user start $SERVICE_NAME
echo "✅ V-Mart AI Agent started"
echo "Access at: http://localhost:5000"
EOF

cat > "$INSTALL_DIR/stop.sh" << EOF
#!/bin/bash
systemctl --user stop $SERVICE_NAME
echo "✅ V-Mart AI Agent stopped"
EOF

cat > "$INSTALL_DIR/status.sh" << EOF
#!/bin/bash
systemctl --user status $SERVICE_NAME
EOF

cat > "$INSTALL_DIR/restart.sh" << EOF
#!/bin/bash
systemctl --user restart $SERVICE_NAME
echo "✅ V-Mart AI Agent restarted"
echo "Access at: http://localhost:5000"
EOF

cat > "$INSTALL_DIR/logs.sh" << EOF
#!/bin/bash
journalctl --user -u $SERVICE_NAME -f
EOF

chmod +x "$INSTALL_DIR/start.sh"
chmod +x "$INSTALL_DIR/stop.sh"
chmod +x "$INSTALL_DIR/status.sh"
chmod +x "$INSTALL_DIR/restart.sh"
chmod +x "$INSTALL_DIR/logs.sh"

print_info "✅ Created management scripts"

# Create uninstaller
cat > "$INSTALL_DIR/uninstall.sh" << EOF
#!/bin/bash
echo "Uninstalling V-Mart AI Agent..."
systemctl --user stop $SERVICE_NAME 2>/dev/null || true
systemctl --user disable $SERVICE_NAME 2>/dev/null || true
rm -f "$SERVICE_FILE"
systemctl --user daemon-reload
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
print_info "   Logs:    $INSTALL_DIR/logs.sh"
echo ""
print_info "4. Systemd Commands:"
print_info "   Start:   systemctl --user start $SERVICE_NAME"
print_info "   Stop:    systemctl --user stop $SERVICE_NAME"
print_info "   Status:  systemctl --user status $SERVICE_NAME"
print_info "   Logs:    journalctl --user -u $SERVICE_NAME -f"
echo ""
print_info "5. Custom Domain (Optional):"
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
print_info "   3. Edit .env: nano $ENV_FILE"
print_info "   4. Add: GEMINI_API_KEY=your_key_here"
print_info "   5. Restart: $INSTALL_DIR/restart.sh"
echo ""
print_info "🔧 View Logs:"
print_info "   Live: $INSTALL_DIR/logs.sh"
print_info "   Files: $INSTALL_DIR/logs/"
echo ""
print_info "Need help? Visit: https://github.com/ds25041974/V-Mart-Personal-AI-Agent"
echo ""
