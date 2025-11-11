#!/bin/bash
# Quick login test script

echo "🔐 Logging in to V-Mart AI Agent..."

# Login with email
curl -s -c cookies.txt -X POST http://localhost:8000/email-login \
  -d "email=test@vmart.co.in" \
  -d "name=Test User" \
  > /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Login successful!"
    echo ""
    echo "🌐 Opening browser session..."
    echo "URL: http://localhost:8000"
    echo ""
    echo "📋 You can now test the UI with these credentials:"
    echo "   Email: test@vmart.co.in"
    echo "   Name: Test User"
    echo ""
    
    # Check if index.html has VERSION 3.0
    echo "🔍 Checking if VERSION 3.0 is loaded..."
    curl -s -b cookies.txt http://localhost:8000 | grep -q "VERSION: 3.0" && \
        echo "✅ VERSION 3.0 detected!" || \
        echo "❌ VERSION 3.0 NOT found - cache issue!"
    
    echo ""
    echo "🧪 To test manually:"
    echo "1. Open http://localhost:8000 in browser"
    echo "2. Login with: test@vmart.co.in / Test User"
    echo "3. Open DevTools Console (Cmd+Option+J)"
    echo "4. Look for 'VERSION: 3.0'"
    
else
    echo "❌ Login failed!"
fi

rm -f cookies.txt
