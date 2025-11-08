#!/bin/bash
# V-Mart Backend Server - Deployment Script
# Run this on your central server (LAN or WAN accessible)

set -e

echo "=============================================="
echo "🚀 V-Mart Backend Server Deployment"
echo "=============================================="

# Configuration
BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}"
BACKEND_PORT="${BACKEND_PORT:-5000}"
BACKEND_SSL="${BACKEND_SSL:-false}"
BACKEND_WORKERS="${BACKEND_WORKERS:-4}"

# Check if running on central server
echo ""
echo "📍 Deployment Target: Central Backend Server"
echo "   Host: $BACKEND_HOST"
echo "   Port: $BACKEND_PORT"
echo "   SSL:  $BACKEND_SSL"
echo ""

# Install dependencies
echo "📦 Installing backend dependencies..."
pip install -r backend_requirements.txt

# Create directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p ~/.vmart

# Set permissions
chmod 700 ~/.vmart

# Check for GEMINI_API_KEY
if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo "⚠️  WARNING: GEMINI_API_KEY not set"
    echo "   AI insights will not be available"
    echo "   Set it with: export GEMINI_API_KEY='your-key-here'"
    echo ""
fi

# Generate default API key if needed
if [ ! -f ~/.vmart/api_keys.json ]; then
    echo "🔑 Generating default API key..."
    python3 backend_server.py generate-key --name "Default Admin" --permissions "all"
fi

# Production deployment options
echo ""
echo "=============================================="
echo "📋 Deployment Options"
echo "=============================================="
echo ""
echo "Option 1: Development Mode (Flask built-in server)"
echo "  python3 backend_server.py --host $BACKEND_HOST --port $BACKEND_PORT"
echo ""
echo "Option 2: Production Mode (Gunicorn)"
echo "  gunicorn -w $BACKEND_WORKERS -b $BACKEND_HOST:$BACKEND_PORT backend_server:app"
echo ""
echo "Option 3: Production with SSL"
echo "  gunicorn -w $BACKEND_WORKERS -b $BACKEND_HOST:$BACKEND_PORT \\"
echo "    --certfile=/path/to/cert.pem --keyfile=/path/to/key.pem \\"
echo "    backend_server:app"
echo ""
echo "Option 4: Systemd Service"
echo "  sudo cp backend.service /etc/systemd/system/"
echo "  sudo systemctl enable backend"
echo "  sudo systemctl start backend"
echo ""

# Ask user which option
echo "=============================================="
echo ""
read -p "Start server now? (1=Dev, 2=Prod, 3=Prod+SSL, N=No) [1]: " choice
choice=${choice:-1}

case $choice in
    1)
        echo ""
        echo "🚀 Starting backend server in development mode..."
        python3 backend_server.py --host "$BACKEND_HOST" --port "$BACKEND_PORT"
        ;;
    2)
        echo ""
        echo "🚀 Starting backend server in production mode..."
        gunicorn -w "$BACKEND_WORKERS" -b "$BACKEND_HOST:$BACKEND_PORT" backend_server:app
        ;;
    3)
        echo ""
        read -p "SSL Certificate path: " cert_path
        read -p "SSL Key path: " key_path
        echo "🚀 Starting backend server with SSL..."
        gunicorn -w "$BACKEND_WORKERS" -b "$BACKEND_HOST:$BACKEND_PORT" \
            --certfile="$cert_path" --keyfile="$key_path" \
            backend_server:app
        ;;
    *)
        echo ""
        echo "✅ Backend setup complete"
        echo ""
        echo "🔑 Default API Key: admin_key_default"
        echo "   (Generate secure keys with: python3 backend_server.py generate-key)"
        echo ""
        echo "📡 To start server later, run:"
        echo "   python3 backend_server.py"
        echo ""
        echo "📚 See docs/ARCHITECTURE_SEPARATION.md for more details"
        ;;
esac
