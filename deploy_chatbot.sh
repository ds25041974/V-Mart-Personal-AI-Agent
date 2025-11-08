#!/bin/bash
# V-Mart Chatbot Agent - Deployment Script
# Run this on each user's individual system

set -e

echo "=============================================="
echo "🤖 V-Mart Chatbot Agent Deployment"
echo "=============================================="

# Configuration
CHATBOT_PORT="${CHATBOT_PORT:-8000}"
BACKEND_URL="${BACKEND_URL}"
BACKEND_API_KEY="${BACKEND_API_KEY}"

# Check if running on user system
echo ""
echo "📍 Deployment Target: User System (Individual)"
echo "   Port: $CHATBOT_PORT"
echo ""

# Install dependencies
echo "📦 Installing chatbot dependencies..."
pip install -r chatbot_requirements.txt

# Create directories
echo "📁 Creating directories..."
mkdir -p logs

# Configure backend connection
echo ""
echo "=============================================="
echo "⚙️  Backend Configuration"
echo "=============================================="

if [ -z "$BACKEND_URL" ]; then
    echo ""
    echo "Backend server URL not configured."
    echo ""
    echo "Examples:"
    echo "  LAN:  http://192.168.1.100:5000"
    echo "  WAN:  https://backend.vmart.co.in:5000"
    echo "  Local: http://localhost:5000 (if running backend locally)"
    echo ""
    read -p "Enter backend server URL: " BACKEND_URL
    
    # Save to .env
    if ! grep -q "BACKEND_URL" .env 2>/dev/null; then
        echo "BACKEND_URL=$BACKEND_URL" >> .env
    fi
fi

if [ -z "$BACKEND_API_KEY" ]; then
    echo ""
    read -p "Enter backend API key: " BACKEND_API_KEY
    
    # Save to .env
    if ! grep -q "BACKEND_API_KEY" .env 2>/dev/null; then
        echo "BACKEND_API_KEY=$BACKEND_API_KEY" >> .env
    fi
fi

# Test backend connection
echo ""
echo "🔍 Testing backend connection..."
if python3 -c "from src.backend_client import BackendClient; client = BackendClient('$BACKEND_URL', '$BACKEND_API_KEY'); exit(0 if client.health_check() else 1)"; then
    echo "✅ Backend connection successful"
else
    echo "⚠️  WARNING: Cannot connect to backend"
    echo "   The chatbot will run in local mode only"
    echo "   Some features may be limited"
fi

# Check for API keys
echo ""
echo "=============================================="
echo "🔑 API Key Configuration"
echo "=============================================="

if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo "⚠️  GEMINI_API_KEY not set"
    echo "   Get your key from: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Enter Gemini API key (or press Enter to skip): " GEMINI_KEY
    if [ -n "$GEMINI_KEY" ]; then
        if ! grep -q "GEMINI_API_KEY" .env 2>/dev/null; then
            echo "GEMINI_API_KEY=$GEMINI_KEY" >> .env
        fi
    fi
fi

if [ -z "$GOOGLE_CLIENT_ID" ]; then
    echo ""
    echo "⚠️  GOOGLE_CLIENT_ID not set"
    echo "   OAuth login will not be available"
    echo "   Get credentials from: https://console.cloud.google.com"
    echo ""
fi

# Start chatbot
echo ""
echo "=============================================="
echo "🚀 Starting Chatbot Agent"
echo "=============================================="
echo ""
echo "Backend: $BACKEND_URL"
echo "Port:    $CHATBOT_PORT"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Source .env if exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start Flask app
python3 src/web/app.py
