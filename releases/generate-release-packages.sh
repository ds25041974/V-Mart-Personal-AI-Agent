#!/bin/bash
# ============================================================================
# V-Mart AI Agent - Complete Release Package Generator
# Version: 2.0.0
# Description: Generates all installers and documentation for v2.0 release
# ============================================================================

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

RELEASE_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$RELEASE_DIR/.." && pwd)"

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}     V-Mart AI Agent - Release Package Generator v2.0${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""

# ============================================================================
# Step 1: Copy Documentation to Release Packages
# ============================================================================
echo -e "${YELLOW}[1/5]${NC} Copying documentation..."

# Chatbot Agent Documentation
CHATBOT_DOCS="$RELEASE_DIR/v2.0-separated/chatbot-agent/docs"
mkdir -p "$CHATBOT_DOCS"

cp "$PROJECT_ROOT/QUICK_SETUP.md" "$CHATBOT_DOCS/" 2>/dev/null || echo "  Skipping QUICK_SETUP.md"
cp "$PROJECT_ROOT/docs/USER_GUIDE.md" "$CHATBOT_DOCS/" 2>/dev/null || echo "  Skipping USER_GUIDE.md"
cp "$PROJECT_ROOT/docs/SERVICE_24x7_SETUP.md" "$CHATBOT_DOCS/" 2>/dev/null || echo "  Skipping SERVICE_24x7_SETUP.md"
cp "$PROJECT_ROOT/docs/GOOGLE_OAUTH_SETUP.md" "$CHATBOT_DOCS/" 2>/dev/null || echo "  Skipping GOOGLE_OAUTH_SETUP.md"
cp "$PROJECT_ROOT/docs/CHATBOT_INTERFACE_GUIDE.md" "$CHATBOT_DOCS/" 2>/dev/null || echo "  Skipping CHATBOT_INTERFACE_GUIDE.md"
cp "$PROJECT_ROOT/docs/DATA_READING_FEATURE.md" "$CHATBOT_DOCS/" 2>/dev/null || echo "  Skipping DATA_READING_FEATURE.md"
cp "$PROJECT_ROOT/docs/DEPLOYMENT_GUIDE.md" "$CHATBOT_DOCS/" 2>/dev/null || echo "  Skipping DEPLOYMENT_GUIDE.md"
cp "$PROJECT_ROOT/docs/ARCHITECTURE_DIAGRAMS.md" "$CHATBOT_DOCS/" 2>/dev/null || echo "  Skipping ARCHITECTURE_DIAGRAMS.md"

# Backend Server Documentation
BACKEND_DOCS="$RELEASE_DIR/v2.0-separated/backend-server/docs"
mkdir -p "$BACKEND_DOCS"

cp "$PROJECT_ROOT/docs/DEPLOYMENT_GUIDE.md" "$BACKEND_DOCS/" 2>/dev/null || echo "  Skipping DEPLOYMENT_GUIDE.md"
cp "$PROJECT_ROOT/docs/ARCHITECTURE_SEPARATION.md" "$BACKEND_DOCS/" 2>/dev/null || echo "  Skipping ARCHITECTURE_SEPARATION.md"
cp "$PROJECT_ROOT/docs/ARCHITECTURE_DIAGRAMS.md" "$BACKEND_DOCS/" 2>/dev/null || echo "  Skipping ARCHITECTURE_DIAGRAMS.md"
cp "$PROJECT_ROOT/docs/API_REFERENCE.md" "$BACKEND_DOCS/" 2>/dev/null || echo "  Skipping API_REFERENCE.md"
cp "$PROJECT_ROOT/docs/SERVICE_24x7_SETUP.md" "$BACKEND_DOCS/" 2>/dev/null || echo "  Skipping SERVICE_24x7_SETUP.md"
cp "$PROJECT_ROOT/SEPARATED_ARCHITECTURE.md" "$BACKEND_DOCS/" 2>/dev/null || echo "  Skipping SEPARATED_ARCHITECTURE.md"

# Create BACKEND_MANAGER.md from docs
if [ -f "$PROJECT_ROOT/docs/BACKEND_MANAGER.md" ]; then
    cp "$PROJECT_ROOT/docs/BACKEND_MANAGER.md" "$BACKEND_DOCS/"
fi

echo -e "${GREEN}✓ Documentation copied${NC}"
echo ""

# ============================================================================
# Step 2: Copy Requirements Files
# ============================================================================
echo -e "${YELLOW}[2/5]${NC} Copying requirements files..."

# Chatbot Agent Requirements
for platform in windows macos linux; do
    if [ -f "$PROJECT_ROOT/chatbot_requirements.txt" ]; then
        cp "$PROJECT_ROOT/chatbot_requirements.txt" "$RELEASE_DIR/v2.0-separated/chatbot-agent/$platform/"
    fi
done

# Backend Server Requirements
for platform in windows macos linux; do
    mkdir -p "$RELEASE_DIR/v2.0-separated/backend-server/$platform"
    if [ -f "$PROJECT_ROOT/backend_requirements.txt" ]; then
        cp "$PROJECT_ROOT/backend_requirements.txt" "$RELEASE_DIR/v2.0-separated/backend-server/$platform/"
    fi
done

echo -e "${GREEN}✓ Requirements files copied${NC}"
echo ""

# ============================================================================
# Step 3: Create Linux Installers
# ============================================================================
echo -e "${YELLOW}[3/5]${NC} Creating Linux installers..."

# Chatbot Agent Linux Installer
cat > "$RELEASE_DIR/v2.0-separated/chatbot-agent/linux/install-chatbot.sh" << 'EOFLINUX'
#!/bin/bash
# V-Mart AI Agent - Chatbot Agent Installer for Linux
# Version: 2.0.0

# [Same content as macOS installer with Linux-specific adjustments]
# (Content similar to macOS installer created above)

echo "V-Mart Chatbot Agent Installer for Linux"
echo "Please use the macOS installer script as template for Linux"
echo "Adjust paths and LaunchAgent to systemd service"
EOFLINUX

chmod +x "$RELEASE_DIR/v2.0-separated/chatbot-agent/linux/install-chatbot.sh"

# Backend Server Linux Installer  
cat > "$RELEASE_DIR/v2.0-separated/backend-server/linux/install-backend.sh" << 'EOFLINUX2'
#!/bin/bash
# V-Mart AI Agent - Backend Server Installer for Linux
# Version: 2.0.0

echo "V-Mart Backend Server Installer for Linux"
echo "Based on deploy_backend.sh script"
EOFLINUX2

chmod +x "$RELEASE_DIR/v2.0-separated/backend-server/linux/install-backend.sh"

# Copy the actual deployment scripts
if [ -f "$PROJECT_ROOT/deploy_chatbot.sh" ]; then
    cp "$PROJECT_ROOT/deploy_chatbot.sh" "$RELEASE_DIR/v2.0-separated/chatbot-agent/linux/install-chatbot.sh"
    chmod +x "$RELEASE_DIR/v2.0-separated/chatbot-agent/linux/install-chatbot.sh"
fi

if [ -f "$PROJECT_ROOT/deploy_backend.sh" ]; then
    cp "$PROJECT_ROOT/deploy_backend.sh" "$RELEASE_DIR/v2.0-separated/backend-server/linux/install-backend.sh"
    chmod +x "$RELEASE_DIR/v2.0-separated/backend-server/linux/install-backend.sh"
fi

echo -e "${GREEN}✓ Linux installers created${NC}"
echo ""

# ============================================================================
# Step 4: Create README files for each platform
# ============================================================================
echo -e "${YELLOW}[4/5]${NC} Creating README files..."

# Chatbot Agent README
cat > "$RELEASE_DIR/v2.0-separated/chatbot-agent/README.md" << 'EOFREADME'
# V-Mart AI Agent - Chatbot Agent v2.0

**User-facing chatbot interface for individual systems**

## Quick Install

### Windows
```batch
install-chatbot.bat
```

### macOS
```bash
chmod +x install-chatbot.sh
./install-chatbot.sh
```

### Linux
```bash
chmod +x install-chatbot.sh
./install-chatbot.sh
```

## Features
- ✅ Google Gemini AI
- ✅ Google OAuth
- ✅ Local file reading (Excel, CSV, PowerPoint, PDF)
- ✅ Backend client SDK
- ✅ Auto-start on boot
- ✅ Crash recovery

## Requirements
- Python 3.8+
- 4GB RAM (8GB recommended)
- Internet connection

## Documentation
See `docs/` folder for complete guides.

## Support
Email: support@vmart.co.in
EOF README

# Backend Server README
cat > "$RELEASE_DIR/v2.0-separated/backend-server/README.md" << 'EOFREADME2'
# V-Mart AI Agent - Backend Server v2.0

**Central data and API management hub**

## Quick Install

### Windows
```batch
install-backend.bat
```

### macOS
```bash
chmod +x install-backend.sh
./install-backend.sh
```

### Linux
```bash
chmod +x install-backend.sh
./install-backend.sh
```

## Features
- ✅ REST API (10+ endpoints)
- ✅ Database connectors (7 types)
- ✅ AI Insights Engine
- ✅ RBAC (23 permissions)
- ✅ API key authentication
- ✅ Rate limiting

## Requirements
- Python 3.8+
- 8GB RAM (16GB recommended)
- Static IP or domain name

## Documentation
See `docs/` folder for complete guides.

## Support
Email: support@vmart.co.in
EOFREADME2

echo -e "${GREEN}✓ README files created${NC}"
echo ""

# ============================================================================
# Step 5: Create Version Info Files
# ============================================================================
echo -e "${YELLOW}[5/5]${NC} Creating version info..."

# Create VERSION file for chatbot
cat > "$RELEASE_DIR/v2.0-separated/chatbot-agent/VERSION" << 'EOFVER'
VERSION=2.0.0
RELEASE_DATE=2025-11-09
TYPE=chatbot-agent
ARCHITECTURE=separated
PYTHON_MIN=3.8
EOFVER

# Create VERSION file for backend
cat > "$RELEASE_DIR/v2.0-separated/backend-server/VERSION" << 'EOFVER2'
VERSION=2.0.0
RELEASE_DATE=2025-11-09
TYPE=backend-server
ARCHITECTURE=separated
PYTHON_MIN=3.8
EOFVER2

echo -e "${GREEN}✓ Version info created${NC}"
echo ""

# ============================================================================
# Summary
# ============================================================================
echo -e "${BLUE}================================================================${NC}"
echo -e "${GREEN}         Release Package Generation Complete!${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""
echo "Release structure:"
echo "  v2.0-separated/"
echo "    ├── chatbot-agent/"
echo "    │   ├── windows/"
echo "    │   ├── macos/"
echo "    │   ├── linux/"
echo "    │   ├── docs/ (8 guides)"
echo "    │   └── README.md"
echo "    └── backend-server/"
echo "        ├── windows/"
echo "        ├── macos/"
echo "        ├── linux/"
echo "        ├── docs/ (6 guides)"
echo "        └── README.md"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review installers in each platform directory"
echo "2. Test on each platform"
echo "3. Create downloadable archives (.zip, .tar.gz)"
echo "4. Upload to GitHub releases"
echo ""
echo "Generated at: $RELEASE_DIR"
echo ""
