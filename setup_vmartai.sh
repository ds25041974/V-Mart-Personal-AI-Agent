#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   Setting up vmartai custom domain                              ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if entry already exists
if grep -q "vmartai" /etc/hosts 2>/dev/null; then
    echo "⚠️  vmartai already exists in /etc/hosts"
    echo ""
    echo "Current entry:"
    grep vmartai /etc/hosts
else
    echo "Adding vmartai to /etc/hosts..."
    echo "127.0.0.1       vmartai" | sudo tee -a /etc/hosts > /dev/null
    echo "✅ Successfully added vmartai to /etc/hosts"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   Setup Complete!                                                ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 You can now access your V-Mart AI Agent at:"
echo "   • http://vmartai:5000"
echo "   • http://localhost:5000 (still works)"
echo ""
echo "✅ Both URLs point to the same application"
echo ""
echo "🧪 Test it:"
echo "   curl http://vmartai:5000/health"
echo ""

