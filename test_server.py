#!/usr/bin/env python3
"""
Quick test server for V-Mart Retail Intelligence QA
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask
from web.intelligence_routes import intelligence_bp

app = Flask(__name__)
app.secret_key = 'test-secret-key-for-qa'

# Register the intelligence blueprint
app.register_blueprint(intelligence_bp)

@app.route('/')
def index():
    return {
        "status": "online",
        "system": "V-Mart Retail Intelligence System",
        "endpoints": [
            "POST /api/intelligence/chat",
            "POST /api/intelligence/sales/analyze",
            "POST /api/intelligence/sales/forecast",
            "POST /api/intelligence/inventory/forecast",
            "POST /api/intelligence/fashion/trends",
            "POST /api/intelligence/data/upload",
        ]
    }

if __name__ == '__main__':
    print("🚀 Starting V-Mart Retail Intelligence Test Server...")
    print("📍 Server running on http://localhost:5001")
    print("📊 Testing all retail intelligence endpoints")
    app.run(host='0.0.0.0', port=5001, debug=False)
