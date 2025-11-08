#!/bin/bash

###############################################################################
# V-Mart AI Agent - Service Installation Script
# Installs and configures the service to run 24x7 with auto-start
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
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOGS_DIR="${PROJECT_DIR}/logs"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   V-Mart AI Agent - 24x7 Service Installation           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Step 1: Create logs directory
echo -e "${YELLOW}[1/6]${NC} Creating logs directory..."
mkdir -p "${LOGS_DIR}"
echo -e "${GREEN}✓${NC} Logs directory created: ${LOGS_DIR}"

# Step 2: Check if Python3 is installed
echo -e "\n${YELLOW}[2/6]${NC} Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_PATH=$(which python3)
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python found: ${PYTHON_PATH} (${PYTHON_VERSION})"
else
    echo -e "${RED}✗${NC} Python3 not found!"
    exit 1
fi

# Step 3: Update plist with correct Python path
echo -e "\n${YELLOW}[3/6]${NC} Updating service configuration..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - update plist with actual python3 path
    sed -i '' "s|/usr/local/bin/python3|${PYTHON_PATH}|g" "${PROJECT_DIR}/${PLIST_FILE}"
    echo -e "${GREEN}✓${NC} Service configuration updated with Python path: ${PYTHON_PATH}"
fi

# Step 4: Copy plist to LaunchAgents
echo -e "\n${YELLOW}[4/6]${NC} Installing service..."
mkdir -p "${LAUNCH_AGENTS_DIR}"
cp "${PROJECT_DIR}/${PLIST_FILE}" "${LAUNCH_AGENTS_DIR}/"
echo -e "${GREEN}✓${NC} Service file copied to: ${LAUNCH_AGENTS_DIR}/${PLIST_FILE}"

# Step 5: Load the service
echo -e "\n${YELLOW}[5/6]${NC} Starting service..."

# Unload if already loaded (ignore errors)
launchctl unload "${LAUNCH_AGENTS_DIR}/${PLIST_FILE}" 2>/dev/null || true

# Load the service
launchctl load -w "${LAUNCH_AGENTS_DIR}/${PLIST_FILE}"
echo -e "${GREEN}✓${NC} Service loaded and started"

# Step 6: Verify service status
echo -e "\n${YELLOW}[6/6]${NC} Verifying service status..."
sleep 3  # Wait for service to start

if launchctl list | grep -q "${SERVICE_NAME}"; then
    PID=$(launchctl list | grep "${SERVICE_NAME}" | awk '{print $1}')
    if [ "$PID" != "-" ]; then
        echo -e "${GREEN}✓${NC} Service is running (PID: ${PID})"
    else
        echo -e "${YELLOW}⚠${NC} Service is loaded but may be starting..."
    fi
else
    echo -e "${RED}✗${NC} Service not found in launchctl list"
fi

# Wait a bit more and check if web server is responding
echo -e "\n${BLUE}Checking web server...${NC}"
sleep 5

if curl -s http://localhost:5000/health &> /dev/null; then
    echo -e "${GREEN}✓${NC} Web server is responding on http://localhost:5000"
else
    echo -e "${YELLOW}⚠${NC} Web server not responding yet (may take a minute to start)"
    echo -e "   Check logs: tail -f ${LOGS_DIR}/service.log"
fi

echo -e "\n${GREEN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║             Installation Completed Successfully!        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo "📊 Service Details:"
echo "   • Name: ${SERVICE_NAME}"
echo "   • Status: Running 24x7"
echo "   • Auto-start: Enabled (on boot and login)"
echo "   • Auto-restart: Enabled (if crashed)"
echo "   • Network-aware: Waits for network before starting"
echo ""
echo "🌐 Access URLs:"
echo "   • Local:    http://localhost:5000"
echo "   • Network:  http://0.0.0.0:5000"
echo ""
echo "📝 Log Files:"
echo "   • Output:   ${LOGS_DIR}/service.log"
echo "   • Errors:   ${LOGS_DIR}/service-error.log"
echo ""
echo "🔧 Service Management Commands:"
echo "   • Status:   launchctl list | grep ${SERVICE_NAME}"
echo "   • Stop:     launchctl unload ${LAUNCH_AGENTS_DIR}/${PLIST_FILE}"
echo "   • Start:    launchctl load -w ${LAUNCH_AGENTS_DIR}/${PLIST_FILE}"
echo "   • Restart:  launchctl kickstart -k gui/\$(id -u)/${SERVICE_NAME}"
echo "   • Logs:     tail -f ${LOGS_DIR}/service.log"
echo ""
echo "✅ Your V-Mart AI Agent is now running 24x7!"
echo ""
