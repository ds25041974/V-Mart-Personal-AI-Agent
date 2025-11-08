#!/bin/bash

###############################################################################
# V-Mart AI Agent - Service Uninstallation Script
# Stops and removes the 24x7 service
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="com.vmart.aiagent"
PLIST_FILE="${SERVICE_NAME}.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   V-Mart AI Agent - Service Uninstallation              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Step 1: Stop the service
echo -e "${YELLOW}[1/2]${NC} Stopping service..."
if launchctl list | grep -q "${SERVICE_NAME}"; then
    launchctl unload "${LAUNCH_AGENTS_DIR}/${PLIST_FILE}"
    echo -e "${GREEN}✓${NC} Service stopped"
else
    echo -e "${YELLOW}⚠${NC} Service was not running"
fi

# Step 2: Remove the plist file
echo -e "\n${YELLOW}[2/2]${NC} Removing service file..."
if [ -f "${LAUNCH_AGENTS_DIR}/${PLIST_FILE}" ]; then
    rm "${LAUNCH_AGENTS_DIR}/${PLIST_FILE}"
    echo -e "${GREEN}✓${NC} Service file removed"
else
    echo -e "${YELLOW}⚠${NC} Service file not found"
fi

echo -e "\n${GREEN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║          Service Uninstalled Successfully!              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo "📊 The V-Mart AI Agent service has been removed."
echo "   • Auto-start: Disabled"
echo "   • Service: Stopped"
echo ""
echo "💡 To run manually: python3 main.py"
echo "💡 To reinstall: ./install_service.sh"
echo ""
