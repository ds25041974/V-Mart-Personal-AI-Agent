#!/bin/bash

###############################################################################
# V-Mart AI Agent - Service Status Checker
# Shows current status and provides management commands
###############################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="com.vmart.aiagent"
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOGS_DIR="${PROJECT_DIR}/logs"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║        V-Mart AI Agent - Service Status                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if service is loaded
echo -e "${YELLOW}Service Status:${NC}"
if launchctl list | grep -q "${SERVICE_NAME}"; then
    SERVICE_INFO=$(launchctl list | grep "${SERVICE_NAME}")
    PID=$(echo "$SERVICE_INFO" | awk '{print $1}')
    STATUS=$(echo "$SERVICE_INFO" | awk '{print $2}')
    
    if [ "$PID" != "-" ]; then
        echo -e "   ${GREEN}✓ RUNNING${NC} (PID: ${PID})"
    else
        echo -e "   ${RED}✗ LOADED BUT NOT RUNNING${NC}"
        if [ "$STATUS" != "0" ]; then
            echo -e "   ${RED}  Last Exit Code: ${STATUS}${NC}"
        fi
    fi
else
    echo -e "   ${RED}✗ NOT LOADED${NC}"
    echo -e "   ${YELLOW}  Run ./install_service.sh to install${NC}"
fi

# Check web server
echo -e "\n${YELLOW}Web Server:${NC}"
if curl -s http://localhost:5000/health &> /dev/null; then
    RESPONSE=$(curl -s http://localhost:5000/health)
    echo -e "   ${GREEN}✓ RESPONDING${NC}"
    echo -e "   ${BLUE}  URL: http://localhost:5000${NC}"
else
    echo -e "   ${RED}✗ NOT RESPONDING${NC}"
    echo -e "   ${YELLOW}  Check logs for details${NC}"
fi

# Check port
echo -e "\n${YELLOW}Port Status:${NC}"
if lsof -i :5000 &> /dev/null; then
    PORT_INFO=$(lsof -i :5000 | grep LISTEN | head -1)
    echo -e "   ${GREEN}✓ Port 5000 is in use${NC}"
    echo -e "   ${BLUE}  ${PORT_INFO}${NC}"
else
    echo -e "   ${YELLOW}⚠ Port 5000 is free${NC}"
fi

# Check logs
echo -e "\n${YELLOW}Recent Logs:${NC}"
if [ -f "${LOGS_DIR}/service.log" ]; then
    echo -e "   ${BLUE}Last 5 lines from service.log:${NC}"
    tail -5 "${LOGS_DIR}/service.log" | sed 's/^/   /'
else
    echo -e "   ${YELLOW}⚠ No logs found${NC}"
fi

if [ -f "${LOGS_DIR}/service-error.log" ] && [ -s "${LOGS_DIR}/service-error.log" ]; then
    echo -e "\n   ${RED}Recent errors:${NC}"
    tail -5 "${LOGS_DIR}/service-error.log" | sed 's/^/   /'
fi

# Display management commands
echo -e "\n${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              Service Management Commands                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo "🔧 Control Commands:"
echo "   • Check status:    ./check_service.sh"
echo "   • Restart:         launchctl kickstart -k gui/\$(id -u)/${SERVICE_NAME}"
echo "   • Stop:            launchctl unload ~/Library/LaunchAgents/${SERVICE_NAME}.plist"
echo "   • Start:           launchctl load -w ~/Library/LaunchAgents/${SERVICE_NAME}.plist"
echo "   • Uninstall:       ./uninstall_service.sh"
echo ""
echo "📝 Log Commands:"
echo "   • View logs:       tail -f ${LOGS_DIR}/service.log"
echo "   • View errors:     tail -f ${LOGS_DIR}/service-error.log"
echo "   • Clear logs:      > ${LOGS_DIR}/service.log"
echo ""
echo "🌐 Access URLs:"
echo "   • Local:           http://localhost:5000"
echo "   • Health check:    http://localhost:5000/health"
echo ""
