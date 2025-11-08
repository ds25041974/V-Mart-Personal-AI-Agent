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
